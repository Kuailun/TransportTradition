# -*- coding: utf-8 -*-
# @File       : #2 GenerateArticle.py
# @Author     : Yuchen Chai
# @Date       : 2020-06-20 14:46
# @Description:

import pandas as pd

df = pd.read_csv("Wechat_Moments.csv")

df.fillna("")
puretext = df[['Article']]
puretext = puretext.to_dict("records")
output = []
with open("data_article.txt", 'w', encoding="utf8") as f:
    for item in puretext:
        s = str(item['Article'])
        if s!="nan":
            output.append(s)
    output = list(set(output))
    for item in output:
        f.write(item + "\n")