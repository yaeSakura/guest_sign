#! /usr/bin/env python 
# -*- coding:utf-8 -*-

from celery import Celery

app = Celery('tasks',
             broker='amqp://admin:admin@138.128.220.107:5672//',
             # backend='amqp://admin:admin@138.128.220.107:5672//',
             backend='amqp',
             )

@app.task
def add(x,y):
    print("running...",x,y)
    return x+y

# app = Celery('hello', broker='amqp://guest@localhost//')