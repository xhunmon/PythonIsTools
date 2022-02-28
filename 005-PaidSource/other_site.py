#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Description: 获取其他站点信息爬虫
@Date       :2022/1/14
@Author     :xhunmon
@Mail       :xhunmon@gmail.com
"""
import os
import random
import re
import time

import requests
from bs4 import BeautifulSoup

import file_util as futls
import v2ray_util as utils
from v2ray_pool import Net


class Cncic(Net):
    '''中华全国商业中心：https://www.cncic.org/'''

    def start_task(self):
        utils.restart_v2ray()
        cncic = Cncic()
        keys = [{'cat': 92, 'name': '专题分析报告'}, {'cat': 95, 'name': '政策法规'}, {'cat': 8, 'name': '月度分析'},
                {'cat': 10, 'name': '黄金周分析'}, {'cat': 16, 'name': '零售百强'}, {'cat': 94, 'name': '市场观察'}, ]
        success_datas = []
        for key in keys:
            cat = key.get('cat')
            name = key.get('name')
            datas = cncic.load_list(cat)
            while len(datas) == 0:
                utils.restart_v2ray()
                datas = cncic.load_list(cat)
            success_datas.append({'name': name, 'data': datas})
            futls.write_json(success_datas, 'data/cncic/keys.json')  # 每次保存到本地

        success_datas = futls.read_json('data/cncic/keys.json')
        key_size = len(success_datas)
        is_need_start = False
        key = None
        for i in range(key_size):
            if is_need_start:
                utils.restart_v2ray()
            else:
                key = success_datas.pop()
            if key is None:
                key = success_datas.pop()
            is_need_start = True
            folder = key.get('name')
            datas = key.get('data')
            for data in datas:
                try:
                    load_page = cncic.load_page(data.get('url'))
                except Exception as e:
                    print(e)
                    continue
                title, content = cncic.parse_page(load_page)
                html_path = 'data/html/cncic/%s/%s.html' % (folder, title)
                doc_path = 'data/doc/cncic/%s/%s.docx' % (folder, title)
                futls.write_to_html(content, html_path)
                try:
                    futls.html_cover_doc(html_path, doc_path)
                except Exception as e:
                    print(e)
            futls.write_json(success_datas, 'data/cncic/keys.json')  # 更新本地数据库
            is_need_start = False
            i += 1
        utils.kill_all_v2ray()

    def load_list(self, cat, paged=1) -> []:
        results = []
        while True:
            url = 'https://www.cncic.org/?cat=%d&paged=%d' % (cat, paged)
            try:
                page = self.load_page(url)
                results += self.parse_list(page)
                paged += 1
                time.sleep(random.randint(3, 6))
            except Exception as e:
                print(e)
                break
        return results

    def load_page(self, url):
        '''加载页面，如：https://www.cncic.org/?p=3823'''
        r = self.request_zh(url)
        r.encoding = r.apparent_encoding
        print('Cncic[%s] code[%d]' % (url, r.status_code))
        if r.status_code == 200:
            return r.text
        elif r.status_code == 301 or r.status_code == 302 or r.status_code == 303:
            location = r.headers['Location']
            time.sleep(1)
            return self.load_page(location)
        return None

    def parse_page(self, page):
        '''解析页面，返回标题和文章页面内容，如果生成文章则还需要组装'''
        soup = BeautifulSoup(page, 'html.parser')
        article = soup.find('article')
        header = article.find('header')
        title = header.text.replace('\n', '').replace(' ', '')
        content = article.find('div', class_='single-content')
        result = str(header)
        result += str(content)
        return title, result

    def parse_list(self, page):
        '''解析列表（如：https://www.cncic.org/?cat=92）页面，返回标题、连接、日期'''
        soup = BeautifulSoup(page, 'html.parser')
        main = soup.find('main')
        articles = main.find_all('article')
        results = []
        for article in articles:
            header = article.find('header')
            url = header.find('a').get_attribute_list('href')[0]
            title = header.text.replace('\n', '').replace(' ', '')
            date = article.find('span', class_='date').text
            results.append({'url': url, 'title': title, 'date': date})
        return results


class Ceicdata(Net):
    '''https://www.ceicdata.com/'''

    def start_task_1(self):
        cd = Ceicdata()
        utils.restart_v2ray()
        success_datas = futls.read_json('data/keys/ceicdata.json')
        key_size = len(success_datas)
        print(key_size)
        is_need_start = False
        key = None
        for i in range(key_size):
            if is_need_start:
                utils.restart_v2ray()
                cd.update_agent()
            else:
                key = success_datas.pop()
            is_need_start = True
            if key is None:
                key = success_datas.pop()
            title = key.get('title')
            url = key.get('url')
            try:
                page = cd.load_page(url)
            except Exception as e:
                page = None
                print(e)
            if page is None:
                continue
            html_path = 'data/html/ceicdata/%s.html' % title
            content = cd.parse_page_1(page)
            futls.write_to_html(content, html_path)
            futls.html_cover_excel(html_path, 'data/doc/ceicdata/%s.xlsx' % title)
            futls.write_json(success_datas, 'data/keys/ceicdata.json')  # 更新本地数据库
            is_need_start = False
            i += 1
        utils.kill_all_v2ray()

    @staticmethod
    def start_task2():
        utils.restart_v2ray()
        cd = Ceicdata()
        keys_path = 'data/keys/ceicdata.json'
        keys = futls.read_json(keys_path)
        if not keys:
            url = 'https://www.ceicdata.com/zh-hans/country/china'
            page = cd.load_page(url)
            if page is None:
                raise Exception('获取页面失败')
            keys = cd.parse_main_2(page)
            if len(keys) == 0:
                raise Exception('获取链接失败')
            futls.write_json(keys, keys_path)
        key_size = len(keys)
        print('下载数量[%d]' % key_size)
        is_need_start = False
        key = None
        for i in range(key_size):
            if is_need_start:
                utils.restart_v2ray()
                cd.update_agent()
            else:
                key = keys.pop()
            is_need_start = True
            if key is None:
                key = keys.pop()
            url = key.get('url')
            try:
                page = cd.load_page(url)
            except Exception as e:
                page = None
                print(e)
            if page is None:
                continue
            try:
                title, content = cd.parse_page_2(page)
            except Exception as e:
                print(e)
                continue
            html_path = 'data/html/ceicdata2/%s.html' % title
            futls.write_to_html(content, html_path)
            futls.html_cover_doc(html_path, 'data/doc/ceicdata/%s.docx' % title)
            futls.write_json(keys, keys_path)  # 更新本地数据库
            is_need_start = False
            i += 1
        utils.kill_all_v2ray()

    def load_page(self, url):
        '''加载页面，如：https://www.cncic.org/?p=3823'''
        r = self.request_en(url)
        # r = self.request(url)
        r.encoding = r.apparent_encoding
        print('Cncic[%s] code[%d]' % (url, r.status_code))
        if r.status_code == 200:
            return r.text
        elif r.status_code == 301 or r.status_code == 302 or r.status_code == 303:
            location = r.headers['Location']
            time.sleep(1)
            return self.load_page(location)
        return None

    def parse_main_1(self, page):
        '''解析页面，返回标题和文章页面内容，如果生成文章则还需要组装'''
        soup = BeautifulSoup(page, 'html.parser')
        main = soup.find('main')
        lists = main.find('div', class_='indicators-lists')
        results = []
        for a in lists.find_all('a'):
            # https://www.ceicdata.com/zh-hans/indicator/nominal-gdp
            title = a.text.replace(' ', '')
            url = 'https://www.ceicdata.com' + a.get_attribute_list('href')[0].replace(' ', '')
            results.append({'title': title, 'url': url})
        return results

    def parse_main_2(self, page):
        '''解析页面，返回标题和文章页面内容，如果生成文章则还需要组装'''
        soup = BeautifulSoup(page, 'html.parser')
        main = soup.find('main')
        results = []
        for tbody in main.find_all('tbody'):
            for a in tbody.find_all('a'):
                # https://www.ceicdata.com/zh-hans/indicator/nominal-gdp
                title = a.text.replace(' ', '')
                url = 'https://www.ceicdata.com' + a.get_attribute_list('href')[0].replace(' ', '')
                results.append({'title': title, 'url': url})
        return results

    def parse_page_1(self, page):
        '''解析页面，返回标题和文章页面内容，如果生成文章则还需要组装'''
        soup = BeautifulSoup(page, 'html.parser')
        main = soup.find('main')
        clearfix = main.find('div', class_='clearfix')
        h1 = clearfix.find('h1')
        h2 = clearfix.find('h2')
        tables = clearfix.find_all('table')
        content = str(h1) + str(tables[0]) + str(h2) + str(tables[1])
        return content

    def parse_page_2(self, page):
        '''解析页面，返回标题和文章页面内容，如果生成文章则还需要组装'''
        soup = BeautifulSoup(page, 'html.parser')
        main = soup.find('main')
        left = main.find('div', id='left-col-7')
        title = left.find('span', class_='c-purple').text.replace(' ', '').replace('\n', '')
        left.find('div', id='breadcrumb').decompose()  # 移除节点
        for ele in left.find_all('div', class_='hide'):
            ele.decompose()  # 移除节点
        for ele in left.find_all('div', class_='div-chart-btns'):
            ele.decompose()  # 移除节点
        for ele in left.find_all('div', class_='table-buy'):
            ele.decompose()  # 移除节点
        for ele in left.find_all('div', class_='div-bgr-2'):
            if '查看价格选项' in str(ele):
                ele.decompose()  # 移除节点
        for ele in left.find_all('h4'):
            if '购买' in str(ele):
                ele.decompose()  # 移除节点
        for ele in left.find_all('button'):
            if '加载更多' in str(ele):
                ele.decompose()  # 移除节点
        for ele in left.find_all('div', class_='div-bgr-1'):
            if '详细了解我们' in str(ele):
                ele.decompose()  # 移除节点
        i = 1
        for img in left.find_all('img'):
            src = str(img.get('src'))
            path = '/Users/Qincji/Desktop/develop/py/project/PythonIsTools/005-PaidSource/data/img/%d.svg' % i
            dst = '/Users/Qincji/Desktop/develop/py/project/PythonIsTools/005-PaidSource/data/img/%d.png' % i
            if 'www.ceicdata.com' in src:
                print('下载图片url[%s]' % src)
                r = self.request_zh(src)
                # r = self.request(src)
                if r.status_code == 200:
                    with open(path, 'wb') as f:
                        f.write(r.content)
                    futls.svg_cover_jpg(path, dst)  # 将svg转换成jpg
                    img['src'] = dst
                    i += 1
                else:
                    raise Exception('下载图片失败！')
        rs = re.sub(r'href=".*?"', '', str(left))  # 移除href
        return title, rs


class Cnnic(Net):
    '''http://www.cnnic.net.cn/hlwfzyj/hlwxzbg/ , 注意：因为文件过大，使用别人代理下载，固定代理'''

    @staticmethod
    def start_task():
        cnnic = Cnnic()
        keys_path = 'data/keys/cnnic.json'
        all_keys = futls.read_json(keys_path)
        if not all_keys:
            all_keys = []
            for i in range(7):
                if i == 0:
                    url = 'http://www.cnnic.net.cn/hlwfzyj/hlwxzbg/index.htm'
                else:
                    url = 'http://www.cnnic.net.cn/hlwfzyj/hlwxzbg/index_%d.htm' % i
                page = cnnic.load_page(url)
                if page:
                    futls.write(page, 'test/src.html')
                all_keys += cnnic.parse_page(page)
                futls.write_json(all_keys, keys_path)
        size = len(all_keys)
        print('将要下载数量[%d]' % size)
        for i in range(size):
            key = all_keys.pop()
            name = key.get('title')
            url = key.get('url')
            path = 'data/doc/cnnic/%s.pdf' % name
            cnnic.download(url, path)
            futls.write_json(all_keys, keys_path)
            print('已下载[%d] | 还剩[%d]' % (i + 1, size - i - 1))

    def load_page(self, url):
        time.sleep(3)
        # r = self.request_en(url)
        # r = self.request(url)
        proxies = {'http': 'http://11.0.222.4:80', 'https': 'http://11.0.222.4:80'}
        r = requests.get(url=url, headers=self._headers, allow_redirects=False, verify=False,
                         proxies=proxies, timeout=15)
        r.encoding = r.apparent_encoding
        print('Cnnic[%s] code[%d]' % (url, r.status_code))
        if r.status_code == 200:
            return r.text
        elif r.status_code == 301 or r.status_code == 302 or r.status_code == 303:
            location = r.headers['Location']
            time.sleep(1)
            return self.load_page(location)
        return None

    def parse_page(self, page):
        '''解析页面，返回标题和文章页面内容，如果生成文章则还需要组装'''
        soup = BeautifulSoup(page, 'html.parser')
        content = soup.find('div', class_='content')
        results = []
        for li in content.find_all('li'):
            a = li.find('a')
            date = li.find('div', class_='date').text[0:4]  # 只要年份
            title = a.text.replace('\n', '').replace(' ', '')
            # http://www.cnnic.net.cn/hlwfzyj/hlwxzbg/hlwtjbg/202109/P020210915523670981527.pdf
            #                                      ./hlwtjbg/202109/P020210915523670981527.pdf
            url = 'http://www.cnnic.net.cn/hlwfzyj/hlwxzbg/' + str(a.get('href')).replace('./', '')
            if not '年' in title:
                title = '%s年发布%s' % (date, title)
            results.append({'title': title, 'url': url})
        return results

    def download(self, url, path):
        if os.path.exists(path):
            os.remove(path)
        proxies = {'http': 'http://11.0.222.4:80', 'https': 'http://11.0.222.4:80'}
        r = requests.get(url=url, headers=self._headers, allow_redirects=False, verify=False,
                         proxies=proxies, timeout=15, stream=True)
        i = 0
        print('name[%s]|code[%d]' % (path, r.status_code))
        with open(path, "wb") as pdf:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    i += 1
                    if i % 30 == 0:
                        print('.', end='')
                    pdf.write(chunk)
            pdf.close()
        time.sleep(random.randint(3, 12))


class Othersite(Net):
    def __init__(self):
        super(Othersite, self).__init__()
        self.dir = 'Othersite'

    @staticmethod
    def start_task():
        reqs = [{'title': 'xxx', 'url': 'https://www.xxx.com/wedding/engagement-rings.html'}]
        # utils.restart_v2ray()
        sl = Othersite()
        datas = futls.read_json(os.path.join('Othersite', 'page_urls.json'))
        if datas is None:
            datas = []
        for req in reqs:
            title = req.get('title')
            url = req.get('url')
            has_write = False
            for data in datas:
                if title in data.get('title'):
                    has_write = True
                    break
            if has_write:  # 已经请求过了
                print('页面连接 [%s]已存在，跳过！' % title)
                continue
            start = 1
            page_urs = []
            while True:
                if start != 1:
                    temp = url + '?p=' + str(start)
                else:
                    temp = url
                try:
                    page = sl.load_page(temp)
                except Exception as e:
                    print(e)
                    print('--------000')
                    utils.restart_v2ray()
                    continue
                futls.write(page, 'test/src.html')
                has_next, results = sl.parse_list(page)
                print('has_next: {} | {}'.format(has_next, results))
                page_urs += results
                if not has_next:
                    break
                start += 1
                # page = futls.read('test/src.html')
            # print(sl.parse_details(page))
            datas.append({'title': title, 'urls': page_urs})
            futls.write_json(datas, os.path.join('Othersite', 'page_urls.json'))
        all_results = []  # 总数据表
        size = len(datas)
        alls_local = futls.read_json(os.path.join('Othersite', 'all.json'))
        for i in range(size):
            data = datas.pop()
            title = data.get('title')
            page_urs = data.get('urls')
            has_write_all = False
            # for local in alls_local:
            #     if title in local.get('title'):
            #         has_write_all = True
            #         break
            # if has_write_all:
            #     print('[%s]已下载，跳过！' % title)
            #     continue
            sl.dir = os.path.join('Othersite', title)
            url_size = len(page_urs)
            print('下载数量[%d]' % url_size)
            is_need_start = False
            url = None
            results = []
            for i in range(url_size):
                if is_need_start:
                    utils.restart_v2ray()
                    sl.update_agent()
                else:
                    url = page_urs.pop()
                is_need_start = True
                if url is None:
                    url = page_urs.pop()
                # 本地是否也已经存在
                sku1 = url[url.rfind('-') + 1:].replace('.html', '').upper()
                if os.path.exists(os.path.join(sl.dir, sku1)):
                    is_need_start = False
                    print('ksu [%s]已存在，跳过！' % sku1)
                    continue
                try:
                    page = sl.load_page(url)
                    sku = sl.parse_details(page)
                    results.append(sku)
                    is_need_start = False
                except Exception as e:
                    print(e)
                    print('--------333')
            all_results.append({'title': title, 'skus': results})
            futls.write_json(all_results, os.path.join('Othersite', 'all.json'))
            futls.write_json(datas, os.path.join('Othersite', 'page_urls.json'))
        utils.kill_all_v2ray()

    def load_page(self, url):
        '''加载页面，如：https://www.cncic.org/?p=3823'''
        time.sleep(random.randint(3, 8))
        r = self.request_en(url)
        # r = self.request(url)
        r.encoding = r.apparent_encoding
        print('Othersite code[%d] |url [%s] ' % (r.status_code, url))
        if r.status_code == 200:
            return r.text
        elif r.status_code == 301 or r.status_code == 302 or r.status_code == 303:
            location = r.headers['Location']
            time.sleep(1)
            return self.load_page(location)
        return None

    def parse_home(self, page):
        soup = BeautifulSoup(page, 'html.parser')
        nav = soup.find('nav')
        results = []
        for a in nav.find_all('a'):
            results.append({'title': a.text, 'url': str(a.get('href'))})
        return results

    def parse_list(self, page):
        soup = BeautifulSoup(page, 'html.parser')
        ol = soup.find('ol')
        # 判断是否还有下一页
        next = False
        pages = soup.find('div', class_='pages')
        if pages:
            pages_n = pages.find('li', class_='pages-item-next')
            if pages_n:
                next = True
        results = []
        for a in ol.find_all('a'):
            results.append(str(a.get('href')))
        return next, results

    def parse_details(self, page):
        soup = BeautifulSoup(page, 'html.parser')
        # content = soup.find('div', class_='content')
        # main = content.find('main')
        right = soup.find('div', class_='product-info-main')
        title = right.find('h1').text.replace('Othersite ', '')
        sku = right.find('div', class_='value').text
        try:
            price = right.find('span', id='price-saved').find('span').text
        except Exception:
            print('没有折扣，继续找..')
            price = right.find('span', class_='special-price').find('span', class_='price').text
        # 下载图片
        layout = soup.find('amp-layout')
        carousel = layout.find('amp-carousel')
        imgs = []
        i = 0
        content = '{}\n{}'.format(sku, title)
        for img in carousel.find_all('amp-img'):
            src = str(img.get('src'))
            imgs.append(src)
            path = self.download_img(src, sku, i)
            content = content + '\n' + path
            i += 1
        futls.write(content, os.path.join(self.dir, sku, '{}.txt'.format(sku)))
        return {'sku': sku, 'title': title, 'price': price, 'imgs': imgs}

    def download_img(self, src, sku, i):
        path = os.path.join(self.dir, sku, '{}-{}.jpg'.format(sku, i))
        pre_path, file_name = os.path.split(path)
        if pre_path and not os.path.exists(pre_path):
            os.makedirs(pre_path)
        time.sleep(random.randint(1, 2))
        r = self.request_en(src)
        if r.status_code == 200:
            with open(path, 'wb') as f:
                f.write(r.content)
        else:
            raise Exception('下载图片失败！')
        return path


if __name__ == "__main__":
    pass
