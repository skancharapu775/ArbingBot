import os
import time

import pandas as pd
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


REGIONS = ["us"]    # us = American sportsbooks
MARKETS = ["h2h", "spreads"]   # h2h = moneyline (win/lose)
BOOKMAKERS = []
SPORTS = ["basketball_nba", "americanfootball_nfl", "baseball_mlb"] 

# Replace with actual sport keys, or upcoming for all sports

def fetch_odds_for_sports(api_key, regions, markets, bookmakers, sports):
    all_odds = []

    for sport_key in sports:
        url = f"https://api.the-odds-api.com/v4/sports/{sport_key}/odds"

        params = {"apiKey": api_key}
        
        # If empty, don't add the parameter
        if regions:
            params["regions"] = regions
        if markets:
            params["markets"] = ",".join(markets)
        if bookmakers:
            params["bookmakers"] = ",".join(bookmakers)

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            if isinstance(data, list) and data:
                # Add sport_key to each event
                for event in data:
                    event['sport_key'] = sport_key
                all_odds.extend(data)
                print(f"✅ Retrieved odds for: {sport_key} ({len(data)} events)")
            else:
                print(f"⚠️ No odds found for: {sport_key}")

        except requests.exceptions.RequestException as e:
            print(f"❌ Error fetching odds for {sport_key}: {e}")
        
        time.sleep(0.75)

    return all_odds

def fetch_odds():
    url = f"https://api.the-odds-api.com/v4/sports/{SPORT}/odds" # toggle sport and sport keys
    params = {
        "apiKey": get_api_key(),
        "regions": REGIONS,
        "markets": MARKETS,
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data

def get_all_bookmakers():
    sports_url = f"https://api.the-odds-api.com/v4/sports"
    sports = requests.get(sports_url, params={"apiKey": get_api_key()}).json()

    all_bookmakers = []  # List of (key, title) tuples
    for sport in sports:
        odds_url = f"https://api.the-odds-api.com/v4/sports/{sport['key']}/odds"
        params = {"apiKey": get_api_key(), "regions": "us,us2,eu,uk,au"}
    return all_bookmakers

def detect_arbitrage(event):
    outcomes = {}

    for bookmaker in event['bookmakers']:
        for market in bookmaker['markets']:
            for outcome in market['outcomes']:
                name = outcome['name']
                price = outcome['price']
                if name not in outcomes or price > outcomes[name]['price']:
                    outcomes[name] = {
                        'bookmaker': bookmaker['title'],
                        'price': price
                    }

    if len(outcomes) < 2:
        return None  # Skip if incomplete data

    implied_prob_sum = sum(1 / o['price'] for o in outcomes.values())

    if implied_prob_sum < 1:
        return {
            "event": event['home_team'] + " vs " + event['away_team'],
            "outcomes": outcomes,
            "implied_prob": implied_prob_sum,
            "profit_margin": round((1 - implied_prob_sum) * 100, 2),
            "sport": event['sport_key']  # Add the sport key from the event
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
    data = get_all_bookmakers()
    '''
    data = fetch_odds_for_sports(API_KEY, REGIONS, MARKETS, BOOKMAKERS, SPORTS)

    if not isinstance(data, list):
        print("Error: API did not return a list of events.")
        print("Full response:", data)
        return

    arbitrage_opps = get_arbitrage_opps(data)

    print(arbitrage_opps[0])

    count = 0
    for event in data:
        arb = detect_arbitrage(event)
        if arb:
            count += 1
            print("\n💰 Arbitrage Found!")
            print(f"Match: {arb['event']}")
            print(f"Profit Margin: {arb['profit_margin']}%")
            for team, details in arb['outcomes'].items():
                print(f"  Bet on {team} at {details['bookmaker']} (odds: {details['price']})")
    
    print(f"\n{count} events found!")
    '''

if __name__ == "__main__":
    main()