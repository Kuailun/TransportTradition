# -*- coding: utf-8 -*-
# @File       : POI.py
# @Author     : Yuchen Chai
# @Date       : 2020/3/15 13:15
# @Description: 检测用户一天内是否在兴趣点的算法

from Tools import CommonTools as ct
from geopy.distance import vincenty
import numpy as np

##################################################
# 设置区域
##################################################

# 每段时间的最少点数
DATAPOINTS_MIN = 30

# 对于POI中的不同层级兴趣点，定义作用范围（单位：米）
distance = {"First":100, "Second":100, "Third":1000}

# 准备时间分段
timePeriod = {"0700":25200,"0900":32400,
              "0911":33060,"0921":33660,"0931":34260,"0941":34860,"0951":35460,"1001":36060,
              "1011":36660,"1021":37260,"1031":37860,"1041":38460,"1051":39060,"1101":39660,
              "1111":40260,"1121":40860,"1131":41460,"1141":42060,"1151":42660,"1201":43260,
              "1211":43860,"1221":44460,"1231":45060,"1241":45660,"1251":46260,"1301":46860,
              "1311":47460,"1321":48060,"1331":48660,"1341":49260,"1351":49860,"1401":50460,
              "1411":51060,"1421":51660,"1431":52260,"1441":52860,"1451":53460,"1501":54060,
              "1511":54660,"1521":55260,"1531":55860,"1541":56460,"1551":57060,"1601":57660,
              "1611":58260,"1621":58860,"1631":59460,"1641":60060,"1651":60660,"1900":68400,
              }

def getTime(p_timePeriod, record):
    """
    根据第一条时间戳，得到当前日期，更新所有时间分段
    @param timePeriod:
    @param record:
    @return:
    """
    period = p_timePeriod.copy()

    date = record['datestamp'].split(" ")[0]
    datebase = ct.TimeStr_TimeStamp(date + " 00:00:01")

    for item in period:
        period[item] = period[item] + datebase
        pass

    return period

def getData(p_gpsdata, p_timezone):
    """
    将得到的gps数据根据时间进行分段
    @param p_gpsdata:
    @param p_timezone:
    @return:
    """
    ret_data = p_timezone.copy()

    # 清空回传数据中的空间
    for item in ret_data:
        ret_data[item] = []
        pass

    index = 0
    for item in ret_data:
        while index < len(p_gpsdata) and (ct.TimeStr_TimeStamp(p_gpsdata[index]['datestamp']) < p_timezone[item]):
            ret_data[item].append(p_gpsdata[index])
            index = index + 1
            pass
        pass
    return ret_data

