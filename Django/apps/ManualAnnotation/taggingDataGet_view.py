# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.decorators import csrf
import random

local_path = '/root/MHKG/Django/data/'


# 先将标注写入文件，之后跳转到tagging_cache.html再进行新页面的跳转
def tagging_push(request):
    ctx = {}
    # 先将已有的labels存入字典中
    s = set()
    try:
        f1 = open(local_path + 'labeled_data.txt', 'r')
        for f in f1:
            pair = f.strip().split()
            curs = ""
            for i in range(1, len(pair)):
                if i > 1:
                    curs += ' '
                curs += str(pair[i])
            s.add(curs.strip())

        f1.close()
    except Exception:
        makefile = open(local_path + 'labeled_data.txt', 'w')
        makefile.close()

    f2 = open(local_path + 'unlabeled_data.txt', 'r')
    all_list = []
    for f in f2:
        all_list.append(f.strip())
    f2.close()
    ln = len(all_list)
    next_title = all_list[random.randint(0, ln - 1)]

    if 'label' in request.GET and 'title' in request.GET:
        print(str(request.GET) + ".....")
        title = str(request.GET['title']).strip()
        label = str(request.GET['label']).strip()
        if label is not None:
            f3 = open(local_path + 'labeled_data.txt', 'a')
            if title in s:
                print("该title已存在，冲突！")
            else:
                f3.write(label + " " + title + "\n")
                s.add(title)
            f3.close()
        else:
            print('用户未选择label')

    if len(s) >= len(all_list):
        return render(request, "ManualAnnotation/over.html")

    # 如果冲突就再选
    while next_title in s:
        next_title = all_list[random.randint(0, ln - 1)].strip()

    ctx['next'] = "<input id='next' value='" + next_title + "' style='display:none;'></input>"

    return render(request, "ManualAnnotation/tagging_cache.html", ctx)
