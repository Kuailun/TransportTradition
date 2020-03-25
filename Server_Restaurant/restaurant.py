# -*- coding: utf-8 -*-
# @File       : restaurant.py
# @Author     : Yuchen Chai
# @Date       : 2020/3/21 13:50
# @Description:

from Server_Restaurant.logger import logger
from Server_Restaurant.functions import mRestaurant

class Restaurant:
    def __init__(self):
        self._status = True
        self._msg = ''
        pass

    def Restaurant_Interface(self, p_data):
        '''
        接受服务器传来的用户注册数据并处理
        :param data:
        :return:
        '''

        status = True
        msg = ''
        logger.debug(p_data)
        data = []

        status, msg, data = self.__Restaurant_ExtractData(p_data)
        if status:
            if data == "All":
                # 返回所有数据
                data = mRestaurant.Restaurant_All()
                pass
            elif data:
                # 返回搜索的结果
                data = mRestaurant.Restaurant_Key(data)
                pass
            pass

        # 成功
        if status:
            return 0, msg, data
        # 失败
        else:
            return 1, msg, []

        pass

    def __Restaurant_ExtractData(self, p_data):
        """
        从发来的数据中解析出当前需要搜索的关键词
        @param p_data:
        @return:
        """
        status = True
        msg = ''

        if not 'KeyWord' in p_data:
            msg = r'页面数据请求缺少KeyWords类型，错误'
            logger.warning(msg)
            return False, msg, ''

        mType = p_data['KeyWord']
        return status, msg, mType

        pass
    pass



restaurant = Restaurant()