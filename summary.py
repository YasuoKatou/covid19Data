# -*- coding: utf-8 -*-

import requests
import json
#import psycopg2 as DB
import sqlite3  as DB

from covid19_const import URL104
from area_const import getAreaCode
from db_const import DSN

# 都道府県別累積陽性者
headers = {"content-type": "application/json"}
r = requests.get(URL104, headers=headers)
print('https status : %d' % r.status_code)
print('response content-type : %s' % r.headers['content-type'])
data = r.json()
#print(json.dumps(data, indent=4))
recs = {}
lastUpdate = data[0]['lastUpdate']
print('最終更新日 :　%s' % lastUpdate)
for p in data[0]['area']:
    n = p['name_jp']
    ac = getAreaCode(n)
    print('%s[%s], %d' % (n, ac, p['npatients']))
    recs[ac] = p['npatients']

with DB.connect(DSN) as con:
    cur = con.cursor()
    sql = "delete from summary where last_update = '%s'" % lastUpdate
    cur.execute(sql)
    print('deleted rows : %d' % cur.rowcount)
    cur.close()
    num = 0
    for cd, n in recs.items():
        cur = con.cursor()
        sql = "insert into summary (last_update, area_code, total) values "
        sql += "('%s', '%s', %d)" % (lastUpdate, cd, n)
        cur.execute(sql)
        cur.close()
        num += 1
    con.commit()
print('new record : %d' % num)

#[EOF]