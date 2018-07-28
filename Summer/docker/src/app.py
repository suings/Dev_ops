#!/usr/bin/env python
#-*- coding:utf-8 -*-

"""
@author:Su
@file:app.py
@time:2018/07/15 
"""
import traceback
import json
from bson import json_util
from flask import Flask,render_template,request,jsonify
import api

app=Flask(__name__)
@app.route("/",methods=["GET"])
def main():
    return render_template("index.html")
@app.route("/info",methods=["POST","get"])
def info():
    if request.method=="GET":
        # 如果是get请求则跳转回主页
        return "<script>window.location.href='/';</script> "
    user=request.form["username"]
    pwd=request.form["password"]
    try:
        content=api.get_info(user,pwd)
    except:
        traceback.print_exc()
        return "阿勒，服务器出现了一个异常，请稍后再试试吧"
    if content["状态"]=="正常":
        return render_template("info.html",content=content)
    elif content["状态"]=="密码错误":
        return "密码错误"
    else:
        return "ugly refuse"

@app.route("/remind",methods=["GET","POST"])
def remind():
    if request.method=="GET":
        return render_template("remind.html")
    elif request.method=="POST":
        user_id=int(request.args.get("user_id"))
        mail=request.form.get("mail")
        result=api.mailupdate(user_id,mail)
        if result:
            content={"status":"ok"}
            content=jsonify(json.dumps(content,default=json_util.default))
            return content
        else:
            content = {"status": "error"}
            content = jsonify(json.dumps(content, default=json_util.default))
            return content
if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5000,debug=True)
