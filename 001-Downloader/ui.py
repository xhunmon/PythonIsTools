#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Description: 用于GUI界面显示
@Date       :2021/08/14
@Author     :xhunmon
@Mail       :xhunmon@gmail.com
"""
from tkinter import *
from tkinter.filedialog import (askdirectory)

from douyin.dy_download import DouYin
from downloader import Downloader
from kuaishou.ks_download import KuaiShou
from type_enum import PrintType
from utils import *


# from PIL import Image, ImageTk


class Ui(Frame):
    def __init__(self, master=None):
        global bg_color
        bg_color = '#373434'
        Frame.__init__(self, master, bg=bg_color)
        self.ui_width = 0
        self.pack(expand=YES, fill=BOTH)
        self.window_init()
        self.createWidgets()

    def window_init(self):
        self.master.title(
            '欢迎使用-自媒体资源下载器' + Config.instance().get_version_name() + '，本程序仅用于学习交流！如有疑问请联系：xhunmon@gmail.com')
        self.master.bg = bg_color
        width, height = self.master.maxsize()
        # self.master.geometry("{}x{}".format(width, height))
        self.master.geometry("%dx%d+%d+%d" % (width / 2, height / 2, width / 4, height / 4))
        self.ui_width = width / 2

    def createWidgets(self):
        # fm1
        self.fm1 = Frame(self, bg=bg_color)
        self.fm1.pack(fill='y', pady=10)
        # window没有原生PIL 64位支持
        # load = Image.open('res/logo.png')
        # load.thumbnail((38, 38), Image.ANTIALIAS)
        # initIamge = ImageTk.PhotoImage(load)
        # self.panel = Label(self.fm1, image=initIamge, bg=bg_color)
        # self.panel.image = initIamge
        # self.panel.pack(side=LEFT, fill='y', padx=5)
        self.titleLabel = Label(self.fm1, text="资源下载器", font=('微软雅黑', 32), fg="white", bg=bg_color)
        self.titleLabel.pack(side=LEFT, fill='y')

        # fm2
        self.fm2 = Frame(self, bg=bg_color)
        self.fm2.pack(side=TOP, fill="y")
        self.fm2_right = Frame(self.fm2, bg=bg_color)
        self.fm2_right.pack(side=RIGHT, padx=0, pady=10, expand=YES, fill='y')
        self.fm2_left = Frame(self.fm2, bg=bg_color)
        self.fm2_left.pack(side=LEFT, padx=15, pady=10, expand=YES, fill='x')
        self.fm2_left_top = Frame(self.fm2_left, bg=bg_color)
        self.fm2_left_bottom = Frame(self.fm2_left, bg=bg_color)

        self.downloadBtn = Button(self.fm2_right, text='开始下载', fg="#ffffff", bg=bg_color,
                                  font=('微软雅黑', 18), command=self.start_download)
        self.downloadBtn.pack(side=RIGHT)

        self.dirEntry = Entry(self.fm2_left_top, font=('微软雅黑', 14), width='72', fg='#ffffff', bg=bg_color, bd=1)
        self.dirEntry.config(insertbackground='#ffffff')
        # self.set_dir(os.path.dirname(os.path.realpath(sys.argv[0])))
        self.dirBtn = Button(self.fm2_left_top, text='选择保存目录：', bg=bg_color, fg='#aaaaaa',
                             font=('微软雅黑', 12), width='10', command=self.save_dir)
        self.dirBtn.pack(side=LEFT)
        self.dirEntry.pack(side=LEFT, fill='y')
        self.fm2_left_top.pack(side=TOP, fill='x')

        self.urlEntry = Entry(self.fm2_left_bottom, font=('微软雅黑', 14), width='72', fg='#ffffff', bg=bg_color, bd=1)
        self.urlEntry.config(insertbackground='#ffffff')
        self.urlButton = Button(self.fm2_left_bottom, text='清空下载地址：', bg=bg_color, fg='#aaaaaa',
                                font=('微软雅黑', 12), width='10', command=self.download_url)
        self.urlButton.pack(side=LEFT)
        self.urlEntry.pack(side=LEFT, fill='y')
        self.fm2_left_bottom.pack(side=TOP, pady=10, fill='x')

        # fm3 任务数状态
        self.fm3 = Frame(self, bg=bg_color, height=6)
        self.fm3.pack(side=TOP, fill="x")
        self.totalLabel = Label(self.fm3, width=10, text="预计总数：0", font=('微软雅黑', 12), fg="white", bg=bg_color)
        self.totalLabel.pack(side=LEFT, fill='y', padx=20)
        self.downloadingLabel = Label(self.fm3, width=10, text="正在下载：0", font=('微软雅黑', 12), fg="white", bg=bg_color)
        self.downloadingLabel.pack(side=LEFT, fill='y', padx=20)
        self.successLabel = Label(self.fm3, width=10, text="已完成：0", font=('微软雅黑', 12), fg="white", bg=bg_color)
        self.successLabel.pack(side=LEFT, fill='y', padx=20)
        self.failLabel = Label(self.fm3, width=10, text="已失败：0", font=('微软雅黑', 12), fg="white", bg=bg_color)
        self.failLabel.pack(side=LEFT, fill='y', padx=20)

        # fm4
        self.fm4 = Frame(self, bg=bg_color)
        self.fm4.pack(side=TOP, expand=YES, fill="both")
        self.logLabel = Label(self.fm4, anchor='w', wraplength=self.ui_width - 40, text="", font=('微软雅黑', 12),
                              fg="white",
                              bg=bg_color)
        self.logLabel.pack(side=TOP, fill='both', padx=20)

        # 注册回调
        Downloader.func_ui_print = self.func_ui_print
        # 判断是否有网络
        if Downloader.get_beijing_time() == 0:
            self.output("获取数据异常，请检查您的网络！")
        else:
            Downloader.print_hint()

    def save_dir(self):
        path = askdirectory()
        self.set_dir(path)

    def set_dir(self, path):
        self.dirEntry.delete(0, END)
        self.dirEntry.insert(0, path)

    def download_url(self):
        ground_truth = ''
        self.urlEntry.delete(0, END)
        self.urlEntry.insert(0, ground_truth)

    def output(self, txt):
        self.logLabel.config(text=txt)

    def func_ui_print(self, txt, print_type: PrintType = None):
        if print_type == PrintType.log:
            self.logLabel.config(text=txt)
        elif print_type == PrintType.total:
            self.totalLabel.config(text=txt)
        elif print_type == PrintType.downloading:
            self.downloadingLabel.config(text=txt)
        elif print_type == PrintType.success:
            self.successLabel.config(text=txt)
        elif print_type == PrintType.failed:
            self.failLabel.config(text=txt)

    def start_download(self):
        # 判断是否有网络
        if Downloader.get_beijing_time() == 0:
            self.output("获取数据异常，请检查您的网络！")
            return
        if Downloader.is_expired():
            self.output("授权证书已到期，请联系客服！")
            return
        url = self.urlEntry.get()
        path = self.dirEntry.get()
        domain = get_domain(url)
        if "kwaicdn" in domain or "kuaishou" in domain:
            downloader: KuaiShou = KuaiShou()
            # downloader.set_cookie()
        else:
            downloader: Downloader = DouYin()
        downloader_t = threading.Thread(target=downloader.start, args=(url, path))
        downloader_t.setDaemon(True)  # 设置守护进程，避免界面卡死
        downloader_t.start()
