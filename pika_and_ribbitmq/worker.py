#! /usr/bin/env python 
# -*- coding:utf-8 -*-

import pika
import time

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    time.sleep(body.count(b'.'))
    print(" [x] Done")
    ch.basic_ack(delivery_tag=method.delivery_tag)

credentials = pika.PlainCredentials("admin", "admin")
connection = pika.BlockingConnection(pika.ConnectionParameters(
    "138.128.220.107",
    credentials=credentials,
))

channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True)

print(' [*] Waiting for logs. To exit press CTRL+C')

channel.basic_qos(prefetch_count=1)
channel.basic_consume(callback, queue='task_queue')
channel.start_consuming()