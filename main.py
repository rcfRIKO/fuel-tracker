import json, time, requests, random, os
import sqlite3
from secrets import API_KEY

def get_prices(station_ids):
    url = 'https://creativecommons.tankerkoenig.de/json/prices.php?ids=' + ','.join(station_ids) + '&apikey=' + API_KEY
    time.sleep(random.randint(0, 45))
    result = requests.get(url).json()
    if (result['ok']):
        return result["prices"]
    else:
        print('Error')
        return {}

def get_ids():
    with open('ids.json') as file_name:
        data = json.load(file_name)
        return data['ids']

if __name__ == '__main__':
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)
    ids = get_ids()
    res = get_prices(ids)
    con = sqlite3.connect("data.db")
    insert_list = []
    for key, value in res.items():
        insert_list.append((key, value.get("status") == "open", value.get("e10", -1), value.get("e5", -1), value.get("diesel", -1)))
    cur = con.cursor()
    cur.executemany("INSERT INTO fueltracker (uuid, open, e10, e5, diesel) VALUES (?, ?, ?, ?, ?)", insert_list) 
    con.commit()
    con.close()


        

