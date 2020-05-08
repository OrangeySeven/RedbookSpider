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
    'Device-Fingerprint': 'WHJMrwNw1k/GlXqZzeuw8+tSQY4MXwq6dZ2nKzuBmvUOQrof1RlMW08Eos7yVvMgVhnYkWA10aq1rj6WzyrssBJh3Fx6nPiKJdCW1tldyDzmauSxIJm5Txg==1487582755342',
   # 'Cookie':'xhsTrackerId=6e0e0a57-717f-4d5e-cd99-613d9a5ca9c4; extra_exp_ids=; xhs_spid.5dde=eff4c944cdbf9565.1568039581.1.1568040423.1568039581.acafa140-1747-4aee-acdc-c58603b59b4f; xhs_spses.5dde=*',
    'Host':'www.xiaohongshu.com',
    'Referer':'https://servicewechat.com/wxffc08ac7df482a27/346/page-frame.html',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat',
    'X-Sign':'X95259a5dad05dac65fe7b3750916b652',
    'Authorization':'50505c06-6584-4278-8b97-e27a905fa996',
    }
    return headers

def html_header():
    headers = {
    'Accept-Encoding':'gzip, deflate, br',
    'Accept-Language':'zh-cn',
    'Connection':'keep-alive',
    'Device-Fingerprint': 'WHJMrwNw1k/GlXqZzeuw8+tSQY4MXwq6dZ2nKzuBmvUOQrof1RlMW08Eos7yVvMgVhnYkWA10aq1rj6WzyrssBJh3Fx6nPiKJdCW1tldyDzmauSxIJm5Txg==1487582755342',
    'Cookie':'xhsTrackerId=19b877cc-5a36-4243-c2aa-044e4fe51696; extra_exp_ids=gif_clt1|ques_clt1; timestamp1=258918568; hasaki=JTVCJTIyTW96aWxsYSUyRjUuMCUyMChXaW5kb3dzJTIwTlQlMjAxMC4wJTNCJTIwV09XNjQpJTIwQXBwbGVXZWJLaXQlMkY1MzcuMzYlMjAoS0hUTUwlMkMlMjBsaWtlJTIwR2Vja28pJTIwQ2hyb21lJTJGODAuMC4zOTg3LjEzMiUyMFNhZmFyaSUyRjUzNy4zNiUyMiUyQyUyMnpoLUNOJTIyJTJDMjQlMkMtNDgwJTJDdHJ1ZSUyQ3RydWUlMkN0cnVlJTJDJTIydW5kZWZpbmVkJTIyJTJDJTIyZnVuY3Rpb24lMjIlMkNudWxsJTJDJTIyV2luMzIlMjIlMkM0JTJDNCUyQ251bGwlMkMlMjJDaHJvbWUlMjBQREYlMjBQbHVnaW4lM0ElM0FQb3J0YWJsZSUyMERvY3VtZW50JTIwRm9ybWF0JTNBJTNBYXBwbGljYXRpb24lMkZ4LWdvb2dsZS1jaHJvbWUtcGRmfnBkZiUzQkNocm9tZSUyMFBERiUyMFZpZXdlciUzQSUzQSUzQSUzQWFwcGxpY2F0aW9uJTJGcGRmfnBkZiUzQk5hdGl2ZSUyMENsaWVudCUzQSUzQSUzQSUzQWFwcGxpY2F0aW9uJTJGeC1uYWNsfiUyQ2FwcGxpY2F0aW9uJTJGeC1wbmFjbH4lMjIlMkMzNDQxOTcwNDc3JTVE; timestamp2=e900d18af4a531aa4437e5cd045b5c24',
    'Host':'www.xiaohongshu.com',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
    'X-Sign':'X97983f0e1bc015c942bd8e7d40502480',        
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

