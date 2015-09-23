#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import re
import datetime
import sys
sys.path.append('/usr/lib/python2.6/site-packages/MySQL_python-1.2.5-py2.6.egg')
import MySQLdb as mysql
from log import *
from mycrypt import prpcrypt
from binascii import b2a_hex, a2b_hex

#锁定主目录
DIR = '/opt/oracle/apache/htdocs/panoramic/'

def getIdIp(node, id):
    '''根据sourceid生成对应IP，返回字符串'''
    with open(DIR + 'config/tab.conf') as f:
        tab_conf = f.read()
        tab_conf = re.findall('\[.*\][A-Z0-9\n=,.:]*', tab_conf)
    if node == 'mas':
        conf = tab_conf[6]
    elif node == 'aps':
        conf = tab_conf[7]
    conf_t = conf.split('\n')[1:][0].split('=')[1].split(',')
    conf_a = conf.split('\n')[2:][0].split('=')[1].split(',')
    conf_b = conf.split('\n')[3:][0].split('=')[1].split(',')
    id_ip = {}
    for i in conf_t:
        id_ip[i.split(':')[0]] = i.split(':')[1]
    for i in conf_a:
        id_ip[i.split(':')[0]] = i.split(':')[1]
    for i in conf_b:
        id_ip[i.split(':')[0]] = i.split(':')[1]
    return id_ip[id]

def getNodeData(node, unit):
    '''根据节点及机组生成关键字字典，返回列表'''
    log = getNodeLog(node, unit)
    data = []
    #忽略log前两个字段time、node
    for i in log[2:]:
        d = {}
        if node == 'pos_machine':
            d['product'] = 'CPS'
            d['name'] = 'POS机'
            d['node'] = 'pos_machine'
            d['time'] = log[0]
            d['type'] = '节点监控'
            d['unit'] = unit
            d['flush'] = int(i.split('=')[1].split(':')[0])
        else:
            d['product'] = 'CPS'
            d['name'] = log[1]
            d['node'] = log[1]
            d['time'] = log[0]
            d['type'] = '节点监控'
            d['unit'] = unit
            d['ip'] = i.split('=')[0]
            if i.split('=')[1].split(':')[0] == '':
                d['request'] = 0
            else:
                d['request'] = int(i.split('=')[1].split(':')[0])
            if i.split('=')[1].split(':')[1] == '':
                d['response'] = 0
            else:
                d['response'] = int(i.split('=')[1].split(':')[1])
            if node == 'tais':
                if i.split('=')[1].split(':')[2] == '':
                    d['forward'] = 0
                else:
                    d['forward'] = int(i.split('=')[1].split(':')[2])
        data.append(d)
    for i in range(len(data)):
        #total ips
        if node == 'tais':
            total_request = total_response = total_forward = 0
            for j in data:
                total_request += int(j['request'])
                total_response += int(j['response'])
                total_forward += int(j['forward'])
            data[i]['differ'] = total_request - total_response - total_forward
            if (total_request - total_response - total_forward) >= 60 or (total_response + total_forward - total_request) >= 60:
                data[i]['alert_level'] = 'critical'
            elif (total_request - total_response - total_forward) >= 45 or (total_response + total_forward - total_request) >= 45:
                data[i]['alert_level'] = 'warning'
            else:
                data[i]['alert_level'] = 'normal'
            data[i]['total_request'] = total_request
            data[i]['total_response'] = total_response
            data[i]['total_forward'] = total_forward
            data[i]['range'] = 'total'
        #total ips
        elif node == 'mas':
            total_request = total_response = 0
            for j in data:
                total_request += int(j['request'])
                total_response += int(j['response'])
            data[i]['differ'] = total_request - total_response 
            if (total_request - total_response) >= 60 or (total_response - total_request) >= 60:
                data[i]['alert_level'] = 'critical'
            elif (total_request - total_response) >= 45 or (total_response - total_request) >= 45:
                data[i]['alert_level'] = 'warning'
            else:
                data[i]['alert_level'] = 'normal'
            data[i]['total_request'] = total_request
            data[i]['total_response'] = total_response
            data[i]['range'] = 'total'
        #total ips
        elif node == 'pos_machine':
            total_flush = 0
            for j in data:
                total_flush += int(j['flush'])
            if total_flush >= 20:
                data[i]['alert_level'] = 'critical'
            elif total_flush >= 10:
                data[i]['alert_level'] = 'warning'
            else:
                data[i]['alert_level'] = 'normal'
            data[i]['total_flush'] = total_flush
            data[i]['range'] = 'total'
        #single IP
        elif node == 'mgw':
            request = int(data[i]['request'])
            response = int(data[i]['response'])
            data[i]['differ'] = request - response
            if (request - response) >= 20 or (response - request) >= 20:
                data[i]['alert_level'] = 'critical'
            elif (request - response) >= 10 or (response - request) >= 10:
                data[i]['alert_level'] = 'warning'
            else:
                data[i]['alert_level'] = 'normal'
            data[i]['range'] = 'single'
        #single IP
        else:
            request = int(data[i]['request'])
            response = int(data[i]['response'])
            data[i]['differ'] = request - response
            if (request - response) >= 30 or (response - request) >= 30:
                data[i]['alert_level'] = 'critical'
            elif (request - response) >= 20 or (response - request) >= 20:
                data[i]['alert_level'] = 'warning'
            else:
                data[i]['alert_level'] = 'normal'
            data[i]['range'] = 'single'
    return data

