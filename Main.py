# -*- coding: utf-8 -*-
import os
import time
import json
import pymongo
import urllib3
import requests
import Setting
import urllib.parse
from urllib import request
from bs4 import BeautifulSoup
from pymongo import MongoClient

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


#主程序
def start(startPage, endPage):
    api = 'http://www.xiaohongshu.com/fe_api/burdock/weixin/v2/search/notes?keyword={}&sortBy=general&page={}&pageSize=20&needGifCover=true&sid=session.1575338664880906512653'
    user_input = input('输入需要搜索的关键词: \n')
    keyword = urllib.parse.quote(user_input)
    print('Start!')
    for page in range(startPage, endPage):
        time.sleep(5)
        url = api.format(keyword, page)
        Setting.getData(Setting.getBookId(url))


if __name__ == '__main__':
    client=MongoClient('localhost',27017)
    db=client.Redbook
    start(1,1000)


