# ArbingBot

ArbingBot finds sports-betting arbitrage. It compares odds across sportsbooks and lists games where you can bet every outcome and lock in a profit if the prices are out of line with each other.

It does not place bets. It only detects opportunities and shows them in a web UI.

## Architecture

```
The Odds API → update_arbs.py → SQLite (arbs.db) → Flask /api/listings → React UI
```

1. **The Odds API** returns decimal odds for NBA and MLB from US sportsbooks.
2. **`update_arbs.py`** turns those odds into arbitrage opportunities. `app.py` runs this on startup and every 5 minutes.
3. **SQLite (`arbs.db`)** stores the latest opportunities. A refresh deletes and inserts in one transaction, so the API never serves a half-empty table. Each row has a `fetched_at` timestamp.
4. **Flask** serves `GET /api/listings` on port 5001. The bookmaker filter uses `GET /api/bookmakerlistings`, which asks the Odds API again instead of reading the cache.
5. **React** (Vite) loads `/api/listings` and renders one card per opportunity.

## Arbitrage math

Decimal odds convert to an implied probability with `1 / odds`. A price of 2.00 means 0.50.

For each outcome, keep the best (highest) odds across books. An arb exists when the sum of those implied probabilities is less than 1. The profit margin is `1 - sum`.

Example: best prices 2.00 and 2.50.

- Implied probabilities: `1/2.00 + 1/2.50 = 0.50 + 0.40 = 0.90`
- Profit margin: `1 - 0.90 = 0.10` (10%). The API field `profit_margin` is that value as a percentage.

For a total stake `S`, the stake on outcome `i` is `S * (1/odds_i) / sum_of_implied_probs`. On $100 in the example, that is about $55.56 at 2.00 and $44.44 at 2.50. `calculate_stakes` in `arb_detector.py` does this split. Both bets then return the same amount, so the profit does not depend on who wins.

## Setup

Python 3 and Node.js are required. The Odds API key is read from the environment, not from source.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
```

Edit `.env` and set `ODDS_API_KEY` to a key from [The Odds API](https://the-odds-api.com/). `.env` is gitignored. If the variable is missing, the Python scripts exit with an error instead of calling the API.

Fill the database, then start the API:

```bash
python update_arbs.py
python app.py
```

`app.py` listens on http://localhost:5001. Listings are at http://localhost:5001/api/listings.

Start the UI in another terminal:

```bash
cd frontend
npm install
npm run dev
```

The UI runs at http://localhost:5173.

## Tests

```bash
pytest
```

The tests cover an arbitrage, a market with no arbitrage, the case where implied probabilities sum to exactly 1, and the stake calculator. They do not call the Odds API.

## Limitations / lessons learned

Sportsbooks limit winning accounts. An account that only bets mispriced lines gets stake limits or is closed, so a detected arb is not the same as being able to get both bets on.

Opportunities go stale quickly. Odds move, and the rows in SQLite are only as fresh as the last refresh. A price that was profitable when it was fetched may be gone by the time both bets are placed.
