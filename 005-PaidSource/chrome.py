#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Description: 用已经打开的chrome浏览器进行自动化操作。
在某些应用场景我们获取怎么都获取不到cookie，但我们可以使用先在浏览器上登录，然后进行自动化操作。
这里实现book118.com网站自动化操作。
@Date       :2022/1/14
@Author     :xhunmon
@Mail       :xhunmon@gmail.com
"""

import asyncio
import random
import time

import aiohttp
import requests
from bs4 import BeautifulSoup
from pyppeteer import launcher

import file_util as futls
from v2ray_pool import Net

loop = asyncio.get_event_loop()


async def get_cookie(page):
    """
    获取cookie
    :param:page page对象
    :return:cookies 处理后的cookie
    """
    cookie_list = await page.cookies()
    cookies = ""
    for cookie in cookie_list:
        coo = "{}={};".format(cookie.get("name"), cookie.get("value"))
        cookies += coo
    return cookies


async def main():
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get("http://localhost:9222/json/version") as response:
                chrome = await response.json()
                browser = await launcher.connect(
                    defaultViewport=None,
                    loop=loop,
                    browserWSEndpoint=chrome['webSocketDebuggerUrl']
                )
        except aiohttp.ClientConnectorError:
            print("start chrome --headless --remote-debugging-port=9222 --disable-gpu")
            return
    # pages = await browser.pages()
    page = await browser.newPage()  # "通过 Browser 对象创建页面 Page 对象"
    await page.goto('https://max.book118.com/user_center_v1/doc/Doclist/trash.html')
    table = await page.waitForSelector('#table')
    print(table)
    content = await page.content()  # 获取页面内容
    futls.write(content, 'test/src.html')
    agent = await browser.userAgent()
    cookies = await get_cookie(page)
    print('agent：[%s]' % agent)
    print('cookies:[%s]' % cookies)
    results = Book118.parse_page(content)
    print(results)
    print('需要操作的个数:[%d]' % len(results))
    headers = {
        'Cookie': cookies,
        'User-Agent': agent
    }
    for result in results:
        aids = result.get('aids')
        title = result.get('title')
        Book118.recycling(headers, aids, title)
        time.sleep(random.randint(2, 5))
        Book118.recycling_name(headers, aids)
        time.sleep(random.randint(2, 5))


class Book118(Net):
    '''https://max.book118.com/user_center_v1/doc/index/index.html#trash'''

    @staticmethod
    def recycling(headers, aids, title):
        data = {
            'aids': aids,
            'is_optimization': 0,
            'title': title,
            'keywords': '',
            'typeid': 481,
            'dirid': 0,
            'is_original': 0,
            'needmoney': random.randint(3, 35),
            'summary': ''
        }
        url = 'https://max.book118.com/user_center_v1/doc/Api/updateDocument/docListType/recycling'
        r = requests.post(url=url, data=data, headers=headers, allow_redirects=False, verify=False, timeout=15,
                          stream=True)
        if r.status_code == 200:
            print('修改[%s]成功' % title)
        else:
            print(r)
            raise Exception('[%s]修改失败！' % title)

    @staticmethod
    def recycling_name(headers, aids):
        data = {
            'aids': aids,
            'reason': '文件名已修复',
            'status': 1
        }
        url = 'https://max.book118.com/user_center_v1/doc/Api/recoverDocument/docListType/recycling'
        r = requests.post(url=url, data=data, headers=headers, allow_redirects=False, verify=False,
                          timeout=15, stream=True)
        if r.status_code == 200:
            print('提交[%s]成功' % aids)
        else:
            print(r)
            raise Exception('[%s]操作失败！' % aids)

    @staticmethod
    def load_page(url):
        r = requests.get(url=url, allow_redirects=False, verify=False,
                         timeout=15, stream=True)
        r.encoding = r.apparent_encoding
        print('url[%s], code[%d]' % (url, r.status_code))
        if r.status_code == 200:
            return r.text
        return None

    @staticmethod
    def parse_page(content):
        soup = BeautifulSoup(content, 'html.parser')
        tbody = soup.find('tbody')
        results = []
        for tr in tbody.find_all('tr'):
            if '文档名不规范' in tr.find('td', class_='col-delete-reason').text:
                title: str = tr.get_attribute_list('data-title')[0]
                if title.endswith('..docx'):
                    title = title.replace('..docx', '')
                    aids = tr.get_attribute_list('data-aid')[0]
                    results.append({'aids': aids, 'title': title})
        return results


if __name__ == "__main__":
    '''
    注意：需要以该方式启动的浏览器：
    win: chrome.exe --remote-debugging-port=9222
    mac：/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome  --remote-debugging-port=9222&
    '''
    loop.run_until_complete(main())
