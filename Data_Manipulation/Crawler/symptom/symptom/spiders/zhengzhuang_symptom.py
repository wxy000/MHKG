# -*- coding: utf-8 -*-
import scrapy

from ..custom_setting import zhengzhuang_symptom_settings
from ..items import ZhengzhuangSymptomItem


class ZhengzhuangSymptomSpider(scrapy.Spider):

    custom_settings = zhengzhuang_symptom_settings

    name = 'zhengzhuang_symptom'
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

            item = dict()
            item['entity1'] = i

            yield scrapy.Request(self.base_url + url, meta={'item': item}, callback=self.parse_next)

    def parse_next(self, response):
        items = response.meta['item']
        症状s = response.xpath('//ul[@class="about-zzlist clearfix"]/li/a/@title').extract()
        if len(症状s) != 0:
            for i in 症状s:

                item = ZhengzhuangSymptomItem()
                item['entity1'] = items['entity1']
                item['entity2'] = i
                item['relation'] = '相关症状'

                yield item
