#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Description: 快手视频下载
@Date       :2021/09/102
@Author     :qincji
@Mail       :xhunmon@gmail.com
"""

import json
import os
import re
import time
import urllib

import requests

from downloader import Downloader

requestUrl = 'https://video.kuaishou.com/graphql'


class KuaiShou(Downloader):
    cookie = 'clientid=3; client_key=65890b29; kpf=PC_WEB; kpn=KUAISHOU_VISION; did=web_3e09c32da1db9d38c0122ffa25ad8b7d'

    # 初始化
    def __init__(self):
        super().__init__()
        self.headers = self._headers
        # 抓获所有视频
        self.end = False

    def set_cookie(self, c):
        """当cookie过期时，需要从外界出入"""
        KuaiShou.cookie = c

    def start(self, url, path):
        Downloader.print_ui("开始解析下载链接")
        # 读取保存路径
        self.save = path
        if '/profile/' in url:
            self.parse_user(url)
        elif '/short-video/' in url:
            if 'trendingId' in url:
                self.parse_single_trendingId(urllib.parse.unquote(url, encoding="utf-8"))
            elif 'streamSource' in url:
                self.parse_single_streamSource(urllib.parse.unquote(url, encoding="utf-8"))
            else:
                Downloader.print_ui('该链接不支持下载')
        else:
            Downloader.print_ui('该链接不支持下载')

    # 单条数据页面
    def parse_single_trendingId(self, url):
        try:
            Downloader.print_ui('----为您下载单个视频----\r')
            # userId = re.findall(r'/short-video/(.+?)\?', url)[0].strip()
            trendingId = re.findall(r'trendingId=(.+?)&', url)[0].strip()
            area = re.findall(r'area=(.+?)$', url)[0].strip()
        except:
            Downloader.print_ui('地址%s输入错误' % url)
            return
        links = []
        try:
            result = self.post_single_trendingId(url, KuaiShou.cookie, trendingId, area)
            data = json.loads(result)
            feeds = data['data']['hotData']['feeds']
            size = len(feeds)
            links.append(feeds)
        except Exception as e:
            Downloader.print_ui(str(e))
            return
        if size < 1:
            Downloader.print_ui('解析地址%s异常' % url)
            return
        Downloader.add_total_count(size)
        for link in links:
            self.download(link)

    # 单条数据页面
    def parse_single_streamSource(self, url):
        try:
            Downloader.print_ui('----为您下载单个视频----\r')
            userId = re.findall(r'/short-video/(.+?)\?', url)[0].strip()
            area = re.findall(r'area=(.+?)$', url)[0].strip()
        except:
            Downloader.print_ui('地址%s输入错误' % url)
            return
        links = []
        try:
            result = self.post_single_streamSource(url, KuaiShou.cookie, userId, area)
            data = json.loads(result)
            feeds = [data['data']['visionVideoDetail'], ]
            size = len(feeds)
            links.append(feeds)
        except Exception as e:
            Downloader.print_ui(str(e))
            return
        if size < 1:
            Downloader.print_ui('解析地址%s异常' % url)
            return
        Downloader.add_total_count(size)
        for link in links:
            self.download(link)

    # 判断个人主页api链接
    def parse_user(self, url):
        # https://www.kuaishou.com/profile/3xcx5qwycxzxdre
        try:
            Downloader.print_ui('----为您下载多个视频----\r')
            userId = re.findall(r'/profile/(.+?)$', url)[0].strip()
        except:
            Downloader.print_ui('地址%s输入错误' % url)
            return
        pcursor = ''
        all_count = 0
        links = []
        while True:
            try:
                result = self.post_user(userId, KuaiShou.cookie, pcursor)
                data = json.loads(result)
                feeds = data['data']['visionProfilePhotoList']['feeds']
                flen = len(feeds)
                pcursor = data['data']['visionProfilePhotoList']['pcursor']
                if flen == 0:
                    break
                all_count += flen
                links.append(feeds)
            except Exception as e:
                Downloader.print_ui(str(e))
                break
        if len(links) < 1:
            Downloader.print_ui('解析地址%s异常' % url)
            return
        Downloader.add_total_count(all_count)
        for link in links:
            self.download(link)

    def post_single_trendingId(self, url, Cookie, trendingId, area):
        data = {
            "operationName": "hotVideoQuery",
            "variables": {
                "trendingId": trendingId,
                "page": "detail",
                "webPageArea": area
            },
            "query": "query hotVideoQuery($trendingId: String, $page: String, $webPageArea: String) {\n  hotData(trendingId: $trendingId, page: $page, webPageArea: $webPageArea) {\n    result\n    llsid\n    expTag\n    serverExpTag\n    pcursor\n    webPageArea\n    feeds {\n      type\n      trendingId\n      author {\n        id\n        name\n        headerUrl\n        following\n        headerUrls {\n          url\n          __typename\n        }\n        __typename\n      }\n      photo {\n        id\n        duration\n        caption\n        likeCount\n        realLikeCount\n        coverUrl\n        photoUrl\n        coverUrls {\n          url\n          __typename\n        }\n        timestamp\n        expTag\n        animatedCoverUrl\n        stereoType\n        videoRatio\n        __typename\n      }\n      canAddComment\n      llsid\n      status\n      currentPcursor\n      __typename\n    }\n    __typename\n  }\n}\n"
        }
        headers = {
            'Host': 'www.kuaishou.com',
            'Connection': 'keep-alive',
            'Content-Length': '1261',
            'accept': '*/*',
            'User-Agent': 'Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/89.0.4389.114Safari/537.36Edg/89.0.774.68',
            'content-type': 'application/json',
            'Origin': 'https://www.kuaishou.com',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': url.encode(encoding='utf-8'),
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'Cookie': Cookie,
        }
        requests.packages.urllib3.disable_warnings()
        r = requests.post('https://www.kuaishou.com/graphql', data=json.dumps(data), headers=headers)
        r.encoding = r.apparent_encoding
        html = r.text
        return html

    def post_single_streamSource(self, url, Cookie, photoId, area):
        data = {
            "operationName": "visionVideoDetail",
            "variables": {
                "photoId": photoId,
                "page": "detail",
                "webPageArea": area
            },
            "query": "query visionVideoDetail($photoId: String, $type: String, $page: String, $webPageArea: String) {\n  visionVideoDetail(photoId: $photoId, type: $type, page: $page, webPageArea: $webPageArea) {\n    status\n    type\n    author {\n      id\n      name\n      following\n      headerUrl\n      __typename\n    }\n    photo {\n      id\n      duration\n      caption\n      likeCount\n      realLikeCount\n      coverUrl\n      photoUrl\n      liked\n      timestamp\n      expTag\n      llsid\n      viewCount\n      videoRatio\n      stereoType\n      croppedPhotoUrl\n      manifest {\n        mediaType\n        businessType\n        version\n        adaptationSet {\n          id\n          duration\n          representation {\n            id\n            defaultSelect\n            backupUrl\n            codecs\n            url\n            height\n            width\n            avgBitrate\n            maxBitrate\n            m3u8Slice\n            qualityType\n            qualityLabel\n            frameRate\n            featureP2sp\n            hidden\n            disableAdaptive\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    tags {\n      type\n      name\n      __typename\n    }\n    commentLimit {\n      canAddComment\n      __typename\n    }\n    llsid\n    danmakuSwitch\n    __typename\n  }\n}\n"
        }
        headers = {
            'Host': 'www.kuaishou.com',
            'Connection': 'keep-alive',
            'Content-Length': '1261',
            'accept': '*/*',
            'User-Agent': 'Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/89.0.4389.114Safari/537.36Edg/89.0.774.68',
            'content-type': 'application/json',
            'Origin': 'https://www.kuaishou.com',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': url.encode(encoding='utf-8'),
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'Cookie': Cookie,
        }
        requests.packages.urllib3.disable_warnings()
        r = requests.post('https://www.kuaishou.com/graphql', data=json.dumps(data), headers=headers)
        r.encoding = r.apparent_encoding
        html = r.text
        return html

    def post_user(self, userId, Cookie, pcursor):
        data = {"operationName": "visionProfilePhotoList",
                "variables": {"userId": userId, "pcursor": pcursor, "page": "profile"},
                "query": "query visionProfilePhotoList($pcursor: String, $userId: String, $page: String, $webPageArea: String) {\n  visionProfilePhotoList(pcursor: $pcursor, userId: $userId, page: $page, webPageArea: $webPageArea) {\n    result\n    llsid\n    webPageArea\n    feeds {\n      type\n      author {\n        id\n        name\n        following\n        headerUrl\n        headerUrls {\n          cdn\n          url\n          __typename\n        }\n        __typename\n      }\n      tags {\n        type\n        name\n        __typename\n      }\n      photo {\n        id\n        duration\n        caption\n        likeCount\n        realLikeCount\n        coverUrl\n        coverUrls {\n          cdn\n          url\n          __typename\n        }\n        photoUrls {\n          cdn\n          url\n          __typename\n        }\n        photoUrl\n        liked\n        timestamp\n        expTag\n        animatedCoverUrl\n        stereoType\n        videoRatio\n        __typename\n      }\n      canAddComment\n      currentPcursor\n      llsid\n      status\n      __typename\n    }\n    hostName\n    pcursor\n    __typename\n  }\n}\n"}
        failed = {'msg': 'failed...'}
        headers = {
            'Host': 'video.kuaishou.com',
            'Connection': 'keep-alive',
            'Content-Length': '1261',
            'accept': '*/*',
            'User-Agent': 'Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/89.0.4389.114Safari/537.36Edg/89.0.774.68',
            'content-type': 'application/json',
            'Origin': 'https://video.kuaishou.com',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://video.kuaishou.com/profile/' + userId,
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'Cookie': Cookie,

        }
        requests.packages.urllib3.disable_warnings()
        r = requests.post(requestUrl, data=json.dumps(data), headers=headers)
        r.encoding = 'UTF-8'
        html = r.text
        return html

    def progressbar(self, url, filepath, filename):
        if not os.path.exists(filepath):
            os.mkdir(filepath)
        start = time.time()
        response = requests.get(url, stream=True)
        size = 0
        chunk_size = 1024
        content_size = int(response.headers['content-length'])
        if response.status_code == 200:
            # print('Start download,[File size]:{size:.2f} MB'.format(size=content_size / chunk_size / 1024))
            Downloader.print_ui(('%s Start download,[File size]:{size:.2f} MB' % filename).format(
                size=content_size / chunk_size / 1024))
            filename = filename.replace("\n", "")
            # filepath = filepath + filename
            filepath = os.path.join(filepath, filename)
            try:
                with open(filepath, 'wb') as file:
                    for data in response.iter_content(chunk_size=chunk_size):
                        file.write(data)
                        size += len(data)
                        Downloader.print_ui('\r' + '%s[下载进度]:%s%.2f%%' % (filename,
                                                                          '>' * int(size * 50 / content_size),
                                                                          float(size / content_size * 100)))
                        # print('\r' + '[下载进度]:%s%.2f%%' % (
                        #     '>' * int(size * 50 / content_size), float(size / content_size * 100)), end=' ')
                end = time.time()
                # print('Download completed!,times: %.2f秒' % (end - start))
                Downloader.print_ui('%s Download completed!,times: %.2f秒' % (filename, end - start))
            except:
                Downloader.add_failed_count()
                Downloader.print_ui('%s [下载失败！！]' % filename)

    def download(self, feeds):
        author = ''
        for feed in feeds:
            try:
                Downloader.add_downloading_count()
                author = feed['author']['name']
                filename = feed['photo']['caption'] + '.mp4'
                # filepath = self.save + '/' + author + '/'
                filepath = os.path.join(self.save, author)
                filename_path = os.path.join(filepath, filename)
                if not os.path.exists(filename_path):
                    self.progressbar(feed['photo']['photoUrl'], filepath, filename)
                    # print(filename + ",下载完成")
                    Downloader.print_ui('%s--下载完成' % filename)
                    Downloader.add_success_count()
                else:
                    # print(filename + ",已存在，跳过")
                    Downloader.print_ui('%s--已存在，跳过' % filename)
                    Downloader.add_success_count()
            except:
                Downloader.add_failed_count()
                Downloader.print_ui('%s下载失败' % author)
