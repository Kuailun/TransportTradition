# -*- coding: utf-8 -*-
# @File       : Prediction.py
# @Author     : Yuchen Chai
# @Date       : 2019/12/23 12:03
# @Description: 交通方式预测类

from Server import settings as ss
from Server.logger import logger
from Server.TransportationPredict_Tradition.BusStop import mBusStop
import json
import numpy as np
from geopy.distance import vincenty


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
            status, msg, processedData, distance, time = self.Prediction_ProcessData(gpsData)
            pass

        # 如果预测成功则重新整理数据并返回
        if status:
            status, msg, data = self._Prediction_AssembleData(processedData, distance, time)
        elif status == False and msg == '所含数据记录为空，错误':
            status, _, data = self._Prediction_AssembleData([], [], [])
        elif status == False and msg == '无有效数据':
            status, _, data = self._Prediction_AssembleData([], [], [])


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

        data = []
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
                    logger.warning(r'数据包名称错误，ID: {0}, 第 {1} 条记录， {2}'.format(userId, i, item))
                    return False, '数据包名称错误，ID: {0}, 第 {1} 条记录， {2}'.format(userId, i, item), None, None
                pass
            pass

        # 检查数组是否为空
        if len(gpsData) == 0:
            msg = r'所含数据记录为空，错误'
            logger.warning(msg)
            return False, msg, None, None

        # 迁移数据到新的变量
        for i in range(len(gpsData)):
            subItem = {}
            for item in gps_keyWords_New:
                subItem[item] = gpsData[i][item]
                pass
            data.append(subItem)
            pass

        return True, msg, userId, data

    def Prediction_ProcessData(self, p_data):
        '''
        数据处理并预测
        :param p_data:
        :return:
        '''

        status = True
        msg = ''

        mData_Filtered = self._STEP01_Valid_Data_Filter(p_data)

        if len(mData_Filtered) == 0:
            return False, '无有效数据', [], [], []

        data_segment_time = self._STEP02_Trip_Segment(mData_Filtered)

        data_segment_feature = self._STEP03_Feature_Calculation(data_segment_time)

        data_subsegs_processed = []
        for i in range(len(data_segment_feature)):
            data_subsegs = self._STEP04_Segment_Trip_By_Feature(data_segment_feature[i])
            data_subsegs_processed.append(self._STEP05_Get_Final_Tag(data_subsegs))
            pass

        distance, time = self._STEP06_Data_Describe(data_subsegs_processed)
        self._STEP07_Data_Accuracy(data_subsegs_processed)

        return status, msg, data_subsegs_processed, distance, time
        pass

    def _Prediction_AssembleData(self, p_data, p_distance, p_time):
        '''
        将数据还原为接口形式
        :param p_data:
        :return:
        '''

        status = True
        msg = ''

        # 接口定义的出行方式代码
        transportation_dict = ss.PREDICTION_INTERFACE_DICT

        # 需要返回的数据
        data = {'travelData':[],'travelDistanceData':[],'awardMoney':self._Prediction_Calculate_Award(p_data, p_distance, p_time)}
        for i in range(len(p_data)):
            # 部分旅程由于过短被判别为None
            if not p_data[i] == None:
                # 获取此段行程的全部label
                labels = p_data[i]['label']

                for j in range(len(p_data[i]['data'])):
                    for k in range(len(p_data[i]['data'][j])):
                        subItem = {}
                        subItem['id'] = p_data[i]['data'][j][k]['id']
                        subItem['travelWay'] = ss.PREDICTION_INTERFACE_DICT[labels[j]]
                        data['travelData'].append(subItem)
                        pass
                    pass
                pass
            pass

        # 将实际出行距离数据加入到回复中
        for item in p_distance:
            subItem = {
                'travelWay': ss.PREDICTION_INTERFACE_DICT[item],
                'travelRealDistance': p_distance[item]
            }
            data['travelDistanceData'].append(subItem)
            pass

        return status, msg, data

    def _Prediction_Calculate_DistanceAcc(self, GPS1, GPS2):
        '''
        根据两个GPS点，计算当前速度和方向
        :param GPS1:
        :param GPS2:
        :return: 距离，加速度
        '''
        deltaTime = (GPS2['timestamp'] - GPS1['timestamp']) / 1000.0
        if deltaTime == 0:
            deltaTime = 0.1
            print("deltaTime=0")
            pass

        distance = GPS1['velocity'] * deltaTime
        acc = (GPS2['velocity']-GPS1['velocity']) / deltaTime

        return distance, acc

    def _STEP01_Valid_Data_Filter(self, p_data):
        '''
        第一步，在已有数据中滤除不合理的记录
        :param p_data: 发送来的GPS数据
        :return:
        '''

        # 返回时装数据的列表
        r_data = []

        # 所有出行方式的速度上限
        p_speed = ss.PREDICTION_GPS_FILTER_SPEED_MAXIMUM

        # 卫星数量低于此则认为数据不合格
        p_star = ss.PREDICTION_GPS_FILTER_STAR_MINIMUM

        # 当前最新时间戳
        currentTime = 0
        for i in range(len(p_data)):
            # 如果纬度不在范围内则删除
            if p_data[i]['latitude'] > 90 or p_data[i]['latitude'] < -90:
                continue
            # 如果经度不在范围内则删除
            elif p_data[i]['longitude'] > 180 or p_data[i]['longitude'] < -180:
                continue
            # 如果速度不在范围内则删除
            elif p_data[i]['velocity'] > p_speed or p_data[i]['velocity'] < 0:
                continue
            # 如果卫星数量不在范围内则删除
            elif p_data[i]['star'] < p_star:
                continue
            # 如果时间戳有问题内则删除
            elif currentTime >= p_data[i]['timestamp']:
                continue
            r_data.append(p_data[i])
            currentTime = p_data[i]['timestamp']
            pass

        return r_data

    def _STEP02_Trip_Segment(self, p_data):
        '''
        将旅程分割，按照时间间隔分割成不同的旅途
        :param p_data:
        :return:
        '''

        # 将旅程按照此时间间隔分割
        p_interval = ss.PREDICTION_GPS_SEGMENT_INTERVAL_MAXIMUM

        # 旅程数据点的最低值
        p_sample = ss.PREDICTION_GPS_SEGMENT_DATA_MINIMUM

        i = 0
        currentTime = p_data[i]['timestamp']
        currentSegment = []
        Trips = []
        while i < len(p_data) - 1:
            if ((p_data[i + 1]['timestamp'] - currentTime) / 1000.0 > p_interval):
                Trips.append(currentSegment)
                i = i + 1
                currentTime = p_data[i]['timestamp']
                currentSegment = []
                continue
                pass
            currentSegment.append(i)
            i = i + 1
            currentTime = p_data[i]['timestamp']
            pass
        Trips.append(currentSegment)

        # 如果一段旅程的GPS点数少于阈值，则删除该段旅程
        i = len(Trips) - 1
        while (i >= 0):
            if (len(Trips[i]) < p_sample):
                del Trips[i]
                pass
            i = i - 1

        subTrip = []
        mTrip = []
        for i in range(len(Trips)):
            for j in range(len(Trips[i])):
                subTrip.append(p_data[Trips[i][j]])
                pass
            mTrip.append(subTrip)
            subTrip = []
            pass
        return mTrip

    def _STEP03_Feature_Calculation(self, p_data):
        '''
        根据数据计算特征，并加入到数据列表种
        :param p_data:
        :return:
        '''

        for i in range(len(p_data)):
            for j in range(len(p_data[i]) - 1):
                GPS1 = p_data[i][j]
                GPS2 = p_data[i][j + 1]
                distance, acc = self._Prediction_Calculate_DistanceAcc(GPS1, GPS2)
                p_data[i][j]['distance'] = distance
                p_data[i][j]['acc'] = acc
                pass
            p_data[i][-1]['distance'] = distance
            p_data[i][-1]['acc'] = acc
            pass
        return p_data

    def _STEP04_Segment_Trip_By_Feature(self, p_data):
        '''
        根据数据，将单一旅程分段，并给出可能的标签
        :param p_data:
        :return:
        '''

        p_vthd = ss.PREDICTION_GPS_CALCULATE_WALK_VELOCITY_MAXIMUM
        p_athd = ss.PREDICTION_GPS_CALCULATE_WALK_ACCELERATION_MAXIMUM
        p_N = ss.PREDICTION_GPS_CALCULATE_MODE_RANGE
        p_scale = ss.PREDICTION_GPS_CALCULATE_MODE_SCALE

        m_label = np.zeros((len(p_data)), dtype='int8')

        # 将所有可能的步行点都找出来
        for i in range(len(p_data)):
            if (p_data[i]['velocity'] <= p_vthd and abs(p_data[i]['acc']) <= p_athd):
                m_label[i] = 1
                pass
            pass

        m_Mthd = int(p_N * p_scale)

        # 根据前后关系，将部分点进行反转
        changeFlag = True
        while (changeFlag):
            changeFlag = False
            for i in range(len(p_data)):
                prePoint = max(0, i - p_N)
                postPoint = min(len(p_data) - 1, i + p_N)
                walkRate = sum(m_label[prePoint:postPoint]) / (postPoint - prePoint)
                if (m_label[i] == 0 and walkRate > p_scale):
                    m_label[i] = 1
                    changeFlag = True
                    pass
                elif (m_label[i] == 1 and walkRate < 1 - p_scale):
                    m_label[i] = 0
                    changeFlag = True
                    pass
                pass
            pass

        if (len(p_data) < 2 * p_N):
            return []

        # 可以寻找正或反变化
        func = 0
        initial = 0
        CTP = [0]
        for i in range(p_N, len(p_data) - p_N, 1):
            prePoint = max(0, i - p_N)
            postPoint = min(len(p_data) - 1, i + p_N)
            preRate = sum(m_label[prePoint:i]) / (i - prePoint)
            postRate = sum(m_label[i:postPoint]) / (postPoint - i)
            # 非步行-》步行
            if ((func == 0 or func == 2) and preRate < 1 - p_scale and postRate > p_scale):
                CTP.append(i)
                func = 1
                if (initial == 0):
                    # 首段非步行
                    initial = 1
                continue
                # 步行-》非步行
            if ((func == 0 or func == 1) and preRate > p_scale and postRate < 1 - p_scale):
                CTP.append(i)
                func = 2
                if (initial == 0):
                    # 首段步行
                    initial = 2
                pass
            pass
        CTP.append(len(p_data) - 1)
        if (func == 0):
            ratio = sum(m_label) / len(m_label)
            if (ratio > 0.5):
                # 步行
                func = 2
                initial = 2
            else:
                # 非步行
                func = 1
                initial = 1

        trip = {"label": [], "data": []}
        trueInitial = 2

        CTPS = [0]
        # 首段非步行
        if (initial == 1):
            i = 0
            first = True
            while (i < len(CTP) - 1):
                start = CTP[i]
                end = CTP[i + 1]
                deltaTime = (p_data[end]['timestamp'] - p_data[start]['timestamp']) / 1000.0
                dist = 0
                for j in range(start, end, 1):
                    dist = dist + p_data[j]['distance']
                    pass
                if (dist / deltaTime < p_vthd + 0.5):
                    i = i + 2
                    pass
                else:
                    if (first):
                        CTPS.append(CTP[i + 1])
                        trueInitial = 1
                    else:
                        CTPS.append(CTP[i])
                        CTPS.append(CTP[i + 1])
                    i = i + 2
                    pass
                first = False
                pass
            if (not CTPS[-1] == CTP[-1]):
                CTPS.append(CTP[-1])
        # 首段步行
        else:
            i = 1
            while (i < len(CTP) - 1):
                start = CTP[i]
                end = CTP[i + 1]
                deltaTime = (p_data[end]['timestamp'] - p_data[start]['timestamp']) / 1000.0
                dist = 0
                for j in range(start, end, 1):
                    dist = dist + p_data[j]['distance']
                    pass
                if (dist / deltaTime < p_vthd + 0.5):
                    i = i + 2
                    pass
                else:
                    CTPS.append(CTP[i])
                    CTPS.append(CTP[i + 1])
                    i = i + 2
                    pass
                pass
            if (not CTPS[-1] == CTP[-1]):
                CTPS.append(CTP[-1])

        for i in range(len(CTPS) - 1):
            if (len(trip['label']) == 0 and trueInitial == 1):
                trip["label"].append("non-walk")
                trip['data'].append(p_data[CTPS[i]:CTPS[i + 1] + 1])
                pass
            elif (len(trip['label']) == 0 and trueInitial == 2):
                trip["label"].append("walk")
                trip['data'].append(p_data[CTPS[i]:CTPS[i + 1] + 1])
            elif (trip['label'][-1] == "non-walk"):
                trip['label'].append("walk")
                trip['data'].append(p_data[CTPS[i]:CTPS[i + 1] + 1])
            elif (trip['label'][-1] == "walk"):
                trip['label'].append("non-walk")
                trip['data'].append(p_data[CTPS[i]:CTPS[i + 1] + 1])
                pass
        return trip

    def _STEP05_Get_Final_Tag(self, p_data):
        '''
        给出最终的出行方式标签
        :param p_data:
        :return:
        '''
        if p_data == []:
            return
        dataFeature = []

        # 计算数据特征
        for i in range(len(p_data['label'])):
            max_speed = 0
            min_speed = 100
            max_acc = 0
            min_acc = 100
            dist = 0
            deltaTime = 0
            averageSpeed = 0
            for j in range(len(p_data['data'][i])):
                currentItem = p_data['data'][i][j]
                if (currentItem['velocity'] < min_speed):
                    min_speed = currentItem['velocity']
                    pass
                if (currentItem['velocity'] > max_speed):
                    max_speed = currentItem['velocity']
                    pass
                if (abs(currentItem['acc']) > max_acc):
                    max_acc = abs(currentItem['acc'])
                    pass
                if (abs(currentItem['acc'] < min_acc)):
                    min_acc = abs(currentItem['acc'])
                dist = dist + currentItem['distance']
                pass
            deltaTime = (p_data['data'][i][-1]['timestamp'] - p_data['data'][i][0]['timestamp']) / 1000.0
            averageSpeed = dist / deltaTime
            dataFeature.append({'min_speed':min_speed, 'max_speed':max_speed, 'min_acc':min_acc, 'max_acc':max_acc, 'distance':dist, 'averageSpeed':averageSpeed, 'deltaTime': deltaTime})
            pass

        # 判断骑车
        for i in range(len(p_data['label'])):
            if (p_data['label'][i] == "non-walk"):
                # 自行车
                if (dataFeature[i]['max_speed'] < 6 and dataFeature[i]['averageSpeed'] < 5):
                    p_data['label'][i] = 'bike'
                    pass
            pass

        # 判断开车
        for i in range(len(p_data['label'])):
            if (p_data['label'][i] == "non-walk"):
                # 开车
                if (dataFeature[i]['max_speed'] > 8 and dataFeature[i]['averageSpeed'] > 4):
                    p_data['label'][i] = 'car'
                    pass
            pass

        # 合并非走路项
        changeFlag = True
        while (changeFlag):
            changeFlag = False
            for i in range(len(p_data['label']) - 2):
                # 前后均为开车的情况
                if (p_data['label'][i] == p_data['label'][i + 2] and (not p_data['label'][i] == 'walk') and (
                        not p_data['label'][i] == 'walk') and p_data['label'][i + 1] == 'walk'):
                    # 如果中途的走路时间超过一定阈值，则为真走路
                    if(dataFeature[i+1]['deltaTime']>120 and dataFeature[i+1]['averageSpeed']>0.5):
                        continue
                    p_data['label'][i + 1] = p_data['label'][i]
                    changeFlag = True
                    pass

                if(p_data['label'][i] == 'non-walk' and p_data['label'][i+1]=='walk' and p_data['label'][i+2]=='car'):
                    # 如果中途的走路时间超过一定阈值，则为真走路
                    if (dataFeature[i + 1]['deltaTime'] > 120 and dataFeature[i+1]['averageSpeed']>0.5):
                        continue
                    p_data['label'][i + 1] = 'car'
                    p_data['label'][i] = 'car'
                    changeFlag = True
                    pass

                if (p_data['label'][i+2] == 'non-walk' and p_data['label'][i + 1] == 'walk' and p_data['label'][
                    i] == 'car'):
                    # 如果中途的走路时间超过一定阈值，则为真走路
                    if (dataFeature[i + 1]['deltaTime'] > 120 and dataFeature[i+1]['averageSpeed']>0.5):
                        continue
                    p_data['label'][i + 1] = 'car'
                    p_data['label'][i + 2] = 'car'
                    changeFlag = True
                    pass

                if (p_data['label'][i] == 'car' and p_data['label'][i+1] == 'car' and p_data['label'][i+2] == 'non-walk'):
                    p_data['label'][i + 2] = 'car'
                    changeFlag = True
                    pass

                if (p_data['label'][i] == 'non-walk' and p_data['label'][i+1] == 'car' and p_data['label'][i+2] == 'car'):
                    p_data['label'][i] = 'car'
                    changeFlag = True
                    pass
                pass
            pass

        totalResult = []
        result = {}
        # 判断公交站
        for i in range(len(p_data['label'])):
            if (p_data['label'][i] == 'walk'):
                for j in range(len(p_data['data'][i])):
                    busStops = mBusStop.busStop_Search(p_data['data'][i][j])
                    for k in range(len(busStops)):
                        di = vincenty((p_data['data'][i][j]['latitude'], p_data['data'][i][j]['longitude']),
                                      (busStops[k][1], busStops[k][0])).meters
                        #
                        if (di < ss.PREDICTION_BUSSTOP_RANGE):
                            # 如果该ID从未出现过，则添加
                            if not busStops[k][4] in result:
                                result[busStops[k][4]] = 1
                            else:
                                result[busStops[k][4]] += 1
                    pass

                totalResult.append(result)
                result = {}

                pass
            elif (not p_data['label'][i] == 'walk'):
                for j in range(len(p_data['data'][i])):
                    if (p_data['data'][i][j]['velocity'] <= 0.2):
                        busStops = mBusStop.busStop_Search(p_data['data'][i][j])
                        for k in range(len(busStops)):
                            di = vincenty((p_data['data'][i][j]['latitude'], p_data['data'][i][j]['longitude']),
                                          (busStops[k][1], busStops[k][0])).meters
                            #
                            if (di < ss.PREDICTION_BUSSTOP_RANGE):
                                # 如果该ID从未出现过，则添加
                                if not busStops[k][4] in result:
                                    result[busStops[k][4]] = 1
                                else:
                                    result[busStops[k][4]] += 1
                        pass
                    pass
                pass
            pass
        if not p_data['label'][-1] == 'walk':
            totalResult.append(result)

        busFlag = []
        for i in range(len(totalResult)):
            value = 0
            for j in totalResult[i]:
                if value < totalResult[i][j]:
                    value = totalResult[i][j]
            if(len(totalResult[i]) >= 4 or value >= 35):
                busFlag.append(1)
            else:
                busFlag.append(0)
                pass
            pass

        index = 0
        # 判断是否需要将car改为bus
        for i in range(len(p_data['label'])):
            if(p_data['label'][i] == 'walk'):
                index = index + 1
                pass
            elif(p_data['label'][i] == 'car'):
                if busFlag[index] == 1:
                    p_data['label'][i] = 'bus'
                pass



        return p_data

    def _STEP06_Data_Describe(self, p_data):
        '''
        统计预测后当天的各种出行方式距离
        :param p_data:
        :return:
        '''
        distance = {"walk": 0, "bike": 0, "bus": 0, "car": 0, "non-walk": 0}
        time = {"walk": 0, "bike": 0, "bus": 0, "car": 0, "non-walk": 0}
        for i in range(len(p_data)):
            if (p_data[i] == None):
                continue
            for j in range(len(p_data[i]['label'])):
                for k in range(len(p_data[i]['data'][j])):
                    distance[p_data[i]['label'][j]] = distance[p_data[i]['label'][j]] + p_data[i]['data'][j][k]['distance']
                time[p_data[i]['label'][j]] = time[p_data[i]['label'][j]] + (p_data[i]['data'][j][-1]['timestamp'] - p_data[i]['data'][j][0]['timestamp']) / 1000.0
                pass
            pass

        logger.debug(r'出行距离统计： ' + str(distance))
        logger.debug(r'出行时间统计： ' + str(time))
        return distance, time
        pass

    def _STEP07_Data_Accuracy(self, p_data):
        '''
        统计预测的结果与真实标签的相似度
        :param p_data:
        :return:
        '''

        # 实际为走路，预测为走路、骑车、地铁、公交、汽车、其他
        confusionMatrix = {'walk': {'walk': 0, 'bike': 0, 'subway': 0, 'bus': 0, 'car': 0, 'non-walk': 0},
                           'bike': {'walk': 0, 'bike': 0, 'subway': 0, 'bus': 0, 'car': 0, 'non-walk': 0},
                           'subway': {'walk': 0, 'bike': 0, 'subway': 0, 'bus': 0, 'car': 0, 'non-walk': 0},
                           'bus': {'walk': 0, 'bike': 0, 'subway': 0, 'bus': 0, 'car': 0, 'non-walk': 0},
                           'car': {'walk': 0, 'bike': 0, 'subway': 0, 'bus': 0, 'car': 0, 'non-walk': 0}}

        for i in range(len(p_data)):
            if (p_data[i] == None):
                continue
            for j in range(len(p_data[i]['label'])):
                for k in range(len(p_data[i]['data'][j])):
                    currentItem = p_data[i]['data'][j][k]
                    if currentItem['label'] == '':
                        continue
                    confusionMatrix[currentItem['label']][p_data[i]['label'][j]] += 1
                    pass
                pass
            pass
        tag = ['walk', 'bike', 'subway', 'bus', 'car', 'non-walk']
        num = 0
        for i in confusionMatrix:
            divide = confusionMatrix[i][tag[0]] + confusionMatrix[i][tag[1]] + confusionMatrix[i][tag[2]] + \
                     confusionMatrix[i][tag[3]] + confusionMatrix[i][tag[4]] + confusionMatrix[i][tag[5]]
            if divide == 0:
                acc = 0
            else:
                acc = confusionMatrix[i][i] / divide
            print("{0} {1}, Accuracy: {2}".format(tag[num], confusionMatrix[i], acc))
            num += 1
        pass

    def _Prediction_Calculate_Award(self, p_data, p_distance, p_time):
        '''
        用于计算应该给予的钱数
        :param p_data:
        :return:
        '''

        # 如果所含数据为空
        if len(p_data) == 0:
            # 返回结果，扣除每日份的所有钱数
            return ss.PREDICTION_AWARD_PENALTY

        # 如果当日没有开车里程，不扣钱
        if p_distance['car'] == 0:
            #返回结果，不扣钱
            return 0

        # 如果当日有开车，且开车里程为绝大多数，则扣钱
        if p_distance['car'] >= p_distance['bus']:
            return ss.PREDICTION_AWARD_PENALTY

        return 0



prediction = Prediction()
