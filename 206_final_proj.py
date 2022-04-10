import requests
import time
import json
import sqlite3
import os
# for i in range(10):
#     print(i)

#     time.sleep(3)
# data = requests.get('https://api.covidtracking.com/v1/us/20200502.json').json()

def CreateDB(db_name):
    name = f'{db_name}.db'
    conn = sqlite3.connect(name)
    cur = conn.cursor()
    return cur, conn 
    
def air_pollution_death(cur,conn):
    data = requests.get('https://ghoapi.azureedge.net/api/AIR_4').json()
    with open('air_pollution.json','w') as f:
        json.dump(data,f,indent=4)
    cur.execute('DROP TABLE IF EXISTS Air_Pollution_Death')
    cur.execute('CREATE TABLE Air_pollution_Death (ID NUMBER PRIMARY KEY, Country TEXT, Cause_ID TEXT, GENDER TEXT, Number of Death NUMBER)')
    conn.commit()
    id = 0
    count = 0
    index = 0
    for index in range(len(data)):
        id += 1
        country = data['SpatialDim']
        cid = data['Dim2']
        g = data['Dim1']
        num = data['NumericValue']
        cur.execute('INSERT INTO Air_Pollution_Death (ID, Country, Cause_ID, GENDER, Number of Death) VALUES (?,?,?,?,?)',
            (id, country, cid, g, num))
        conn.commit()
        
    

def COVID_API(cur,conn):
# def COVID_API():
    cur.execute('DROP TABLE IF EXISTS COVID_TEST')
    cur.execute('CREATE TABLE COVID_TEST (Date NUMBER PRIMARY KEY, Positive NUMBER, Negative NUMBER, Currently_Hospitalized NUMBER,Cumulative_Hospitalized NUMBER)')
    conn.commit()
    
    # cur.execute('DROP TABLE IF EXISTS COVID_TEST')
    # cur.execute('CREATE TABLE COVID_TEST (Date NUMBER PRIMARY KEY, Positive NUMBER, Negative NUMBER)')
    # conn.commit()

    for mon in range(13)[3:]: 
        for day in range(30)[1:]:
            req_date = f'2020'
            if( mon < 10):
                req_date +=f'0{mon}'
            else:
                req_date += f'{mon}'
            if(day < 10):
                req_date +=f'0{day}'
            else:
                req_date +=f'{day}'
            # print(req_date)
            req = f'https://api.covidtracking.com/v1/us/{req_date}.json'
            # print(req)
            data = requests.get(req).json()
            # print(data)

            date = data['date']
            num_pos = data['positive']
            num_neg = data['negative']
            cur_hos = data['hospitalizedCurrently']
            accu_hos = data['hospitalizedCumulative']
            cur.execute('INSERT INTO COVID_TEST (Date , Positive , Negative ,Currently_Hospitalized, Cumulative_Hospitalized) VALUES (?,?,?,?,?)',
                (date, num_pos, num_neg,cur_hos, accu_hos))
            conn.commit()
            
            
        

    

def main():
    db_name = '206_final'
    cur, conn = CreateDB(db_name)
    COVID_API(cur, conn)
    
    # COVID_API()
if __name__ == '__main__':
    main()