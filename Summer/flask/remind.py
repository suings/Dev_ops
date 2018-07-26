#!/usr/bin/env python3
#-*- coding:utf-8 -*-

"""
@author:Su
@file:remind.py
@time:2018/07/26 
"""

import schedule
from pymongo import MongoClient
from config import dbconfig
from api import get_new_info,sendmail

def checkupdate():
    client = MongoClient(dbconfig["mongodb"], dbconfig["mondgodb_port"])
    table = client[dbconfig["db"]][dbconfig["table"]]
    for info in table.find({"订阅":{"$regex":"[\s\S]*"}}):
        user_id=info["学号"]
        pwd=info["密码"]
        email=info["订阅"]
        print("11")
        new_info=get_new_info(user_id,pwd)
        print(22)
        if info["成绩"] != new_info["成绩"]:
            # 成绩有更新
            # 先构建邮件内容
            content='<style type="text/css">table{text-align: center;border-collapse:collapse;border: 3px solid;}td,th{border-color: pink;border: 1px solid;}</style><table style="text-align: center;"><tr><th>课程名称</th><th>课程时间</th><th>课程类别</th><th>学分</th><th>最终成绩</th><th>绩点</th></tr>'
            base="<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td></td>"
            for cj in info["成绩"]:
                content=content+base.format(cj["课程名称"],cj["学年学期"],cj["课程类别"],cj["学分"],cj["总评成绩"],cj["绩点"])
            content=content+"</table>"
            print(content)
            sendmail(email,content)

def mail():
    schedule.every().day.at("05:00").do(checkupdate)
    schedule.every().day.at("17:00").do(checkupdate)
    while 1:
        schedule.run_pending()
if __name__ == '__main__':
    mail()
