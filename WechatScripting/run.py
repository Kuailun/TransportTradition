# -*- coding: utf-8 -*-
# @File       : run.py
# @Author     : Yuchen Chai
# @Date       : 2020/4/13 10:58
# @Description:


from appium import webdriver
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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


    def find_xiaoshuaib(self):
        # Discover
        discover_btn = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.ID, "com.tencent.mm:id/tb")))
        discover_btn.click()
        # Moment
        moment_btn = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.ID, "com.tencent.mm:id/aoi")))
        moment_btn.click()
        print('进入朋友圈...')

    def get_data(self):
        final_data = []
        while True:
            try:
                # 获取 ListView
                items = self.wait.until(EC.presence_of_all_elements_located((By.ID, 'com.tencent.mm:id/fiw')))
                # 滑动
                self.driver.swipe(self.start_x, self.start_y, self.end_x, self.end_y, 2000)
                #遍历获取每个List数据
                for item in items:
                    try:
                        content_type = ""
                        text = None
                        article = None
                        image = None
                        video = None

                        # 如果获取不到用户名，就进入下一次循环
                        user = item.find_element_by_id('com.tencent.mm:id/e0n').text

                        # 获取文字
                        try:
                            text = item.find_element_by_id("com.tencent.mm:id/b8c").text
                        except:
                            pass

                        # 获取推送
                        try:
                            article = item.find_element_by_id("com.tencent.mm:id/g8d").text
                        except:
                            pass

                        # 获取图片
                        try:
                            image = item.find_element_by_id("com.tencent.mm:id/hx")
                        except:
                            pass

                        # 获取视频
                        try:
                            video = item.find_element_by_id("com.tencent.mm:id/cli")
                        except:
                            pass

                        userData = {
                            "Date":"",
                            "Name": user,
                            "Text":"",
                            "Article":"",
                            "Image": 0,
                            "Video":0
                        }

                        if text:
                            userData["Text"] = text.replace("\n"," ")
                        if article:
                            userData["Article"] = article
                        if image:
                            userData['Image'] = 1
                        if video:
                            userData['Video'] = 1

                        if text or article or image or video:
                            final_data.append(userData)
                    except:
                        pass
                    pass

                df = pd.DataFrame(final_data,columns=["Date","Name","Text","Article","Image","Video"])
                df.to_csv("wechat_moment.csv")
            except:
                pass

if __name__ == '__main__':
    wc_moment = Wechat_Moment()
#    wc_moment.login()
 #   wc_moment.find_xiaoshuaib()
    wc_moment.get_data()