# -*- coding: utf-8 -*-
import re

import scrapy

from ..custom_setting import jiancha_settings
from ..items import JianchaItem


class JianchaSpider(scrapy.Spider):

    custom_settings = jiancha_settings

    name = 'jiancha'
    allowed_domains = ['jck.xywy.com']
    start_urls = []

    base_url = 'http://jck.xywy.com'

    # 生成字母a-z，并组合为链接
    char = list(map(chr, range(ord('a'), ord('z') + 1)))
    for c in char:
        start_urls.append(base_url + '/' + c + '.html')

    def parse(self, response):
        urls = response.xpath('//ul[@class="clearfix letterli letterlito fYaHei"]/li/a/@href').extract()
        if len(urls) != 0:
            for i in urls:
                title = response.xpath(
                    '//ul[@class="clearfix letterli letterlito fYaHei"]/li/a[contains(@href, "' + i + '")]/@title').extract()[
                    0]

                item = dict()
                item['title'] = title

                yield scrapy.Request(self.base_url + i, meta={'item': item}, callback=self.parse_drug)

    def parse_drug(self, response):
        items = response.meta['item']
        分类s = response.xpath('//div[@class="headings f12 fYaHei gray-a mt10"]//a/text()').extract()
        分类 = ''
        if len(分类s) != 0:
            for i in 分类s:
                分类 += i + "##"
        分类 = re.sub('\r|\n|\\s', '', 分类)
        if '##' == 分类[-2:]:
            分类 = 分类[:-2]
        简介s = response.xpath(
            '//div[@class="baby-weeks"]/p[@class="baby-weeks-infor mt20 t2 lh28 f13 graydeep"]/text()').extract()
        简介 = ''
        if len(简介s) != 0:
            for i in 简介s:
                简介 += i
        简介 = re.sub('\r|\n|\\s', '', 简介)
        # print(简介)
        适用性别s = response.xpath(
            '//div[@class="target-txt pl20 pr20"]/p/span[contains(text(), "适用性别：")]//text()').extract()
        适用性别 = ''
        if len(适用性别s) != 0:
            for i in 适用性别s:
                适用性别 += i
        适用性别 = re.sub('\r|\n|\\s', '', 适用性别)
        适用性别 = 适用性别.split("：")
        # print(适用性别[1])
        是否空腹s = response.xpath(
            '//div[@class="target-txt pl20 pr20"]/p/span[contains(text(), "是否空腹：")]//text()').extract()
        是否空腹 = ''
        if len(是否空腹s) != 0:
            for i in 是否空腹s:
                是否空腹 += i
        是否空腹 = re.sub('\r|\n|\\s', '', 是否空腹)
        是否空腹 = 是否空腹.split("：")
        # print(是否空腹[1])
        温馨提示s = response.xpath('//div[@class="fl blue-a"]//text()').extract()
        温馨提示 = ''
        if len(温馨提示s) != 0:
            for i in 温馨提示s:
                温馨提示 += i
        温馨提示 = re.sub('\r|\n|\\s', '', 温馨提示)
        # print(温馨提示)
        正常值s = response.xpath('//div[@class="target-bt f20 deepgray pl20 mt25 step"][@id="B"][text('
                              ')="正常值"]/following-sibling::div[1]//p//text()').extract()
        正常值 = ''
        if len(正常值s) != 0:
            for i in 正常值s:
                正常值 += i
        正常值 = re.sub('\r|\n|\\s', '', 正常值)
        if 正常值 == '临床意义' or 正常值 == '基本信息' or 正常值 == '注意事项' or \
                正常值 == '检查过程' or 正常值 == '不适宜人群' or 正常值 == '不良反应与风险':
            正常值 = '无'
        # print(正常值)
        检查过程s = response.xpath('//div[@class="target-bt f20 deepgray pl20 mt25 step"][@id="E"][text('
                               ')="检查过程"]/following-sibling::div[1]//p//text()').extract()
        检查过程 = ''
        if len(检查过程s) != 0:
            for i in 检查过程s:
                检查过程 += i
        检查过程 = re.sub('\r|\n|\\s', '', 检查过程)
        if 检查过程 == '临床意义' or 检查过程 == '基本信息' or 检查过程 == '注意事项' or \
                检查过程 == '正常值' or 检查过程 == '不适宜人群' or 检查过程 == '不良反应与风险':
            检查过程 = '无'
        # print(检查过程)
        不适宜人群s = response.xpath('//div[@class="target-bt f20 deepgray pl20 mt25 step"][@id="F"][text('
                                ')="不适宜人群"]/following-sibling::div[1]//p//text()').extract()
        不适宜人群 = ''
        if len(不适宜人群s) != 0:
            for i in 不适宜人群s:
                不适宜人群 += i
        不适宜人群 = re.sub('\r|\n|\\s', '', 不适宜人群)
        if 不适宜人群 == '临床意义' or 不适宜人群 == '基本信息' or 不适宜人群 == '注意事项' or \
                不适宜人群 == '正常值' or 不适宜人群 == '检查过程' or 不适宜人群 == '不良反应与风险':
            不适宜人群 = '无'
        # print(不适宜人群)
        不良反应与风险s = response.xpath('//div[@class="target-bt f20 deepgray pl20 mt25 step"][@id="G"][text('
                                  ')="不良反应与风险"]/following-sibling::div[1]//p//text()').extract()
        不良反应与风险 = ''
        if len(不良反应与风险s) != 0:
            for i in 不良反应与风险s:
                不良反应与风险 += i
        不良反应与风险 = re.sub('\r|\n|\\s', '', 不良反应与风险)
        if 不良反应与风险 == '临床意义' or 不良反应与风险 == '基本信息' or 不良反应与风险 == '注意事项' or \
                不良反应与风险 == '正常值' or 不良反应与风险 == '检查过程' or 不良反应与风险 == '不适宜人群':
            不良反应与风险 = '无'
        # print(不良反应与风险)

        item = JianchaItem()
        item['title'] = items['title']
        item['分类'] = 分类
        item['简介'] = 简介
        item['适用性别'] = 适用性别[1]
        item['是否空腹'] = 是否空腹[1]
        item['温馨提示'] = 温馨提示
        item['正常值'] = 正常值
        item['检查过程'] = 检查过程
        item['不适宜人群'] = 不适宜人群
        item['不良反应与风险'] = 不良反应与风险

        return item
