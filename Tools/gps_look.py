# -*- coding: utf-8 -*-
# @File       : gps_look.py
# @Author     : Yuchen Chai
# @Date       : 2020/3/12 20:59
# @Description:

with open("C:\\Users\\59367\Desktop\\40.txt", encoding="utf-8") as f:
    content = f.readline()
    pass

new_content = content.replace("},","\n")

with open("C:\\Users\\59367\Desktop\\744_new.txt","w",encoding="utf-8") as f:
    f.write(new_content)
    pass