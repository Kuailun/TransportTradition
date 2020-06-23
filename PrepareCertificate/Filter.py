# -*- coding: utf-8 -*-
# @File       : Filter.py
# @Author     : Yuchen Chai
# @Date       : 2020-05-19 16:19
# @Description:

import pandas as pd

df = pd.read_csv("证书制作.csv")

mList = []
temp = {"ID":"","Name":"","Gender":"","Age":"","Phone":""}
bad = []
for index, item in df.iterrows():
    le = len(item['Name'])
    temp = {"ID": "", "Name": "", "Gender": "", "Age": "", "Phone": ""}
    temp["ID"] = item['ID']
    temp['Name'] = item['Name']
    temp['Gender'] = item['Gender']
    temp['Age'] = item['Age']
    temp['Phone'] = item['Phone']
    if le==1 or le>=4:
        bad.append(temp)
    else:
        mList.append(temp)
        pass
    pass

dfg = pd.DataFrame(mList,columns=["ID","Name","Gender","Age","Phone"])
dfg.to_csv("Good.csv")
dfb = pd.DataFrame(bad,columns=["ID","Name","Gender","Age","Phone"])
dfb.to_csv("Bad.csv")