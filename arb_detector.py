import os
import time

import requests
from dotenv import load_dotenv


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


def fetch_odds(sport, api_key=None, regions=None, markets=None, bookmakers=None):
    """Fetch odds for one sport from The Odds API.

    sport is an Odds API sport key such as "basketball_nba".
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
        params["regions"] = regions
    if markets:
        params["markets"] = ",".join(markets)
    if bookmakers:
        params["bookmakers"] = ",".join(bookmakers)

    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()


def fetch_odds_for_sports(api_key, regions, markets, bookmakers, sports):
    all_odds = []

    for sport_key in sports:
        try:
            data = fetch_odds(sport_key, api_key, regions, markets, bookmakers)
            if isinstance(data, list) and data:
                for event in data:
                    event["sport_key"] = sport_key
                all_odds.extend(data)
                print(f"✅ Retrieved odds for: {sport_key} ({len(data)} events)")
            else:
                print(f"⚠️ No odds found for: {sport_key}")
        except requests.exceptions.RequestException as e:
            print(f"❌ Error fetching odds for {sport_key}: {e}")

        time.sleep(0.75)

    return all_odds


def detect_arbitrage(event):
    outcomes = {}

    for bookmaker in event["bookmakers"]:
        for market in bookmaker["markets"]:
            for outcome in market["outcomes"]:
                name = outcome["name"]
                price = outcome["price"]
                if name not in outcomes or price > outcomes[name]["price"]:
                    outcomes[name] = {
                        "bookmaker": bookmaker["title"],
                        "price": price,
                    }

    if len(outcomes) < 2:
        return None

    implied_prob_sum = sum(1 / o["price"] for o in outcomes.values())

    if implied_prob_sum < 1:
        return {
            "event": event["home_team"] + " vs " + event["away_team"],
            "outcomes": outcomes,
            "implied_prob": implied_prob_sum,
            "profit_margin": round((1 - implied_prob_sum) * 100, 2),
            "sport": event["sport_key"],
        }
    return None


def get_arbitrage_opps(data):
    arbitrage_opps = []
    for event in data:
        arb = detect_arbitrage(event)
        if arb:
            arbitrage_opps.append(arb)
    return arbitrage_opps


def main():
    data = fetch_odds_for_sports(get_api_key(), REGIONS, MARKETS, BOOKMAKERS, SPORTS)

    if not isinstance(data, list):
        print("Error: API did not return a list of events.")
        print("Full response:", data)
        return

    arbitrage_opps = get_arbitrage_opps(data)
    if arbitrage_opps:
        print(arbitrage_opps[0])

    count = 0
    for event in data:
        arb = detect_arbitrage(event)
        if arb:
            count += 1
            print("\n💰 Arbitrage Found!")
            print(f"Match: {arb['event']}")
            print(f"Profit Margin: {arb['profit_margin']}%")
            for team, details in arb["outcomes"].items():
                print(f"  Bet on {team} at {details['bookmaker']} (odds: {details['price']})")

    print(f"\n{count} events found!")


if __name__ == "__main__":
    main()
