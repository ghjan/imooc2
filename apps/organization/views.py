# -*- coding: utf-8 -*-

import json
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.base import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from operation.models import UserFavorite
from .models import CityDict, CourseOrg, Teacher


class TeachersList(View):
    def get(self, request):
        all_teachers = Teacher.objects.all()
        hot_teachers = Teacher.objects.order_by("-click_num")[:3]

        sort = request.GET.get("sort", "")
        if sort:
            if sort == "hot":
                all_teachers = all_teachers.order_by('-fav_num')

        try:
            param_page = request.GET.get('page', 1)
        except:
            param_page = 1
        # Provide Paginator with the request object for complete querystring generation
        p = Paginator(all_teachers, 2, request=request)
        teachers = p.page(param_page)
        teacher_nums = len(all_teachers)
        return render(request, 'teachers_list.html', {
            'list_view': 'teachers',
            'all_teachers': teachers,
            'teacher_nums': teacher_nums,
            'sort': sort,
            'hot_teachers': hot_teachers,
        })


class OrgList(View):
    def get(self, request):
        all_orgs = CourseOrg.objects.all()
        hot_orgs = CourseOrg.objects.order_by("-click_num")[:3]
        all_cities = CityDict.objects.all()
        all_ct = dict((("pxjg", "培训机构"), ("gr", "个人"), ("gx", "高校"),))

        city_id = request.GET.get('city', "")
        if city_id:
            all_orgs = all_orgs.filter(city__id=int(city_id))

        ct = request.GET.get('ct', "")
        if ct:
            all_orgs = all_orgs.filter(category=ct)

        sort = request.GET.get("sort", "")
        if sort:
            if sort == "students":
                all_orgs = all_orgs.order_by('-students')
            elif sort == "courses":
                all_orgs = all_orgs.order_by('-course_num')
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        # Provide Paginator with the request object for complete querystring generation
        p = Paginator(all_orgs, 2, request=request)
        orgs = p.page(page)
        org_nums = len(all_orgs)
        return render(request, 'org_list.html', {
            'list_view': 'orgs',
            "all_orgs": orgs,
            "all_cities": all_cities,
            "org_nums": org_nums,
            "city_id": city_id,
            "all_ct": all_ct,
            "ct": ct,
            "hot_orgs": hot_orgs,
            "sort": sort,
        })


class OrgHomepageView(View):
    def get(self, request, org_id):
        try:
            data = {}
            org = CourseOrg.objects.get(id=int(org_id))
            has_fav = True if request.user.is_authenticated() and UserFavorite.objects.filter(user=request.user,
                                                                                              fav_id=int(org_id),
                                                                                              fav_type=int(
                                                                                                  2)) else False
            all_courses = org.course_set.all()
            all_teachers = org.teacher_set.all()
            data.update({
                'has_fav': has_fav,
                'view': "homepage",
                'all_courses': all_courses,
                'all_teachers': all_teachers,
                'org': org,
            })
            return render(request, 'org_detail_homepage.html', data)
        except Exception as e:
            print(e)
            # return render(request, 'org_detail_homepage.html', {})


class OrgCourseView(View):
    def get(self, request, org_id):
        try:
            org = CourseOrg.objects.get(id=int(org_id))
            has_fav = True if request.user.is_authenticated() and UserFavorite.objects.filter(user=request.user,
                                                                                              fav_id=int(org_id),
                                                                                              fav_type=int(
                                                                                                  2)) else False
            all_courses = org.course_set.all()

            courses_nums = len(all_courses)

            return render(request, 'org_detail_course.html', {
                'has_fav': has_fav,
                'view': "course",
                'all_courses': all_courses,
                'courses_nums': courses_nums,
                'org': org,
            })
        except Exception as e:
            print(e)


class OrgDescView(View):
    def get(self, request, org_id):
        try:
            org = CourseOrg.objects.get(id=int(org_id))
            has_fav = True if request.user.is_authenticated() and UserFavorite.objects.filter(user=request.user,
                                                                                              fav_id=int(org_id),
                                                                                              fav_type=int(
                                                                                                  2)) else False
            return render(request, 'org_detail_desc.html', {
                'has_fav': has_fav,
                'view': "desc",
                'org': org,
            })
        except Exception as e:
            print(e)


class TeacherListView(View):
    def get(self, request, org_id):
        try:
            org = CourseOrg.objects.get(id=int(org_id))
            has_fav = True if request.user.is_authenticated() and UserFavorite.objects.filter(user=request.user,
                                                                                              fav_id=int(org_id),
                                                                                              fav_type=int(
                                                                                                  2)) else False
            all_teachers = org.teacher_set.all()
            return render(request, 'org_detail_teachers.html', {
                'has_fav': has_fav,
                'view': "teachers",
                'all_teachers': all_teachers,
                'org': org,
            })
        except Exception as e:
            print(e)


class TeacherDetailView(View):
    def get(self, request, teacher_id):
        hot_teachers = Teacher.objects.order_by("-click_num")[:3]
        data = {'hot_teachers': hot_teachers,}
        try:
            teacher = Teacher.objects.get(id=int(teacher_id))
            if teacher:
                teacher.click_num += 1
                teacher.save()
                data.update({
                    'teacher': teacher,
                })
                if request.user.is_authenticated():
                    has_fav = False
                    try:
                        uf = UserFavorite.objects.get(user=request.user, fav_id=teacher_id, fav_type=3)
                        if uf:
                            has_fav = True
                    except:
                        pass
                    has_fav_org = False
                    try:
                        uf = UserFavorite.objects.get(user=request.user, fav_id=teacher.org.id, fav_type=2)
                        if uf:
                            has_fav_org = True
                    except:
                        pass
                    data.update({
                        'has_fav': has_fav,
                        'has_fav_org': has_fav_org
                    })
                return render(request, 'teacher_detail.html', data)
        except Exception as e:
            print(e)


class AddFavView(View):
    """
    用户收藏/取消收藏
    """

    def post(self, request):
        fav_id = request.POST.get('fav_id')
        fav_type = request.POST.get('fav_type')

        # 判断用户登录状态
        if not request.user.is_authenticated():
            return HttpResponse(json.dumps({'status': 'fail', 'msg': '用户未登录'}), content_type='application/json')

        exist_records = UserFavorite.objects.filter(user=request.user, fav_id=int(fav_id), fav_type=int(fav_type))
        if exist_records:
            # 已经存在，表示取消收藏
            exist_records.delete()
            return HttpResponse(json.dumps({'status': 'success', 'msg': '已取消收藏'}),
                                content_type='application/json')
        else:
            if int(fav_id) > 0 and int(fav_type) > 0:
                user_fav = UserFavorite()
                user_fav.fav_type = fav_type
                user_fav.fav_id = fav_id
                user_fav.user = request.user
                user_fav.save()
                return HttpResponse(json.dumps({'status': 'success', 'msg': '已收藏'}),
                                    content_type='application/json')
            else:
                return HttpResponse(json.dumps({'status': 'fail', 'msg': '收藏出错'}), content_type='application/json')
