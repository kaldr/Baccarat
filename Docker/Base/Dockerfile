# 这是开发用镜像
FROM docker.iflying.com/ubuntu16.04

# apt-get安装基本工具并且设置语言
RUN apt-get install -y  python3 python3-pip
# 添加阿里云的pip源
ARG PIPSource="[global]\nindex-url = http://mirrors.aliyun.com/pypi/simple/\n[install]\ntrusted-host = mirrors.aliyun.com"
# 安装基本的python工具包
RUN mkdir /root/.pip && mkdir /root/.pip3 && echo $PIPSource > /root/.pip/pip.conf && echo $PIPSource > /root/.pip3/pip.conf && echo $PIPSource > /root/.pip3/pip3.conf && ln -s /usr/bin/python3 /usr/bin/python && ln -s /usr/bin/pip3 /usr/bin/pip && pip install --upgrade pip && pip install pika flower xlwt celery colorama pymongo matplotlib numpy pandas scikit-learn stylus django scipy pymodm moment watchdog asyncio websockets jupyter ipython flask attrdict bunch
# 端口暴露
EXPOSE 8878
EXPOSE 5858
EXPOSE 5888
# 将自动运行程序写入到 /root/autorun.sh 中
ARG programmes="#!/bin/bash\nexport PYTHONPATH=/home/Gamble/source\nmkdir /home/jupyter\n chown jupyter.jupyter /home/jupyter\n mkdir /home/celery\n chown celery.celery /home/celery"
RUN echo $programmes > /root/autorun.sh
# 添加新用户
RUN useradd celery && useradd jupyter && mkdir /home/jupyter && chown jupyter.jupyter /home/jupyter && mkdir /home/celery && chown celery.celery /home/celery && mkdir /var/log/gamble && chmod -R 777 /var/log/gamble
