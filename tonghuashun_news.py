#from StockerSpider import url_manager, html_downloader, html_parser, html_output
import re
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import time
from http import cookiejar
from urllib import request, error
from urllib.parse import urlparse


#抓取该网页content
def download(url, retry_count=3, headers=None, proxy=None, data=None):
    if url is None:
        return None
    try:
        req = request.Request(url, headers=headers, data=data)
        cookie = cookiejar.CookieJar()
        cookie_process = request.HTTPCookieProcessor(cookie)
        opener = request.build_opener()
        if proxy:#设置代理，防止禁止访问
            proxies = {urlparse(url).scheme: proxy}
            opener.add_handler(request.ProxyHandler(proxies))
        content = opener.open(req).read()
        #print(content)
    except error.URLError as e:
        print('HtmlDownLoader download error:', e.reason)
        content = None
        if retry_count > 0:
            if hasattr(e, 'code') and 500 <= e.code < 600:
                # 说明是 HTTPError 错误且 HTTP CODE 为 5XX 范围说明是服务器错误，可以尝试再次下载
                return download(url, retry_count - 1, headers, proxy, data)
    return content


#获取该页所有的文章地址url和发布时间
def get_html_url(url,temp):
    header = {
        'Accept': 'application/json, text/plain, */*',#在 JSON RPC 调用时使用
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
        'Cookie': 'aliyungf_tc=AQAAAAdRAVATegoAT+pX0+qNj6mJZeQp; s=ee1654wer9; xq_a_token=584d0cf8d5a5a9809761f2244d8d272bac729ed4; xq_r_token=98f278457fc4e1e5eb0846e36a7296e642b8138a; u=791534754487065; device_id=f917f072df7f6eb12b5889844a1914a2; __utma=1.599491956.1534754491.1534754491.1534754491.1; __utmc=1; __utmz=1.1534754491.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); _ga=GA1.2.599491956.1534754491; _gid=GA1.2.507250158.1534754494; Hm_lvt_1db88642e346389874251b5a1eded6e3=1534754487,1534765774,1534765909,1534765919; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1534766265    '
    }
    #downloader = html_downloader.HtmlDownLoader()
    html_content = download(url, retry_count=2, headers=header, proxy=None, data=None)
    soup = BeautifulSoup(html_content, "html.parser", from_encoding="gbk")
    #print(soup)
    title_node = soup.find_all("span", class_="arc-title")
    #print(title_node)
    urls = []
    times=[]
    #years = '2018'
    for name in title_node:
        texttime = name.get_text()#取文本信息
        #print(texttime)
        Thetime=texttime[len(texttime) - 13:len(texttime) - 1]
        #print(Thetime)
        ti=Thetime[0:2]
        # if ti=='12':
        #     temp='13'
        #years=get_years(ti,temp)
        years='2017'
        Thetime=str(years)+'年'+str(Thetime)
        times.append(Thetime)
        name = str(name)

        soups = BeautifulSoup(name)

        #传入正则表达式作为参数,Beautiful Soup会通过正则表达式的 match() 来匹配内容.
        #传入 href 参数,Beautiful Soup会搜索每个tag的”href”属性
        title = soups.find('a', href=re.compile(r"^http.*?shtml$"))["href"]
        #print(title)#每个文章地址url
        urls.append(title)
    url_time={'time':times,'url':urls}
    return url_time

def get_years(y1,y2):
    if int(y1)<int(y2):
        return '2017'
    else:
        return '2018'


