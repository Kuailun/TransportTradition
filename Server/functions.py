# -*- coding: utf-8 -*-
# @File       : Functions.py
# @Author     : Yuchen Chai
# @Date       : 2019/12/19 11:16
# @Description: 数据库类

import os
import xlrd, xlwt
from xlutils.copy import copy
from Server.logger import logger
from Server import settings as ss


class Database:
    def __init__(self, path, name):
        '''
        初始化数据库类
        :param path: 数据库保存目录
        :param name: 数据库名称
        '''

        self._name = name
        # 数据库路径
        self._database_path = path + name
        # 数据库是否可用标签
        self._database_available = True

        pass

    def _Database_Path_Existing(self):
        '''
        检查数据库文件是否存在
        :return:
        '''

        # 检查数据库的路径是否存在
        if not os.path.exists(self._database_path):
            logger.info(r"{0} 不存在，开始创建".format(self._name))
            self._Database_CreateFile()
            pass
        else:
            pass
        pass

    def _Database_CreateFile(self):
        '''
        创建用户注册的数据库
        :return:
        '''
        raise ("_Database_CreateFile函数未初始化")

    def _Database_ReadFile(self):
        '''
        读入已有的用户注册数据库
        :return:
        '''
        raise ("_Database_ReadFile函数未初始化")

    def _Database_WriteFile(self):
        '''
        将数据库中现有数据覆盖写入文件
        :return:
        '''
        raise ("_Database_WriteFile函数未初始化")


class Database_Registeration(Database):
    '''
    基于Database类，用户注册的数据库
    '''

    def __init__(self):
        '''
        初始化用户注册数据类
        '''

        super(Database_Registeration, self).__init__(ss.REGISTERATION_DATABASE_PATH, ss.REGISTERATION_DATABASE_NAME)
        # 工作簿头部标签
        self._database_title = ['用户ID', '姓名', '电话', '家庭地址', '工作地址', '家庭经度', '家庭纬度', '办公经度', '办公纬度', '开车距离', '开车时间',
                                '公共交通-公交距离', '公共交通-公交时间',
                                '公共交通-地铁距离', '公共交通-地铁时间',
                                '公共交通-步行距离', '公共交通-步行时间', '骑行距离', '骑行时间', '步行距离', '步行时间']
        # 数据库
        self._database = {}
        # 检查数据库的路径是否存在
        self._Database_Path_Existing()
        # 读取用户注册数据库
        self._Database_ReadFile()
        pass

    def _Database_CreateFile(self):
        '''
        创建用户注册的数据库
        :return:
        '''

        self._database_available = False

        # 创建工作簿
        workbook = xlwt.Workbook(encoding='utf-8')
        worksheet = workbook.add_sheet('data')

        for i in range(len(self._database_title)):
            # 设置列宽，128为单元，后面为英文字符宽度
            current_col = worksheet.col(i)
            current_col.width = 128 * (len(self._database_title[i]) * 4 + 4)

            # 写入头部标签
            worksheet.write(0, i, self._database_title[i])
            pass

        # 保存工作簿
        workbook.save(self._database_path)

        self._database_available = True

        pass

    def _Database_ReadFile(self):
        '''
        读入已有的用户注册数据库
        :return:
        '''

        # 若数据库现在不可用，等待
        while (not self._database_available):
            pass

        # 禁止其他应用操作
        self._database_available = False

        # 准备读入数据
        workbook = xlrd.open_workbook(self._database_path)
        worksheet = workbook.sheet_by_name('data')

        # 循环读入数据
        for i in range(worksheet.nrows - 1):
            item = []
            for j in range(len(self._database_title)):
                item.append(worksheet.cell_value(i + 1, j))
                pass
            self._database[item[0]] = item
            pass

        logger.info(r"用户注册数据库读取完成，共计 " + str(len(self._database)) + ' 项')
        # 允许其他应用操作
        self._database_available = True
        pass

    def _Database_WriteFile(self):
        '''
        将数据库中现有数据覆盖写入文件
        :return:
        '''

        # 创建工作簿
        workbook = xlwt.Workbook(encoding='utf-8')
        worksheet = workbook.add_sheet('data')

        # 循环写入头部标签
        for i in range(len(self._database_title)):
            # 写入头部标签
            worksheet.write(0, i, self._database_title[i])
            pass

        # 循环写入数据
        for i, item in enumerate(self._database):
            for j in range(len(self._database_title)):
                worksheet.write(i + 1, j, self._database[item][j])
                pass
            pass

        # 保存工作簿
        workbook.save(self._database_path)
        pass

    def Database_Get_Title_Number(self):
        '''
        获取Title的数量
        :return:
        '''
        return len(self._database_title)

    def Database_Set_Record(self, p_data):
        '''
        外部函数调用，写入数据
        :param data:
        :return:
        '''

        # 若数据库现在不可用，等待
        while (not self._database_available):
            pass

        stauts = True
        msg = ''

        self._database_available = False

        # 并非首次注册，已存在于数据库中
        if (p_data[0] in self._database):
            self._database[p_data[0]] = p_data
            status = True
            msg = r"用户ID已存在于数据库中，非首次注册： " + str(p_data[0])
            logger.warning(msg)

        # 首次注册，成功添加
        else:
            self._database[p_data[0]] = p_data
            status = True
            msg = ''

        # 写到外部文件
        self._Database_WriteFile()

        # 允许其他使用
        self._database_available = True

        return stauts, msg

    def Database_Update_Record(self, p_data):
        '''
        更新一个当前的记录
        :param p_data:
        :return:
        '''

        # 并非更新，实际首次注册，不在数据库中
        if not (p_data[0] in self._database):
            self._database[p_data[0]] = p_data
            status = True
            msg = r"用户ID不在数据库中，首次注册： " + str(p_data[0])
            logger.warning(msg)

        # 非首次注册，成功更新
        else:
            self._database[p_data[0]] = p_data
            status = True
            msg = ''

        # 写到外部文件
        self._Database_WriteFile()

        # 允许其他使用
        self._database_available = True

        return status, msg

    def Database_Search_Item(self, item):
        '''
        根据用户ID，查询家庭有关信息
        :param item:
        :return:
        '''
        status = True
        msg = ''
        data = []

        # 检查数据库中是否有该ID
        if item in self._database:
            data = self._database[item]
            return status, msg, data
        # 该ID不存在于数据库中
        else:
            status = False
            msg = '数据库中无此ID'
            logger.warning(r'数据库中无此ID: {0}，无法返回空气污染信息'.format(item))
            return status, msg, data
        pass

    pass


