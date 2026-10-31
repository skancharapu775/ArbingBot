# backend/update_arbs.py
import json
import logging
import sqlite3
from datetime import datetime, timezone

from arb_detector import *
from models import create_table

logger = logging.getLogger(__name__)

REGIONS = ["us"]  # us = American sportsbooks
MARKETS = ["h2h", "spreads"]  # h2h = moneyline (win/lose)
BOOKMAKERS = []
SPORTS = ["basketball_nba", "baseball_mlb"]  # NFL is omitted; it is a much larger feed.


def save_to_db(arbs):
    """Replace stored opportunities in one transaction.

    Readers keep seeing the previous rows until the delete and inserts commit
    together. A failure rolls the whole write back.
    """
    create_table()
    conn = sqlite3.connect("arbs.db")
    try:
        with conn:
            conn.execute("DELETE FROM arbs")
            conn.executemany(
                """
                INSERT INTO arbs (event, outcomes, profit_margin, sport, timestamp, fetched_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                [
                    (
                        arb["event"],
                        json.dumps(arb["outcomes"]),
                        arb["profit_margin"],
                        arb["sport"],
                        arb["fetched_at"],
                        arb["fetched_at"],
                    )
                    for arb in arbs
                ],
            )
    finally:
        conn.close()


def refresh_arbs():
    create_table()
    data = fetch_odds_for_sports(get_api_key(), REGIONS, MARKETS, BOOKMAKERS, SPORTS)
    if data is None:
        logger.error("Odds fetch failed; existing arbitrage rows were left unchanged.")
        return

    fetched_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    arbs = get_arbitrage_opps(data)
    for arb in arbs:
        arb["fetched_at"] = fetched_at
    save_to_db(arbs)


if __name__ == "__main__":
    refresh_arbs()
