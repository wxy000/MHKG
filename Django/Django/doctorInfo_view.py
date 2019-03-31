# -*- coding: utf-8 -*-

import json
import os
import random
import time

from django.http import HttpResponse
from django.shortcuts import render

# noinspection PyUnresolvedReferences
from toolkit.mongodb_operation.mongodb_doctor import mongo


def doctorInfo(request):
    doctorId = request.GET.get('doctorId', '')
    if doctorId == '':
        return render(request, 'doctor/login1.html')
    else:
        find = mongo()
        info = find.getDoctorInfo({'doctorId': doctorId})
        return render(request, 'doctor/doctorInfo.html', {'doctorInfo': info[0]})


def updateDoctorInfo(request):
    find = mongo()
    data = json.loads(request.body.decode())
    query = data['doctorId']
    data.pop('doctorId')
    data.pop('file')
    num = find.uploadById(query, data)
    if num >= 1:
        result = {"code": 0, "msg": "信息修改成功"}
    else:
        result = {'code': 500, 'msg': "发生错误，请稍后再试"}
    return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json,charset=utf-8")


def uploadPass(request):
    doctorId = request.GET.get('doctorId', '')
    if doctorId == '':
        return render(request, 'doctor/login1.html')
    else:
        return render(request, 'doctor/uploadPass.html', {'doctorId': doctorId})


def uploadPassword(request):
    find = mongo()
    data = json.loads(request.body.decode())
    query = data['doctorId']
    if query == '' or query is None or query == 'None' or query is False:
        result = {'code': 0, 'msg': "请先登录"}
    else:
        info = find.getDoctorInfo({'doctorId': query})
        if len(info) == 0:
            result = {'code': 0, 'msg': "用户不存在"}
        else:
            if info[0]['doctorpassword'] != data['oldPassword']:
                result = {'code': 200, 'msg': "原密码错误，请重新输入"}
            else:
                num = find.uploadById(query, {'doctorpassword': data['password']})
                if num >= 1:
                    result = {"code": 0, "msg": "密码修改成功"}
                else:
                    result = {'code': 500, 'msg': "发生错误，请稍后再试"}
    return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json,charset=utf-8")


def logout(request):
    return render(request, 'doctor/login1.html')
