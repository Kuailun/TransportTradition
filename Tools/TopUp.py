# -*- coding: utf-8 -*-
# @File       : TopUp.py
# @Author     : Yuchen Chai
# @Date       : 2020/3/22 8:15
# @Description:

import xlrd
import requests

wb = xlrd.open_workbook("E:\Dropbox (MIT)\文档\MIT\Siqi\RCT1\实施阶段\大问卷1\问卷1-第三次充值.xlsx")
ws = wb.sheet_by_name("Sheet1")

numbers = []
for i in range(ws.nrows):
    numbers.append(ws.cell_value(i,68))
    pass
numbers = numbers[1:]

# 已充值数据库
wb = xlrd.open_workbook("E:\Dropbox (MIT)\文档\MIT\Siqi\RCT1\实施阶段\大问卷1\问卷1-已给钱用户.xlsx")
ws = wb.sheet_by_name("Sheet1")

already = []
for i in range(ws.nrows):
    already.append(ws.cell_value(i,0))
    pass

# 生成未给钱列表
datatosend = []
for i in range(len(numbers)):
    if numbers[i] in already:
        continue
    else:
        datatosend.append(int(numbers[i]))
        pass
    pass
# Todo: 跟已有数据库匹配

url = "http://47.94.224.205/server/api/user/userCharge"
raw = {
"describe":"问卷1奖励",
"key":"5UmQyY2HxC2v6XZhbhgKfJUSb7sc5MHF",
"money":"2000",
"type":10,
"userPhone":None
}


for i in range(len(datatosend)):
    raw['userPhone'] = datatosend[i]
    resp = requests.post(url=url,json=raw)
    print(i)
    pass