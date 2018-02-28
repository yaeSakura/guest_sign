#! /usr/bin/env python 
# -*- coding:utf-8 -*-
import pika
import json
import time
from indoor_patrol.models import Record

def consumer():
    def callback(ch, method, properties, body):
        if len(body) > 0:
            print("Received %r" % body)
            body = body.decode('utf8')
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
            print('Record null')

    credentials = pika.PlainCredentials("admin", "admin")
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        "138.128.220.107",
        credentials=credentials,
    ))
    channel = connection.channel()

    # 声明交换机
    channel.exchange_declare(exchange='hzqtest', exchange_type='direct', passive=False, durable=True, auto_delete=False)

    channel.queue_declare(queue='patrol')
    channel.queue_bind(exchange='hzqtest', routing_key='aoi', queue='patrol')
    channel.basic_consume(callback, queue='patrol', no_ack=True)
    channel.start_consuming()
    print('Start consumer...')
