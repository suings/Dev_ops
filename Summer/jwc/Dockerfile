# alpine's default python version is python3
FROM python:alpine 
# author:github/suings
LABEL maintainer="github/suings"
# 更换时区
RUN apk update && apk add tzdata && \ 
    cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && \
    apk del tzdata 
# install python 第三方包 
RUN pip install flask requests pymongo bs4

COPY src /src

EXPOSE 5000
CMD ["python","/src/app.py"]
