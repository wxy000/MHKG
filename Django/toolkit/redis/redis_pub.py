# -*- coding:utf8 -*-

# noinspection PyUnresolvedReferences
from redis_helper import RedisHelper

obj = RedisHelper()
obj.public('channel1', 'hello')
