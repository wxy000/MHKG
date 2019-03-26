# -*- coding: utf-8 -*-
import json

from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

# noinspection PyUnresolvedReferences
from users.models import UserProfile

# noinspection PyUnresolvedReferences
from toolkit.mongodb_operation.mongodb_doctor import mongo


def myDoctor(request):
    userid = request.GET.get('id', '')
    doctors = list()
    # 取登陆用户的信息
    user = get_object_or_404(User, pk=userid)
    user_profile = get_object_or_404(UserProfile, user=user)
    result = {'username': user.username, 'id': user.id, 'status': "online", 'sign': "每天好心情",
              'avatar': user_profile.image}

    # 取全部医生的信息
    find = mongo()
    ds = find.getDoctorInfo({})
    for i in ds:
        if i['isAuditing'] == 1 or i['isAuditing'] == '1':
            temp = {'id': i['doctorId'], 'username': i['doctorname'], 'avatar': i['doctorheader'],
                    'sign': i['positionalTitle']}
            doctors.append(temp)
    return render(request, 'views/myDoctor.html', {'result': result, 'friends': doctors})
