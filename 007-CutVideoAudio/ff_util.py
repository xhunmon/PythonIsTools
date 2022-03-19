#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Description:ff_util.py ffmpeg截切命令工具
@Date       :2022/03/14
@Author     :xhunmon
@Mail       :xhunmon@gmail.com
"""
import os


def get_duration(ff_file, src):
    '''
    执行命令获取输出这样的：Duration: 00:00:31.63, start: 0.000000, bitrate: 1376 kb/s
    :param ff_file: ffmpeg程序路径
    :param src: 音视频文件
    :return: 返回毫秒
    '''
    info = os.popen(r'{} -i "{}" 2>&1 | grep "Duration"'.format(ff_file, src)).read()
    dur = info.split(',')[0].replace(' ', '').split(':')
    h, m, ss = int(dur[1]) * 60 * 60 * 1000, int(dur[2]) * 60 * 1000, dur[3]
    if '.' in ss:
        s1 = ss.split('.')
        s = int(s1[0]) * 1000 + int(s1[1]) * 10
    else:
        s = int(ss) * 1000
    return h + m + s


def format_h_m_s(t):
    if t < 10:
        return '0{}'.format(t)
    else:
        return '{}'.format(t)


def format_ms(t):
    if t < 10:
        return '00{}'.format(t)
    elif t < 100:
        return '0{}'.format(t)
    else:
        return '{}'.format(t)


def format_duration_by_ms(ms):
    '''
    通过毫秒转化成 'xx:xx:xx.xxx' 格式
    :param ms: 毫秒
    :return:
    '''
    h = format_h_m_s(int(ms / 1000 / 60 / 60))
    m = format_h_m_s(int(ms / 1000 / 60 % 60))
    s = format_h_m_s(int(ms / 1000 % 60))
    m_s = format_ms(int(ms % 1000))
    return '{}:{}:{}.{}'.format(h, m, s, m_s)


def cut_audio(ff_file, src, start, dur, dst):
    '''
    裁剪一段音频进行输出
    :param ff_file: ffmpeg程序路径
    :param src: 要裁剪的文件路径，可以是视频文件
    :param start: 开始裁剪点，单位毫秒开始
    :param dur: 裁剪时长，单位秒
    :param dst: 输出路径，包括后缀名
    :return:
    '''
    if os.path.exists(dst):
        os.remove(dst)
    os.system(
        r'{} -i "{}" -vn -acodec copy -ss {} -t {} "{}"'.format(ff_file, src, format_duration_by_ms(start), dur, dst))


def cut_video(ff_file, src, start, dur, fps, bit, dst):
    '''
    裁剪一段视频进行输出， -ss xx:xx:xx.xxx
    :param ff_file: ffmpeg程序路径
    :param src: 要裁剪的文件路径，可以是视频文件
    :param start: 开始裁剪点，单位毫秒开始
    :param dur: 裁剪时长，单位秒
    :param fps: 帧率，通常是25~30
    :param bit: 比特率，通常是1600~2000即可
    :param dst: 输出路径，包括后缀名
    :return:
    '''
    if os.path.exists(dst):
        os.remove(dst)
    os.system(
        r'{} -i "{}" -ss {} -t {} -r {} -b:v {}K -an "{}"'.format(ff_file, src, format_duration_by_ms(start), dur, fps,
                                                                  bit, dst))


def muxer_va(ff_file, src_v, src_a, dst):
    if os.path.exists(dst):
        os.remove(dst)
    os.system(r'{} -i "{}" -i "{}" -c:v copy -c:a aac -strict experimental "{}"'.format(ff_file, src_v, src_a, dst))
