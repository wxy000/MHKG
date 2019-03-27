# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.shortcuts import render

# noinspection PyUnresolvedReferences
from toolkit.mongodb_operation.mongodb_doctor import mongo

# noinspection PyUnresolvedReferences
from users.models import UserProfile


def inquiry(request):
    doctorId = request.GET.get('doctorId', '')
    if doctorId == '':
        return render(request, 'doctor/login1.html')
    else:
        find = mongo()
        temp = {'doctorId': doctorId}
        doctors = find.getDoctorInfo(temp)
        if len(doctors) == 0:
            return render(request, 'doctor/login1.html')
        else:
            friends = list()
            result = doctors[0]
            mine = {'username': result['doctorname'], 'id': result['doctorId'], 'status': "online",
                    'sign': '(' + result['positionalTitle'] + ')擅长' + result['goodAt'],
                    'avatar': result['doctorheader']}

            # 取全部用户的信息
            user1 = User.objects.all()
            user2 = UserProfile.objects.all()
            for i in user1:
                if not i.is_superuser:
                    for j in user2:
                        if i.id == j.user_id:
                            # 图片地址
                            url = j.image

                            temp = {'id': i.id, 'username': i.username, 'avatar': url}
                            friends.append(temp)
            return render(request, 'doctor/inquiry.html',
                          {'result': result, 'mine': mine,
                           'friends': [{'groupname': "患者", 'id': -100000, 'list': friends}]})
