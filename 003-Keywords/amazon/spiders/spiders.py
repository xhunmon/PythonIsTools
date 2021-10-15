#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Description: 爬虫页面集合
@Date       :2021/09/26
@Author     :xhunmon
@Mail       :xhunmon@gmail.com
"""
import re
from urllib.parse import quote_plus

import scrapy
from my_fake_useragent import UserAgent


class CheckIpSpider(scrapy.Spider):
    """
    检查当前代理ip信息
    """
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


class AmazonSpider(scrapy.Spider):
    """
    https://www.amazon.com/s?k=？？
    亚马逊页面获取搜索词相关：
    """
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


class EtsySpider(scrapy.Spider):
    """需要连接外网
    https://www.etsy.com/market/
    """
    name = 'etsy'
    allowed_domains = ['etsy.com']
    results = []
    keywords = []
    headers = {
        'User-Agent': UserAgent().random()
    }

    def start_requests(self):
        print('etsy start_requests')
        """
            start_requests做为程序的入口，可以重写，自定义第一批请求
        """
        start_urls = ['https://www.etsy.com/market/{k}'.format(k=quote_plus(k)) for k in self.keywords]
        # , meta={'proxy': 'socks5h://127.0.0.1:1080/'}
        for url in start_urls:
            yield scrapy.Request(url, headers=self.headers,
                                 callback=self.parse)

    def parse(self, response):
        print('etsy parse')
        with open('etsy.html', mode='w') as f:
            f.write(response.text)
            f.close()
        temps = re.findall(r'<span class="a-size-base a-color-base s-line-clamp-2">(.+?)</span>', response.text,
                           re.DOTALL)
        deal = [x.replace('\n', '').strip() for x in temps]
        print(deal)
        self.results += deal


class LakesideSpider(scrapy.Spider):
    """一个商城网站
    https://www.lakeside.com/browse/Clothing-Accessories
    """
    name = 'lakeside'
    allowed_domains = ['lakeside.com']
    results = []
    keywords = []
    headers = {
        'User-Agent': UserAgent().random()
    }

    def start_requests(self):
        print('lakeside start_requests')
        """
            start_requests做为程序的入口，可以重写，自定义第一批请求
        """
        start_urls = ['https://www.lakeside.com/browse/{k}'.format(k=quote_plus(k)) for k in self.keywords]
        # , meta={'proxy': 'socks5h://127.0.0.1:1080/'}
        for url in start_urls:
            yield scrapy.Request(url, headers=self.headers,
                                 callback=self.parse)

    def parse(self, response):
        print('lakeside parse')
        with open('lakeside.html', mode='w') as f:
            f.write(response.text)
            f.close()
        # temps = re.findall(r'<span class="a-size-base a-color-base s-line-clamp-2">(.+?)</span>', response.text,
        #                    re.DOTALL)
        # deal = [x.replace('\n', '').strip() for x in temps]
        # print(deal)
        # self.results += deal


class WordtrackerSpider(scrapy.Spider):
    """
    https://www.wordtracker.com/search?query=food%20bags
    """
    name = 'wordtracker'
    allowed_domains = ['wordtracker.com']
    results = []
    keywords = []
    headers = {
        'User-Agent': UserAgent().random()
    }

    def start_requests(self):
        print('wordtracker start_requests')
        """
            start_requests做为程序的入口，可以重写，自定义第一批请求
        """
        start_urls = ['https://www.wordtracker.com/search?query={k}'.format(k=quote_plus(k)) for k in self.keywords]
        # , meta={'proxy': 'socks5h://127.0.0.1:1080/'}
        for url in start_urls:
            yield scrapy.Request(url, headers=self.headers,
                                 callback=self.parse)

    def parse(self, response):
        print('wordtracker parse')
        with open('wordtracker.html', mode='w') as f:
            f.write(response.text)
            f.close()
        temps = re.findall(r'<span class="a-size-base a-color-base s-line-clamp-2">(.+?)</span>', response.text,
                           re.DOTALL)
        deal = [x.replace('\n', '').strip() for x in temps]
        print(deal)
        self.results += deal
