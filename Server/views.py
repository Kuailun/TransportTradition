# -*- coding: utf-8 -*-
# @File        : views.py
# @Author      : Yuchen Chai
# @Date        : 2019/12/19 10:33
# @Description : 接口的定义

from Server import app
from flask import request,jsonify
from Server.Registeration.Registeration import registeration
from Server.PollutionExposure.interface import Pollution_Interface
from Server.TransportationPredict_Tradition.interface import GPS_Interface

# 注册/修改用户的注册信息
@app.route('/registeration', methods=['POST'])
def Registeration():
    code, msg = registeration.Registeration_Interface(request.form)

    response = {
        'code': code,
        'msg': msg
    }
    return jsonify(response), 200

@app.route('/pollutionexposure',methods=['POST'])
def Pollutionexposure():
    code, msg, data = Pollution_Interface(request.form)

    response = {
        'code': code,
        'msg': msg,
        'data':data
    }
    return jsonify(response), 200

@app.route('/gps',methods=['POST'])
def Gps():
    code, msg, data = GPS_Interface(request.form)

    response = {
        'code': code,
        'msg': msg,
        'data': data
    }
    return jsonify(response), 200