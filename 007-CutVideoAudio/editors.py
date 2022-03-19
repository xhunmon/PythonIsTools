#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Description:editing.py 所有视频类的基类，负责与UI界面的绑定
@Date       :2022/03/14
@Author     :xhunmon
@Mail       :xhunmon@gmail.com
"""
import time
from threading import Lock

import requests
from my_fake_useragent import UserAgent

from type_enum import PrintType
from utils import Config

ua = UserAgent(family='chrome')


class Editors(object):
    func_ui_print = None
    __mutex_total = Lock()
    __mutex_success = Lock()
    __mutex_failed = Lock()
    __mutex_bmg = Lock()
    __count_total = 0
    __count_success = 0
    __count_failed = 0
    __count_bmg = 0
    __beijing_time = 0  # 在线北京时间

    def __init__(self):
        self._headers = {'user-agent': ua.random()}
        self.get_beijing_time()

    @staticmethod
    def print_hint():
        """显示初始提示信息"""
        Editors.print_ui(
            """
程序原理：
\t1、随机裁剪掉视频头尾；
\t2、随机改变视频帧率和比特率；
\t3、随机更换视频bgm；
\t4、保证每次输出不重复。
使用说明：
\t1、必须安装FFmpeg；
\t2、最短bgm长度大于最大视频长度。
            """
        )

    def start(self, ffmpeg, video, music, dst):
        """业务逻辑由子类实现"""
        pass

    @staticmethod
    def print_ui(txt):
        """在界面显示内容"""
        Editors.print_all_ui(txt=txt)  # 打印日志

    @staticmethod
    def print_all_ui(txt, print_type: PrintType = PrintType.log):
        """通知ui中func_ui_print更新内容"""
        if Editors.func_ui_print is not None:
            Editors.func_ui_print(txt=txt, print_type=print_type)

    @staticmethod
    def get_beijing_time():
        """静态方法：获取在线的北京时间"""
        if Editors.__beijing_time > 0:
            return Editors.__beijing_time
        try:
            response = requests.get(url='http://www.beijing-time.org/t/time.asp', headers={'user-agent': ua.random()})
            result = response.text
            data = result.split("\r\n")
            year = data[1][len("nyear") + 1: len(data[1]) - 1]
            month = data[2][len("nmonth") + 1: len(data[2]) - 1]
            day = data[3][len("nday") + 1: len(data[3]) - 1]
            # wday = data[4][len("nwday")+1 : len(data[4])-1]
            hrs = data[5][len("nhrs") + 1: len(data[5]) - 1]
            minute = data[6][len("nmin") + 1: len(data[6]) - 1]
            sec = data[7][len("nsec") + 1: len(data[7]) - 1]

            beijinTimeStr = "%s/%s/%s %s:%s:%s" % (year, month, day, hrs, minute, sec)
            beijinTime = time.strptime(beijinTimeStr, "%Y/%m/%d %X")
            Editors.__beijing_time = int(time.mktime(beijinTime))
        except:
            pass
        return Editors.__beijing_time

    @staticmethod
    def is_expired():
        """静态方法：判断是否已过期"""
        if Editors.__beijing_time == 0:  # 还没获取到时间
            return True
        expired_time_str = time.strptime(Config.instance().get_expired_time(), "%Y/%m/%d %X")
        expired_time_int = int(time.mktime(expired_time_str))
        return Editors.__beijing_time > expired_time_int

    @staticmethod
    def add_total_count(count=1):
        """静态方法：添加总下载任务数"""
        Editors.__mutex_total.acquire()
        Editors.__count_total += count
        Editors.__mutex_total.release()
        Editors.print_all_ui(txt="视频总数：%d" % Editors.__count_total, print_type=PrintType.total)

    @staticmethod
    def add_bgm_count(count=1):
        """静态方法：添加总下载任务数"""
        Editors.__mutex_bmg.acquire()
        Editors.__count_bmg += count
        Editors.__mutex_bmg.release()
        Editors.print_all_ui(txt="bmg数量：%d" % Editors.__count_bmg, print_type=PrintType.bgm)

    @staticmethod
    def get_total_count():
        """静态方法：获取总下载任务数"""
        return Editors.__count_total

    @staticmethod
    def get_bgm_count():
        """静态方法：获取正在下载任务数"""
        return Editors.__count_bmg

    @staticmethod
    def add_success_count():
        """静态方法：添加下载成功任务数"""
        Editors.__mutex_success.acquire()
        Editors.__count_success += 1
        Editors.__mutex_success.release()
        # 成功一条，减正在下载的一条
        Editors.print_all_ui(txt="已完成：%d" % Editors.__count_success, print_type=PrintType.success)

    @staticmethod
    def get_success_count():
        """静态方法：获取下载成功任务数"""
        return Editors.__count_success

    @staticmethod
    def add_failed_count():
        """静态方法：添加下载失败任务数"""
        Editors.__mutex_failed.acquire()
        Editors.__count_failed += 1
        Editors.__mutex_failed.release()
        # 失败一条，减正在下载的一条
        Editors.print_all_ui(txt="已失败：%d" % Editors.__count_failed, print_type=PrintType.failed)

    @staticmethod
    def get_failed_count():
        """静态方法：获取下载失败任务数"""
        return Editors.__count_failed
