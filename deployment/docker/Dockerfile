FROM python
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /data/www/imooc \
    && mkdir -p /data/media/imooc/static

WORKDIR /data/www/imooc
COPY requirements.txt /data/www/imooc
RUN  pip install -i http://pypi.douban.com/simple/ -r requirements.txt --trusted-host pypi.douban.com
#RUN pip install git+git://github.com/sshwsfc/xadmin.git
WORKDIR /data/www/imooc/

git@github.com:twz915/DjangoUeditor3.git