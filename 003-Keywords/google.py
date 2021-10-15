#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Description: google相关获取
@Date       :2021/10/08
@Author     :xhunmon
@Mail       :xhunmon@gmail.com
"""
import csv
import os.path

import matplotlib.pyplot as plt

from mypytrends.request import TrendReq


class GoogleTrend(object):
    def __init__(self):
        self.data = {}

    def search(self, keyword, path, hl='en-US', proxies=False, retries=2, timeframe='2019-10-01 2021-10-11'):
        if not os.path.exists(path):
            os.makedirs(path)
        csv_file = os.path.join(path, "%s.csv" % keyword)
        self.__save_line(csv_file, ['keyword', 'no', 'top keyword', 'top range', 'rising keyword', 'rising range'],
                         mode='w')
        tr = self.__get_req(hl=hl, proxies=proxies, retries=retries)
        self.__search_trends(path, keyword, timeframe, tr)
        first_data = self.__search_related_queries(keyword, timeframe, tr)
        tops = first_data[keyword]['top']
        risings = first_data[keyword]['rising']
        top_size = len(tops)
        rising_size = len(risings)
        max_len = top_size if top_size > rising_size else rising_size
        for i in range(max_len):
            top_key, top_range, rising_key, rising_range = None, None, None, None
            if i < top_size:
                top_key = tops[i]['keyword']
                top_range = tops[i]['range']
            if i < rising_size:
                rising_key = risings[i]['keyword']
                rising_range = risings[i]['range']
            self.__save_line(csv_file, [keyword, i, top_key, top_range, rising_key, rising_range])
        self.__save_line(csv_file, ['', ''])  # 换行
        for top in tops:
            top_key = top['keyword']
            try:
                self.__sub_search(top_key, path, csv_file, timeframe, tr)
                self.__save_line(csv_file, ['', ''])  # 换行
            except:
                pass
        for rising in risings:
            rising_key = rising['keyword']
            try:
                self.__sub_search(rising_key, path, csv_file, timeframe, tr)
                self.__save_line(csv_file, ['', ''])  # 换行
            except:
                pass

    def __sub_search(self, keyword, path, csv_file, timeframe, tr):
        self.__search_trends(path, keyword, timeframe, tr)
        first_data = self.__search_related_queries(keyword, timeframe, tr)
        tops = first_data[keyword]['top']
        risings = first_data[keyword]['rising']
        top_size = len(tops)
        rising_size = len(risings)
        max_len = top_size if top_size > rising_size else rising_size
        for i in range(max_len):
            top_key, top_range, rising_key, rising_range = None, None, None, None
            if i < top_size:
                top_key = tops[i]['keyword']
                top_range = tops[i]['range']
                try:
                    self.__search_trends(path, top_key, timeframe, tr)
                except:
                    pass
            if i < rising_size:
                rising_key = risings[i]['keyword']
                rising_range = risings[i]['range']
                try:
                    self.__search_trends(path, rising_key, timeframe, tr)
                except:
                    pass
            self.__save_line(csv_file, [keyword, i, top_key, top_range, rising_key, rising_range])

    def __search_related_queries(self, keyword, timeframe, tr: TrendReq) -> {}:
        tr.build_payload([keyword, ], cat=0, timeframe=timeframe, geo='', gprop='')
        related = tr.related_queries()
        r_value = [related[key] for key in related][0]
        r_top = r_value['top']
        r_rising = r_value['rising']
        tops = []
        risings = []
        print('---------top--------')
        for index, row in r_top.iterrows():
            print(index, row["query"], row["value"])
            tops.append({"keyword": row["query"], "range": row["value"]})
        print('---------rising--------')
        for index, row in r_rising.iterrows():
            print(index, row["query"], row["value"])
            risings.append({"keyword": row["query"], "range": row["value"]})
        return {keyword: {"top": tops, "rising": risings}}

    def __search_trends(self, path, keyword, timeframe, tr: TrendReq):
        tr.build_payload([keyword, ], cat=0, timeframe=timeframe, geo='', gprop='')
        trends = tr.interest_over_time()
        x_data = []
        y_data = []
        year = ''
        month = ''
        temp_value = 0
        count = 0
        for time, row in trends.iterrows():
            value = row[keyword]
            date = str(time)
            t = date.split(' ')[0] if ' ' in date else date
            y = t.split('-')[0]
            m = t.split('-')[1]
            if month != m and month != '':
                y_data.append(int(temp_value / count))
                x_data.append(year[2:] + "-" + month)
                year = ''
                month = ''
                count = 0
                temp_value = 0
                continue
            year = y
            month = m
            count += 1
            temp_value += value
        y_data.append(int(temp_value / count))
        x_data.append(year[2:] + "-" + month)
        print(y_data)
        print(x_data)
        print('%s : %d - %d' % (keyword, len(y_data), len(x_data)))
        # self.__draw_graph(x_data, y_data, 'pci.jpg', keyword)
        self.__draw_histogram(x_data, y_data, os.path.join(path, "%s.jpg" % keyword), keyword)

    def __draw_histogram(self, x: [], y: [], path, title, x_name='date', y_name='trends'):
        plt.figure(dpi=60)
        plt.ylim(0, 100)
        plt.style.use('ggplot')
        plt.bar(x, y, label=title)
        # 显示图例（使绘制生效）
        plt.legend()
        # 横坐标名称
        plt.xlabel(x_name)
        # 纵坐标名称
        plt.ylabel(y_name)
        # 横坐标显示倒立
        plt.xticks(rotation=90)
        # 保存图片到本地
        plt.savefig(path)
        # 显示图片
        # plt.show()

    def __draw_graph(self, x: [], y: [], path, title, x_name='date', y_name='trends'):
        plt.figure()
        '''绘制第一条数据线
        1、节点为圆圈
        2、线颜色为红色
        3、标签名字为y1-data
        '''
        plt.ylim(0, 100)
        plt.plot(x, y, marker='o', color='r', label=title)
        # 显示图例（使绘制生效）
        plt.legend()
        # 横坐标名称
        plt.xlabel(x_name)
        # 纵坐标名称
        plt.ylabel(y_name)
        # 横坐标显示倒立
        plt.xticks(rotation=90)
        # 保存图片到本地
        plt.savefig(path)
        # 显示图片
        # plt.show()

    def __save_line(self, path, line, mode='a'):
        with open(path, mode=mode, encoding='utf-8', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(line)
            csvfile.close()

    def __get_req(self, hl='en-US', proxies=False, retries=2) -> TrendReq:
        if proxies:
            return TrendReq(hl=hl, tz=360, timeout=(10, 35), proxies=['socks5h://127.0.0.1:1080', ], retries=retries,
                            backoff_factor=0.1, requests_args={'verify': False})
        else:
            return TrendReq(hl=hl, tz=360, timeout=(10, 35), retries=retries, backoff_factor=0.1,
                            requests_args={'verify': False})