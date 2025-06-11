from flask import Flask, jsonify, request
from flask_cors import CORS
from update_arbs import refresh_arbs, create_table
import sqlite3
import threading
import time

app = Flask(__name__)
CORS(app)

def get_db_connection():
    conn = sqlite3.connect('arbs.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/api/arbs', methods=['GET'])
def get_arbs():
    bookmakers = request.args.getlist('bookmakers')
    conn = get_db_connection()
    
    if bookmakers:
        # Create a parameterized query for multiple bookmakers
        placeholders = ','.join(['?'] * len(bookmakers))
        query = f"""
            SELECT * FROM arbs 
            WHERE EXISTS (
                SELECT 1 FROM json_each(outcomes) 
                WHERE json_extract(value, '$.bookmaker') IN ({placeholders})
            )
        """
        arbs = conn.execute(query, bookmakers).fetchall()
    else:
        arbs = conn.execute('SELECT * FROM arbs').fetchall()
    
    conn.close()
    return jsonify([dict(arb) for arb in arbs])

def background_refresh():
    while True:
        refresh_arbs()
        time.sleep(120)  # Refresh every 2 minutes

if __name__ == '__main__':
    create_table()  # Create table before starting
    refresh_thread = threading.Thread(target=background_refresh)
    refresh_thread.daemon = True
    refresh_thread.start()
    app.run(debug=True, port=5000) 