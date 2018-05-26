# -*- coding: utf-8 -*-
import json
from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponse
from .models import UserAsk
from .forms import UserAskForm


class AddUserAskView(View):
    '''
    用户添加我要学习
    '''

    def post(self, request):
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            user_ask = userask_form.save(commit=True)
            return HttpResponse(json.dumps({'status': 'success'}), content_type='application/json')
        else:
            return HttpResponse(json.dumps({'status': 'fail', 'msg': userask_form.errors}),
                                content_type='application/json')
