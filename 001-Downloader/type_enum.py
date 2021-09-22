#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Description:dy_download.py
@Date       :2021/08/14
@Author     :xhunmon
@Mail       :xhunmon@gmail.com
"""

from enum import Enum


class PrintType(Enum):
    log = 1
    total = 2
    downloading = 3
    success = 4
    failed = 5
