# -*- coding: utf-8 -*-
from datetime import datetime
from django.db import models
from users.models import UserProfile
from courses.models import Course


class UserAsk(models.Model):
    name = models.CharField(max_length=20, verbose_name=u"姓名")
    mobile = models.CharField(max_length=11, verbose_name=u"手机")
    course_name = models.CharField(max_length=20, verbose_name=u"课程名")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"用户咨询"
        verbose_name_plural = verbose_name


class CourseComments(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name=u"用户名")
    course = models.ForeignKey(Course, verbose_name=u"课程")
    comments = models.CharField(max_length=200, verbose_name=u'评论')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"用户评论"
        verbose_name_plural = verbose_name


class UserFavorite(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name=u"用户名")
    fav_id = models.IntegerField(default=0, verbose_name=u"收藏id")
    fav_type = models.IntegerField(choices=((1, u"课程"), (2, u"授课机构"), (3, u"讲师")), verbose_name=u"收藏种类")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"用户收藏"
        verbose_name_plural = verbose_name
        unique_together = ('user', 'fav_id', 'fav_type')


# 用户消息，可能发给全员或者某个用户
class UserMessage(models.Model):
    user = models.IntegerField(default=0, verbose_name=u"接收用户")  # 0表示所有用户
    message = models.CharField(max_length=500, verbose_name=u'消息内容')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")
    has_read = models.BooleanField(default=False, verbose_name=u"是否已读")

    class Meta:
        verbose_name = u'用户消息'
        verbose_name_plural = verbose_name


class UserCourse(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name=u"用户名")
    course = models.ForeignKey(Course, verbose_name=u"课程")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"用户课程"
        verbose_name_plural = verbose_name
        unique_together = ('user', 'course')
