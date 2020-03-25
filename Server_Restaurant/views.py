# -*- coding: utf-8 -*-
# @File        : views.py
# @Author      : Yuchen Chai
# @Date        : 2019/12/19 10:33
# @Description : 接口的定义
from Server_Restaurant import app
from flask import request,jsonify,redirect
from Server_Restaurant.logger import logger
from Server_Restaurant.restaurant import restaurant

def after_request(resp):
    resp.headers['Access-Control-Allow-Origin']='*'
    return resp
app.after_request(after_request)

@app.before_request
def before_request():
    """
    获取请求内容
    @return:
    """
    if request.path == "/restaurant":
        if request.method == "POST":
            return
    elif request.path == "/":
        return
    return redirect("/")

# 获取餐厅信息
@app.route('/restaurant', methods=['POST'])
def Restaurant():
    code, msg, data = restaurant.Restaurant_Interface(request.form)

    response = {
        'code': code,
        'msg': msg,
        'data': data
    }
    return jsonify(response), 200


@app.route("/",methods = ['GET',"POST"])
def default():
    return "Error",404