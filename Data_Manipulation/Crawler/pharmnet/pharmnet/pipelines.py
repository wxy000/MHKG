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


class DrugsPipeline(object):

    def __init__(self):
        firstRow = ['title', 'img', '英文名称', '批准文号', '主要规格', '用途', '产品说明']
        self.f = open(os.path.join(local_url, 'drugs.csv'), 'w')
        self.fd = open(os.path.join(local_url, 'drugs.json'), 'w')
        self.writer = csv.writer(self.f)
        self.writer.writerow(firstRow)
        self.itemSet = set()
        self.start = time.time()

    def process_item(self, item, spider):
        title = item['title']
        img = item['img']
        英文名称 = item['英文名称']
        批准文号 = item['批准文号']
        主要规格 = item['主要规格']
        用途 = item['用途']
        产品说明 = item['产品说明']
        # 去重
        if title not in self.itemSet:
            self.writer.writerow((title, img, 英文名称, 批准文号, 主要规格, 用途, 产品说明))

            entityItem = copy.deepcopy(item)
            entityItem.pop("title")
            entityItem.pop("img")
            entityItem.pop("英文名称")
            entityItem.pop("批准文号")
            entityItem.pop("主要规格")
            entityItem.pop("用途")
            entityItem.pop("产品说明")
            entityItem['分类'] = entityItem['分类'] + '##' + item['title']
            line = json.dumps(dict(entityItem), ensure_ascii=False) + '\n'
            self.fd.write(line)

            self.itemSet.add(title)
        return item

    def open_spider(self, spider):
        print("==================开启爬虫" + spider.name + "===================")

    def close_spider(self, spider):
        self.f.close()
        self.fd.close()
        now = time.time()
        t = int(now - self.start)
        print("总共用时：" + sec2time(t))
        print("==================关闭爬虫" + spider.name + "===================")
