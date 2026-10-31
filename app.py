import json
import sqlite3
from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, jsonify, request
from flask_cors import CORS

from arb_detector import *
from models import *
from update_arbs import refresh_arbs

app = Flask(__name__)
CORS(app)  # This enables CORS for all routes

@app.route('/', defaults={'path': ''}, methods=['OPTIONS'])
@app.route('/<path:path>', methods=['OPTIONS'])
def handle_options(path):
    return '', 200

REGIONS = ["us"]    # us = American sportsbooks
MARKETS = ["h2h", "spreads"]   # h2h = moneyline (win/lose)
BOOKMAKERS = []
SPORTS = ["basketball_nba", "baseball_mlb"]

# Background Listings
scheduler = BackgroundScheduler()
scheduler.add_job(func=refresh_arbs, trigger="interval", minutes=5)
scheduler.start()

@app.route('/api/listings', methods=['GET'])
def listings():
    conn = sqlite3.connect("arbs.db")
    c = conn.cursor()
    c.execute(
        """
        SELECT event, outcomes, profit_margin, sport, timestamp, fetched_at
        FROM arbs
        ORDER BY profit_margin DESC
        """
    )
    rows = c.fetchall()
    conn.close()

    results = []
    for event, outcomes, margin, sport, timestamp, fetched_at in rows:
        results.append({
            "event": event,
            "outcomes": json.loads(outcomes),
            "profit_margin": margin,
            "sport": sport,
            "timestamp": timestamp,
            "fetched_at": fetched_at,
        })
    return jsonify(results)
    

@app.route('/api/bookmakerlistings', methods=['GET'])
def bookmakerlistings():
    bookmakers = request.args.get('bookmakers', '').split(',')
    print("Received bookmakers:", bookmakers)
    data = fetch_odds_for_sports(get_api_key(), REGIONS, MARKETS, bookmakers, SPORTS)
    print("Fetched odds data length:", len(data) if isinstance(data, list) else "Not a list")
    if not isinstance(data, list):
        return jsonify([])
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
            'timestamp': current_time,
            'fetched_at': current_time
        })
    print("Processed results length:", len(results))
    return jsonify(results)

if __name__ == "__main__":
    get_api_key()
    create_table()
    refresh_arbs()
    app.run(debug=True, port=5001)
