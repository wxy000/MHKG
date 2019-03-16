# -*- coding: utf-8 -*-
import re

import scrapy

from ..custom_setting import drug_settings
from ..items import DrugItem


class DrugSpider(scrapy.Spider):
    custom_settings = drug_settings
    name = 'drug'
    allowed_domains = ['jib.xywy.com']
    start_urls = []

    base_url = 'http://jib.xywy.com'

    # 生成字母a-z，并组合为链接
    char = list(map(chr, range(ord('a'), ord('z') + 1)))
    for c in char:
        start_urls.append(base_url + '/html/' + c + '.html')

    def parse(self, response):
        path = response.xpath('//ul[@class="ks-zm-list clearfix mt10"]/li/a/@href').extract()
        for p in path:

            title = response.xpath('//a[@href="' + p + '"]/text()').extract()[0].strip()
            if '...' in title:
                title = '###'
            item = dict()
            item['entity1'] = title

            p = re.sub('/il_sii_', '/il_sii/drug/', p)
            yield scrapy.Request(self.base_url + p, meta={'item': item}, callback=self.parse_drug)

    def parse_drug(self, response):
        items = response.meta['item']
        if items['entity1'] == '###':
            items['entity1'] = response.xpath('//div[@class="jb-name fYaHei gre"]/text()').extract()[0]

        药品s = response.xpath('//a[@class="gre mr10"]/text()').extract()
        if len(药品s) != 0:
            for i in 药品s:

                i = re.sub('\r|\n|\t', '', i)
                flag = re.search(u'\\s', i, re.S)
                if flag is not None:
                    i = re.findall(u'.*\\s(.*)', i, re.S)[0]
                    i = re.findall(u'([^\x00-\xff]+)', i, re.S)[0]
                药品 = i

                item = DrugItem()
                item['entity1'] = items['entity1']
                item['entity2'] = 药品
                item['relation'] = '相关药品'

                yield item
