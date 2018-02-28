#! /usr/bin/env python 
# -*- coding:utf-8 -*-

import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'guest.settings')
app = Celery('guest')

app.config_from_object('djnago.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))