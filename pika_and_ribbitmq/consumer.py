#! /usr/bin/env python 
# -*- coding:utf-8 -*-
import pika


def callback(ch, method, properties, body):
    print("Received %r" % body)


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
