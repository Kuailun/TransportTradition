# -*- coding: utf-8 -*-
# @File     : Unicode2UTF8.py
# @Author   : Yuchen Chai
# @Date     : 2019/12/17 20:54

import json as js

f=open('busStops.json',encoding='utf-8')
data=js.load(f)

busStops=[]
for i in range(len(data)):
    for j in range(len(data[i]['data'])):
        if data[i]['data'][j]['name'] not in busStops:
            busStops.append(data[i]['data'][j]['name'])
            pass
        pass
    pass

busStops.sort()

print()