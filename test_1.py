#! /usr/bin/env python 
# -*- coding:utf-8 -*-

# import copy
# origin = [1,2,[3,4]]
#
# cop1 = copy.copy(origin)
# cop2 = copy.deepcopy(origin)
#
# origin[0] = "hey"
# print(cop1, cop2)
# print(origin)

# import time
#
# a = time.time()
# print(a)

# from collections import OrderedDict
# data=OrderedDict([
#             ('per_page', 10),
#             ('count', 30),
#             ('page', 3),
#             ('total_page', 3),
#             ('results', 'data')
#         ])
#
# print(data)

# a = {1:'a',2:'b',3:'c',4:'d'}
# print(*a[1])

# import math
# print(math.ceil(3/2.5))

# import datetime
# a = '2017-12-26 09:11:06.054987'
# now = datetime.datetime.now()
# print(now,type(now))
# b = datetime.datetime.strptime(a ,'%Y-%m-%d %H:%M:%S')
# print(b)

# import sys
# a = sys.argv[1:]
# print(a)
import time
time1 = "Fri Jan  5 14:35:17 2018"
a1 = time.strptime(time1, "%a %b  %d %H:%M:%S %Y")
a2 = time.strftime("%Y-%m-%d %H:%M:%S", a1)

print(a2)

# a2 = time1.format("%Y-%m-%d %H:%M:%S")
# print(a2)