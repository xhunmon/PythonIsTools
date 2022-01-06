#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Description: 主要入口
@Date       :2021/08/25
@Author     :xhunmon
@Mail       :xhunmon@gmail.com
"""
from core import utils
from core.conf import Config
from db.db_main import *

EXIT_NUM = 100

if __name__ == '__main__':
    utils.kill_all_v2ray()
    Config.set_v2ray_core_path('/Users/Qincji/Desktop/develop/soft/intalled/v2ray-macos-64')  # v2ray内核存放路径
    Config.set_v2ray_node_path('/Users/Qincji/Desktop/develop/py/project/PythonIsTools')  # 保存获取到节点的路径
    proxy_url = 'vmess://ew0KICAidiI6ICIyIiwNCiAgInBzIjogIkBTU1JTVUItVjUyLeS7mOi0ueaOqOiNkDpzdW8ueXQvc3Nyc3ViIiwNCiAgImFkZCI6ICIxMTIuMzMuMzIuMTM2IiwNCiAgInBvcnQiOiAiMTAwMDMiLA0KICAiaWQiOiAiNjVjYWM1NmQtNDE1NS00M2M4LWJhZTAtZjM2OGNiMjFmNzcxIiwNCiAgImFpZCI6ICIxIiwNCiAgInNjeSI6ICJhdXRvIiwNCiAgIm5ldCI6ICJ0Y3AiLA0KICAidHlwZSI6ICJub25lIiwNCiAgImhvc3QiOiAiMTEyLjMzLjMyLjEzNiIsDQogICJwYXRoIjogIiIsDQogICJ0bHMiOiAiIiwNCiAgInNuaSI6ICIiDQp9'
    dbm = DBManage()
    dbm.init()  # 必须初始化
    if dbm.check_url_single(proxy_url):
        urls = dbm.load_urls_by_net(proxy_url=proxy_url)
        dbm.check_and_save(urls, append=False)
    # print(urls)
    # urls = load_unchecked_urls_by_local()
    # check_and_save(urls, append=False)
    # urls = load_enable_urls_by_local()
    # load_urls_and_save_auto()
    utils.kill_all_v2ray()
