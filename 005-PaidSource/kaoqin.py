"""
@Description: excel表的常规操作，这里实现统计考勤
@Date       :2022/02/21
@Author     :xhunmon
@Mail       :xhunmon@gmail.com
"""

import pandas as pd
import calendar
from pandas._libs.tslibs.timestamps import Timestamp


def get_days(year, month):  # 获取输出日期的列明
    dates = calendar.monthrange(year, month)
    week = dates[0]  # 1号那天是星期几
    days = dates[1]  # 总共的天数
    print(dates)
    index_time = []
    for day in range(1, days):
        index_time.append('{}-{}-{}  星期{}'.format(year, month, day, (week + day) % 7))
    print(index_time)
    return index_time


def parse_excel(csv_file, out_file, names, dates):
    df = pd.read_excel(csv_file, sheet_name='Sheet')  # 从文件和表格名称读取
    datas = df.values
    size = len(df)
    print('总共有{}行数据'.format(size))
    results = {}
    for name in names:  # 我是根据名字统计
        results.update({name: ['' for x in range(len(dates))]})  # 默认生成每个日期的空格
    for col in range(0, size):
        s_name = datas[col][2]  # 打印一下就知道去的那是哪里列的值了
        t_time: Timestamp = datas[col][6]  # 我这里是时间戳，用type(datas[col][6])打印类型可知
        if s_name not in names:
            continue
        # 获取这天是哪一天的，name_datas是哪个人对应的列表数据
        d, h, m, name_datas = t_time.day, t_time.hour, t_time.minute, results.get(s_name)
        # 早上 9:00前打卡，下午18:00后打卡，取一天最早和最晚的一次即可，门禁可能有很多数据
        tt = '2022-1-{} {}:{}'.format(d, h, m)
        old = name_datas[d - 1]  # 下标
        if len(old) < 5:  # 空的
            name_datas[d - 1] = '{} 早 {};'.format(tt, '' if h < 9 else '异常')  # 上班打卡
        else:
            # 去除第一个：
            first = old.split(';')[0]
            last = '{} 晚 {}'.format(tt, '' if h >= 18 else '异常')
            name_datas[d - 1] = '{};{}'.format(first, last)
    print(results)
    df_write = pd.DataFrame(results, index=dates)
    df_write.to_excel(out_file, index=True)  # 写入输出表格数据


if __name__ == '__main__':
    names = ['x1', 'x2', 'x3', 'x4', 'x5']  # 要统计那些人
    parse_excel('data/一月考勤.xls', 'data/out_kaoqin.xls', names, get_days(2022, 1))
