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
