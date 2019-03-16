# -*- coding: utf-8 -*-
import re
from urllib.parse import urlsplit

import scrapy

from ..items import DrugsItem


class DrugsSpider(scrapy.Spider):
    name = 'drugs'
    allowed_domains = ['www.pharmnet.com.cn']
    base_url = 'http://www.pharmnet.com.cn/product/11/1/'
    href = '1.html'
    start_urls = [base_url + href]

    def parse(self, response):
        base_link = response.xpath('//div[@class="list"]')
        links = base_link.xpath('./ul/li/h3/span/a/@href').extract()
        for link in links:
            if urlsplit(link).netloc == 'www.pharmnet.com.cn':
                yield scrapy.Request(link, callback=self.parse_page)
            else:
                yield scrapy.Request(link, callback=self.parse_page1)

        flag = base_link.xpath('./h6/a[@class="fno"]/text()').extract()
        next_link = base_link.xpath('./h6/a[@class="fno"]/@href').extract()
        if len(flag) == 2:
            yield scrapy.Request(self.base_url + next_link[-1], callback=self.parse)
        elif len(flag) == 1 and flag[0] == '下一页':
            yield scrapy.Request(self.base_url + next_link[-1], callback=self.parse)

    def parse_page(self, response):
        base_link = response.xpath('//div[@id="main"]/dl')
        # 药品名称
        title = base_link.xpath('./dt/h1/text()').extract()[0].strip()
        # 图片
        img = base_link.xpath('./dd/div[@class="img"]/a/img/@src').extract()[0].strip()
        分类 = base_link.xpath('./dd/div[@class="text01"]/ul/li[2]/text()').extract()
        if len(分类) != 0:
            分类 = 分类[0].strip()
        else:
            分类 = ""
        分类 = re.sub('/', '##', 分类)
        英文名称 = base_link.xpath('./dd/div[@class="text01"]/ul/li[3]/h3/text()').extract()
        if len(英文名称) != 0:
            英文名称 = 英文名称[0].strip()
        else:
            英文名称 = ""
        批准文号 = base_link.xpath('./dd/div[@class="text01"]/ul/li[4]/h3/text()').extract()
        if len(批准文号) != 0:
            批准文号 = 批准文号[0].strip()
        else:
            批准文号 = ""
        主要规格 = base_link.xpath('./dd/div[@class="text01"]/ul/li[5]/text()').extract()
        if len(主要规格) != 0:
            主要规格 = 主要规格[0].strip()
        else:
            主要规格 = ""
        # 处理‘用途’、‘产品说明’等
        attributes = base_link.xpath('./dd[@class="text03"]//text()').extract()
        strings = ''
        for s in attributes:
            strings += re.sub('\r|\n|\\s', '', s)
        strings = re.findall(u'·(.*?)：([^·]+)', strings, re.S)
        用途 = str()
        产品说明 = str()
        for s in strings:
            if s[0] == '用途':
                用途 = s[1].strip()
            elif s[0] == '产品说明':
                产品说明 = s[1].strip()

        item = DrugsItem()
        item['title'] = title
        item['img'] = img
        item['分类'] = 分类
        item['英文名称'] = 英文名称
        item['批准文号'] = 批准文号
        item['主要规格'] = 主要规格
        item['用途'] = 用途
        item['产品说明'] = 产品说明
        yield item

    def parse_page1(self, response):
        title = response.xpath('//table/tr/td[contains(text(), "产品名称")]/following-sibling::td[1]//text()').extract()[0].strip()
        # print(title)
        img = response.xpath('//table/tr/td[contains(text(), "产品名称")]/following-sibling::td[2]/a/img/@src').extract()[0].strip()
        # print(img)
        分类 = response.xpath('//table/tr/td[contains(text(), "产品分类")]/following-sibling::td[1]//text()').extract()[0].strip()
        分类 = re.sub('/', '##', 分类)
        # print(分类)
        英文名称 = response.xpath('//table/tr/td[contains(text(), "英文名称")]/following-sibling::td[1]//text()').extract()[0].strip()
        # print(英文名称)
        批准文号 = response.xpath('//table/tr/td[contains(text(), "批准文号")]/following-sibling::td[1]//text()').extract()[0].strip()
        # print(批准文号)
        主要规格 = response.xpath('//table/tr/td[contains(text(), "主要规格")]/following-sibling::td[1]//text()').extract()[0].strip()
        # print(主要规格)
        用途s = response.xpath('//table/tr/td[contains(text(), "用途")]/following-sibling::td[1]//text()').extract()
        用途 = ''
        if len(用途s) != 0:
            for i in 用途s:
                用途 += i
        用途 = re.sub('\r\n\\s', '', 用途)
        # print(用途)
        产品说明s = response.xpath('//table/tr/td[contains(text(), "产品说明")]/following-sibling::td[1]//text()').extract()
        产品说明 = ''
        if len(产品说明s) != 0:
            for i in 产品说明s:
                产品说明 += i
        产品说明 = re.sub('\r\n\\s', '', 产品说明)
        # print(产品说明)

        item = DrugsItem()
        item['title'] = title
        item['img'] = img
        item['分类'] = 分类
        item['英文名称'] = 英文名称
        item['批准文号'] = 批准文号
        item['主要规格'] = 主要规格
        item['用途'] = 用途
        item['产品说明'] = 产品说明
        yield item
