from bs4 import BeautifulSoup
import sqlite3
import requests
import re
import unittest
import os
import csv

def CreateDB(db_name):
    name = f'{db_name}.db'
    conn = sqlite3.connect(name)
    cur = conn.cursor()
    return cur, conn 

def create_covid_table(cur, conn):
    cur.execute('CREATE TABLE IF NOT EXISTS covid (Country TEXT PRIMARY KEY, Case INTEGER, Death INTEGER)')
    conn.commit()

def add_covid(cur, conn):

    data = requests.get('https://www.worldometers.info/coronavirus/countries-where-coronavirus-has-spread')
    soup = BeautifulSoup(data.content, 'html.parser')
    matches = soup.find_all('tbody')
    for match in matches:
        data = match.find_all('tr')

    for item in data:
        temp = item.find_all('td')
        country = temp[0].text
        case = temp[1].text
        death = temp[2].text
        region = temp[3].text
        cur.execute(
            """
            INSERT OR IGNORE INTO covid (Country, Cases, Deaths, Region)
            VALUES (?, ?, ?, ?)
            """,
            (country, case, death, region)
        )
    conn.commit()



def main():
    cur, conn = CreateDB("covid.db")
    add_covid(cur, conn)

if __name__ == "__main__":
    main()



