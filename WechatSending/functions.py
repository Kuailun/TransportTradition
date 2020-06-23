# -*- coding: utf-8 -*-
# @File       : functions.py
# @Author     : Yuchen Chai
# @Date       : 2020/4/4 20:35
# @Description:

import pyautogui as pg
from WechatSending import settings
import time
import pyperclip
import random
from io import BytesIO
import win32clipboard
import clipboard
import os
import PIL.Image as Image

def Wait():
    """
    随机等待函数
    @return:
    """
    # long_parameter = random.randint(0,100)
    # if long_parameter >= 95:
    #     wait_time = random.randint(65,105)
    # elif long_parameter <= 5:
    #     wait_time = random.randint(100,500)/1000
    # # elif long_parameter <= 30:
    # #     wait_time = random.randint(22000,35000)/1000
    # else:
    #     wait_time = random.randint(3000,10000)/1000
    wait_time = random.randint(3000, 10000) / 1000
    print("\r等待时间：{0}".format(wait_time), end="")
    time.sleep(wait_time)
    return

def step01_get_wechat_icon():
    """
    用于获取并修改微信图标位置
    @return:
    """
    # 微信图标位置
    try:
        while(True):
            print("\r+{0}".format(pg.position()),end="",flush=True)
            pass
    except KeyboardInterrupt:
        print("开始自动发送")
        pass
    return

def step02_prepare_wechat():
    """
    用于打开微信并准备
    @return:
    """
    pg.leftClick(settings.wechat_icon_pos[0],settings.wechat_icon_pos[1])
    pass

def step03_read_data(path):
    """
    根据路径读入数据
    @param path:
    @return:
    """
    mPath = settings.data_path + "\\" + path + "\\data.txt"
    mData = {"Name":"","Data":[]}
    mLines = []
    with open(mPath, 'r', encoding='utf-8') as f:
        mLines = f.readlines()
        f.close()
        pass

    mData['Name'] = mLines[0].replace("\n","")
    for i in range(len(mLines)-1):
        if mLines[i+1].find("Text:")>=0:
            mContent = mLines[i+1][5:]
            mContent = mContent.replace("\n","")
            mContent = mContent.replace("[return]","\n")
            mData['Data'].append({"Type":"Text","Data":mContent})
            pass
        pass
    return mData

def step03_read_image(item):
    mPath = settings.data_path + "\\" +item + "\\Image.jpg"
    img = Image.open(mPath)
    output=BytesIO()
    img.convert("RGB").save(output,'BMP')
    img=output.getvalue()[14:]
    output.close()

    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(win32clipboard.CF_DIB,img)
    win32clipboard.CloseClipboard()
    return


def step04_send_wechat(p_data):
    """
    找到用户并发送内容
    @param p_data:
    @return:
    """
    print("\n正在给{0}发送消息".format(p_data['Name']))

    # 搜索用户
    pyperclip.copy(p_data['Name'])
    pg.leftClick(settings.wechat_search_line[0],settings.wechat_search_line[1])
    pg.hotkey("ctrlleft",'v')

    time.sleep(1)

    # 检测是否存在
    img = pg.screenshot()
    color1 = img.getpixel((140, 109))
    color2 = img.getpixel((150, 119))
    if color1 == (26, 173, 25) and color2 == (26, 173, 25):
        pg.leftClick(settings.wechat_cancel_button[0], settings.wechat_cancel_button[1])
        return False
    elif color1[0] == 0 and color1[1] == 0 and color1[2] == 0 and color2[0] == 0 and color2[1] == 0 and color2[2] == 0 :
        exit(-1)
        return False

    # 点击该人头像
    pg.leftClick(settings.wechat_target_icon[0], settings.wechat_target_icon[1])

    # 循环输入内容
    for i in range(len(p_data["Data"])):
        if p_data['Data'][i]['Type'] == "Text":
            # 点击输入栏
            pg.leftClick(settings.wechat_content_line[0], settings.wechat_content_line[1])

            # 复制进入内容
            pyperclip.copy(p_data['Data'][i]['Data'])
            pg.hotkey("ctrlleft",'v')

            # 点击发送
            pg.leftClick(settings.wechat_send_button[0],settings.wechat_send_button[1])

            # 等待，防止被踢下线
            Wait()
            pass
        pass
    return True

def step04_send_wechat_image(name):
    """
    找到用户并发送内容
    @param p_data:
    @return:
    """
    print("\n正在给{0}发送消息".format(name))

    # 搜索用户
    pyperclip.copy(name)
    pg.leftClick(settings.wechat_search_line[0],settings.wechat_search_line[1])
    pg.hotkey("ctrlleft",'v')

    time.sleep(1)

    # 检测是否存在
    img = pg.screenshot()
    color1 = img.getpixel((140, 109))
    color2 = img.getpixel((150, 119))
    if color1 == (26, 173, 25) and color2 == (26, 173, 25):
        pg.leftClick(settings.wechat_cancel_button[0], settings.wechat_cancel_button[1])
        return False
    elif color1[0] == 0 and color1[1] == 0 and color1[2] == 0 and color2[0] == 0 and color2[1] == 0 and color2[2] == 0 :
        exit(-1)
        return False

    # 点击该人头像
    pg.leftClick(settings.wechat_target_icon[0], settings.wechat_target_icon[1])

    # 循环输入内容
    # 点击输入栏
    pg.leftClick(settings.wechat_content_line[0], settings.wechat_content_line[1])

    # 复制进入内容
    step03_read_image(name)
    time.sleep(1)
    pg.hotkey("ctrlleft", 'v')

    # 点击发送
    pg.leftClick(settings.wechat_send_button[0], settings.wechat_send_button[1])

    # 等待，防止被踢下线
    Wait()
    return True