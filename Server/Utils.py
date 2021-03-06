# -*- coding: utf-8 -*-
# @File       : Utils.py
# @Author     : Yuchen Chai
# @Date       : 2019/12/22 14:08
# @Description:

from datetime import datetime
import time
from Server import settings as ss
def Get_Current_Timestamp_Rounded():
    '''
    获得当前的时间戳，且取整到整数小时
    :return:
    '''
    dateTimeObj=datetime.now()

    # 获取当前的取整时间
    date_format="%Y-%m-%d %H:%M:%S"
    current = dateTimeObj.strftime("%Y-%m-%d %H:00:00")
    default = ss.POLLUTIONEXPOSURE_DEFAULT_DATA[0]

    # 计算与标准时间的时间戳
    currentTime = datetime.strptime(current, date_format)
    defaultTime = datetime.strptime(default, date_format)
    no_days = currentTime-defaultTime

    delta_time=no_days.days+currentTime.hour/24.0

    return [current, delta_time]

def Get_Today_Date():
    """
    获取当日的日期
    """
    today = time.strftime("%Y-%m-%d", time.localtime())
    return today

def Get_Day_Of_Week():
    """
    获取当天是星期几
    """
    dayOfWeek = datetime.now().isoweekday() - 1
    return dayOfWeek

def TimeStr_TimeStamp(p_str):
    """
    时间字符串转时间戳
    @return:
    """
    timeArray = time.strptime(p_str, "%Y-%m-%d %H:%M:%S")
    timeStamp = int(time.mktime(timeArray))
    return timeStamp