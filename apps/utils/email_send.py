# _*_ coding: utf-8 _*_
__author__ = 'david'
__date__ = '2018/5/22 15:39'
import random
import datetime
import string
from users.models import EmailVerifyRecord
from django.core.mail import send_mail
from django.conf import settings


def send_register_email(email, send_type="register"):
    email_record = EmailVerifyRecord()
    code = generate_random_str(16 if send_type != "update_email" else 4)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()

    if send_type == "register":
        email_title = "慕雪在线网注册激活链接"
        email_body = "请点击下列链接激活你的账号：http://www.davidzhang.xin:8000/activate/{0}".format(code)
        send_status = send_mail(email_title, email_body, settings.EMAIL_FROM, [email])
        if send_status:
            pass
    elif send_type == "forget":
        email_title = "慕雪在线网密码重置链接"
        email_body = "请点击下列链接密码重置：http://www.davidzhang.xin:8000/reset/{0}".format(code)
        send_status = send_mail(email_title, email_body, settings.EMAIL_FROM, [email])
        if send_status:
            pass
    elif send_type == "update_email":
        email_title = "慕雪在线网修改邮箱验证码链接"
        email_body = "你的邮箱验证码为：{0}".format(code)
        send_status = send_mail(email_title, email_body, settings.EMAIL_FROM, [email])
        if send_status:
            pass


def generate_random_str(count=5):
    chr_num = ''
    random.seed(str(datetime.datetime.now()))
    for i in range(count):
        str_num = str(random.choice(string.ascii_lowercase + string.digits))
        chr_num += str_num
    return chr_num
