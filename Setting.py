# -*- coding: utf-8 -*-
import time
import json
import pymongo
import urllib3
import requests
import Setting
from urllib import request
from bs4 import BeautifulSoup
from pymongo import MongoClient

client=MongoClient('localhost',27017)
db=client.Redbook

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
#api地址
def header():
    headers = {
    'Accept-Encoding':'gzip, deflate, br',
    'Accept-Language':'zh-cn',
    'Connection':'keep-alive',
    'Device-Fingerprint':,
   # 'Cookie':,
    'Host':'www.xiaohongshu.com',
    'Referer':'https://servicewechat.com/wxffc08ac7df482a27/346/page-frame.html',
    'User-Agent':,
    'Authorization':,
    }
    return headers

def html_header():
    headers = {
    'Accept-Encoding':'gzip, deflate, br',
    'Accept-Language':'zh-cn',
    'Connection':'keep-alive',
    'Device-Fingerprint': ,
    'Cookie':,
    'Host':'www.xiaohongshu.com',
    'User-Agent':,
    'X-Sign':,      
    }
    return headers
# 解析Json数据
def getJsonSession(url):
    ses = requests.session()
    html = ses.get(url, headers = header(), verify = False)
    soup = json.loads(html.text)
    return soup
# 解析HTML页面
def getHtmlSession(url):
    ses = requests.session()
    html = ses.get(url, headers = html_header(), verify = False)
    soup = BeautifulSoup(html.content, 'html.parser')
    return soup



# 获取笔记类型和id
def getBookId(url):    
    normalBook = []
    videoBook = []
    json = getJsonSession(url)
    jsonData = json['data']['notes']
    for data in jsonData:
        if data['type'] == 'normal':
            normalBook.append('https://www.xiaohongshu.com/discovery/item/' + data['id'])
        else:
            videoBook.append('https://www.xiaohongshu.com/discovery/item/' + data['id'])
    return normalBook, videoBook

# 获取标题、文本、图片、视频链接 保存至MongoDB
def getData(bookUrl):
    picUrls = []
    for url in bookUrl[0]:
        time.sleep(5)
        soup = getHtmlSession(url)
        title = soup.find('div', class_ = 'note-top').find('h1', class_ = 'title').get_text()
        text = soup.find('div', class_ = 'content').get_text()
        pics = soup.find('div', class_ = 'small-pic').find_all('div')
        for pic in pics:
           picUrl = pic.find('i', class_ = 'img').get('style')[21:-32]
           picUrls.append(picUrl)
        # 保存到MongoDB
        db.normalDatas.insert_many([{
            'titleData' : title,
            'textData' : text,
            'picData' : picUrls
            }])
    for url in bookUrl[1]:
        soup = getHtmlSession(url)
        videoSrc = soup.find('div', class_ = 'videoframe').find('video').get('src')
        # 保存到MongoDB
        db.videoDatas.insert_many([{
            'videoUrls': videoSrc
            }])

