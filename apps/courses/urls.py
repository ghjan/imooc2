# -*- coding: utf-8 -*-
from django.conf.urls import url
from courses.views import CoursesListView, CourseDetailView, CourseVideoView, CourseCommentView, CourseAddComment

urlpatterns = [
    url(r'^list$', CoursesListView.as_view(), name="courses_list"),
    url(r'^detail/(?P<course_id>\d+)$', CourseDetailView.as_view(), name="course_detail"),
    url(r'^video/(?P<course_id>\d+)$', CourseVideoView.as_view(), name="course_video"),
    url(r'^comment/(?P<course_id>\d+)$', CourseCommentView.as_view(), name="course_comment"),
    url(r'^add_comment$', CourseAddComment.as_view(), name="add_comment"),

]
