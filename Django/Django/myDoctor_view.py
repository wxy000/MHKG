# -*- coding: utf-8 -*-
import json
import math
import random
import time

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
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

# noinspection PyUnresolvedReferences
from toolkit.mongodb_operation.mongodb_rate import mongo_rate

# noinspection PyUnresolvedReferences
from toolkit.mongodb_operation.mongodb_pingjia import mongo_pingjia

# noinspection PyUnresolvedReferences
from toolkit.mongodb_operation.mongodb_chatlog import mongo_chatlog


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
    fen = request.POST.get('fen', '5')
    mongoRate = mongo_rate().insertOrUploadById(str(request.user.id), {'rate': int(fen)}, '-')
    if mongoRate:
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
    else:
        result = {'code': 500, 'msg': "积分扣除异常，请重新发布求助"}
    return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json,charset=utf-8")


def getAllAnswerQiuzhu(qiuzhuId):
    allAnswerQiuzhu = list()
    allAnswerList = mongo_answer_qiuzhu().getAnswerQiuzhuByQuery({'qiuzhuId': qiuzhuId})
    find = mongo()
    for asl in allAnswerList:
        doctors = find.getDoctorInfo({'doctorId': asl['doctorId']})
        if len(doctors) > 0:
            asl['doctorname'] = doctors[0]['doctorname']
            asl['doctorheader'] = doctors[0]['doctorheader']
            allAnswerQiuzhu.append(asl)
    return allAnswerQiuzhu


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
            allAnswerQiuzhu = getAllAnswerQiuzhu(qiuzhuId)
            result = {'code': 0, 'msg': "", 'qiuzhuTitle': get_qiuzhu_title[0]['content'],
                      'allAnswerQiuzhu': allAnswerQiuzhu, 'qiuzhuId': qiuzhuId}
    return render(request, 'doctor/qiuzhu.html', {'result': result})


@login_required
def getMyRate(request):
    userid = request.GET.get('userId', '')
    fen = request.GET.get('fen', '5')
    if userid == '':
        result = {'code': 500, 'msg': "登陆已过期，请重新登录"}
    else:
        mongoRate = mongo_rate().getRateById(userid)
        if mongoRate is None:
            myRate = 0
        else:
            myRate = mongoRate['rate']
        if myRate < int(fen):
            result = {'code': 200, 'msg': "你的积分为<span style='color: red;'>" + str(myRate) +
                                          "</span>，不足本次支付，请充值"}
        else:
            result = {'code': 0, 'fen': str(fen), 'msg': "你的积分为<span style='color: red;'>" + str(myRate) +
                                                         "</span>，本次求助需花费<span style='color: red;'>" + str(fen) +
                                                         "</span>个积分，是否继续？"}
    return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json,charset=utf-8")


@login_required
def pingjia(request):
    qiuzhuId = request.GET.get('qiuzhuId', '')
    if qiuzhuId == '':
        result = {'code': 500, 'msg': "请正确选择"}
    else:
        get_qiuzhu_title = mongo_qiuzhu().getQiuzhuByQuery({'qiuzhuId': qiuzhuId})
        if len(get_qiuzhu_title) == 0:
            result = {'code': 500, 'msg': "该条求助不存在"}
        else:
            allAnswerQiuzhu = getAllAnswerQiuzhu(qiuzhuId)
            allDoctor = list()
            for aaq in allAnswerQiuzhu:
                allDoctor.append({'doctorId': aaq['doctorId'], 'doctorname': aaq['doctorname']})
            allD = list()
            for ii in allDoctor:
                if ii not in allD:
                    allD.append(ii)
            mongoPingjia = mongo_pingjia().getPingjiaByQuery({'qiuzhuId': qiuzhuId})
            if len(mongoPingjia) == 0:
                result = {'code': 0, 'msg': "", 'allDoctor': allD, 'qiuzhuId': qiuzhuId,
                          'pingjia': mongoPingjia, 'toDoctor': 'null'}
            else:
                find = mongo()
                ds = find.getDoctorInfo({'doctorId': mongoPingjia[0]['doctorId']})
                if len(ds) == 0:
                    dname = 'null'
                else:
                    dname = ds[0]['doctorname']
                result = {'code': 0, 'msg': "", 'allDoctor': allD, 'qiuzhuId': qiuzhuId,
                          'pingjia': mongoPingjia, 'toDoctor': dname}
    return render(request, 'views/pingjia.html', {'result': result})


@login_required
def setPingjia(request):
    doctorId = request.POST.get('doctor', '')
    rate = request.POST.get('rate', '2.5')
    qiuzhuId = request.POST.get('qiuzhuId', '')
    text = request.POST.get('textarea', '')
    if doctorId == '' or rate == '' or qiuzhuId == '' or text == '':
        result = {'code': 500, 'msg': "请填写完整"}
    else:
        mongoPingjia = mongo_pingjia().insert({'doctorId': doctorId, 'rate': rate, 'text': text,
                                               'qiuzhuId': qiuzhuId, 'userId': request.user.id,
                                               'createTime': str(time.strftime('%Y-%m-%d %H:%M',
                                                                               time.localtime(time.time())))})
        if mongoPingjia:
            mongoRate = mongo_rate().insertOrUploadById(doctorId, {'rate': 5}, '+')
            result = {'9code': 0, 'msg': "评价完成"}
        else:
            result = {'code': 500, 'msg': "评价失败，请稍后再试"}
    return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json,charset=utf-8")


def getDoctorAndPingjia(request):
    doctorId = request.GET.get('doctorId', '')
    if doctorId == '':
        result = {'code': 500, 'msg': "请选择用户"}
    else:
        doctor = list()
        find = mongo()
        ds = find.getDoctorInfo({'doctorId': doctorId})
        for i in ds:
            if i['isAuditing'] == 1 or i['isAuditing'] == '1':
                doctor.append(i)
        mongoPingjia = mongo_pingjia().getPingjiaByQuery({'doctorId': doctorId})
        if len(mongoPingjia) <= 0:
            pj_len = 1
        else:
            pj_len = len(mongoPingjia)
        rate_sum = 0
        for pj in mongoPingjia:
            rate_sum += float(pj['rate'])
            user1 = User.objects.filter(Q(id__exact=pj['userId']))
            user2 = UserProfile.objects.all()
            for u1 in user1:
                for u2 in user2:
                    if u1.id == u2.user_id:
                        pj['username'] = u1.username
                        pj['userheader'] = u2.image
        if rate_sum == 0:
            rate_avg = 2.5
        else:
            rate_avg = rate_sum / pj_len
        result = {'code': 0, 'msg': "", 'doctorInfo': doctor, 'rate_avg': rate_avg,
                  'allPingjia': mongoPingjia}
    return render(request, 'views/doctorAndPingjia.html', {'result': result})


def getChatLog(request):
    id1 = request.GET.get('id1', '')
    id2 = request.GET.get('id2', '')
    mongo_cl = mongo_chatlog()
    chatList = mongo_cl.getChatLogByQuery(id1, id2)
    if len(chatList) == 0:
        result = {'code': 500, 'msg': "暂无聊天记录"}
    else:
        result = {'code': 0, 'msg': "", 'chatList': chatList}
    return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json,charset=utf-8")
