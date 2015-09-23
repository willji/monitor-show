#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import time
import os
import sys
sys.path.append('/usr/lib/python2.6/site-packages/Werkzeug-0.9-py2.6.egg')
sys.path.append('/usr/lib/python2.6/site-packages/MarkupSafe-0.9-py2.6.egg')
sys.path.append('/usr/lib/python2.6/site-packages/Jinja2-2.7-py2.6.egg')
sys.path.append('/usr/lib/python2.6/site-packages/Flask-0.9-py2.6.egg')
from flask import Flask, render_template
from data import *
from alert import *
from pic import *
import mylog

app = Flask(__name__)

def getImage():
    images = []
    images.append('./static/images/cp_web_normal.jpg')
    images.append(getEntryPic('cnp_web'))
    images.append(getNodePic('pos_machine'))
    images.append('./static/images/fi_ddp_normal.jpg')
    images.append('./static/images/app_normal.jpg')
    images.append('./static/images/arrow_normal.jpg')
    images.append(getNodePic('vpos'))
    images.append(getNodePic('mgw'))
    images.append(getNodePic('posp'))
    images.append(getNodePic('internal'))
    images.append(getNodePic('mbp'))
    images.append('./static/images/arrow_normal.jpg')
    images.append(getNodePic('tais'))
    images.append('./static/images/arrow_normal.jpg')
    images.append(getNodePic('mas'))
    images.append(getSlaPic('mas'))
    images.append(getNodePic('aps'))
    images.append(getSlaPic('aps'))
    images.append(getBgwPic('cups_cp'))
    images.append(getBgwPic('cups_cnp'))
    images.append(getBgwPic('cups_kj'))
    images.append(getBgwPic('icbc_sh_kj'))
    images.append(getBgwPic('abc_sz_kj'))
    images.append(getSlaPic('bgw'))
    images.append(getBankPic('cups')) 
    images.append(getBankPic('boc')) 
    images.append(getBankPic('icbc')) 
    images.append(getBankPic('abc')) 
    images.append(getBankPic('ccb')) 
    return images

@app.route('/index.html', methods=['GET'])
def index():
    return render_template('index.html', images=getImage())

@app.route('/index.htm', methods=['GET'])
def index2():
    try:
        return render_template('index.htm', images=getImage())
    except:
        mylog.mylog.exception('error')

@app.route('/index2.htm', methods=['GET'])
def index3():
    return render_template('index2.htm', images=getImage())

@app.route('/entry.htm', methods=['GET'])
def entry():
    return render_template('./entry.htm', images=getImage())

@app.route('/channel.htm', methods=['GET'])
def channel():
    return render_template('./channel.htm', images=getImage())

@app.route('/tais.htm', methods=['GET'])
def tais2():
    return render_template('./tais.htm', images=getImage())

@app.route('/mas.htm', methods=['GET'])
def mas2():
    return render_template('./mas.htm', images=getImage())

@app.route('/aps.htm', methods=['GET'])
def aps2():
    return render_template('./aps.htm', images=getImage())

@app.route('/bgw.htm', methods=['GET'])
def bgw():
    return render_template('./bgw.htm', images=getImage())

@app.route('/bank.htm', methods=['GET'])
def bank():
    return render_template('./bank.htm', images=getImage())

@app.route('/pos_machine.html', methods=['GET'])
def pos_machine():
    return render_template('./cps/pos_machine.html')

@app.route('/cps/pos_machine_t.html', methods=['GET'])
def pos_machine_t():
    return render_template('./cps/pos_machine_t.html', pos_machine=getNodeData('pos_machine', 'T'))

@app.route('/cps/pos_machine_a.html', methods=['GET'])
def pos_machine_a():
    return render_template('./cps/pos_machine_a.html', pos_machine=getNodeData('pos_machine', 'A'))

@app.route('/cps/pos_machine_b.html', methods=['GET'])
def pos_machine_b():
    return render_template('./cps/pos_machine_b.html', pos_machine=getNodeData('pos_machine', 'B'))

@app.route('/vpos.html', methods=['GET'])
def vpos():
    return render_template('./cps/vpos.html')

@app.route('/cps/vpos_t.html', methods=['GET'])
def vpos_t():
    return render_template('./cps/vpos_t.html', vpos=getNodeData('vpos', 'T'))

@app.route('/cps/vpos_a.html', methods=['GET'])
def vpos_a():
    return render_template('./cps/vpos_a.html', vpos=getNodeData('vpos', 'A'))

@app.route('/cps/vpos_b.html', methods=['GET'])
def vpos_b():
    return render_template('./cps/vpos_b.html', vpos=getNodeData('vpos', 'B'))

