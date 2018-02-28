#! /usr/bin/env python 
# -*- coding:utf-8 -*-

import json
import logging
import datetime

from .models import Pikamsg

logger = logging.getLogger(__name__)

def process_message(msg:str):
    # print('msg is ',msg)
    if type(msg) == bytes:
        msg = msg.decode('utf8')
    msg_dic = json.loads(msg)
    logger.info(msg_dic)
    # print('msg_dic is', msg_dic)

    Pikamsg.objects.create(
        msg = msg_dic['msg'],
        time = msg_dic['time'],
    )
