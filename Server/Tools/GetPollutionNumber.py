# -*- coding: utf-8 -*-
# @File       : GetPollutionNumber.py
# @Author     : Yuchen Chai
# @Date       : 2020/1/9 14:59
# @Description: 获取污染信息，发送到服务器

import os
import sys
print(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(r"C:\Users\Administrator\Desktop\TransportTradition")
import requests
from pyquery import PyQuery as pq
from Server import settings as ss
from Server.logger import logger
import Server.Utils as ut
import time
import json

# 爬虫目标网址
targetUrl = 'http://www.pm25.in/zhengzhou'

def _Pollution_Post(p_data):
    '''
    将所得的数据发送到服务器的指定接口
    :param p_data:
    :return:
    '''

    data = {
        'pollution': json.dumps(p_data),
    }

    _ = requests.post('http://127.0.0.1:2000/submit/pollution', data = data)

    pass

def _Pollution_Analyze(p_content):
    '''
    解析获得的网络内容
    :param p_content:
    :return:
    '''

    # 如果网站爬取出现问题，返回默认值
    if not p_content.status_code == 200:
        logger.warning(r"污染数据爬取错误，回复代码 {0}".format(str(p_content.status_code)))
        return ss.POLLUTIONEXPOSURE_DEFAULT_DATA

    # 将获得的网站转为pyquery对象
    doc = pq(p_content.text)
    items = doc('.span1')

    # 如果返回的数据量不为标准的9个
    if not len(items) == 9:
        logger.warning(r"污染数据爬取错误，所含项目数少于9")
        return ss.POLLUTIONEXPOSURE_DEFAULT_DATA

    # 第9项非数据，需要排除
    index = 0
    newItem = ut.Get_Current_Timestamp_Rounded()
    for item in items:
        if (index < 8):
            # 将子项再归为pq对象
            item = pq(item)
            value = item.text()
            value = value.split('\n')
            newItem.append(float(value[0]))
            pass
        index += 1
        pass

    return newItem


logger.info(r'开始爬取污染数据，定时间隔为：{0} min'.format(str(ss.POLLUTIONEXPOSURE_PM25_INTERVAL // 60)))

while(True):

    try:
        # 从网页获取需要分析的数据
        response = requests.get(url=targetUrl)

        # 返回分析好的数据
        newItem = _Pollution_Analyze(response)
        logger.debug(r"爬取污染数据，最新污染值为: {0}   PM2.5: {1} ".format(newItem[0], newItem[2]))

        # 发送数据到服务器
        _Pollution_Post(newItem)

        # 等待，定时间隔
        time.sleep(ss.POLLUTIONEXPOSURE_PM25_INTERVAL)

    except:
        logger.warning(r'发生错误')

    pass