@app.route('/mgw.html', methods=['GET'])
def mgw():
    return render_template('./cps/mgw.html')

@app.route('/cps/mgw_t.html', methods=['GET'])
def mgw_t():
    return render_template('./cps/mgw_t.html', mgw=getNodeData('mgw', 'T'))

@app.route('/cps/mgw_a.html', methods=['GET'])
def mgw_a():
    return render_template('./cps/mgw_a.html', mgw=getNodeData('mgw', 'A'))

@app.route('/cps/mgw_b.html', methods=['GET'])
def mgw_b():
    return render_template('./cps/mgw_b.html', mgw=getNodeData('mgw', 'B'))

@app.route('/posp.html', methods=['GET'])
def posp():
    return render_template('./cps/posp.html')

@app.route('/cps/posp_t.html', methods=['GET'])
def posp_t():
    return render_template('./cps/posp_t.html', posp=getNodeData('posp', 'T'))

@app.route('/cps/posp_a.html', methods=['GET'])
def posp_a():
    return render_template('./cps/posp_a.html', posp=getNodeData('posp', 'A'))

@app.route('/cps/posp_b.html', methods=['GET'])
def posp_b():
    return render_template('./cps/posp_b.html', posp=getNodeData('posp', 'B'))

@app.route('/internal.html', methods=['GET'])
def internal():
    return render_template('./cps/internal.html')

@app.route('/cps/internal_t.html', methods=['GET'])
def internal_t():
    return render_template('./cps/internal_t.html', internal=getNodeData('internal', 'T'))

@app.route('/cps/internal_a.html', methods=['GET'])
def internal_a():
    return render_template('./cps/internal_a.html', internal=getNodeData('internal', 'A'))

@app.route('/cps/internal_b.html', methods=['GET'])
def internal_b():
    return render_template('./cps/internal_b.html', internal=getNodeData('internal', 'B'))

@app.route('/mbp.html', methods=['GET'])
def mbp():
    return render_template('./cps/mbp.html')

@app.route('/cps/mbp_t.html', methods=['GET'])
def mbp_t():
    return render_template('./cps/mbp_t.html', mbp=getNodeData('mbp', 'T'))

@app.route('/cps/mbp_a.html', methods=['GET'])
def mbp_a():
    return render_template('./cps/mbp_a.html', mbp=getNodeData('mbp', 'A'))

@app.route('/cps/mbp_b.html', methods=['GET'])
def mbp_b():
    return render_template('./cps/mbp_b.html', mbp=getNodeData('mbp', 'B'))

@app.route('/tais.html', methods=['GET'])
def tais():
    return render_template('./cps/tais.html')

@app.route('/cps/tais_t.html', methods=['GET'])
def tais_t():
    return render_template('./cps/tais_t.html', tais=getNodeData('tais', 'T'))

@app.route('/cps/tais_a.html', methods=['GET'])
def tais_a():
    return render_template('./cps/tais_a.html', tais=getNodeData('tais', 'A'))

@app.route('/cps/tais_b.html', methods=['GET'])
def tais_b():
    return render_template('./cps/tais_b.html', tais=getNodeData('tais', 'B'))

@app.route('/mas.html', methods=['GET'])
def mas():
    return render_template('./cps/mas.html')

@app.route('/cps/mas_t.html', methods=['GET'])
def mas_t():
    return render_template('./cps/mas_t.html', mas=getNodeData('mas', 'T'))

@app.route('/cps/mas_a.html', methods=['GET'])
def mas_a():
    return render_template('./cps/mas_a.html', mas=getNodeData('mas', 'A'))

@app.route('/cps/mas_b.html', methods=['GET'])
def mas_b():
    return render_template('./cps/mas_b.html', mas=getNodeData('mas', 'B'))

@app.route('/aps.html', methods=['GET'])
def aps():
    return render_template('./cps/aps.html')

@app.route('/cps/aps_t.html', methods=['GET'])
def aps_t():
    return render_template('./cps/aps_t.html', aps=getNodeData('aps', 'T'))

@app.route('/cps/aps_a.html', methods=['GET'])
def aps_a():
    return render_template('./cps/aps_a.html', aps=getNodeData('aps', 'A'))

@app.route('/cps/aps_b.html', methods=['GET'])
def aps_b():
    return render_template('./cps/aps_b.html', aps=getNodeData('aps', 'B'))

@app.route('/cups_cp.html', methods=['GET'])
def cups_cp():
    return render_template('./bgw/cups_cp.html', cups_cp=getBgwData('cups_cp'))

@app.route('/cups_cnp.html', methods=['GET'])
def cups_cnp():
    return render_template('./bgw/cups_cnp.html', cups_cnp=getBgwData('cups_cnp'))

