# -*- coding: utf-8 -*-
# @File       : userData.py
# @Author     : Yuchen Chai
# @Date       : 2020/4/3 0:25
# @Description:
from datetime import datetime

from Server_Restaurant.logger import logger
from Server_Restaurant.functions import mUserData

class UserData:
    def __init__(self):
        self._status = True
        self._msg = ''
        pass

    def UserData_Interface(self, p_data, p_ip):
        '''
        接受服务器传来的用户回答并处理
        :param data:
        :return:
        '''

        status = True
        msg = ''
        logger.debug(p_data)
        data = []

        status, msg, phone = self.__UserData_ExtractData(p_data)

        phone['IP'] = p_ip
        phone['Timestamp'] = str(datetime.now())
        if status:
            status, msg = self.__UserData_SaveData(phone)
            pass

        # 成功
        if status:
            return 0, msg
        # 失败
        else:
            return 1, msg

        pass

    def __UserData_ExtractData(self, p_data):
        """
        从提交的数据中提取有效数据
        @param p_data:
        @return:
        """
        status = True
        msg = ''

        title = ['cellphone',"predict_rest","predict_park","rest_risk","park_risk","willing"]

        for item in title:
            if not item in p_data:
                msg = r'数据请求缺少{0}字段，错误！'.format(item)
                logger.warning(msg)
                return False,msg,None

        ret_data = {}
        for item in title:
            ret_data[item] = p_data[item]

        return status, msg, ret_data

    def __UserData_SaveData(self, p_data):
        """
        存入数据
        @param p_data:
        @return:
        """
        status = True
        msg = ""

        status, msg = mUserData.isCellphone(p_data['cellphone'])
        mUserData.submitData(p_data)

        return status, msg

userdata = UserData()