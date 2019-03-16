# -*- coding: utf-8 -*-
import json
import string
from zhon import hanzi

import pinyin
from django.http import HttpResponse
from django.shortcuts import render

# noinspection PyUnresolvedReferences
from toolkit.mongodb_operation.mongodb_crud import Mongo

# noinspection PyUnresolvedReferences
from toolkit.readLabel import predict_labels


def classifiedQuery(request):
    return render(request, 'views/classifiedQuery.html')


def getFenlei(request):
    m = Mongo()
    fenlei = m.getFenlei()
    result = {'fenlei': fenlei}
    return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json,charset=utf-8")


def getEntity(request):
    # 所有的标点符号
    punc = string.punctuation
    hanzipunc = hanzi.punctuation
    print(punc, hanzipunc)

    entities = list()
    temp = list()
    cc = set()
    m = Mongo()
    ids = request.POST
    for key in ids:
        val = request.POST.getlist(key)
        for jid in val:
            for entity in m.getEntity(jid):
                labels = predict_labels
                entity['url'] = "baike?name=" + entity['name'] + "&id=" + str(entity['nid']) + "&label=" + str(labels[entity['name']])
                if (entity['name'][0] in hanzipunc) or (entity['name'][0] in punc):
                    shou = '_'
                else:
                    shou = pinyin.get_initial(entity['name'][0]).upper()
                tmp = {'key': shou, 'value': entity}
                temp.append(tmp)
    for e in temp:
        if e['key'] not in cc:
            t = {'key': e['key'], 'value': [e['value']]}
            entities.append(t)
            cc.add(e['key'])
        else:
            for i in entities:
                if i['key'] == e['key']:
                    i['value'].append(e['value'])
    result = {'entities': sorted(entities, key=lambda x: x['key'])}
    return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json,charset=utf-8")
