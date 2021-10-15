#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Description: 通过框架自带命令 启动命令脚本
@Date       :2021/09/20
@Author     :xhunmon
@Mail       :xhunmon@gmail.com
"""
from scrapy.crawler import CrawlerProcess
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings

from amazon.spiders.alibaba import AlibabaSpider
from amazon.spiders.amazon import AmazonSpider
from amazon.spiders.checkip import CheckIpSpider

settings = get_project_settings()
configure_logging(settings)
crawler = CrawlerProcess(settings)


def check_ip():
    spider = CheckIpSpider
    crawler.crawl(spider)
    crawler.start()
    return spider.ips


def crawl_amazon(keywords: []):
    spider = AmazonSpider
    spider.keywords = keywords
    crawler.crawl(spider)
    crawler.start()
    return spider.results


def crawl_alibaba(keywords: []):
    spider = AlibabaSpider
    spider.keywords = keywords
    crawler.crawl(spider)
    crawler.start()
