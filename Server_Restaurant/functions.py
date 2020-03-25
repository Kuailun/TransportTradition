# -*- coding: utf-8 -*-
# @File       : functions.py
# @Author     : Yuchen Chai
# @Date       : 2020/3/21 13:43
# @Description:

from Server_Restaurant.logger import logger
import json
import os
from Server_Restaurant import settings as ss
import pandas as pd
import re

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

class Database_Restaurant(Database):
    """
    基于Database类，餐厅数据库
    """

    def __init__(self):
        """
        初始化餐厅数据库
        """
        super(Database_Restaurant, self).__init__(ss.RESTAURANT_DATABASE_PATH, ss.RESTAURANT_DATABASE_NAME)
        # 数据库
        self._database = {}
        # 检查数据库的路径是否存在
        self._Database_Path_Existing()
        # 读取用户注册数据库
        self.__Database_ReadFile()

        pass

    def __Database_CreateFile(self):
        pass

    def __Database_ReadFile(self):
        """
        读入餐厅数据库
        @return:
        """

        # 若数据库现在不可用，等待
        while (not self._database_available):
            pass

        # 禁止其他应用操作
        self._database_available = False

        # 读入数据
        self._database = pd.read_csv(ss.RESTAURANT_DATABASE_PATH+ss.RESTAURANT_DATABASE_NAME)

        # 处理数据
        self._database = self._database.sort_values(by= ["Crowd"], ascending= False)
        crowd = self._database.Crowd.astype(float)
        crowd = crowd*100
        crowd = round(crowd, 1)
        crowd = crowd.astype(str) + "%"
        self._database.Crowd = crowd

        self._database_js = self.__Database_DF2JSON(self._database)

        # 允许其他应用操作
        self._database_available = True

        pass

    def __Database_WriteFile(self):
        pass

    def __Database_DF2JSON(self, df):
        """
        将dataframe转为json格式
        @param df:
        @return:
        """
        ret_data = []
        for index, row in df.iterrows():
            temp = {}
            temp['shopName'] = row.shopName
            temp['crowd'] = row.Crowd
            ret_data.append(temp)
            pass
        return ret_data

    def Restaurant_All(self):
        """
        返回所有数据
        @return:
        """
        return self._database_js

    def Restaurant_Key(self, keyword):
        """
        返回有关键词的数据
        @return:
        """
        # 若数据库现在不可用，等待
        while (not self._database_available):
            pass

        # 禁止其他应用操作
        self._database_available = False

        # 检查特殊字符
        regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
        # 没有特殊字符
        if regex.search(keyword) == None:
            df = self._database[self._database.shopName.str.contains(keyword, na=False)]
            ret_json = self.__Database_DF2JSON(df)
        else:
            ret_json = []
            for i in range(len(self._database_js)):
                temp = self._database_js[i]["shopName"].find(keyword)
                if temp >= 0:
                    ret_json.append(self._database_js[i])
                pass
            pass




        self._database_available = True

        return ret_json
    pass

mRestaurant = Database_Restaurant()