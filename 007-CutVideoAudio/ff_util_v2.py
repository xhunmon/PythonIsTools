#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Description:ff_util.py ffmpeg截切命令工具
@Date       :2022/03/14
@Author     :xhunmon
@Mail       :xhunmon@gmail.com
"""
import os
import re
import time
from datetime import datetime, timedelta


def get_va_infos(ff_file, src):
    """
    获取视频的基本信息
    @param ff_file: ffmpeg路径
    @param src: 视频路径
    @return: 结果：{'duration': '00:11:26.91', 'bitrate': '507', 'v_codec': 'h264', 'v_size': '1280x720', 'v_bitrate': '373', 'v_fps': '25', 'a_codec': 'aac', 'a_bitrate': '128'}
    """
    cmd = r'{} -i "{}" -hide_banner 2>&1'.format(ff_file, src)
    output = os.popen(cmd).read()
    lines = output.splitlines()
    result = {}
    for line in lines:
        if line.strip().startswith('Duration:'):
            result['duration'] = line.split(',')[0].split(': ')[-1]
            result['bitrate'] = line.split(',')[-1].strip().split(': ')[-1].split(' ')[0]
        elif line.strip().startswith('Stream #0'):
            line = re.sub(r'\[.*?\]', '', re.sub(r'\(.*?\)', '', line))
            if 'Video' in line:
                result['v_codec'] = line.split(',')[0].split(': ')[-1].strip()
                result['v_size'] = line.split(',')[2].strip().split(' ')[0].strip()
                result['v_bitrate'] = line.split(',')[3].strip().split(' ')[0].strip()
                result['v_fps'] = line.split(',')[4].strip().split(' ')[0].strip()
            elif 'Audio' in line:
                result['a_codec'] = line.split(',')[0].split(': ')[-1].strip()
                result['a_bitrate'] = line.split(',')[4].strip().split(' ')[0].strip()
    print(result)
    return result


def get_duration(ff_file, src):
    '''
    执行命令获取输出这样的：Duration: 00:00:31.63, start: 0.000000, bitrate: 1376 kb/s
    :param ff_file: ffmpeg程序路径
    :param src: 音视频文件
    :return: 返回毫秒
    '''
    cmd = r'{} -i "{}" 2>&1 | grep "Duration"'.format(ff_file, src)
    info = os.popen(cmd).read()
    dur = info.split(',')[0].replace(' ', '').split(':')
    h, m, ss = int(dur[1]) * 60 * 60 * 1000, int(dur[2]) * 60 * 1000, dur[3]
    if '.' in ss:
        s1 = ss.split('.')
        s = int(s1[0]) * 1000 + int(s1[1]) * 10
    else:
        s = int(ss) * 1000
    return h + m + s


def format_h_m_s(t):
    return f'0{t}' if t < 10 else f'{t}'


def format_ms(t):
    if t < 10:
        return f'00{t}'
    return f'0{t}' if t < 100 else f'{t % 1000}'


def format_to_time(ms):
    '''
     毫秒 --> 'xx:xx:xx.xxx'
    :param ms: 毫秒
    :return: 'xx:xx:xx.xxx'
    '''
    # t = timedelta(milliseconds=ms)
    # return str(t)
    h = format_h_m_s(int(ms / 1000 / 60 / 60))
    m = format_h_m_s(int(ms / 1000 / 60 % 60))
    s = format_h_m_s(int(ms / 1000 % 60))
    m_s = format_ms(int(ms % 1000))
    return '{}:{}:{}.{}'.format(h, m, s, m_s)


def format_to_ms(duration: str):
    """
    'xx:xx:xx.xxx' --> 毫秒
    @param duration: 时间长度'xx:xx:xx.xxx'
    @return:  毫秒
    """
    hms = duration.split(':')
    s_str = hms[2]
    ms_str = '0'
    if '.' in s_str:
        s_ms = s_str.split('.')
        s_str = s_ms[0]
        ms_str = s_ms[1]
    h = int(hms[0]) * 1000 * 60 * 60
    m = int(hms[1]) * 1000 * 60
    s = int(s_str) * 1000
    ms = int(ms_str)
    return h + m + s + ms


def srt_to_ass(ff_file, src, dst):
    os.system(f'{ff_file} -i {src} {dst}')


def cut_with_subtitle(ff_file, src, dst, srt, width, height, margin_v, font_size=50, dur_full: str = None,
                      start='00:00:00.000', tail='00:00:00.000', fps=None,
                      v_bit=None, a_bit=None):
    """
    添加硬字幕：ffmpeg -i "../output/733316.mp4" -ss "00:02:00" -t 10 -r 23 -b:v 400K -c:v libx264 -b:a 38K -c:a aac -vf "subtitles=../output/input.ass:force_style='PlayResX=1280,PlayResY=720,MarginV=80,Fontsize=50'" ../output/ass.mp4
    """
    t_start = time.time()
    dur_ms = format_to_ms(dur_full) - format_to_ms(tail) - format_to_ms(start)
    dur = format_to_time(dur_ms)

    filename, ext = os.path.splitext(srt)
    ass = f'{filename}.ass'
    if os.path.exists(ass):
        os.remove(ass)
    ass_cmd = '{} -i "{}" "{}"'.format(ff_file, srt, ass)
    print(ass_cmd)
    os.system(ass_cmd)
    # ffmpeg -i "input.mp4" -ss "00:02:10.000" -t 12397 -r 15 -b:v 500K -c:v libx264 -c:a aac
    cmd = '{} -i "{}"'.format(ff_file, src)
    cmd = '{} -ss "{}" -t {}'.format(cmd, start, int(format_to_ms(dur) / 1000))
    if fps:  # 添加裁剪的fps
        cmd = '{} -r {}'.format(cmd, fps)
    # -c copy 不经过解码，会出现黑屏，因为有可能是P帧和B帧
    if v_bit:  # 添加视频bitrate，并且指定用libx264进行编码（ffmpeg必须安装）
        cmd = '{} -b:v {}K -c:v libx264'.format(cmd, v_bit)
    if a_bit:  # 添加音频bitrate，并且指定用aac进行编码
        cmd = '{} -b:a {}K -c:a aac'.format(cmd, a_bit)
    # -vf "subtitles=input.ass:force_style='PlayResX=1280,PlayResY=720,MarginV=70,Fontsize=50'"
    style = "PlayResX={},PlayResY={},MarginV={},Fontsize={}".format(width, height, margin_v, font_size)
    sub_file = "{}".format(ass)
    cmd = '''{} -vf "subtitles={}:force_style='{}'"'''.format(cmd, sub_file, style)
    # cmd = f'{cmd} -vf "subtitles={ass}:force_style="""PlayResX={width},PlayResY={height},MarginV={margin_v},Fontsize={font_size}""""'
    cmd = '{} {}'.format(cmd, dst)
    print(cmd)
    if os.path.exists(dst):
        os.remove(dst)
    os.system(cmd)
    os.remove(ass)
    print('一共花了 {} 秒 进行裁剪并添加字幕 {}'.format(int(time.time() - t_start), src))


def cut_va_full(ff_file, src, dst, dur: str = None, start='00:00:00.000', fps=None, v_bit=None, a_bit=None,
                copy_a=False):
    """
    ffmpeg -i "input.mp4" -ss "00:02:10.000" -t 12397 -r 15 -b:v 500K -c:v libx264 -c:a aac "凡人修仙传1重制版-国创-高清独家在线观看-bilibili-哔哩哔哩.mp4"
    其他所有的视频裁剪命令都需要通过这个实现
    @param ff_file: ffmpeg路径
    @param src:     输入路径
    @param dst:     输出路径
    @param dur:     裁剪长度，格式为'00:00:00.000'
    @param start:   裁剪的起点，如果dur=None，表示需要对时间进行裁剪，只是转换格式罢了
    @param fps:     帧率，通常视频15~18帧即可，动漫一般24帧
    @param v_bit:   单独控制视频的比特率
    @param a_bit:   单独控制音频的比特率
    @param copy_a:  直接复制音频通道数据，当 a_bit=None方有效
    """
    cmd = '{} -i "{}"'.format(ff_file, src)  # 输入文件
    if dur is not None:  # 添加裁剪时间
        cmd = '{} -ss "{}" -t {}'.format(cmd, start, int(format_to_ms(dur) / 1000))
    if fps:  # 添加裁剪的fps
        cmd = '{} -r {}'.format(cmd, fps)
    # -c copy 不经过解码，会出现黑屏，因为有可能是P帧和B帧
    if v_bit:  # 添加视频bitrate，并且指定用libx264进行编码（ffmpeg必须安装）
        cmd = '{} -b:v {}K -c:v libx264'.format(cmd, v_bit)
    if a_bit:  # 添加音频bitrate，并且指定用aac进行编码
        cmd = '{} -b:a {}K -c:a aac'.format(cmd, a_bit)
    elif copy_a:  # 是否完全复制音频
        cmd = '{} -c:a copy'.format(cmd)
    cmd = '{} "{}"'.format(cmd, dst)  # 添加输出
    if os.path.exists(dst):
        os.remove(dst)
    t_start = time.time()
    os.system(cmd)
    print('一共花了 {} 秒 进行裁剪 {}'.format(int(time.time() - t_start), src))


def cut_va_tail(ff_file, src, dst, dur_full: str = None, start='00:00:00.000', tail='00:00:00.000', fps=None,
                v_bit=None, a_bit=None, copy_a=False):
    """
    裁剪头尾
    """
    dur_ms = format_to_ms(dur_full) - format_to_ms(tail) - format_to_ms(start)
    dur = format_to_time(dur_ms)
    cut_va_full(ff_file, src, dst, dur, start, fps, v_bit, a_bit, copy_a)


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
        r'{} -i "{}" -vn -acodec copy -ss {} -t {} "{}"'.format(ff_file, src, format_to_time(start), dur, dst))


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
        r'{} -i "{}" -ss {} -t {} -r {} -b:v {}K -an "{}"'.format(ff_file, src, format_to_time(start), dur, fps,
                                                                  bit, dst))


def cut_va_dur(ff_file, src, dst, start=0, dur=0, fps=None, bit=None):
    """
    根据头尾裁剪视频
    :param ff_file: ffmpeg工具
    :param src: 输入资源
    :param dst: 输出文件
    :param start:   起点
    :param end: 终点
    :param fps: 帧率
    :param bit: 比特率
    :return:
    """
    length = get_duration(ff_file, src)
    if start + dur > length:
        print('裁剪比视频长')
        return
    if os.path.exists(dst):
        os.remove(dst)

    cmd = r'{} -i "{}"'.format(ff_file, src)
    cmd = cmd + ' -ss {}'.format(format_to_time(start))
    cmd = cmd + ' -t {}'.format(format_to_time(dur))
    if fps:
        cmd = cmd + ' -r {}'.format(fps)
    if bit:
        cmd = cmd + ' -b:v {}K'.format(bit)
    cmd = cmd + ' -c:v libx264 "{}"'.format(dst)  # 使用x264解码后重新封装
    # cmd = cmd+' -c copy {}'.format(dst)  #不经过解码，会出现黑屏
    os.system(cmd)


def cut_va_start_end(ff_file, src, dst, start='00:00:00', end='00:00:00', dur='00:00:00', fps=None, bit=None):
    dur = format_to_ms(dur) - format_to_ms(end)
    cmd = f'{ff_file} -i "{src}" -ss {start} -t {dur} -c copy "{dst}"'
    if os.path.exists(dst):
        os.remove(dst)
    os.system(cmd)


def cut_va_end(ff_file, src, dst, start=0, end=0, fps=None, bit=None):
    """
    根据头尾裁剪视频
    :param ff_file: ffmpeg工具
    :param src: 输入资源
    :param dst: 输出文件
    :param start:   起点
    :param end: 终点
    :param fps: 帧率
    :param bit: 比特率
    :return:
    """
    length = get_duration(ff_file, src)
    dur = length - (start + end)
    if dur <= 0:
        print('裁剪比视频长')
        return
    cut_va_dur(ff_file, src, dst, start, dur, fps, bit)


def muxer_va(ff_file, src_v, src_a, dst):
    if os.path.exists(dst):
        os.remove(dst)
    os.system(r'{} -i "{}" -i "{}" -c:v copy -c:a aac -strict experimental "{}"'.format(ff_file, src_v, src_a, dst))
