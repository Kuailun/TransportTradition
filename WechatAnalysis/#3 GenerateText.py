# -*- coding: utf-8 -*-
# @File       : #3 GenerateText.py
# @Author     : Yuchen Chai
# @Date       : 2020-06-20 14:48
# @Description:

import pandas as pd

df = pd.read_csv("Wechat_Moments.csv")

df.fillna("")
puretext = df[['Text']]
puretext = puretext.to_dict("records")
output = []
with open("data_text.txt", 'w', encoding="utf8") as f:
    for item in puretext:
        s = str(item['Text'])
        if s!="nan":
            output.append(s)
    output = list(set(output))
    for item in output:
        f.write(item + "\n")