#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import re
#YW数据库数据使用datetime
import datetime

#锁定主目录
DIR = '/usr/local/apache/htdocs/monitor-show/'

def getNodeIp(node, unit=None):
    '''根据节点及机组生成该节点在TAB机组的IP分布列表，返回IP列表'''
    t = []
    a = []
    b = []
    all = []
    with open(DIR + 'config/tab.conf') as f:
        tab_conf = f.read()
        tab_conf = re.findall('\[.*\][A-Z0-9\n=,.:]*', tab_conf)
    #获取各节点IP信息
    nodes = ['vpos', 'mgw', 'posp', 'internal', 'mbp', 'tais', 'mas', 'aps', 'cups_cp', 'cups_cnp', 'cups_kj', 'icbc_sh_kj', 'abc_sz_kj']
    if node == 'pos_machine':
        conf = tab_conf[2]
    else:
        for i in range(len(nodes)):
            if node == nodes[i]:
                conf = tab_conf[i]
                break
    #获取节点各机组IP信息
    if node in ['mas', 'aps']:
        t = [ i.split(':')[1] for i in conf.split('\n')[1].split('=')[1].split(',') ]
        a = [ i.split(':')[1] for i in conf.split('\n')[2].split('=')[1].split(',') ]
        b = [ i.split(':')[1] for i in conf.split('\n')[3].split('=')[1].split(',') ]
    elif node in ['pos_machine', 'vpos', 'mgw', 'posp', 'internal', 'mbp', 'tais']:
        t = conf.split('\n')[1].split('=')[1].split(',')
        a = conf.split('\n')[2].split('=')[1].split(',')
        b = conf.split('\n')[3].split('=')[1].split(',')
    else:
        all = conf.split('\n')[1].split('=')[1].split(',')
    if unit == 'T':
        return t
    elif unit == 'A':
        return a
    elif unit == 'B':
        return b
    elif unit == None:
        return all
    else:
        return []

def analyzeLog(node, unit, node_log):
    '''根据节点、机组及日志处理该日志，返回只包含该机组的日志'''
    log = []
    ip = getNodeIp(node, unit)
    for i in range(1, len(node_log)):
        for j in range(len(ip)):
            if ip[j] == re.findall('[0-9]{1,3}\.[0-9]{1,3}', node_log[i].split('=')[0])[1]:
                log.append(re.search('[0-9]{1,3}\.[0-9]{1,3}=.*', node_log[i]).group(0))
    log.append(node)
    return log

def getNodeLog(node, unit):
    '''根据节点及机组生成对应日志，返回日志列表'''
    with open(DIR + 'datas/splunk.data') as f:
        time = re.search('\d{2}:\d{2}', f.readline())
        if time:
            time = time.group()
        else:
            time = time.strftime("%H:%M", time.localtime())
        raw_log = f.read()
    #按节点名称将日志拆分成多个字符串并放入列表
    raw_log = [ i.rstrip('\n') for i in re.findall('\[.*\][0-9\n=:.]*', raw_log) ]
    nodes = ['pos_machine', 'vpos', 'posp', 'mgw', 'internal', 'mbp', 'tais', 'mas', 'aps']
    for i in range(len(nodes)):
        if node == nodes[i]:
            node_log = raw_log[i]
            node_log = [ node_log.split('\n')[i] for i in range(len(node_log.split('\n'))) ]
            if unit == 'T':
                log = analyzeLog(node, 'T', node_log)
            elif unit == 'A':
                log = analyzeLog(node, 'A', node_log)
            else:
                log = analyzeLog(node, 'B', node_log)
            break
    #没数据的IP统一设为0
    ip = getNodeIp(node, unit)
    for i in log[:-1]:
        for j in ip:
            if j == i.split('=')[0]:
                ip.remove(j)
    for i in ip:
        if node == 'tais':
            log.insert(-1, i+'=0:0:0')
        elif node == 'pos_machine':
            log.insert(-1, i+'=0')
        else:
            log.insert(-1, i+'=0:0')
    #统一格式为[time, node, data]
    log.insert(0, time)
    node = log[-1]
    log = log[:-1]
    log.insert(1, node)
    return log

