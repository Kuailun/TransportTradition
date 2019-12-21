# -*- coding: utf-8 -*-
# @File       : Registeration.py
# @Author     : Yuchen Chai
# @Date       : 2019/12/19 16:13
# @Description:

import os
from Server.logger import logger
from Server.settings import REGISTERATION_DATABASE_PATH, REGISTERATION_DATABASE_NAME, REGISTERATION_INTERFACE_KEYWORDS
import xlrd, xlwt


class Registeration:
    def __init__(self):
        '''
        初始化用户注册类，维护数据库
        '''

        # 数据库路径
        self._database_path = REGISTERATION_DATABASE_PATH + REGISTERATION_DATABASE_NAME
        # 数据库是否可用标签
        self._database_available = True
        # 工作簿头部标签
        self._database_title = ['用户ID', '姓名', '电话', '家庭地址', '工作地址','家庭经度','家庭纬度','办公经度','办公纬度', '开车距离', '开车时间', '公共交通-公交距离', '公共交通-公交时间',
                                '公共交通-地铁距离', '公共交通-地铁时间',
                                '公共交通-步行距离', '公共交通-步行时间', '骑行距离', '骑行时间', '步行距离', '步行时间']
        # 数据库
        self._database = {}

        # 检查数据库的路径是否存在
        if not os.path.exists(self._database_path):
            logger.info("用户注册数据库不存在，开始创建")
            self._Registeration_CreateFile()
            pass
        else:
            pass

        # 读取用户注册数据库
        self._Registeration_ReadFile()
        pass

    def _Registeration_CreateFile(self):
        '''
        创建用户注册的数据库
        :return:
        '''

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

    def _Registeration_ReadFile(self):
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

        logger.info("用户注册数据库读取完成，共计 "+ str(len(self._database))+ ' 项')
        # 允许其他应用操作
        self._database_available = True
        pass

    def _Registeration_WriteFile(self):
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
        for i,item in enumerate(self._database):
            for j in range(len(self._database_title)):
                worksheet.write(i + 1, j, self._database[item][j])
                pass
            pass

        # 保存工作簿
        workbook.save(self._database_path)

        pass

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
            logger.warning("数据包不完整，缺少关键字")
            return False, '数据包不完整，缺少关键字'

        # 检查数据的一致性
        for item in keyWords:
            if not item in js:
                status = False
                logger.warning('数据包名称错误，缺少' + str(item))
                return status, '数据包名称错误，缺少' + str(item)

        newItem = [0 for i in range(len(self._database_title))]

        # 除type外，其余均放到新的一项中
        for i in range(len(keyWords) - 1):
            newItem[i] = js[keyWords[i]]
            pass

        # 若数据库现在不可用，等待
        while (not self._database_available):
            pass

        self._database_available = False

        # 新注册用户
        if (js['type'] == '1'):
            # 并非首次注册，已存在于数据库中
            if (js['userId'] in self._database):
                self._database[js['userId']] = newItem
                status = True
                msg = "用户ID已存在于数据库中，非首次注册： " + str(js['userId'])
                logger.warning(msg)


            # 首次注册，成功添加
            else:
                self._database[js['userId']] = newItem
                status = True
                msg = ''
        # 非新注册用户
        elif (js['type'] == '2'):
            # 并非首次注册，已存在于数据库中
            if not (js['userId'] in self._database):
                self._database[js['userId']] = newItem
                status = True
                msg = "用户ID不在数据库中，首次注册： " + str(js['userId'])
                logger.warning(msg)

            # 非首次注册，成功更新
            else:
                self._database[js['userId']] = newItem
                status = True
                msg = ''
        # 发来的Type错误
        else:
            status = False
            msg = '发送的用户注册类型错误： ' + str(js['userId'])+ '-'+ str(js['type'])
            logger.warning(msg)
            pass

        # 写到外部文件
        self._Registeration_WriteFile()

        # 允许其他应用操作
        self._database_available = True
        return status, msg

    def Registeration_Interface(self, data):
        '''
        接受服务器传来的用户注册数据并处理
        :param data:
        :return:
        '''

        status = True
        msg = ''

        status, msg = self._Registeration_ExtractData(data)

        # 成功
        if status:
            return 0, msg
        # 失败
        else:
            return 1, msg

        pass

    pass


registeration = Registeration()
