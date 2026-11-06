import logging
import os
import time

import requests
from dotenv import load_dotenv

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

REQUEST_TIMEOUT = 10


def get_api_key():
    """Return the Odds API key, or exit if ODDS_API_KEY is missing."""
    load_dotenv()
    key = os.getenv("ODDS_API_KEY", "").strip()
    if not key:
        raise SystemExit(
            "Error: ODDS_API_KEY is not set. "
            "Copy .env.example to .env and set ODDS_API_KEY to your Odds API key."
        )
    return key


REGIONS = ["us"]  # us = American sportsbooks
MARKETS = ["h2h", "spreads"]  # h2h = moneyline (win/lose)
BOOKMAKERS = []
SPORTS = ["basketball_nba", "americanfootball_nfl", "baseball_mlb"]


def _csv(value):
    if isinstance(value, (list, tuple)):
        return ",".join(value)
    return value


def fetch_odds(sport, api_key=None, regions=None, markets=None, bookmakers=None):
    """Fetch odds for one sport from The Odds API.

    sport is an Odds API sport key such as "basketball_nba".
    Returns the parsed JSON body, or None if the request failed.
    """
    if api_key is None:
        api_key = get_api_key()
    if regions is None:
        regions = REGIONS
    if markets is None:
        markets = MARKETS
    if bookmakers is None:
        bookmakers = BOOKMAKERS

    url = f"https://api.the-odds-api.com/v4/sports/{sport}/odds"
    params = {"apiKey": api_key}
    if regions:
        params["regions"] = _csv(regions)
    if markets:
        params["markets"] = _csv(markets)
    if bookmakers:
        params["bookmakers"] = _csv(bookmakers)

    try:
        response = requests.get(url, params=params, timeout=REQUEST_TIMEOUT)
    except requests.exceptions.RequestException as exc:
        logger.error("Network error fetching odds for %s: %s", sport, exc)
        return None

    if response.status_code != 200:
        logger.error(
            "Odds API returned HTTP %s for %s: %s",
            response.status_code,
            sport,
            response.text[:300],
        )
        return None

    try:
        return response.json()
    except ValueError as exc:
        logger.error("Odds API returned invalid JSON for %s: %s", sport, exc)
        return None


def fetch_odds_for_sports(api_key, regions, markets, bookmakers, sports):
    """Fetch odds for each sport. Returns None if every request failed."""
    all_odds = []
    any_success = False

    for sport_key in sports:
        data = fetch_odds(sport_key, api_key, regions, markets, bookmakers)
        if data is None:
            time.sleep(0.75)
            continue

        any_success = True
        if isinstance(data, list) and data:
            for event in data:
                event["sport_key"] = sport_key
            all_odds.extend(data)
            print(f"✅ Retrieved odds for: {sport_key} ({len(data)} events)")
        else:
            print(f"⚠️ No odds found for: {sport_key}")

        time.sleep(0.75)

    if not any_success:
        return None
    return all_odds


def _line(outcome):
    point = outcome.get("point")
    if point is None:
        return None
    return abs(float(point))


def detect_arbitrage(event):
    """Return arbitrage opportunities for one event, one per market.

    Decimal odds convert to implied probability as 1/odds. Moneylines and
    spreads are scored separately, and a spread is only compared with the
    same point. Within a market, keep the best price per outcome. An arb
    exists when those implied probabilities sum to less than 1. The profit
    margin is 1 minus that sum, returned as a percentage.
    """
    groups = {}
    for bookmaker in event.get("bookmakers", []):
        for market in bookmaker.get("markets", []):
            market_key = market.get("key") or "h2h"
            for outcome in market.get("outcomes", []):
                group = groups.setdefault((market_key, _line(outcome)), {})
                name = outcome["name"]
                price = outcome["price"]
                current = group.get(name)
                if current is None or price > current["price"]:
                    picked = {
                        "bookmaker": bookmaker["title"],
                        "price": price,
                        "market": market_key,
                    }
                    if outcome.get("point") is not None:
                        picked["point"] = outcome["point"]
                    group[name] = picked

    found = []
    for outcomes in groups.values():
        if len(outcomes) < 2:
            continue
        implied_prob_sum = sum(1 / o["price"] for o in outcomes.values())
        if implied_prob_sum < 1:
            found.append({
                "event": event["home_team"] + " vs " + event["away_team"],
                "outcomes": outcomes,
                "implied_prob": implied_prob_sum,
                "profit_margin": round((1 - implied_prob_sum) * 100, 2),
                "sport": event["sport_key"],
            })
    return found


def calculate_stakes(total_stake, odds):
    """Split a total stake across outcomes so each pays out the same amount.

    For a total stake S, the stake on outcome i is
    S * (1/odds_i) / sum_of_implied_probs. Stakes are returned in the same
    order as odds.
    """
    implied = [1 / price for price in odds]
    implied_sum = sum(implied)
    return [total_stake * probability / implied_sum for probability in implied]


def get_arbitrage_opps(data):
    """Collect arbitrage opportunities from a list of Odds API events.

    Each market is checked on its own: best price per outcome, implied
    probability 1/odds, and an arb only when those probabilities sum to
    less than 1.
    """
    arbitrage_opps = []
    for event in data:
        arbitrage_opps.extend(detect_arbitrage(event))
    return arbitrage_opps


def main():
    data = fetch_odds_for_sports(get_api_key(), REGIONS, MARKETS, BOOKMAKERS, SPORTS)

    if data is None:
        print("Error: could not fetch odds.")
        return

    if not isinstance(data, list):
        print("Error: API did not return a list of events.")
        print("Full response:", data)
        return

    arbitrage_opps = get_arbitrage_opps(data)
    if arbitrage_opps:
        print(arbitrage_opps[0])

    count = 0
    for event in data:
        for arb in detect_arbitrage(event):
            count += 1
            print("\n💰 Arbitrage Found!")
            print(f"Match: {arb['event']}")
            print(f"Profit Margin: {arb['profit_margin']}%")
            for team, details in arb["outcomes"].items():
                point = details.get("point")
                side = team if point is None else f"{team} {point}"
                print(f"  Bet on {side} at {details['bookmaker']} (odds: {details['price']})")

    print(f"\n{count} events found!")


if __name__ == "__main__":
    main()
