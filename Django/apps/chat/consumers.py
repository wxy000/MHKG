from channels.generic.websocket import AsyncWebsocketConsumer
import json

# noinspection PyUnresolvedReferences
from toolkit.aiml.handle.neo4j import Find

# noinspection PyUnresolvedReferences
from toolkit.aiml.im import im


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
        to_user = text_data_json['data']['to']
        to_user_id = 'chat_' + str(text_data_json['data']['to']['id'])
        if to_user_id == 'chat_-2':
            to_user_id = self.room_group_name

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
            message['content'] = robot(message['content'])
            message['username'] = to_user['name']
            message['id'] = to_user['id']
            message['avatar'] = to_user['avatar']
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }, ensure_ascii=False).replace(u'\xa0', u''))


def robot(content):
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
            return "找不到答案face[委屈]，你可以戳戳a(https://www.baidu.com/s?wd=" + ucontent + ")[这里]"

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
                    return "找不到答案face[委屈]，你可以戳戳a(https://www.baidu.com/s?wd=" + ucontent + ")[这里]"
                else:
                    if '简介' in ans.keys():
                        return str(ans['简介'])
                    elif '介绍' in ans.keys():
                        return str(ans['介绍'])
                    elif '产品说明' in ans.keys():
                        return str(ans['产品说明'])
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
