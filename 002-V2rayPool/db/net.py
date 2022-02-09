#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Description: 从网络获取
@Date       :2021/08/30
@Author     :xhunmon
@Mail       :xhunmon@gmail.com
"""
import json

from base.net_proxy import Net

import re
import time
import chardet


def re_vmess_ss_trojan(pattern, html) -> []:
    """传入规则：r'xxx%sxxx', %s为固定的：(vmess://.+?|ss://.+?|trojan://.+?)"""
    results = re.findall(pattern % '(vmess://.+?|ss://.+?|trojan://.+?)', html, re.DOTALL)
    urls = []
    for i in results:
        temp: str = i.strip()
        if len(temp) < 20 and temp in results:  # 凭感觉
            continue
        # 如果是换行的
        if '\n' in temp:
            items = temp.split('\n')
            for j in items:
                temp_j: str = j.strip()
                if len(temp_j) < 20 and temp_j in results:  # 凭感觉
                    continue
                value_j = temp_j.replace('\n', '')
                if len(value_j) > 10:
                    urls.append(value_j)
            continue
        value = temp.replace('\n', '')
        if len(value) > 10:
            urls.append(value)
    return urls


class PYCheck(Net):
    def get_curren_ip(self, url='https://ip.cn/api/index?ip=&type=0'):
        """获取内容"""
        try:
            r = self.request_zh(url)
            if r.status_code == 200:
                charset = chardet.detect(r.content)
                content = r.content.decode(charset['encoding'])
                r.encoding = r.apparent_encoding
                # {"rs":1,"code":0,"address":"德国  Hessen  ","ip":"51.38.122.98","isDomain":0}
                results = json.loads(content)
                if not results:
                    return None
                return [results['ip'], results['address']]
            elif r.status_code == 301 or r.status_code == 302 or r.status_code == 303:
                location = r.headers['Location']
                time.sleep(1)
                return self.get_curren_ip(location)
        except Exception as e:
            print(e)
            return None


class PNFreeV2ray(Net):
    """
    https://view.freev2ray.org/
    """

    def get_urls(self) -> []:
        try:
            r = self.request(r'https://view.freev2ray.org/')
            if r.status_code != 200:
                return None
            r.encoding = r.apparent_encoding
            return re_vmess_ss_trojan(r'"%s"', r.text)
        except Exception as e:
            print(e)
            return None


class PNTWGithubV2ray(Net):
    """
    # https://hub.xn--gzu630h.xn--kpry57d/freefq/free
    """

    def get_urls(self) -> []:
        try:
            r = self.request(r'https://hub.xn--gzu630h.xn--kpry57d/freefq/free')
            if r.status_code != 200:
                return None
            r.encoding = r.apparent_encoding
            return re_vmess_ss_trojan(r'"%s"', r.text)
        except Exception as e:
            print(e)
            return None


class PNSsfree(Net):
    """
    https://view.ssfree.ru/
    """

    def get_urls(self) -> []:
        try:
            r = self.request(r'https://view.ssfree.ru/')
            if r.status_code != 200:
                return None
            r.encoding = r.apparent_encoding
            html = r.text
            return re_vmess_ss_trojan(r'"%s"', html)
        except Exception as e:
            print(e)
            return None


class PNFreevpnX(Net):
    """
    https://freevpn-x.com/
    """

    def get_urls(self) -> []:
        """
        获取当前页面中文本的url
        :param date: 如：2021/08/29
        :return:
        """
        url2 = r'https://url.cr/api/user.ashx?do=freevpn&ip=127.0.0.1&uuid=C5E0C9BA-FECB-44ED-9BD8-90C55365E11B&_=%d' % (
                time.time() * 1000)
        try:
            r = self.request(url2)
            if r.status_code != 200:
                return None
            r.encoding = r.apparent_encoding
            html = r.text
            results = html.split('\n')
            urls = []
            for i in results:
                temp = i.strip()
                if len(temp) > 10:
                    urls.append(temp)
            return urls
        except Exception as e:
            print(e)
            return None


class PNGithubIwxf(Net):
    """
    https://github.com/iwxf/free-v2ray/blob/master/README.md
    """

    def get_urls(self) -> []:
        """
        获取当前页面中文本的url
        :param date: 如：2021/08/29
        :return:
        """
        try:
            r = self.request(r'https://github.com/iwxf/free-v2ray/blob/master/README.md')
            if r.status_code != 200:
                return None
            r.encoding = r.apparent_encoding
            html = r.text
            return re_vmess_ss_trojan(r'<pre><code>%s</code></pre>', html)
        except Exception as e:
            print(e)
            return None


class PYFreevpnnet(Net):
    """
    https://www.freevpnnet.com/
    需要代理
    """

    def get_urls(self) -> []:
        try:
            r = self.request_en(r'https://www.freevpnnet.com/')
            if r.status_code != 200:
                return None
            r.encoding = r.apparent_encoding
            html = r.text
            return re_vmess_ss_trojan(r'>%s<', html)
        except Exception as e:
            print(e)
            return None


class PYMerlinblog(Net):
    """
    https://merlinblog.xyz/wiki/freess.html
    需要代理
    """

    def get_urls(self) -> []:
        try:
            r = self.request_en(r'https://merlinblog.xyz/wiki/freess.html')
            if r.status_code != 200:
                return None
            r.encoding = r.apparent_encoding
            html = r.text
            return re_vmess_ss_trojan('%s<', html)
        except Exception as e:
            print(e)
            return None


class PYFlyingboat(Net):
    """
    https://t.me/s/flyingboat
    需要代理
    """

    def get_urls(self) -> []:
        try:
            r = self.request_en(r'https://t.me/s/flyingboat')
            if r.status_code != 200:
                return None
            r.encoding = r.apparent_encoding
            html = r.text
            return re_vmess_ss_trojan('>%s<', html)
        except Exception as e:
            print(e)
            return None


class PYIvmess(Net):
    """
    https://t.me/s/ivmess
    需要代理
    """

    def get_urls(self) -> []:
        try:
            r = self.request_en(r'https://t.me/s/ivmess')
            if r.status_code != 200:
                return None
            r.encoding = r.apparent_encoding
            html = r.text
            return re_vmess_ss_trojan('>%s<', html)
        except Exception as e:
            print(e)
            return None


class PYFreeFq(Net):
    """
    从https://freefq.com/获取免费节点，规则：https://freefq.com/v2ray/2021/08/30/v2ray.html
    """

    def __get_content_url(self, date) -> str:
        """
        获取当前页面中文本的url
        :param date: 如：2021/08/29
        :return:
        """
        try:
            r = self.request_en(r'https://freefq.com/v2ray/%s/v2ray.html' % date)
            if r.status_code != 200:
                return None
            r.encoding = r.apparent_encoding
            return self.__get_url_by_content_html(r.text)
        except Exception as e:
            print(e)
            return None

    def __get_url_by_content_html(self, html: str):
        """从文本中通过正则获取节点所在文本的url"""
        results = re.findall(r'<td>.+?</td>', html)
        tag = None
        pre = 'https://www.freefq.com/d/file/v2ray'
        for url in results:
            if pre in url:
                tag = url
                break
        if not tag:
            print('无法获取节点url：%s' % results)
            return None
        try:
            url = re.findall(r'%s.+?\.htm' % pre, tag)[0]
        except Exception as e:
            print(e)
            return None
        return url

    def __get_url_by_detail_html(self, html: str):
        """截取文本中的节点url"""
        # results = re.findall(r'(trojan://.+?|vmess://.+?|ss://.+?)<br>', html)
        results = re_vmess_ss_trojan(r'%s<br>', html)
        urls = []
        for url in results:
            temp: str = url.strip()
            if len(temp) < 20 and temp in results:  # 凭感觉
                continue
            urls.append(url)
        return urls

    def __get_detail_urls(self, url: str) -> []:
        """获取内容"""
        try:
            r = self.request_en(url)
            if r.status_code != 200:
                return None
            r.encoding = r.apparent_encoding
            # return self.__get_url_by_detail_html(r.text)
            return re_vmess_ss_trojan(r'%s<br>', r.text)
        except Exception as e:
            print(e)
            return None

    def download_urls(self, f_day=1) -> []:
        """
        开始获取
        :param f_day: 需要获取往前的天数
        :return:
        """
        DAY = 24 * 60 * 60
        l_time = time.time()
        all_url = []
        for day in range(1, f_day + 1):  # 需要从前一天开始
            temp_day = time.strftime("%Y/%m/%d", time.localtime(l_time - (day * DAY)))
            url = self.__get_content_url(temp_day)
            if not url:
                continue
            urls = self.__get_detail_urls(url)
            if not urls:  # 如果是None或者[]
                continue
            for temp in urls:
                if temp not in all_url:
                    all_url.append(temp)
            time.sleep(1)
        return all_url

    def get_urls(self) -> []:
        return self.download_urls()
