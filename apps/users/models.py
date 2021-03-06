# -*- coding: utf-8 -*-
import os
from datetime import datetime

from django.core import validators
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.deconstruct import deconstructible
from django.utils.translation import ugettext_lazy as _


@deconstructible
class MobileValidator(validators.RegexValidator):
    regex = r'^((13[0-9])|(14[5,7])|(15[0-3,5-9])|(17[0,3,5-8])|(18[0-9])|166|198|199|(147))\d{8}$'
    message = _('Enter a valid mobile number.')


class UserProfile(AbstractUser):
    nick_name = models.CharField(max_length=50, blank=True, default='', verbose_name=u'昵称')
    birday = models.DateField(null=True, blank=True, verbose_name=u"生日")
    gender = models.CharField(choices=(("male", u"男"), ("female", u"女")), default="female", max_length=6)
    address = models.CharField(max_length=100, default="")
    mobile = models.CharField(_('mobile'), max_length=11, unique=True, validators=[MobileValidator()])
    image = models.ImageField(upload_to="image/%Y/%m",
                              default=u"image/default.png", max_length=100, null=True, blank=True)

    class Meta:
        verbose_name = "用户基本信息"
        verbose_name_plural = verbose_name
        # app_label = "users"

    def __unicode__(self):
        return self.username

    def get_unread_nums(self):
        # 获取用户未读消息的数量
        from operation.models import UserMessage
        return UserMessage.objects.filter(user=self.id, has_read=False).count()


class EmailVerifyRecord(models.Model):
    code = models.CharField(max_length=20, verbose_name=u"验证码")
    email = models.EmailField(max_length=50, verbose_name=u"邮箱")
    send_type = models.CharField(choices=(("register", u"注册"), ("forget", u"找回密码"), ('update_email', u'更新邮箱')),
                                 max_length=10,
                                 verbose_name=u"验证码类型")
    send_time = models.DateTimeField(default=datetime.now, verbose_name=u"发送时间")

    class Meta:
        verbose_name = "邮箱验证码"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return "{0}({1})".format(self.code, self.email)

    def __str__(self):
        return self.__unicode__()


class Banner(models.Model):
    title = models.CharField(max_length=100, verbose_name=u"标题")
    image = models.ImageField(upload_to="banner/%Y/%m", verbose_name=u"轮播图", max_length=100, null=True, blank=True)
    url = models.URLField(max_length=200, verbose_name=u"访问地址")
    index = models.IntegerField(default=100, verbose_name=u"顺序")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u"轮播图"
        verbose_name_plural = verbose_name
