# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JianchaItem(scrapy.Item):
    title = scrapy.Field()
    分类 = scrapy.Field()
    简介 = scrapy.Field()
    适用性别 = scrapy.Field()
    是否空腹 = scrapy.Field()
    温馨提示 = scrapy.Field()
    正常值 = scrapy.Field()
    检查过程 = scrapy.Field()
    不适宜人群 = scrapy.Field()
    不良反应与风险 = scrapy.Field()
