# -*- coding: utf-8 -*-

import psycopg2

from db_const import DSN
from area_const import _PREF

num = 0
with psycopg2.connect(DSN) as con:
    with con.cursor() as cur:
        cur.execute('truncate table area')
    for c, v in _PREF.items():
        with con.cursor() as cur:
            sql = "insert into area (area_code, area_name, area_group1) values "
            sql += "('%s', '%s', '%s')" % (c, v['name'], v['group1'], )
            cur.execute(sql)
            num += 1
    con.commit()
print('area table inset : %d records' % num)

#[EOF]