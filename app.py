from flask import Flask, request, jsonify
from flask_cors import CORS
from arb_detector import *
from models import *
import sqlite3
import json
from apscheduler.schedulers.background import BackgroundScheduler
from update_arbs import refresh_arbs
import requests
import time
from datetime import datetime

app = Flask(__name__)
CORS(app)  # This enables CORS for all routes

@app.route('/', defaults={'path': ''}, methods=['OPTIONS'])
@app.route('/<path:path>', methods=['OPTIONS'])
def handle_options(path):
    return '', 200

API_KEY = "a80d02c6475d4516feb8202d5196f03b"
REGIONS = ["us"]    # us = American sportsbooks
MARKETS = ["h2h", "spreads"]   # h2h = moneyline (win/lose)
BOOKMAKERS = []
SPORTS = ["basketball_nba", "baseball_mlb"]
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

    results = []
    for event, outcomes, margin, sport, timestamp in rows:
        results.append({
            'event': event,
            'outcomes': json.loads(outcomes),
            'profit_margin': margin,
            'sport': sport,
            'timestamp': timestamp
        })
    print(results)
    return jsonify(results)
    

@app.route('/api/bookmakerlistings', methods=['GET'])
def bookmakerlistings():
    bookmakers = request.args.get('bookmakers', '').split(',')
    print("Received bookmakers:", bookmakers)
    data = fetch_odds_for_sports(API_KEY, REGIONS, MARKETS, bookmakers, SPORTS)
    print("Fetched odds data length:", len(data) if isinstance(data, list) else "Not a list")
    arbs = get_arbitrage_opps(data)
    print("Generated arbs length:", len(arbs) if isinstance(arbs, list) else "Not a list")

    results = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for arb in arbs:
        results.append({
            'event': arb['event'],
            'outcomes': arb['outcomes'],
            'profit_margin': arb['profit_margin'],
            'sport': arb['sport'],
            'timestamp': current_time
        })
    print("Processed results length:", len(results))
    return jsonify(results)

if __name__ == "__main__":
    create_table()
    refresh_arbs()
    app.run(debug=True, port=5001)
