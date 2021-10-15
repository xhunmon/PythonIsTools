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


class AmazonSpider(scrapy.Spider):
    name = 'amazon'
    allowed_domains = ['amazon.com']
    results = []
    keywords = []
    headers = {
        'Host': 'www.amazon.com',
        'User-Agent': UserAgent().random()
    }

    def start_requests(self):
        print('amazon start_requests')
        """
            start_requests做为程序的入口，可以重写，自定义第一批请求
        """
        start_urls = ['https://www.amazon.com/s?k={k}'.format(k=quote_plus(k)) for k in self.keywords]
        # , meta={'proxy': 'socks5h://127.0.0.1:1080/'}
        for url in start_urls:
            yield scrapy.Request(url, headers=self.headers,
                                 callback=self.parse)

    def parse(self, response):
        print('amazon parse')
        temps = re.findall(r'<span class="a-size-base a-color-base s-line-clamp-2">(.+?)</span>', response.text,
                           re.DOTALL)
        deal = [x.replace('\n', '').strip() for x in temps]
        print(deal)
        self.results += deal