@app.route('/cups_kj.html', methods=['GET'])
def cups_kj():
    return render_template('./bgw/cups_kj.html', cups_kj=getBgwData('cups_kj'))

@app.route('/icbc_sh_kj.html', methods=['GET'])
def icbc_sh_kj():
    return render_template('./bgw/icbc_sh_kj.html', icbc_sh_kj=getBgwData('icbc_sh_kj'))

@app.route('/abc_sz_kj.html', methods=['GET'])
def abc_sz_kj():
    return render_template('./bgw/abc_sz_kj.html', abc_sz_kj=getBgwData('abc_sz_kj'))

@app.route('/cps/T.htm', methods=['GET'])
def T():
    return render_template('./cps/T.htm')

@app.route('/cps/A.htm', methods=['GET'])
def A():
    return render_template('./cps/A.htm')

@app.route('/cps/B.htm', methods=['GET'])
def B():
    return render_template('./cps/B.htm')

@app.route('/cps/ip_tais_t.html', methods=['GET'])
def ip_tais_t():
    return render_template('./cps/ip_tais_t.html', tais=getNodeData('tais', 'T'))

@app.route('/cps/ip_tais_a.html', methods=['GET'])
def ip_tais_a():
    return render_template('./cps/ip_tais_a.html', tais=getNodeData('tais', 'A'))

@app.route('/cps/ip_tais_b.html', methods=['GET'])
def ip_tais_b():
    return render_template('./cps/ip_tais_b.html', tais=getNodeData('tais', 'B'))

@app.route('/cps/ip_mas_t.html', methods=['GET'])
def ip_mas_t():
    return render_template('./cps/ip_mas_t.html', mas=getSumData('mas', 'T'))

@app.route('/cps/ip_mas_a.html', methods=['GET'])
def ip_mas_a():
    return render_template('./cps/ip_mas_a.html', mas=getSumData('mas', 'A'))

@app.route('/cps/ip_mas_b.html', methods=['GET'])
def ip_mas_b():
    return render_template('./cps/ip_mas_b.html', mas=getSumData('mas', 'B'))

@app.route('/cps/ip_aps_t.html', methods=['GET'])
def ip_aps_t():
    return render_template('./cps/ip_aps_t.html', aps=getSumData('aps', 'T'))

@app.route('/cps/ip_aps_a.html', methods=['GET'])
def ip_aps_a():
    return render_template('./cps/ip_aps_a.html', aps=getSumData('aps', 'A'))

@app.route('/cps/ip_aps_b.html', methods=['GET'])
def ip_aps_b():
    return render_template('./cps/ip_aps_b.html', aps=getSumData('aps', 'B'))

@app.route('/cps/queue_t.html', methods=['GET'])
def queue_t():
    data = []
    for i in ['bgw', 'cis', 'internal', 'mas', 'tais']:
        data.extend(getQueueData(i, 'T'))
    return render_template('./cps/queue_t.html', queue=data)

@app.route('/cps/queue_a.html', methods=['GET'])
def queue_a():
    data = []
    for i in ['bgw', 'cis', 'internal', 'mas', 'tais']:
        data.extend(getQueueData(i, 'A'))
    return render_template('./cps/queue_a.html', queue=data)

@app.route('/cps/queue_b.html', methods=['GET'])
def queue_b():
    data = []
    for i in ['bgw', 'cis', 'internal', 'mas', 'tais']:
        data.extend(getQueueData(i, 'B'))
    return render_template('./cps/queue_b.html', queue=data)

@app.route('/alert.htm', methods=['GET'])
def alert():
    return render_template('alert.htm', alert=text2html())

@app.route('/sla_bgw.html', methods=['GET'])
def sla_bgw():
    data=getSlaData('cups_cp')
    data.extend(getSlaData('cups_cnp'))
    data.extend(getSlaData('icbc_sh_kj'))
    data.extend(getSlaData('abc_sz_kj'))
    return render_template('./cps/sla_bgw.html', data=data)

@app.route('/sla_aps.html', methods=['GET'])
def sla_aps():
    return render_template('./cps/sla_aps.html', data=getSlaData('aps'))

@app.route('/sla_mas.html', methods=['GET'])
def sla_mas():
    return render_template('./cps/sla_mas.html', data=getSlaData('mas'))

@app.route('/time.htm', methods=['GET'])
def getTime():
    return render_template('time.htm', time=time.strftime("%d %H:%M:%S", time.localtime()))

@app.route('/test.htm', methods=['GET'])
def test():
    return os.getcwd()

@app.route('/monitor.html', methods=['GET'])
def monitor():
    return render_template('monitor.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8888, debug=True)
