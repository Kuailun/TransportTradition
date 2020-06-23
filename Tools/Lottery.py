# -*- coding: utf-8 -*-
# @File       : Lottery.py
# @Author     : Yuchen Chai
# @Date       : 2020/4/6 15:22
# @Description:

from Tools import CommonTools as ct
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

data = ct.read_json("C:\\Users\\59367\Desktop\\UserLogin.josn")
date = ["2020-04-04","2020-04-05"]

Beijing = [122,97,61,40,41,129,130,131,133,134,135,138,139,140,141,142,143,145,149,150,152,154,156,157,159,160,161,162,163,165,166,169,174,179,224,227,238,256,257,261,263,271,274,276,299,304,307,308,311,312,314,317,342,365,374,383,386,403,408,411,413,414,415,490,496,496,502,567,570,575,576,582,609,611,648,650,656,660,664,679,680,683,738,744,777,784,787,788,789,790,792,800,802,803,804]
potential = []
todayBeijing = []
for item in data:
    if date[0] in data[item]['history'] and date[1] in data[item]['history']:
        if not int(item) in Beijing:
            potential.append(int(item))
        pass
    pass

lottery = []
# 多少人符合给钱标准
for i in range(len(potential)):
    for j in range(len(date)):
        todayItem = data[str(potential[i])]['login_statistic'][date[j]]
        morning = todayItem["Morning"]['Weak'] + todayItem["Morning"]['Strong']
        middle = todayItem["Middle"]['Weak'] + todayItem["Middle"]['Strong']
        evening = todayItem["Evening"]['Weak'] + todayItem["Evening"]['Strong']
        night = todayItem["Night"]['Weak'] + todayItem["Night"]['Strong']

        if middle >= 180 and evening >= 900:
            if j == 1:
                lottery.append(potential[i])
            else:
                continue
            pass
        else:
            break
    pass

i=0
while i < len(lottery):
    if "2020-04-03" in data[str(lottery[i])]['history']:
        todayItem = data[str(lottery[i])]['login_statistic']["2020-04-03"]
        morning = todayItem["Morning"]['Weak'] + todayItem["Morning"]['Strong']
        middle = todayItem["Middle"]['Weak'] + todayItem["Middle"]['Strong']
        evening = todayItem["Evening"]['Weak'] + todayItem["Evening"]['Strong']
        night = todayItem["Night"]['Weak'] + todayItem["Night"]['Strong']

        if evening >= 900:
            i = i + 1
            continue
        else:
            lottery.pop(i)
            i = i
            pass
    else:
        lottery.pop(i)
        i = i + 1

save_xls(data, lottery,"2020-04-05")