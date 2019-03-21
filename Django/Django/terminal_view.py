# -*- coding: utf-8 -*-
import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render

# noinspection PyUnresolvedReferences
from toolkit.toolbar1 import Toolbar1
# noinspection PyUnresolvedReferences
from toolkit.mongodb_operation.mongodb_logfile import mongo


@login_required
def getTerminal(request):
    return render(request, 'admin_views/terminal.html')


@login_required
def getTerminalData(request):
    id = request.GET.get('id', '')
    day = request.GET.get('day', '')
    if id == '' or day == '':
        result = {'code': 500, 'msg': "请求错误！"}
    else:
        toolbar1 = Toolbar1()
        m = mongo()
        if id == 'liulanqi':
            if day == '0':
                result = toolbar1.getData('liulanqi')
            else:
                result = m.log_data2(int(day), 'liulanqi')
        elif id == 'xitong':
            if day == '0':
                result = toolbar1.getData('xitong')
            else:
                result = m.log_data2(int(day), 'xitong')
    return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json,charset=utf-8")
