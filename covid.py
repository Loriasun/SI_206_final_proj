
import requests
import sqlite3
from covid19dh import covid19

def CreateDB(db_name):
    name = f'{db_name}.db'
    conn = sqlite3.connect(name)
    cur = conn.cursor()
    return cur, conn 

def get_Case_Death_By_Country(cur,conn):

    matches = soup.find('div', {'class':'external-html'})
    rows = matches.find_all('strong') 
    row_cells = row.find_all('span')
    print(rows) 
    cur.execute('CREATE TABLE IF NOT EXISTS Case_Death_By_Country (Country TEXT PRIMARY KEY, Case INTEGER, Death INTEGER)')
    cur.execute('SELECT MAX(Case) FROM Case_Death_By_Country')
    cur.execute('SELECT MAX(Death) FROM Case_Death_By_Country')

    temp = cur.fetchone()[0]
    if not temp:
        index = 0
    else:
        index = int(temp)
    for i in range(len(page['value']))[index:]:
        key = row_cells[0].text.strip()
        case = row_cells[2].text.strip()
        death = row_cells[2].text.strip()
        
        cur.execute('INSERT OR IFNORE INTO Case_Death_By_Country (Country, Case, Death) VALUES (?,?,?)',
            (i+1, country, Case, Death)) 
        index += 1
        if(index % 25 == 0):
            break
    conn.commit()


def main():
    cur, conn = CreateDB("covid.db")
    get_Case_Death_By_Country(cur, conn)

if __name__ == "__main__":
    main()



