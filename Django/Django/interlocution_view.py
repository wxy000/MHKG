# -*- coding: utf-8 -*-
import json

from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

# noinspection PyUnresolvedReferences
from users.models import UserProfile

# noinspection PyUnresolvedReferences
from toolkit.mongodb_operation.mongodb_doctor import mongo


def interlocution(request):
    userid = request.GET.get('id', '')
    if userid == '' or userid == 'None':
        result = {'username': "游客", 'id': -1, 'status': "online", 'sign': "每天好心情",
                  'avatar': "../../../static/layuiadmin/style/userhead.gif"}
    else:
        # 取登陆用户的信息
        user = get_object_or_404(User, pk=userid)
        user_profile = get_object_or_404(UserProfile, user=user)
        result = {'username': user.username, 'id': user.id, 'status': "online", 'sign': "每天好心情",
                  'avatar': user_profile.image}

    return render(request, 'views/interlocution.html', {'result': result})


def getDoctor(request):
    doctorId = request.GET.get('doctorId', '')
    if doctorId != '':
        find = mongo()
        ds = find.getDoctorInfo({'doctorId': doctorId})
        if len(ds) >= 1:
            data = {'doctorheader': ds[0]['doctorheader'], 'doctorname': ds[0]['doctorname'],
                    'quiz2': ds[0]['quiz2'], 'positionalTitle': ds[0]['positionalTitle'],
                    'goodAt': "擅长" + ds[0]['goodAt']}
            result = {'code': 0, 'msg': "", 'data': data}
        else:
            result = {'code': 500, 'msg': ""}
    else:
        result = {'code': 500, 'msg': ""}
    return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json,charset=utf-8")
