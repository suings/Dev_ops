# docker的使用(debian系)


## 安装:  
`uname -r`显示出的版本需要大于3.10  
`wget -qO- https://get.docker.com/ | sh`
## 启动:
    `service docker start`
## 改源(大概就这个意思):
编辑`/etc/docker/daemon.json`文件，没有就新建文件，添加：
```
{
  "registry-mirrors": ["http://hub-mirror.c.163.com"]
}
```
改源时遇到一个问题，直接vim daemon.json然后将数据添加进去后，docker不能启动  
在确定是daemon.json的问题后，百度参照了[Docker daemon 配置和故障排除](https://blog.csdn.net/warrior_0319/article/details/78407172?locationNum=10&fps=1)  
### 解决方法:
先移除原来的daemon.json文件`rm /etc/docker/daemon.json`
然后如下执行命令：
```
tee /etc/docker/daemon.json <<-'EOF'
{
    "registry-mirrors": ["http://hub-mirror.c.163.com"]
}
EOF
```
注意大小写，注意拼写
执行完毕后`service docker start`就可以正常启动了
## hello-world:
运行`docker run hello-world`

## Dockerfile
以YUOL成绩查询系统为例
```
mkdir demo
cd demo
mkdir src
#src中为flask相关的代码
```

[Dockerfile](Dockerfile):
```
# alpine's default python version is python3
FROM python:alpine 
# author:github/suings
LABEL maintainer="github/suings"

# install python 第三方包 
RUN pip install flask requests pymongo bs4

# install mongodb
RUN apk update
RUN apk add mongodb 
RUN mkdir -p /data/db
# copy ./src/ to docker:/src/
COPY src /src/
# 赋予启动脚本执行权限
RUN chmod u+x /src/start.sh

EXPOSE 5000
# 调用启动脚本启动
CMD /src/start.sh
```

Dockerfile的使用：  
`docker build -t yuol:0.1 ./`  
即`docker build -t 自定义的名称:版本 目录`
  
然后启动:  
`docker run -d -p 80:5000 yuol:0.1`  
解释:  
`-d`:后台运行  
`-p 80:5000`将本机80端口与docker容器的5000端口绑定  
`yuol:0.1`使用哪个docker镜像，上面build的是yuol:0.1,所以使用的也是yuol:0.1  
启动以后就可以通过本机ip访问了:

## 测试用访问地址
[http://47.94.130.223:3100](http://47.94.130.223:3100)
