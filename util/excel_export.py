#! /usr/bin/env python 
# -*- coding:utf-8 -*-

from functools import reduce
import os
import logging
import xlwt
from datetime import datetime
from django.conf import settings

logger = logging.getLogger('djnago')

def export(sub_dir, file_name, data, column_names=None):
    """
    export data to file_name
    :param sub_dir:
    :param file_name:
    :param data:
    :param column_names:
    :return:
    """
    logger.debug(data)
    folder = 'excel_exported'
    file_name = datetime.now().strftime("%Y%m%d%H%M%S_") + file_name + '.xls'

    dir_path = os.path.join(settings.MEDIA_ROOT, folder, sub_dir)
    os.makedirs(dir_path, exist_ok=True)
    path = os.path.join(dir_path, file_name)
    logger.info(path)

    wb = xlwt.Workbook()
    ws = wb.add_sheet('数据导出')

    for i, name in enumerate(column_names):
        ws.write(0, i, name)

    for row_num, row_data in enumerate(data, start=1):
        for col_num, col_data in enumerate(row_data):
            logger.debug((row_num, col_num, col_data))
            ws.write(row_num, col_num, col_data)

    wb.save(path)

    logger.debug(settings.BASE_DIR)
    logger.debug(path)

    return path.replace(settings.BASE_DIR, "")

def queryset_to_data(queryset, attr_list):
    a = [list(map(str, [getattr(e, attr, None) for attr in attr_list])) for e in queryset]
    # print(a)
    return a


