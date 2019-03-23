# -*- coding: utf-8 -*-
import json

from django.http import HttpResponse
from django.shortcuts import render

# noinspection PyUnresolvedReferences
from toolkit.mongodb_operation.mongodb_doctor import mongo


def getAllDoctor(request):
    return render(request, 'admin_views/doctorList.html')


def shenhe(request):
    isAuditing = request.GET.get('isAuditing', '')
    return render(request, 'doctor/shenhe.html', {'isAuditing': isAuditing})


def getDoctorInfo(request):
    find = mongo()
    # 获取get请求中的值
    page = int(request.GET.get('page'))
    limit = int(request.GET.get('limit'))
    doctorId = request.GET.get('doctorId', '')
    doctorname = request.GET.get('doctorname', '')
    doctoremail = request.GET.get('doctoremail', '')

    if doctorId == '' and doctorname == '' and doctoremail == '':
        user = find.getDoctorInfo({})
    else:
        query = {'doctorId': {'$regex': '.*' + doctorId + '.*'}, 'doctorname': {'$regex': '.*' + doctorname + '.*'},
                 'doctoremail': {'$regex': '.*' + doctoremail + '.*'}}
        user = find.getDoctorInfo(query)

    data = list()
    for i in user:
        try:
            doctorheader = i['doctorheader']
        except:
            doctorheader = '/static/images/default.gif'
        try:
            phone = i['phone']
        except:
            phone = ''
        try:
            sex = i['sex']
        except:
            sex = '男'
        try:
            date = i['date']
        except:
            date = '1980-01-01'
        try:
            identity = i['identity']
        except:
            identity = ''
        try:
            paper = i['paper']
        except:
            paper = ''
        try:
            quiz1 = i['quiz1']
        except:
            quiz1 = ''
        try:
            quiz2 = i['quiz2']
        except:
            quiz2 = ''

        temp = {'doctorId': i['doctorId'], 'doctorname': i['doctorname'], 'doctorheader': doctorheader,
                'phone': phone, 'doctoremail': i['doctoremail'], 'sex': sex, 'date': date,
                'identity': identity, 'paper': paper, 'quiz1': quiz1, 'quiz2': quiz2,
                'isPerfect': i['isPerfect'], 'isAuditing': i['isAuditing']}
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


def updateAuditing(request):
    find = mongo()
    doctorId = request.GET.get('doctorId', '')
    isAuditing = request.GET.get('isAuditing', '')
    if doctorId == '':
        result = {'code': 500, 'msg': '请选择用户'}
    else:
        query = {'isAuditing': int(isAuditing)}
        num = find.uploadById(doctorId, query)
        if num >= 1:
            result = {'code': 0, 'msg': "状态修改成功"}
        else:
            result = {'code': 500, 'msg': "该用户不存在或其他未知错误"}
    return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json,charset=utf-8")


def delDoctor(request):
    find = mongo()
    doctorId = request.GET.get('doctorId', '')
    num = find.deleteById(doctorId)
    if num >= 1:
        result = {'code': 0, 'msg': '删除成功'}
    else:
        result = {'code': 500, 'msg': "用户不存在"}
    return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json,charset=utf-8")


def batchDelDoctor(request):
    find = mongo()
    ids = request.GET.get('ids', '')
    idList = ids.split(',')
    count = 0
    for i in idList:
        count += find.deleteById(i)
    if count >= 1:
        result = {'code': 0, 'msg': '删除成功'}
    else:
        result = {'code': 500, 'msg': "用户不存在"}
    return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json,charset=utf-8")
