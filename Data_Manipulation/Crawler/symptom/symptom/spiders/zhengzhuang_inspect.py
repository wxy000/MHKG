# -*- coding: utf-8 -*-
import re

import scrapy

from ..custom_setting import zhengzhuang_inspect_settings
from ..items import ZhengzhuangInspectItem


class ZhengzhuangInspectSpider(scrapy.Spider):

    custom_settings = zhengzhuang_inspect_settings

    name = 'zhengzhuang_inspect'
    allowed_domains = ['zzk.xywy.com']
    start_urls = []

    base_url = 'http://zzk.xywy.com'

    # 生成字母a-z，并组合为链接
    char = list(map(chr, range(ord('a'), ord('z') + 1)))
    for c in char:
        start_urls.append(base_url + '/p/' + c + '.html')

    def parse(self, response):
        title = response.xpath('//ul[contains(@class, "ks-zm-list clearfix")]/li/a/@title').extract()
        for i in title:
            url = response.xpath('//ul[contains(@class, "ks-zm-list clearfix")]/li/a[@title="' + i + '"]/@href').extract()[0]
            url = re.sub('_gaishu', '_jiancha', url)

            item = dict()
            item['entity1'] = i

            yield scrapy.Request(self.base_url + url, meta={'item': item}, callback=self.parse_next)

    def parse_next(self, response):
        items = response.meta['item']
        检查s = response.xpath('//p[@class="f12 mt5"]/a/text()').extract()
        if len(检查s) != 0:
            for i in 检查s:

                item = ZhengzhuangInspectItem()
                item['entity1'] = items['entity1']
                item['entity2'] = i
                item['relation'] = '相关检查'

                yield item
