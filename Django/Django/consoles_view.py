# -*- coding: utf-8 -*-
import os
import random

from django.shortcuts import render

# noinspection PyUnresolvedReferences
from toolkit.readCSV import readCSVByColumn

# noinspection PyUnresolvedReferences
from toolkit.neo4j_operation.neo4j_crud import Find

# noinspection PyUnresolvedReferences
from toolkit.readLabel import predict_labels


def getNode(request):
    local_url = os.path.abspath(os.path.join(os.getcwd(), 'data'))
    titles = readCSVByColumn(os.path.join(local_url, 'jibing.csv'), 'title')
    num = random.randint(0, len(titles))
    find = Find()
    result = find.matchNodeRelationbyTitle('疾病', titles[num])
    # print(result)
    return result


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


# noinspection PyStatementEffect
def consoles(request):
    result = getNode(request)
    # print(result)
    node = list()
    link = list()
    for i in result[0]:
        labels = predict_labels
        temp = {'name': i['title'] + "(" + i['label'] + ")",
                'url': 'baike?name=' + i['title'] + '&id=' + str(i['id']) + '&label=' + str(labels[i['title']]),
                'category': getNum(request, i['label'])}
        if temp not in node:
            node.append(temp)
    # print(node)
    for j in result[1]:
        findNode = Find()
        label1 = findNode.matchNodeLabel(j['source'])
        source = findNode.get_node(j['source'])
        j['source'] = source + "(" + label1 + ")"
        label2 = findNode.matchNodeLabel(j['target'])
        target = findNode.get_node(j['target'])
        j['target'] = target + "(" + label2 + ")"
        link.append(j)
    # print(link)
    nodeRelation = {'data': node, 'links': link}
    return render(request, 'views/consoles.html', {'item': result[0][0], 'nodeRelation': nodeRelation})
