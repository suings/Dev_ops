# docker-compose
使用了docker-compose,将mongodb与flask容器分开。解决上个版本中停止容器时mongodb非正常退出问题，修复时区问题和[api.py](../docker/api.py)中遗留bug

## [Dockerfile](Dockerfile)
Dockerfile可以比作图纸,docker由Dockerfile构建镜像
```
FROM python:alpine 
LABEL maintainer="github/suings"
# 更换时区,内容源自网络
RUN apk update && \
    apk add tzdata && \ 
    cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && \
    apk del tzdata 
# 安装项目必须第三方库
RUN pip install flask requests pymongo bs4

COPY src /src

EXPOSE 5000
CMD ["python","/src/app.py"]
```
## [docker-compose.yml](docker-compose.yml)
docker-compose.yml可以比作docker-compose的图纸，用来构建一个项目，整合多个镜像
```
version: "3"
services:

   db:
     image: mongo
     volumes:
       - ~/dbdata:/data/db
     restart: always
     expose:
      - "27017"
   flask:
     build: .
     depends_on:
       - db
     ports:
       - "3100:5000"
     volumes:
       - ./src:/src
     restart: always
volumes:
    db_data:
```
经由docker-compose连接在一起，flask的镜像中可以与mongodb连通，而两个容器又相对独立