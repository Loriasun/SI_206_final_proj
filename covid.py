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
            VALUES (?, ?, ?, ?,?)
            """,
            (country, case, death, percentage, region)
        )
    conn.commit()

def covid_Cases_bar_chart(cur,conn):
    cur.execute('SELECT Cases, Country FROM covid LIMIT 10')
    conn.commit()

    temp = []
    values = []
    # dict = {}
    for t in cur.fetchall():
        temp.append(t[0])
        values.append(t[1])   
    objects = tuple(values)
    y_pos = np.arange(len(objects))
    fig1, ax = plt.subplots(figsize =(23,8))
    ax.ticklabel_format(style='plain')
    plt.bar(y_pos,temp,align='center',alpha=1)
    plt.xticks(y_pos,objects)
    
    plt.xlabel('Country')
    plt.ylabel('Number of cases of Deaths')
    plt.title('Number of cases of Deaths by Country')
    plt.savefig('Cases_Deaths_by_Country_bar_chart.png')

def covid_Percentage_bar_chart(cur,conn):
    cur.execute('SELECT Percentage, Country FROM covid LIMIT 10')
    conn.commit()

    temp = []
    values = []
    # dict = {}
    for t in cur.fetchall():
        temp.append(t[0])
        values.append(t[1])
        
    objects = tuple(values)
    y_pos = np.arange(len(objects))
    fig1, ax = plt.subplots(figsize =(23,8))
    ax.ticklabel_format(style='plain')
    plt.bar(y_pos,temp,align='center',alpha=1)
    plt.xticks(y_pos,objects)
    
    plt.xlabel('Country')
    plt.ylabel('Percentage of Deaths')
    plt.title('Percentage of Deaths by Country')
    plt.savefig('Percentage_Deaths_by_Country_bar_chart.png')

   



def main():
    cur, conn = CreateDB("206_final.db")
    drop_table(cur, conn)
    create_covid_table(cur,conn)
    add_covid(cur, conn)
    covid_Cases_bar_chart(cur, conn)
    covid_Percentage_bar_chart(cur,conn)

if __name__ == "__main__":
    main()




