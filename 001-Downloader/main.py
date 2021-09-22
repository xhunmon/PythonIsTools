#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Description: 程序主入口
@Date       :2021/08/14
@Author     :xhunmon
@Mail       :xhunmon@gmail.com
"""
import os
import sys

from ui import Ui

# 主模块执行
if __name__ == "__main__":
    path = os.path.dirname(os.path.realpath(sys.argv[0]))
    app = Ui()
    app.set_dir(path)
    # to do
    app.mainloop()
