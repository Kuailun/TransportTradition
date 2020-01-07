from flask import Flask,jsonify,request
import os
import json
import codecs
import xlwt
from flask_apscheduler import APScheduler
import time
import random
import math
from datetime import datetime

app = Flask(__name__)
if not os.path.exists("Database"):
    os.mkdir("Database")
if not os.path.exists("Backup"):
    os.mkdir("Backup")
mID={}

def after_request(resp):
    resp.headers['Access-Control-Allow-Origin']='*'
    return resp
app.after_request(after_request)

def get_json_data(data):
    if (len(data) < 1):
        return ""
    js = ""
    for subdata in data:
        js = subdata
        break

    try:
        json.loads(js)
    except:
        print("Error happens")
        return "";
    return json.loads(js)

def days_date(time_str):
    date_format = "%Y-%m-%d %H:%M:%S"
    current = datetime.strptime(time_str, date_format)
    date_format = "%Y-%m-%d"
    bench = datetime.strptime('1899-12-30', date_format)
    no_days = current - bench
    delta_time_days = no_days.days + current.hour / 24.0 + current.minute / (24. * 60.) + current.second / (24. * 3600.)
    return delta_time_days

def putInDatabase(id,data):
    fileName=str(id)
    with open("Database/" + fileName + ".txt",'a') as f:
        f.write(data+"\n")
        f.close()
        pass

def Store(data):

    m_name=data['name']
    m_lat=data['latitude']
    m_lon=data['lontitude']
    m_spd=data['speed']
    m_brg=data['bearing']
    m_str=data['star']
    m_tsp=data['timeStamp']
    m_mde=data['mode']

    m_processedData="{0},{1},{2},{3},{4},{5},{6},{7}".format(format(m_lat,".6f"),format(m_lon,".6f"),format(m_spd,".2f"),format(m_brg,".1f"),m_str,format(days_date(m_tsp),".10f"),m_tsp,m_mde)

    print(r'接收，id为：{0}'.format(m_name))

    putInDatabase(m_name,m_processedData)

    pass

def CheckMJson(mJson):
    # 未获得有效值
    if mJson=='':
        return False

    # 不包含各个字段
    if not type(mJson)==dict:
        return False

    # 测试各个字段
    keyWords=['name','latitude','lontitude','speed','bearing','star','timeStamp','mode']
    for item in keyWords:
        if not item in mJson:
            return False
        pass


    return True



@app.route('/submitData',methods=['POST'])
def SubmitData():
    mJson=get_json_data(request.form)

    status=CheckMJson(mJson)
    if not status:
        return jsonify("Data Error"), 500

    Store(mJson)
    response={
        "Message":"Received",
    }
    return jsonify(response),200

if __name__=='__main__':
    scheduler=APScheduler()
    scheduler.init_app(app)
    scheduler.start()
    app.run(host="0.0.0.0",port=80,debug=False)
