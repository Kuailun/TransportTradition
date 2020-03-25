# -*- coding: utf-8 -*-
# @File       : 换组.py
# @Author     : Yuchen Chai
# @Date       : 2020/3/21 11:46
# @Description:

import requests

url = "http://47.94.224.205/server/modules/group/moveUsersToAnotherGroup"

header = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US, en; q=0.8, zh-Hans-CN; q=0.5, zh-Hans; q=0.3",
    "Cookie": "Admin-Token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1aWQiOiIxIn0.mCDZeoHB4JGQVIpI_TT4pdXDZ11L3tyeyzqd1uQ2YUE; UserName=admin; UserId=1; UserUuid=undefined; UserDuty=%E6%8A%80%E6%9C%AF%E5%91%98; UserInfo={%22token%22:%22eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1aWQiOiIxIn0.mCDZeoHB4JGQVIpI_TT4pdXDZ11L3tyeyzqd1uQ2YUE%22%2C%22accountResult%22:{%22id%22:1%2C%22roleId%22:1%2C%22username%22:%22admin%22%2C%22realname%22:%22%E7%AE%A1%E7%90%86%E5%91%98%22%2C%22mobile%22:%2218610055553%22%2C%22telephone%22:null%2C%22address%22:%22%E5%8C%97%E4%BA%AC%E5%B8%82%E6%B5%B7%E6%B7%80%E5%8C%BA%22%2C%22email%22:%223435454@qq.com%22%2C%22photo%22:%22871f2bf118b44bb4bd22a485832cebfa.jpg%22%2C%22duty%22:%22%E6%8A%80%E6%9C%AF%E5%91%98%22%2C%22organizationId%22:2%2C%22totalPoint%22:999860%2C%22point%22:999860%2C%22remark%22:%22%22%2C%22approvalState%22:3%2C%22orderNum%22:1%2C%22isLogout%22:0%2C%22isPublish%22:1%2C%22updateTime%22:%222020-01-14%2013:54:41%22}}",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko Core/1.70.3741.400 QQBrowser/10.5.3863.400",
    "x-access-token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1aWQiOiIxIn0.mCDZeoHB4JGQVIpI_TT4pdXDZ11L3tyeyzqd1uQ2YUE"
}

content = {"groupId":5,"newGroupId":1,"userIdList":[40]}

rep = requests.post(url, headers=header, json=content)
print(1)