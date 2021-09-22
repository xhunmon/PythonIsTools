#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Description:工具类
@Date       :2021/08/16
@Author     :xhunmon
@Mail       :xhunmon@gmail.com
"""
import threading
import configparser
import os
import re


def get_domain(url: str = None):
    """
    获取链接地址的域名
    :param url:
    :return:
    """
    # http://youtube.com/watch
    return re.match(r"(http://|https://).*?\/", url, re.DOTALL).group(0)


class Config(object):
    """
    配置文件的单例类
    """
    _instance_lock = threading.Lock()

    def __init__(self):
        parent_dir = os.path.dirname(os.path.abspath(__file__))
        conf_path = os.path.join(parent_dir, 'config.ini')
        self.conf = configparser.ConfigParser()
        self.conf.read(conf_path, encoding="utf-8")

    @classmethod
    def instance(cls, *args, **kwargs):
        with Config._instance_lock:
            if not hasattr(Config, "_instance"):
                Config._instance = Config(*args, **kwargs)
        return Config._instance

    def get_expired_time(self):
        return self.conf.get("common", "expired_time")

    def get_version_name(self):
        return self.conf.get("common", "version_name")

    def get_version_code(self):
        return self.conf.get("common", "version_code")
