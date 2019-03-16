# -*- coding: utf-8 -*-
from django.shortcuts import render

# noinspection PyUnresolvedReferences
from toolkit.neo4j_operation.neo4j_crud import Find

# noinspection PyUnresolvedReferences
from toolkit.mongodb_operation.mongodb_getlabel import MongoLabel


def getNum(request, label):
    num = ''
    if label == '疾病':
        num = 0
    elif label == '症状':
        num = 1
    elif label == '检查':
        num = 2
    elif label == '药品':
        num = 3
    return num


def entity(request):
    # 获取get请求中的值
    name = request.GET.get('name')
    id = request.GET.get('id')

    # 查询某节点全部父分类
    parentlabel = list()
    ml = MongoLabel()
    jids = ml.getJid(id, name)
    for jid in jids:
        parentlabel.append(ml.getLabel(jid))

    # 查询对应节点
    findNode = Find()
    label = findNode.matchNodeLabel(id)
    result = findNode.matchNodeRelationbyTitle(label, name)
    # print(len(result))
    if len(result[0]) == 0 and len(result[1]) == 0:
        result = [[findNode.matchNodebyId(id)], []]
        # print(result)
    node = list()
    link = list()
    for i in result[0]:
        if str(i['id']) != id:
            temp = {'name': i['title'] + "(" + i['label'] + ")", 'url': '?name=' + i['title'] + '&id=' + str(i['id']), 'category': getNum(request, i['label'])}
        else:
            temp = {'name': i['title'] + "(" + i['label'] + ")", 'category': getNum(request, i['label'])}
        if temp not in node:
            node.append(temp)
    for j in result[1]:
        # print(j)
        findNode = Find()
        label1 = findNode.matchNodeLabel(j['source'])
        source = findNode.get_node(j['source'])
        j['source'] = source + "(" + label1 + ")"
        label2 = findNode.matchNodeLabel(j['target'])
        target = findNode.get_node(j['target'])
        j['target'] = target + "(" + label2 + ")"
        link.append(j)
    # print(node)
    nodeRelation = {'data': node, 'links': link}

    return render(request, 'views/entity.html', {'item': result[0][0], 'nodeRelation': nodeRelation,
                                                 'parentlabel': parentlabel})
