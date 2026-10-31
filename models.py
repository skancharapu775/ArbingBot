# backend/models.py
import sqlite3


def create_table():
    conn = sqlite3.connect("arbs.db")
    c = conn.cursor()
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS arbs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event TEXT,
            outcomes TEXT,
            profit_margin REAL,
            sport TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            fetched_at TEXT
        )
        """
    )
    columns = {row[1] for row in c.execute("PRAGMA table_info(arbs)")}
    if "fetched_at" not in columns:
        c.execute("ALTER TABLE arbs ADD COLUMN fetched_at TEXT")
    conn.commit()
    conn.close()
