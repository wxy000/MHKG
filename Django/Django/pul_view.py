# -*- coding: utf-8 -*-
import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render

# noinspection PyUnresolvedReferences
from toolkit.toolbar import Toolbar
# noinspection PyUnresolvedReferences
from toolkit.mongodb_operation.mongodb_logfile import mongo


@login_required
def pul(request):
    return render(request, 'admin_views/pul.html')


@login_required
def getPulData(request):
    toolbar = Toolbar()
    m = mongo()
    id = request.GET.get('id', '')
    day = request.GET.get('day', '')
    if id == '' or day == '':
        result = {'code': 500, 'msg': "请求错误！"}
    else:
        if id == 'pvuv':
            if day == '0':
                result = toolbar.openfile_pul()
            else:
                result = m.log_data1(int(day))
        elif id == 'flux':
            if day == '0':
                result = toolbar.openfile_pul()
            else:
                result = m.log_data1(int(day))
    return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json,charset=utf-8")
