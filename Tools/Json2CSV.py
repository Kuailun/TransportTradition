# -*- coding: utf-8 -*-
# @File       : Json2CSV.py
# @Author     : Yuchen Chai
# @Date       : 2020/4/3 14:17
# @Description:

import json
import pandas as pd
import Tools.CommonTools as ut

data = ut.read_json("C:\\Users\\59367\Desktop\\RestaurantView.json")
ret_data = []
for item in data['record']:
    ret_data.append(item)
    pass

# df = pd.DataFrame(ret_data,columns=['cellphone','predict_rest','predict_park','rest_risk','park_risk','willing',"IP","Timestamp"])
df = pd.DataFrame(ret_data,columns=['IP','Timestamp'])
print(df)
df.to_csv("Website.csv")