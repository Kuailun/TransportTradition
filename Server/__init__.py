# -*- coding: utf-8 -*-
# @File        : __init__.py
# @Author      : Yuchen Chai
# @Date        : 2019/12/19 10:31
# @Description : 正式服务器的初始化

from flask import Flask
import os

# 检查Database路径
if not os.path.exists(os.getcwd()+"/Database"):
    os.mkdir(os.getcwd()+"/Database")

app=Flask(__name__)