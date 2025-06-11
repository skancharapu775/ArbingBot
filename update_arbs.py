# backend/update_arbs.py
import json
import sqlite3
from arb_detector import *

API_KEY = "b1112544946fe651cbb564457f73464c"
REGIONS = ["us"]    # us = American sportsbooks
MARKETS = ["h2h", "spreads"]   # h2h = moneyline (win/lose)
BOOKMAKERS = []
SPORTS = ["basketball_nba", "baseball_mlb"] #for testing, exclude NFL, it's too much. 

def save_to_db(arbs):
    conn = sqlite3.connect('arbs.db')
    c = conn.cursor()
    c.execute("DELETE FROM arbs")  # Optional: clear old entries

    for arb in arbs:
        c.execute('''
            INSERT INTO arbs (event, outcomes, profit_margin)
            VALUES (?, ?, ?)
        ''', (arb['event'], json.dumps(arb['outcomes']), arb['profit_margin']))
        #dumps turns the dict into json

    conn.commit()
    conn.close()

def refresh_arbs():
    # Your actual fetch config
    data = fetch_odds_for_sports(API_KEY, REGIONS, MARKETS, BOOKMAKERS, SPORTS)
    arbs = get_arbitrage_opps(data)
    save_to_db(arbs)

if __name__ == "__main__":
    refresh_arbs()
