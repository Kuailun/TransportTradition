# -*- coding: utf-8 -*-
# @File       : OnebyOne.py
# @Author     : Yuchen Chai
# @Date       : 2020-06-12 10:48
# @Description:

from appium import webdriver
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from commonTools import timeDelay as td
import time
import os

class Wechat_Moment():
    def __init__(self):
        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        desired_caps['platformVersion'] = '8'
        desired_caps['deviceName'] = 'APU0215B30003729'
        desired_caps['appPackage'] = 'com.tencent.mm'
        desired_caps['appActivity'] = '.ui.LauncherUI'
        desired_caps['noReset'] = True

        # 定义在朋友圈的时候滑动位置
        self.start_x = 300
        self.start_y = 1000
        self.end_x = 300
        self.end_y = 100

        # 启动微信
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
        # 设置等待
        self.wait = WebDriverWait(self.driver, 300)
        print('微信启动...')


    def login(self):
        # 获取到登录按钮后点击
        login_btn = WebDriverWait(self.driver,5).until(EC.presence_of_element_located((By.ID,"com.tencent.mm:id/ene")))
        login_btn.click()
        # 获取到授权按钮后点击
        auth_btn = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.ID, "com.tencent.mm:id/b49")))
        auth_btn.click()
        # 获取到系统授权按钮后点击
        sys_btn = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.ID, "android:id/button1")))
        sys_btn.click()
        # 获取填手机号的位置
        phone = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.ID, "com.tencent.mm:id/m7")))
        phone.send_keys("8572720858")
        # 点击Next
        next_btn = WebDriverWait(self.driver,5).until(EC.element_to_be_clickable((By.ID, "com.tencent.mm:id/b2f")))
        next_btn.click()
        # 选择短信验证码
        sms_btn = WebDriverWait(self.driver,5).until(EC.element_to_be_clickable((By.ID,"com.tencent.mm:id/d16")))
        sms_btn.click()
        # 发送短信验证码
        sms_send_btn = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.ID, "com.tencent.mm:id/dkp")))
        sms_send_btn.click()
        # 手动输入验证码：
        code = input("请输入验证码：")
        # 获取输入验证码元素并输入
        password = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(
            (By.XPATH, '//*[@resource-id="com.tencent.mm:id/d1f"]/android.widget.EditText')))
        password.send_keys(code)
        # 登录
        login = self.wait.until(EC.element_to_be_clickable((By.ID, "com.tencent.mm:id/b2f")))
        login.click()

        # 不重置密码
        back = self.wait.until(EC.presence_of_element_located((By.ID, "com.tencent.mm:id/m1")))
        back.click()

        # 点击去掉通讯录提示框
        # no_btn = self.wait.until(EC.element_to_be_clickable((By.ID, "com.tencent.mm:id/az9")))
        # no_btn.click()
        print('登陆成功...')


    def gettxt(self):
        wholepage = self.wait.until(EC.presence_of_element_located((By.ID, "com.tencent.mm:id/fyd")))
        # 文字+文章
        try:
            text = wholepage.find_element_by_id("com.tencent.mm:id/b8j").text
            return text
        except:
            pass

        # 图片
        try:
            text = wholepage.find_element_by_id("com.tencent.mm:id/fid").text
            return text
        except:
            pass

        return None

    def cmp(self,d1, d2):
        key = d1.keys()
        for item in key:
            if d1[item] != d2[item]:
                return False
            pass
        return True

    def moment_page(self):
        Slip = True
        year = "2020"
        month = "10"
        date = "01"
        dateDict = {"Jan": "01", "Feb": "02", "Mar": "03", "Apr": "04", "May": "05", "Jun": "06",
                    "Jul": "07", "Aug": "08", "Sep": "09", "Oct": "10", "Nov": "11", "Dec": "12", }
        year_2020 = td.date2Timestamp("2020-01-01 00:00:00")
        earliest_time = td.date2Timestamp("2020-10-01 00:00:00")
        ret_data = []

        #一直往下滑，直到需要停止
        while(Slip):
            moments = None
            try:
                moments = self.driver.find_element_by_id('com.tencent.mm:id/b1_')
            except Exception as e:
                Slip = False
                continue
            if moments:
                moments = self.wait.until(EC.presence_of_all_elements_located((By.ID, "com.tencent.mm:id/b1_")))
                pass

            # first = True
            allSame = True
            for moment in moments:
                # if first:
                #     first = False
                #     continue
                #1 尝试获取日期，如果
                #extractDate

                try:
                    mYear = moment.find_element_by_id("com.tencent.mm:id/fm4").text
                    year = str(mYear)
                except:
                    pass

                try:
                    mMonth = moment.find_element_by_id("com.tencent.mm:id/fjf").text
                    month = dateDict[mMonth]
                except:
                    pass

                try:
                    mDate = moment.find_element_by_id("com.tencent.mm:id/fic").text
                    date = str(mDate).zfill(2)
                except:
                    pass

                mTimestamp = td.date2Timestamp("{0}-{1}-{2} 00:00:00".format(year, month, date))
                print("{0}-{1}-{2}".format(year, month, date))

                if mTimestamp < year_2020:
                    Slip = False
                    continue

                if mTimestamp<=earliest_time:
                    earliest_time = mTimestamp
                else:
                    continue

                puretext = False
                imagetext = False
                media = False
                article = False
                articleTitle = "Void"

                # 判断朋友圈类型
                try:
                    puretext = moment.find_element_by_id("com.tencent.mm:id/b8j")
                except:
                    pass
                try:
                    imagetext = moment.find_element_by_id("com.tencent.mm:id/b88")
                except:
                    pass

                try:
                    media = moment.find_element_by_id("com.tencent.mm:id/cn8")
                except:
                    pass
                try:
                    article = moment.find_element_by_id("com.tencent.mm:id/dj7")
                    articleTitle = moment.find_element_by_id("com.tencent.mm:id/g8d").text
                except:
                    pass

                data = {
                    "Date": "{0}-{1}-{2}".format(year, month, date),
                    "Media": 0,
                    "Code": None,
                    "Text": None,
                    "Article": None
                }
                if puretext and article:
                    data["Code"] = 'text + article'
                    data['Article'] = articleTitle
                    try:
                        puretext.click()
                        time.sleep(1)
                        text = self.gettxt()
                        if text:
                            data['Text'] = text.replace("\n"," ")
                            self.driver.back()
                        time.sleep(1)
                    except:
                        data['Code'] = "Error"
                elif imagetext and media:
                    data["Code"] = "text + image"
                    data['Media'] = 1
                    try:
                        imagetext.click()
                        time.sleep(1)
                        text = self.gettxt()
                        if text:
                            data['Text'] = text.replace("\n"," ")
                            self.driver.back()
                        time.sleep(1)
                    except:
                        data['Code'] = "Error"
                elif puretext:
                    data["Code"] = "text"
                    try:
                        puretext.click()
                        time.sleep(1)
                        text = self.gettxt()
                        if text:
                            data['Text'] = text.replace("\n"," ")
                            self.driver.back()
                        time.sleep(1)
                    except:
                        data['Code'] = "Error"
                elif media:
                    data["Code"] = "media"
                    data['Media'] = 1
                elif article:
                    data["Code"] = "article"
                    data['Article'] = articleTitle
                else:
                    data["Code"] = "Error"

                if data['Code']!="Error":
                    isin = False
                    for mm in ret_data:
                        if self.cmp(mm,data)==False:
                            continue
                        else:
                            isin = True
                            break
                        pass
                    if not isin:
                        allSame = False
                        print(data['Text'])
                        ret_data.append(data)
                pass

            if allSame:
                Slip = False
            else:
                self.driver.swipe(self.start_x, self.start_y, self.end_x, self.end_y, 2000)
            time.sleep(1)
        return ret_data


    def personal_page(self):
        wholePage = self.wait.until(EC.presence_of_element_located((By.ID,'com.tencent.mm:id/dmc')))
        try:
            moment_btn = wholePage.find_element_by_id("com.tencent.mm:id/ja")
        except:
            return
        moment_btn = self.wait.until(EC.presence_of_element_located((By.ID,'com.tencent.mm:id/ja')))
        moment_btn.click()
        time.sleep(1)
        ret_data = self.moment_page()
        self.driver.back()
        time.sleep(1)
        return ret_data

    def get_data(self):
        #1 识别尚未打开过的用户
        nameList = os.listdir("Data")
        stopSign = True
        data = []
        while stopSign:
            try:
                # 获取 微信好友名字
                items = self.wait.until(EC.presence_of_all_elements_located((By.ID, 'com.tencent.mm:id/dux')))
                for item in items:
                    fileName = str(item.text).replace("\t"," ") + ".csv"
                    # 将用户名称加入列表
                    if fileName in nameList:
                        continue
                    else:
                        nameList.append(fileName)
                        pass

                    # 点击进入个人页面
                    item.click()
                    time.sleep(1)
                    data = self.personal_page()
                    self.driver.back()
                    time.sleep(1)

                    print(fileName)
                    df = pd.DataFrame(data,columns=['Date',"Media","Code","Text","Article"])
                    df.to_csv("Data/{0}".format(fileName))
                # 滑动
                self.driver.swipe(self.start_x, self.start_y, self.end_x, self.end_y, 2000)
            except Exception as e:
                # df = pd.DataFrame(data, columns=['Date', "Media", "Code", "Text", "Article"])
                # df.to_csv("Data/{0}.csv".format(item.text))
                print(e)
                pass

if __name__ == '__main__':
    wc_moment = Wechat_Moment()
    wc_moment.get_data()