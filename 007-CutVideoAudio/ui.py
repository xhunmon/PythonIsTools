#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Description: 用于GUI界面显示
@Date       :2021/08/14
@Author     :xhunmon
@Mail       :xhunmon@gmail.com
"""
from tkinter import *
from tkinter.filedialog import (askdirectory, askopenfilename)

from editors import Editors
from ff_cut import ListCut
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
            '欢迎使用-音视频批量截切工具' + Config.instance().get_version_name() + '  如有疑问请联系：xhunmon@gmail.com')
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
        self.titleLabel = Label(self.fm1, text="视频批量剪辑，适合一个视频多账号发送", font=('微软雅黑', 28), fg="white", bg=bg_color)
        self.titleLabel.pack(side=LEFT, fill='y')

        # fm2
        self.fm2 = Frame(self, bg=bg_color)
        self.fm2.pack(side=TOP, fill="y")
        self.fm2_right = Frame(self.fm2, bg=bg_color)
        self.fm2_right.pack(side=RIGHT, padx=0, pady=10, expand=YES, fill='y')
        self.fm2_left = Frame(self.fm2, bg=bg_color)
        self.fm2_left.pack(side=LEFT, padx=15, pady=10, expand=YES, fill='x')
        self.fm2_left_ffmpeg = Frame(self.fm2_left, bg=bg_color)
        self.fm2_left_souce_video = Frame(self.fm2_left, bg=bg_color)
        self.fm2_left_souce_music = Frame(self.fm2_left, bg=bg_color)
        self.fm2_left_dst = Frame(self.fm2_left, bg=bg_color)

        self.downloadBtn = Button(self.fm2_right, text='开始', fg="#aaaaaa", bg=bg_color,
                                  font=('微软雅黑', 18), command=self.start_download)
        self.downloadBtn.pack(side=RIGHT)

        self.ffmFileEntry = Entry(self.fm2_left_ffmpeg, font=('微软雅黑', 14), width='72', fg='#ffffff', bg=bg_color, bd=1)
        self.ffmFileEntry.config(insertbackground='#ffffff')
        self.ffmFileBtn = Button(self.fm2_left_ffmpeg, text='选择FFmpeg程序：', bg=bg_color, fg='#aaaaaa',
                                 font=('微软雅黑', 12), width='12', command=self.save_file)
        self.ffmFileBtn.pack(side=LEFT)
        self.ffmFileEntry.pack(side=LEFT, fill='y')
        self.fm2_left_ffmpeg.pack(side=TOP, fill='x')

        self.videoDirEntry = Entry(self.fm2_left_souce_video, font=('微软雅黑', 14), width='72', fg='#ffffff', bg=bg_color,
                                   bd=1)
        self.videoDirEntry.config(insertbackground='#ffffff')
        self.videoDirBtn = Button(self.fm2_left_souce_video, text='选择视频源目录：', bg=bg_color, fg='#aaaaaa',
                                  font=('微软雅黑', 12), width='12', command=self.save_dir)
        self.videoDirBtn.pack(side=LEFT)
        self.videoDirEntry.pack(side=LEFT, fill='y')
        self.fm2_left_souce_video.pack(side=TOP, fill='x')

        self.musicDirEntry = Entry(self.fm2_left_souce_music, font=('微软雅黑', 14), width='72', fg='#ffffff', bg=bg_color,
                                   bd=1)
        self.musicDirEntry.config(insertbackground='#ffffff')
        self.musicDirBtn = Button(self.fm2_left_souce_music, text='选择bmg源目录：', bg=bg_color, fg='#aaaaaa',
                                  font=('微软雅黑', 12), width='12', command=self.save_dir)
        self.musicDirBtn.pack(side=LEFT)
        self.musicDirEntry.pack(side=LEFT, fill='y')
        self.fm2_left_souce_music.pack(side=TOP, fill='x')

        self.dstEntry = Entry(self.fm2_left_dst, font=('微软雅黑', 14), width='72', fg='#ffffff', bg=bg_color, bd=1)
        self.dstEntry.config(insertbackground='#ffffff')
        self.dstBtn = Button(self.fm2_left_dst, text='选择输出目录：', bg=bg_color, fg='#aaaaaa',
                             font=('微软雅黑', 12), width='12', command=self.download_url)
        self.dstBtn.pack(side=LEFT)
        self.dstEntry.pack(side=LEFT, fill='y')
        self.fm2_left_dst.pack(side=TOP, pady=10, fill='x')

        # fm3 任务数状态
        self.fm3 = Frame(self, bg=bg_color, height=6)
        self.fm3.pack(side=TOP, fill="x")
        self.totalLabel = Label(self.fm3, width=10, text="视频总数：0", font=('微软雅黑', 12), fg="white", bg=bg_color)
        self.totalLabel.pack(side=LEFT, fill='y', padx=20)
        self.totalBgmLabel = Label(self.fm3, width=10, text="bgm总数：0", font=('微软雅黑', 12), fg="white", bg=bg_color)
        self.totalBgmLabel.pack(side=LEFT, fill='y', padx=20)
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
        Editors.func_ui_print = self.func_ui_print
        # 判断是否有网络
        if Editors.get_beijing_time() == 0:
            self.output("获取数据异常，请检查您的网络！")
        else:
            Editors.print_hint()

    def save_dir(self):
        path = askdirectory()
        self.set_dir(path)

    def save_file(self):
        path = askopenfilename()
        self.set_dir(path)

    def set_dir(self, ffmpeg=None, video=None, music=None, dst=None):
        if ffmpeg:
            self.ffmFileEntry.delete(0, END)
            self.ffmFileEntry.insert(0, ffmpeg)
        if video:
            self.videoDirEntry.delete(0, END)
            self.videoDirEntry.insert(0, video)
        if music:
            self.musicDirEntry.delete(0, END)
            self.musicDirEntry.insert(0, music)
        if dst:
            self.dstEntry.delete(0, END)
            self.dstEntry.insert(0, dst)

    def download_url(self):
        ground_truth = ''
        self.dstEntry.delete(0, END)
        self.dstEntry.insert(0, ground_truth)

    def output(self, txt):
        self.logLabel.config(text=txt)

    def func_ui_print(self, txt, print_type: PrintType = None):
        if print_type == PrintType.log:
            self.logLabel.config(text=txt)
        elif print_type == PrintType.total:
            self.totalLabel.config(text=txt)
        elif print_type == PrintType.bgm:
            self.totalBgmLabel.config(text=txt)
        elif print_type == PrintType.success:
            self.successLabel.config(text=txt)
        elif print_type == PrintType.failed:
            self.failLabel.config(text=txt)

    def start_download(self):
        # 判断是否有网络，去掉
        # if Editors.get_beijing_time() == 0:
        #     self.output("获取数据异常，请检查您的网络！")
        #     return
        if Editors.is_expired():
            self.output("授权证书已到期，请联系客服！")
            return
        ffmpeg = self.ffmFileEntry.get()
        video = self.videoDirEntry.get()
        music = self.musicDirEntry.get()
        dst = self.dstEntry.get()
        editors: Editors = ListCut()
        editor = threading.Thread(target=editors.start, args=(ffmpeg, video, music, dst))
        editor.setDaemon(True)  # 设置守护进程，避免界面卡死
        editor.start()
