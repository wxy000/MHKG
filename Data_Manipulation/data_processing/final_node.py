# -*- coding: utf-8 -*-
import json
import os

local_url = os.path.abspath(os.path.join(os.getcwd(), "../data"))
hebing = list()
with open(os.path.join(local_url, 'jibing_node.json'), 'r') as jibing:
    result1 = json.load(jibing)
    for i1 in result1:
        hebing.append(i1)
with open(os.path.join(local_url, 'zhengzhuang_node.json'), 'r') as zhengzhuang:
    result2 = json.load(zhengzhuang)
    for i2 in result2:
        hebing.append(i2)
with open(os.path.join(local_url, 'jiancha_node.json'), 'r') as jiancha:
    result3 = json.load(jiancha)
    for i3 in result3:
        hebing.append(i3)
with open(os.path.join(local_url, 'drugs_node.json'), 'r') as drugs:
    result4 = json.load(drugs)
    for i4 in result4:
        hebing.append(i4)

with open(os.path.join(local_url, 'final_node.json'), 'w') as f:
    json.dump(hebing, f, indent=4, ensure_ascii=False)
