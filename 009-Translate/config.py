# -*- coding: utf-8 -*-
"""
@Author  : Xhunmon 
@Time    : 2023/4/23 08:51
@FileName: config.py
@desc: 
"""
import configparser
import json
import locale
import os

from utils import *

__version__ = '1.0.0'
__email__ = 'xhunmon@126.com'
__wechet__ = 'VABlog'

language, encoding = locale.getdefaultlocale()


def is_zh_language():
    cache = get_cache(Key.LANGUAGE, None)
    # if cache == 'zh_CN' or language == 'zh_CN':
    #     return True
    # else:
    #     return False
    return True


class IniConfig(object):
    def __init__(self):
        asset_path = os.path.join(os.path.dirname(__file__), 'asset')
        language_path = os.path.join(asset_path, 'language.json')
        config_path = os.path.join(asset_path, 'config.ini')
        ch_ini = os.path.join(asset_path, 'ch.ini')
        en_ini = os.path.join(asset_path, 'en.ini')
        ini = ch_ini if is_zh_language() else en_ini
        self.language = configparser.ConfigParser()
        self.language.read(ini, encoding='utf-8')
        self.cfg = configparser.ConfigParser()
        self.cfg.read(config_path, encoding='utf-8')
        with open(language_path, 'r') as f:
            self.trl = json.load(f)
            f.close()

    def full(self, tag, name):
        return self.language[tag][name]

    def main(self, name):
        return self.full('Main', name)

    def settings(self, name):
        return self.full('Settings', name)

    def loading(self, name):
        return self.full('Loading', name)

    def language(self, name):
        return self.full('Language', name)

    def config(self, name):
        return self.cfg['Config'][name]

    def translate(self):
        return self.trl


conf = IniConfig()
