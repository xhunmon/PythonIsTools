#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Description: 关键词获取
@Date       :2021/09/22
@Author     :xhunmon
@Mail       :xhunmon@gmail.com
"""
# from amazon import run_api
import os
import time

import xlwt

import run_api
import v2ray_util as v2util
from google import GoogleTrend
from openpyxl import load_workbook


def Write_Img():
    import xlsxwriter
    book = xlsxwriter.Workbook('test_source.xlsx')
    sheet = book.get_worksheet_by_name('Sheet1')
    # sheet = book.add_worksheet('demo')
    # sheet.insert_image(0, 5, 'Necklace/Necklace.jpg', {'x_scale': 0.2, 'y_scale': 0.2, 'object_position': 1})
    print(sheet)
    book.close()


def read_xlsl():
    import pandas as pd
    df = pd.read_excel('test_source.xlsx', sheet_name='Sheet1')
    data = df.values
    print(data)
    print('\n')
    df = pd.read_excel('test_souce1.xlsx', sheet_name='2021xuqiu')
    data = df.values
    print(data)



if __name__ == "__main__":
    # v2util.restart_v2ray()
    # 获取amazon中相关词，代理需要看：middlewares.py，
    # results = run_api.crawl_amazon(['plastic packaging', ])
    # 把通过google trends查出关键词相关词，以及其词的趋势图，如：
    # GoogleTrend().search('Necklace', 'Necklace', proxies=True, timeframe='2021-01-01 2022-01-01')
    # v2util.kill_all_v2ray()
    # Write_Img()
    read_xlsl()
