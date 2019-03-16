# -*- coding: utf-8 -*-

"""
    说明： appid和secretKey为百度翻译文档中自带的，需要切换为自己的
           python2和python3部分库名称更改对应如下：
           httplib      ---->    http.client
           md5          ---->    hashlib.md5
           urllib.quote ---->    urllib.parse.quote
    官方链接：
           http://api.fanyi.baidu.com/api/trans/product/index

"""

import http.client
import hashlib
import json
import random
from urllib.parse import quote

import requests


def baidu_translate(word, fromlang, tolang):
    # appid = '20151113000005349'
    # secretKey = 'osubCEzlGjzvw8qdQc41'
    # httpClient = None
    # myurl = '/api/trans/vip/translate'
    # q = word
    # # 源语言
    # fromLang = fromlang
    # # 翻译后的语言
    # toLang = tolang
    # salt = random.randint(32768, 65536)
    # sign = appid + q + str(salt) + secretKey
    # sign = hashlib.md5(sign.encode()).hexdigest()
    # myurl = myurl + '?appid=' + appid + '&q=' + quote(q) + '&from=' + fromLang + '&to=' + toLang + '&salt=' + str(salt) + '&sign=' + sign
    #
    # try:
    #     httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
    #     httpClient.request('GET', myurl)
    #     # response是HTTPResponse对象
    #     response = httpClient.getresponse()
    #     # 获得返回的结果，结果为json格式
    #     jsonResponse = response.read().decode("utf-8")
    #     # 将json格式的结果转换字典结构
    #     js = json.loads(jsonResponse)
    #     # 取得翻译后的文本结果
    #     dst = str(js["trans_result"][0]["dst"])
    #     return dst
    # except Exception as e:
    #     print(e)
    #     return None
    # finally:
    #     if httpClient:
    #         httpClient.close()

    req_url = 'https://fanyi.baidu.com/transapi'
    Form_Data = {"query": word, 'from': fromlang, 'to': tolang}

    translate_result = requests.post(req_url, Form_Data)
    result = translate_result.json()  # 转化为json格式
    return result['data'][0]['dst']


# if __name__ == '__main__':
#     content = input("请输入要翻译的内容：")
#     print(baidu_translate(content, 'auto', 'zh'))
