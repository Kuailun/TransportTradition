# -*- coding: utf-8 -*-
# @File       : __init__.py
# @Author     : Yuchen Chai
# @Date       : 2020/3/21 13:38
# @Description:

from flask import Flask
import os

# 检查Database路径
if not os.path.exists(os.getcwd()+"/Database"):
    os.mkdir(os.getcwd()+"/Database")

app=Flask(__name__)