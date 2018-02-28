#! /usr/bin/env python 
# -*- coding:utf-8 -*-

from __future__ import absolute_import, unicode_literals
from celery import Celery

app = Celery('proj',
             broker='amqp://admin:admin@138.128.220.107:5672//',
             backend='amqp://admin:admin@138.128.220.107:5672//',
             include=['proj.tasks'])

app.conf.update(
    result_expires=3600,
)

if __name__ == '__main__':
    app.start()