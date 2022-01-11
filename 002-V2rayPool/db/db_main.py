#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Description: 数据相关接口封装
@Date       :2021/08/30
@Author     :xhunmon
@Mail       :xhunmon@gmail.com
"""
import random

from core import client
from db.local import DbLocal, DbEnable
from db.net import *


class DBManage(object):
    def init(self):
        self.dbLocal = DbLocal()
        self.check = PYCheck()
        self.dbEnable = DbEnable().get()

    def __add_urls_de_dup(self, all_urls: [], new_urls: []) -> []:
        """合并数组，并且去重，去空"""
        if not new_urls:  # 为 [] 或者 None
            return all_urls
        for url in new_urls:
            temp = url.strip().replace('\n', '')
            if temp in all_urls or len(temp) < 20:
                continue
            all_urls.append(temp)

    def start_random_v2ray_by_local(self, isSysOn=False):
        """从本地随机启动一个可用的proxy"""
        urls = self.load_enable_urls_by_local()
        for url in urls:
            if client.Creator().v2ray_start_with_log(random.choice(urls),isSysOn) is False:
                time.sleep(1)
                continue
            time.sleep(2)
            ips = PYCheck().get_curren_ip()
            if not ips:
                print('无效地址：%s' % url)
                continue
            print('代理开启成功')
            time.sleep(1)
            return True
        return False

    def load_urls_and_save_auto(self):
        """首先通过不需要代理的网页获取节点，当代理有可用时，开启代理，获取需要代理获取的网页"""
        self.dbLocal.clear_local()
        all_urls = self.load_urls_by_not_proxy()
        proxy_url = None
        for url in all_urls:
            if client.Creator().v2ray_start_with_log(url) is False:
                time.sleep(1)
                continue
            time.sleep(2)
            ips = PYCheck().get_curren_ip()
            if not ips:
                print('无效地址：%s' % url)
                continue
            proxy_url = url
            break
        if proxy_url is None:
            raise Exception("无代理可用，退出！")
        print("获得可用代理地址：%s" % proxy_url)
        proxy_urls = self.load_urls_by_net_with_proxy(proxy_url=proxy_url)
        all_urls = all_urls + proxy_urls
        self.check_and_save(all_urls, append=False)

    def load_urls_by_not_proxy(self, save_local=True):
        all_urls = []
        # 1. 先把不需要代理的先请求下来
        self.__add_urls_de_dup(all_urls, PNSsfree().get_urls())
        print("获取https://view.ssfree.ru/后数目：%d" % len(all_urls))
        self.__add_urls_de_dup(all_urls, PNFreevpnX().get_urls())
        print("获取https://freevpn-x.com/后数目：%d" % len(all_urls))
        self.__add_urls_de_dup(all_urls, PNGithubIwxf().get_urls())
        print("获取https://github.com/iwxf/free-v2ray/blob/master/README.md 后数目：%d" % len(all_urls))
        self.__add_urls_de_dup(all_urls, PNFreeV2ray().get_urls())
        print("获取https://view.freev2ray.org/ 后数目：%d" % len(all_urls))
        if save_local:  # 保存到本地
            self.dbLocal.save_urls(all_urls)
        return all_urls

    def load_urls_by_net_with_proxy(self, proxy_url=None, save_local=True):
        all_urls = []
        if save_local:  # 保存到本地
            self.dbLocal.save_urls(all_urls)
        if not proxy_url:
            proxy_url = 'ss://YWVzLTI1Ni1nY206NGVqSjhuNWRkTHVZRFVIR1hKcmUydWZK@212.102.40.68:48938#github.com/freefq%20-%20%E6%84%8F%E5%A4%A7%E5%88%A9%20%201'
        creator = client.Creator()
        creator.v2ray_start(proxy_url)
        time.sleep(2)
        self.__add_urls_de_dup(all_urls, PYIvmess().get_urls())
        print("获取https://t.me/s/ivmess 后数目：%d" % len(all_urls))
        self.__add_urls_de_dup(all_urls, PYFlyingboat().get_urls())
        print("获取https://t.me/s/flyingboat 后数目：%d" % len(all_urls))
        self.__add_urls_de_dup(all_urls, PYFreevpnnet().get_urls())
        print("获取https://www.freevpnnet.com/ 后数目：%d" % len(all_urls))
        self.__add_urls_de_dup(all_urls, PYMerlinblog().get_urls())
        print("获取https://merlinblog.xyz/wiki/freess.html 后数目：%d" % len(all_urls))
        # __add_urls_de_dup(all_urls, PYFreeFq().get_urls())
        self.__add_urls_de_dup(all_urls, PYFreeFq().download_urls(f_day=1))  # 前2天的地址
        print("获取从https://freefq.com/ 后数目：%d" % len(all_urls))
        if save_local:  # 保存到本地
            self.dbLocal.save_urls(all_urls)
        return all_urls

    def load_urls_by_net(self, proxy_url=None, save_local=True, need_proxy=True):
        """
        通过网络获取最新的节点，但是需要代理
        :param proxy_url: 代理url，默认的如果失效了则回去失败
        :param save_local: 是否保存到本地
        :param need_proxy: 如果程序本身就在外网跑，就不需要开启代理获取了
        :return:
        """
        all_urls = []
        # 1. 先把不需要代理的先请求下来
        self.__add_urls_de_dup(all_urls, PNSsfree().get_urls())
        print("获取https://view.ssfree.ru/后数目：%d" % len(all_urls))
        self.__add_urls_de_dup(all_urls, PNFreevpnX().get_urls())
        print("获取https://freevpn-x.com/后数目：%d" % len(all_urls))
        self.__add_urls_de_dup(all_urls, PNGithubIwxf().get_urls())
        print("获取https://github.com/iwxf/free-v2ray/blob/master/README.md 后数目：%d" % len(all_urls))
        self.__add_urls_de_dup(all_urls, PNFreeV2ray().get_urls())
        print("获取https://view.freev2ray.org/ 后数目：%d" % len(all_urls))
        print("准备开启代理获取...")
        if need_proxy:
            if not proxy_url:
                proxy_url = 'ss://YWVzLTI1Ni1nY206NGVqSjhuNWRkTHVZRFVIR1hKcmUydWZK@212.102.40.68:48938#github.com/freefq%20-%20%E6%84%8F%E5%A4%A7%E5%88%A9%20%201'
            # 需要代理
            creator = client.Creator()
            creator.v2ray_start(proxy_url)
        time.sleep(2)
        self.__add_urls_de_dup(all_urls, PYIvmess().get_urls())
        print("获取https://t.me/s/ivmess 后数目：%d" % len(all_urls))
        self.__add_urls_de_dup(all_urls, PYFlyingboat().get_urls())
        print("获取https://t.me/s/flyingboat 后数目：%d" % len(all_urls))
        self.__add_urls_de_dup(all_urls, PYFreevpnnet().get_urls())
        print("获取https://www.freevpnnet.com/ 后数目：%d" % len(all_urls))
        self.__add_urls_de_dup(all_urls, PYMerlinblog().get_urls())
        print("获取https://merlinblog.xyz/wiki/freess.html 后数目：%d" % len(all_urls))
        # __add_urls_de_dup(all_urls, PYFreeFq().get_urls())
        self.__add_urls_de_dup(all_urls, PYFreeFq().download_urls(f_day=1))  # 前2天的地址
        print("获取从https://freefq.com/ 后数目：%d" % len(all_urls))
        if save_local:  # 保存到本地
            self.dbLocal.save_urls(all_urls, append=False)
        return all_urls

    def load_unchecked_urls_by_local(self):
        """获取本地未校验过的url"""
        self.dbLocal.get_urls(False)
        urls = self.dbLocal.get_checked_urls()
        return urls

    def load_enable_urls_by_local(self):
        """获取已检测过的url"""
        return self.dbEnable.get_urls()

    def check_url_single(self, url: str):
        client.Creator().v2ray_start(url)
        time.sleep(2)
        ips = PYCheck().get_curren_ip()
        if not ips:
            print('地址无效！')
            return False
        print('检查地址结果：%s' % url)
        print(ips)
        return True

    def check_and_save(self, urls: [], append=True):
        """检测url是否可用，并且保存到本地"""
        if not append:
            self.dbEnable.clear_local()
        all_infos = self.dbEnable.get_infos()
        new_infos = []
        size = len(urls)
        for i in range(size):
            try:
                if i % 30 == 0:  # 每三十个更新一次
                    self.dbLocal.save_urls(urls=urls, append=False)  # 更新剩下的
                url = urls.pop()
                in_all = False
                for item in all_infos:
                    if url in item:
                        in_all = True
                        break
                if in_all:
                    print('取出地址已存在：%s' % url)
                    continue
                if client.Creator().v2ray_start_with_log(url) is False:
                    time.sleep(1)
                    continue
                time.sleep(2)
                ips = PYCheck().get_curren_ip()
                if not ips:
                    print('地址无效！')
                    continue
                ip, add = str(ips[0]), ips[1]
                hase_item = False  # 已存在
                for item in all_infos:
                    if ip in item:
                        hase_item = True
                        break
                if hase_item:
                    print('ip=%s已存在！' % ip)
                    continue
                info = r'%s,%s,%s' % (url.strip(), ip.strip(), add.strip().replace('\n', ''))
                print('%s！总共：%d |待检测：%d |可用：%d' % ('地址有效', size, len(urls), len(all_infos)))
                new_infos.append(info)
                all_infos.append(info)
                self.dbEnable.save_urls(new_infos)  # 写入已通过的
                new_infos.clear()
            except Exception as e:
                print(e)
        # 最后
        print('%s！总共：%d |待检测：%d |可用：%d' % ('全部检测完毕！', size, len(urls), len(all_infos)))
        self.dbEnable.save_urls(new_infos)
        self.dbLocal.clear_local()
