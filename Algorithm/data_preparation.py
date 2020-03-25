# -*- coding: utf-8 -*-
# @File       : data_preparation.py
# @Author     : Yuchen Chai
# @Date       : 2020/3/18 11:17
# @Description:

import pandas as pd
from Tools import CommonTools as ct

df = pd.read_csv("F:\\WorkSpace\\python\\TransportTradition\\Algorithm\\top1000_restaurant_lastComments.csv",encoding='gbk',sep=",")
# print(df.columns.values)
df_5stars = df[df.shopPowerTitle == "五星商户"]
# print(df_5stars)

df_export = df_5stars[["geoLat","geoLng","shopName"]]
# print(df_export[0:1])

poiData = {
    "First":[
        {
            "Name":"Home",
            "Latitude":0,
            "Longitude":0
        },
        {
            "Name":"Office",
            "Latitude":0,
            "Longitude":0
        }
    ],
    "Second":[

    ],
    "Third":[

    ]
}

for index, row in df_export.iterrows():
    temp = {}
    temp['Name'] = row['shopName']
    temp['Latitude'] = round(float(row['geoLat']),6)
    temp['Longitude'] = round(float(row['geoLng']),6)
    poiData['Second'].append(temp)
    pass

ct.write_json("top_restaurant.json",poiData)