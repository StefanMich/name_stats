#!/usr/bin/env python
from datetime import date
import re
import sqlite3

import requests as requests
from bs4 import BeautifulSoup

from api import app

url = 'https://www.dst.dk/da/Statistik/emner/borgere/navne/HvorMange?ajax=1'

name_count = requests.get(url, params={'firstName': 'eny',}, headers={'Accept': 'application/json'})
response_text = name_count.text
soup = BeautifulSoup(response_text, 'html.parser')


year = soup.div.div.table.find_all('tr')[0].find_all('th')[2]
assert year.text == str(date.today().year)

count = soup.div.div.table.find_all('tr')[1].find_all('td')[2]
name_text = soup.div.div.table.find_all('tr')[1].find_all('td')[0]
name = re.search(r'.*\'(\S+)\'', name_text.text).group(1)


with sqlite3.connect(app.config['DB']) as con:
    con.execute('CREATE TABLE IF NOT EXISTS names (name TEXT, count INTEGER, year INTEGER, creation_date DATETIME DEFAULT CURRENT_TIMESTAMP)')
    con.execute('INSERT INTO names (name, count, year) VALUES (?, ?, ?)', (name, count.text, year.text))

    print(con.execute('SELECT * FROM names').fetchall())
