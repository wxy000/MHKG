# -*- coding: utf-8 -*-
import re

import scrapy

from ..custom_setting import jibing_settings
from ..items import JibingItem


class JibingSpider(scrapy.Spider):

    # 加载配置
    custom_settings = jibing_settings

    name = 'jibing'
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
            item = JibingItem()
            item['title'] = title

            p = re.sub('/il_sii_', '/il_sii/gaishu/', p)
            yield scrapy.Request(self.base_url + p, meta={'item': item}, callback=self.parse_gaishu)

    def parse_gaishu(self, response):
        item = response.meta['item']
        if item['title'] == '###':
            item['title'] = response.xpath('//div[@class="jb-name fYaHei gre"]/text()').extract()[0]
        分类s = response.xpath('//div[@class="wrap mt10 nav-bar"]//a/text()').extract()
        分类 = ''
        if len(分类s) != 0:
            for i in 分类s:
                分类 += i + "##"
        分类 = re.sub('\r|\n|\\s', '', 分类)
        if '##' == 分类[-2:]:
            分类 = 分类[:-2]
        path = response.xpath('//div[@class="jib-articl fr f14 "]')
        简介 = path.xpath('./div[@class="jib-articl-con jib-lh-articl"]/p/text()').extract()[0]
        简介 = re.sub('\r|\n|\\s', '', 简介)
        # print(简介)
        易感人群s = path.xpath('./div[@class="mt20 articl-know"]/p/span[contains(text(), "易感人群：")]/../span[@class="fl '
                           'txt-right"]/text()').extract()
        易感人群 = ''
        if len(易感人群s) != 0:
            for i in 易感人群s:
                易感人群 += i
        易感人群 = re.sub('\r|\n|\\s', '', 易感人群)
        # print(易感人群)
        传染方式s = path.xpath('./div[@class="mt20 articl-know"]/p/span[contains(text(), "传染方式：")]/../span[@class="fl '
                           'txt-right"]/text()').extract()
        传染方式 = ''
        if len(传染方式s) != 0:
            for i in 传染方式s:
                传染方式 += i
        传染方式 = re.sub('\r|\n|\\s', '', 传染方式)
        # print(传染方式)

        item['分类'] = 分类
        item['简介'] = 简介
        item['易感人群'] = 易感人群
        item['传染方式'] = 传染方式

        p = re.sub('/il_sii/gaishu/', '/il_sii/prevent/', response.url)
        yield scrapy.Request(p, meta={'item': item}, callback=self.parse_prevent)

    def parse_prevent(self, response):
        item = response.meta['item']
        预防s = response.xpath('//div[@class="jib-articl fr f14 jib-lh-articl"]/p//text()').extract()
        预防 = ''
        if len(预防s) != 0:
            for i in 预防s:
                预防 += i
        预防 = re.sub('\r|\n|\\s', '', 预防)
        # print(预防)

        item['预防'] = 预防

        p = re.sub('/il_sii/prevent/', '/il_sii/food/', response.url)
        yield scrapy.Request(p, meta={'item': item}, callback=self.parse_food)

    def parse_food(self, response):
        item = response.meta['item']
        饮食保健s = response.xpath('//div[@class="diet-item"]/p//text()').extract()
        饮食保健 = ''
        if len(饮食保健s) != 0:
            for i in 饮食保健s:
                饮食保健 += i
        饮食保健 = re.sub('\r|\n|\\s', '', 饮食保健)
        # print(饮食保健)

        item['饮食保健'] = 饮食保健

        return item
