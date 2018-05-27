# -*- coding: utf-8 -*-
import json
from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponse
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from utils.views import LoginRequiredMixin
from operation.models import UserFavorite, CourseComments, UserCourse
from organization.models import Teacher

from .models import Course, Lesson, Video


class CoursesListView(View):
    def get(self, request):
        keywords = request.GET.get('keywords')
        if not keywords:
            all_courses = Course.objects.all()
        else:
            all_courses = Course.objects.filter(name__contains=keywords)
        hot_courses = Course.objects.order_by("-click_num")[:3]
        sort = request.GET.get("sort", "")
        if sort:
            if sort == "students":
                all_courses = all_courses.order_by('-students')
            elif sort == "hot":
                all_courses = all_courses.order_by('-click_num')

        # paginator = Paginator(all_courses, 3, request=request)
        paginator = Paginator(all_courses, 3, request=request)
        try:
            page = request.GET.get('page', 1)
        except:
            page = 1
        try:
            courses = paginator.page(page)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            courses = paginator.page(paginator.num_pages)

        try:
            return render(request, 'courses_list.html', {
                'list_view': 'courses',
                "all_courses": courses,
                "hot_courses": hot_courses,
                "sort": sort,
            })
        except Exception as e:
            print(e)


class CourseDetailView(View):
    def get(self, request, course_id):
        try:
            course = Course.objects.get(id=course_id)
            if course:
                course.click_num += 1
                course.save()
                tag = course.tag
                related_course = []
                if tag:
                    related_course = Course.objects.exclude(id=course_id).filter(tag=tag)[:1]
                data = {
                    'course': course,
                    'related_course': related_course
                }
                if request.user.is_authenticated():
                    has_fav = False
                    try:
                        uf = UserFavorite.objects.get(user=request.user, fav_id=course_id, fav_type=1)
                        if uf:
                            has_fav = True
                    except:
                        pass
                    has_fav_org = False
                    try:
                        uf = UserFavorite.objects.get(user=request.user, fav_id=course.course_org.id, fav_type=2)
                        if uf:
                            has_fav_org = True
                    except:
                        pass
                    data.update({
                        'has_fav': has_fav,
                        'has_fav_org': has_fav_org
                    })
                return render(request, 'course_detail.html', data)
        except Exception as e:
            print(e)


class CourseVideoView(LoginRequiredMixin, View):
    def get(self, request, course_id):
        try:
            course = Course.objects.get(id=course_id)
            if course:
                Teacher.objects.get(course=course_id)

                user_courses_self = UserCourse.objects.filter(user=request.user, course=course)
                if not user_courses_self:
                    # 如果没有，先保存
                    user_course = UserCourse(user=request.user, course=course)
                    user_course.save()

                # 学过该课程的还学过
                related_courses = _get_related_learn_courses(course_id)

                data = {
                    'course': course,
                    'related_courses': related_courses,
                }
                return render(request, 'course_video.html', data)
        except Exception as e:
            print(e)


def _get_related_learn_courses(course_id):
    '''
    # 学过该课程的还学过
    :param course_id:
    :return:
    '''
    user_courses = UserCourse.objects.filter(course=course_id)
    userids = [uc.user.id for uc in user_courses]
    user_courses2 = UserCourse.objects.filter(user__in=userids).exclude(course=course_id)
    # 取出所有课程id
    courseids = [uc2.course.id for uc2 in user_courses2]
    related_courses = Course.objects.filter(id__in=courseids).order_by("-click_num")[:5]
    return related_courses


class CourseCommentView(LoginRequiredMixin, View):
    def get(self, request, course_id):
        try:
            course = Course.objects.get(id=course_id)
            if course:
                all_comments = CourseComments.objects.filter(course=course_id)
                # 学过该课程的还学过
                related_courses = _get_related_learn_courses(course_id)

                data = {
                    'course': course,
                    'related_courses': related_courses,
                    'all_comments': all_comments,
                }

                return render(request, 'course_comment.html', data)
        except Exception as e:
            print(e)


class CourseAddComment(View):
    def post(self, request):
        if request.user.is_authenticated():
            try:
                course_id = request.POST.get('course_id')
                comments = request.POST.get('comments')
                if course_id and comments:
                    cc = CourseComments()
                    cc.user = request.user
                    cc.course = Course.objects.get(id=course_id)
                    cc.comments = comments
                    cc.save()
                    return HttpResponse(json.dumps({'status': 'success', 'msg': '评论成功'}),
                                        content_type='application/json')
            except:
                pass
            return HttpResponse(json.dumps({'status': 'fail', 'msg': '评论失败'}),
                                content_type='application/json')
        else:
            return HttpResponse(json.dumps({'status': 'fail', 'msg': '用户未登录'}),
                                content_type='application/json')


class VideoPlayView(LoginRequiredMixin, View):
    def get(self, request, video_id):
        try:
            video = Video.objects.get(id=video_id)
            if video:
                course = video.lesson.course
                course_id = course.id
                Teacher.objects.get(course=course_id)

                user_courses_self = UserCourse.objects.filter(user=request.user, course=course)
                if not user_courses_self:
                    # 如果没有，先保存
                    user_course = UserCourse(user=request.user, course=course)
                    user_course.save()

                # 学过该课程的还学过
                related_courses = _get_related_learn_courses(course_id)

                data = {
                    'video': video,
                    'course': course,
                    'related_courses': related_courses,
                }
                return render(request, 'course_play.html', data)
        except Exception as e:
            print(e)
