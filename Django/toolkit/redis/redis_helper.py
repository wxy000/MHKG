# -*- coding:utf8 -*-

import redis


class RedisHelper(object):

    def __init__(self):
        pool = redis.ConnectionPool(host='39.108.111.94', password='wxy123456', decode_responses=True)
        self.__conn = redis.Redis(connection_pool=pool)

    def public(self, chan_sub, msg):
        self.__conn.publish(chan_sub, msg)
        return True

    def subscribe(self, chan_sub):
        pub = self.__conn.pubsub()
        pub.subscribe(chan_sub)  # 订阅的频道
        # pub.listen()
        return pub
