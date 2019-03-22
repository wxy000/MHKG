# -*- coding: utf-8 -*-
import json
import os
import random
import time

from django.contrib.sessions.models import Session
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.utils import timezone

from .models import UserProfile
from django.contrib import auth
from .forms import RegistrationForm, LoginForm, UserinfoForm, PwdChangeForm
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required


def register(request):
    if request.method == 'POST':

        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password2']

            # 使用内置User自带create_user方法创建用户，不需要使用save()
            user = User.objects.create_user(username=username, password=password, email=email)

            # 如果直接使用objects.create()方法后不需要使用save()
            user_profile = UserProfile(user=user)
            user_profile.save()

            return HttpResponseRedirect("/accounts/login/")

    else:
        form = RegistrationForm()

    return render(request, 'users/registration.html', {'form': form})


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = auth.authenticate(username=username, password=password)

            if user is not None and user.is_active:
                auth.login(request, user)

                # 同一个用户在另外一个地方登陆时，会将之前该用户的session清除
                session_key = request.session.session_key
                for session in Session.objects.filter(~Q(session_key=session_key), expire_date__gte=timezone.now()):
                    data = session.get_decoded()
                    if data.get('_auth_user_id', None) == str(request.user.id):
                        session.delete()

                # 删除掉所有过期的session
                request.session.clear_expired()

                response = HttpResponseRedirect(reverse('index'))
                response.set_signed_cookie('userId', user.id, max_age=3600, salt="salt")
                # 关闭浏览器，删除session
                request.session.set_expiry(0)
                return response
                # return render(request, 'index.html?id=' + str(user.id))

            else:
                # 登陆失败
                return render(request, 'users/login.html', {'form': form, 'message': '密码错误，请重试！'})
    else:
        form = LoginForm()

    return render(request, 'users/login.html', {'form': form})


@login_required
def userinfo(request, pk):
    user = get_object_or_404(User, pk=pk)
    user_profile = get_object_or_404(UserProfile, user=user)

    if request.method == "POST":
        form = UserinfoForm(request.POST)

        if form.is_valid():
            user.username = form.cleaned_data['username']
            user.email = form.cleaned_data['email']
            user.save()

            user_profile.gender = form.cleaned_data['gender']
            user_profile.phone = form.cleaned_data['phone']
            user_profile.image = form.cleaned_data['image']
            user_profile.save()

            return HttpResponseRedirect(reverse('users:userinfo', args=[user.id]))
    else:
        default_data = {'username': user.username, 'email': user.email,
                        'gender': user_profile.gender, 'phone': user_profile.phone,
                        'image': user_profile.image}
        form = UserinfoForm(default_data)

    return render(request, 'users/userinfo.html', {'form': form, 'user': user})


@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/accounts/login/")


@login_required
def pwd_change(request, pk):
    user = get_object_or_404(User, pk=pk)

    if request.method == "POST":
        form = PwdChangeForm(request.POST)

        if form.is_valid():

            password = form.cleaned_data['old_password']
            username = user.username

            user = auth.authenticate(username=username, password=password)

            if user is not None and user.is_active:
                new_password = form.cleaned_data['password2']
                user.set_password(new_password)
                user.save()
                return HttpResponseRedirect(reverse('users:login'))

            else:
                return render(request, 'users/pwd_change.html',
                              {'form': form, 'user': user, 'message': '原密码错误，请重试！'})
    else:
        form = PwdChangeForm()

    return render(request, 'users/pwd_change.html', {'form': form, 'user': user})


def rename(request, name):
    # 文件扩展名
    ext = os.path.splitext(name)[1]
    # 定义文件名，年月日时分秒随机数
    fn = time.strftime('%Y%m%d%H%M%S')
    fn = fn + '_%d' % random.randint(0, 100)
    # 重写合成文件名
    name = fn + ext
    return name


@login_required
def upload(request):
    file_obj = request.FILES.get('file')
    file_path = os.path.join('static/images', rename(request, file_obj.name))
    with open(file_path, 'wb') as f:
        for chunk in file_obj.chunks():
            f.write(chunk)
    result = {"code": 0, "msg": "图片上传成功", "data": {"src": "/" + file_path}}
    return HttpResponse(json.dumps(result, ensure_ascii=False))


@login_required
def edit_userinfo(request):
    id = request.GET.get('id', '')
    if id == '':
        return render(request, 'users/edit_userinfo.html', {'flag': 1, 'code': 0})
    else:
        id_filter = User.objects.filter(id=id)
        profile_filter = UserProfile.objects.filter(user_id=id)
        if len(id_filter) == 1:
            temp = {'id': id_filter[0].id, 'username': id_filter[0].username, 'phone': profile_filter[0].phone,
                    'email': id_filter[0].email, 'sex': profile_filter[0].gender}
            print(temp)
            return render(request, 'users/edit_userinfo.html', {'data': temp, 'flag': 0, 'code': 0})
        else:
            return render(request, 'users/edit_userinfo.html', {'code': 500, 'msg': "用户不存在！"})


@login_required
def adduser(request):
    username = request.GET.get('username', '')
    password = request.GET.get('password', '')
    phone = request.GET.get('phone', '')
    email = request.GET.get('email', '')
    sex = request.GET.get('sex', '')
    if username != '' and password != '' and phone != '' and email != '' and sex != '':
        username_filter = User.objects.filter(username__exact=username)
        email_filter = User.objects.filter(email__exact=email)
        if len(username_filter) > 0:
            result = {'code': 500, 'msg': "用户名已存在！"}
        elif len(email_filter) > 0:
            result = {'code': 500, 'msg': "该邮箱已注册！"}
        elif len(username) < 3 or len(username) > 50:
            result = {'code': 500, 'msg': "用户名长度3~50"}
        elif len(password) < 6:
            result = {'code': 500, 'msg': "密码不得小于6位！"}
        else:
            user = User.objects.create_user(username=username, password=password, email=email)

            user_profile = UserProfile(
                user=user,
                gender=sex,
                phone=phone
            )
            user_profile.save()
            result = {'code': 0, 'msg': ""}
    else:
        result = {'code': 500, 'msg': "请将信息填写完整！"}
    return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json,charset=utf-8")


@login_required
def updateuser(request):
    id = request.GET.get('id', '')
    username = request.GET.get('username', '')
    phone = request.GET.get('phone', '')
    email = request.GET.get('email', '')
    sex = request.GET.get('sex', '')
    if id == '':
        result = {'code': 500, 'msg': "请选择一个用户！"}
    elif id != '' and username != '' and phone != '' and email != '' and sex != '':
        id_filter = User.objects.filter(id=id)
        if len(id_filter) > 0:
            email_filter = User.objects.filter(email__exact=email)
            if email != id_filter[0].email:
                if len(email_filter) > 0:
                    result = {'code': 500, 'msg': "该邮箱已注册！"}
                else:
                    id_filter.update(email=email)
                    UserProfile.objects.filter(user_id=id).update(phone=phone)
                    UserProfile.objects.filter(user_id=id).update(gender=sex)
                    result = {'code': 0, 'msg': ""}
            else:
                UserProfile.objects.filter(user_id=id).update(phone=phone)
                UserProfile.objects.filter(user_id=id).update(gender=sex)
                result = {'code': 0, 'msg': ""}
        else:
            result = {'code': 500, 'msg': "用户不存在！"}

    else:
        result = {'code': 500, 'msg': "请将信息填写完整！"}
    return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json,charset=utf-8")
