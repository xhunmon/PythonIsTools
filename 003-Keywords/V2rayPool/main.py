#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Description: 主要入口
@Date       :2021/08/25
@Author     :xhunmon
@Mail       :xhunmon@gmail.com
"""
from core.conf import Config
from db.db_main import *

EXIT_NUM = 100

if __name__ == '__main__':
    Config.set_v2ray_core_path('xxx/Downloads/v2ray-macos-64')
    url = 'ss://YWVzLTI1Ni1nY206WXlDQmVEZFlYNGNhZEhwQ2trbWRKTHE4@37.120.144.211:43893#github.com/freefq%20-%20%E7%BD%97%E9%A9%AC%E5%B0%BC%E4%BA%9A%20%2041'
    if check_url_single(url):
        urls = load_urls_by_net(proxy_url=url)
        check_and_save(urls, append=False)
    # print(urls)
    # urls = load_unchecked_urls_by_local()
    # urls = load_enable_urls_by_local()
    # load_urls_and_save_auto()
