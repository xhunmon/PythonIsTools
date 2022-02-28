#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Description: ffmpeg去掉最后一帧，改变md5
@Date       :2022/02/17
@Author     :xhunmon
@Mail       :xhunmon@gmail.com
"""
import os


def cute_video(folder):
    files = next(os.walk(folder))[2]  # 获取文件
    for file in files:
        file_path = os.path.join(folder, file)
        shotname, extension = os.path.splitext(file)
        if len(shotname) == 0 or len(extension) == 0:
            continue
        out_file = os.path.join(folder, 'out-{}{}'.format(shotname, extension))
        # 获取时间。输入自己系统安装的ffmpeg，注意斜杠
        time = os.popen(
            r"/usr/local/ffmpeg/bin/ffmpeg -i {} 2>&1 | grep 'Duration' | cut -d ' ' -f 4 | sed s/,//".format(
                file_path)).read().replace('\n', '').replace(' ', '')
        if '.' in time:
            match_time = time.split('.')[0]
        else:
            match_time = time
        print(match_time)
        ts = match_time.split(':')
        sec = int(ts[0]) * 60 * 60 + int(ts[1]) * 60 + int(ts[2])
        # 从0分0秒100毫秒开始截切（目的就是去头去尾）
        os.popen(r"/usr/local/ffmpeg/bin/ffmpeg -ss 0:00.100 -i {} -t {} -c:v copy -c:a copy {}".format(file_path, sec,
                                                                                                        out_file))


# 主模块执行
if __name__ == "__main__":
    # path = os.path.dirname('/Users/Qincji/Downloads/ffmpeg/')
    path = os.path.dirname('需要处理的目录')  # 目录下的所有视频
    cute_video(path)
