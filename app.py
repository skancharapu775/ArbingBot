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

API_KEY = "864f7d3a85ed040365fe9fc446902e79"
REGIONS = ["us"]    # us = American sportsbooks
MARKETS = ["h2h", "spreads"]   # h2h = moneyline (win/lose)
BOOKMAKERS = []
SPORTS = ["basketball_nba", "baseball_mlb"] #for testing, exclude NFL, it's too much. 
# SPORTS = ["basketball_nba", "americanfootball_nfl", "baseball_mlb"] 


# Background Listings
scheduler = BackgroundScheduler()
scheduler.add_job(func=refresh_arbs, trigger="interval", minutes=5)
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
    c.execute("SELECT event, outcomes, profit_margin, sport, timestamp FROM arbs ORDER BY profit_margin DESC")
    rows = c.fetchall()
    conn.close()

    result = []
    for event, outcomes, margin, sport, timestamp in rows:
        result.append({
            'event': event,
            'outcomes': json.loads(outcomes),
            'profit_margin': margin,
            'sport': sport,
            'timestamp': timestamp
        })
    return jsonify(result)

@app.route('/api/bookmakerlistings', methods=['GET'])
def bookmakerlistings():
    # bookmakers = ["betmgm", "betonlineag", "betrivers", "betus", "bovada", "caesars" "draftkings", "fanduel", "fanatics","lowvig", "mybookieag"]
    BOOKMAKERS = request.args.get('bookmakers')
    data = fetch_odds_for_sports(API_KEY, REGIONS, MARKETS, BOOKMAKERS, SPORTS)
    arbs = get_arbitrage_opps(data)
    return jsonify(arbs)

if __name__ == "__main__":
    create_table()
    refresh_arbs()
    app.run(debug=True, port=5001)
