# _*_ coding: utf-8 _*_
__author__ = 'david'
__date__ = '2018/5/21 23:00'

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model


class EmailAuthBackend(ModelBackend):
    """
    Authenticate using e-mail account.
    """
    class_user = get_user_model()

    def authenticate(self, username=None, password=None):
        try:
            user = self.class_user.objects.get(email=username)
            if user.check_password(password):
                return user
            return None
        except:
            return None

    def get_user(self, user_id):
        try:
            return self.class_user.objects.get(pk=user_id)
        except:
            return None
