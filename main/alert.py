#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from data import *

#告警列表
alert = []   

def getAlert():
    '''获取所有异常数据'''
    log = []
    alert = []
    #节点数据
    for i in ['T', 'A', 'B']:
        log.append(getNodeData('pos_machine', i)[0]) #total
        log.extend(getNodeData('vpos', i))
        log.extend(getNodeData('mgw', i))
        log.extend(getNodeData('posp', i))
        log.extend(getNodeData('internal', i))       
        log.extend(getNodeData('mbp', i))
        log.append(getNodeData('tais', i)[0])        #total
        log.append(getNodeData('mas', i)[0])         #total
        log.extend(getNodeData('aps', i))
    #bgw数据
    for i in ['cups_cp', 'cups_cnp', 'cups_kj', 'icbc_sh_kj', 'abc_sz_kj']:
        log.extend(getBgwData(i))
    #SLA数据
    for i in ['mas', 'aps', 'cups_cp', 'cups_cnp', 'icbc_sh_kj', 'abc_sz_kj']:
        log.extend(getSlaData(i))
    #Queue数据
    for i in ['mas', 'internal', 'tais', 'cis', 'bgw']:
        for j in ['T', 'A', 'B']:
            log.extend(getQueueData(i, j))
    #YW数据
    log.extend(getYWData())
    for i in log:
        if i['alert_level'] == 'warning':
            alert.append(i)
    for i in log:
        if i['alert_level'] == 'critical':
            alert.append(i)
    return alert

def analyzeAlert():
    '''保证报警信息为10行'''
    global alert
    new_alert = getAlert()
    if alert == []:
        #无报警记录且无新的报警
        if new_alert == []:
            for i in range(10):
                alert.append({'name': '', 'no': '', 'ip': '', 'alert_level': 'null', 'request': '', 'range': 'single', 'time': '', 'type': '', 'response': ''})
            for i in range(len(alert)):
                alert[i]['no'] = i+1
            alerts = []
            for i in range(5):
                alerts.append([alert[i], alert[i+5]])
            return alerts
        #无报警记录且有新的报警
        else:
            line = len(alert)+len(new_alert) - 10
            #新报警超过10行
            if line > 0:
                if line <= len(alert):
                    for i in range(line):
                        alert.pop()
                else:
                    for i in range(len(alert)):
                        alert.pop()
                for i in range(len(new_alert)):
                    alert.insert(0, new_alert[i])
                for i in range(len(alert)):
                    alert[i]['no'] = i+1
            #新报警不超过10行
            else:
                for i in range(len(new_alert)):
                    alert.insert(0, new_alert[i])
                for i in range(10-len(alert)):
                    alert.append({'name': '', 'no': '', 'ip': '', 'alert_level': 'null', 'request': '', 'range': 'single', 'time': '', 'type': '', 'response': ''})
                for i in range(len(alert)):
                    alert[i]['no'] = i+1
            alerts = []
            for i in range(5):
                alerts.append([alert[i], alert[i+5]])
            return alerts
    else:
        #有报警记录且无新的报警
        if new_alert == []:
            alerts = []
            for i in range(5):
                alerts.append([alert[i], alert[i+5]])
            return alerts
        #有报警记录且有新的报警
        else:
            #新报警是相同报警忽略 
            if new_alert[-1]['name'] == alert[0]['name'] and new_alert[-1]['time'] == alert[0]['time'] and new_alert[-1]['type'] == alert[0]['type']:
                alerts = []
                for i in range(5):
                    alerts.append([alert[i], alert[i+5]])
                return alerts
            #新报警是不同报警
            else:
                line = len(alert)+len(new_alert) - 10

                if line > 10: #避免pop超过10次报错
                    line = 10
                for i in range(line):
                    alert.pop()
                for i in range(len(new_alert)):
                    alert.insert(0, new_alert[i])
                for i in range(len(alert)):
                    alert[i]['no'] = i+1
                alerts = []
                for i in range(5):
                    alerts.append([alert[i], alert[i+5]])
                return alerts

