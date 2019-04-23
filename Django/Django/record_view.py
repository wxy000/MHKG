# -*- coding: utf-8 -*-
import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render

# noinspection PyUnresolvedReferences
from users.models import UserProfile

# noinspection PyUnresolvedReferences
from toolkit.mongodb_operation.mongodb_chatlog import mongo_chatlog

# noinspection PyUnresolvedReferences
from toolkit.mongodb_operation.mongodb_doctor import mongo


@login_required
def record(request):
    mongo_dc = mongo()
    mongo_cl = mongo_chatlog()
    collist = mongo_cl.getAllCollection()
    chatlist = list()
    for cl in collist:
        temp = {}
        for c in cl[8:].split('_'):
            if c.startswith('YS'):
                dclist = mongo_dc.getDoctorInfo({'doctorId': str(c)})
                if len(dclist) == 0:
                    temp['doctorId'] = '###'
                    temp['doctorname'] = '###'
                    temp['doctorheader'] = '/static/images/default.gif'
                else:
                    temp['doctorId'] = dclist[0]['doctorId']
                    temp['doctorname'] = dclist[0]['doctorname']
                    temp['doctorheader'] = dclist[0]['doctorheader']
            else:
                user1 = User.objects.filter(Q(id__exact=c))
                user2 = UserProfile.objects.all()
                temp['userId'] = '###'
                temp['username'] = '###'
                temp['userheader'] = '/static/images/default.gif'
                for u1 in user1:
                    if not u1.is_superuser:
                        for u2 in user2:
                            if u1.id == u2.user_id:
                                temp['userId'] = c
                                temp['username'] = u1.username
                                temp['userheader'] = u2.image
        chatlist.append(temp)
    # print(chatlist)
    return render(request, 'admin_views/record.html', {'chatlist': chatlist})
