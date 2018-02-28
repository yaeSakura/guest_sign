#! /usr/bin/env python 
# -*- coding:utf-8 -*-

from celery import task

@task
def add(x,y):
    return x + y