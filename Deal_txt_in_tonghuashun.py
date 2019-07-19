#!/usr/bin/python
# -*- coding:utf8 -*-

import os
import pandas as pd
import jieba
allFileNum = 0


def printPath(level, path):
    global allFileNum
    #打印一个目录下的所有文件夹和文件
    # 所有文件夹，第一个字段是次目录的级别
    dirList = []
    # 所有文件
    fileList = []
    # 返回一个列表，其中包含在目录条目的名称(google翻译)
    files = os.listdir(path)
    # 先添加目录级别
    dirList.append(str(level))
    for f in files:
        if (os.path.isdir(path + '/' + f)):
            # 排除隐藏文件夹。因为隐藏文件夹过多
            if (f[0] == '.'):
                pass
            else:
                # 添加非隐藏文件夹
                dirList.append(f)
        if (os.path.isfile(path + '/' + f)):
            # 添加文件
            fileList.append(f)
            # 当一个标志使用，文件夹列表第一个级别不打印
    i_dl = 0
    for dl in dirList:
        if (i_dl == 0):
            i_dl = i_dl + 1
        else:
            # 打印至控制台，不是第一个的目录
            print('-' * (int(dirList[0])), dl)

            # 打印目录下的所有文件夹和文件，目录级别+1
            printPath((int(dirList[0]) + 1), path + '/' + dl)
    for fl in fileList:
        # 打印文件
        print(fl)

        # 随便计算一下有多少个文件
        allFileNum = allFileNum + 1

def get_filelist(level, path):
    global allFileNum
    # 打印一个目录下的所有文件夹和文件
    # 所有文件夹，第一个字段是次目录的级别
    dirList = []
    # 所有文件
    fileList = []
    # 返回一个列表，其中包含在目录条目的名称(google翻译)
    files = os.listdir(path)
    # 先添加目录级别
    dirList.append(str(level))
    for f in files:
        if (os.path.isdir(path + '/' + f)):
            # 排除隐藏文件夹。因为隐藏文件夹过多
            if (f[0] == '.'):
                pass
            else:
                # 添加非隐藏文件夹
                dirList.append(f)
        if (os.path.isfile(path + '/' + f)):
            # 添加文件
            fileList.append(f)
            # 当一个标志使用，文件夹列表第一个级别不打印
    i_dl = 0
    for dl in dirList:
        if (i_dl == 0):
            i_dl = i_dl + 1
        else:
            # 打印至控制台，不是第一个的目录
            print('-' * (int(dirList[0])), dl)
            # 打印目录下的所有文件夹和文件，目录级别+1
            printPath((int(dirList[0]) + 1), path + '/' + dl)
    return fileList

def deal_text(filelist):
    #生成停用词表
    fl = open("stopwords.txt", encoding='utf-8')
    line = fl.readline()
    stop = []
    while line:
        line = fl.readline().replace(' ', '')
        stop.append(line.replace('\n', ''))
    fl.close()
    #获取所有的文章的标题和内容，并进行分词处理
    title=[]
    text=[]
    times=[]
    for file in filelist:
        path='E:/TheNews/'+str(file)
        title.append(file.replace('.txt',''))
        f = open(path, encoding='utf-8')
        line = f.readline()
        count =1
        finaltext=''
        temptime=''
        while line:
            if count==1:
                temptime=str(line)
                count=2
            else:
                line = f.readline().replace(' ', '')
                finaltext=finaltext+line
        times.append(temptime)
        #分词和去停用词
        seg_list = jieba.cut(finaltext, cut_all=False)
        texts = "/ ".join(seg_list)  # 精确模式
        texts = texts.replace(' ', '')
        textword = texts.split('/')
        Thefinaltext = ''
        for t in textword:
            if t not in stop:
                Thefinaltext = Thefinaltext + t + '/'
        text.append(Thefinaltext)
        f.close()
    print(len(times))
    print(len(title))
    print(len(text))
    textlist={'time':times,'title':title,'text':text}
    return textlist


def out_put(list):
    dataframe = pd.DataFrame({'time':list['time'],'title': list['title'], 'text': list['text']})
    path = 'E:/StockerNewsMerge.xlsx'
    dataframe.to_excel(path)


if __name__ == '__main__':
    #printPath(1, 'C:/Users/li_xm/Desktop/news/stock_news')
    filelist=get_filelist(1, 'E:/TheNews')
    textlist=deal_text(filelist)
    out_put(textlist)
    print(filelist)
    print('总文件数 =', allFileNum)
