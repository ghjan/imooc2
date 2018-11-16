# _*_ coding: utf-8 _*_
from django.db.models import Q

__author__ = 'david'
__date__ = '2018/5/21 23:00'

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model


class CustomBackend(ModelBackend):
    """
    让用户可以用用户名/邮箱/手机号码登录
    setting 里要有对应的配置
    """
    class_user = get_user_model()

    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = self.class_user.objects.get(Q(username=username) | Q(mobile=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None
