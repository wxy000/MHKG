# -*- coding: utf-8 -*-
from django.shortcuts import render

# noinspection PyUnresolvedReferences
from toolkit.nlp.NER import NER

# noinspection PyUnresolvedReferences
from toolkit.neo4j_operation.neo4j_crud import Find

local_path = '/root/MHKG/Django/data/'


# 数据标注页面的view
# 接收GET请求数据
def show(request):
    ctx = {}
    if 'title' in request.GET:
        ctx['title'] = '<h3><b>' + str(request.GET['title']) + '</b></h3>'
        find = Find()
        node = find.matchItemByTitle(str(request.GET['title']))
        if len(node) > 0:
            jianjie = '<div>'
            try:
                jianjie += '<img src="' + node[0]['n']['img'] + '"' \
                    'onerror="this.src=\'../../../static/layuiadmin/style/default.jpg\';' \
                    'this.onerror=null" height="auto" width="20%"' \
                    'style="float: left; padding-right: 20px;">'
            except:
                jianjie += '<img src="../../../static/layuiadmin/style/default.jpg"' \
                    'height="auto" width="20%"' \
                    'style="float: left; padding-right: 20px;">'
            try:
                jianjie += '<p style="text-indent:2em;">' + node[0]['n']['介绍'] + '</p>'
            except:
                jianjie += ''
            try:
                jianjie += '<p style="text-indent:2em;">' + node[0]['n']['简介'] + '</p>'
            except:
                jianjie += ''
            try:
                jianjie += '<p style="text-indent:2em;">' + node[0]['n']['产品说明'] + '</p>'
            except:
                jianjie += ''
            jianjie += '</div>'
            ctx['jianjie'] = jianjie
        # 动态生成check控件----------------------------------

        tag_name_list = []
        file_object = open(local_path + 'tag_list.txt', 'r')
        for f in file_object:
            tag_name_list.append(f.strip())
        file_object.close()

        text = '<div class="layui-form-item" style="padding-left: 10px;"><div class="layui-input-inline">'
        label = NER()
        for tag in tag_name_list:
            l1 = label.get_explain(tag)
            text += '<input type="radio" name="label" value="' + str(tag) + '"' \
                'title="' + str(tag) + '(' + str(l1) + ')"><br/>'
        text += '</div></div>'

        # 放置一个隐藏的输入框，传递title的值到缓冲页面
        text += "<input name='title' value='" + str(request.GET["title"]) + "' style='display:none;'></input>"

        ctx['taggingCheck'] = text

        # 统计当前标注情况
        file_object = open(local_path + 'labeled_data.txt', 'r')
        s = {}
        sum = 0
        # LEN = len(tag_name_list)
        for i in tag_name_list:
            s[i] = 0
        try:
            for f in file_object:
                pair = f.split()
                s[pair[0].strip()] += 1
        except Exception:
            pass
        for i in tag_name_list:
            sum += s[i]
        file_object.close()
        # 用于记录已标注样本个数
        text = "<br/>"
        for i in tag_name_list:
            text += '<h3 style="line-height: 2; margin-left: 20px;">标签 '
            text += '<span style="color: #393D49;">' + str(i) + '</span>：' + str(s[i]) + '</h3>'
        text += '<hr/><h3 style="line-height: 2; margin-left: 20px;"><b>已标记总数：' + str(sum) + '</b></h3><br/>'
        ctx['already'] = text

    return render(request, "ManualAnnotation/tagging_data.html", ctx)
