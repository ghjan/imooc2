# _*_ coding: utf-8 _*_
__author__ = 'david'
__date__ = '2018/5/20 23:39'
import xadmin
from .models import CityDict, CourseOrg, Teacher


class CityDictAdmin(object):
    # 后台列表显示列
    list_display = ['name', 'desc', 'add_time']
    # 后台列表查询条件
    search_fields = ['name', 'desc']
    # 后台列表通过时间查询
    list_filter = ['name', 'desc', 'add_time']
    model_icon = 'fa fa-building'


class CourseOrgAdmin(object):
    # 后台列表显示列
    list_display = ['name', 'desc', 'address', 'city', 'fav_num', 'click_num', 'add_time']
    # 后台列表查询条件
    search_fields = ['name', 'desc', 'address', 'city__name', 'fav_num', 'click_num']
    # 后台列表通过时间查询
    list_filter = ['name', 'desc', 'address', 'city__name', 'fav_num', 'click_num', 'add_time']
    model_icon = 'fa fa-university'


class TeacherAdmin(object):
    # 后台列表显示列
    list_display = ['name', 'org', 'work_years', 'work_company', 'work_position', 'points', 'fav_num', 'click_num',
                    'add_time']
    # 后台列表查询条件
    search_fields = ['name', 'org', 'work_years', 'work_company', 'work_position', 'points', 'fav_num', 'click_num']
    # 后台列表通过时间查询
    list_filter = ['name', 'org', 'work_years', 'work_company', 'work_position', 'points', 'fav_num', 'click_num',
                   'add_time']
    model_icon = 'fas fa-chalkboard-teacher'


xadmin.site.register(CourseOrg, CourseOrgAdmin)
xadmin.site.register(CityDict, CityDictAdmin)
xadmin.site.register(Teacher, TeacherAdmin)
