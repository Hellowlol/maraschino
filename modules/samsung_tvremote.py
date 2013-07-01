#!  /usr/bin/python
#   Title: samsungremote.py
#   Author: Asif Iqbal
#   Date: 05APR2012
#   Info: To send remote control commands to the Samsung tv over LAN
#   TODO:

import socket
import base64
import time, datetime

from flask import *
from Maraschino import app
from maraschino.tools import *
from maraschino import *

# http://wiki.samygo.tv/index.php5/D-Series_Key_Codes

#@requires.auth
@app.route('/xhr/samsung_tvremote/send/<key>/')
def sendKeyz(key):
    
    src = get_setting_value('samsung_tvremote_myip')
    mac = get_setting_value('samsung_tvremote_mymac')
    remote = 'Maraschino remote'
    dst = get_setting_value('samsung_tvremote_tvip')
    application = 'python'
    tv = get_setting_value('samsung_tvremote_tvmodel')
    
    new = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    new.connect((dst, 55000))
    msg = chr(0x64) + chr(0x00) +\
        chr(len(base64.b64encode(src)))    + chr(0x00) + base64.b64encode(src) +\
        chr(len(base64.b64encode(mac)))    + chr(0x00) + base64.b64encode(mac) +\
        chr(len(base64.b64encode(remote))) + chr(0x00) + base64.b64encode(remote)
    pkt = chr(0x00) +\
        chr(len(application)) + chr(0x00) + application +\
        chr(len(msg)) + chr(0x00) + msg
    new.send(pkt)
    msg = chr(0x00) + chr(0x00) + chr(0x00) +\
        chr(len(base64.b64encode(key))) + chr(0x00) + base64.b64encode(key)
    pkt = chr(0x00) +\
        chr(len(tv))  + chr(0x00) + tv +\
        chr(len(msg)) + chr(0x00) + msg
    new.send(pkt)
    new.close()
    time.sleep(0.1)
  
    logger.log('Sending key :: %s' % key, 'INFO')
    #print key
    return render_template('samsung_tvremote.html', key=key)
