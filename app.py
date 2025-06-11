from flask import Flask, request, jsonify
from flask_cors import CORS
from arb_detector import *

app = Flask(__name__)
CORS(app)  # This enables CORS for all routes

API_KEY = "4ea69ca031077470df2fe2b8e1b33b72"
REGIONS = ["us"]    # us = American sportsbooks
MARKETS = ["h2h", "spreads"]   # h2h = moneyline (win/lose)
BOOKMAKERS = []
SPORTS = ["basketball_nba", "baseball_mlb"] #for testing, exclude NFL, it's too much. 
# SPORTS = ["basketball_nba", "americanfootball_nfl", "baseball_mlb"] 

@app.route('/api/listings', methods=['GET'])
def listings():
    # these are the default settings but they can be overridden by the user with filters
    odds = fetch_odds_for_sports(API_KEY, REGIONS, MARKETS, BOOKMAKERS, SPORTS)
    arbitrage_opps = get_arbitrage_opps(odds)
    return jsonify(arbitrage_opps)

if __name__ == "__main__":
    app.run(debug=True, port=5001)
