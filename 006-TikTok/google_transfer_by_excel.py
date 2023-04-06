#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Description: 实现从excel文件获取关键词进行翻译后写入新文件
@Date       :2021/10/22
@Author     :xhunmon
@Mail       :xhunmon@gmail.com
"""

import json
import os
import os.path
import random
import time

import chardet
import pandas as pd
import requests

import file_util as futls
from my_fake_useragent import UserAgent


class GTransfer(object):
    def __init__(self, file):
        self.file = file
        self._ua = UserAgent()
        self._agent = self._ua.random()  # 随机生成的agent
        self.USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
        self._headers = {"user-agent": self.USER_AGENT, 'Connection': 'close'}

    def request(self, url, allow_redirects=False, verify=False, proxies=None, timeout=8):
        """最终的请求实现"""
        requests.packages.urllib3.disable_warnings()
        if proxies:
            return requests.get(url=url, headers=self._headers, allow_redirects=allow_redirects, verify=verify,
                                proxies=proxies, timeout=timeout)
        else:
            return requests.get(url=url, headers=self._headers, allow_redirects=allow_redirects, verify=verify,
                                timeout=timeout)

    def search_page(self, url, pause=3):
        """
        Google search
        :param query: Keyword
        :param language: Language
        :return: result
        """
        time.sleep(random.randint(1, pause))
        try:
            r = self.request(url)
            print('resp code=%d' % r.status_code)
            if r.status_code == 200:
                charset = chardet.detect(r.content)
                content = r.content.decode(charset['encoding'])
                return content
            elif r.status_code == 301 or r.status_code == 302 or r.status_code == 303:
                location = r.headers['Location']
                time.sleep(random.randint(1, pause))
                return self.search_page(location)
            return None
        except Exception as e:
            print(e)
            return None

    def transfer(self, content):
        # url = 'http://translate.google.com/translate_a/single?client=gtx&dt=t&dj=1&ie=UTF-8&sl=auto&tl=zh-CN&q=' + content
        url = 'http://translate.google.cn/translate_a/single?client=gtx&dt=t&dj=1&ie=UTF-8&sl=zh-CN&tl=en&q=' + content
        try:
            cache = futls.read_json('lib/cache.json')
            for c in cache:
                if content in c:
                    print('已存在，跳过：{}'.format(content))
                    return c.get(content)
        except Exception as e:
            pass
        try:
            result = self.search_page(url)
            trans = json.loads(result)['sentences'][0]['trans']
            # 解析获取翻译后的数据
            # print(result)
            print(trans)
            self.local_cache.append({content: trans})
            futls.write_json(self.local_cache, self.file)
            # 写入数据吗？下次直接缓存取
        except Exception as e:
            print(e)
            return self.transfer(content)
        return trans

    def transfer_list(self, lists):
        self.local_cache = []
        for c in lists:
            self.transfer(c)


# http://translate.google.com/translate_a/single?client=gtx&dt=t&dj=1&ie=UTF-8&sl=auto&tl=zh-CN&q=what


if __name__ == '__main__':
    files = next(os.walk('xxx/folder'))[2]
    results = []
    for f in files:
        name, ext = os.path.splitext(f)
        if len(name) > 0 and len(ext):
            results.append(name)
    g = GTransfer('xxx/en.json')
    g.transfer_list(results)
