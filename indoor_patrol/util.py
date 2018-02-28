#! /usr/bin/env python 
# -*- coding:utf-8 -*-
import json
import time
from indoor_patrol.models import Record

def save_spot_msg(msg):
    if len(msg) > 0:
        # print("Received %r" % msg)
        body = msg.decode('utf8')
        msg = json.loads(body)
        time_spot = time.strptime(msg['time'], "%a %b  %d %H:%M:%S %Y")
        time_spot = time.strftime("%Y-%m-%d %H:%M:%S", time_spot)
        try:
            Record.objects.create(dvice_id=msg['DviceID'],
                                  spot=msg['Spot'].replace('0x', '00'),
                                  time=time_spot,
                                  events=msg['events'])
        except Exception as e:
            print('Record save error!', e)
    else:
        print('Post record null')