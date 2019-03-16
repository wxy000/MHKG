# -*- coding: utf-8 -*-
import json

from django.http import HttpResponse
from django.shortcuts import render

# noinspection PyUnresolvedReferences
from toolkit.mongodb_operation.mongodb_logfile import mongo

m = mongo()


def newOld(request):
    days = m.getSixDay()
    result = {'days': days}
    return render(request, 'admin_views/newOld.html', {'result': result})


def getNewOldData(request):
    day = request.GET.get('day', '')
    if day == '':
        result = {'code': 500, 'msg': "请求错误"}
    elif day == '0':
        result = m.log_data4()
    else:
        result = m.log_data5(int(day))
    return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json,charset=utf-8")
