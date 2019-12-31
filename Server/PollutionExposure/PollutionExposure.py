# -*- coding: utf-8 -*-
# @File       : PollutionExposure.py
# @Author     : Yuchen Chai
# @Date       : 2019/12/20 22:39
# @Description: 空气污染类

from Server.functions import mPollution_Database
from Server.functions import mRegister_Database
import requests
from pyquery import PyQuery as pq
from Server.logger import logger
import Server.Utils as ut
import Server.settings as ss
import datetime
from apscheduler.schedulers.background import BackgroundScheduler

class PollutionExposure:
    def __init__(self):
        '''
        初始化污染信息暴露类，准备网络爬虫
        '''

        # 爬虫目标网址
        self.targetUrl='http://www.pm25.in/zhengzhou'

        # 初始化时更新一次污染结构
        self._Pollution_Fetch()

        # 设置定时任务，定时获取最新污染情况
        scheduler = BackgroundScheduler()
        scheduler.add_job(self._Pollution_Fetch,'interval',seconds=ss.POLLUTIONEXPOSURE_PM25_INTERVAL)
        scheduler.start()
        logger.info(r'污染暴露定时爬虫开启，间隔时间: {0} min'.format(str(ss.POLLUTIONEXPOSURE_PM25_INTERVAL//60)))

    def Pollution_Interface(self,p_data):
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
            status, msg, data= self._Pollution_CalculateData(userId)

        # 成功
        if status:
            return 0, msg, data
        # 失败
        else:
            return 1, msg, data
        pass

    def _Pollution_CalculateData(self,p_data):
        '''
        根据UserId，计算需要返回的数值
        :param data:
        :return:
        '''
        status=True
        msg=''
        data=[{'travelWay':"开车","value":-1},{'travelWay':"公共交通","value":-1},{'travelWay':"骑行","value":-1},{'travelWay':"步行","value":-1}]

        # 从注册数据库中提取有关信息
        status, msg, user_data= mRegister_Database.Database_Search_Item(p_data)

        # 如果成功提取则计算，否则返回
        if status:
            data[0]['value'] = user_data[9] + user_data[10]
            data[1]['value'] = user_data[11] + user_data[12]+ user_data[13]+ user_data[14]+ user_data[15]+ user_data[16]
            data[2]['value'] = user_data[17] + user_data[18]
            data[3]['value'] = user_data[19] + user_data[20]
            pass

        return status, msg, data

    def _Pollution_ExtractData(self,js):
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
        # 从网页获取需要分析的数据
        response=requests.get(url=self.targetUrl, timeout = ss.POLLUTIONEXPOSURE_PM25_TIMEOUT)

        # 返回分析好的数据
        newItem = self._Pollution_Analyze(response)
        logger.debug(r"爬取污染数据，最新污染值为: {0}   PM2.5: {1} ".format(newItem[0],newItem[2]))

        # 写入数据库
        mPollution_Database.Database_Set_Record(newItem)
        pass

    def _Pollution_Analyze(self, p_content):
        '''
        解析获得的网络内容
        :param p_content:
        :return:
        '''

        # 如果网站爬取出现问题，返回默认值
        if not p_content.status_code==200:
            logger.warning(r"污染数据爬取错误，回复代码 {0}".format(str(p_content.status_code)))
            return ss.POLLUTIONEXPOSURE_DEFAULT_DATA

        # 将获得的网站转为pyquery对象
        doc=pq(p_content.text)
        items=doc('.span1')

        # 如果返回的数据量不为标准的9个
        if not len(items)==9:
            logger.warning(r"污染数据爬取错误，所含项目数少于9")
            return ss.POLLUTIONEXPOSURE_DEFAULT_DATA

        # 第9项非数据，需要排除
        index=0
        newItem=ut.Get_Current_Timestamp_Rounded()
        for item in items:
            if(index<8):
                # 将子项再归为pq对象
                item=pq(item)
                value=item.text()
                value=value.split('\n')
                newItem.append(float(value[0]))
                pass
            index+=1
            pass

        return newItem

pollutionExposure = PollutionExposure()