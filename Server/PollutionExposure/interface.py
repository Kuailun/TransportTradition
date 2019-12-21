# -*- coding: utf-8 -*-
# @File       : interface.py
# @Author     : Yuchen Chai
# @Date       : 2019/12/19 12:39
# @Description: 接受服务器传来的请求并处理

def Pollution_Interface(data):
    '''
    接受服务器传来的用户信息并返回有关参数
    :param data:
    :return:
    '''

    status = True
    msg = ''
    data=[]

    # 成功
    if status:
        return 0, msg, data
    # 失败
    else:
        return 1, msg, data