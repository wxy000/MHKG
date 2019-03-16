# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZhengzhuangItem(scrapy.Item):
    title = scrapy.Field()
    分类 = scrapy.Field()
    介绍 = scrapy.Field()
    预防 = scrapy.Field()
    食疗 = scrapy.Field()


class ZhengzhuangSymptomItem(scrapy.Item):
    entity1 = scrapy.Field()
    entity2 = scrapy.Field()
    relation = scrapy.Field()


class ZhengzhuangInspectItem(scrapy.Item):
    entity1 = scrapy.Field()
    entity2 = scrapy.Field()
    relation = scrapy.Field()


class ZhengzhuangDrugItem(scrapy.Item):
    entity1 = scrapy.Field()
    entity2 = scrapy.Field()
    relation = scrapy.Field()
