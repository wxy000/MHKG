# -*- coding: utf-8 -*-
import json
import math
import random
import time

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

# noinspection PyUnresolvedReferences
from users.models import UserProfile

# noinspection PyUnresolvedReferences
from toolkit.mongodb_operation.mongodb_doctor import mongo

# noinspection PyUnresolvedReferences
from toolkit.mongodb_operation.mongodb_qiuzhu import mongo_qiuzhu

# noinspection PyUnresolvedReferences
from toolkit.mongodb_operation.mongodb_answerQiuzhu import mongo_answer_qiuzhu


@login_required
def myDoctor(request):
    userid = request.GET.get('id', '')
    # 取登陆用户的信息
    user = get_object_or_404(User, pk=userid)
    user_profile = get_object_or_404(UserProfile, user=user)
    result = {'username': user.username, 'id': user.id, 'status': "online", 'sign': "每天好心情",
              'avatar': user_profile.image}

    # 取全部医生的信息
    doctors = list()
    alldoctors = list()
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
            alldoctors.append(i)
    for j in tmp:
        if j['groupname'] not in quiz2:
            doctors.append(j)
            quiz2.add(j['groupname'])
        else:
            for k in doctors:
                if k['groupname'] == j['groupname']:
                    k['list'].append(j['list'][0])
    allQiuzhu = mongo_qiuzhu().getQiuzhuByQuery({'userId': int(userid)})
    for aq in allQiuzhu:
        if len(aq['content']) > 9:
            aq['content'] = aq['content'][0:9] + '...'
    return render(request, 'views/myDoctor.html', {'result': result, 'friends': doctors,
                                                   'alldoctors': alldoctors, 'allQiuzhu': allQiuzhu})


def makeQiuzhuId():
    find = mongo_qiuzhu()
    fn = time.strftime('%y%m%d')
    xx = find.getMaxId('qz' + fn)
    if len(xx) == 0:
        return 'qz' + fn + '00000'
    else:
        return 'qz' + str(int(xx[0]['qiuzhuId'][2:]) + 1)


@login_required
def setHelper(request):
    text = request.POST.get('textarea', '')
    if text == "":
        result = {'code': 500, 'msg': "求助内容不能为空"}
    else:
        find = mongo_qiuzhu()
        data = {'userId': request.user.id, 'qiuzhuId': makeQiuzhuId(), 'content': text,
                'createTime': str(time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time())))}
        if find.insertQiuzhu(data):
            result = {'code': 0, 'msg': "求助已发布"}
        else:
            result = {'code': 500, 'msg': "发布求助失败"}
    return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json,charset=utf-8")


@login_required
def getQiuzhu(request):
    qiuzhuId = request.GET.get('qiuzhuId', '')
    if qiuzhuId == '':
        result = {'code': 500, 'msg': "请正确选择"}
    else:
        get_qiuzhu_title = mongo_qiuzhu().getQiuzhuByQuery({'qiuzhuId': qiuzhuId})
        if len(get_qiuzhu_title) == 0:
            result = {'code': 500, 'msg': "该条求助不存在"}
        else:
            allAnswerQiuzhu = list()
            allAnswerList = mongo_answer_qiuzhu().getAnswerQiuzhuByQuery({'qiuzhuId': qiuzhuId})
            find = mongo()
            for asl in allAnswerList:
                doctors = find.getDoctorInfo({'doctorId': asl['doctorId']})
                if len(doctors) > 0:
                    asl['doctorname'] = doctors[0]['doctorname']
                    asl['doctorheader'] = doctors[0]['doctorheader']
                    allAnswerQiuzhu.append(asl)
            result = {'code': 0, 'msg': "", 'qiuzhuTitle': get_qiuzhu_title[0]['content'],
                      'allAnswerQiuzhu': allAnswerQiuzhu}
    return render(request, 'doctor/qiuzhu.html', {'result': result})
