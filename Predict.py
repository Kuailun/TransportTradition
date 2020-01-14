# -*- coding: utf-8 -*-
# @File       : Predict.py
# @Author     : Yuchen Chai
# @Date       : 2020/1/10 10:43
# @Description:

from Server.TransportationPredict_Tradition.Prediction import Prediction as pre

def readData(p_path):

    # 读入数据
    table=[]
    try:
        with open(p_path,'rb') as f:
            for row in f:
                row = row.rstrip()
                row = row.decode("utf-8")
                row = row.split(',')
                if len(row) == 8:
                    table.append(row)
    except IOError:
        pass

    ret_table = []
    # 将数据转为float值
    index=[0,1,2,3,4,5]
    m_tab = {}
    for i in range(len(table)):
        m_tab['latitude']=float(table[i][0])
        m_tab['longitude']=float(table[i][1])
        m_tab['velocity']=float(table[i][2])
        m_tab['direction']=float(table[i][3])
        m_tab['star']=float(table[i][4])
        m_tab['timestamp']=float(table[i][5])*24*60*60*1000.0
        m_tab['datestamp']=table[i][6]
        m_tab['label']=table[i][7]
        ret_table.append(m_tab)
        m_tab = {}
        pass
    return ret_table

if __name__ =='__main__':
    fileName="Database/YSY.txt"

    mData=readData(fileName)

    pp = pre()

    status, msg, processedData, distance, time = pp.Prediction_ProcessData(mData)
