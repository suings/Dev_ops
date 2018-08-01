# docker的使用(debian系)
基于docker-compose的构建位于[jwc](../jwc/)
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

## dockerhub
先于dockerhub注册账户，然后在终端登录`docker login`  
登录以后push就很简单了:
1. 更改tag为username/tag:version格式
1. 推送  

全过程:
```
[root@winserver2012 db3]# docker login
Login with your Docker ID to push and pull images from Docker Hub. If you don't have a Docker ID, head over to https://hub.docker.com to create one.
Username: suing
Password: 
Login Succeeded
[root@winserver2012 db3]# docker images 
REPOSITORY              TAG                 IMAGE ID            CREATED             SIZE
yuol                    0.1                 e68d36db6693        28 hours ago        253 MB
docker.io/python        alpine              0df00792d84c        3 days ago          78.8 MB
docker.io/hello-world   latest              f2a91732366c        8 months ago        1.85 kB
[root@winserver2012 db3]# docker tag yuol:0.3 suing/yuol:0.1
[root@winserver2012 db3]# docker images 
REPOSITORY              TAG                 IMAGE ID            CREATED             SIZE
suing/yuol              0.1                 e68d36db6693        28 hours ago        253 MB
yuol                    0.1                 8834cefac118        28 hours ago        253 MB
docker.io/python        alpine              0df00792d84c        3 days ago          78.8 MB
docker.io/hello-world   latest              f2a91732366c        8 months ago        1.85 kB
[root@winserver2012 db3]# docker push suing/yuol:0.1
The push refers to a repository [docker.io/suing/yuol]
f12a1eed4793: Pushed 
21b2d63db7f2: Pushed 
30dd5a85e9c4: Pushed 
a2b418a2bc3b: Pushed 
992d5560ec09: Pushed 
168cd6ea3ea6: Mounted from library/python 
08f0588bd3d4: Mounted from library/python 
5aff2448ca83: Mounted from library/python 
73046094a9b8: Mounted from library/python 
0.1: digest: sha256:db84d3451b68240e6d0bd28638b2a40358c68cb45edd67b70aa703219dca92ca size: 2207
[root@winserver2012 db3]# 
```
简要过程  
```
docker images
docker tag yuol:0.3 suing/yuol:0.1
docker push suing/yuol:0.1
```
### 问题
push后可以在dockerhub查到image,但是通过`docker search username`不能搜到，以及`docker search username/image:version`也搜不到  
但是直接在另一台电脑`docker pull suing/yuol:0.1`可以拉下来，就是搜索不到，~~还待解决~~已经解决(过几天可以搜索到)
## 测试用访问地址
[http://47.94.130.223:3100](http://47.94.130.223:3100)

## 参考
[Docker — 从入门到实践](https://yeasy.gitbooks.io/docker_practice/)

