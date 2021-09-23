#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Description: 网络代理请求的基类
@Date       :2021/09/15
@Author     :xhunmon
@Mail       :xhunmon@gmail.com
"""

import requests
from my_fake_useragent import UserAgent


class Net(object):
    """
    基类，封装常用接口
    """
    TIMEOUT = 8

    def __init__(self, timeout=8):
        Net.TIMEOUT = timeout
        self._ua = UserAgent()
        self._agent = self._ua.random()  # 随机生成的agent
        self.USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
        self._headers = {"user-agent": self.USER_AGENT, 'Connection': 'close'}
        # determine
        self._proxy = '127.0.0.1:1080'
        self._proxies_en = {
            'http': 'socks5h://' + self._proxy,
            'https': 'socks5h://' + self._proxy,
        }
        self._proxies_zh = {
            'http': 'socks5://' + self._proxy,
            'https': 'socks5://' + self._proxy,
        }

    def get_header(self, headers, key):
        key_lower = key.lower()
        headers_lower = {k.lower(): v for k, v in headers.items()}
        if (key_lower in headers_lower):
            return headers_lower[key_lower]
        else:
            return ''

    def get_urls(self) -> []:
        """需子类实现"""
        pass

    def request(self, url, allow_redirects=False, verify=False, timeout=TIMEOUT):
        """普通请求"""
        return self.__request(url, allow_redirects=allow_redirects, verify=verify, timeout=timeout)

    def request_en(self, url, allow_redirects=False, verify=False, timeout=TIMEOUT):
        """国外网站请求，需要开代理"""
        return self.__request(url, allow_redirects=allow_redirects, verify=verify, proxies=self._proxies_en,
                              timeout=timeout)

    def request_zh(self, url, allow_redirects=False, verify=False, timeout=TIMEOUT):
        """国内网站请求，需要开代理"""
        return self.__request(url, allow_redirects=allow_redirects, verify=verify, proxies=self._proxies_zh,
                              timeout=timeout)

    def __request(self, url, allow_redirects=False, verify=False, proxies=None, timeout=TIMEOUT):
        """最终的请求实现"""
        requests.packages.urllib3.disable_warnings()
        if proxies:
            return requests.get(url=url, headers=self._headers, allow_redirects=allow_redirects, verify=verify,
                                proxies=proxies, timeout=timeout)
        else:
            return requests.get(url=url, headers=self._headers, allow_redirects=allow_redirects, verify=verify,
                                timeout=timeout)