class Database_PollutionExposure(Database):
    '''
    基于Database类，污染物的数据库
    '''

    def __init__(self):
        '''
        初始化污染物数据类
        '''

        super(Database_PollutionExposure, self).__init__(ss.POLLUTIONEXPOSURE_DATABASE_PATH,
                                                         ss.POLLUTIONEXPOSURE_DATABASE_NAME)
        # 工作簿头部标签
        self._database_title = ['日期', '时间戳', 'AQI', 'PM2.5', 'PM10', 'CO', 'NO2', 'O31', 'O38', 'SO2']
        # 数据库
        self._database_last_data = []
        self._database_latest_data = ss.POLLUTIONEXPOSURE_DEFAULT_DATA
        # 检查数据库的路径是否存在
        self._Database_Path_Existing()
        # 读取用户注册数据库
        self._Database_ReadFile()

        pass

    def _Database_CreateFile(self):
        '''
        创建污染历史数据库
        :return:
        '''
        self._database_available = False

        # 创建工作簿
        workbook = xlwt.Workbook(encoding='utf-8')
        worksheet = workbook.add_sheet('data')

        for i in range(len(self._database_title)):
            # 设置列宽，128为单元，后面为英文字符宽度
            current_col = worksheet.col(i)
            current_col.width = 128 * (len(self._database_title[i]) * 4 + 4)

            # 写入头部标签
            worksheet.write(0, i, self._database_title[i])
            pass

        # 保存工作簿
        workbook.save(self._database_path)

        self._database_available = True

        pass

    def _Database_ReadFile(self):
        '''
        读取历史数据中最新的一条
        :return:
        '''
        # 若数据库现在不可用，等待
        while (not self._database_available):
            pass

        # 禁止其他应用操作
        self._database_available = False

        # 准备读入数据
        workbook = xlrd.open_workbook(self._database_path)
        worksheet = workbook.sheet_by_name('data')

        # 如果是新建的数据库，则使用初始值
        if worksheet.nrows == 1:
            self._database_last_data = []
        else:
            # 数据库中包含更新的数据，读入
            item = []
            for j in range(len(self._database_title)):
                item.append(worksheet.cell_value(worksheet.nrows - 1, j))
                pass
            self._database_last_data = item

        if (len(self._database_last_data) == 0):
            # 新建数据库，没有记录
            pass
        else:
            # 比较新老
            if (self._database_last_data[1] > self._database_latest_data[1]):
                self._database_latest_data = self._database_last_data

        logger.info(
            r"污染数据库读取完成，最新污染值为: {0}   PM2.5: {1} ".format(self._database_latest_data[0], self._database_latest_data[2]))
        # 允许其他应用操作
        self._database_available = True

        pass

    def _Database_WriteFile(self):
        '''
        将数据库中最新的一条数据写入文件
        :return:
        '''
        # 读取并复制工作簿
        workbook = xlrd.open_workbook(self._database_path)
        workbook = copy(workbook)

        worksheet = workbook.get_sheet(0)
        rows = len(worksheet.rows)

        if (len(self._database_last_data) == 0):
            # 全新的数据页，可直接写入
            for i in range(len(self._database_latest_data)):
                worksheet.write(rows, i, self._database_latest_data[i])
                pass
            pass
        elif (self._database_last_data[1] < self._database_latest_data[1]):
            # 时间戳不一致，继续写入
            for i in range(len(self._database_latest_data)):
                worksheet.write(rows, i, self._database_latest_data[i])
                pass
            pass

        # 保存工作簿
        workbook.save(self._database_path)
        pass

    def Database_Set_Record(self, p_data):
        '''
        外部函数调用，写入数据
        :param data:
        :return:
        '''

        # 若数据库现在不可用，等待
        while (not self._database_available):
            pass

        stauts = True
        msg = ''

        # 禁止其他应用操作
        self._database_available = False

        # 如果获取的数据时间戳比数据库中新，则更新数据库
        if (p_data[1] > self._database_latest_data[1]):
            self._database_latest_data = p_data
            self._Database_WriteFile()
            logger.info(r"污染数据库读取完成，最新污染值为: {0}   PM2.5: {1} ".format(self._database_latest_data[0],
                                                                      self._database_latest_data[2]))
        else:
            pass

        # 允许其他使用
        self._database_available = True

        return stauts, msg


mRegister_Database = Database_Registeration()
mPollution_Database = Database_PollutionExposure()
