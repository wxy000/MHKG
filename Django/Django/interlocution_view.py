# -*- coding: utf-8 -*-
import json

from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

# noinspection PyUnresolvedReferences
from users.models import UserProfile


def interlocution(request):
    userid = request.GET.get('id', '')
    friends = list()
    if userid == '' or userid == 'None':
        result = {'username': "游客", 'id': -1, 'status': "online", 'sign': "问一些问题",
                  'avatar': "../../../static/layuiadmin/style/userhead.gif"}
    else:
        # 取登陆用户的信息
        user = get_object_or_404(User, pk=userid)
        user_profile = get_object_or_404(UserProfile, user=user)
        result = {'username': user.username, 'id': user.id, 'status': "online", 'sign': "问一些问题",
                  'avatar': user_profile.image}

        # 取全部用户的信息
        user1 = User.objects.all()
        user2 = UserProfile.objects.all()
        for i in user1:
            if not i.is_superuser and str(i.id) != str(userid):
                for j in user2:
                    if i.id == j.user_id:
                        # 图片地址
                        url = j.image

                        temp = {'id': i.id, 'username': i.username, 'avatar': url}
                        friends.append(temp)
    return render(request, 'views/interlocution.html', {'result': result, 'friends': friends})
