# -*- coding: utf-8 -*-
# @File       : CommonTools.py
# @Author     : Yuchen Chai
# @Date       : 2020/3/11 9:32
# @Description:

import json
import time

def read_json(path):
    """
    根据路径读入Json数据
    @param path:
    @return:
    """
    with open(path,'r',encoding='utf-8') as f:
        content = json.load(f)

        return content
    pass

def write_json(path, content):
    """
    根据路径写入Json数据
    @param path:
    @param content:
    @return:
    """
    with open(path,'w',encoding='utf-8') as f:
        json_str = json.dump(content,f)
        pass

def TimeStr_TimeStamp(p_str):
    """
    时间字符串转时间戳
    @return:
    """
    timeArray = time.strptime(p_str, "%Y-%m-%d %H:%M:%S")
    timeStamp = int(time.mktime(timeArray))
    return timeStamp