# -*- coding: utf-8 -*-
import re

import scrapy

from ..custom_setting import inspect_settings
from ..items import InspectItem


class InspectSpider(scrapy.Spider):
    custom_settings = inspect_settings

    name = 'inspect'
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

            p = re.sub('/il_sii_', '/il_sii/inspect/', p)
            yield scrapy.Request(self.base_url + p, meta={'item': item}, callback=self.parse_inspect)

    def parse_inspect(self, response):
        items = response.meta['item']
        if items['entity1'] == '###':
            items['entity1'] = response.xpath('//div[@class="jb-name fYaHei gre"]/text()').extract()[0]
        # print(title)
        检查项目s = response.xpath('//div[@class="more-zk pr"]//ul[@class="clearfix jib-check "]/li['
                               '@class="check-item"]/a/@href').extract()

        if len(检查项目s) != 0:
            for j in 检查项目s:

                title = response.xpath('//ul[@class="clearfix jib-check "]/li[@class="check-item"]/a[@href="' + j + '"]/text()').extract()[0].strip()
                if '...' in title:
                    title = '###'

                item = InspectItem()
                item['entity1'] = items['entity1']
                item['entity2'] = title
                item['relation'] = '相关检查'

                yield scrapy.Request(j, meta={'item': item}, callback=self.parse_next, dont_filter=True)

    def parse_next(self, response):
        item = response.meta['item']
        if item['entity2'] == '###':
            item['entity2'] = response.xpath('//div[@class="baby-weeks"]/div[@class="clearfix"]/strong/text()').extract()[0]
        return item
