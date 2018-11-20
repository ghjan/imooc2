# -*- coding: utf-8 -*-
import os
import json

from django.db.models import Q
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
# 密码 加密
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
from django.views.generic.base import View
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response

from utils.util import FAV_CLASSES, FAV_TEMPLATES
from utils.email_send import send_register_email
from utils.views import LoginRequiredMixin
from operation.models import UserCourse, UserFavorite, UserMessage
from .forms import LoginForm, RegisterForm, ForgetForm, SetpwdForm, ImageUploadForm, UserEmailForm, UserInfoForm
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
                    # up = UserProfile.objects.get(Q(username=username) | Q(mobile=username) | Q(email=username))
                    return HttpResponseRedirect(reverse('index'))
                    # return render(request, 'index.html',
                    #               {'username': username, 'image': up.image.url})
                else:
                    return render(request, 'login.html', {"msg": "用户未激活", "login_form": login_form})
            else:
                return render(request, 'login.html', {"msg": "用户名或者密码错误", "login_form": login_form})
        else:
            return render(request, 'login.html', {"msg": "", "login_form": login_form})


# sql注入演示
class LoginUnsafeView(View):
    def get(self, request):
        return render(request, 'login.html', {})

    def post(self, request):
        username = request.POST.get('username', "")
        password = request.POST.get('password'"")
        # 不再使用django的 orm，因为已经做了sql注入防护
        import pymysql
        conn = pymysql.connect(host='127.0.0.1', user='root', password='123456', db='imooc', charset='utf-8')
        cursor = conn.cursor()
        sql_select = "select * from users_userprofile where email={0} and password={1}".format(username, password)
        result = cursor.execute(sql_select)
        for row in cursor.fetchall():
            # 查询到了用户
            pass


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

            # welcome message
            user_message = UserMessage()
            user_message.user = user_profile.id
            user_message.message = "欢迎到慕课网"
            user_message.save()
            # 发送激活email
            send_register_email(email, "register")
            return render(request, "login.html")
        else:
            return render(request, "register.html", {'register_form': register_form})


class UsercenterView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'usercenter_info.html', {
        })

    def post(self, request):
        user_form = UserInfoForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            return HttpResponse(json.dumps({'status': 'success'}), content_type='application/json')
        else:
            data = {'status': 'fail', 'msg': u'保存失败'}
            data.update(user_form.errors)
            return HttpResponse(json.dumps(data), content_type='application/json')


class MyCourseView(LoginRequiredMixin, View):
    def get(self, request):
        user_courses = UserCourse.objects.only('course').filter(user=request.user)
        courses = []
        if user_courses:
            courses = [uc.course for uc in user_courses]
        return render(request, 'usercenter_mycourse.html', {"courses": courses,
                                                            })


class MyFavView(LoginRequiredMixin, View):
    def get(self, request, fav_type):
        ufs = UserFavorite.objects.filter(user=request.user, fav_type=fav_type)
        data = []
        if ufs:
            ids = [uf.fav_id for uf in ufs]
            class_ = FAV_CLASSES.get(int(fav_type))
            data = class_.objects.filter(id__in=ids)
        template_file = FAV_TEMPLATES.get(int(fav_type)) or 'usercenter_fav_course.html'
        return render(request, template_file, {"data": data, "fav_type": fav_type})


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


class SendEmailCodeView(LoginRequiredMixin, View):
    '''
    发送邮箱验证码
    '''

    def get(self, request):
        email = request.GET.get('email')
        if email:
            if UserProfile.objects.filter(email=email):
                return HttpResponse(json.dumps({'status': 'fail', 'msg': '邮箱已经存在'}),
                                    content_type='application/json')
            send_register_email(email, "update_email")
            return HttpResponse(json.dumps({'status': 'success'}), content_type='application/json')
        return HttpResponse(json.dumps({'status': 'fail', 'msg': '请提供邮箱'}), content_type='application/json')


class UpdateEmailView(View):
    '''
    更新验证码
    '''

    def post(self, request):
        email = request.POST.get('email')
        code = request.POST.get('code')
        if email and code:
            if UserProfile.objects.filter(email=email):
                return HttpResponse(json.dumps({'status': 'fail', 'msg': '你提供的邮箱已经登记过，请重新选择一个邮箱地址'}),
                                    content_type='application/json')
            try:
                evr = EmailVerifyRecord.objects.get(code=code, email=email)
                if not evr:
                    return HttpResponse(json.dumps({'status': 'fail', 'msg': '验证码不合法,请重新核对验证码'}),
                                        content_type='application/json')
                email_form = UserEmailForm(request.POST, instance=request.user)
                if email_form.is_valid():
                    request.user.save()
                    return HttpResponse(json.dumps({'status': 'success'}), content_type='application/json')
                else:
                    data = {
                        "status": "fail",
                    }
                    data.update(email_form.errors)
                    return HttpResponse(json.dumps(data), content_type='application/json')
            except:
                pass
            return HttpResponse(json.dumps({'status': 'fail', 'msg': '更新邮箱失败'}),
                                content_type='application/json')

        else:
            return HttpResponse(json.dumps({'status': 'fail', 'msg': '请提供正确的邮箱和验证码'}), content_type='application/json')


class MyMessageView(LoginRequiredMixin, View):
    def get(self, request):
        all_messages = UserMessage.objects.filter(user=request.user.id)

        paginator = Paginator(all_messages, 3, request=request)
        try:
            page = request.GET.get('page', 1)
        except:
            page = 1
        try:
            messages = paginator.page(page)
            # 已读
            for m in messages.object_list:
                if not m.has_read:
                    m.has_read = True
                    m.save()
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            messages = paginator.page(paginator.num_pages)

        return render(request, "usercenter_message.html", {"all_messages": messages})


def page_not_found(request):
    response = render_to_response('404.html', {})
    response.status_code = 404
    return response


def page_error(request):
    response = render_to_response('500.html', {})
    response.status_code = 500
    return response
