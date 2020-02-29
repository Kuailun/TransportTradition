# -*- coding: utf-8 -*-
# @File     : Try.py
# @Author   : Yuchen Chai
# @Date     : 2019/12/17 22:02

from geopy.distance import vincenty

name='一马路陇海路（公交站）'
GPS_AMAP=(34.744804,113.756796)
GPS_API=(34.13276,114.711143)
# GPS_Jianghao=(34.740044,113.66481)

Distance_12=vincenty(GPS_AMAP,GPS_API).meters
# Distance_13=vincenty(GPS_AMAP,GPS_Jianghao).meters
# Distance_23=vincenty(GPS_API,GPS_Jianghao).meters

print("站点名称： ", name)
print("高德地图在线查询-高德地图API查询： ", Distance_12)
# print("高德地图在线查询-jianghao 数据库： ", Distance_13)
# print("高德地图API查询-jianghao 数据库： ", Distance_23)