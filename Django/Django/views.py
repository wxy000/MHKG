# -*- coding: utf-8 -*-
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User

from django.views.decorators.csrf import csrf_exempt
# noinspection PyUnresolvedReferences
from users.models import UserProfile


# @login_required
def index(request):
    userid = request.get_signed_cookie('userId', '', salt="salt")
    if userid == '' or userid is None:
        auth.logout(request)
        return render(request, 'index.html')
    else:
        user = get_object_or_404(User, pk=userid)
        user_profile = get_object_or_404(UserProfile, user=user)
        return render(request, 'index.html', {'user': user, 'user_profile': user_profile})


def searchCondition(request):
    return render(request, 'admin_views/searchCondition.html')


# def pages(request, p):
#     return render(request, 'views/' + p + '.html')


# @csrf_exempt
# def page_not_found(request):
#     return render(request, 'abnormal/404.html')
#
#
# @csrf_exempt
# def page_error(request):
#     return render(request, 'abnormal/500.html')
#
#
# @csrf_exempt
# def permission_denied(request):
#     return render(request, 'abnormal/403.html')
#
#
# @csrf_exempt
# def bad_request(request):
#     return render(request, 'abnormal/400.html')
