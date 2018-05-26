# -*- coding: utf-8 -*-
import os
from django.shortcuts import render
# 密码 加密
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
from django.views.generic.base import View
from .forms import LoginForm, RegisterForm, ForgetForm, SetpwdForm
from .models import UserProfile, EmailVerifyRecord
from utils.email_send import send_register_email


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html', {})

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = request.POST.get('username', "")
            password = request.POST.get('password'"")
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    if user.backend == 'users.authentication.EmailAuthBackend':
                        up = UserProfile.objects.get(email=username)
                    else:
                        up = UserProfile.objects.get(username=username)

                    return render(request, 'index.html',
                                  {'username': username, 'image': up.image.url})
                else:
                    return render(request, 'login.html', {"msg": "用户未激活", "login_form": login_form})
            else:
                return render(request, 'login.html', {"msg": "用户名或者密码错误", "login_form": login_form})
        else:
            return render(request, 'login.html', {"msg": "", "login_form": login_form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return render(request, 'index.html', {'username': '', 'image': ''})


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, "register.html", {'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            email = request.POST.get('email', '')
            if UserProfile.objects.filter(email=email):
                return render(request, "register.html", {'msg': "用户已经存在"})
            pass_word = request.POST.get('password', '')
            user_profile = UserProfile()
            user_profile.username = email
            user_profile.email = email
            user_profile.is_active = False
            # 对密码加密
            user_profile.password = make_password(pass_word)
            user_profile.save()  # 保存到数据库
            # 发送激活email
            send_register_email(email, "register")
            return render(request, "login.html")
        else:
            return render(request, "register.html", {'register_form': register_form})


class UsercenterView(View):
    def get(self, request):
        return render(request, 'usercenter-info.html', {})


class ActivateUserView(View):
    def get(self, request, code):
        try:
            evr = EmailVerifyRecord.objects.get(code=code)
            if evr:
                up = UserProfile.objects.get(email=evr.email)
                up.is_active = True
                up.save()
        except Exception as e:
            print(e)
        return render(request, "login.html")


class ResetView(View):
    def get(self, request, code):
        try:
            evr = EmailVerifyRecord.objects.get(code=code)
            if evr:
                return render(request, "password_reset.html", {"email": evr.email})
            else:
                return render(request, "forgetpwd.html", {"msg": "重置码错误"})
        except Exception as e:
            print(e)
        return render(request, "login.html")


class SetpwdView(View):
    def post(self, request):
        setpwd_form = SetpwdForm(request.POST)
        if setpwd_form.is_valid():
            email = request.POST.get('email', '')
            user_profiles = UserProfile.objects.filter(email=email)
            if not user_profiles:
                return render(request, "forgetpwd.html", {'msg': "邮箱不存在"})
            pass_word = request.POST.get('password', '')
            pass_word2 = request.POST.get('password2', '')
            if pass_word != pass_word2:
                return render(request, "password_reset.html", {"email": email, "msg": "密码两次输入不匹配"})
            for user_profile in user_profiles:
                # 对密码加密
                user_profile.password = make_password(pass_word)
                user_profile.save()  # 保存到数据库
        else:
            email = request.POST.get('email', '')
            return render(request, "password_reset.html", {"email": email, "setpwd_form": setpwd_form})
        return render(request, "login.html")


class ForgetpwdView(View):
    def get(self, request):
        forget_form = ForgetForm()
        return render(request, "forgetpwd.html", {"forget_form": forget_form})

    def post(self, request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get('email', '')
            if not email or not UserProfile.objects.filter(email=email):
                return render(request, "forgetpwd.html", {'msg': "用户不存在"})
            # 发送重置密码mail
            send_register_email(email, "forget")
            return render(request, "send_success.html")
        else:
            return render(request, "forgetpwd.html", {'forget_form': forget_form})
