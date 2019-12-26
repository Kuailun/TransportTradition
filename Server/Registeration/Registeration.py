# -*- coding: utf-8 -*-
# @File       : Registeration.py
# @Author     : Yuchen Chai
# @Date       : 2019/12/19 16:13
# @Description: 用户注册类

import os
from Server.logger import logger
from Server.settings import REGISTERATION_INTERFACE_KEYWORDS, REGISTERATION_SERVICE_KEYWORDS
import xlrd, xlwt
from Server.functions import mRegister_Database


class Registeration:
    def __init__(self):
        self._status = True
        self._msg = ''
        pass

    def Registeration_Interface(self, data):
        '''
        接受服务器传来的用户注册数据并处理
        :param data:
        :return:
        '''

        status = True
        msg = ''

        if self._status == True:
            status, msg = self._Registeration_ExtractData(data)

        else:
            status = False
            msg = self._msg

        # 成功
        if status:
            return 0, msg
        # 失败
        else:
            return 1, msg

        pass

    def Registeration_Service_Interface(self, data):
        '''
        接受服务器传来的用户注册命令并处理
        :param data:
        :return:
        '''

        status = True
        msg = ''

        # 提取命令内容
        status, msg, type = self._Registeration_Service_ExtractData(data)

        # 停止接收新注册
        if type == 'USER_STOP_REGISTER':
            self._status = False
            self._msg = r'服务器更新用户注册数据库，暂停接收新注册'
            msg = self._msg
            logger.warning(self._msg)
            pass

        # 开始接收新注册
        if type == 'USER_START_REGISTER':
            mRegister_Database.Database_ReadFile()
            self._status = True
            self._msg = r'服务器正常接收新注册'
            msg = self._msg
            logger.info(msg)
            pass

        return status, msg


    def _Registeration_Service_ExtractData(self, js):
        '''
        从外部提交的数据还原数据结构
        :param js:
        :return:
        '''
        # 获取传送来的数据模板
        keyWords = REGISTERATION_SERVICE_KEYWORDS

        status = True
        msg = ''

        # 检查数据个数
        if not len(js) == len(keyWords):
            logger.warning(r"数据包不完整，缺少关键字")
            return False, '数据包不完整，缺少关键字'

        # 检查数据的一致性
        for item in keyWords:
            if not item in js:
                status = False
                logger.warning(r'数据包名称错误，缺少' + str(item))
                return status, '数据包名称错误，缺少' + str(item)

        return True, '', js[keyWords[0]]


    def _Registeration_ExtractData(self, js):
        '''
        从外部提交的数据还原数据结构
        :param js:
        :return:
        '''

        # 获取传送来的数据模板
        keyWords = REGISTERATION_INTERFACE_KEYWORDS

        status = True
        msg = ''

        # 检查数据个数
        if not len(js) == len(keyWords):
            logger.warning(r"数据包不完整，缺少关键字")
            return False, '数据包不完整，缺少关键字'

        # 检查数据的一致性
        for item in keyWords:
            if not item in js:
                status = False
                logger.warning(r'数据包名称错误，缺少' + str(item))
                return status, '数据包名称错误，缺少' + str(item)

        newItem = [0 for i in range(mRegister_Database.Database_Get_Title_Number())]

        # 除type外，其余均放到新的一项中
        for i in range(len(keyWords) - 1):
            newItem[i] = js[keyWords[i]]
            pass

        if js['type'] == '1':
            # 新插入一个记录
            status, msg = mRegister_Database.Database_Set_Record(newItem)
        elif js['type'] == '2':
            # 更新一个记录
            status, msg = mRegister_Database.Database_Update_Record(newItem)
        else:
            # 错误的代码
            status = False
            msg = r'发送的用户注册类型错误： ' + str(newItem[0]) + '-' + str(js['type'])
            logger.warning(msg)
            pass

        return status, msg

    pass


registeration = Registeration()