def text2html():
    data = analyzeAlert()
    alert = []
    for i in data:
        no = "<td>" +  str(i[0]['no'])  + "</td>"
        time = "<td>" +  i[0]['time']  + "</td>"
        name = "<td>" +  i[0]['name']  + "</font></td>"
        if i[0]['type'] == 'Queue监控':
            ip = "<td>" +  i[0]['unit']  + "机组" + "</td>"
        elif i[0]['type'] == '节点监控':
            if i[0]['node'] in ['mas', 'tais', 'pos_machine']:
                ip = "<td>" +  i[0]['unit']  + "机组" + "</td>"
            else:
                ip = "<td>" +  i[0]['ip']  + "</td>"
        else:
            ip = "<td>" +  i[0]['ip']  + "</td>"
        if i[0]['type'] == 'YW监控':
            type = "<td>" +  i[0]['type2']  + "</td>"
        else:
            type = "<td>" +  i[0]['type']  + "</td>"
        if i[0]['alert_level'] == 'critical':
            alert_level = "<td bgcolor='f88888'></td>"
        elif i[0]['alert_level'] == 'warning':
            alert_level = "<td bgcolor='ffff00'></td>"
        else:
            alert_level = "<td></td>"
        if i[0]['type'] == '节点监控':
            if i[0]['name'] == 'POS机':
                alert_desc = "<td>" + str(i[0]['total_flush']) + "笔POS机冲正</td>"
            elif i[0]['name'] == 'tais':
                alert_desc = "<td>" + str(i[0]['total_request']) + ":" + str(i[0]['total_response']) + ":" + str(i[0]['total_forward']) + "请返相差" + str(i[0]['differ']) + "</td>"
            elif i[0]['name'] == 'mas':
                alert_desc = "<td>" + str(i[0]['total_request']) + ":" + str(i[0]['total_response']) + "请返相差" + str(i[0]['differ']) + "</td>"
            else:
                alert_desc = "<td>" + str(i[0]['request']) + ":" + str(i[0]['response']) + "请返相差" + str(i[0]['differ']) + "</td>"
        elif i[0]['type'] == 'Sla监控':
            alert_desc = '<td>Sla为' + str(i[0]['sla']) + 'S</td>'
        elif i[0]['type'] == 'Queue监控':
            alert_desc = '<td>' + 'Msge:' + i[0]['msge'] + '  Size:' + i[0]['size']
        elif i[0]['type'] == 'YW监控':
            alert_desc = "<td>" + i[0]['alert_desc'] + "</td>"
        else:
            alert_desc = "<td></td>"
        a = {'no': no, 'time': time, 'name': name, 'ip': ip, 'type':type, 'alert_level':alert_level, 'alert_desc': alert_desc}
        #第二大列
        no = "<td>" +  str(i[1]['no'])  + "</td>"
        time = "<td>" +  i[1]['time']  + "</td>"
        name = "<td>" +  i[1]['name']  + "</font></td>"
        if i[1]['type'] == 'Queue监控':
            ip = "<td>" +  i[1]['unit']  + "机组" + "</td>"
        elif i[1]['type'] == '节点监控':
            if i[1]['node'] in ['mas', 'tais', 'pos_machine']:
                ip = "<td>" +  i[1]['unit']  + "机组" + "</td>"
            else:
                ip = "<td>" +  i[1]['ip']  + "</td>"
        else:
            ip = "<td>" +  i[1]['ip']  + "</td>"
        if i[1]['type'] == 'YW监控':
            type = "<td>" +  i[1]['type2']  + "</td>"
        else:
            type = "<td>" +  i[1]['type']  + "</td>"
        if i[1]['alert_level'] == 'critical':
            alert_level = "<td bgcolor='f88888'></td>"
        elif i[1]['alert_level'] == 'warning':
            alert_level = "<td bgcolor='ffff00'></td>"
        else:
            alert_level = "<td></td>"
        if i[1]['type'] == '节点监控':
            if i[1]['name'] == 'POS机':
                alert_desc = "<td>" + str(i[1]['total_flush']) + "笔POS机冲正</td>"
            elif i[1]['name'] == 'tais':
                alert_desc = "<td>" + str(i[1]['total_request']) + ":" + str(i[1]['total_response']) + ":" + str(i[1]['total_forward']) + "请返相差" + str(i[1]['differ']) + "</td>"
            elif i[1]['name'] == 'mas':
                alert_desc = "<td>" + str(i[1]['total_request']) + ":" + str(i[1]['total_response']) + "请返相差" + str(i[1]['differ']) + "</td>"
            else:
                alert_desc = "<td>" + str(i[1]['request']) + ":" + str(i[1]['response']) + "请返相差" + str(i[1]['differ']) + "</td>"
        elif i[1]['type'] == 'Sla监控':
            alert_desc = '<td>Sla为' + str(i[1]['sla']) + 'S</td>'
        elif i[1]['type'] == 'Queue监控':
            alert_desc = '<td>' + 'Msge:' + i[1]['msge'] + '  Size:' + i[1]['size']
        elif i[1]['type'] == 'YW监控':
            alert_desc = "<td>" + i[1]['alert_desc'] + "</td>"
        else:
            alert_desc = "<td></td>"
        b = {'no': no, 'time': time, 'name': name, 'ip': ip, 'type':type, 'alert_level':alert_level, 'alert_desc': alert_desc}
        alert.append([a, b])
    return alert

if __name__ == '__main__':
    print getAlert()
