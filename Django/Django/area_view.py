# -*- coding: utf-8 -*-
import json

from django.http import HttpResponse
from django.shortcuts import render

# noinspection PyUnresolvedReferences
from toolkit.toolbar1 import Toolbar1
# noinspection PyUnresolvedReferences
from toolkit.mongodb_operation.mongodb_logfile import mongo


def area(request):
    return render(request, 'admin_views/area.html')


def getMapData(request):
    day = request.GET.get('day', '')
    if day == '':
        result = {'code': 500, 'msg': "请求错误"}
    elif day == '0':
        toolbar1 = Toolbar1()
        result = toolbar1.getData('area')
    else:
        m = mongo()
        temp = m.log_data(int(day))
        citytemp = set()
        # 每个城市的ip数量
        citynum = list()
        # 每个城市的经纬度
        cityaddress = dict()
        for item in temp:
            if item['city'] in citytemp and (str(item['city']) + item['ip']) not in citytemp:
                for city in citynum:
                    if city['name'] == item['city']:
                        city['value'] += 1
                        citytemp.add(str(item['city']) + item['ip'])
            elif item['city'] not in citytemp:
                citynum.append({'name': item['city'], 'value': 1})
                cityaddress[item['city']] = [float(item['longitude']), float(item['latitude'])]
                citytemp.add(item['city'])
                citytemp.add(str(item['city']) + item['ip'])
        result = {'citynum': citynum, 'cityaddress': cityaddress}
    return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json,charset=utf-8")
