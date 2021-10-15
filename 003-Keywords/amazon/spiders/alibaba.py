#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Description: 亚马逊相关关键词获取
@Date       :2021/09/24
@Author     :xhunmon
@Mail       :xhunmon@gmail.com
"""
import re
from urllib.parse import quote_plus

import scrapy
from my_fake_useragent import UserAgent


class AlibabaSpider(scrapy.Spider):
    name = 'alibaba'
    allowed_domains = ['alibaba.com']
    results = []
    keywords = []
    headers = {
        'Host': 'www.alibaba.com',
        'User-Agent': UserAgent().random()
    }

    def start_requests(self):
        print('alibaba start_requests')
        """
            start_requests做为程序的入口，可以重写，自定义第一批请求
            
        """
        start_urls = ['https://www.alibaba.com/trade/search?fsb=y&IndexArea=product_en&CatId=&SearchText={k}'.format(
            k=quote_plus(k)) for k in self.keywords]
        # , meta={'proxy': 'socks5h://127.0.0.1:1080/'}
        for url in start_urls:
            yield scrapy.Request(url, headers=self.headers,
                                 callback=self.parse)

    def parse(self, response):
        print('alibaba parse')
        with open('alibaba.html', mode='w') as f:
            f.write(response.text)