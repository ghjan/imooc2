# _*_ coding: utf-8 _*_
__author__ = 'david'
__date__ = '2018/5/25 0:13'
from django.shortcuts import render

from django.views.generic.base import View
from organization.models import CourseOrg
from courses.models import Course
from users.models import Banner


class HomepageView(View):
    def get(self, request):
        all_orgs = CourseOrg.objects.all()[:15]
        courses = Course.objects.filter(is_banner=False)[:5]
        banner_courses = Course.objects.filter(is_banner=True)[:3]
        all_banners = Banner.objects.all().order_by('index')
        return render(request, 'index.html', {
            'all_orgs': all_orgs,
            'courses': courses,
            'banner_courses': banner_courses,
            'all_banners': all_banners,
        })
