# -*- coding: utf-8 -*-
import re
from django import forms
from .models import UserAsk, CourseComments, UserFavorite, UserMessage, UserCourse


class UserAskForm(forms.ModelForm):
    class Meta:
        model = UserAsk
        fields = ['name', 'mobile', 'course_name']

    def clean_mobile(self):
        """
        验证手机号码是否合法
        :return:
        """
        mobile = self.cleaned_data['mobile']
        REGEX_MOBILE = "^1[3458]\d{9}$"
        p = re.compile(REGEX_MOBILE)
        if p.match(mobile):
            return mobile
        else:
            raise forms.ValidationError(u"手机号码非法", code="mobile invalid")


class CourseCommentsForm(forms.ModelForm):
    class Meta:
        model = CourseComments
        fields = ['user', 'course', 'comments']


class UserFavoriteForm(forms.ModelForm):
    class Meta:
        model = UserFavorite
        fields = ['user', 'fav_id', 'fav_type']


class UserMessageForm(forms.ModelForm):
    class Meta:
        model = UserMessage
        fields = ['user', 'message', 'has_read']


class UserCourseForm(forms.ModelForm):
    class Meta:
        model = UserCourse
        fields = ['user', 'course', ]
