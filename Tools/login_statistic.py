# -*- coding: utf-8 -*-
# @File       : login_statistic.py
# @Author     : Yuchen Chai
# @Date       : 2020/3/11 9:31
# @Description: 将服务器上的用户登陆数据做统计

from Tools import CommonTools as ut
import xlwt

def save_xls(d,t,date):
    wb = xlwt.Workbook()
    ws = wb.add_sheet("data")
    period = ["Morning","Middle","Evening","Night","Others"]
    title = ["Weak","Strong","Others"]

    for i in range(len(t)):
        item = t[i]
        ws.write(i+1,0,item)
        for k in range(len(period)):
            su = 0
            p = period[k]

            for j in range(len(title)):
                su = su + d[str(item)]['login_statistic'][date][p][title[j]]
                pass

            ws.write(i+1,k+1,su)
            pass
        pass

    wb.save("data.xls")

data = ut.read_json("C:\\Users\\59367\Desktop\\UserLogin.josn")
date = "2020-03-22"

Beijing = [122,97,61,40,41,129,130,131,133,134,135,138,139,140,141,142,143,145,149,150,152,154,156,157,159,160,161,162,163,165,166,169,174,179,224,227,238,256,257,261,263,271,274,276,299,304,307,308,311,312,314,317,342,365,374,383,386,403,408,411,413,414,415,490,496,496,502,567,570,575,576,582,609,611,648,650,656,660,664,679,680,683,738,744,777,784,787,788,789,790,792,800,802,803,804]
today = []
todayBeijing = []
for item in data:
    if date in data[item]['history']:
        if not int(item) in Beijing:
            today.append(int(item))
        else:
            todayBeijing.append(int(item))
        pass
    pass

print(1)

giveMoney = []
# 多少人符合给钱标准
for i in range(len(today)):
    todayItem = data[str(today[i])]['login_statistic'][date]
    morning = todayItem["Morning"]['Weak'] + todayItem["Morning"]['Strong']
    middle = todayItem["Middle"]['Weak'] + todayItem["Middle"]['Strong']
    evening = todayItem["Evening"]['Weak'] + todayItem["Evening"]['Strong']
    night = todayItem["Night"]['Weak'] + todayItem["Night"]['Strong']

    if morning >= 900 or middle >= 180 or evening >= 900 or night >= 180:
        giveMoney.append(today[i])
        pass
    pass

# Sent = [119, 124, 130, 136, 146, 148, 158, 164, 177, 218, 229, 246, 247, 251, 258, 263, 265, 305, 321, 325, 370, 383, 395, 402, 406, 407, 409, 410, 433, 44, 45, 46, 460, 474, 478, 49, 513, 521, 522, 538, 546, 562, 59, 596, 598, 600, 62, 70, 74, 89]
# count = []
# for item in Sent:
#     if item in today:
#         count.append(item)
#         pass
#     pass

save_xls(data, today, date)