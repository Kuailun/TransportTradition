# -*- coding: utf-8 -*-
# @File       : BusStop.py
# @Author     : Yuchen Chai
# @Date       : 2020/1/11 16:53
# @Description: 在本类中读入公交数据并归类，可快速查询某个数据是否为公交站附近

import os
import xlrd
from Server import settings as ss
from Server.logger import logger

class busStop():
    def __init__(self):
        '''读入数据'''

        # 检查数据存储情况
        if not os.path.exists(ss.PREDICTION_BUSSTOP_PATH + '/' + ss.PREDICTION_BUSSTOP_NAME):
            logger.critical(r'缺失公交数据库，请检查！')
            pass

        self.data_path = ss.PREDICTION_BUSSTOP_PATH + '/' + ss.PREDICTION_BUSSTOP_NAME

        # 读入数据
        self._bus_data = self._busStop_Load_Data()

        # 数据去重
        self._busStop_Remove_Duplication()

        # 整理数据，形成快速查询的结构
        self._busStop_Structure()

    def _busStop_Load_Data(self):
        '''
        从源文件中读取公交站原始数据
        :return:
        '''

        book = xlrd.open_workbook(self.data_path)
        sheet = book.sheet_by_name('Data')

        ret_data = []
        for i in range(sheet.nrows):
            item = []
            item.append(sheet.cell(i, 1).value)
            item.append(sheet.cell(i, 2).value)
            item.append(sheet.cell(i, 3).value)
            item.append(sheet.cell(i, 4).value)
            item.append(sheet.cell(i, 5).value)
            ret_data.append(item)
            pass

        return ret_data[1:-1]

    def _busStop_Remove_Duplication(self):
        '''
        清洗数据，去掉重复项，去掉不符合要求的项目
        :return:
        '''

        logger.debug(r'读取完成后，公交数据库中有{0}项'.format(len(self._bus_data)))

        # 去掉数据中重复的ID值
        index = []
        ret_data = []
        for i in range(len(self._bus_data)):
            if self._bus_data[i][4] not in index:
                index.append(self._bus_data[i][4])
                ret_data.append(self._bus_data[i])
                pass
            pass

        self._bus_data = ret_data

        logger.debug(r'去除重复的id后，公交数据库中有{0}项'.format(len(self._bus_data)))

        # 去掉范围之外的数据
        ret_data = []
        for i in range(len(self._bus_data)):
            if self._bus_data[i][0] > ss.PREDICTION_BUSSTOP_LOCATION_LON_MAX:
                continue
            elif self._bus_data[i][0] < ss.PREDICTION_BUSSTOP_LOCATION_LON_MIN:
                continue
            elif self._bus_data[i][1] > ss.PREDICTION_BUSSTOP_LOCATION_LAT_MAX:
                continue
            elif self._bus_data[i][1] < ss.PREDICTION_BUSSTOP_LOCATION_LAT_MIN:
                continue
            ret_data.append(self._bus_data[i])
            pass

        self._bus_data = ret_data
        logger.debug(r'去除范围之外的数据后，公交数据库中有{0}项'.format(len(self._bus_data)))

        return

    def _busStop_Structure(self):
        '''
        将数据分割成小的数据结构
        :return:
        '''
        self.interval_x = (ss.PREDICTION_BUSSTOP_LOCATION_LON_MAX - ss.PREDICTION_BUSSTOP_LOCATION_LON_MIN) / float(ss.PREDICTION_BUSSTOP_X_GROUPS)
        self.interval_y = (ss.PREDICTION_BUSSTOP_LOCATION_LAT_MAX - ss.PREDICTION_BUSSTOP_LOCATION_LAT_MIN) / float(ss.PREDICTION_BUSSTOP_X_GROUPS)

        # 准备数据结构
        ret_data = []
        for i in range(ss.PREDICTION_BUSSTOP_X_GROUPS):
            subItem = []
            for j in range(ss.PREDICTION_BUSSTOP_Y_GROUPS):
                subItem.append([])
                pass
            ret_data.append(subItem)
            pass

        for i in range(len(self._bus_data)):
            # 计算每一项应该存储在哪个单元格内
            x = int((self._bus_data[i][0] - ss.PREDICTION_BUSSTOP_LOCATION_LON_MIN)//self.interval_x)
            y = int((self._bus_data[i][1] - ss.PREDICTION_BUSSTOP_LOCATION_LAT_MIN)//self.interval_y)
            ret_data[x][y].append(self._bus_data[i])
            pass

        self._bus_data_structured = ret_data

        pass

    def busStop_Search(self, p_data):
        '''
        根据gps坐标，查询在范围内的车站ID
        :param p_data:
        :return:
        '''
        # 获取当前GPS数据所在的区域
        x = int((p_data['longitude'] - ss.PREDICTION_BUSSTOP_LOCATION_LON_MIN) // self.interval_x)
        y = int((p_data['latitude'] - ss.PREDICTION_BUSSTOP_LOCATION_LAT_MIN) // self.interval_y)

        # 拓展区域到+-1的范围
        x_min = max(0, x-1)
        x_max = min(ss.PREDICTION_BUSSTOP_X_GROUPS-1, x+1)

        y_min = max(0, y-1)
        y_max = min(ss.PREDICTION_BUSSTOP_Y_GROUPS-1, y+1)

        ret_data = []
        for i in range(x_max - x_min):
            for j in range(y_max - y_min):
                ret_data = ret_data + self._bus_data_structured[i+x_min][j+y_min]
                pass
            pass

        return ret_data

mBusStop = busStop()