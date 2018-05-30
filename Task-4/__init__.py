#!/usr/bin/env python
#-*- coding:utf-8 -*-

"""
@author:Su
@file:__init__.py
@time:2018/05/27 
"""

import re
import requests
from bs4 import BeautifulSoup


url="https://bbs.hupu.com/20415703.html"
content=requests.get(url).text

soup=BeautifulSoup(content,"html.parser")

comments=[]
for i in soup(class_="floor"):

    author = i(class_="author")[0](class_="u")[0].string # 回复者姓名
    quote = i.blockquote # None 或其他  引用某楼的内容

    quoteauthor = None # 回复的谁
    quotefloornum = "0" #回复谁的层数
    if quote:
        quoteauthor = quote(class_="u")[0].string
        quotefloornum = re.search("引用([0-9]*)楼",str(quote.b)).groups()[0]
        # print(quote.)
    floornum=i(class_="floornum")[0].string # 本层数
    msg = re.sub("<[^>]*>","",str(i.td).replace(str(quote),"").replace(str(i.td.small),"").replace("\n","")) # 本楼评论信息,简单处理

    comments.append([author,msg,quoteauthor,quotefloornum])

# utf-8解决编码问题,sig解决BOM问题
with open("comments.csv","w+",encoding="utf-8-sig") as code:
    code.write("author,comments,quoteauthor,quotefloor\n")
    for comment in comments:
        code.write("%s,%s,%s,%s\n"%(comment[0],comment[1],comment[2],comment[3]))