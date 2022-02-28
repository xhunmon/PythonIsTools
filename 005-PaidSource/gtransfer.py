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

import file_util as futls
import v2ray_util as utils
from v2ray_pool import Net

BLACK_DOMAIN = ['www.google.gf', 'www.google.io', 'www.google.com.lc']
DOMAIN = 'www.google.com'


class GTransfer(Net):
    def search_page(self, url, pause=3):
        """
        Google search
        :param query: Keyword
        :param language: Language
        :return: result
        """
        time.sleep(random.randint(1, pause))
        try:
            r = self.request_en(url)
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
        url = 'http://translate.google.cn/translate_a/single?client=gtx&dt=t&dj=1&ie=UTF-8&sl=en&tl=zh-CN&q=' + content
        try:
            cache = futls.read_json('data/cache.json')
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
            futls.write_json(self.local_cache, 'data/cache.json')
            # 写入数据吗？下次直接缓存取
        except Exception as e:
            print(e)
            utils.restart_v2ray()
            return self.transfer(content)
        return trans

    def init_param(self, file_name):
        utils.restart_v2ray()
        self.local_cache = []
        # 第一次加载本地的（已翻译的就不再翻译了）
        try:
            cache = futls.read_json('data/cache.json')
            for c in cache:
                self.local_cache.append(c)
        except Exception as e:
            pass
        csv_file = os.path.join('data', file_name)
        csv_out = os.path.join('data', 'out_' + file_name)
        df = pd.read_excel(csv_file, sheet_name='CompetitorWords')
        # 代表取出第一行至最后一行，代表取出第四列至最后一列。
        datas = df.values
        size = len(df)
        print('总共有{}行数据'.format(size))
        titles, titles_zh, keys1, keys2, keys3, pros = [], [], [], [], [], []
        for col in range(0, size):
            t = datas[col][0]
            titles.append(t)
            keys1.append(datas[col][1])
            keys2.append(datas[col][2])
            keys3.append(datas[col][3])
            pros.append(datas[col][4])
            titles_zh.append(self.transfer(t))
            print('总共{}，现在到{}'.format(size, col + 1))
        df_write = pd.DataFrame(
            {'标题': titles, '中文标题': titles_zh, '关键词1': keys1, '关键词2': keys2, '关键词3': keys3, '橱窗产品': pros})
        df_write.to_excel(csv_out, index=False)
        utils.kill_all_v2ray()


# http://translate.google.com/translate_a/single?client=gtx&dt=t&dj=1&ie=UTF-8&sl=auto&tl=zh-CN&q=what


if __name__ == '__main__':
    g = GTransfer()
    g.init_param('xxx.xls')
    # utils.search_node()
