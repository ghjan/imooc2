# _*_ coding: utf-8 _*_
__author__ = 'david'
__date__ = '2018/5/25 0:13'
from django.shortcuts import render

from django.views.generic.base import View
from organization.models import CourseOrg
from courses.models import Course


class HomepageView(View):
    def get(self, request):
        all_orgs = CourseOrg.objects.all()
        all_courses = Course.objects.all()
        return render(request, 'index.html', {
            'list_view': 'home',
            'all_orgs': all_orgs,
            'all_courses': all_courses,
        })
