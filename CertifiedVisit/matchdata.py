# -*- coding: utf-8 -*-
# @File       : matchdata.py
# @Author     : Yuchen Chai
# @Date       : 2020-06-17 15:17
# @Description:

import pandas as pd
import json

df_survey = pd.read_csv("#1 Processed Survey Result.csv")
df_dict = pd.read_csv("#3 Processed Restaurant Dictionary.csv")

df_dict = df_dict.fillna("")

# 去掉记录为空的
df_survey = df_survey[(df_survey["rest_actual"]!="否") & (df_survey['rest_name']!="(空)")]
df_survey_clean = df_survey[['phone','user_index','restaurant_visitation','rest_name']]
df_survey_clean = df_survey_clean.to_dict("records")

df_survey_list = []
for item in df_survey_clean:
    mStr = item['restaurant_visitation'].replace("'",'"')
    times = json.loads(mStr)
    for time in times:
        df_survey_list.append({"phone":item['phone'],'user_index':item['user_index'],'rest_name':item['rest_name'],"time":time})
        pass
    pass

# 准备好餐馆字典
df_dict = df_dict.to_dict("records")
mDict = {}
for item in df_dict:
    mDict[item['origin_name']] = item
    pass

# 更新调研记录
for i in range(len(df_survey_list)):
    item = df_survey_list[i]
    old_name = item['rest_name']
    code = -1
    new_name = ""
    certified = ""
    special_mark = ""

    if old_name in mDict:
        new_name = mDict[old_name]['final_name']
        code = mDict[old_name]['errorcode']
        if code == 0 or code == 3 or code == 2:
            certified = mDict[old_name]['certified']
            special_mark = mDict[old_name]['hasany']
            if special_mark == 1:
                special_mark = "TRUE"
            else:
                special_mark = certified
            pass
    df_survey_list[i]['code'] = code
    df_survey_list[i]['certified'] = certified
    df_survey_list[i]['special_mark'] = special_mark

df = pd.DataFrame(df_survey_list)
df.to_csv("processed_survey_result.csv")