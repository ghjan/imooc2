# -*- coding: utf-8 -*-
from django.conf.urls import url
from .views import AddUserAskView

urlpatterns = [
    url(r'^add_ask$', AddUserAskView.as_view(), name="add_ask"),
]
