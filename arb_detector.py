import requests
import pandas as pd
import time

API_KEY = "4ea69ca031077470df2fe2b8e1b33b72"
REGIONS = ["us"]    # us = American sportsbooks
MARKETS = ["h2h", "spreads"]   # h2h = moneyline (win/lose)
BOOKMAKERS = []
SPORTS = ["basketball_nba", "americanfootball_nfl", "baseball_mlb"] 

# Replace with actual sport keys, or upcoming for all sports

def fetch_odds_for_sports():
    all_odds = []

    for sport_key in SPORTS:
        url = f"https://api.the-odds-api.com/v4/sports/{sport_key}/odds"

        params = {"apiKey": API_KEY}
        
        # Conditionally add optional parameters if they are not empty
        if REGIONS:
            params["regions"] = REGIONS
        if MARKETS:
            params["markets"] = ",".join(MARKETS)
        if BOOKMAKERS:
            params["bookmakers"] = ",".join(BOOKMAKERS)

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            if isinstance(data, list) and data:
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
        "apiKey": API_KEY,
        "regions": REGIONS,
        "markets": MARKETS,
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data

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
            "profit_margin": round((1 - implied_prob_sum) * 100, 2)
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
    data = fetch_odds_for_sports()

    if not isinstance(data, list):
        print("Error: API did not return a list of events.")
        print("Full response:", data)
        return

    arbitrage_opps = get_arbitrage_opps(data)

    print(arbitrage_opps[0])

    '''
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