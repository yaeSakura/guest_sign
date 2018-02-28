#! /usr/bin/env python 
# -*- coding:utf-8 -*-

from sign.models import Guest
from rest_framework import serializers

class GuestSerializer(serializers.ModelSerializer):
    '''签到用户序列化'''
    class Meta:
        model = Guest
        fields = '__all__'
        read_only_fields = ('create_time',)


