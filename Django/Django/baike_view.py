# -*- coding: utf-8 -*-
from django.shortcuts import render

# noinspection PyUnresolvedReferences
from toolkit.neo4j_operation.neo4j_crud import Find

# noinspection PyUnresolvedReferences
from toolkit.mongodb_operation.mongodb_getlabel import MongoLabel

# noinspection PyUnresolvedReferences
from toolkit.nlp.NER import NER

# noinspection PyUnresolvedReferences
from toolkit.readLabel import predict_labels


def baike(request):
    # 获取get请求中的值
    name = request.GET.get('name')
    id = request.GET.get('id')
    nodelabel = str(request.GET.get('label', ''))
    explain = ''
    detail_explain = ''
    if nodelabel != '':
        ner = NER()
        explain = ner.get_explain(nodelabel)
        detail_explain = ner.get_detail_explain(nodelabel)

    # 查询对应节点
    findNode = Find()
    label = findNode.matchNodeLabel(id)
    result = findNode.matchNodeRelationbyTitle(label, name)
    # print(result)
    if len(result[0]) == 0 and len(result[1]) == 0:
        result = [[findNode.matchNodebyId(id)], []]
    node = list()
    # 查询某节点全部父分类
    parentlabel = list()
    ml = MongoLabel()
    jids = ml.getJid(id, name)
    for jid in jids:
        parentlabel.append(ml.getLabel(jid))

    for i, num in zip(result[0], range(200, -1, -1)):
        if str(i['id']) != id:
            labels = predict_labels
            temp = {'name': i['title'], 'value': num,
                    'url': '?name=' + i['title'] + '&id=' + str(i['id']) + '&label=' + str(labels[i['title']])}
            if temp not in node:
                node.append(temp)

    return render(request, 'views/baike.html', {'item': result[0][0], 'nodes': node,
                                                'explain': explain, 'detail_explain': detail_explain,
                                                'parentlabel': parentlabel})
