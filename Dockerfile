FROM ubuntu
RUN sed -i 's#http://archive.ubuntu.com/#http://mirrors.tuna.tsinghua.edu.cn/#' /etc/apt/sources.list;
RUN apt-get update --fix-missing\
    && apt-get install git -y --fix-missing\
    && apt-get install python3 -y --fix-missing\
    && apt-get install python3-pip -y --fix-missing\
    && git clone https://github.com/luorixin/proxyPoolEx \
    && apt-get install redis-server -y --fix-missing
WORKDIR /proxyPoolEx
RUN sed -i "s/bind .*/bind 127.0.0.1/g" /etc/redis/redis.conf \
    && sed -i "s/# requirepass foobared/requirepass 123456/g" /etc/redis/redis.conf \
    && /etc/init.d/redis-server start
RUN pip3 install -r requirements.txt
EXPOSE 5555
CMD ["bash", "-c", "/etc/init.d/redis-server start && python3 run.py"]