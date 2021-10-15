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
    Config.set_v2ray_core_path('/Users/Qincji/Desktop/develop/soft/intalled/v2ray-macos-64')
    url = 'vmess://ewogICJ2IjogIjIiLAogICJwcyI6ICIiLAogICJhZGQiOiAiNDUuNzkuMjEwLjE0MSIsCiAgInBvcnQiOiA1MDcyNCwKICAiaWQiOiAiNDMzNWYzZDUtODI0Mi00NTJlLWY2YjQtNmI5YTVmZDlmMzg1IiwKICAiYWlkIjogMCwKICAibmV0IjogInRjcCIsCiAgInR5cGUiOiAibm9uZSIsCiAgImhvc3QiOiAiIiwKICAicGF0aCI6ICIiLAogICJ0bHMiOiAibm9uZSIKfQ=='
    if check_url_single(url):
        urls = load_urls_by_net(proxy_url=url)
        check_and_save(urls, append=False)
    # print(urls)
    # urls = load_unchecked_urls_by_local()
    # check_and_save(urls, append=False)
    # urls = load_enable_urls_by_local()
    # load_urls_and_save_auto()
