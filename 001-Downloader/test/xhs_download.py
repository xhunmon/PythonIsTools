import os
import random
import time

import requests
from my_fake_useragent import UserAgent

ua = UserAgent(family='chrome')
pre_save = os.path.join(os.path.curdir, '0216')

'''

'''


def download_url(url, index):
    try:
        headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'identity;q=1, *;q=0',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Cookie': 'xhsTrackerId=6970aca9-a496-4f50-cf98-118929f063bf; timestamp2=2022021544322a4e45f1e1dec93beb82; timestamp2.sig=jk1cFo-zHueSZUpZRvlqyJwTFoA1y8ch9t76Bfy28_Q; solar.beaker.session.id=1644906492328060192125; xhsTracker=url=index&searchengine=google',
            'Host': 'v.xiaohongshu.com',
            'Pragma': 'no-cache',
            'Referer': url,
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36'
        }
        video = requests.get(url, headers=headers)  # 保存视频
        start = time.time()  # 下载开始时间
        size = 0  # 初始化已下载大小
        chunk_size = 100  # 每次下载的数据大小
        content_size = int(video.headers['content-length'])  # 下载文件总大小
        print(video.status_code)
        if video.status_code == 200:  # 判断是否响应成功
            print(str(index) + '[文件 大小]:{size:.2f} MB'.format(size=content_size / 1024 / 1024))  # 开始下载，显示下载文件大小
            v_url = os.path.join(pre_save, '{}.mp4'.format(index))
            # v_url = pre_save + '[' + author_list[i] + '].mp4'
            with open(v_url, 'wb') as file:  # 显示进度条
                for data in video.iter_content(chunk_size=chunk_size):
                    file.write(data)
                    size += len(data)
                    # print('\r' + i + '\n[下载进度]:%s%.2f%%' % (
                    #     '>' * int(size * 50 / content_size), float(size / content_size * 100)))
                end = time.time()  # 下载结束时间
                print('\n' + str(index) + '\n[下载完成]:耗时: %.2f秒\n' % (end - start))  # 输出下载用时时间
    except Exception as error:
        # Downloader.print_ui2(error)
        print(error)
        print('该页视频没有' + str(index) + ',已为您跳过\r')


if __name__ == '__main__':
    ls = []
    if not os.path.exists(pre_save):
        os.makedirs(pre_save)
    with open('../xhs/urls.txt', 'r') as f:
        for line in f:
            if 'http' in line:
                ls.append(line.replace('\n', '').replace(' ', ''))
    size = len(ls)
    for i in range(0, size):
        url = ls[i]
        print('{}-{}'.format(i, url))
        download_url(url, i)
        time.sleep(random.randint(5, 10))
