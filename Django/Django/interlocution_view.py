# -*- coding: utf-8 -*-
import json

from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

import uwsgi

# noinspection PyUnresolvedReferences
from toolkit.aiml.im import im

# noinspection PyUnresolvedReferences
from toolkit.aiml.handle.neo4j import Find

# noinspection PyUnresolvedReferences
from users.models import UserProfile


def interlocution(request):
    userid = request.GET.get('id', '')
    if userid == '' or userid == 'None':
        result = {'username': "游客", 'id': -1, 'status': "online", 'sign': "问一些问题",
                  'avatar': "../../../static/layuiadmin/style/userhead.gif"}
    else:
        user = get_object_or_404(User, pk=userid)
        user_profile = get_object_or_404(UserProfile, user=user)
        result = {'username': user.username, 'id': user.id, 'status': "online", 'sign': "问一些问题",
                  'avatar': user_profile.image}
    return render(request, 'views/interlocution.html', {'result': result})


def getAnswer(request):
    find = Find()
    send = im()
    alice = send.get_alice()
    uwsgi.websocket_handshake()  # 与客户端建立连接 ，在uwsgi2.0中，这个函数不需要参数
    uwsgi.websocket_send(alice.respond('CONNECT SUCCEED'))
    try:
        while True:
            msg = uwsgi.websocket_recv()  # 阻塞，等待客户端发来的消息
            msg = msg.decode()
            data = json.loads(msg)
            content = data['data']['mine']['content']
            if data['data']['to']['id'] == -2:
                robot(find, alice, content)
            else:
                uwsgi.websocket_send(content)
    except Exception as e:
        print("except---" + str(e))


def robot(find, alice, content):
    ucontent = ''
    for char in content:
        if u'\u2E80' <= char <= u'\uFFFDh':
            ucontent += ' ' + char + ' '
        else:
            ucontent += char
    if ucontent.strip() == '':
        uwsgi.websocket_send("不要空格哦")
    else:
        receive = alice.respond(ucontent)
        if receive == '':
            uwsgi.websocket_send("找不到答案face[委屈]，你可以戳戳a(https://www.baidu.com/s?wd=" + ucontent + ")[这里]")

        # 数据库查询
        elif receive[0] == '$':
            # 获取用户输入的变量
            res = receive.split(':')

            # neo4j查询
            if receive.__contains__('neo4j'):
                # 实体
                entity = str(res[1]).replace(" ", "")
                ans = find.matchNodebyTitle(entity)
                if ans is None:
                    uwsgi.websocket_send("找不到答案face[委屈]，你可以戳戳a(https://www.baidu.com/s?wd=" + ucontent + ")[这里]")
                else:
                    if '简介' in ans.keys():
                        uwsgi.websocket_send(str(ans['简介']))
                    elif '介绍' in ans.keys():
                        uwsgi.websocket_send(str(ans['介绍']))
                    elif '产品说明' in ans.keys():
                        uwsgi.websocket_send(str(ans['产品说明']))
                    else:
                        uwsgi.websocket_send("a(https://www.baidu.com/s?wd=" + entity + ")[" + entity + "]")

        # 其他查询
        elif receive[0] == '#':
            res = receive.split(':')

            # 浏览器查询
            if receive.__contains__("NoMatchingTemplate"):
                wq = str(res[1].replace(" ", ""))
                # 如果包含表情符号，则直接输出
                if 'face[' in wq:
                    uwsgi.websocket_send(wq)
                else:
                    uwsgi.websocket_send("百度搜索-->a(https://www.baidu.com/s?wd=" + wq + ")[" + wq + "]")
        else:
            uwsgi.websocket_send(str(receive))


# @accept_websocket
# def getAnswer(request):
#     if request.is_websocket():
#         find = Find()
#         send = im()
#         alice = send.get_alice()
#         request.websocket.send(alice.respond('CONNECT SUCCEED').encode())
#         try:
#             while True:
#                 msg = request.websocket.read()
#                 if msg:
#                     msg = msg.decode()
#                     data = json.loads(msg)
#                     content = data['data']['mine']['content']
#                     ucontent = ''
#                     for char in content:
#                         if u'\u2E80' <= char <= u'\uFFFDh':
#                             ucontent += ' ' + char + ' '
#                         else:
#                             ucontent += char
#                     if ucontent.strip() == '':
#                         request.websocket.send("不要空格哦".encode())
#                     else:
#                         receive = alice.respond(ucontent)
#                         if receive == '':
#                             request.websocket.send(
#                                 ("找不到答案face[委屈]，你可以戳戳"
#                                     "a(https://www.baidu.com/s?wd=" + ucontent + ")[这里]").encode())
#
#                         # 数据库查询
#                         elif receive[0] == '$':
#                             # 获取用户输入的变量
#                             res = receive.split(':')
#
#                             # neo4j查询
#                             if receive.__contains__('neo4j'):
#                                 # 实体
#                                 entity = str(res[1]).replace(" ", "")
#                                 ans = find.matchNodebyTitle(entity)
#                                 if ans is None:
#                                     request.websocket.send(
#                                         ("找不到答案face[委屈]，你可以戳戳"
#                                             "a(https://www.baidu.com/s?wd=" + ucontent + ")[这里]").encode())
#                                 else:
#                                     if '简介' in ans.keys():
#                                         request.websocket.send(str(ans['简介']).encode())
#                                     elif '介绍' in ans.keys():
#                                         request.websocket.send(str(ans['介绍']).encode())
#                                     elif '产品说明' in ans.keys():
#                                         request.websocket.send(str(ans['产品说明']).encode())
#                                     else:
#                                         request.websocket.send(
#                                             ("a(https://www.baidu.com/s?wd=" + entity + ")[" + entity + "]").encode())
#
#                         # 其他查询
#                         elif receive[0] == '#':
#                             res = receive.split(':')
#
#                             # 浏览器查询
#                             if receive.__contains__("NoMatchingTemplate"):
#                                 wq = str(res[1].replace(" ", ""))
#                                 # 如果包含表情符号，则直接输出
#                                 if 'face[' in wq:
#                                     request.websocket.send(wq.encode())
#                                 else:
#                                     request.websocket.send(
#                                         ("百度搜索-->"
#                                             "a(https://www.baidu.com/s?wd=" + wq + ")[" + wq + "]").encode())
#                         else:
#                             request.websocket.send(str(receive).encode())
#         except BaseException as e:
#             print(e)
