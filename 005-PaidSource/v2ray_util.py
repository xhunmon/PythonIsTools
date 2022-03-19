#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Description: 管理v2ray_pool的工具
@Date       :2022/1/14
@Author     :xhunmon
@Mail       :xhunmon@gmail.com
"""

import time

from v2ray_pool import utils, Config, DBManage


def search_node():
    # 如果有系统全局代理，可不需要开启v2ray_core代理，GoogleTrend(proxies=False)
    utils.kill_all_v2ray()
    Config.set_v2ray_core_path('/Users/Qincji/Desktop/develop/soft/intalled/v2ray-macos-64')  # v2ray内核存放路径
    Config.set_v2ray_node_path(
        '/Users/Qincji/Desktop/develop/py/project/PythonIsTools/005-PaidSource/v2ray_pool')  # 保存获取到节点的路径
    proxy_url = 'ss://YWVzLTI1Ni1nY206WTZSOXBBdHZ4eHptR0M@134.195.196.3:3306#github.com/freefq%20-%20%E5%8C%97%E7%BE%8E%E5%9C%B0%E5%8C%BA%20%201'
    dbm = DBManage()
    dbm.init()  # 必须初始化
    if dbm.check_url_single(proxy_url):
        urls = dbm.load_urls_by_net(proxy_url=proxy_url)
        dbm.check_and_save(urls, append=False)
    # dbm.load_urls_and_save_auto()
    # urls = dbm.load_unchecked_urls_by_local()
    # dbm.check_and_save(urls, append=False)
    utils.kill_all_v2ray()


def restart_v2ray(isSysOn=False):
    utils.kill_all_v2ray()
    Config.set_v2ray_core_path('/Users/Qincji/Desktop/develop/soft/intalled/v2ray-macos-64')  # v2ray内核存放路径
    Config.set_v2ray_node_path(
        '/Users/Qincji/Desktop/develop/py/project/PythonIsTools/005-PaidSource/v2ray_pool')  # 保存获取到节点的路径
    dbm = DBManage()
    dbm.init()  # 必须初始化
    while 1:
        if dbm.start_random_v2ray_by_local(isSysOn=isSysOn):
            break
        else:
            print("启动失败，进行重试！")
            time.sleep(1)


def kill_all_v2ray():
    utils.kill_all_v2ray()
