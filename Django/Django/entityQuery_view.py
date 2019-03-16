# -*- coding: utf-8 -*-
import json
import re
import time

import requests
from django.shortcuts import render


def crawlweek(request):
    # 访问页面
    base_url = 'http://med.ckcest.cn/index.html'
    # 爬取页面
    r = requests.get(base_url)
    # r.encoding = 'gb2312'
    week = list()
    # print(r.text)

    try:
        # 文章标题
        pattern1 = re.compile('class="item".*?<h3>.*?<a.*?class="ellipsis".*?>(.*?)</a>.*?</h3>', re.S)
        titles = re.findall(pattern1, r.text)
        # print(titles)
        # 文章链接
        pattern2 = re.compile('class="item".*?<a.*?href="(.*?)".*?>.*?<img.*?class="ellipsis"', re.S)
        url = re.findall(pattern2, r.text)
        # print(url)
        # 图片链接
        pattern2 = re.compile('class="item".*?<a.*?href=".*?".*?>.*?<img.*?src="(.*?)".*?class="ellipsis"', re.S)
        imgurl = re.findall(pattern2, r.text)
        # print(imgurl)

        for t, u, i in zip(titles, url, imgurl):
            if i[:2] == '//':
                i = 'http:' + i
            else:
                i = 'http://med.ckcest.cn/' + i
            temp = {'title': t, 'url': 'http://med.ckcest.cn/' + u, 'imgurl': i}
            week.append(temp)

    except:
        week = []

    return week


def crawlarticle(request):
    # 访问页面
    base_url = 'http://news.bioon.com/medical'
    # 头部标识
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/52.0.2743.116 Safari/537.36 '
    }
    # 爬取页面
    r = requests.get(base_url, headers=headers)
    # r.encoding = 'gb2312'
    # print(r.text)
    article = list()

    try:
        # for text in sj[0]['searchNews']:
        #     # print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        #     title = text['title'][0]
        #     url = 'http://med.ckcest.cn/details.html?id=' + str(text['id'][0]) + '&classesEn=news'
        #     # date = '2018' + '-' + str(text['date'][0]['month'] + 1) + '-' + str(text['date'][0]['date'])
        #     date = time.strftime("%Y-%m-%d", time.localtime())
        #     temp = {'title': title, 'url': url, 'date': date}
        #     article.append(temp)
        # 文章标题
        pattern1 = re.compile('<li.*?data-i.*?<h4>.*?<a.*?>(.*?)</a>.*?</h4>', re.S)
        titles = re.findall(pattern1, r.text)
        # 文章链接
        pattern2 = re.compile('<li.*?data-i.*?<h4>.*?<a.*?href="(.*?)".*?>.*?</a>.*?</h4>', re.S)
        url = re.findall(pattern2, r.text)
        # 发表时间
        pattern3 = re.compile('<li.*?data-i.*?class="fl huise".*?>(.*?)</div>', re.S)
        date = re.findall(pattern3, r.text)
        for title, u, d in zip(titles, url, date):
            if len(title) > 25:
                title = title[0:25] + '...'
            temp = {'title': title, 'url': u, 'date': d}
            article.append(temp)

    except:
        article = []

    return article


def entityQuery(request):
    r = crawlweek(request)
    print(r)
    a = crawlarticle(request)
    print(a)
    return render(request, 'views/entityQuery.html', {'week': r, 'article': a})
