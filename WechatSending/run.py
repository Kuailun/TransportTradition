# -*- coding: utf-8 -*-
# @File       : run.py
# @Author     : Yuchen Chai
# @Date       : 2020/4/4 20:34
# @Description: 利用pyautogui包自动化发送微信

import time
import os
import shutil
from WechatSending import functions as ut
from WechatSending import settings as ss

# Step01 获取微信图标位置
if ss.GetIcon:
    ut.step01_get_wechat_icon()

# Step02 准备微信窗口
ut.step02_prepare_wechat()

# 循环读入文件夹下的内容
dirList = os.listdir(ss.data_path)

status_data = []
start_time = time.time()
for item in dirList:

    # Step03 读入数据内容
    # sending_data = ut.step03_read_data(item)


    # Step04 发送该微信
    # status = ut.step04_send_wechat(sending_data)
    status = ut.step04_send_wechat_image(item)

    # 检测发送状态
    if status:
        if ss.DeleteDir:
            # 删除文件夹
            shutil.rmtree(ss.data_path + "\\" + item)
        pass

    else:
        print("该用户发送失败：{0}".format(item))
        # exit()
        status_data.append(item)
        pass
    pass

print("\n总计需要发送{0}个微信，其中成功{1}个，有{2}个失败".format(len(dirList),len(dirList)-len(status_data),len(status_data)))
end_time = time.time()
print("总用时{0}，平均用时{1}".format(end_time-start_time, (end_time-start_time)/len(dirList)))