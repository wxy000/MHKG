# -*- coding: utf-8 -*-
import re

import scrapy

from ..items import SymptomItem
from ..custom_setting import symptom_settings


class SymptomSpider(scrapy.Spider):
    custom_settings = symptom_settings

    name = 'symptom'
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

            p = re.sub('/il_sii_', '/il_sii/symptom/', p)
            yield scrapy.Request(self.base_url + p, meta={'item': item}, callback=self.parse_symptom)

    def parse_symptom(self, response):
        items = response.meta['item']
        if items['entity1'] == '###':
            items['entity1'] = response.xpath('//div[@class="jb-name fYaHei gre"]/text()').extract()[0]
        # print(title)
        已知症状s = response.xpath('//span[@class="db f12 lh240 mb15 "]/a/@href').extract()

        症状内容s = response.xpath('//div[@class="jib-articl fr f14 jib-lh-articl"]/p//text()').extract()
        症状内容 = ''
        if len(症状内容s) != 0:
            for i in 症状内容s:
                症状内容 += i
        症状内容 = re.sub('\r|\n|\\s', '', 症状内容)

        if len(已知症状s) != 0:
            for j in 已知症状s:

                title = response.xpath('//span[@class="db f12 lh240 mb15 "]/a[@href="' + j + '"]/text()').extract()[0].strip()
                if '...' in title:
                    title = '###'

                item = SymptomItem()
                item['entity1'] = items['entity1']
                item['entity2'] = title
                item['relation'] = '相关症状'
                item['症状内容'] = 症状内容

                yield scrapy.Request(j, meta={'item': item}, callback=self.parse_next, dont_filter=True)

    def parse_next(self, response):
        item = response.meta['item']
        if item['entity2'] == '###':
            item['entity2'] = response.xpath('//div[@class="jb-name fYaHei gre"]/text()').extract()[0]
        return item
