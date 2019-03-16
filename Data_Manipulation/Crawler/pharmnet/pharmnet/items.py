# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DrugsItem(scrapy.Item):
    title = scrapy.Field()
    img = scrapy.Field()
    分类 = scrapy.Field()
    英文名称 = scrapy.Field()
    批准文号 = scrapy.Field()
    主要规格 = scrapy.Field()
    用途 = scrapy.Field()
    产品说明 = scrapy.Field()
