# -*- coding: utf-8 -*-
import json
import re

from django.http import HttpResponse
from django.shortcuts import render

# noinspection PyUnresolvedReferences
from toolkit.nlp.NER import NER

# noinspection PyUnresolvedReferences
from toolkit.neo4j_operation.neo4j_crud import Find


def distinguish(request):
    return render(request, 'views/distinguish.html')


def getDistinguishData(request):
    text = request.POST.get('textarea', '')
    text = re.sub('\r|\n|\\s', '', text)
    text = text.replace('\\', '\\\\').replace('(', '\(').replace(')', '\)')
    text = text.replace('`', '\\`').replace('"', '\\"').replace('\'', '\\\'').replace(';', '\;')
    if text == '':
        result = {'code': 500, 'msg': "请输入要识别的句子"}
    else:
        ner = NER()
        retext = ""

        pipeitable = ""
        # 去重
        distinctnode = set()

        NE_List = ner.get_NE(text)
        for pair in NE_List:
            if str(pair[1]) == '#':
                retext += str(pair[0])
            elif str(pair[1]) == '##':
                retext += '<a style="color: #5FB878;" href="javascript:;">' + str(pair[0]) + '</a>'
            else:
                retext += '<a style="color: #01AAED;" href="baike?name=' + str(pair[0]) + '&id='\
                          + str(pair[1]) + '&label=' + str(pair[2]) + '">' + str(pair[0]) + '</a>'

                if str(pair[0]) not in distinctnode:
                    findNode = Find()
                    node = findNode.matchNodebyId(str(pair[1]))
                    jianjie = ""
                    try:
                        jianjie += node['简介']
                    except:
                        jianjie += ""
                    try:
                        jianjie += node['介绍']
                    except:
                        jianjie += ""
                    try:
                        jianjie += node['产品说明']
                    except:
                        jianjie += ""
                    pipeitable += '<tr><td>' + str(pair[0]) + '</td><td><a style="color: #01AAED;" href="baike?name='\
                                  + str(pair[0]) + '&id=' + str(pair[1]) + '&label='\
                                  + str(pair[2]) + '">' + str(pair[0]) + '</a></td><td>' + jianjie + '</td></tr>'
                    distinctnode.add(str(pair[0]))

        retext = '<p style="text-indent: 2em;">' + retext + '</p>'
        result = {'code': 0, 'msg': "", 'retext': retext, 'pipeitable': pipeitable}
    return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json,charset=utf-8")
