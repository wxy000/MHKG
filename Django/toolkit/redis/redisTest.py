# -*- coding:utf8 -*-

# noinspection PyUnresolvedReferences
from redis_helper import RedisHelper

obj = RedisHelper()
redis_sub = obj.subscribe('channel1')

while True:
    msg = redis_sub.parse_response()
    print(msg)
    print("111")
# for item in redis_sub.listen():
#     print(item)
# print("1212121")

# import redis
#
# pool = redis.ConnectionPool(host='39.108.111.94', password='wxy123456', decode_responses=True)
# r = redis.Redis(connection_pool=pool)
# r.lpush('1', 'hello1')
# r.lpush('1', 'hello2')
# r.lpush('1', 'hello3')
# r.lpush('1', 'hello1')
# for i in range(r.llen('1')):
#     print(r.rpop('1'))
