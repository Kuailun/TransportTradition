# -*- coding: utf-8 -*-
# @File       : PollutionExposure.py
# @Author     : Yuchen Chai
# @Date       : 2019/12/20 22:39
# @Description: 空气污染类

from Server.functions import mPollution_Database
from Server.functions import mRegister_Database
import requests
from Server.logger import logger
import Server.settings as ss
import threading
import json

class PollutionExposure:
    def __init__(self):
        '''
        初始化污染信息暴露类，准备网络爬虫
        '''

        logger.info(r'请启动污染数据爬虫程序，间隔时间: {0} min'.format(str(ss.POLLUTIONEXPOSURE_PM25_INTERVAL // 60)))

    def Pollution_Interface(self, p_data):
        '''
        接受服务器传来的用户信息并返回有关参数
        :param data:
        :return:
        '''

        status = True
        msg = ''
        data = []

        # 解析发来的数据
        status, msg, userId = self._Pollution_ExtractData(p_data)

        # 如果成功获得userId则计算，否则直接返回
        if status:
            status, msg, data = self._Pollution_CalculateData(userId)

        # 成功
        if status:
            return 0, msg, data
        # 失败
        else:
            return 1, msg, data
        pass

    def Pollution_Submit_Pollution(self, p_data):
        '''
        用于接收外部发来的污染数值
        :param p_data:
        :return:
        '''
        status = True
        msg = ''

        status, msg, newItem = self._Pollution_ExtractPollution(p_data)

        # 写入数据库
        mPollution_Database.Database_Set_Record(newItem)

        return True,''

    def _Pollution_ExtractPollution(self, p_data):
        '''
        对从外部发来的数据进行解析
        :return:
        '''
        # 获取传送来的数据模板
        keyWords = ss.POLLUTIONEXPOSURE_INTERFACE_KEYWORDS

        msg = ''

        # 检查数据个数
        if not len(p_data) == 1:
            logger.warning(r"数据包不完整，缺少关键字")
            return False, '数据包不完整，缺少关键字', None

        data = p_data['pollution']

        data = json.loads(data)
        return True, msg, data

    def _Pollution_CalculateData(self, p_data):
        '''
        根据UserId，计算需要返回的数值
        :param data:
        :return:
        '''
        status = True
        msg = ''
        data = [{'travelWay': "开车", "value": -1}, {'travelWay': "公共交通", "value": -1}, {'travelWay': "骑行", "value": -1},
                {'travelWay': "步行", "value": -1}]

        # 从注册数据库中提取有关信息
        status, msg, user_data = mRegister_Database.Database_Search_Item(p_data)

        # 如果成功提取则计算，否则返回
        if status:
            data[0]['value'] = user_data[9] + user_data[10]
            data[1]['value'] = user_data[11] + user_data[12] + user_data[13] + user_data[14] + user_data[15] + \
                               user_data[16]
            data[2]['value'] = user_data[17] + user_data[18]
            data[3]['value'] = user_data[19] + user_data[20]
            pass

        return status, msg, data

    def _Pollution_ExtractData(self, js):
        '''
        解析发来的数据，检查并返回有用信息
        :param js:
        :return:
        '''
        # 获取传送来的数据模板
        keyWords = ss.POLLUTIONEXPOSURE_INTERFACE_KEYWORDS

        msg = ''

        # 检查数据个数
        if not len(js) == len(keyWords):
            logger.warning(r"数据包不完整，缺少关键字")
            return False, '数据包不完整，缺少关键字', None

        # 检查数据的一致性
        for item in keyWords:
            if not item in js:
                logger.warning(r'数据包名称错误，缺少' + str(item))
                return False, '数据包名称错误，缺少' + str(item), None

        userId = js['userId']
        return True, msg, userId

    def _Pollution_Fetch(self):
        '''
        从目标url爬取数据
        :return:
        '''


        self.lastStatus = True
        self.lastTID = threading.get_ident()

        # 从网页获取需要分析的数据
        response = requests.get(url=self.targetUrl, timeout=ss.POLLUTIONEXPOSURE_PM25_TIMEOUT)

        # 返回分析好的数据
        newItem = self._Pollution_Analyze(response)
        logger.debug(r"爬取污染数据，最新污染值为: {0}   PM2.5: {1} ".format(newItem[0], newItem[2]))

        # 写入数据库
        mPollution_Database.Database_Set_Record(newItem)

        self.lastStatus = False
        self.lastTID = ''
        pass

pollutionExposure = PollutionExposure()
