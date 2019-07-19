import re
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from http import cookiejar
from urllib import request, error
from urllib.parse import urlparse
import csv
import os

import requests
from bs4 import BeautifulSoup

i=0

# 获取网站的通用类
def get_html(url):
    try:
        header = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',  # 在 JSON RPC 调用时使用
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
            'Cookie': 'UM_distinctid=16a0b4126b155d-0e8a69464e5e8d-7a1437-13c680-16a0b4126b218c; CNZZDATA1273924096=2122113580-1554966981-https%253A%252F%252Fwww.google.com.hk%252F%7C1554966981; yunsuo_session_verify=a25efe35211e728f487d41ea393749f9; ZDEDebuggerPresent=php,phtml,php3; '
        }

        r = requests.get(url, timeout=30,headers=header)
        r.raise_for_status()

        return r.text
    except:
        print("wrong")


# 下载图片的通用工具类
def get_pic_from_url(url):
    # 从url以二进制的格式下载图片数据
    pic_content = requests.get(url, stream=True).content
    open('filename', 'wb').write(pic_content)


def main(url):
    global i
    html = get_html(url)
    soup = BeautifulSoup(html, 'lxml')
    #print(soup)
    # 获取这个ul大标签的对象
    moves_list = soup.find('ul', attrs={'class': 'tv-list clearfix'});

    # 获取ul下的所有的li标签
    #print(moves_list)
    li_list = moves_list.find_all('li')

    #print(li_list)

    for li in li_list:
        time.sleep(1)
        # 获取图片的连接
        try:
            img_src = li.find('img')['data-src']
            with open('2017/'+str(i) + '.png', 'wb+') as f:
                try:
                    f.write(requests.get(img_src).content)
                except:
                    f.write(requests.get(str('http://www.7hsc.net')+img_src).content)
            i = i + 1
            print(i)
        except:
            pass


if __name__ == '__main__':

    for j in range (1,8):
        url='http://www.7hsc.net/search.php?page='+str(j)+'&searchtype=5&tid=1&area=%E5%A4%A7%E9%99%86&year=2017'

        #url='http://www.7hsc.net/search.php?searchtype=5&tid=1&year=2014&area=%E9%A6%99%E6%B8%AF'

        main(url)
