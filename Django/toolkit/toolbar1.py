# -*- coding:utf-8 -*-
import re
import time
import sys

import geoip2.database
from user_agents import parse


class Toolbar1:

    def getData(self, name, tableip='', tableaddress='', tablestarttime='00:00:00', tableendtime='23:59:59'):

        line = open("/root/MHKG/Django/logs/nginx_access.log", 'r')

        try:
            temp = list()
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

                    # print(logdict)
                    temp.append(logdict)
            if name == 'area':
                citytemp = set()
                # 每个城市的ip数量
                citynum = list()
                # 每个城市的经纬度
                cityaddress = dict()
                for item in temp:
                    if item['city'] in citytemp and (str(item['city']) + item['ip']) not in citytemp:
                        for city in citynum:
                            if city['name'] == item['city']:
                                city['value'] += 1
                                citytemp.add(str(item['city']) + item['ip'])
                    elif item['city'] not in citytemp:
                        citynum.append({'name': item['city'], 'value': 1})
                        cityaddress[item['city']] = [float(item['longitude']), float(item['latitude'])]
                        citytemp.add(item['city'])
                        citytemp.add(str(item['city']) + item['ip'])
                # print(citytemp)
                return {'citynum': citynum, 'cityaddress': cityaddress}
            elif name == 'liulanqi':
                bwtemp = set()
                # 浏览器
                liulanqi = list()
                # 浏览器数量
                liulanqivalue = list()
                for item in temp:
                    if item['bw'] in bwtemp:
                        for brower in liulanqivalue:
                            if brower['name'] == item['bw']:
                                brower['value'] += 1
                    else:
                        bwtemp.add(item['bw'])
                        liulanqivalue.append({'name': item['bw'], 'value': 1})
                for ss in bwtemp:
                    liulanqi.append(ss)
                return {'liulanqi': liulanqi, 'liulanqivalue': liulanqivalue}
            elif name == 'xitong':
                ostemp = set()
                # 操作系统
                xitong = list()
                # 操作系统数量
                xitongvalue = list()
                for item in temp:
                    if item['s'] in ostemp:
                        for oss in xitongvalue:
                            if oss['name'] == item['s']:
                                oss['value'] += 1
                    else:
                        ostemp.add(item['s'])
                        xitongvalue.append({'name': item['s'], 'value': 1})
                for ss in ostemp:
                    xitong.append(ss)
                return {'xitong': xitong, 'xitongvalue': xitongvalue}
            elif name == 'table':
                item = list()
                for it in temp:
                    if (tableip in it['ip']) and (tableaddress in it['country'] or tableaddress in it['subdivisions']
                                                  or tableaddress in it['city']) and (
                            tablestarttime <= it['log_time'][11:]) and (tableendtime >= it['log_time'][11:]):
                        t = {'log_time': it['log_time'], 'refer': it['refer'], 'request': it['request'],
                             'ip': it['ip'], 'address': it['country'] + '-' + it['subdivisions'] + '-' + it['city']}
                        item.append(t)
                return item

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
