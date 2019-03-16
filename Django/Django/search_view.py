# -*- coding: utf-8 -*-
import re

from django.shortcuts import render

# noinspection PyUnresolvedReferences
from toolkit.neo4j_operation.neo4j_crud import Find


def search(request):
    # 获取get请求中的值
    keywords = request.GET.get('keywords')
    p = re.compile(r'[\s+\.\!\/_,$%^*(+\"\'\\\]+|[+——！，。？、~@#￥%……&*（）]+')
    keywords = re.sub(p, "", keywords)
    node = list()
    if keywords != '':
        # 查询对应节点
        findNode = Find()
        result = findNode.likeMatchNodeByTitle(keywords)
        # print(result)
        if result is not None:
            for i in result:
                id = i[0]['id']
                title = i[0]['title']
                t = title
                title = title.replace(keywords, '<span style="color: red;">' + keywords + '</span>')
                if '简介' in i[0].keys():
                    des = i[0]['简介']
                elif '介绍' in i[0].keys():
                    des = i[0]['介绍']
                elif '产品说明' in i[0].keys():
                    des = i[0]['产品说明']
                else:
                    des = ''
                des = des.replace(keywords, '<span style="color: red;">' + keywords + '</span>')
                if 'img'in i[0].keys():
                    img = i[0]['img']
                else:
                    img = ''
                temp = {'title': title, 'des': des, 'img': img, 'url': 'entity?name=' + t + '&id=' + str(id)}
                node.append(temp)
        # print(node)
    else:
        node = []

    return render(request, 'views/search.html', {'nodes': node})
