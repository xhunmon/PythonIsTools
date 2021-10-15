#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Description: 关键词获取
@Date       :2021/09/22
@Author     :xhunmon
@Mail       :xhunmon@gmail.com
"""
# from amazon import run_api
import time

import run_api
from V2rayPool.core import utils
from V2rayPool.core.conf import Config
from V2rayPool.db import db_main
from google import GoogleTrend

if __name__ == "__main__":
    #如果有系统全局代理，可不需要开启v2ray_core代理，GoogleTrend(proxies=False)
    utils.kill_all_v2ray()
    Config.set_v2ray_core_path('/Users/Qincji/Desktop/develop/soft/intalled/v2ray-macos-64')
    if not db_main.start_random_v2ray_by_local():
        raise Exception('启动代理失败')
    # 获取amazon中相关词，代理需要看：middlewares.py，
    # results = run_api.crawl_amazon(['plastic packaging', ])
    #把通过google trends查出关键词相关词，以及其词的趋势图，如：
    GoogleTrend().search('women ring', 'women-ring', proxies=True, timeframe='2019-10-01 2021-10-11')
    utils.kill_all_v2ray()
