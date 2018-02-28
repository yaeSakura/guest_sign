#! /usr/bin/env python 
# -*- coding:utf-8 -*-

import sys
import pika

message = ' '.join(sys.argv[1:]) or "Hello World!"

credentials = pika.PlainCredentials("admin", "admin")
connection = pika.BlockingConnection(pika.ConnectionParameters(
    "138.128.220.107",
    credentials=credentials,
))

channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True)

channel.basic_publish(exchange='',
                      routing_key='task_queue',
                      body=message,
                      properties=pika.BasicProperties(
                          delivery_mode=2,
                      ))

print(" [x] Sent %r" % message)

connection.close()