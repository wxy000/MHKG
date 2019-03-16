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


class JibingPipeline(object):

    def __init__(self):
        firstRow = ['title', '简介', '易感人群', '传染方式', '预防', '饮食保健']
        self.f = open(os.path.join(local_url, 'jibing.csv'), 'w')
        self.fj = open(os.path.join(local_url, 'jibing.json'), 'w')
        self.writer = csv.writer(self.f)
        self.writer.writerow(firstRow)
        self.itemSet = set()
        self.start = time.time()

    def process_item(self, item, spider):
        self.writer.writerow((item['title'], item['简介'], item['易感人群'], item['传染方式'], item['预防'], item['饮食保健']))
        if item['title'] not in self.itemSet:
            entityItem = copy.deepcopy(item)
            entityItem.pop("title")
            entityItem.pop("简介")
            entityItem.pop("易感人群")
            entityItem.pop("传染方式")
            entityItem.pop("预防")
            entityItem.pop("饮食保健")
            line = json.dumps(dict(entityItem), ensure_ascii=False) + '\n'
            self.fj.write(line)
            self.itemSet.add(item['title'])
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


class NeopathyPipeline(object):

    def __init__(self):
        self.f = open(os.path.join(local_url, 'jibing_neopathy.json'), 'w')
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


class SymptomPipeline(object):

    def __init__(self):
        firstRow = ['entity1', 'entity2', 'relation']
        self.fc = open(os.path.join(local_url, 'jibing_symptom.csv'), 'w')
        self.fj = open(os.path.join(local_url, 'jibing_symptom.json'), 'w')
        self.writer = csv.writer(self.fc)
        self.writer.writerow(firstRow)
        self.itemSet = set()
        self.start = time.time()

    def process_item(self, item, spider):
        self.writer.writerow((item['entity1'], item['entity2'], item['relation']))
        if item['entity1'] not in self.itemSet:
            entityItem = copy.deepcopy(item)
            entityItem.pop("entity2")
            entityItem.pop("relation")
            line = json.dumps(dict(entityItem), ensure_ascii=False) + '\n'
            self.fj.write(line)
            self.itemSet.add(item['entity1'])
        return item

    def open_spider(self, spider):
        print("==================开启爬虫" + spider.name + "===================")

    def close_spider(self, spider):
        self.fc.close()
        self.fj.close()
        now = time.time()
        t = int(now - self.start)
        print("总共用时：" + sec2time(t))
        print("==================关闭爬虫" + spider.name + "===================")


class InspectPipeline(object):

    def __init__(self):
        firstRow = ['entity1', 'entity2', 'relation']
        self.f = open(os.path.join(local_url, 'jibing_inspect.csv'), 'w')
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


class DrugPipeline(object):

    def __init__(self):
        firstRow = ['entity1', 'entity2', 'relation']
        self.f = open(os.path.join(local_url, 'jibing_drug.csv'), 'w')
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
