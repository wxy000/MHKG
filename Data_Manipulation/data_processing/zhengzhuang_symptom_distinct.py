# -*- coding: utf-8 -*-
import codecs
import json
import os

local_url = os.path.abspath(os.path.join(os.getcwd(), '../data'))

entity = list()
resultJsonFile = codecs.open(os.path.join(local_url, 'zhengzhuang_symptom_corrected.json'), 'w', encoding='utf-8')
with open(os.path.join(local_url, 'zhengzhuang_symptom.json'), 'r') as f:
    for line in f.readlines():
        resultJson = json.loads(line)
        entity1 = resultJson['entity1']
        entity2 = resultJson['entity2']
        if entity1 == entity2:
            continue
        e12 = entity1 + '-' + entity2
        e21 = entity2 + '-' + entity1
        if e12 not in entity and e21 not in entity:
            entity.append(e12)
            entity.append(e21)
            resultJsonFile.write(line)
