# -*- coding: utf-8 -*-

import json
import os
import random
import time

from django.http import HttpResponse
from django.shortcuts import render

# noinspection PyUnresolvedReferences
from toolkit.mongodb_operation.mongodb_doctor import mongo


def login(request):
    return render(request, 'doctor/login1.html')


def register(request):
    return render(request, 'doctor/register1.html')


def makeDoctorId():
    find = mongo()
    fn = time.strftime('%y%m%d')
    xx = find.getMaxId('YS' + fn)
    if len(xx) == 0:
        return 'YS' + fn + '00'
    else:
        return 'YS' + str(int(xx[0]['doctorId'][2:]) + 1)


def getRegister(request):
    doctorId = makeDoctorId()
    find = mongo()
    data = json.loads(request.body.decode())
    data.pop('doctorpassword2')
    data['doctorId'] = doctorId
    # 0表示审核中，1表示审核通过，2表示审核未通过
    data['isAuditing'] = 0
    # 0表示信息未完善，1表示信息已完善
    data['isPerfect'] = 0
    flagemail = find.getNodeByEmail(data['doctoremail'])
    if len(flagemail) == 0:
        if find.insertDoctor(data):
            result = {'code': 0, 'msg': "", 'doctorId': doctorId, 'doctorname': data['doctorname']}
        else:
            result = {'code': 500, 'msg': "注册失败"}
    else:
        result = {'code': 500, 'msg': "该邮箱已注册"}
    return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json,charset=utf-8")


def perfectInfo(request):
    doctorId = request.GET.get('doctorId', '')
    doctorname = request.GET.get('doctorname', '')
    return render(request, 'doctor/perfectInfo.html', {'doctorId': doctorId, 'doctorname': doctorname})


def rename(request, name):
    # 文件扩展名
    ext = os.path.splitext(name)[1]
    # 定义文件名，年月日时分秒随机数
    fn = time.strftime('%Y%m%d%H%M%S')
    fn = fn + '_%d' % random.randint(0, 100)
    # 重写合成文件名
    name = fn + ext
    return name


def upload(request):
    file_obj = request.FILES.get('file')
    file_path = os.path.join('static/images/doctorheader', rename(request, file_obj.name))
    with open(file_path, 'wb') as f:
        for chunk in file_obj.chunks():
            f.write(chunk)
    result = {"code": 0, "msg": "图片上传成功", "data": {"src": "/" + file_path}}
    return HttpResponse(json.dumps(result, ensure_ascii=False))


def uploadpaper(request):
    file_obj = request.FILES.get('file')
    file_path = os.path.join('static/images/paper', rename(request, file_obj.name))
    with open(file_path, 'wb') as f:
        for chunk in file_obj.chunks():
            f.write(chunk)
    result = {"code": 0, "msg": "图片上传成功", "data": {"src": "/" + file_path}}
    return HttpResponse(json.dumps(result, ensure_ascii=False))


def getPerfectInfo(request):
    find = mongo()
    data = json.loads(request.body.decode())
    query = data['doctorId']
    data.pop('doctorId')
    data.pop('doctorname')
    data.pop('file')
    # 0表示信息未完善，1表示信息已完善
    data['isPerfect'] = 1
    num = find.uploadById(query, data)
    if num >= 1:
        result = {"code": 0, "msg": "已通知管理员审核，请您耐心等待"}
    else:
        result = {'code': 500, 'msg': "用户不存在或已经修改过"}
    return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json,charset=utf-8")


def getLogin(request):
    find = mongo()
    data = json.loads(request.body.decode())
    data.pop('code')
    temp = find.login(data)
    if temp is None:
        result = {'code': 500, 'msg': "用户名或密码错误"}
    else:
        if temp['isPerfect'] == 0:
            result = {'code': 200, 'msg': "请完善信息，以便管理员审核", 'doctorId': temp['doctorId'],
                      'doctorname': temp['doctorname']}
        elif temp['isPerfect'] == 1:
            if temp['isAuditing'] == 0:
                result = {'code': 500, 'msg': "管理员正在审核中，请您耐心等待"}
            elif temp['isAuditing'] == 1:
                result = {'code': 0, 'msg': "", 'doctorId': temp['doctorId']}
            elif temp['isAuditing'] == 2:
                result = {'code': 500, 'msg': "您的信息不符合规定，已被驳回"}
    return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json,charset=utf-8")


def index(request):
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
            result = doctors[0]
            return render(request, 'doctor/index.html', {'result': result})
