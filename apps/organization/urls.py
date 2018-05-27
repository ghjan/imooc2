# -*- coding: utf-8 -*-
from django.conf.urls import url
from organization.views import TeachersList, OrgList, OrgHomepageView, OrgDescView, OrgCourseView, \
    TeacherListView, AddFavView, TeacherDetailView

urlpatterns = [
    url(r'^teacher/list$', TeachersList.as_view(), name="teachers_list"),
    url(r'^org_list$', OrgList.as_view(), name="org_list"),
    url(r'^org_home/(?P<org_id>\d+)$', OrgHomepageView.as_view(), name="org_detail_homepage"),
    url(r'^org_course/(?P<org_id>\d+)$', OrgCourseView.as_view(), name="org_detail_course"),
    url(r'^org_desc/(?P<org_id>\d+)$', OrgDescView.as_view(), name="org_detail_desc"),
    url(r'^teacher/list/(?P<org_id>\d+)$', TeacherListView.as_view(), name="org_teacher_list"),
    url(r'^teacher/detail/(?P<teacher_id>\d+)$', TeacherDetailView.as_view(), name="org_teacher_detail"),
    url(r'^add_fav$', AddFavView.as_view(), name="add_fav"),
]
