# -*- coding: utf-8 -*-
# @File       : Financial.py
# @Author     : Yuchen Chai
# @Date       : 2020/3/14 9:45
# @Description:
import xlrd


def read_xls(path):
    data = xlrd.open_workbook(path)
    table = data.sheet_by_name("sheet1")

    ret_data = []
    for i in range(table.nrows - 1):
        item = {"Date":"","Name":"","Type":"","Number":0}
        item['Date'] = table.cell_value(i+1, 0)
        item['Name'] = table.cell_value(i+1, 1)
        item['Type'] = table.cell_value(i+1, 3)
        item['Number'] = int(table.cell_value(i+1, 4))/100
        ret_data.append(item)
        pass
    return ret_data

data = read_xls("C:\\Users\\59367\Desktop\\账户明细.xls")
print(1)

virtual = 0
real = 0
da = {"用户提现":0,"每日任务完成奖励":0,"系统充值":0,"其他":0}

for i in range(len(data)):
    for j in da:
        if j == data[i]['Type']:
            da[j] = da[j] + data[i]['Number']
            pass
        pass
    pass

print(1)