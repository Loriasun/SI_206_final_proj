import requests
import time
import json
import sqlite3

conn = sqlite3.connect('206_final.db')
cur = conn.cursor()
cur.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='Air_Pollution_Category' ''')
print(cur.fetchone()[0])
