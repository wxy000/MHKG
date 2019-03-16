# -*- coding: utf-8 -*-
import json

from django.http import HttpResponse
from django.shortcuts import render

# noinspection PyUnresolvedReferences
from toolkit.neo4j_operation.neo4j_crud import Find

# noinspection PyUnresolvedReferences
from toolkit.readLabel import predict_labels


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


def relationQuery(request):
    return render(request, 'views/relationQuery.html')


def getRelation(request):
    findNode = Find()
    relation = findNode.matchAllRelation()
    result = {'relation': relation}
    return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json,charset=utf-8")


def getNode(request):
    name = request.GET.get('name')
    findNode = Find()
    nodes = findNode.matchAllNode(name)
    return HttpResponse(json.dumps(nodes, ensure_ascii=False), content_type="application/json,charset=utf-8")


def getNodeRelation(request):
    entity1 = request.GET.get('entity1')
    entity2 = request.GET.get('entity2')
    relation = request.GET.get('relation')
    find = Find()
    result = find.matchRelationByNode(entity1, entity2, relation)
    if len(result[0]) == 0 and len(result[1]) == 0:
        if entity1 != 'undefined' and entity2 != 'undefined':
            result = [[find.matchNodebyId(entity1), find.matchNodebyId(entity2)], []]
        elif entity1 == 'undefined':
            result = [[find.matchNodebyId(entity2)], []]
        elif entity2 == 'undefined':
            result = [[find.matchNodebyId(entity1)], []]

    node = list()
    link = list()
    for i in result[0]:
        labels = predict_labels
        temp = {'name': i['title'] + "(" + i['label'] + ")",
                'url': 'baike?name=' + i['title'] + '&id=' + str(i['id']) + '&label=' + str(labels[i['title']]),
                'category': getNum(request, i['label'])}
        if temp not in node:
            node.append(temp)
    for j in result[1]:
        label1 = find.matchNodeLabel(j['source'])
        source = find.get_node(j['source'])
        j['source'] = source + "(" + label1 + ")"
        label2 = find.matchNodeLabel(j['target'])
        target = find.get_node(j['target'])
        j['target'] = target + "(" + label2 + ")"
        link.append(j)

    items = {'data': node, 'links': link}

    return HttpResponse(json.dumps(items, ensure_ascii=False), content_type="application/json,charset=utf-8")
