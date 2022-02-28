import re
import time
import os
from urllib.parse import quote_plus

import chardet
import requests_html
import pypandoc  # 要安装pandoc

from v2ray_pool import Net
from bs4 import BeautifulSoup
import googlesearch as ggs
import os
import random
import sys
import time
import ssl

BLACK_DOMAIN = ['www.google.gf', 'www.google.io', 'www.google.com.lc']
DOMAIN = 'www.google.com'


class GSearch(Net):
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
            # elif r.status_code == 429 or r.status_code == 443:
            #     time.sleep(3)
            #     return search_page(url)
            return None
        except Exception as e:
            print(e)
            return None

    def parse_html(self, html):
        soup = BeautifulSoup(html, 'html.parser')  # 声明BeautifulSoup对象
        # find = soup.find('p')  # 使用find方法查到第一个p标签
        # print('----->>>>%s' % str(find.text))
        p_s = soup.find_all('p')
        results = []
        for p in p_s:
            if p.find('img'):  # 不要带有图片的标签
                continue
            if p.find('a'):  # 不要带有链接的标签
                continue
            content = str(p)
            if "文章来源" in content:
                print('过滤[文章来源]>>>>>%s' % content)
                continue
            if "来源：" in content:
                print('过滤[来源：]>>>>>%s' % content)
                continue
            if len(p.text.replace('\n', '').strip()) < 1:  # 过滤空内容
                # print('过滤[空字符]>>>>>！')
                continue
            results.append(content)
        results.append('<p></br></p>')  # 隔一下
        return results
        # return re.findall(r'(<p.*?</p>)', html, re.DOTALL)

    def get_html(self, url):
        session = requests_html.HTMLSession()
        html = session.get(url)
        html.encoding = html.apparent_encoding
        return html.text

    def conver_to_doc(self, in_name, out_name):
        try:
            pypandoc.convert_file('%s.html' % in_name, 'docx', outputfile="doc/%s.docx" % out_name)
            os.remove('%s.html' % in_name)
        except Exception as e:
            print(e)

    def download_and_merge_page(self, urls, name):
        try:
            page = ['''<!DOCTYPE html>
                <html>
                <head>
                    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
                </head>
            ''']
            k = 0
            size = random.randint(3, 5)  # 每次合并成功5篇即可
            for i in range(len(urls)):
                if k >= size:
                    break
                try:
                    temp = self.parse_html(self.get_html(urls[i]))
                except Exception as e:
                    print(e)
                    continue
                if len(temp) < 3:  # 篇幅太短
                    continue
                page.append(
                    '<p style="text-align: left; font-family: 宋体; font-size: 16px; line-height: 1.75; margin-bottom: 10px;"><strong>第%d篇：</strong></p>' % (
                            k + 1))  # 加入标题
                page += temp
                page.append('\n')
                k += 1
            page.append('</html>')
            with open("%s.html" % name, mode="w") as f:  # 写入文件
                for p in page:
                    f.write(p)
            return k
        except Exception as e:
            print(e)
            return 0

    def get_full_urls(self, html):
        a_s = re.findall(r'<a.*?</a>', html, re.DOTALL)
        results = []
        for a in a_s:
            try:
                # print(a)
                # url = re.findall(r'/url\?q=(.*?\.html)', a, re.DOTALL)[0]
                url: str = re.findall(r'(http[s]{0,1}://.*?\.html)', a, re.DOTALL)[0]
                # title = re.findall(r'<span.*?>(.*?)</span>', a, re.DOTALL)[0] #会有问题
                # print('{"url":"%s","title":"%s"}' % (url, title))
                if 'google.com' in url:
                    continue
                if url in results:
                    continue
                # 过来同一个网站的
                domain = re.findall('http[s]{0,1}://(.*?)/', url, re.DOTALL)[0]
                # 含有--的
                if '-' in domain:
                    continue
                # www.sz.gov.cn，'.'超过4个时绝对不行的，像：bbs.jrj.ex3.http.80.ipv6.luzhai.gov.cn
                if domain.count('.') > 4:
                    continue
                for u in results:
                    if domain in u:
                        continue
                results.append(url)
            except Exception as e:
                # print(e)
                pass
        return results

    def get_full_titles(self, html):
        results = []
        soup = BeautifulSoup(html, "html.parser")
        results = []
        for a in soup.find_all(name='a'):

            try:
                h3 = a.find(name='h3')
                if h3 and h3.has_attr('div'):
                    div = h3.find(name='div')
                    results.append(div.getText())
                else:
                    div = a.find(name='span')
                    results.append(div.getText())

            except Exception as e:
                print(e)
        return results

    def format_common_url(self, search, domain='www.google.com', start=0):
        url = 'https://{domain}/search?q={search}&start={start}'
        url = url.format(domain=domain, search=quote_plus(search), start=start)
        return url

    def format_full_url(self, domain, as_q='', as_epq='', as_oq='', as_eq='', as_nlo='', as_nhi='', lr='', cr='',
                        as_qdr='',
                        as_sitesearch='',
                        as_filetype='', tbs='', start=0, num=10):
        """
        https://www.google.com/advanced_search
        https://www.google.com/search?as_q=%E8%A1%A3%E6%9C%8D+%E8%A3%A4%E5%AD%90+%E6%9C%8D%E8%A3%85+%E9%A5%B0%E5%93%81+%E7%8F%A0%E5%AE%9D+%E9%93%B6%E9%A5%B0&as_epq=%E5%AE%98%E7%BD%91&as_oq=%E6%9C%8D%E8%A3%85+or+%E9%85%8D%E9%A5%B0&as_eq=%E9%9E%8B%E5%AD%90&as_nlo=20&as_nhi=1000&lr=lang_zh-CN&cr=countryCN&as_qdr=m&as_sitesearch=.com&as_occt=body&safe=active&as_filetype=&tbs=
        allintext: 衣服 裤子 服装 饰品 珠宝 银饰 服装 OR or OR 配饰 "官网" -鞋子 site:.com 20..1000
        :param domain: 域名：google.com
        :param as_q:  输入重要字词： 砀山鸭梨
        :param as_epq: 用引号将需要完全匹配的字词引起： "鸭梨"
        :param as_oq: 在所需字词之间添加 OR： 批发 OR 特价
        :param as_eq: 在不需要的字词前添加一个减号： -山大、-"刺梨"
        :param as_nlo: 起点，在数字之间加上两个句号并添加度量单位：0..35 斤、300..500 元、2010..2011 年
        :param as_nhi: 终点，在数字之间加上两个句号并添加度量单位：0..35 斤、300..500 元、2010..2011 年
        :param lr: 查找使用您所选语言的网页。
        :param cr: 查找在特定地区发布的网页。
        :param as_qdr: 查找在指定时间内更新的网页。
        :param as_sitesearch: 搜索某个网站（例如 wikipedia.org ），或将搜索结果限制为特定的域名类型(例如 .edu、.org 或 .gov)
        :param as_filetype: 查找采用您指定格式的网页。如：filetype:pdf
        :param tbs: 查找可自己随意使用的网页。
        :param start: 第几页，如 90：表示从第9页开始，每一页10条
        :param num: 每一页的条数
        :return:
        """
        url = 'https://{domain}/search?as_q={as_q}&as_epq={as_epq}&as_oq={as_oq}&as_eq={as_eq}&as_nlo={as_nlo}&as_nhi={as_nhi}&lr={lr}&cr={cr}&as_qdr={as_qdr}&as_sitesearch={as_sitesearch}&as_occt=body&safe=active&as_filetype={as_filetype}&tbs={tbs}&start={start}&num={num}'
        url = url.format(domain=domain, as_q=quote_plus(as_q), as_epq=quote_plus(as_epq), as_oq=quote_plus(as_oq),
                         as_eq=quote_plus(as_eq), as_nlo=as_nlo, as_nhi=as_nhi, lr=lr, cr=cr, as_qdr=as_qdr,
                         as_sitesearch=as_sitesearch, start=start, num=num, tbs=tbs, as_filetype=as_filetype)
        return url


if __name__ == '__main__':
    url = 'http://www.sz.gov.cn/cn/zjsz/nj/content/post_1356218.html'
    domain: str = re.findall('http[s]{0,1}://(.*?)/', url, re.DOTALL)[0]
    print(domain.count('.'))
    print(domain)
