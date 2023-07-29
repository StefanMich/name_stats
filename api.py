# create flask api that fetches all entries with a given name from the database and returns as json
from collections import defaultdict

from flask import (
    Flask,
    jsonify,
    render_template,
)
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
app.config.from_prefixed_env()
print(app.config.get('ENV'))
if app.config.get('ENV') == 'production':
    app.config['API_URL'] = 'https://name-stats.onrender.com/stats/eny'
else:
    app.config['API_URL'] = 'http://127.0.0.1:8000/stats/eny'
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


@app.route('/app')
def get_app():
    return render_template('name.html')
