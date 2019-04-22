import random

from channels.generic.websocket import AsyncWebsocketConsumer
import json

# noinspection PyUnresolvedReferences
from toolkit.aiml.handle.neo4j import Find

# noinspection PyUnresolvedReferences
from toolkit.aiml.im import im

# noinspection PyUnresolvedReferences
from toolkit.mongodb_operation.mongodb_chatlog import mongo_chatlog


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['data']['mine']

        # message.pop('mine')
        mongo_cl = mongo_chatlog()
        mongo_cl.insertChatLog(str(message['id']), str(text_data_json['data']['to']['id']), message)

        to_user = text_data_json['data']['to']
        to_user_id = 'chat_' + str(text_data_json['data']['to']['id'])

        # Send message to room group
        await self.channel_layer.group_send(
            to_user_id,
            {
                'type': 'chat_message',
                'message': message,
                'to_user': to_user
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        to_user = event['to_user']
        if to_user['id'] == '-2' or to_user['id'] == -2:
            message['username'] = to_user['name']
            message['id'] = to_user['id']
            message['avatar'] = to_user['avatar']
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }, ensure_ascii=False).replace(u'\xa0', u''))


class RobotConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'robot_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['data']['mine']

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'robot_message',
                'message': message
            }
        )

    # Receive message from room group
    async def robot_message(self, event):
        message = event['message']
        msg = robot(message['content'], self.room_name)
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': msg
        }, ensure_ascii=False).replace(u'\xa0', u''))


def robot(content, userid):
    find = Find()
    send = im()
    alice = send.get_alice()
    ucontent = ''
    for char in content:
        if u'\u2E80' <= char <= u'\uFFFDh':
            ucontent += ' ' + char + ' '
        else:
            ucontent += char
    if ucontent.strip() == '':
        return "不要空格哦"
    else:
        receive = alice.respond(ucontent)
        if receive == '':
            return "找不到答案face[委屈]，你可以戳戳a(https://www.baidu.com/s?wd=" + content + ")[这里]"

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
                    if '.' not in str(userid):
                        return "找不到答案face[委屈]" \
                               "[div]你可以戳戳a(https://www.baidu.com/s?wd=" + content + ")[这里][/div]"
                    else:
                        return "找不到答案face[委屈]" \
                               "[div]1、你可以戳戳a(https://www.baidu.com/s?wd=" + content + ")[这里][/div]" \
                               "[div]2、a(javascript:get_doctor('#');)[点此登陆]，您可以享受到专业医生的服务[/div]"
                else:
                    if '简介' in ans.keys():
                        return str(ans['简介']) + \
                               "[div class=jiacu]详细情况可以咨询" + getDoctor(userid, entity) + "[/div]"
                    elif '介绍' in ans.keys():
                        return str(ans['介绍']) + \
                               "[div class=jiacu]详细情况可以咨询" + getDoctor(userid, entity) + "[/div]"
                    elif '产品说明' in ans.keys():
                        return str(ans['产品说明']) + \
                               "[div class=jiacu]详细情况可以咨询" + getDoctor(userid, entity) + "[/div]"
                    else:
                        return "a(https://www.baidu.com/s?wd=" + entity + ")[" + entity + "]"

        # 其他查询
        elif receive[0] == '#':
            res = receive.split(':')

            # 浏览器查询
            if receive.__contains__("NoMatchingTemplate"):
                wq = str(res[1].replace(" ", ""))
                # 如果包含表情符号，则直接输出
                if 'face[' in wq:
                    return wq
                else:
                    return "百度搜索-->a(https://www.baidu.com/s?wd=" + wq + ")[" + wq + "]"
        else:
            return str(receive)


def getDoctor(userid, entity):
    if '.' not in str(userid):
        return "[span doctorId=YS19032700 onmouseenter=get_doctor_mouseenter(this)]" \
               "a(javascript:get_doctor('YS19032700');)[欧阳豆豆][/span]"
    else:
        return "[span doctorId=# onmouseenter=get_doctor_mouseenter(this)]" \
               "a(javascript:get_doctor('#');)[" + entity + "][/span]"
