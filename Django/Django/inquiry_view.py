# -*- coding: utf-8 -*-
import json
import time

from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render

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
            bufenQiuzhu = mongo_qiuzhu().getQiuzhuByQuery({})
            for aq in bufenQiuzhu:
                if len(aq['content']) > 13:
                    aq['content'] = aq['content'][0:13] + '...'
            allQiuzhu = mongo_qiuzhu().getQiuzhuByQuery({})
            for aq in allQiuzhu:
                if len(aq['content']) > 10:
                    aq['content'] = aq['content'][0:10] + '...'
            myAnswerQiuzhu = list()
            myAnswerQiuzhuIds = mongo_answer_qiuzhu().getAnswerQiuzhuByQuery({'doctorId': doctorId})
            maqid = set()
            for ii in myAnswerQiuzhuIds:
                maqid.add(ii['qiuzhuId'])
            for jj in maqid:
                tt = mongo_qiuzhu().getQiuzhuByQuery({'qiuzhuId': jj})[0]
                if len(tt['content']) > 30:
                    tt['content'] = tt['content'][0:30] + '...'
                myAnswerQiuzhu.append(tt)
            mongoRate = mongo_rate().getRateById(doctorId)
            if mongoRate is None:
                myRate = 0
            else:
                myRate = mongoRate['rate']
            mongoPingjia = mongo_pingjia().getPingjiaByQuery({'doctorId': doctorId})
            for mpj in mongoPingjia:
                if len(mpj['text']) > 13:
                    mpj['text'] = mpj['text'][0:13] + '...'
            return render(request, 'doctor/inquiry.html',
                          {'result': result, 'mine': mine, 'bufenQiuzhu': bufenQiuzhu[-3:],
                           'allQiuzhu': allQiuzhu, 'myAnswerQiuzhu': myAnswerQiuzhu,
                           'friends': [{'groupname': "患者", 'id': -100000, 'list': friends}],
                           'myRate': myRate, 'myPingjia': mongoPingjia[-2:],
                           'pingjiaNum': len(mongoPingjia)})


def getQiuzhu1(request):
    qiuzhuId = request.GET.get('qiuzhuId', '')
    doctorId = request.GET.get('doctorId', '')
    if qiuzhuId == '' or doctorId == '':
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
                      'qiuzhuId': qiuzhuId, 'doctorId': doctorId, 'allAnswerQiuzhu': allAnswerQiuzhu}
    return render(request, 'doctor/answer_qiuzhu.html', {'result': result})


def makeAnswerQiuzhuId():
    find = mongo_answer_qiuzhu()
    fn = time.strftime('%y%m%d')
    xx = find.getMaxId('asqz' + fn)
    if len(xx) == 0:
        return 'asqz' + fn + '00000'
    else:
        return 'asqz' + str(int(xx[0]['answerQiuzhuId'][4:]) + 1)


def setAnswerQiuzhu(request):
    text = request.POST.get('desc', '')
    doctorId = request.POST.get('doctorId', '')
    qiuzhuId = request.POST.get('qiuzhuId', '')
    if text == "" or doctorId == '' or qiuzhuId == '':
        result = {'code': 500, 'msg': "回复内容不能为空"}
    else:
        find = mongo_answer_qiuzhu()
        data = {'doctorId': doctorId, 'qiuzhuId': qiuzhuId, 'answerQiuzhuId': makeAnswerQiuzhuId(),
                'content': text,
                'createTime': str(time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time())))}
        if find.insertAnswerQiuzhu(data):
            result = {'code': 0, 'msg': "回复已发布"}
        else:
            result = {'code': 500, 'msg': "发布回复失败，请稍后再试"}
    return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json,charset=utf-8")
