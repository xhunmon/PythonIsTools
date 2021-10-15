#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import configparser

import os


class Config:
    __v2ray_core_path = None

    def __init__(self):
        self.config = configparser.ConfigParser()
        parent_dir = os.path.dirname(os.path.abspath(__file__))
        self.config_path = os.path.join(parent_dir, 'config.json')
        self.json_path = os.path.join(parent_dir, 'json_template')
        # self.config.read(self.config_path)

    def get_path(self, key):
        # return self.config.get('path', key)
        return self.config_path

    def get_data(self, key):
        return self.config.get('data', key)

    def set_data(self, key, value):
        self.config.set('data', key, value)
        self.config.write(open(self.config_path, "w"))

    @staticmethod
    def set_v2ray_core_path(dir: str):
        """设置当前v2ray_core程序的目录"""
        Config.__v2ray_core_path = dir

    @staticmethod
    def get_v2ray_core_path():
        """获取当前v2ray_core程序的目录"""
        return Config.__v2ray_core_path
