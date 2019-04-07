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

# noinspection PyUnresolvedReferences
from toolkit.mongodb_operation.mongodb_rate import mongo_rate


@login_required
def getRate(request):
    userid = request.GET.get('userId', '')
    if userid == '':
        result = {'code': 500, 'msg': "请登录"}
    else:
        mongoRate = mongo_rate().getRateById(userid)
        if mongoRate is None:
            myRate = 0
        else:
            myRate = mongoRate['rate']
        result = {'code': 0, 'msg': "", 'id': userid, 'myRate': myRate}
    return render(request, 'views/myRate.html', {'result': result})


@login_required
def setMoney(request):
    money = request.POST.get('money', '0')
    id = request.POST.get('id', '')
    if money == '0' or id == '':
        result = {'code': 500, 'msg': "请输入金额或刷新后再试"}
    else:
        mongoRate = mongo_rate().insertOrUploadById(id, {'rate': int(money) * 10}, '+')
        if mongoRate:
            result = {'code': 0, 'msg': "充值成功"}
        else:
            result = {'code': 500, 'msg': "充值失败，请稍后再试"}
    return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json,charset=utf-8")
