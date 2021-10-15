#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Description: 检查当前代理是否起作用
@Date       :2021/09/24
@Author     :xhunmon
@Mail       :xhunmon@gmail.com
"""
import re

import scrapy
from my_fake_useragent import UserAgent


class CheckIpSpider(scrapy.Spider):
    name = 'ip138'
    allowed_domains = ['ip138.com']
    ips = None
    headers = {
        'User-Agent': UserAgent().random()
    }

    def start_requests(self):
        print('CheckIpSpider start_requests')
        """
            start_requests做为程序的入口，可以重写，自定义第一批请求
        """
        start_urls = ['https://2021.ip138.com']
        # , meta={'proxy': 'socks5h://127.0.0.1:1080/'}
        for url in start_urls:
            yield scrapy.Request(url, headers=self.headers,
                                 callback=self.parse)

    def parse(self, response):
        print('CheckIpSpider parse')
        results = re.findall(r'\[<a.+?>(.+?)</a>.+?：(.+?)\n</p>', response.text, re.DOTALL)
        print(results)
        self.ips = results