def getBgwData(node):
    '''根据bgw名称返回字典列表'''
    log = getBgwLog(node)
    data = []
    #忽略log前两个字段time、node
    for i in log[2:]:
        d = {}
        d['product'] = 'CPS'
        d['name'] = log[1]
        d['node'] = log[1]
        d['time'] = log[0]
        d['type'] = '节点监控'
        d['range'] = 'single'
        d['ip'] = i.split('=')[0]
        if i.split('=')[1].split(':')[0] == '':
            d['request'] = 0
        else:
            d['request'] = int(i.split('=')[1].split(':')[0])
        if i.split('=')[1].split(':')[1] == '':
            d['response'] = 0
        else:
            d['response'] = int(i.split('=')[1].split(':')[1])
        d['differ'] = d['request'] - d['response']
        if (d['request'] - d['response']) >= 45 or (d['response'] - d['request']) >= 45:
            d['alert_level'] = 'critical'
        elif (d['request'] - d['response']) >= 30 or (d['response'] - d['request']) >= 30:
            d['alert_level'] = 'warning'
        else:
            d['alert_level'] = 'normal'
        data.append(d)
    return data

def getSlaData(node):
    '''根据名称生成关键字字典，返回列表'''
    log = getSlaLog(node)
    data = []
    if node in ['mas', 'aps']:
        #忽略log前两个字段time、node
        for i in log[2:]:
            d = {}
            d['product'] = 'CPS'
            d['name'] = log[1][1:-1]
            d['node'] = log[1][1:-1]
            d['time'] = log[0]
            d['type'] = 'Sla监控'
            d['range'] = 'single'
            d['ip'] = getIdIp(node, i.split('=')[0])
            d['sla'] = i.split('=')[1]
            if float(d['sla'].split('%')[0]) >= 10:
                d['alert_level'] = 'critical'
            elif float(d['sla'].split('%')[0]) >= 5:
                d['alert_level'] = 'warning'
            else:
                d['alert_level'] = 'normal'
            data.append(d)
    else:
        #忽略log前两个字段time、node
        for i in log[2:]:
            d = {}
            d['product'] = 'CPS'
            d['name'] = log[1][1:-1]
            d['node'] = log[1][1:-1]
            d['time'] = log[0]
            d['type'] = 'Sla监控'
            d['range'] = 'total'
            d['ip'] = '--'
            if i.split('=')[1] == 'N':
                d['sla'] = 0
            else:
                d['sla'] = i.split('=')[1]
            if float(d['sla']) >= 3:
                d['alert_level'] = 'critical'
            elif float(d['sla']) >= 2:
                d['alert_level'] = 'warning'
            else:
                d['alert_level'] = 'normal'
            data.append(d)
    return data

def getQueueData(node, unit):
    log = getQueueLog(unit)
    data = []
    #忽略log第一个字段time及最后一个字段DivMsgs
    for i in log[1:-1]:
        if node == i[0].split('.')[0]:
            d = {}
            d['product'] = 'CPS'
            d['name'] = i[0]
            d['node'] = i[0].split('.')[0]
            d['time'] = log[0]
            d['type'] = 'Queue监控'
            d['range'] = 'single'
            d['unit'] = unit
            d['rcvrs'] = i[1]
            d['msge'] = i[2]
            d['size'] = i[3]
            if int(d['msge']) >= 15:
                d['alert_level'] = 'critical'
            elif int(d['msge']) >=10:
                d['alert_level'] = 'warning'
            else:
                d['alert_level'] = 'normal'
            data.append(d)
    return data

