#!/usr/bin/python3.9
# -*- coding: utf-8 -*-
"""
@Time    : 2023/5/22 11:44
@Author  : xhunmon
@Email   : xhunmon@126.com
@File    : main.py
@Desc    : 使用案例
"""
import sys

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from youtube import *

if __name__ == '__main__':
    meta = {
        "title": '标题',
        "description": "描述内容",
        "tags": ['标签1', '标签2', '标签3'],
        "edit": False,
        "playlist_title": '播放列表1',
        "schedule": ""
    }

    executable_path = "chromedriver"
    options = Options()
    # TODO - 以下配置是为了打开现有的浏览器，公用cookie，安全有效，需要提起配置。
    if sys.platform == 'linux':
        print("Current OS is Linux.")
    elif sys.platform == 'darwin':
        print("Current OS is mac OS.")
        executable_path = '/usr/local/bin/chromedriver'
        options.debugger_address = 'localhost:9222'
    elif sys.platform == 'win32':
        print("Current OS is Windows.")

    __g_browser = webdriver.Chrome(executable_path=executable_path, chrome_options=options)
    __g_browser.implicitly_wait(10)  # 设置查找运算智能等待超时时间

    yt = YtbUploader()
    yt.upload(__g_browser, 'xxx/xxx.mp4', options, None)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
