# 暑期主作业
主要分为两块  
- 运行flask  
- 另一块检查订阅用户，每天2次从教务处更新信息，有更新则通过邮件推送给用户  
## 目录结构
- [app.py](app.py) flask主文件  
- [config.py](config.py) 配置(不完全)  
- [api.py](api.py) 包含获取用户信息`get_info()`，为用户添加订阅标记`mailupdate()`(这个的函数名称没想到合适的)，发送邮件`sendmail()`等函数
- [remind.py](remind.py)
- [static/](static/) 静态文件目录
- [templates/index.html](templates/index.html) 登录页面 
- [templates/info.html](templates/info.html) 信息展示页面
- [templates/remind.html](templates/remind.html) 订阅页面

## flask


## 成绩推送