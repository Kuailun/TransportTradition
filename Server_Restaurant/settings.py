# -*- coding: utf-8 -*-
# @File       : settings.py
# @Author     : Yuchen Chai
# @Date       : 2020/3/21 13:40
# @Description:

import os

# -----------------------------------------------------------------------------
# 服务器运行的设置
# -----------------------------------------------------------------------------
SERVER_HOST = '0.0.0.0'
SERVER_PATH = os.path.dirname(os.path.realpath(__file__))
# 服务器运行模式： NORMAL, TEST
SERVER_MODE = "NORMAL"
SERVER_PORT = 0
if SERVER_MODE == "NORMAL":
    SERVER_PORT = 2002
elif SERVER_MODE == "TEST":
    SERVER_PORT = 0
else:
    raise("SERVER模式错误！")

# -----------------------------------------------------------------------------
# 日志记录的设置
# -----------------------------------------------------------------------------
# 是否输出到控制台
LOGGING_CONSOLE_FLAG = True

# 是否输出到文件
LOGGING_FILE_LOG = True

# 输出日志的等级
LOGGING_LEVEL = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
LOGGING_CURRENT_LEVEL = LOGGING_LEVEL[1]

# -----------------------------------------------------------------------------
# 用户数据库的设置
# -----------------------------------------------------------------------------
RESTAURANT_DATABASE_NAME = 'Restaurant.csv'
RESTAURANT_DATABASE_PATH = SERVER_PATH + "/Database/"