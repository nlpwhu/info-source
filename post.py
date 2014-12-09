#!/usr/bin/python
#-*-coding:utf-8 -*-

import requests
from config import USERNAME, PASSWORD

LOGON = "http://119.254.102.70:8080/crawler-source/logon.do"
ADD = "http://119.254.102.70:8080/crawler-source/info/add.do"
login_data = {'username':USERNAME,'password':PASSWORD}

class Post:
    def __init__(self):
        # Start a session so we can have persistant cookies
        self.session = requests.session()

    # log onto the site
    def logon(self):
        return self.session.post(LOGON, data=login_data)
        
    # post data
    # data format:
    # data = {'group_name': '其他',
    #         'url': 'http://www.21xc.com/article/ShowClass.asp?ClassID=321',
    #         'level_name': '国内地方',
    #         'regionname': '河南省',
    #         'region': '41',
    #         'level': 5,
    #         'category': '新闻',
    #         'websiteplate': '许昌网_新闻中心_文学',
    #         'website': '许昌网',
    #         'type': 1,
    #         'sourcegroup': -1}

    def post(self, data):
        return self.session.post(ADD, data=data)

