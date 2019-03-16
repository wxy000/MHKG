# -*- coding: utf-8 -*-
import json

import psutil
from django.http import HttpResponse
from django.shortcuts import render

# noinspection PyUnresolvedReferences
from toolkit.mongodb_operation.mongodb_logfile import mongo
# noinspection PyUnresolvedReferences
from toolkit.toolbar import Toolbar


def general(request):
    toolbar = Toolbar()
    m = mongo()
    week_data = m.log_data(7)

    pv = len(week_data)
    if pv == 0:
        pv = 1
    u = set()
    sum_bytes = 0
    sum_code = 0
    for i in week_data:
        u.add(i['ip'])
        sum_bytes += int(i['bodyBytesSent'])
        if i['status'] == '200':
            sum_code += 1
    byte = toolbar.filesize(sum_bytes)
    uv = len(u)
    code_ratio = str(round((sum_code / pv) * 100, 2)) + '%'
    item = toolbar.openfile()
    result = {'pv': pv, 'pv_now': item['pv_now'], 'uv': uv, 'uv_now': item['uv_now'],
              'byte': byte, 'byte_now': item['byte_now'], 'code_ratio': code_ratio,
              'code_ratio_now': item['code_ratio_now']}
    return render(request, 'admin_views/general.html', {'result': result})


def getCpuAndMemory(request):
    cpu = psutil.cpu_percent(None)
    memory = psutil.virtual_memory().percent
    result = {'cpu': cpu, 'memory': memory}
    return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json,charset=utf-8")
