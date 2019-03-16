#!/usr/bin/python
# -*- coding:utf-8 -*-
import re
import time
import sys

import geoip2.database
from user_agents import parse

# noinspection PyUnresolvedReferences
from mongodb_operation.mongodb_logfile import mongo


class nginx:

    def getData(self, filepath1, filepath2, filepath3):

        filepath = filepath1 + filepath2 + filepath3
        line = open(filepath, 'r')

        try:
            for i in line:
                matchObj = re.match(r'(.*) - (.*) \[(.*)\] \"(.*) (\/.*) (.*)\" (.*) (.*) \"(.*)\" \"(.*)\"', i, re.I)
                if matchObj is not None:
                    logdict = dict()
                    ip = matchObj.group(1)
                    user = matchObj.group(2)
                    log_time = self.parsetime(matchObj.group(3))
                    method = matchObj.group(4)
                    request = matchObj.group(5)
                    status = matchObj.group(7)
                    bodyBytesSent = matchObj.group(8)
                    refer = matchObj.group(9)
                    userAgent = matchObj.group(10)

                    # 解析成user_agent
                    user_agent = parse(userAgent)
                    # 判断是什么浏览器
                    bw = user_agent.browser.family
                    # 判断是什么操作系统
                    s = user_agent.os.family

                    # print(ip, user, log_time, method, request, status, bodyBytesSent, refer, bw, s)
                    logdict['ip'] = ip
                    logdict['user'] = user
                    logdict['log_time'] = log_time
                    logdict['method'] = method
                    logdict['request'] = request
                    logdict['status'] = status
                    logdict['bodyBytesSent'] = bodyBytesSent
                    logdict['refer'] = refer
                    logdict['bw'] = bw
                    logdict['s'] = s

                    ips = self.parse_ip(ip)
                    if ips['code'] == 0:
                        logdict['country'] = ips['country']
                        logdict['subdivisions'] = ips['subdivisions']
                        logdict['city'] = ips['city']
                        logdict['latitude'] = ips['latitude']
                        logdict['longitude'] = ips['longitude']
                    else:
                        logdict['country'] = '中国'
                        logdict['subdivisions'] = '浙江'
                        logdict['city'] = '杭州'
                        logdict['latitude'] = '30.294'
                        logdict['longitude'] = '120.1619'

                    # 执行sql插入
                    print(logdict)
                    m = mongo()
                    m.insertDict(filepath2, logdict)

        finally:
            line.close()

    def parsetime(self, log_time):
        time_str = '%s' % log_time.split(' ')[0]
        return time.strftime("%Y-%m-%d %H:%M:%S", time.strptime(time_str, '%d/%b/%Y:%H:%M:%S'))

    def parse_ip(self, ip):
        try:
            reader = geoip2.database.Reader('GeoLite2-City.mmdb')
            data = reader.city(ip)
            try:
                country = data.country.names['zh-CN']  # 获取国家
            except:
                country = data.country.name
            try:
                subdivisions = data.subdivisions.most_specific.names['zh-CN']  # 获取省份
            except:
                subdivisions = data.subdivisions.most_specific.name
            try:
                city = data.city.names['zh-CN']  # 获取城市
            except:
                city = data.city.name
            latitude = data.location.latitude  # 获取纬度
            longitude = data.location.longitude  # 获取经度
            return {'code': 0, 'country': country, 'subdivisions': subdivisions,
                    'city': city, 'latitude': latitude, 'longitude': longitude}
        except:
            return {'code': 500}


if __name__ == '__main__':
    t = nginx()
    t.getData(sys.argv[1], sys.argv[2], sys.argv[3])
    # t.getData("/root/MHKG/Django/logs/", "nginx_access_20190222", ".log")
