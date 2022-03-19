#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Description: 程序主入口
@Date       :2022/03/14
@Author     :xhunmon
@Mail       :xhunmon@gmail.com
"""
import os
import sys

from ui import Ui

# 主模块执行
if __name__ == "__main__":
    path = os.path.dirname(os.path.realpath(sys.argv[0]))
    # ffmpeg = os.path.dirname('/usr/local/ffmpeg/bin/ffmpeg/')
    # video = os.path.dirname('/Users/Qincji/Documents/zmt/handmade/')
    # music = os.path.dirname('/Users/Qincji/Documents/zmt/music/')
    # dst = os.path.dirname('/Users/Qincji/Downloads/ffmpeg/')
    app = Ui()
    # app.set_dir(ffmpeg, video, music, dst)
    app.set_dir(path, path, path, path)
    # to do
    app.mainloop()
