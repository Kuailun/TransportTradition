# -*- coding: utf-8 -*-
# @File       : 02_FixProblemInCSV.py
# @Author     : Yuchen Chai
# @Date       : 2020-05-28 16:24
# @Description:

import pandas as pd
from commonTools import timeDelay as td
import os


def visits(p_date, p_time):
    if p_date == "(空)":
        return []
    elif p_date == "(跳过)":
        return []
    else:
        dates = p_time.split("┋")
        ret = []
        for item in dates:
            date = ""
            if item[1] == "五":
                date = date + td.timestamp2Date(p_date)[:10]
            elif item[1] == "六":
                date = date + td.timestamp2Date(p_date + 86400)[:10]
            elif item[1] == "日":
                date = date + td.timestamp2Date(p_date + 86400 * 2)[:10]
            elif item[0] == "5":
                date = "2020-05-0{0}".format(item[2])
            if item[0]!="5":
                if item[2:] == "中午":
                    date = date + " noon"
                elif item[2:] == "晚上":
                    date = date + " evening"
                    pass
                pass
            ret.append(date)
            pass
        pass
    return ret
def process_csvs(p_user):
    dirs = os.listdir("restaurant_name")
    ret_data = []
    dates = [1585872001+43200,1586476801+43200,1587081601+43200,1587686401+43200,1588291201+43200]
    index = 0
    for item in dirs:
        df = pd.read_csv("restaurant_name/" + item)
        for i, d in df.iterrows():
            try:
                temp = {
                    "rest_actual":d['rest_actual'],
                    "rest_time":d['rest_time'],
                    "rest_name":d['rest_name'],
                    "phone":d['phone'],
                    "user_index": p_user[p_user.手机号==d['phone']]['用户id'].values[0],
                    "restaurant_visitation": visits(dates[index],d['rest_time'])
                }
                ret_data.append(temp)
            except:
                pass
            pass
        index = index + 1
        pass
    return ret_data

if __name__ == "__main__":
    # Step01 Read in user file
    users = pd.read_csv("app user.csv")

    # Step02 find the result number for each restaurant name
    restaurant_info = process_csvs(users)

    df = pd.DataFrame(restaurant_info,columns=['rest_actual','rest_time','rest_name','phone','user_index',"restaurant_visitation"])
    df.to_csv("week1-5.csv")