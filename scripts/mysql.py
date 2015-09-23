#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import sys
sys.path.append('/usr/lib/python2.6/site-packages/MySQL_python-1.2.5-py2.6.egg')
import MySQLdb as mysql
sys.path.append('/opt/oracle/apache/htdocs/panoramic/main')
from alert import getAlert

def putData():
    db = mysql.connect(host='127.0.0.1', user="tab", passwd="p@ssw0rd", db="monitor", charset="utf8")
    db.autocommit(True)
    c = db.cursor()
    data = getAlert()
    alert = []
    for i in data:
        name = i['name']
        alert_time = i['time']
        alert_level = i['alert_level']
        if i['type'] == 'Queue监控':
            ip = i['unit']  + "机组" 
        elif i['type'] == '节点监控':
            if i['node'] in ['mas', 'tais', 'pos_machine']:
                ip = i['unit']  + "机组" 
            else:
                ip = i['ip']
        else:
            ip = i['ip']
        if i['type'] == 'YW监控':
            type = i['type2']
        else:
            type = i['type']
        if i['type'] == '节点监控':
            if i['name'] == 'POS机':
                alert_desc = str(i['total_flush']) + "笔POS机冲正"
            elif i['name'] == 'tais':
                alert_desc = str(i['total_request']) + ":" + str(i['total_response']) + ":" + str(i['total_forward']) + "请返相差" + str(i['differ']) 
            elif i['name'] == 'mas':
                alert_desc = str(i['total_request']) + ":" + str(i['total_response']) + "请返相差" + str(i['differ'])
            else:
                alert_desc = str(i['request']) + ":" + str(i['response']) + "请返相差" + str(i['differ'])
        elif i['type'] == 'Sla监控':
            alert_desc = 'Sla为' + str(i['sla']) + 'S'
        elif i['type'] == 'Queue监控':
            alert_desc = 'Msge:' + i['msge'] + '  Size:' + i['size']
        elif i['type'] == 'YW监控':
            alert_desc = i['alert_desc'] 
        else:
            alert_desc = "--"
        a = {'time': time.strftime('%Y-%m-%d %H:%M',time.localtime(time.time())), 'name': name, 'ip': ip, 'type':type, 'alert_time':alert_time, 'alert_level':alert_level, 'alert_desc': alert_desc}
        alert.append(a)
    try:
        for data in alert:
            sql = "INSERT INTO alert(`time`, `name`, `ip`, `type`, `alert_time`, `alert_level`, `alert_desc`) \
            VALUES('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}')".format(data['time'], \
            data['name'], data['ip'], data['type'], data['alert_time'], data['alert_level'], data['alert_desc'])
            c.execute(sql)
    except Exception as e:
        print(e)
    finally:
        c.close()
        db.close()

if __name__ == "__main__":
    while True:
        putData()
        time.sleep(60)
