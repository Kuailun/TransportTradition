# -*- coding: utf-8 -*-
# @File       : SearchUserRegisteration.py
# @Author     : Yuchen Chai
# @Date       : 2019/12/24 20:28
# @Description: 根据高德API，查询用户出行情况

import sys
sys.path.append(r"E:\WorkSpace\Python\TransportTradition")
from Server.functions import mRegister_Database
from Server.logger import logger
from Server import settings as ss
import requests

class AMAP_User:
    def __init__(self):
        self._Process_UserID()
        pass

    def _Process_UserID(self):
        '''
        一个个更新数据库中的UserID
        :return:
        '''

        status = True
        msg = ''
        data = [0]

        # 用户注册数据记录
        num_Register = len(mRegister_Database)

        # 查询失败列表
        item_Fail = []

        # 查询成功列表
        item_Success = []

        while (status == True and (not len(data) == 0)):
            # 从UserID数据库中提取未查询过的记录
            status, msg, data = mRegister_Database.Database_Return_Record()

            # 检查是否已经完成所有查询
            if len(data) == 0:
                break

            # 检查该ID是否出现在成功的列表内
            if data[0] in item_Success:
                status = False
                msg = '该ID重复出现在成功列表, {0}'.format(data[0])
                data = []
                pass

            # 检查该ID是否出现在失败的列表内
            if data[0] in item_Fail:
                status = False
                msg = '该ID重复出现在失败列表, {0}'.format(data[0])
                data = []
                logger.warning(msg)
                pass

            # 根据AMAP查询结果
            if status:
                status, msg, data = self._Search_AMAP(data)
                pass

            # 记录ID到成功、失败数据库中
            if status:
                item_Success.append(data[0])
            else:
                status = True
                data[9] = 1
                item_Fail.append(data[0])

            # 设置回到数据库中
            if status:
                status, msg = mRegister_Database.Database_Set_UserInfo(data)

        if status == True:
            logger.info(r'User信息查询成功，数据库中共计 {0} 个数据，本次查询 {1} 个'.format(num_Register, len(item_Success)))

        if status == False:
            logger.warning(r'查询失败，{0}'.format(msg))

        pass

    def _Search_AMAP(self, p_data):
        '''
        使用高德API查询并返回结果
        :param p_data:
        :return:
        '''

        status = True
        msg = ''
        data = p_data

        # 检查p_data的数据长度
        if not len(p_data) == mRegister_Database.Database_Get_Title_Number():
            status = False
            msg = r'数据长度错误'
            logger.warning(msg)

        try:
            # 检查经度范围
            if float(p_data[5]) < ss.AMAP_LOCATION_LON_MIN or float(p_data[5]) > ss.AMAP_LOCATION_LON_MAX:
                status = False
                msg = r'ID: {0} 经度数据超过允许的范围'.format(p_data[0])
                logger.warning(msg)
            # 检查经度范围
            if float(p_data[7]) < ss.AMAP_LOCATION_LON_MIN or float(p_data[7]) > ss.AMAP_LOCATION_LON_MAX:
                status = False
                msg = r'ID: {0} 经度数据超过允许的范围'.format(p_data[0])
                logger.warning(msg)
            # 检查纬度范围
            if float(p_data[6]) < ss.AMAP_LOCATION_LAT_MIN or float(p_data[6]) > ss.AMAP_LOCATION_LAT_MAX:
                status = False
                msg = r'ID: {0} 纬度数据超过允许的范围'.format(p_data[0])
                logger.warning(msg)
            # 检查纬度范围
            if float(p_data[8]) < ss.AMAP_LOCATION_LAT_MIN or float(p_data[8]) > ss.AMAP_LOCATION_LAT_MAX:
                status = False
                msg = r'ID: {0} 纬度数据超过允许的范围'.format(p_data[0])
                logger.warning(msg)
        except:
            status = False
            msg = r'检查经纬度范围出错'
            logger.warning(msg)

        url_walk = 'https://restapi.amap.com/v3/direction/walking'
        walk_body = {
            'key': ss.AMAP_SERVER_KEY,
            'origin': '{0},{1}'.format(p_data[5], p_data[6]),
            'destination': '{0},{1}'.format(p_data[7], p_data[8])
        }

        url_bike = 'https://restapi.amap.com/v4/direction/bicycling'
        bike_body = {
            'key': ss.AMAP_SERVER_KEY,
            'origin': '{0},{1}'.format(p_data[5], p_data[6]),
            'destination': '{0},{1}'.format(p_data[7], p_data[8])
        }

        url_bus = 'https://restapi.amap.com/v3/direction/transit/integrated'
        bus_body = {
            'key': ss.AMAP_SERVER_KEY,
            'origin': '{0},{1}'.format(p_data[5], p_data[6]),
            'destination': '{0},{1}'.format(p_data[7], p_data[8]),
            'city': '郑州',
            'cityd': '郑州',
            'strategy': ss.AMAP_SERVER_STRATEGY,
            'nightflag': 0
        }

        url_car = 'https://restapi.amap.com/v3/direction/driving'
        car_body = {
            'key': ss.AMAP_SERVER_KEY,
            'origin': '{0},{1}'.format(p_data[5], p_data[6]),
            'destination': '{0},{1}'.format(p_data[7], p_data[8]),
            'strategy': ss.AMAP_SERVER_STRATEGY
        }

        if status:

            # 获得各种出行方式的数据

            content_walk = requests.post(url_walk, data = walk_body)
            content_bike = requests.post(url_bike, data = bike_body)
            content_bus = requests.post(url_bus, data = bus_body)
            content_car = requests.post(url_car, data = car_body)

        if status:
            # 转换走路的结果
            status, msg, content_walk = self._Process_Received_Data(content_walk,'walk')
        if status:
            # 转换骑行的结果
            status, msg, content_bike = self._Process_Received_Data(content_bike,'bike')
        if status:
            # 转换公交的结果
            status, msg, content_bus = self._Process_Received_Data(content_bus, 'bus')
        if status:
            # 转换开车的结果
            status, msg, content_car = self._Process_Received_Data(content_car, 'car')

        if status:
            # 分析结果
            status, msg, data = self._AnalyzeData(content_walk, content_bike, content_bus, content_car, p_data)

        return status, msg, data

    def _AnalyzeData(self, content_walk, content_bike, content_bus, content_car, p_data):
        '''
        分析数据包，得到各种出行方式的时间和距离
        :param content_walk:
        :param content_bike:
        :param content_bus:
        :param content_car:
        :return:
        '''

        try:
            # 分析走路
            p_data[24] = int(content_walk['route']['paths'][0]['distance'])
            p_data[25] = int(content_walk['route']['paths'][0]['duration'])

            # 分析骑车
            p_data[22] = int(content_bike['data']['paths'][0]['distance'])
            p_data[23] = int(content_bike['data']['paths'][0]['duration'])

            # 分析开车
            p_data[14] = int(content_car['route']['paths'][0]['distance'])
            p_data[15] = int(content_car['route']['paths'][0]['duration'])

            # 分析公共交通
            trip = content_bus['route']['transits'][0]

            walk_distance = 0
            walk_duration = 0
            bus_distance = 0
            bus_duration = 0
            subway_distance = 0
            subway_duration = 0

            for segment in range(len(trip['segments'])):
                # 如果走路段不为空
                if not len(trip['segments'][segment]['walking'])==0:
                    walk_distance += int(trip['segments'][segment]['walking']['distance'])
                    walk_duration += int(trip['segments'][segment]['walking']['duration'])
                    pass

                # 如果公交段不为空
                if not len(trip['segments'][segment]['bus']['buslines'])==0:
                    for i in range(len(trip['segments'][segment]['bus']['buslines'])):
                        mode_type = trip['segments'][segment]['bus']['buslines'][i]['type']
                        # 统计地铁的距离、时间
                        if mode_type == '地铁线路':
                            subway_distance += int(trip['segments'][segment]['bus']['buslines'][i]['distance'])
                            subway_duration += int(trip['segments'][segment]['bus']['buslines'][i]['duration'])
                            pass
                        # 统计公交的距离、时间
                        else:
                            bus_distance += int(trip['segments'][segment]['bus']['buslines'][i]['distance'])
                            bus_duration += int(trip['segments'][segment]['bus']['buslines'][i]['duration'])
                            pass
                        pass
                    pass
                pass

            # 复制到数据体里
            p_data[16] = bus_distance
            p_data[17] = bus_duration
            p_data[18] = subway_distance
            p_data[19] = subway_duration
            p_data[20] = walk_distance
            p_data[21] = walk_duration

            # 设置处理过的标志
            p_data[9] = 1

            return True, '', p_data
        except:
            msg = '分析出行数据失败，ID {0}'.format(p_data[0])
            logger.warning(msg)
            return False, msg, p_data

    def _Process_Received_Data(self, p_data, type):
        '''
        检查查询的结果，返回有效数据
        :param data:
        :return:
        '''

        # 如果返回的查询结果不是200 ok
        if not p_data.status_code == 200:
            logger.warning(r'AMAP API获取数据失败, {0}'.format(type))
            return False, 'AMAP API获取数据失败, {0}'.format(type), []

        # 获取数据包中的json数据
        data = p_data.json()
        return True, '', data

amap_user = AMAP_User()