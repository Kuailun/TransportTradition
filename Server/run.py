# -*- coding: utf-8 -*-
# @File        : run.py
# @Author      : Yuchen Chai
# @Date        : 2019/12/19 10:36
# @Description : 服务器启动运行
import os
import sys
import settings
print(os.path.dirname(os.path.realpath(__file__)))
print("当前服务器运行模式为：{0}".format(settings.SERVER_MODE))
if settings.SERVER_MODE == "NORMAL":
    sys.path.append(r"C:\Users\Administrator\Desktop\TransportTradition")
elif settings.SERVER_MODE == "TEST":
    sys.path.append(r"C:\Users\Administrator\Desktop\TransportTradition-Test")

from Server import app
import Server.views
import Server.TransportationPredict_Tradition.BusStop
from Server.logger import logger
from Server.settings import SERVER_HOST, SERVER_PORT

logger.info("启动服务器")
app.run(host=SERVER_HOST, port=SERVER_PORT, debug=False, threaded=True)
