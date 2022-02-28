#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Description: 关键词获取
@Date       :2021/09/22
@Author     :xhunmon
@Mail       :xhunmon@gmail.com
"""
# from amazon import run_api
import json
import re

import yagooglesearch

import v2ray_util as utils
from gsearch import GSearch
from keywords import Keywords


def start_task():
    kd = Keywords()
    keywords = kd.get_titles_by_local()
    name = 'temp'
    gs = GSearch()
    i = 0
    is_need_start = True
    while i < len(keywords):
        if is_need_start:
            utils.restart_v2ray()
            gs.update_agent()
        is_need_start = True
        key = keywords[i]
        query = 'site:gov.cn filetype:html "%s"' % key
        client = yagooglesearch.SearchClient(
            query,
            tbs="li:1",
            max_search_result_urls_to_return=100,
            http_429_cool_off_time_in_minutes=49,
            http_429_cool_off_factor=1.5,
            proxy="socks5h://127.0.0.1:1080",
            verbosity=5,
        )
        client.assign_random_user_agent()
        try:
            page_urls = client.search()
        except Exception:
            continue
        new_urls = []
        for u1 in page_urls:
            domain: str = re.findall('http[s]{0,1}://(.*?)/', u1, re.DOTALL)[0]
            # 含有--的
            if '-' in domain:
                continue
            # www.sz.gov.cn，'.'超过4个时绝对不行的，像：bbs.jrj.ex3.http.80.ipv6.luzhai.gov.cn
            if domain.count('.') > 4:
                continue
            for u2 in new_urls:
                if domain in u2:
                    continue
                new_urls.append(u2)
        print('过滤器链接数：%d, 过滤后链接数：%d' % (len(page_urls), len(new_urls)))
        page_size = len(new_urls)
        if page_size == 0:
            print('[%s]获取文章链接失败！' % key)
            continue
        if not gs.download_and_merge_page(page_urls, name):  # 合并文章
            print('下载或者合并失败')
            continue
        doc_name = '%d篇%s' % (page_size, key)
        gs.conver_to_doc(name, doc_name)
        is_need_start = False
        i += 1

    utils.kill_all_v2ray()


def start_proxy_task():
    kd = Keywords()
    keywords: [] = kd.get_titles_by_local()
    name = 'temp'
    gs = GSearch()
    key_s = []
    key_s.pop()


def start_task2():
    kd = Keywords()
    keywords: [] = kd.get_titles_by_local()
    name = 'temp'
    gs = GSearch()
    i = 0
    is_need_start = True
    key_size = len(keywords)
    key = keywords.pop()
    while i < key_size:
        if is_need_start:
            utils.restart_v2ray()
            gs.update_agent()
        else:
            key = keywords.pop()
        is_need_start = True
        # key_url = gs.format_full_url(domain='google.com', as_sitesearch='.gov.cn', as_filetype='html', as_epq=key,
        #                              lr='lang_zh-CN', cr='countryCN')
        # key_url = gs.format_full_url(domain='search.iwiki.uk', as_sitesearch='gov.cn', as_filetype='html', as_epq=key,
        #                              lr='lang_zh-CN', cr='countryCN')
        # key_url = gs.format_common_url('site:gov.cn filetype:html %s' % key, domain='search.iwiki.uk')
        key_url = gs.format_common_url('site:gov.cn intitle:%s' % key, domain='www.google.com')
        print(key_url)
        content = gs.search_page(key_url)
        if content is None:
            print('[%s]搜索失败，进行重试！' % key)
            continue
        with open('test/test_search.html', 'w') as f:
            f.write(content)
            f.close()
        page_urls = gs.get_full_urls(content)  # 获取文章的url
        page_size = len(page_urls)
        if page_size == 0:
            print('[%s]没有内容，下一个...' % key)
        else:
            size = gs.download_and_merge_page(page_urls, name)
            if size == 0:  # 合并文章
                print('下载或者合并失败，跳过！')
            else:
                doc_name = '%d篇%s' % (size, key)
                gs.conver_to_doc(name, doc_name)
                print('生成[%s]文章成功！！！' % doc_name)
        is_need_start = False
        i += 1
        # 重新覆盖本地关键词
        with open('test/key_title.json', 'w') as f:
            json.dump(keywords, f, ensure_ascii=False)
            f.close()

    utils.kill_all_v2ray()


def test_titles():
    kd = Keywords()
    keywords = kd.get_titles_by_local()
    print('总共需要加载%d个关键词' % len(keywords))


def test_task():
    kd = Keywords()
    keywords = kd.get_keys_by_local()
    print('总共需要加载%d个关键词' % len(keywords))
    # keywords = ['股市基金']
    i = 0
    search_keys = []
    utils.restart_v2ray()  # 第一次用固定agent
    is_need_start = False
    while i < len(keywords):
        if is_need_start:
            utils.restart_v2ray()
            # kd.update_agent()
        is_need_start = True
        key = keywords[i]
        print('开始搜索：%s' % key)
        titles = kd.get_titles_by_net(key)
        if titles is None:
            print('[%s]获取关键词标题失败！' % key)
            continue
        print(titles)
        for t in titles:
            if t not in search_keys:
                search_keys.append(t)
        # 每次都要更新一次
        with open('test/key_title.json', 'w') as f:
            json.dump(search_keys, f, ensure_ascii=False)
            f.close()
        is_need_start = False
        i += 1

    utils.kill_all_v2ray()


def test_get_title():
    with open('search_page.html', 'r') as f:
        page = f.read()
        f.close()
    gs = GSearch()
    titles = gs.get_full_titles(page)  # 获取文章的标题
    print(titles)


if __name__ == "__main__":
    # utils.restart_v2ray()
    utils.search_node()
    # utils.kill_all_v2ray()
