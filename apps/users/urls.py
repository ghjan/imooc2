# -*- coding: utf-8 -*-
from django.conf.urls import url
from users.views import LoginView, RegisterView, LogoutView, UsercenterView, ActivateUserView, ForgetpwdView, \
    ResetView, SetpwdView, ImageUploadView, UpdatepwdView

urlpatterns = [
    url(r'^login/$', LoginView.as_view(), name="login"),
    url(r'^logout/$', LogoutView.as_view(), name="logout"),
    url(r'^register/$', RegisterView.as_view(), name="register"),
    url(r'^forgetpwd/$', ForgetpwdView.as_view(), name="forgetpwd"),
    url(r'^activate/(?P<code>\w+)/$', ActivateUserView.as_view()),
    url(r'^reset/(?P<code>\w+)/$', ResetView.as_view(), name="resetpwd"),
    url(r'^setpwd/$', SetpwdView.as_view(), name="setpwd"),  # 重置密码后的设置密码
    url(r'^update/pwd/$', UpdatepwdView.as_view(), name="updatepwd"),  # 用户个人中心修改密码
    url(r'^centerinfo/$', UsercenterView.as_view(), name="usercenterinfo"),
    url(r'^image/upload/$', ImageUploadView.as_view(), name="image_upload"),
]
