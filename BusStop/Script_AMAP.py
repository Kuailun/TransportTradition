# -*- coding: utf-8 -*-
# @File       : Script_AMAP.py
# @Author     : Yuchen Chai
# @Date       : 2020/1/14 21:44
# @Description:

import xlrd,xlwt
from Server.logger import logger
from Server import settings as ss
import requests
import time

def _busStop_Load_Data(data_path):
    '''
    从源文件中读取公交站原始数据
    :return:
    '''

    book = xlrd.open_workbook(data_path)
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

def _busStop_Remove_Duplication(p_data):
    '''
    清洗数据，去掉重复项，去掉不符合要求的项目
    :return:
    '''

    logger.debug(r'读取完成后，公交数据库中有{0}项'.format(len(p_data)))

    # 去掉数据中重复的ID值
    index = []
    ret_data = []
    for i in range(len(p_data)):
        if p_data[i][4] not in index:
            index.append(p_data[i][4])
            ret_data.append(p_data[i])
            pass
        pass

    p_data = ret_data

    logger.debug(r'去除重复的id后，公交数据库中有{0}项'.format(len(p_data)))

    # 去掉范围之外的数据
    ret_data = []
    for i in range(len(p_data)):
        if p_data[i][0] > ss.PREDICTION_BUSSTOP_LOCATION_LON_MAX:
            continue
        elif p_data[i][0] < ss.PREDICTION_BUSSTOP_LOCATION_LON_MIN:
            continue
        elif p_data[i][1] > ss.PREDICTION_BUSSTOP_LOCATION_LAT_MAX:
            continue
        elif p_data[i][1] < ss.PREDICTION_BUSSTOP_LOCATION_LAT_MIN:
            continue
        ret_data.append(p_data[i])
        pass

    p_data = ret_data
    logger.debug(r'去除范围之外的数据后，公交数据库中有{0}项'.format(len(p_data)))

    return p_data

def _busStop_Get_AMAP(p_data):
    '''
    根据POI从高德获取经纬度信息
    :param p_data:
    :return:
    '''
    url = 'https://www.amap.com/detail/get/detail'
    data = {'id': 'BV11019257'}
    header = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN, zh;q=0.9',
        'amapuuid': '5711328c-7f52-4ee1-a438-57d46ed42a03',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Cookie': 'cna=OL6XFcPwsCwCAXM8l7iDI1Rb; UM_distinctid=16f7cda0f9019-0dab80344f72ab-34564a7c-1fa400-16f7cda0f911a5; passport_login=MjQ2ODMzNDYwLGFtYXBfMTM4MTAyOTM2NDBCTnRFd0Q3WE0sbHVwYzd6N241bzM0dmQ2c3Zxc2d6ZnZxY3A1M2IyYmssMTU3ODM0NzcxMyxOamMyWXpkaE5qbGxaRGN6TW1SbU9URmpNVGMxWmpSbU1UVTJNRE0zT1dJPQ%3D%3D; dev_help=PukvRWZyuwatO1dM3Y1FdzJjNGU1ZjMyZWMwZGQ0OWZlZDQ4NzA5ODcwZjA2ZDU3NWE0ZjZjMDFjMDViMGE0YWNkMTNkOTJlNGY0YmJjN2SJgbpmWFAlWgCEu2%2FZ%2FqSO2KOLpmdpBbzl7fPpvOxgFK1v3HjLgS68maIe%2FuFk0GlA2hbdjcNUzilRv1021dlAFo4lz%2BygbdNovYUe10W4cDrvcJW6oQf6qV70dO0G%2BLhdgBbmaWtO4EYRkd5r2I9R; CNZZDATA1255626299=1601011742-1578528758-https%253A%252F%252Fwww.baidu.com%252F%7C1579009647; x-csrf-token=9d037d8e04abb5be926a1c1892bc4c51; x5sec=7b22617365727665723b32223a2236326565323764346438343037666262666238626165326230633436343732664349756a392f4146454c69417a64797869367a6743513d3d227d; l=cBg72U6cqa4oFfh8BOfwZEwXGo7OyQJRCNVyhO7aZICP_0W68iWRWZDB9vtBCnhVLsb9J3lYhYu7BRYsCyzhCf2gY9ce8k45.; isg=BFBQGHdVOs7XfeXxFamN4895NJ6wByTnK6yNRUojrKt-hfcv8ysg8ll7XQ3ABuw7',
        'Pragma': 'no-cache',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3741.400 QQBrowser/10.5.3863.400',
        'x-csrf-token': '9d037d8e04abb5be926a1c1892bc4c51',
        'X-Requested-With': 'XMLHttpRequest'
    }

    for i in range(len(p_data)):
        data['id'] = p_data[i][4]
        try:
            ret = requests.get(url, params=data, headers=header)
            txt = ret.json()
            txt = txt['data']['base']
            p_data[i].append(txt['x'])
            p_data[i].append(txt['y'])
            time.sleep(0.1)
            print('Index: {0}, ID: {1}'.format(i, p_data[i][4]))
        except:
            print('wrong')

    return p_data

def _busStop_Write_File(p_data):
    '''
    将获取的数据写入文件
    :param p_data:
    :return:
    '''
    myexcel = xlwt.Workbook()
    sheet = myexcel.add_sheet('sheet')
    for i in range(len(p_data)):
        for j in range(len(p_data[i])):
            sheet.write(i,j,p_data[i][j])
            pass
        pass
    myexcel.save('E:\WorkSpace\Python\TransportTradition\Server\Database\BusStop2.xls')


mData = _busStop_Load_Data('E:\WorkSpace\Python\TransportTradition\Server\Database\BusStop.xls')
mData = _busStop_Remove_Duplication(mData)
mData = _busStop_Get_AMAP(mData)
_busStop_Write_File(mData)
print(1)