from bs4 import BeautifulSoup
import sqlite3
import requests
import matplotlib.pyplot as plt
import os
import numpy as np


def CreateDB(db_name):
    name = f'{db_name}'
    conn = sqlite3.connect(name)
    cur = conn.cursor()
    return cur, conn 

def create_covid_table(cur, conn):
    cur.execute('CREATE TABLE IF NOT EXISTS covid (Country TEXT PRIMARY KEY, Cases NUMBER, Deaths Number, Region TEXT )')
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


def covid_bar_chart(cur,conn):
    cur.execute('SELECT Regions, Deaths,COUNT(*) FROM covid')
    conn.commit()

    temp = []
    values = []
    dict = {}
    for t in cur.fetchall():
        temp.append(t[0])
        values.append(t[1])
        dict[t[0]] = t[1]

    objects = tuple(temp)
    y_pos = np.arange(len(objects))

    plt.barh(y_pos,values,align='center',alpha=1)
    plt.yticks(y_pos,objects)
    plt.xlabel('Number of Deaths')
    plt.title('Regions')

    plt.show()
    return dict



def main():
    cur, conn = CreateDB("covid.db")
    create_covid_table(cur,conn)
    add_covid(cur, conn)

if __name__ == "__main__":
    main()