def getYWNode(ip, name): 
    with open(DIR + 'config/db.cfg') as f:
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
        sql = 'select name from jmx_app_config where instance_id=(select instance_id from jmx_instance_config where ip="%s" and name="%s")' %(ip, name) 
        c.execute(sql)
        node = c.fetchall()
        if node:
            return node[0][0]
        else:
            return '--'
    except:
        return '--'
    finally:
        c.close()
        db.close()

def getYWData():
    log = getYWLog()
    data = []
    for i in log:
        d = {}
        d['product'] = i[1]
        d['name'] = i[8]
        d['time'] = i[3].strftime('%H:%M:%S')
        d['type'] = 'YW监控'
        d['type2'] = i[4]
        #根据告警关键字来判定对应节点
        if d['type2'] == 'MQ':
            if i[6].split('.')[0] == 'distributedAppEventQueue':
                if i[6].split('.')[1].lower():
                    d['node'] = i[6].split('.')[1].lower()
                else:
                    d['node'] = '--'
            elif i[6].split('.')[-1] == 'RequestQueue':
                if i[6].split('.')[0]:
                    d['node'] = i[6].split('.')[0]
                else:
                    d['node'] = '--'
            else:   
                d['node'] = '--'
        elif d['type2'] in ['HTTP', 'PORT']:
            d['node'] = 'cnp_web'
        elif d['type2'] == 'JETTY':
            object_key1 = i[6]
            object_key2 = i[7]
            if object_key1[:2] == 't-':
                d['node'] = getYWNode(object_key2, object_key1)
            else:
                d['node'] = '--'
        elif d['type2'] == 'TOMCAT_APP_STATE':
            object_key1 = i[6]
            if object_key1.split('：')[-1]:
                d['node'] = object_key1.split('：')[-1]
            else:
                d['node'] = '--'
        elif d['type2'] == 'TOMCAT_POOL':
            object_key1 = i[6]
            if object_key1.split('_')[-1].lower():
                d['node'] = object_key1.split('_')[-1].lower()
            else:
                d['node'] = '--'
        elif d['type2'] == 'TOMCAT_MEMORY':
            object_key1 = i[6]
            object_key2 = i[7]
            if object_key1[:2] == 't-':
                d['node'] = getYWNode(object_key2, object_key1)
            else:
                d['node'] = '--'
        elif d['type2'] == 'TOMCAT':
            object_key1 = i[6]
            object_key2 = i[7]
            if object_key1[:2] == 't-':
                d['node'] = getYWNode(object_key2, object_key1)
            elif object_key1[:6] == 'tomcat':
                if re.findall('[A-Z]{1}[a-z]{1,}', object_key1)[0].lower():
                    d['node'] = re.findall('[A-Z]{1}[a-z]{1,}', object_key1)[0].lower()
                else:
                    d['node'] = '--'
            else:
                d['node'] = '--'
        else:
            d['node'] = '--'
        object_key = [i[6]]
        if i[7]:
            object_key.append(i[7])
        for j in object_key:
            ip = re.findall('[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}', j) 
            if ip:
                d['ip'] = re.search('[0-9]{1,3}\.[0-9]{1,3}$', ip[0]).group()
            else:
                d['ip'] = '--'
        if d['type2'] == 'HTTP':
            d['alert_desc'] = i[6] + ' ' + i[7] + ' ' + i[9]
        else:
            d['alert_desc'] = '应用名:' + d['node'] + ' ' + i[9]
        d['alert_desc'] = d['alert_desc'][:60]
        if (int(i[5]) == 2) or (int(i[5]) == 3):
            d['alert_level'] = 'warning'
        elif int(i[5]) == 4:
            d['alert_level'] = 'critical'
        else:
            d['alert_level'] = 'normal'
        data.append(d)
    return data

def getSumData(node, unit):
    '''根据节点及机组返回综合节点报警与SLA报警的报警级别,用于MAS&APS'''
    sladata = getSlaData(node)
    nodedata = getNodeData(node, unit)
    for i in sladata:
        for j in nodedata:
            if i['ip'] == j['ip']:
                if i['alert_level'] == 'critical':
                    j['alert_level'] = 'critical'
                elif i['alert_level'] == 'warning':
                    if j['alert_level'] == 'normal':
                        j['alert_level'] = 'warning'
    return nodedata

if __name__ == '__main__':
    '''
    print getNodeData('pos_machine', 't')
    print
    print getBgwData('cups_cp')
    print 
    print getSlaData('mas')
    print
    print
    print getSumData('mas', 't')
    '''
    print getYWData()
