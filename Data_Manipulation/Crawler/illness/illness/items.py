# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JibingItem(scrapy.Item):
    title = scrapy.Field()
    分类 = scrapy.Field()
    简介 = scrapy.Field()
    易感人群 = scrapy.Field()
    传染方式 = scrapy.Field()
    预防 = scrapy.Field()
    饮食保健 = scrapy.Field()


class NeopathyItem(scrapy.Item):
    entity1 = scrapy.Field()
    relation = scrapy.Field()
    entity2 = scrapy.Field()


class SymptomItem(scrapy.Item):
    entity1 = scrapy.Field()
    relation = scrapy.Field()
    entity2 = scrapy.Field()
    症状内容 = scrapy.Field()


class InspectItem(scrapy.Item):
    entity1 = scrapy.Field()
    relation = scrapy.Field()
    entity2 = scrapy.Field()


class DrugItem(scrapy.Item):
    entity1 = scrapy.Field()
    relation = scrapy.Field()
    entity2 = scrapy.Field()
