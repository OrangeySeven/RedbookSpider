# -*- coding: utf-8 -*-    
from bs4 import BeautifulSoup
import csv
import requests
import urllib3
import uagent
import uip
from urllib import  request
import json
import re
import time
import random
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url = 'http://www.xiaohongshu.com/wx_mp_api/sns/v1/search/notes?keyword=%E6%9D%AD%E5%B7%9E%E4%BA%B2%E5%AD%90&sort=popularity_descending&page={}&per_page=20&sid=session.1575337084864265889209'

authorization = ''
headers = {
}
html_headers = {            
}

def save(data):
    file_csv = open('redbook.csv', 'w+', encoding = 'utf-8', newline = '')
    writer = csv.writer(file_csv)
    header = ['title', 'text', 'list']
    writer.writerow(header)
    for r in data:
        writer.writerow(r)
    file_csv.close()

def get(page):
    offset = 0
    index = 0
    book_page = 0
    result = []
    for i in range(page):
        offset += 1
        url_ = url.format(offset)
        req = requests.get(url_, headers = headers, verify = False)
        a_json = json.loads(req.text)
        #print(a_json)
        redbook_item ={}
        redvideo_item ={}
        a1_json = a_json['data']['notes']
        #print(a1_json)
        for i in a1_json:
            for x in range(random.randint(30,75),-1,-1):
                mystr = "倒计时" + str(x) + "秒"
                print(mystr,end = "")
                print()
                time.sleep(1)
            if i['type'] == 'normal':
                #redbook_item['title'] = i['title']
                #redbook_item['nickname'] = i['user']['nickname']
                redbook_item['id']  = i['id']
            else:
                continue
            for value in redbook_item.values():
                info = []
                book_page += 1
                book_no = '第%s篇'%(book_page)
                redbook_href = 'https://www.xiaohongshu.com/discovery/item/' + value
                redbook_req = requests.get(redbook_href, headers = html_headers, verify = False)
                redbook_html = redbook_req.text
                bf = BeautifulSoup(redbook_html, 'html.parser')
                title_div = bf.find('div', class_ = 'note-top').get_text()
                text_div = bf.find('div', class_ = 'content').get_text()
                img_div = bf.find('div', class_ = 'small-pic').find_all('div')
               # img_div = bf_div.find('i', class_ = 'img')    
                for pic in img_div:
                    img_href = pic.find('i', class_ = 'img').get('style')[21:-16] + '1080'
                    print(img_href)
                    request.urlretrieve(img_href, 'C:/redbook/%s-%s.jpg' %(book_page,index))
                    index += 1
                    print('第%s页第%s篇第%s张'%(offset, book_page, index))
                info.append(title_div)
                info.append(text_div)
                info.append(book_no)
                result.append(info)
                print(result)
                save(result)



get(10)
