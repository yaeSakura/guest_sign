#! /usr/bin/env python 
# -*- coding:utf-8 -*-
from rest_framework.response import Response
from django.http import Http404
import logging

logger = logging.getLogger(__name__)

def get_obj(instance_class, id):
    if not id or not instance_class:
        return None
    try:
        instance = instance_class.objects.get(id =id)
    except instance_class.DoesNotExist:
        raise Http404('对象不存在')
    return instance

class JsonResponse(Response):
    def __init__(self, msg=None, code=200, data=None):
        data = {
            'code': code,
            'msg': msg,
            'data': data}
        # return super().__init__(data, status=200)
        super(JsonResponse, self).__init__(data)