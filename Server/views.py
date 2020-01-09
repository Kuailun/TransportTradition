# -*- coding: utf-8 -*-
# @File        : views.py
# @Author      : Yuchen Chai
# @Date        : 2019/12/19 10:33
# @Description : 接口的定义

from Server import app
from flask import request,jsonify
from Server.Registeration.Registeration import registeration
from Server.PollutionExposure.PollutionExposure import pollutionExposure
from Server.TransportationPredict_Tradition.Prediction import prediction

# 注册/修改用户的注册信息
@app.route('/registeration', methods=['POST'])
def Registeration():
    code, msg = registeration.Registeration_Interface(request.form)

    response = {
        'code': code,
        'msg': msg
    }
    return jsonify(response), 200

# 污染暴露信息的获取
@app.route('/pollutionexposure',methods=['POST'])
def Pollutionexposure():
    code, msg, data = pollutionExposure.Pollution_Interface(request.form)

    response = {
        'code': code,
        'msg': msg,
        'data':data
    }
    return jsonify(response), 200

# GPS预测及红包发放
@app.route('/gps',methods=['POST'])
def Gps():
    code, msg, data = prediction.Prediction_Interface(request.form)

    response = {
        'code': code,
        'msg': msg,
        'data': data
    }
    return jsonify(response), 200

# 让用户注册接口暂时停止运行，用于更新
@app.route('/service/userreg',methods = ['POST'])
def UserReg():
    code, msg= registeration.Registeration_Service_Interface(request.form)

    response = {
        'code': code,
        'msg': msg,
    }
    return jsonify(response), 200

# 用于接收最新污染数值
@app.route('/submit/pollution',methods = ['POST'])
def SubmitPollution():
    code, msg= pollutionExposure.Pollution_Submit_Pollution(request.form)

    response = {
        'code': code,
        'msg': msg,
    }
    return jsonify(response), 200

