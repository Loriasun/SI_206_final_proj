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
    
def drop_table(cur, conn):
    cur.execute('DROP TABLE IF EXISTS covid')
    conn.commit()

def create_covid_table(cur, conn):
    cur.execute('CREATE TABLE IF NOT EXISTS covid (Country TEXT PRIMARY KEY, Cases INTEGER, Deaths INTEGER, Percentage FLOAT, Region TEXT )')
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
        case_b = temp[1].text
        case = int(case_b.replace(',', ''))
        death_b = temp[2].text
        death = int(death_b.replace(',', ''))
        region = temp[3].text
        percentage = death / case
        cur.execute(
            """
            INSERT OR IGNORE INTO covid (Country, Cases, Deaths, Percentage, Region)
            VALUES (?, ?, ?, ?)
            """,
            (country, case, death, percentage, region)
        )
    conn.commit()

def covid_bar_chart(cur,conn):
    cur.execute('SELECT Percentage, Country FROM covid LIMIT 10')
    conn.commit()

    temp = []
    values = []
    dict = {}
    for t in cur.fetchall():
        temp.append(t[0])
        values.append(t[3])
        dict[t[0]] = t[3]

    objects = tuple(temp)
    y_pos = np.arange(len(objects))
    fig1, ax1 = plt.subplots(figsize =(23,8))

    plt.barh(y_pos,values,align='center',alpha=1)
    plt.yticks(y_pos,objects)
    
    plt.xlabel('Country')
    plt.ylabel('Percent of Deaths')
    plt.title('Percent of Deaths by Country')
    plt.savefig('Percent_Deaths_by_Country_bar_chart.png')

    plt.show()
    return dict



def main():
    cur, conn = CreateDB("covid.db")
    drop_table(cur, conn)
    create_covid_table(cur,conn)
    add_covid(cur, conn)
    covid_bar_chart(cur, conn)

if __name__ == "__main__":
    main()




