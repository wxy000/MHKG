# -*- coding: utf-8 -*-
import re

import scrapy

from ..custom_setting import zhengzhuang_drug_settings
from ..items import ZhengzhuangDrugItem


class ZhengzhuangDrugSpider(scrapy.Spider):

    custom_settings = zhengzhuang_drug_settings

    name = 'zhengzhuang_drug'
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
            url = re.sub('_gaishu', '_yao', url)

            item = dict()
            item['entity1'] = i

            yield scrapy.Request(self.base_url + url, meta={'item': item}, callback=self.parse_next)

    def parse_next(self, response):
        items = response.meta['item']
        药品s = response.xpath('//a[@class="gre mr10"]/text()').extract()
        if len(药品s) != 0:
            for i in 药品s:

                i = re.sub('\r|\n|\t', '', i)
                flag = re.search(u'\\s', i, re.S)
                if flag is not None:
                    i = re.findall(u'.*\\s(.*)', i, re.S)[0]
                    i = re.findall(u'([^\x00-\xff]+)', i, re.S)[0]
                药品 = i

                item = ZhengzhuangDrugItem()
                item['entity1'] = items['entity1']
                item['entity2'] = 药品
                item['relation'] = '相关药品'

                yield item
