# -*- coding: utf-8 -*-
# @File       : GenerateCertificate.py
# @Author     : Yuchen Chai
# @Date       : 2020-05-19 16:36
# @Description:

from PIL import Image,ImageDraw,ImageFont
import pandas as pd
import os
import copy

img_raw = Image.open("证书.jpg")


def Generate(Name,Phone):

    img_new = copy.deepcopy(img_raw)

    line = Name
    color = (0, 0, 0)
    text_size = 100
    pos = (400, 1800)

    draw = ImageDraw.Draw(img_new)
    font = ImageFont.truetype("simhei.ttf", text_size, encoding="utf-8")
    draw.text(pos, line, color, font)

    if os.path.exists("Data\\" + str(Phone)):
        pass
    else:
        os.mkdir("Data\\" + str(Phone))
    img_new.save("Data\\" + str(Phone) + "\\Image.jpg")
    with open("Data\\" + str(Phone) + "\\data.txt",'w') as f:
        f.write(str(Phone)+"\n")
        f.write("Image: F:\\WorkSpace\\python\\TransportTradition\\PrepareCertificate\\Data\\"+str(Phone) + "\\Image.jpg")
        f.close()
        pass
    return



if __name__ == "__main__":
    df = pd.read_csv("Good.csv")
    mList = []
    for index,item in df.iterrows():
        Generate(item['Name'],item['Phone'])
        print(index)
        pass