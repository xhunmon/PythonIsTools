#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Description: tool
@Date       :2023/03/31
@Author     :xhunmon
@Mail       :xhunmon@126.com
"""
import configparser
import json
import os
import platform
import re
import threading

import openai


def get_domain(url: str = None):
    # http://youtube.com/watch
    return re.match(r"(http://|https://).*?\/", url, re.DOTALL).group(0)


class ConfigIni(object):
    _instance_lock = threading.Lock()

    def __init__(self):
        parent_dir = os.path.dirname(os.path.abspath(__file__))
        conf_path = os.path.join(parent_dir, 'config.ini')
        self.conf = configparser.ConfigParser()
        self.conf.read(conf_path, encoding="utf-8")

    @classmethod
    def instance(cls, *args, **kwargs):
        with ConfigIni._instance_lock:
            if not hasattr(ConfigIni, "_instance"):
                ConfigIni._instance = ConfigIni(*args, **kwargs)
        return ConfigIni._instance

    def get_expired_time(self):
        return self.conf.get("common", "expired_time")

    def get_version_name(self):
        return self.conf.get("common", "version_name")

    def get_version_code(self):
        return self.conf.get("common", "version_code")

    def get_title(self):
        return self.conf.get("common", "title")

    def get_email(self):
        return self.conf.get("common", "email")


class Config:
    sep = ""
    pre_tips = "Tips:"
    # baseDir = os.path.dirname(os.path.realpath(sys.argv[0]))
    base_dir = ''
    md_sep = '\n\n' + '-' * 10 + '\n'
    encodings = ["utf8", "gbk"]

    api_key = ""
    api_base = ""
    model = ""
    prompt = []
    stream = True
    response = False
    proxy = ""
    folder = ""
    config_path = ""
    repeat = True

    def __init__(self, dir: str) -> None:
        self.base_dir = dir
        if platform.system() == 'Darwin':  # MacOS：use pyinstaller pack issue.
            if '/Contents/MacOS' in dir:  # ./GPT-UI.app/Contents/MacOS/ --> ./
                app_path = dir.rsplit('/Contents/MacOS')[0]
                self.base_dir = app_path[:app_path.rindex('/')]
        self.config_path = os.path.join(self.base_dir, "config.json")
        self.cfg = {}
        self.load(self.config_path)

    def load(self, file):
        if not os.path.exists(file):
            return
        with open(file, "r") as f:
            self.cfg = json.load(f)
        c = self.cfg
        self.api_key = c.get("api_key", c.get("key", openai.api_key))  # compatible with history key
        self.api_base = c.get("api_base", openai.api_base)
        self.model = c.get("model", "gpt-3.5-turbo")
        self.stream = c.get("stream", True)
        self.response = c.get("response", False)
        self.proxy = c.get("proxy", "")
        self.folder = c.get("folder", self.base_dir)
        self.repeat = c.get("repeat", True)

    def get(self, key, default=None):
        return self.cfg.get(key, default)

    def click_create(self):
        results = {
            "key": "",
            "api_base": "",
            "model": "gpt-3.5-turbo",
            "stream": True,
            "response": True,
            "folder": "",
            "repeat": False,
            "proxy": "",
            "prompt": []
        }
        self.write_json(results, self.config_path)

    def write_json(self, content, file_path):
        path, file_name = os.path.split(file_path)
        if path and not os.path.exists(path):
            os.makedirs(path)
        with open(file_path, 'w') as f:
            json.dump(content, f, ensure_ascii=False)
            f.close()

    def update(self, path: str):
        if not path.endswith(".json"):
            return False
        if path and not os.path.exists(path):
            return False
        self.load(path)
        return True

    def update_by_content(self, key: str = None, model: str = None, folder: str = None, proxy: str = None):
        if key and len(key.strip()) > 0 and not key.startswith(Config.pre_tips):
            self.api_key = key
        else:
            self.api_key = ''
        if model and len(model.strip()) > 0 and not model.startswith(Config.pre_tips):
            self.model = model
        else:
            self.model = 'gpt-3.5-turbo'
        if folder and len(folder.strip()) > 0 and not folder.startswith(Config.pre_tips):
            self.folder = folder
        else:
            self.folder = self.base_dir
        if proxy.startswith(Config.pre_tips):
            self.proxy = None
        else:
            self.proxy = proxy if len(proxy.strip()) > 0 else None
