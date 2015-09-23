#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import time
import sys
sys.path.append('/usr/lib/python2.6/site-packages/MySQL_python-1.2.5-py2.6.egg')
import MySQLdb as mysql
from binascii import b2a_hex, a2b_hex
sys.path.append('/opt/oracle/apache/htdocs/panoramic/main')
from mycrypt import prpcrypt

def getYWLog():
    with open('/opt/oracle/apache/htdocs/panoramic/config/db.cfg') as f:
        pc = prpcrypt('keyskeyskeyskeys')
        f = f.readlines()
        host = pc.decrypt(f[0].rstrip())
        port = int(pc.decrypt(f[1].rstrip()))
        user = pc.decrypt(f[2].rstrip())
        passwd = pc.decrypt(f[3].rstrip())
        db = pc.decrypt(f[4].rstrip())
        charset = pc.decrypt(f[5].rstrip())
    try:
        db = mysql.connect(host=host, port=port, user=user, passwd=passwd, db=db, charset=charset)
        #db = mysql.connect(host='192.168.126.157', user='monitor', passwd='monitor', db='monitor', charset='utf8')
        c = db.cursor()
        sql = "select * from triggerred_alert where product_id='CPS' and alert_type not like 'GRAPH%' and last_alert_time > date_sub(now(), interval 1 minute)"
        #sql = "select * from triggerred_alert where product_id='CPS' and alert_type not like 'GRAPH%' and last_alert_time > date_sub(now(), interval 61 minute)"
        c.execute(sql)
        log = c.fetchall()
        return log
    except:
        return []
    finally:
        c.close()
        db.close()

if __name__ == '__main__':
    while True:
        log = getYWLog()
        with open('/opt/oracle/apache/htdocs/panoramic/datas/db.data', 'w') as f:
            for i in log:
                f.write(str(i))
                f.write('\n')
        time.sleep(60)
