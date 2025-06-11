from flask import Flask, request, jsonify
from flask_cors import CORS
from arb_detector import *
from models import *
import sqlite3
import json
from apscheduler.schedulers.background import BackgroundScheduler
from update_arbs import refresh_arbs

app = Flask(__name__)
CORS(app)  # This enables CORS for all routes

API_KEY = "b1112544946fe651cbb564457f73464c"
REGIONS = ["us"]    # us = American sportsbooks
MARKETS = ["h2h", "spreads"]   # h2h = moneyline (win/lose)
BOOKMAKERS = []
SPORTS = ["basketball_nba", "baseball_mlb"] #for testing, exclude NFL, it's too much. 
# SPORTS = ["basketball_nba", "americanfootball_nfl", "baseball_mlb"] 


# Background Listings
scheduler = BackgroundScheduler()
scheduler.add_job(func=refresh_arbs, trigger="interval", minutes=10)
scheduler.start()

@app.route('/api/listings', methods=['GET'])
def listings():
    # these are the default settings but they can be overridden by the user with filters
    # odds = fetch_odds_for_sports(API_KEY, REGIONS, MARKETS, BOOKMAKERS, SPORTS)
    # arbitrage_opps = get_arbitrage_opps(odds)
    # return jsonify(arbitrage_opps) 
    # ^^^ Update on frontend, per reload. 
    conn = sqlite3.connect('arbs.db')
    c = conn.cursor()
    c.execute("SELECT event, outcomes, profit_margin, timestamp FROM arbs ORDER BY profit_margin DESC")
    rows = c.fetchall()
    conn.close()

    result = []
    for event, outcomes, margin, timestamp in rows:
        result.append({
            'event': event,
            'outcomes': json.loads(outcomes),
            'profit_margin': margin,
            'timestamp': timestamp
        })
    return jsonify(result)

if __name__ == "__main__":
    refresh_arbs()
    create_table()
    app.run(debug=True, port=5001)
