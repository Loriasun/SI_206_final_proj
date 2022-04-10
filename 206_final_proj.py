# from types import NoneType
from re import S
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
def Drop_table(cur,conn):
    cur.execute('DROP TABLE IF EXISTS Air_Pollution_Death')
    cur.execute('DROP TABLE IF EXISTS COVID_TEST')
    conn.commit()
    
def Air_Pollution_Death(cur,conn):
    data = requests.get('https://ghoapi.azureedge.net/api/AIR_4').json()
    # with open('air_pollution.json','w') as f:
    #     json.dump(data,f,indent=4)
    cur.execute('CREATE TABLE IF NOT EXISTS Air_pollution_Death (ID NUMBER PRIMARY KEY, Country TEXT, Cause_ID TEXT, GENDER TEXT, Number_of_Death FLOAT)')
    cur.execute('SELECT MAX(ID) FROM Air_pollution_Death')
    # temp = type(cur.fetchone()[0])
    # print(temp)
    temp = cur.fetchone()[0]
    if not temp:
        index = 0
    else:
        # index = int(cur.fetchone()[0])
        index = int(temp)+1
    print(index)
    for i in range(len(data['value']))[index:]:
        country = data['value'][i]['SpatialDim']
        cid = data['value'][i]['Dim2']
        g = data['value'][i]['Dim1']
        num = data['value'][i]['NumericValue']
        print(i)
        cur.execute('INSERT INTO Air_Pollution_Death (ID, Country, Cause_ID, GENDER, Number_of_Death) VALUES (?,?,?,?,?)',
            (i, country, cid, g, num)) 
        index += 1
        if(index % 25 == 0):
            break
    conn.commit()
    

def COVID_API(cur,conn):
# def COVID_API():
    cur.execute('CREATE TABLE IF NOT EXISTS COVID_TEST (Date NUMBER PRIMARY KEY, Positive NUMBER, Negative NUMBER, Currently_Hospitalized NUMBER,Cumulative_Hospitalized NUMBER)')
    cur.execute('SELECT MAX(Date) FROM COVID_TEST')
    temp = cur.fetchone()[0]
    print(str(temp))
    if not temp:
        mon = 3
        day = 1
    else:
        mon = int(str(temp)[4]+ str(temp)[5])
        day = int (str(temp)[6]+str(temp)[7])+1
    if(day == 30):
        day = 1
        mon = mon + 1
    # sys.exit()
    count = 0
    flag = False

    for m in range(13)[mon:]: 
        if count!= 0:
            day = 1
        for d in range(30)[day:]:   
            req_date = f'2020'
            if( m < 10):
                req_date +=f'0{m}'
            else:
                req_date += f'{m}'
            if(d < 10):
                req_date +=f'0{d}'
            else:
                req_date +=f'{d}'
            print(req_date)
            # if(count % 25 == 0):
            #     time.sleep(3)
            
            req = f'https://api.covidtracking.com/v1/us/{req_date}.json'
            count += 1
            # print(req)
            data = requests.get(req).json()
            # print(data)
            # print(data)

            date = data['date']
            num_pos = data['positive']
            num_neg = data['negative']
            cur_hos = data['hospitalizedCurrently']
            accu_hos = data['hospitalizedCumulative']
            cur.execute('INSERT INTO COVID_TEST (Date , Positive , Negative ,Currently_Hospitalized, Cumulative_Hospitalized) VALUES (?,?,?,?,?)',
                (date, num_pos, num_neg,cur_hos, accu_hos))
            conn.commit()
            print(count)
            if(count == 25):
                flag = True
                break
        if flag == True:
            break
    # conn.`commit()
            
            
        

    

def main():
    db_name = '206_final'
    cur, conn = CreateDB(db_name)
    COVID_API(cur, conn)
    # Air_Pollution_Death(cur,conn)
    # cur.execute('DROP TABLE IF EXISTS Air_Pollution_Death')
    # conn.commit()
    
    # COVID_API()
if __name__ == '__main__':
    main()