def getPotential(p_data, p_poi):
    """
    根据当前时间多，判断用户可能在的地方
    @param p_data:
    @param p_poi:
    @return:
    """
    # First
    Home = (p_poi['First'][0]['Latitude'],p_poi['First'][0]['Longitude'])
    Home_count = 0
    Office = (p_poi['First'][1]['Latitude'],p_poi['First'][1]['Longitude'])
    Office_count = 0
    dataLength = len(p_data)

    ret_data = {"First":[],"Second":[],"Third":[]}

    secondarray = []
    thirdarray = []

    for i in range(len(p_data)):
        dist = vincenty(Home, (p_data[i]["latitude"],p_data[i]['longitude'])).meters
        if dist <= distance['First']:
            Home_count = Home_count + 1
            pass

        dist = vincenty(Office, (p_data[i]["latitude"], p_data[i]['longitude'])).meters
        if dist <= distance['First']:
            Office_count = Office_count + 1
            pass
        pass

    # Second
    if not len(p_poi['Second']) == 0:
        secondarray = np.zeros(len(p_poi['Second']))
        for i in range(len(p_data)):
            for j in range(len(p_poi['Second'])):
                dist = vincenty((p_poi['Second'][j]["Latitude"],p_poi['Second'][j]['Longitude']),(p_data[i]["latitude"],p_data[i]['longitude'])).meters
                if dist <= distance['Second']:
                    secondarray[j] = secondarray[j] + 1
                    pass
                pass
            pass
        pass

    # Third
    if not len(p_poi['Third']) == 0:
        thirdarray = np.zeros(len(p_poi['Third']))
        for i in range(len(p_data)):
            for j in range(len(p_poi['Third'])):
                dist = vincenty((p_poi['Third'][j]["Latitude"],p_poi['Third'][j]['Longitude']),(p_data[i]["latitude"],p_data[i]['longitude'])).meters
                if dist <= distance['Third']:
                    thirdarray[j] = thirdarray[j] + 1
                    pass
                pass
            pass
        pass

    # 中间时段获取的数据
    if dataLength <= 60:
        if Home_count >= 40:
            ret_data['First'].append("Home")
            pass

        if Office_count >= 40:
            ret_data['First'].append("Office")
            pass

        for i in range(len(secondarray)):
            if secondarray[i] >= 40:
                ret_data['Second'].append(p_poi["Second"][i])
                pass
            pass

        for i in range(len(thirdarray)):
            if thirdarray[i] >= 40:
                ret_data['Third'].append(p_poi["Third"][i])
                pass
            pass
        pass
    # 前后长时间获取的数据
    else:
        if Home_count >= 300 or Home_count/dataLength >=0.7:
            ret_data['First'].append("Home")
            pass

        if Office_count >= 300 or Office_count/dataLength >= 0.7:
            ret_data['First'].append("Office")
            pass

        for i in range(len(secondarray)):
            if secondarray[i] >= 300 or secondarray[i]/dataLength >= 0.7:
                ret_data['Second'].append(p_poi["Second"][i])
                pass
            pass

        for i in range(len(thirdarray)):
            if thirdarray[i] >= 300 or thirdarray[i]/dataLength >= 0.7:
                ret_data['Third'].append(p_poi["Third"][i])
                pass
            pass
        pass

    return ret_data



def POI(userRegistrationData, userGPSData, poiData):
    """
    检测用户一天内是否在兴趣点
    @param userRegistrationData: 用户注册时的数据，需要家的地址、公司的地址
    @param userGPSData: 用户当天所有gps轨迹数据
    @param poiData: 兴趣点列表
    @return:
    """
    # 更新poi中家庭、公司poi
    poiData["First"] = [
        {
            "Name":"Home",
            "Latitude":userRegistrationData['hLat'],
            "Longitude":userRegistrationData['hLon']
        },
        {
            "Name":"Office",
            "Latitude":userRegistrationData['oLat'],
            "Longitude":userRegistrationData['oLon']
        }
    ]

    # 获得时间分段
    timezone = getTime(timePeriod, userGPSData[0])

    # 获得数据分段
    datapiece = getData(userGPSData, timezone)

    # 候选兴趣点
    potential_points = {}
    for item in datapiece:
        temp_result = []
        if len(datapiece[item]) <= DATAPOINTS_MIN:
            pass
        else:
            temp_result = getPotential(datapiece[item], poiData)
            pass
        potential_points[item] = temp_result
        pass
    print(1)
    pass



userRegistrationData = {
    "Name":"柴宇宸",
    "UserID": 40,
    "hLat": 34.737695,
    "hLon": 113.766494,
    "oLat": 42.389163,
    "oLon": -71.121550
}

userGPSData = ct.read_json("C:\\Users\\59367\Desktop\\40.txt")

# poiData = {
#     "First":[
#         {
#             "Name":"Home",
#             "Latitude":0,
#             "Longitude":0
#         },
#         {
#             "Name":"Office",
#             "Latitude":0,
#             "Longitude":0
#         }
#     ],
#     "Second":[
#         {
#             "Name":"测试餐馆",
#             "Latitude":42.359163,
#             "Longitude":-71.101550
#         }
#     ],
#     "Third":[
#     {
#             "Name":"测试公园",
#             "Latitude":42.360163,
#             "Longitude":-71.111550
#         }
#     ]
# }
poiData = ct.read_json("F:\\WorkSpace\\python\\TransportTradition\\Algorithm\\top_restaurant.json")

POI(userRegistrationData,userGPSData,poiData)