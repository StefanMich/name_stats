#!/usr/bin/env python
from datetime import date
import re
import sqlite3
from typing import Iterable

import requests as requests
from bs4 import BeautifulSoup

from app import app

url = 'https://www.dst.dk/da/Statistik/emner/borgere/navne/HvorMange?ajax=1'


def fetch_stats(name: str) -> Iterable[tuple[str, int, int]]:
    name_count = requests.get(
        url, params={'firstName': name, }, headers={'Accept': 'application/json'})
    response_text = name_count.text
    soup = BeautifulSoup(response_text, 'html.parser')

    rows = soup.div.div.table.find_all('tr')
    # fails if a name is used for more than one gender
    header = rows[0]
    name_rows = len(rows) - 1

    for column in [1, 2]:
        year_cell = header.find_all('th')[column]
        year = int(year_cell.text.replace('.', ''))

        total_count = 0

        for name_row in range(1, name_rows + 1):
            count_cell = rows[name_row].find_all('td')[column]
            count = int(count_cell.text.replace('.', ''))
            total_count += count

        yield name, total_count, year


def ensure_db() -> None:
    with sqlite3.connect(app.config['DB']) as con:
        con.execute('CREATE TABLE IF NOT EXISTS names (name TEXT, count INTEGER, year INTEGER, creation_date DATETIME DEFAULT CURRENT_TIMESTAMP)')


def store_stats(name: str, count: int, year: int) -> None:
    with sqlite3.connect(app.config['DB']) as con:
        con.execute('INSERT INTO names (name, count, year) '
                    'VALUES (?, ?, ?)', (name.upper(), count, year))


def get_all_stats() -> Iterable[tuple[str, int, int]]:
    with sqlite3.connect(app.config['DB']) as con:
        return con.execute('SELECT name, count, year FROM names').fetchall()


names = ['eny', 'stefan', 'katrine', 'alexander', 'peter', 'birthe', 'poul', 'tina', 'maja']


def store_all_stats() -> None:
    for name in names:
        for stat in fetch_stats(name):
            name, count, year = stat
            store_stats(name, count, year)


if __name__ == '__main__':
    ensure_db()
    store_all_stats()
    print(get_all_stats())