def getBgwLog(node):
    '''根据bgw节点返回日志列表'''
    with open(DIR + 'datas/bgw.data') as f:
        time = re.search('\d{2}:\d{2}', f.readline())
        if time:
            time = time.group()
        else:
            time = time.strftime("%H:%M", time.localtime())
        raw_log = f.read()
    raw_log = [ i.rstrip('\n') for i in re.findall('\[.*\][0-9\n=:.]*', raw_log) ]
    nodes = ['cups_cp', 'cups_cnp', 'cups_kj', 'icbc_sh_kj', 'abc_sz_kj']
    for i in range(len(nodes)):
        if node == nodes[i]:
            log = raw_log[i]
            log = [ log.split('\n')[i] for i in range(len(log.split('\n'))) ] 
            if len(log) > 2:
                if re.search('[0-9]{1,3}\.[0-9]{1,3}=[0-9]*:[0-9]*', log[1]):
                    log[1] = re.search('[0-9]{1,3}\.[0-9]{1,3}=[0-9]*:[0-9]*', log[1]).group()
                    if re.search('[0-9]{1,3}\.[0-9]{1,3}=[0-9]*:[0-9]*', log[2]):
                        log[2] = re.search('[0-9]{1,3}\.[0-9]{1,3}=[0-9]*:[0-9]*', log[2]).group()
                    else:
                        log = log[:2]
                else:
                    if re.search('[0-9]{1,3}\.[0-9]{1,3}=[0-9]*:[0-9]*', log[2]):
                        log[1] = re.search('[0-9]{1,3}\.[0-9]{1,3}=[0-9]*:[0-9]*', log[2]).group()
                        log = log[:2]
                    else:
                        log = log[:1]
            elif len(log) > 1:
                if re.search('[0-9]{1,3}\.[0-9]{1,3}=[0-9]*:[0-9]*', log[1]):
                    log[1] = re.search('[0-9]{1,3}\.[0-9]{1,3}=[0-9]*:[0-9]*', log[1]).group()
                else:
                    log = log[:1]
            break
    #没数据的IP统一设为0
    ip = getNodeIp(node)
    for i in log[1:]:
        for j in ip:
            if j == i.split('=')[0]:
                ip.remove(j)
    for i in ip:
        log.append(i+'=0:0')
    #统一格式为[time, node, data]
    log.insert(0, time)
    return log

def getSlaLog(node):
    '''根据节点名称返回日志列表'''
    with open(DIR + 'datas/sla.data') as f:
        time = f.readline().rstrip().split(' ')[1]
        raw_log = f.read()
    raw_log = [ i.rstrip('\n') for i in re.findall('\[.*\][a-zA-Z0-9\n=.%]*', raw_log) ]
    nodes = ['cups_cp', 'cups_cnp', 'icbc_sh_kj', 'abc_sz_kj', 'mas', 'aps']
    for i in range(len(nodes)):
        if node == nodes[i]:
            log = raw_log[i]
            log = log.split('\n')
    #避免多行垃圾日志(可能出现多行同样数据)
    if node in ['cups_cp', 'cups_cnp', 'icbc_sh_kj', 'abc_sz_kj']:
        log = log[:2]
    elif node in ['cups_kj']:
        log = []
    else:
        log = log[:5]
    #统一格式为[time, node, data]
    log.insert(0, time)
    return log

def getQueueLog(unit):
    '''根据节点名称返回日志列表'''
    log = []
    with open(DIR + 'datas/' + unit + '-tibco.data') as f:
        raw_log = f.read()
        raw_log = raw_log.split('\n')[:-1]
    time = raw_log[0].split(' ')[0]
    for i in raw_log:
        log.append(re.findall('[A-Za-z0-9_\.]{1,}', i))
    log[0] = time
    return log

def getYWLog():
    with open(DIR + 'datas/db.data') as f:
        f = f.readlines()
        log = []
        for i in f:
            log.append(eval(i.rstrip()))
        return log

if __name__ == '__main__':
    '''
    print getNodeLog('mas', 't')
    print
    print getBgwLog('cups_cp')
    print
    print getSlaLog('mas')
    print
    print getQueueLog('T')
    '''
    print(getYWLog())
