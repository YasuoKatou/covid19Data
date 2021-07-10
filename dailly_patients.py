# -*- coding: utf-8 -*-

import datetime as DT
import requests
import json
#import psycopg2 as DB
import sqlite3  as DB

from covid19_const import URL105
from area_const import getAreaCode
from db_const import DSN

now = DT.datetime.now()
dd  = DT.timedelta(days=1)
days = 5
#days = 365 * 2
headers = {"content-type": "application/json"}

def save(td, items):
    if not items:
        return
    recs = {}
    for p in items:
        n = p['name_jp']
        ac = getAreaCode(n)
        print('%s[%s], %s' % (n, ac, p['npatients']))
        recs[ac] = p['npatients']
    with DB.connect(DSN) as con:
        cur = con.cursor()
        sql = "delete from dailly_patients where target_date = '%s'" % td
        cur.execute(sql)
        cur.close()
        print('deleted rows : %d' % cur.rowcount)
        num = 0
        ttl = 0
        for cd, n in recs.items():
            cur = con.cursor()
            sql = "insert into dailly_patients (target_date, area_code, patients) values "
            sql += "('%s', '%s', %s)" % (td, cd, n)
            cur.execute(sql)
            cur.close()
            num += 1
            ttl += int(n)
        # 1日の合計を出力
        cur = con.cursor()
        sql = "insert into dailly_patients (target_date, area_code, patients) values "
        sql += "('%s', 'JP', %d)" % (td, ttl)
        cur.execute(sql)
        cur.close()

        con.commit()
        print('date : %s, new record : %d, patients : %d' % (td, num, ttl))

# 新規感染者（日毎）
while True:
    #print(now.strftime('%Y%m%d'))
    td = now.strftime('%Y%m%d')
    #print('target date : %s' % td)
    r = requests.get(URL105 % td, headers=headers)
    #print('https status : %d' % r.status_code)
    #print('response content-type : %s' % r.headers['content-type'])
    data = r.json()
    print('errorInfo:%s, items:%d' % (str(data['errorInfo']), len(data['itemList'])))
    td = now.strftime('%Y-%m-%d')
    save(td, data['itemList'])

    days -= 1
    if not days:
        break
    now -= dd

#[EOF]