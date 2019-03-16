# -*- coding: utf-8 -*-
import re

import scrapy

from ..custom_setting import zhengzhuang_settings
from ..items import ZhengzhuangItem


class ZhengzhuangSpider(scrapy.Spider):
    custom_settings = zhengzhuang_settings

    name = 'zhengzhuang'
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
            url = re.sub('_gaishu', '_jieshao', url)

            item = ZhengzhuangItem()
            item['title'] = i

            yield scrapy.Request(self.base_url + url, meta={'item': item}, callback=self.parse_jieshao)

    def parse_jieshao(self, response):
        item = response.meta['item']

        分类s = response.xpath('//div[@class="wrap mt10 nav-bar"]//a/text()').extract()
        分类 = ''
        if len(分类s) != 0:
            for i in 分类s:
                分类 += i + "##"
        分类 = re.sub('\r|\n|\\s', '', 分类)
        if '##' == 分类[-2:]:
            分类 = 分类[:-2]

        介绍s = response.xpath('//div[@class="zz-articl fr f14"]/p//text()').extract()
        介绍 = ''
        if len(介绍s) != 0:
            for i in 介绍s:
                介绍 += i
        介绍 = re.sub('\r|\n|\\s', '', 介绍)

        item['分类'] = 分类
        item['介绍'] = 介绍

        url = re.sub('_jieshao', '_yufang', response.url)
        yield scrapy.Request(url, meta={'item': item}, callback=self.parse_yufang)

    def parse_yufang(self, response):
        item = response.meta['item']
        预防s = response.xpath('//div[@class="zz-articl fr f14"]/p//text()').extract()
        预防 = ''
        if len(预防s) != 0:
            for i in 预防s:
                预防 += i
        预防 = re.sub('\r|\n|\\s', '', 预防)

        item['预防'] = 预防

        url = re.sub('_yufang', '_food', response.url)
        yield scrapy.Request(url, meta={'item': item}, callback=self.parse_food)

    def parse_food(self, response):
        item = response.meta['item']

        食疗 = ''

        宜s = response.xpath('//div[@class="diet-good clearfix"]/div[@class="fl diet-good-tit mr5 mt5"]/text()').extract()
        宜 = ''
        if len(宜s) != 0:
            for i in 宜s:
                宜 += i
        宜 = '##' + re.sub('\r|\n|\\s', '', 宜) + '##'

        if 宜 != '':
            宜内容s = response.xpath('//div[@class="diet-good clearfix"]/div[contains(text(), "宜")]/../p/text()').extract()
            宜内容 = ''
            if len(宜内容s) != 0:
                for i in 宜内容s:
                    宜内容 += i
            宜内容 = re.sub('\r|\n|\\s', '', 宜内容)

            食疗 += 宜 + 宜内容

        忌s = response.xpath(
            '//div[@class="diet-bad clearfix"]/div[@class="fl diet-good-tit mr5 mt5"]/text()').extract()
        忌 = ''
        if len(忌s) != 0:
            for i in 忌s:
                忌 += i
        忌 = '##' + re.sub('\r|\n|\\s', '', 忌) + '##'

        if 忌 != '':
            忌内容s = response.xpath('//div[@class="diet-bad clearfix"]/div[contains(text(), "忌")]/../p/text()').extract()
            忌内容 = ''
            if len(忌内容s) != 0:
                for i in 忌内容s:
                    忌内容 += i
            忌内容 = re.sub('\r|\n|\\s', '', 忌内容)

            食疗 += 忌 + 忌内容

        item['食疗'] = 食疗

        return item
