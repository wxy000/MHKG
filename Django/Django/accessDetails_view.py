# -*- coding: utf-8 -*-
import json

from django.http import HttpResponse
from django.shortcuts import render

# noinspection PyUnresolvedReferences
from toolkit.mongodb_operation.mongodb_logfile import mongo
# noinspection PyUnresolvedReferences
from toolkit.toolbar1 import Toolbar1


def getAccessDetails(request):
    m = mongo()
    days = m.getSixDay()
    result = {'days': days}
    return render(request, 'admin_views/accessDetails.html', {'result': result})


def getTableData(request):
    day = request.GET.get('day', '')
    page = int(request.GET.get('page'))
    limit = int(request.GET.get('limit'))
    ip = request.GET.get('ip', '')
    address = request.GET.get('address', '')
    starttime = request.GET.get('starttime', '00:00:00')
    endtime = request.GET.get('endtime', '23:59:59')
    if day == '' or page == '' or limit == '':
        result = {'code': 500, 'msg': "请求错误"}
    else:
        toolbar1 = Toolbar1()
        if day == '0':
            temp = toolbar1.getData('table', ip, address, starttime, endtime)
            # 分页
            data_page = list()
            for d in range((page - 1) * limit, page * limit):
                try:
                    data_page.append(temp[d])
                except Exception:
                    pass
            result = {'code': 0, 'msg': '', 'count': str(len(temp)), 'data': data_page}
        else:
            m = mongo()
            temp = m.log_data3(int(day), 'table', ip, address, starttime, endtime)
            # 分页
            data_page = list()
            for d in range((page - 1) * limit, page * limit):
                try:
                    data_page.append(temp[d])
                except Exception:
                    pass
            result = {'code': 0, 'msg': '', 'count': str(len(temp)), 'data': data_page}
    return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json,charset=utf-8")
