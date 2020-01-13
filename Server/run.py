# -*- coding: utf-8 -*-
# @File        : run.py
# @Author      : Yuchen Chai
# @Date        : 2019/12/19 10:36
# @Description : 服务器启动运行
import os
import sys
print(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(r"C:\Users\Administrator\Desktop\TransportTradition")

from Server import app
import Server.views
import Server.TransportationPredict_Tradition.BusStop
from Server.logger import logger
from Server.settings import SERVER_HOST, SERVER_PORT

logger.info("启动服务器")
app.run(host=SERVER_HOST, port=SERVER_PORT, debug=False, threaded=True)
