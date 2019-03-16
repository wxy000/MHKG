# -*- coding: utf-8 -*-
import json
import os

local_url = os.path.abspath(os.path.join(os.getcwd(), "../data"))
fi = list()
with open(os.path.join(local_url, 'jibing_classify.json'), 'r') as jibing:
    result1 = json.load(jibing)
    if result1['name'] == "疾病百科":
        result1['name'] = "疾病"
    for i in result1['children']:
        if i['parent'] == "疾病百科":
            i['parent'] = "疾病"
    fi.append(result1)
with open(os.path.join(local_url, 'zhengzhuang_classify.json'), 'r') as zhengzhuang:
    result2 = json.load(zhengzhuang)
    if result2['name'] == "症状百科":
        result2['name'] = "症状"
    for i in result2['children']:
        if i['parent'] == "症状百科":
            i['parent'] = "症状"
    fi.append(result2)
with open(os.path.join(local_url, 'jiancha_classify.json'), 'r') as jiancha:
    result3 = json.load(jiancha)
    fi.append(result3)
with open(os.path.join(local_url, 'drugs_classify.json'), 'r') as drugs:
    result4 = json.load(drugs)
    fi.append(result4)

with open(os.path.join(local_url, 'final_classify.json'), 'w') as f:
    json.dump(fi, f, indent=4, ensure_ascii=False)