#抓取具体文章的内容
def get_text_content(url):
    header = {
        'Accept': 'application/json, text/plain, */*',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
        'Cookie': 'aliyungf_tc=AQAAAAdRAVATegoAT+pX0+qNj6mJZeQp; s=ee1654wer9; xq_a_token=584d0cf8d5a5a9809761f2244d8d272bac729ed4; xq_r_token=98f278457fc4e1e5eb0846e36a7296e642b8138a; u=791534754487065; device_id=f917f072df7f6eb12b5889844a1914a2; __utma=1.599491956.1534754491.1534754491.1534754491.1; __utmc=1; __utmz=1.1534754491.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); _ga=GA1.2.599491956.1534754491; _gid=GA1.2.507250158.1534754494; Hm_lvt_1db88642e346389874251b5a1eded6e3=1534754487,1534765774,1534765909,1534765919; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1534766265    '
    }
    #downloader = html_downloader.HtmlDownLoader()
    html_content = download(url, retry_count=2, headers=header, proxy=None, data=None)
    Bsoup = BeautifulSoup(html_content, "html.parser", from_encoding="gbk")

    title=Bsoup.find('h2','main-title').get_text()
    text_node = Bsoup.find("div", class_="atc-content")

    texts = str(text_node)
    soup = BeautifulSoup(texts, "html.parser", from_encoding="gbk")
    text = soup.find_all('p',limit=1)   #find_all() 方法搜索当前tag的所有tag子节点,并判断是否符合过滤器的条件,limit限制返回结果数量
    maintext=[]
    print (text)
    for t in text:
        mtext=t.get_text().replace(' ', ' ').split('\u3000\u3000')#每句话用’，’分开
        mtext.pop(0)
        for m in mtext:
            maintext.append(m)
    #main_text=text.get_text().replace(' ', '').split('\u3000\u3000')
    #main_text.pop(0)
    article={'title':title,'text':maintext}
    return article

def out_put_article(main_text,time):
    filename=main_text['title']
   # path='C:/Users/li_xm/Desktop/stocknews/'+str(filename)+'.txt'
    path='E:/TheNews/'+str(filename)+'.txt'
    with open(path, "w", encoding='utf-8') as f_out:
        f_out.write(time + '\n')
        f_out.write(main_text['title']+ '\n')
        for text in main_text['text']:
            f_out.write('       '+text+ '\n')
        # print('输出文章数：'+str(count))
        # count=count+1

#TextRank算法获取关键词
def TextRank(words):
    textword={}
    for t in words:
        list=[]
        textword[t]=list
    #统计每个单词的票
    for i in range(0,len(words)):
        if i>=5 and i<=len(words)-6:
            for j in(i-5,i-1):
                textword[words[j]].append(words[i])
            for j in (i +1, i +5):
                textword[words[j]].append(words[i])
        else:
            p=1
            if i-5<0:
                while i-p>=0:
                    textword[words[i-p]].append(words[i])
                    p=p+1
                for t in range(i+1,i+5):
                    textword[words[t]].append(words[i])
            p=1
            if i+5>len(words)-1:
                while i+p<=len(words)-1:
                    textword[words[i+p]].append(words[i])
                    p=p+1
                for t in range(i-5,i-1):
                    textword[words[t]].append(words[i])

    #统计票数
    tword={}
    for word in words:
        tword[word]=len(textword[word])

    return tword



if __name__ == "__main__":
    rootUrl = "http://stock.10jqka.com.cn/hsdp_list/index_"
    global temp
    temp='0'
    #error=['1','4','6','8','10','13','23','26','30']
    for i in range(439,440):     #抓取页数
         try:
             newurl=rootUrl+str(i)+'.shtml'
             url_time=get_html_url(newurl,temp)
             urls=url_time['url']
             times=url_time['time']
             count=0

             for url in range(1):  #该页所有的文章地址urls
                 try:
                    text_content=get_text_content(urls[1])
                    out_put_article(text_content,times[count])
                    filename = text_content['text']
                    print("aaa\n",TextRank(filename))
                    count=count+1
                 except Exception as e:
                    print(str(e))
             time.sleep(20)
         except Exception as e:
             print(str(i)+str(e))

    # for i in error:
    #     try:
    #         url=rootUrl+str(i)+'.shtml'
    #         urls = get_html_url(url)
    #         for url in urls:
    #             try:
    #                 text_content=get_text_content(url)
    #                 out_put_article(text_content)
    #             except Exception as e:
    #                 print(url)
    #                 print(str(e))
    #     except Exception as e:
    #         print(url)
    #         print(str(e))
    #     time.sleep(20)


    # rurl="http://stock.10jqka.com.cn/hsdp_list/index_1.shtml"
    # url_time = get_html_url(rurl)
    # urls=url_time['url']
    # times=url_time['time']
    # count=0
    # for url in urls:
    #     try:
    #         text_content=get_text_content(url)
    #         out_put_article(text_content,times[count])
    #         count=count+1
    #     except Exception as e:
    #         print(url)
    #         print(str(e))




