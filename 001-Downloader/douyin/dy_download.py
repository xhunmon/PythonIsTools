#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Description: 抖音视频下载
@Date       :2021/08/14
@Author     :xhunmon
@Mail       :xhunmon@gmail.com
"""

import json
import os
import re
import time
from urllib import parse

import requests
import requests_html

from downloader import Downloader


class DouYin(Downloader):
    # 初始化
    def __init__(self):
        super().__init__()
        self.headers = self._headers
        # 抓获所有视频
        self.end = False

    def start(self, url, path):
        Downloader.print_ui("开始解析下载链接")
        # 读取保存路径
        self.save = path
        # 读取下载视频个数
        self.count = 35
        # 读取下载是否下载音频
        self.musicarg = True
        # 读取用户主页地址
        self.user = ''
        # 读取单条
        self.single = ''

        # 读取下载模式 #下载模式选择 like为点赞 post为发布
        self.mode = 'post'

        # 保存用户名
        self.nickname = ''

        if '/user/' in url:
            self.user = url
        else:
            self.single = url

        if len(self.single) > 0:
            self.count = 1
            self.parse_single()
        else:
            self.judge_link()

    # 单条数据页面
    def parse_single(self):
        session = requests_html.HTMLSession()
        html = session.get(self.single)

        result = re.findall(r'id="RENDER_DATA".+?json">(.+?)</script>', html.text)[0]
        urls = parse.unquote_plus(result)
        jsonObj = json.loads(urls)

        # 作者信息
        author_list = []
        # 无水印视频链接
        video_list = []
        # 作品id
        aweme_id = []
        # 作者id
        nickname = []
        max_cursor = 0

        if ('C_12' in jsonObj):
            detail = jsonObj['C_12']['aweme']['detail']
        elif ('C_14' in jsonObj):
            detail = jsonObj['C_14']['aweme']['detail']
        else:
            detail = jsonObj['C_0']['aweme']['detail']
        author_list.append(str(detail['desc']))
        video_list.append(str("https:" + detail['video']['playAddr'][0]['src']))
        aweme_id.append(str(detail['awemeId']))
        nickname.append(str(detail['authorInfo']['nickname']))
        Downloader.print_ui('开始下载单个视频' + video_list[0])
        self.videos_download(1, author_list, video_list, aweme_id, nickname, max_cursor)

    # 匹配粘贴的url地址
    def Find(self, string):
        # findall() 查找匹配正则表达式的字符串
        url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', string)
        Downloader.print_ui('Find url: ' + url)
        return url

    # 判断个人主页api链接
    def judge_link(self):
        user_url = self.user

        Downloader.print_ui('----为您下载多个视频----\r')
        key = re.findall('/user/(.*?)\?', str(user_url))[0]
        if not key:
            key = user_url[28:83]
        Downloader.print_ui('----' + '用户的sec_id=' + key + '----\r')

        # 第一次访问页码
        max_cursor = 0

        # 构造第一次访问链接
        api_post_url = 'https://www.iesdouyin.com/web/api/v2/aweme/%s/?sec_uid=%s&count=%s&max_cursor=%s&aid=1128&_signature=PDHVOQAAXMfFyj02QEpGaDwx1S&dytk=' % (
            self.mode, key, str(self.count), max_cursor)
        self.get_data(api_post_url, max_cursor)
        return api_post_url, max_cursor, key

    # 获取第一次api数据
    def get_data(self, api_post_url, max_cursor):
        # 尝试次数
        index = 0
        # 存储api数据
        result = []
        while result == []:
            index += 1
            Downloader.print_ui('----正在进行第 %d 次尝试----\r' % index)
            time.sleep(0.3)
            response = requests.get(url=api_post_url, headers=self.headers)
            html = json.loads(response.content.decode())
            if self.end == False:
                # 下一页值
                self.nickname = html['aweme_list'][0]['author']['nickname']
                Downloader.print_ui('[  用户  ]:' + str(self.nickname) + '\r')
                max_cursor = html['max_cursor']
                result = html['aweme_list']
                Downloader.print_ui('----抓获数据成功----\r')

                # 处理第一页视频信息
                self.video_info(result, max_cursor)
            else:
                max_cursor = html['max_cursor']
                self.next_data(max_cursor)
                # self.end = True
                Downloader.print_ui('----此页无数据，为您跳过----\r')

        return result, max_cursor

    # 下一页
    def next_data(self, max_cursor):
        if self.count == 1:
            return
        user_url = self.user
        # 获取用户sec_uid
        key = re.findall('/user/(.*?)\?', str(user_url))[0]
        if not key:
            key = user_url[28:83]

        # 构造下一次访问链接
        api_naxt_post_url = 'https://www.iesdouyin.com/web/api/v2/aweme/%s/?sec_uid=%s&count=%s&max_cursor=%s&aid=1128&_signature=RuMN1wAAJu7w0.6HdIeO2EbjDc&dytk=' % (
            self.mode, key, str(self.count), max_cursor)
        index = 0
        result = []
        while self.end == False:
            # 回到首页，则结束
            if max_cursor == 0:
                self.end = True
                return
            index += 1
            Downloader.print_ui('----正在对' + max_cursor + '页进行第 %d 次尝试----\r' % index)
            time.sleep(0.3)
            response = requests.get(url=api_naxt_post_url, headers=self.headers)
            html = json.loads(response.content.decode())
            if self.end == False:
                # 下一页值
                max_cursor = html['max_cursor']
                result = html['aweme_list']
                Downloader.print_ui('----' + max_cursor + '页抓获数据成功----\r')
                # 处理下一页视频信息
                self.video_info(result, max_cursor)
            else:
                self.end == True
                Downloader.print_ui('----' + max_cursor + '页抓获数据失败----\r')
                # sys.exit()

    # 处理视频信息
    def video_info(self, result, max_cursor):
        # 作者信息
        author_list = []

        # 无水印视频链接
        video_list = []

        # 作品id
        aweme_id = []

        # 作者id
        nickname = []

        # 封面大图
        # dynamic_cover = []

        for i2 in range(self.count):
            try:
                author_list.append(str(result[i2]['desc']))
                video_list.append(str(result[i2]['video']['play_addr']['url_list'][0]))
                aweme_id.append(str(result[i2]['aweme_id']))
                nickname.append(str(result[i2]['author']['nickname']))
                # dynamic_cover.append(str(result[i2]['video']['dynamic_cover']['url_list'][0]))
            except Exception as error:
                # Downloader.print_ui2(error)
                pass
        self.videos_download(self.count, author_list, video_list, aweme_id, nickname, max_cursor)
        return self, author_list, video_list, aweme_id, nickname, max_cursor

    def videos_download(self, count, author_list, video_list, aweme_id, nickname, max_cursor):
        Downloader.add_total_count(count)
        for i in range(count):
            if count == 1:
                # 创建并检测下载目录是否存在
                pre_save = os.path.join(self.save, "单条")
            else:
                pre_save = os.path.join(self.save, nickname[i])
            try:
                os.makedirs(pre_save)
            except:
                pass
            Downloader.add_downloading_count()
            try:
                jx_url = f'https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?item_ids={aweme_id[i]}'  # 官方接口
                js = json.loads(requests.get(url=jx_url, headers=self.headers).text)
                music_url = str(js['item_list'][0]['music']['play_url']['url_list'][0])
                music_title = str(js['item_list'][0]['music']['author'])
                if self.musicarg == "yes":  # 保留音频
                    music = requests.get(music_url)  # 保存音频
                    start = time.time()  # 下载开始时间
                    size = 0  # 初始化已下载大小
                    chunk_size = 1024  # 每次下载的数据大小
                    content_size = int(music.headers['content-length'])  # 下载文件总大小
                    if music.status_code == 200:  # 判断是否响应成功
                        Downloader.print_ui('[  音频  ]:' + author_list[i] + '[文件 大小]:{size:.2f} MB'.format(
                            size=content_size / chunk_size / 1024))  # 开始下载，显示下载文件大小
                        # m_url = pre_save + music_title + '-[' + author_list[i] + '].mp3'
                        m_url = os.path.join(pre_save,
                                             nickname[i] + "-" + music_title + '-[' + author_list[i] + '].mp3')
                        Downloader.print_ui("路径：" + m_url)
                        with open(m_url, 'wb') as file:  # 显示进度条
                            for data in music.iter_content(chunk_size=chunk_size):
                                file.write(data)
                                size += len(data)
                                Downloader.print_ui('\r' + music_title + '\n[下载进度]:%s%.2f%%' % (
                                    '>' * int(size * 50 / content_size), float(size / content_size * 100)))
                            end = time.time()  # 下载结束时间
                            Downloader.print_ui('\n' + music_title + '\n[下载完成]:耗时: %.2f秒\n' % (end - start))  # 输出下载用时时间
                            Downloader.add_success_count()
            except Exception as error:
                # Downloader.print_ui2(error)
                Downloader.print_ui('该页音频没有' + str(self.count) + '个,已为您跳过\r')
                Downloader.add_failed_count()
                break

            try:
                video = requests.get(video_list[i])  # 保存视频
                start = time.time()  # 下载开始时间
                size = 0  # 初始化已下载大小
                chunk_size = 100  # 每次下载的数据大小
                content_size = int(video.headers['content-length'])  # 下载文件总大小
                if video.status_code == 200:  # 判断是否响应成功
                    Downloader.print_ui(
                        '[  视频  ]:' + nickname[i] + '-' + author_list[i] + '[文件 大小]:{size:.2f} MB'.format(
                            size=content_size / 1024 / 1024))  # 开始下载，显示下载文件大小
                    v_url = os.path.join(pre_save, nickname[i] + "-" + '[' + author_list[i] + '].mp4')
                    # v_url = pre_save + '[' + author_list[i] + '].mp4'
                    Downloader.print_ui("路径：" + v_url)
                    with open(v_url, 'wb') as file:  # 显示进度条
                        for data in video.iter_content(chunk_size=chunk_size):
                            file.write(data)
                            size += len(data)
                            Downloader.print_ui('\r' + author_list[i] + '\n[下载进度]:%s%.2f%%' % (
                                '>' * int(size * 50 / content_size), float(size / content_size * 100)))
                        end = time.time()  # 下载结束时间
                        Downloader.print_ui('\n' + author_list[i] + '\n[下载完成]:耗时: %.2f秒\n' % (end - start))  # 输出下载用时时间
                        Downloader.add_success_count()
            except Exception as error:
                # Downloader.print_ui2(error)
                Downloader.print_ui('该页视频没有' + str(self.count) + '个,已为您跳过\r')
                Downloader.add_failed_count()
                break
        self.next_data(max_cursor)
