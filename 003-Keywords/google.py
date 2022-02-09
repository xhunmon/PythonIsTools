#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Description: google相关获取
@Date       :2021/10/08
@Author     :xhunmon
@Mail       :xhunmon@gmail.com
"""
import xlsxwriter
import os.path

import matplotlib.pyplot as plt

from mypytrends.request import TrendReq


class GoogleTrend(object):
    def __init__(self):
        self.data = {}
        self.max_column = 0

    def search(self, keyword, path, hl='en-US', proxies=False, retries=2, timeframe='2019-10-01 2022-01-01'):
        if not os.path.exists(path):
            os.makedirs(path)
        csv_file = os.path.join(path, "%s.xlsx" % keyword)
        workbook = xlsxwriter.Workbook(csv_file)
        # 设置整个工作薄的格式
        workbook.formats[0].set_align('vcenter')  # 单元格垂直居中
        # workbook.formats[0].set_text_wrap()  # 自动换行

        worksheet = workbook.add_worksheet('sheet1')
        i_row, i_column = 0, 0
        first_row = ['keyword', 'no', 'top keyword', 'top range', 'rising keyword', 'rising range']
        self.max_column = len(first_row)
        for i in range(self.max_column):
            worksheet.write(i_row, i, first_row[i])
        i_row += 1
        tr = self.__get_req(hl=hl, proxies=proxies, retries=retries)
        i_row = self.__search_trends(i_row, worksheet, path, keyword, timeframe, tr)
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
            max_datas = [keyword, i, top_key, top_range, rising_key, rising_range]
            for j in range(len(max_datas)):
                worksheet.write(i_row, j, max_datas[j])
            i_row += 1
            # self.__save_line(csv_file, [keyword, i, top_key, top_range, rising_key, rising_range])
        # self.__save_line(csv_file, ['', ''])  # 换行
        i_row += 1
        for top in tops:
            top_key = top['keyword']
            try:
                i_row = self.__sub_search(top_key, i_row, worksheet, path, csv_file, timeframe, tr)
                # self.__save_line(csv_file, ['', ''])  # 换行
                i_row += 1
            except:
                pass
        for rising in risings:
            rising_key = rising['keyword']
            try:
                i_row = self.__sub_search(rising_key, i_row, worksheet, path, csv_file, timeframe, tr)
                # self.__save_line(csv_file, ['', ''])  # 换行
                i_row += 1
            except:
                pass
        workbook.close()

    def __sub_search(self, i_row, worksheet, keyword, path, csv_file, timeframe, tr):
        i_row = self.__search_trends(i_row, worksheet, path, keyword, timeframe, tr)
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
                    i_row = self.__search_trends(i_row, worksheet, path, top_key, timeframe, tr)
                except:
                    pass
            if i < rising_size:
                rising_key = risings[i]['keyword']
                rising_range = risings[i]['range']
                try:
                    i_row = self.__search_trends(i_row, worksheet, path, rising_key, timeframe, tr)
                except:
                    pass
            # self.__save_line(csv_file, [keyword, i, top_key, top_range, rising_key, rising_range])
            max_datas = [keyword, i, top_key, top_range, rising_key, rising_range]
            for j in range(len(max_datas)):
                worksheet.write(i_row, j, max_datas[j])
                i_row += 1

        return i_row

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

    def __search_trends(self, i_row, worksheet, path, keyword, timeframe, tr: TrendReq):
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
        img_path = os.path.join(path, "%s.jpg" % keyword)
        self.__draw_histogram(x_data, y_data, img_path, keyword)
        worksheet.insert_image(i_row - 1, self.max_column, img_path,
                               {'x_scale': 0.2, 'y_scale': 0.2, 'object_position': 1})
        i_row += 1
        return i_row

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
