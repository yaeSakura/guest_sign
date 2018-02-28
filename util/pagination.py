#! /usr/bin/env python 
# -*- coding:utf-8 -*-

import logging
import math
from collections import OrderedDict
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

logger = logging.getLogger(__name__)

class StandardPagination(PageNumberPagination):
    # 设定请求中每页显示数据的条数，如果请求中有的话，不能超过max_page_size
    page_size_query_param = 'per_page'
    max_page_size = 10

    def paginate_queryset(self, queryset, request, *args, **kwargs):
        # 获取当前页数‘page’，默认为第1页
        self.page_number = request.query_params.get(self.page_query_param, 1)
        # 获取请求的每页最大数据条数， ‘per_page’如果请求中有的话
        self.page_size = self.get_page_size(request)
        return super().paginate_queryset(queryset, request, *args, **kwargs)

    def get_paginated_response(self, data):
        self.count = self.page.paginator.count
        return Response(data=OrderedDict([
            ('per_page', self.page_size),
            ('count', self.count),
            ('page', self.page_number),
            ('total_page', math.ceil(self.count / self.page_size)),
            ('results', data)
        ]))

class ForkNonePagination(StandardPagination):
    page_size = 3