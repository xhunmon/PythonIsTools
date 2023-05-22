#!/usr/bin/python3.9
# -*- coding: utf-8 -*-
"""
@Time    : 2023/5/18 14:38
@Author  : xhunmon
@Email   : xhunmon@126.com
@File    : tran_test.py
@Desc    : 
"""
import re

from load_srt import Translator
import time
from utils import *


def t_test(srt_source):
    sub_start = '00:02:00'
    v_start = '00:00:17'


def translate_callback(status, **kwargs):
    print(status)
    print(kwargs["src"])
    print(kwargs["dst"])
    print(kwargs["msg"])


if __name__ == '__main__':
    tl = Translator()
    tl.add_callback(translate_callback)
    try:
        tl.translate_file("output/test.srt", "output/test_out.srt")
    except Exception as e:
        print(e)
