# _*_ coding: utf-8 _*_
__author__ = 'david'
__date__ = '2018/5/21 21:37'

from django import forms
from captcha.fields import CaptchaField
from .models import UserProfile


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput, min_length=5)


class RegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput, min_length=5)
    # 验证码,参数：错误信息
    captcha = CaptchaField(error_messages={'invalid': '验证码错误啊'})


class ForgetForm(forms.Form):
    email = forms.EmailField(required=True)
    # 验证码,参数：错误信息
    captcha = CaptchaField(error_messages={'invalid': '验证码错误啊'})


class SetpwdForm(forms.Form):
    password = forms.CharField(required=True, widget=forms.PasswordInput, min_length=5)
    password2 = forms.CharField(required=True, widget=forms.PasswordInput, min_length=5)


class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image']


class UserEmailForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['email']

class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['nick_name', 'gender', 'birday', 'address', 'mobile']
