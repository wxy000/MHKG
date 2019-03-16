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


class ZhengzhuangPipeline(object):

    def __init__(self):
        firstRow = ['title', '介绍', '预防', '食疗']
        self.f = open(os.path.join(local_url, 'zhengzhuang.csv'), 'w')
        self.ff = open(os.path.join(local_url, 'zhengzhuang.json'), 'w')
        self.writer = csv.writer(self.f)
        self.writer.writerow(firstRow)
        self.itemSet = set()
        self.start = time.time()

    def process_item(self, item, spider):
        self.writer.writerow((item['title'], item['介绍'], item['预防'], item['食疗']))
        if item['title'] not in self.itemSet:
            entityItem = copy.deepcopy(item)
            entityItem.pop("title")
            entityItem.pop("介绍")
            entityItem.pop("预防")
            entityItem.pop("食疗")
            line = json.dumps(dict(entityItem), ensure_ascii=False) + '\n'
            self.ff.write(line)
            self.itemSet.add(item['title'])
        return item

    def open_spider(self, spider):
        print("==================开启爬虫" + spider.name + "===================")

    def close_spider(self, spider):
        self.f.close()
        self.ff.close()
        now = time.time()
        t = int(now - self.start)
        print("总共用时：" + sec2time(t))
        print("==================关闭爬虫" + spider.name + "===================")


class ZhengzhuangSymptomPipeline(object):

    def __init__(self):
        self.f = open(os.path.join(local_url, 'zhengzhuang_symptom.json'), 'w')
        self.start = time.time()

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + '\n'
        self.f.write(line)
        return item

    def open_spider(self, spider):
        print("==================开启爬虫" + spider.name + "===================")

    def close_spider(self, spider):
        self.f.close()
        now = time.time()
        t = int(now - self.start)
        print("总共用时：" + sec2time(t))
        print("==================关闭爬虫" + spider.name + "===================")


class ZhengzhuangInspectPipeline(object):

    def __init__(self):
        firstRow = ['entity1', 'entity2', 'relation']
        self.f = open(os.path.join(local_url, 'zhengzhuang_inspect.csv'), 'w')
        self.writer = csv.writer(self.f)
        self.writer.writerow(firstRow)
        self.itemSet = set()
        self.start = time.time()

    def process_item(self, item, spider):
        entity1 = item['entity1']
        entity2 = item['entity2']
        relation = item['relation']
        i = entity1 + entity2 + relation
        # 去重
        if i not in self.itemSet:
            self.writer.writerow((entity1, entity2, relation))
            self.itemSet.add(i)
        return item

    def open_spider(self, spider):
        print("==================开启爬虫" + spider.name + "===================")

    def close_spider(self, spider):
        self.f.close()
        now = time.time()
        t = int(now - self.start)
        print("总共用时：" + sec2time(t))
        print("==================关闭爬虫" + spider.name + "===================")


class ZhengzhuangDrugPipeline(object):

    def __init__(self):
        firstRow = ['entity1', 'entity2', 'relation']
        self.f = open(os.path.join(local_url, 'zhengzhuang_drug.csv'), 'w')
        self.writer = csv.writer(self.f)
        self.writer.writerow(firstRow)
        self.itemSet = set()
        self.start = time.time()

    def process_item(self, item, spider):
        entity1 = item['entity1']
        entity2 = item['entity2']
        relation = item['relation']
        i = entity1 + entity2 + relation
        # 去重
        if i not in self.itemSet:
            self.writer.writerow((entity1, entity2, relation))
            self.itemSet.add(i)
        return item

    def open_spider(self, spider):
        print("==================开启爬虫" + spider.name + "===================")

    def close_spider(self, spider):
        self.f.close()
        now = time.time()
        t = int(now - self.start)
        print("总共用时：" + sec2time(t))
        print("==================关闭爬虫" + spider.name + "===================")
