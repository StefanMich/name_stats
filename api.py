# create flask api that fetches all entries with a given name from the database and returns as json
from collections import defaultdict

from flask import (
    jsonify,
    render_template,
)
import sqlite3

from app import app


@app.route('/stats/')
def get_all_stats():
    with sqlite3.connect(app.config['DB']) as con:
        cursor = con.execute('SELECT name, count, year FROM names')
        rows = cursor.fetchall()

        name_stats = defaultdict(list)
        for name, count, year in rows:
            name_stats[name].append((year, count))
        return jsonify(name_stats)


@app.route('/stats/<name>')
def get_name(name):
    with sqlite3.connect(app.config['DB']) as con:
        cursor = con.execute('SELECT DISTINCT name, count, year FROM names WHERE name = ? COLLATE NOCASE', (name,))
        rows = cursor.fetchall()

        name_stats = defaultdict(list)
        for name, count, year in rows:
            name_stats[name].append((year, count))
        return jsonify(name_stats)


@app.route('/')
def get_app():
    return render_template('name.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
