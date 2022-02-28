#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Description: 文件相关处理
@Date       :2022/01/22
@Author     :xhunmon
@Mail       :xhunmon@gmail.com
"""

import datetime
import json
import os
import re
import shutil

import cairosvg
import pandas as pd
import pypandoc  # 要安装pandoc
from docx import Document


def file_name(file_dir):
    results = []
    for root, dirs, files in os.walk(file_dir):
        # print(root)  # 当前目录路径
        # print(dirs)  # 当前路径下所有子目录
        # print(files)  # 当前路径下所有非目录子文件
        results += files
    return results


def deal_one_page():
    fs = file_name('100条')
    for f in fs:
        try:
            print('正在检测【%s】' % f)
            shotname, extension = os.path.splitext('%s' % f)
            print('正在检测【%s】' % shotname)
            if '1篇' in shotname:
                new_name = re.sub(r'1篇', '', f)
                document = Document(r"html/%s" % f)
                paragraphs = document.paragraphs
                p = paragraphs[0]
                p._element.getparent().remove(p._element)
                document.save(r"html/%s" % new_name)
                os.remove('html/%s' % f)
        except Exception as e:
            print(e)


def copy_doc():
    fs = file_name('all')
    i = 1
    k = 1
    temp_dir = '01'
    os.makedirs('100条/%s' % temp_dir)
    for f in fs:
        try:
            # print('正在检测【%s】' % f)
            shotname, extension = os.path.splitext('%s' % f)
            shutil.copyfile(r'all/%s' % f, r'100条/%s/%s' % (temp_dir, f))
            if i % 100 == 0:
                temp_dir = '0%d' % k if k < 10 else '%d' % k
                k += 1
                os.makedirs('100条/%s' % temp_dir)
            i += 1
        except Exception as e:
            print(e)


'''########文件处理相关#########'''


def html_cover_doc(in_path, out_path):
    '''将html转化成功doc'''
    path, file_name = os.path.split(out_path)
    if path and not os.path.exists(path):
        os.makedirs(path)
    pypandoc.convert_file(in_path, 'docx', outputfile=out_path)


def svg_cover_jpg(src, dst):
    ''''
    drawing = svg2rlg("drawing.svg")
    renderPDF.drawToFile(drawing, "drawing.pdf")
    renderPM.drawToFile(drawing, "fdrawing.png", fmt="PNG")
    renderPM.drawToFile(drawing, "drawing.jpg", fmt="JPG")
    '''
    path, file_name = os.path.split(dst)
    if path and not os.path.exists(path):
        os.makedirs(path)
    # drawing = svg2rlg(src)
    # renderPM.drawToFile(drawing, dst, fmt="JPG")
    cairosvg.svg2png(url=src, write_to=dst)


def html_cover_excel(content, out_path):
    '''将html转化成excel'''
    path, file_name = os.path.split(out_path)
    if path and not os.path.exists(path):
        os.makedirs(path)
    tables = pd.read_html(content, encoding='utf-8')
    writer = pd.ExcelWriter(out_path)
    for i in range(len(tables)):
        tables[i].to_excel(writer, sheet_name='表%d' % (i + 1))  # startrow
    writer.save()  # 写入硬盘


def write_to_html(content, file_path):
    '''将内容写入本地，自动加上head等信息'''
    page = '''<!DOCTYPE html>
                <html>
                <head>
                    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
                </head>
                <body>'''
    page += content
    page += '''</body>
    </html>'''
    write(page, file_path)


def write_json(content, file_path):
    '''写入json'''
    path, file_name = os.path.split(file_path)
    if path and not os.path.exists(path):
        os.makedirs(path)
    with open(file_path, 'w') as f:
        json.dump(content, f, ensure_ascii=False)
        f.close()


def read_json(file_path):
    '''读取json'''
    with open(file_path, 'r') as f:
        js_get = json.load(f)
        f.close()
    return js_get


def write(content, file_path):
    '''写入txt文本内容'''
    path, file_name = os.path.split(file_path)
    if path and not os.path.exists(path):
        os.makedirs(path)
    with open(file_path, 'w') as f:
        f.write(content)
        f.close()


def read(file_path) -> str:
    '''读取txt文本内容'''
    content = None
    try:
        with open(file_path, 'r') as f:
            content = f.read()
            f.close()
    except Exception as e:
        print(e)
    return content


def get_next_folder(dst, day_diff, folder, max_size):
    '''遍历目录文件，直到文件夹不存在或者数目达到最大（max_size）时，返回路径'''
    while True:
        day_time = (datetime.date.today() + datetime.timedelta(days=day_diff)).strftime('%Y-%m-%d')  # 下一天的目录继续遍历
        folder_path = os.path.join(dst, day_time, folder)
        if os.path.exists(folder_path):  # 已存在目录
            size = len(next(os.walk(folder_path))[2])
            if size >= max_size:  # 该下一个目录了
                day_diff += 1
                continue
        else:
            os.makedirs(folder_path)
        return day_diff, folder_path


if __name__ == '__main__':
    pass
