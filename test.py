import requests
import time
import json
import sqlite3
import csv

# conn = sqlite3.connect('206_final.db')
# cur = conn.cursor()
# cur.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='Air_Pollution_Category' ''')
# print(cur.fetchone()[0])

Details = ['Name', 'class', 'passoutYear', 'subject']  
rows = [ ['sushma', '2nd', '2023', 'Physics'],  ['john', '3rd', '2022', 'M2'],  ['kushi', '4th', '2021', 'M4']] 
with open('student.csv', 'w') as f: 
    write = csv.writer(f) 
    write.writerow(Details) 
    write.writerows(rows)