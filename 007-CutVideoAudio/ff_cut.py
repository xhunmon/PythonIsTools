#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Description:editing.py 所有视频类的基类，负责与UI界面的绑定
@Date       :2022/03/14
@Author     :xhunmon
@Mail       :xhunmon@gmail.com
"""
import os.path
import random
import shutil
import time

from editors import Editors
from ff_util import *
from utils import *


class ListCut(Editors):
    # 初始化
    def __init__(self):
        super().__init__()
        self.headers = self._headers
        # 抓获所有视频
        self.end = False

    def start(self, ffmpeg, video, music, dst):
        Editors.print_ui("开始准备处理本地数据")
        if not os.path.exists(ffmpeg) or not os.path.exists(video) or not os.path.exists(music) or not os.path.exists(
                dst):
            Editors.print_ui("文件或者目录不存在！")
            return
        dst_temp = os.path.join(dst, 'temp')
        if not os.path.exists(dst_temp):
            os.makedirs(dst_temp)
        fps, bit = random.randint(25, 30), random.randint(1200, 1800)
        start_v, end_v = random.randint(100, 500), random.randint(100, 500)
        v_files, a_files = get_real_files(video), get_real_files(music)
        index, size_v, size_a, start_time = 1, len(v_files), len(a_files), time.time()
        Editors.add_total_count(size_v)
        Editors.add_bgm_count(size_a)
        Editors.print_ui("改系列帧率：{} | 比特率：{} | 截切开头：{} | 截切结尾：{}".format(fps, bit, start_v, end_v))
        time.sleep(3)
        for i in range(0, size_v):
            a_file = random.choice(a_files)
            v_file = random.choice(v_files)
            v_files.remove(v_file)
            Editors.print_ui("{} 与 {} 开始合并！".format(v_file, a_file))
            try:
                name_v, ext_v = os.path.splitext(v_file)
                name_a, ext_a = os.path.splitext(a_file)
                src_v = os.path.join(video, v_file)
                dst_file = os.path.join(dst, '{}-{}{}'.format(format_num(index), name_v, ext_v))
                dur_src_v = get_duration(ffmpeg, src_v)  # 毫秒
                duration = dur_src_v - start_v - end_v
                src_a = os.path.join(music, a_file)
                dur_src_a = get_duration(ffmpeg, src_a)
                random_a = (dur_src_a - duration) if dur_src_a > duration else 100
                start_a = random.randint(0, random_a)  # 随机取音频
                temp_file_v = os.path.join(dst_temp, 'temp{}'.format(ext_v))
                temp_file_a = os.path.join(dst_temp, 'temp{}'.format(ext_a))
                cut_video(ffmpeg, src_v, start_v, duration, fps, bit, temp_file_v)
                cut_audio(ffmpeg, src_a, start_a, duration, temp_file_a)
                muxer_va(ffmpeg, temp_file_v, temp_file_a, dst_file)
                index += 1
                Editors.add_success_count()
            except Exception as e:
                Editors.print_ui(str(e))
                Editors.add_failed_count()
                time.sleep(1)
            use_time = time.time() - start_time
            Editors.print_ui('已运行{}分{}秒...'.format(int(use_time / 60), int(use_time % 60)))
            time.sleep(2)
        shutil.rmtree(dst_temp)
