#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from data import *

def getNodePic(node):
    '''根据报警情况返回对应图片'''
    data = getNodeData(node, 'T')
    data.extend(getNodeData(node, 'A'))
    data.extend(getNodeData(node, 'B'))
    data.extend(getQueueData(node,'T'))
    data.extend(getQueueData(node,'A'))
    data.extend(getQueueData(node,'B'))
    #YW系统数据筛选出确定节点的告警数据
    data_yw = getYWData()
    YWData = []
    for i in data_yw:
        if i['node'] == node:
           YWData.append(i)
    data.extend(YWData)
    number_critical = number_warning = 0
    #total
    if node in ['pos_machine', 'tais', 'mas']:
        for i in range(len(data)):
            if data[i]['alert_level'] == 'critical':
                number_critical += 1
            elif data[i]['alert_level'] == 'warning':
                number_warning += 1
        if number_critical >= 1:
            return './static/image/' + node + '_critical.jpg'
        elif number_warning >= 1:
            return './static/image/' + node + '_warning.jpg'
        else:
            return './static/image/' + node + '_normal.jpg'
    #single
    else:
        for i in range(len(data)):
            if data[i]['alert_level'] == 'critical' and data[i]['type'] == 'Queue监控':
                number_critical += 2
            elif data[i]['alert_level'] == 'critical':
                number_critical += 1
            elif data[i]['alert_level'] == 'warning' and data[i]['type'] == 'Queue监控':
                number_warning += 2
            elif data[i]['alert_level'] == 'warning':
                number_warning += 1
        if number_critical >= 2:
            return './static/image/' + node + '_critical.jpg'
        elif number_critical == 1 or number_warning >= 2:
            return './static/image/' + node + '_warning.jpg'
        else:
            return './static/image/' + node + '_normal.jpg'

def getBgwPic(node):
    '''根据bgw报警情况返回图片'''
    alert_level = 'normal'
    data = getBgwData(node)
    data.extend(getSlaData(node))
    data.extend(getQueueData('bgw', 'T'))
    data.extend(getQueueData('bgw', 'A'))
    data.extend(getQueueData('bgw', 'B'))
    return returnPic(node, alert_level, data)
	    
def getBankPic(node):
    '''根据银行名称返回银行对应图形'''
    bank = []
    alert_level = 'normal'
    if node == 'cups':
        bank = getBgwData('cups_cp')
        bank.extend(getBgwData('cups_cnp'))
        bank.extend(getBgwData('cups_kj'))
        bank.extend(getSlaData('cups_cp'))
        bank.extend(getSlaData('cups_cnp'))
        return returnPic(node, alert_level , bank)
    elif node == 'icbc':
        bank = getBgwData('icbc_sh_kj')
        bank.extend(getSlaData('icbc_sh_kj'))
        return returnPic(node, alert_level , bank)
    elif node == 'ccb':
        return returnPic(node, alert_level , bank)
    elif node == 'abc':
        bank = getBgwData('abc_sz_kj')
        bank.extend(getSlaData('abc_sz_kj'))
        return returnPic(node, alert_level , bank)
    elif node == 'boc':
        return returnPic(node, alert_level , bank)

def getSlaPic(node):
    '''根据Sla报警情况返回图片'''
    #bgw与bank之间的线条
    if node == 'bgw':
        alert_level = 'normal'
        for i in ['cups_cp', 'cups_cnp', 'icbc_sh_kj', 'abc_sz_kj']:
            if getSlaData(i)[0]['alert_level'] == 'critical':
                alert_level = 'critical'
            elif getSlaData(i)[0]['alert_level'] == 'warning':
                alert_level = 'warning'
        if alert_level == 'normal':
            return './static/image/arrow_normal.jpg'
        elif alert_level == 'warning':
            return './static/image/arrow_warning.jpg'
        else:
            return './static/image/arrow_critical.jpg' 
    else:
        if getSlaData(node):
            #the number of clour
            number_critical = number_warning = 0
            data = getSlaData(node)
            if node in ['mas', 'aps']:
                for i in range(len(data)):
                    if data[i]['alert_level'] == 'critical':
                        number_critical += 1
                    elif data[i]['alert_level'] == 'warning':
                        number_warning += 1
                if number_critical >= 2:
                    return './static/image/arrow_' + node + '_critical.jpg'
                elif number_critical == 1 or number_warning >= 2:
                    return './static/image/arrow_' + node + '_warning.jpg'
                else:
                    return './static/image/arrow_' + node + '_normal.jpg'
        else:
            return './static/image/arrow_' + node + '_normal.jpg'

def getEntryPic(node):
    alert_level = 'normal'
    data = []
    for i in getYWData():
        if i['node'] == node:
            data.append(i)
    return returnPic(node, alert_level, data)

def returnPic(node, alert_level, data):
    '''综合多个数据返回等级最高的告警图形'''
    for i in data:
        if i['alert_level'] == 'critical':
            return './static/image/' + node + '_critical.jpg'
        elif i['alert_level'] == 'warning':
            alert_level = 'warning'
    if alert_level == 'normal':            
        return './static/image/' + node + '_normal.jpg'
    elif alert_level == 'warning':
        return './static/image/' + node + '_warning.jpg'

if __name__ == '__main__':
    print(getNodePic('tais'))
