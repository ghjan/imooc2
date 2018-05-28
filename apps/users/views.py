# -*- coding: utf-8 -*-
import os
import json
from django.shortcuts import render
# 密码 加密
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
from django.views.generic.base import View
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from utils.email_send import send_register_email
from utils.views import LoginRequiredMixin
from .forms import LoginForm, RegisterForm, ForgetForm, SetpwdForm, ImageUploadForm
from .models import UserProfile, EmailVerifyRecord


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
        # render是渲染变量到模板中, 而redirect是HTTP中的1个跳转的函数, 一般会生成302状态码
        return HttpResponseRedirect(reverse("index"))


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


class UsercenterView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'usercenter_info.html', {
        })


class ImageUploadView(LoginRequiredMixin, View):
    def post(self, request):
        image_form = ImageUploadForm(request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():
            request.user.save()
            return HttpResponse(json.dumps({'status': 'success'}), content_type='application/json')
        else:
            return HttpResponse(json.dumps({'status': 'fail'}), content_type='application/json')


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
    """
    重置密码
    """

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


class UpdatepwdView(View):
    """
    用户个人中心修改密码
    """

    def post(self, request):
        setpwd_form = SetpwdForm(request.POST)
        if setpwd_form.is_valid():
            user_profile = request.user
            pass_word = request.POST.get('password', '')
            pass_word2 = request.POST.get('password2', '')
            if pass_word != pass_word2:
                return HttpResponse(json.dumps({"status": "fail", "msg": "密码两次输入不匹配"}),
                                    content_type="application/json")
            # 对密码加密
            user_profile.password = make_password(pass_word)
            user_profile.save()  # 保存到数据库
        else:
            data = {
                "status": "fail", "msg": "",
            }
            data.update(setpwd_form.errors)
            return HttpResponse(json.dumps(data),
                                content_type="application/json")
        return HttpResponse(json.dumps({"status": "success", "msg": ""}),
                            content_type="application/json")


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
