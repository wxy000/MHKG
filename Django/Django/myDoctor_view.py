# -*- coding: utf-8 -*-
import json
import math
import random

from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

# noinspection PyUnresolvedReferences
from users.models import UserProfile

# noinspection PyUnresolvedReferences
from toolkit.mongodb_operation.mongodb_doctor import mongo


def myDoctor(request):
    userid = request.GET.get('id', '')
    # 取登陆用户的信息
    user = get_object_or_404(User, pk=userid)
    user_profile = get_object_or_404(UserProfile, user=user)
    result = {'username': user.username, 'id': user.id, 'status': "online", 'sign': "每天好心情",
              'avatar': user_profile.image}

    # 取全部医生的信息
    doctors = list()
    tmp = list()
    quiz2 = set()
    find = mongo()
    ds = find.getDoctorInfo({})
    for i in ds:
        if i['isAuditing'] == 1 or i['isAuditing'] == '1':
            temp = {'id': i['doctorId'], 'username': i['doctorname'], 'avatar': i['doctorheader'],
                    'sign': '(' + i['positionalTitle'] + ')擅长' + i['goodAt']}
            tmp.append({'groupname': i['quiz2'], 'id': math.floor(1e6 * random.random()),
                        'list': [temp]})
    for j in tmp:
        if j['groupname'] not in quiz2:
            doctors.append(j)
            quiz2.add(j['groupname'])
        else:
            for k in doctors:
                if k['groupname'] == j['groupname']:
                    k['list'].append(j['list'][0])
    return render(request, 'views/myDoctor.html', {'result': result, 'friends': doctors})
