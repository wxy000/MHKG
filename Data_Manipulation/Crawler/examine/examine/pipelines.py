# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import copy
import csv
import json
import os
import sys
import time

sys.path.append("/root/MHKG/Data_Manipulation/utils")

from st import sec2time

local_url = os.path.abspath(os.path.join(os.getcwd(), "../../data"))


class JianchaPipeline(object):

    def __init__(self):
        firstRow = ['title', '简介', '适用性别', '是否空腹', '温馨提示', '正常值', '检查过程', '不适宜人群', '不良反应与风险']
        self.f = open(os.path.join(local_url, 'jiancha.csv'), 'w')
        self.fj = open(os.path.join(local_url, 'jiancha.json'), 'w')
        self.writer = csv.writer(self.f)
        self.writer.writerow(firstRow)
        self.itemSet = set()
        self.start = time.time()

    def process_item(self, item, spider):
        title = item['title']
        简介 = item['简介']
        适用性别 = item['适用性别']
        是否空腹 = item['是否空腹']
        温馨提示 = item['温馨提示']
        正常值 = item['正常值']
        检查过程 = item['检查过程']
        不适宜人群 = item['不适宜人群']
        不良反应与风险 = item['不良反应与风险']
        # 去重
        if title not in self.itemSet:
            self.writer.writerow((title, 简介, 适用性别, 是否空腹, 温馨提示, 正常值, 检查过程, 不适宜人群, 不良反应与风险))

            entityItem = copy.deepcopy(item)
            entityItem.pop("title")
            entityItem.pop("简介")
            entityItem.pop("适用性别")
            entityItem.pop("是否空腹")
            entityItem.pop("温馨提示")
            entityItem.pop("正常值")
            entityItem.pop("检查过程")
            entityItem.pop("不适宜人群")
            entityItem.pop("不良反应与风险")
            line = json.dumps(dict(entityItem), ensure_ascii=False) + '\n'
            self.fj.write(line)

            self.itemSet.add(title)
        return item

    def open_spider(self, spider):
        print("==================开启爬虫" + spider.name + "===================")

    def close_spider(self, spider):
        self.f.close()
        self.fj.close()
        now = time.time()
        t = int(now - self.start)
        print("总共用时：" + sec2time(t))
        print("==================关闭爬虫" + spider.name + "===================")
