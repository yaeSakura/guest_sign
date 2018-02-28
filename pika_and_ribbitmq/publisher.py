#! /usr/bin/env python 
# -*- coding:utf-8 -*-
import pika

credentials = pika.PlainCredentials("admin", "admin")
connection = pika.BlockingConnection(pika.ConnectionParameters(
    "138.128.220.107",
    credentials=credentials,
))
channel = connection.channel()

# 声明交换机
channel.exchange_declare(exchange='hzqtest', exchange_type='direct', passive=False, durable=True, auto_delete=False)
channel.queue_declare(queue='hello world')
channel.basic_publish(exchange='hzqtest',
                      routing_key='kiana',
                      body="{'name': 'kiana', 'age': 18, 'hobby': 'yuri'}")
connection.close()
print('over')