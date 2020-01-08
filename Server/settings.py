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
SERVER_PATH = os.path.dirname(os.path.realpath(__file__))

# -----------------------------------------------------------------------------
# 高德路线查询的设置
# -----------------------------------------------------------------------------
AMAP_SERVER_KEY = '00bf37c00932a5a32b1e7810b719d87f'
# 0：最快捷模式;1：最经济模式;2：最少换乘模式;3：最少步行模式;5：不乘地铁模式
AMAP_SERVER_STRATEGY = 0
AMAP_LOCATION_LON_MIN = 113.419367
AMAP_LOCATION_LON_MAX = 113.757247
AMAP_LOCATION_LAT_MIN = 34.673106
AMAP_LOCATION_LAT_MAX = 34.768841
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
REGISTERATION_SERVICE_KEYWORDS = ['command']

# -----------------------------------------------------------------------------
# 污染数据库的设置
# -----------------------------------------------------------------------------
POLLUTIONEXPOSURE_DATABASE_NAME = 'PollutionExposure.xls'
POLLUTIONEXPOSURE_DATABASE_PATH = SERVER_PATH + "/Database/"
POLLUTIONEXPOSURE_DATABASE_KEYWORDS = ['userId']
POLLUTIONEXPOSURE_DEFAULT_DATA = ['2019-12-01 00:00:00', 00000.0000000000, 0, 0, 0, 0, 0, 0, 0, 0]
# 污染数据爬虫间隔时间（秒 sec）
POLLUTIONEXPOSURE_PM25_INTERVAL = 5
POLLUTIONEXPOSURE_PM25_TIMEOUT = 5
POLLUTIONEXPOSURE_INTERFACE_KEYWORDS = ['userId']

# -----------------------------------------------------------------------------
# GPS预测的设置
# -----------------------------------------------------------------------------
PREDICTION_INTERFACE_KEYWORDS = ['userId', 'travel_data']
PREDICTION_GPS_PREDICTION_KEYWORDS = ['id', 'accelerationX', 'accelerationY', 'accelerationZ', 'angleAccX', 'angleAccY',
                                      'angleAccZ', 'angleX', 'angleY', 'angleZ', 'direction', 'elevation', 'label',
                                      'latitude', 'longitude', 'timestamp', 'datestamp', 'velocity', 'star', 'locationType']
PREDICTION_GPS_REAL_KEYWORDS = ['latitude', 'longitude', 'velocity', 'star', 'id', 'timestamp', 'datestamp', 'label']
PREDICTION_INTERFACE_DICT = {'static': 1,'walk': 2, 'bike': 3, 'bus': 4, 'subway': 5, 'car': 6, 'non-walk': 7}

# 速度上限 m/s
PREDICTION_GPS_FILTER_SPEED_MAXIMUM = 50
# GPS定位星数下限
PREDICTION_GPS_FILTER_STAR_MINIMUM = 5
# 旅程分段的时间上限，数据间隔超过该值则分为2段不相关的旅程
PREDICTION_GPS_SEGMENT_INTERVAL_MAXIMUM = 120
# 有效旅程的GPS数据下限，少于该值则删除本段旅程
PREDICTION_GPS_SEGMENT_DATA_MINIMUM = 10
# 识别为走路的最高速度
PREDICTION_GPS_CALCULATE_WALK_VELOCITY_MAXIMUM = 1.8
# 识别为走路的最高加速度
PREDICTION_GPS_CALCULATE_WALK_ACCELERATION_MAXIMUM = 0.6
#
PREDICTION_GPS_CALCULATE_WALK_DISTANCE_MAXIMUM = 50
# 一段旅程最少数据个数
PREDICTION_GPS_CALCULATE_TRIP_SAMPLE_MINIMUM = 20
# 在计算时，看前面几个及后面几个当中是否达到阈值
PREDICTION_GPS_CALCULATE_MODE_RANGE = 10
# 在计算中，看前面几个及后面几个当中是否达到阈值
PREDICTION_GPS_CALCULATE_MODE_SCALE = 0.7

