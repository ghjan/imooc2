# -*- coding: utf-8 -*-
from django.conf.urls import url
from organization.views import TeachersList, OrgList, OrgHomepageView, OrgDescView, OrgCourseView, \
    OrgTeachersView, AddFavView

urlpatterns = [
    url(r'^teachers/list$', TeachersList.as_view(), name="teachers_list"),
    url(r'^list$', OrgList.as_view(), name="org_list"),
    url(r'^home/(?P<org_id>\d+)$', OrgHomepageView.as_view(), name="org_detail_homepage"),
    url(r'^course/(?P<org_id>\d+)$', OrgCourseView.as_view(), name="org_detail_course"),
    url(r'^desc/(?P<org_id>\d+)$', OrgDescView.as_view(), name="org_detail_desc"),
    url(r'^teacher/(?P<org_id>\d+)$', OrgTeachersView.as_view(), name="org_detail_teachers"),
    url(r'^add_fav$', AddFavView.as_view(), name="add_fav"),
]
