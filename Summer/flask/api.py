#-*- coding:utf-8 -*-

import re
import time
import hashlib
import smtplib
from email.mime.text import MIMEText

from email.header import Header
import traceback
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from config import dbconfig

def get_new_info(user_id,pwd,sleep_time=0):
    '''
    从教务处抓取信息并返回
    :param user_id:学号
    :param pwd:密码
    :param sleep_time:这个参数不用传入，也不用作死传入
    :return:
    '''
    user_id=str(user_id)
    pwd=str(pwd)

    s = requests.session()
    r = s.get("http://221.233.24.23/eams/login.action")
    payload = {
        "username": user_id,
        "password": pwd_sha1(r.text, pwd),
        "encodedPassword": "",
        "session_locale": "zh_CN"
    }
    r = s.post("http://221.233.24.23/eams/login.action", data=payload)
    time.sleep(sleep_time)

    info={}
    info["学号"]=user_id
    info["密码"]=pwd
    info["更新时间"]=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    info["时间戳"]=int(time.time())

    if "请不要过快点击" in r.text:
        sleep_time+=1
        return get_new_info(user_id,pwd,sleep_time)
    if "密码错误" in r.text:
        info["状态"]="密码错误"
        return info
    elif "账户不存在" in r.text:
        info["状态"] = "账户不存在"
        return info
    else:
        info["状态"]="正常"

    # 学籍信息
    r=s.get("http://221.233.24.23/eams/stdDetail.action")
    soup = BeautifulSoup(r.text, "html.parser")
    trs = soup.find_all("tr")
    data = {}
    for tr in trs[1:-1]:
        tds = tr.find_all("td")
        try:
            if tds[1].getText():
                data[tds[0].getText()[:-1]] = tds[1].getText()
            if tds[3].getText():
                data[tds[2].getText()[:-1]] = tds[3].getText()
        except:
            pass
    info["学籍信息"] = data
    # 成绩
    r=s.get("http://221.233.24.23/eams/teach/grade/course/person!historyCourseGrade.action?projectType=MAJOR")
    source = r.text
    soup = BeautifulSoup(source, "html.parser")
    tables = soup(class_="gridtable")
    data = []
    for cjtd in tables[1].find_all("tr")[1:]:
        cj = cjtd.find_all("td")
        if len(cj) == 10:
            d = {
                "学年学期": cj[0].getText().strip(),
                "课程代码": cj[1].getText().strip(),
                "课程序号": cj[2].getText().strip(),
                "课程名称": " ".join(cj[3].getText().split()),
                "课程类别": cj[4].getText().strip(),
                "学分": cj[5].getText().strip(),
                "补考成绩": cj[6].getText().strip(),
                "总评成绩": cj[7].getText().strip(),
                "最终": cj[8].getText().strip(),
                "绩点": cj[9].getText().strip(),
            }
            data.append(d)
        else:
            d = {
                "学年学期": cj[0].getText().strip(),
                "课程代码": cj[1].getText().strip(),
                "课程序号": cj[2].getText().strip(),
                "课程名称": " ".join(cj[3].getText().split()),
                "课程类别": cj[4].getText().strip(),
                "学分": cj[5].getText().strip(),
                "补考成绩": "",
                "总评成绩": cj[6].getText().strip(),
                "最终": cj[7].getText().strip(),
                "绩点": cj[8].getText().strip(),
            }
    info["成绩"] = data

    # 在校汇总
    data = None
    tables = soup(class_="gridtable")
    huizong = tables[0].find_all("tr")[-2].find_all("th")
    data = {
        "必修门数": huizong[1].getText(),
        "总学分": huizong[2].getText(),
        "绩点": huizong[3].getText(),
    }
    info["在校汇总"] = data

    # 学年汇总
    datas = []
    for huizong in tables[0].find_all("tr")[1:-2]:
        huizong = huizong.find_all("td")
        data = {
            "学年度": huizong[0].getText(),
            "学期": huizong[1].getText(),
            "必修门数": huizong[2].getText(),
            "必修总学分": huizong[3].getText(),
            "必修平均绩点": huizong[4].getText(),
        }
        datas.append(data)
    info["学年汇总"] = datas
    return info
def get_info(user_id,pwd):
    '''
    先从数据库获取信息，判断是否过期，不过期则返回，否则重新抓取并更新数据库
    :param user_id: 学号
    :return:该学生的数据库信息
    '''
    user_id=str(user_id)
    client = MongoClient(dbconfig["mongodb"],dbconfig["mondgodb_port"])
    table=client[dbconfig["db"]][dbconfig["table"]]
    info=table.find({"学号":user_id})
    if info.count():
        if time.time()-info[0]["时间戳"] < 3600*24:
            return info[0]
        else:
            info = get_new_info(user_id, pwd)
            if info["状态"]=="正常":
                table.update_one({"学籍信息.学号":user_id},info)
            return info
    else:
        # 数据库中没有该用户信息
        info=get_new_info(user_id,pwd)
        table.insert(info)
        return info
def mailupdate(user_id,mail):
    user_id=str(user_id)
    client = MongoClient(dbconfig["mongodb"], dbconfig["mondgodb_port"])
    table = client[dbconfig["db"]][dbconfig["table"]]
    return table.update({"学籍信息.学号":user_id},{"$set":{"订阅":mail}})
def pwd_sha1(page_login,pwd):
    """
    :param page_login: 登录页源码
    :param pwd:原始密码，str类型
    :return: 加密后的密码
    """
    randsrt=re.search(r"CryptoJS\.SHA1\('([a-zA-Z0-9-]+)'",page_login).group(1)
    sha = hashlib.sha1((randsrt+str(pwd)).encode('utf-8'))
    encrypts = sha.hexdigest()
    return encrypts

def sendmail(email,content,type="html"):
    try:
        message = MIMEText(content, 'html', 'utf-8') # html格式的内容
        message['From'] = Header("长大在线", 'utf-8') # 发件人
        message['To'] = Header(email, 'utf-8') # 收件人
        message['Subject'] = Header("成绩更新提醒", 'utf-8') # 邮件主题
        smtp=smtplib.SMTP()
        smtp.connect("smtpdm.aliyun.com","80")
        # smtp.connect("smtp服务器地址","端口")
        smtp.login("xxx@xxx.com","授权码")
        smtp.sendmail("love@yuca.fun",["1357424862@qq.com"],message.as_string())
        # smtp.sendmail("发件人",[所有收件人的数组],message.as_string())

    except:
        traceback.print_exc()