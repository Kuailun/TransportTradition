# -*- coding: utf-8 -*-
# @File       : Settings.py
# @Author     : Yuchen Chai
# @Date       : 2019/12/19 11:16
# @Description: 应用的参数设置表

import os

# -----------------------------------------------------------------------------
# 服务器运行的设置
# -----------------------------------------------------------------------------
SERVER_HOST = '0.0.0.0'
SERVER_PORT = 2000
SERVER_PATH = os.getcwd()

# -----------------------------------------------------------------------------
# 日志记录的设置
# -----------------------------------------------------------------------------
# 是否输出到控制台
LOGGING_CONSOLE_FLAG = True

# 是否输出到文件
LOGGING_FILE_LOG = True

# 输出日志的等级
LOGGING_LEVEL = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
LOGGING_CURRENT_LEVEL = LOGGING_LEVEL[0]

# -----------------------------------------------------------------------------
# 用户数据库的设置
# -----------------------------------------------------------------------------
REGISTERATION_DATABASE_NAME = 'UserInfo.xls'
REGISTERATION_DATABASE_PATH = SERVER_PATH + "/Database/"
REGISTERATION_INTERFACE_KEYWORDS = ['userId', 'name', 'tel', 'familyAdd', 'officeAdd', 'flongitude', 'flatitude',
                                    'olongitude', 'olatitude', 'type']

# -----------------------------------------------------------------------------
# 污染数据库的设置
# -----------------------------------------------------------------------------
POLLUTIONEXPOSURE_DATABASE_NAME = 'PollutionExposure.xls'
POLLUTIONEXPOSURE_DATABASE_PATH = SERVER_PATH + "/Database/"
POLLUTIONEXPOSURE_DATABASE_KEYWORDS = ['userId']
POLLUTIONEXPOSURE_DEFAULT_DATA = ['2019-12-01 00:00:00', 00000.0000000000, 0, 0, 0, 0, 0, 0, 0, 0]
# 污染数据爬虫间隔时间（秒 sec）
POLLUTIONEXPOSURE_PM25_INTERVAL = 600
POLLUTIONEXPOSURE_INTERFACE_KEYWORDS = ['userId']

# -----------------------------------------------------------------------------
# GPS预测的设置
# -----------------------------------------------------------------------------
PREDICTION_INTERFACE_KEYWORDS = ['userId', 'travel_data']
PREDICTION_GPS_PREDICTION_KEYWORDS = ['id', 'accelerationX', 'accelerationY', 'accelerationZ', 'angleAccX', 'angleAccY',
                                      'angleAccZ', 'angleX', 'angleY', 'angleZ', 'direction', 'elevation', 'label',
                                      'latitude', 'longitude', 'timestamp','datestamp', 'velocity','star']
PREDICTION_GPS_REAL_KEYWORDS=['latitude','longitude','velocity','star','id','timestamp','datestamp','label']
PREDICTION_INTERFACE_DICT = {'walk':1, 'bike':2, 'bus':3, 'subway':4, 'car':5 }
