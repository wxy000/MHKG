# -*- coding: utf-8 -*-
import datetime
import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render

# noinspection PyUnresolvedReferences
from users.models import UserProfile


@login_required
def getAllUser(request):
    return render(request, 'admin_views/userList.html')


@login_required
def getUserInfo(request):
    # 获取get请求中的值
    page = int(request.GET.get('page'))
    limit = int(request.GET.get('limit'))
    id = request.GET.get('id', '')
    username = request.GET.get('username', '')
    email = request.GET.get('email', '')
    sex = request.GET.get('sex', '')

    if id == '' and username == '' and email == '' and sex == '':
        user1 = User.objects.all()
        user2 = UserProfile.objects.all()
    else:
        user1 = User.objects.filter(Q(id__contains=id) & Q(username__contains=username) & Q(email__contains=email))
        if sex != '':
            user2 = UserProfile.objects.filter(gender__exact=sex)
        else:
            user2 = UserProfile.objects.filter(gender__contains=sex)

    data = list()
    for i in user1:
        if not i.is_superuser:
            for j in user2:
                if i.id == j.user_id:
                    # 图片地址
                    # u1 = j.image
                    # u2 = u1[u1.index('/') + 1:]
                    # url = u2[u2.index('/'):]
                    url = j.image
                    # 性别
                    sex = '女'
                    if j.gender == 'male':
                        sex = '男'

                    temp = {'id': i.id, 'username': i.username, 'avatar': url, 'phone': j.phone,
                            'email': i.email, 'sex': sex,
                            'jointime': datetime.datetime.strftime(i.date_joined, '%Y-%m-%d %H:%M:%S')}
                    data.append(temp)

    # 分页
    data_page = list()
    for d in range((page - 1) * limit, page * limit):
        try:
            data_page.append(data[d])
        except Exception:
            pass
    result = {'code': 0, 'msg': '', 'count': str(len(data)), 'data': data_page}
    return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json,charset=utf-8")


@login_required
def batchdel(request):
    ids = request.GET.get('ids', '#')
    if ids != '#':
        keys = list()
        for key in ids.split(','):
            keys.append(key)
        for k in keys:
            user = User.objects.filter(id=k)
            if len(user) > 0:
                user.delete()
        result = {'code': 0, 'msg': ""}
    else:
        result = {'code': 500, 'msg': "请选择需要删除的用户！"}
    return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json,charset=utf-8")


@login_required
def delById(request):
    id = request.GET.get('id', '#')
    if id != '#':
        user = User.objects.filter(id=id)
        if len(user) > 0:
            user.delete()
            result = {'code': 0, 'msg': ""}
        else:
            result = {'code': 500, 'msg': "用户不存在！"}
    else:
        result = {'code': 500, 'msg': "请选择需要删除的用户！"}
    return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json,charset=utf-8")
