# -*- coding: utf-8 -*-
# @File       : aliserver.py
# @Author     : Yuchen Chai
# @Date       : 2019/12/27 10:45
# @Description:


from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
client = AcsClient('<accessKeyId>', '<accessSecret>', 'cn-hangzhou')

request = CommonRequest()
request.set_accept_format('json')
request.set_domain('dysmsapi.aliyuncs.com')
request.set_method('POST')
request.set_protocol_type('https') # https | http
request.set_version('2017-05-25')
request.set_action_name('SendSms')

request.add_query_param('RegionId', "cn-hangzhou")
request.add_query_param('PhoneNumbers', "13810293640")
request.add_query_param('SignName', "思享出行")
request.add_query_param('TemplateCode', "SMS_180957233")

response = client.do_action(request)
# python2:  print(response)
print(str(response, encoding = 'utf-8'))
