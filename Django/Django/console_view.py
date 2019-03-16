# -*- coding: utf-8 -*-
import json
import random
import re
import psutil

import requests
from django.http import HttpResponse
from django.shortcuts import render


def crawlpage(request):
    # 随机访问页面
    bigpage = random.randint(1, 405)
    base_url = 'https://ys.99.com.cn/slys/1997-' + str(bigpage) + '.htm'
    # 随机获取页面文章
    smallpage = random.randint(0, 14)
    # 爬取页面
    r = requests.get(base_url)
    r.encoding = 'gb2312'

    print(str(bigpage) + "====" + str(smallpage))
    try:
        # 文章标题
        pattern1 = re.compile('class="ico_pic".*?<a.*?href.*?>(.*?)</a>.*?</div>', re.S)
        titles = re.findall(pattern1, r.text)
        # 文章摘要
        pattern2 = re.compile('class="fengP2".*?>(.*?)</p>', re.S)
        abstract = re.findall(pattern2, r.text)
        # 具体文章链接
        pattern3 = re.compile('class="fengqw".*?>.*?<a.*?href="(.*?)".*?>', re.S)
        url = re.findall(pattern3, r.text)

        article = {'title': titles[smallpage], 'abstract': abstract[smallpage].strip(), 'url': 'https:' + url[smallpage]}
    except:
        article = {'title': '哎呀，走丢了', 'abstract': '', 'url': 'javascript:void(0);'}

    return article


def console(request):
    r = crawlpage(request)
    print(r)
    return render(request, 'views/console.html', {'article': r})
