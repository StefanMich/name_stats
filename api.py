# create flask api that fetches all entries with a given name from the database and returns as json
from collections import defaultdict

from flask import Flask, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

@app.route('/stats/<name>')
def get_name(name):
    with sqlite3.connect('names.db') as con:
        cursor = con.execute('SELECT DISTINCT name, count, year FROM names WHERE name = ? COLLATE NOCASE', (name,))
        rows = cursor.fetchall()

        name_stats = defaultdict(list)
        for name, count, year in rows:
            name_stats[name].append((year, count))
        return jsonify(name_stats)
