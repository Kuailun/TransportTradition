# -*- coding: utf-8 -*-
# @File       : Prediction.py
# @Author     : Yuchen Chai
# @Date       : 2019/12/23 12:03
# @Description: 交通方式预测类

from Server import settings as ss
from Server.logger import logger
import json

class Prediction:
    def __init__(self):
        pass

    def Prediction_Interface(self, p_data):
        '''
        接受服务器传来的GPS信息并处理
        :param data:
        :return:
        '''

        status = True
        msg = ''
        data = []

        # 解析发来的数据
        status, msg, userId, gpsData = self._Prediction_ExtractData(p_data)

        # 如果成功获得gps数据则计算，否则直接返回
        if status:
            status, msg, processedData = self._Prediction_ProcessData(gpsData)
            pass

        # 如果预测成功则重新整理数据并返回
        if status:
            status, msg, data = self._Prediction_AssembleData(processedData)

        # 成功
        if status:
            return 0, msg, data
        # 失败
        else:
            return 1, msg, data
        pass

    def _Prediction_ExtractData(self, p_data):
        '''
        解析数据并提取
        :param p_data:
        :return:
        '''

        # 获取传送来的数据模板
        interface_keyWords = ss.PREDICTION_INTERFACE_KEYWORDS
        gps_keyWords = ss.PREDICTION_GPS_PREDICTION_KEYWORDS
        gps_keyWords_New = ss.PREDICTION_GPS_REAL_KEYWORDS

        data=[]
        msg = ''

        # 检查数据个数
        if not len(p_data) == len(interface_keyWords):
            logger.warning(r"数据包不完整，缺少关键字")
            return False, '数据包不完整，缺少关键字', None, None

        # 检查数据的一致性
        for item in interface_keyWords:
            if not item in p_data:
                logger.warning(r'数据包名称错误，缺少' + str(item))
                return False, '数据包名称错误，缺少' + str(item), None, None

        userId = p_data['userId']
        gpsData = p_data['travel_data']

        try:
            gpsData = json.loads(gpsData)
        except:
            logger.warning(r'数据转为list错误，ID: {0}'.format(userId))
            return False, '数据转为list错误，ID: {0}'.format(userId), None, None

        # 检查GPS数据中的格式
        for i in range(len(gpsData)):
            if not len(gpsData[i]) == len(gps_keyWords):
                logger.warning(r'gps数据不完整，ID: {0}，第 {1} 条记录'.format(userId, i))
                return False, 'gps数据不完整，ID: {0}，第 {1} 条记录'.format(userId, i), None, None
            pass

        # 检查数据名称
        for i in range(len(gpsData)):
            for item in gps_keyWords:
                if not item in gpsData[i]:
                    logger.warning(r'数据包名称错误，ID: {0}, 第 {1} 条记录， {2}'.format(userId,i,item))
                    return False, '数据包名称错误，ID: {0}, 第 {1} 条记录， {2}'.format(userId,i,item), None, None
                pass
            pass

        # 迁移数据到新的变量
        for i in range(len(gpsData)):
            subItem={}
            for item in gps_keyWords_New:
                subItem[item] = gpsData[i][item]
                pass
            data.append(subItem)
            pass

        return True, msg, userId, data

    def _Prediction_ProcessData(self, p_data):
        '''
        数据处理并预测
        :param p_data:
        :return:
        '''

        status = True
        msg = ''
        data_subsegs_processed=[
            {
                'label':['walk','car'],
                'data':[
                    [
                        {
                            'latitude':0,
                            'longitude':0,
                            'velocity':0,
                            'timestamp':0,
                            'datestamp':0,
                            'star':0,
                            'id':0,
                            'label':'walk'
                        },
                        {
                            'latitude': 0,
                            'longitude': 0,
                            'velocity': 0,
                            'timestamp': 0,
                            'datestamp': 0,
                            'star': 0,
                            'id': 1,
                            'label': 'walk'
                        }
                    ],
                    [
                        {
                            'latitude': 0,
                            'longitude': 0,
                            'velocity': 0,
                            'timestamp': 0,
                            'datestamp': 0,
                            'star': 0,
                            'id': 5,
                            'label': 'walk'
                        },
                        {
                            'latitude': 0,
                            'longitude': 0,
                            'velocity': 0,
                            'timestamp': 0,
                            'datestamp': 0,
                            'star': 0,
                            'id': 6,
                            'label': 'walk'
                        }
                    ]
                ]
            },
            None
        ]

        return status, msg, data_subsegs_processed
        pass

    def _Prediction_AssembleData(self, p_data):
        '''
        将数据还原为接口形式
        :param p_data:
        :return:
        '''

        status = True
        msg=''

        # 接口定义的出行方式代码
        transportation_dict = ss.PREDICTION_INTERFACE_DICT

        # 需要返回的数据
        data = []
        for i in range(len(p_data)):
            # 部分旅程由于过短被判别为None
            if not p_data[i] == None:
                # 获取此段行程的全部label
                labels=p_data[i]['label']

                for j in range(len(p_data[i]['data'])):
                    for k in range(len(p_data[i]['data'][j])):
                        subItem={}
                        subItem['id'] = p_data[i]['data'][j][k]['id']
                        subItem['travelWay'] = labels[j]
                        data.append(subItem)
                        pass
                    pass
                pass
            pass

        return status, msg, data






prediction = Prediction()