# -*- coding: utf-8 -*-
# @File       : cellphone.py
# @Author     : Yuchen Chai
# @Date       : 2020/4/2 19:16
# @Description:

from Server_Restaurant.logger import logger
from Server_Restaurant.functions import mCellphone

class Cellphone:
    def __init__(self):
        self._status = True
        self._msg = ''
        pass

    def Cellphone_Interface(self, p_data):
        '''
        接受服务器传来的用户注册数据并处理
        :param data:
        :return:
        '''

        status = True
        msg = ''
        logger.debug(p_data)
        data = []

        status, msg, phone = self.__Cellphone_ExtractData(p_data)

        if status:
            status, msg, data = self.__Cellphone_GenerateData(phone)
            pass

        if status:
            status, msg, data = self.__Cellphone_AssembleData(data,phone)

        # 成功
        if status:
            return 0, msg, data
        # 失败
        else:
            return 1, msg, []

        pass

    def __Cellphone_AssembleData(self, p_data, p_cell):
        """
        组合回传的数据
        @param p_data:
        @return:
        """
        ret_data = {
            "userCell":int(p_cell),
            "userType":int(p_data['treat']),
            "userData":{}
        }
        title = ['prior_plan_rest','prior_plan_park','prior_actual_rest','prior_actual_park','district_rest','district_park','district_cert']
        for i in range(len(title)):
            ret_data['userData'][title[i]] = int(p_data[title[i]])
        return True,"",ret_data

    def __Cellphone_GenerateData(self, p_data):
        """
        根据手机号，生成所需的各项数据
        @param p_data:
        @return:
        """
        status = True
        msg = ""
        data = []

        status, msg = mCellphone.isCellphone(p_data)
        if status:
            # 获得手机号对应的数据
            status, msg, data = mCellphone.GetCellphone(p_data)
            pass

        return status, msg, data
    def __Cellphone_ExtractData(self, p_data):
        """
        得到电话号码
        @param p_data:
        @return:
        """
        status = True
        msg = ''

        if not 'cellphone' in p_data:
            msg = r'页面数据请求缺少Range类型，错误'
            logger.warning(msg)
            return False, msg, None

        mCellphone = p_data['cellphone']
        return status, msg, mCellphone


cellphone = Cellphone()