# -*- coding: utf-8 -*-
from datetime import datetime
from django.db import models
from organization.models import CourseOrg, Teacher


class Course(models.Model):
    course_org = models.ForeignKey(CourseOrg, verbose_name=u"课程机构", null=True, blank=True)
    name = models.CharField(max_length=50, verbose_name=u"课程名称")
    desc = models.CharField(max_length=300, verbose_name=u"课程描述")
    detail = models.TextField(verbose_name=u"课程详情")
    is_banner = models.BooleanField(default=False, verbose_name=u'是否轮播图')
    degree = models.CharField(choices=(("cj", u"初级"), ("zj", u"中级"), ("gj", u"高级")), max_length=2)
    learn_times = models.IntegerField(default=0, verbose_name=u"学习时长（分钟数）")
    students = models.IntegerField(default=0, verbose_name=u"学习人数")
    fav_num = models.IntegerField(default=0, verbose_name=u"收藏人数")
    click_num = models.IntegerField(default=0, verbose_name=u"点击数")
    image = models.ImageField(upload_to="courses/%Y/%m", verbose_name=u"封面图", null=True, blank=True, max_length=100)
    category = models.CharField(max_length=20, null=True, blank=True, verbose_name=u"课程类别")
    tag = models.CharField(default="", verbose_name=u"课程标签", max_length=10)
    teacher = models.ForeignKey(Teacher, verbose_name=u"课程老师", null=True)
    needknown = models.CharField(max_length=300, verbose_name=u"课程须知", default="")
    canlearn = models.CharField(max_length=300, verbose_name=u"课程学到什么", default="")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"课程"
        verbose_name_plural = verbose_name
        app_label = "courses"

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.__unicode__()

    def get_learn_users(self):
        return self.usercourse_set.all()[:5]


class BannerCourse(Course):
    class Meta:
        verbose_name = u"轮播课程"
        verbose_name_plural = verbose_name
        proxy = True  # 这样不会再生成一张表


# 章节
class Lesson(models.Model):
    course = models.ForeignKey(Course, verbose_name=u"课程")
    name = models.CharField(max_length=100, verbose_name=u"章节名")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"章节"
        verbose_name_plural = verbose_name
        app_label = "courses"

    def __unicode__(self):
        return "{0}({1})".format(self.course, self.name)

    def __str__(self):
        return self.__unicode__()


class Video(models.Model):
    lesson = models.ForeignKey(Lesson, verbose_name=u"章节")
    name = models.CharField(max_length=100, verbose_name=u"视频名")
    url = models.URLField(max_length=200, default="", verbose_name=u"访问地址")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"视频"
        verbose_name_plural = verbose_name
        app_label = "courses"

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.__unicode__()


# 课程资源
class CourseResource(models.Model):
    course = models.ForeignKey(Course, verbose_name=u"课程")
    name = models.CharField(max_length=100, verbose_name=u"名称")
    download = models.FileField(upload_to="course/resources/%Y/%m", verbose_name=u"资源文件", max_length=100)
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"课程资源"
        verbose_name_plural = verbose_name
        app_label = "courses"

    def __unicode__(self):
        return "{0}({1})".format(self.course, self.name)

    def __str__(self):
        return self.__unicode__()
