#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Description: 数据库相关类
@Date       :2021/08/25
@Author     :xhunmon
@Mail       :xhunmon@gmail.com
"""
import os
import shutil
from concurrent.futures import ThreadPoolExecutor
from threading import Lock

from core.conf import Config


class DbLocal(object):
    """
    加载本地文件的url，并进行检测是否合法
    """

    def __init__(self):
        path = Config.get_v2ray_node_path()
        parent_dir = os.path.dirname(os.path.abspath(__file__))
        if path:
            parent_dir = path
        if not os.path.exists(parent_dir):
            os.mkdir(parent_dir)

        self.__save_path = os.path.join(parent_dir, '_db-uncheck.txt')
        self.__get_path = os.path.join(parent_dir, '_db-uncheck.txt')
        if not os.path.isfile(self.__save_path):
            open(self.__save_path, mode='w', encoding="utf-8").write('')
        if not os.path.isfile(self.__get_path):
            open(self.__get_path, mode='w', encoding="utf-8").write('')
        self.__reset()

    def __reset(self):
        """恢复默认状态"""
        self.__checked_urls = []
        self.__load_urls = []
        self.__checked_finish = False
        self.__checked_count = 0

    def __check_url(self, url: str):
        """在异步中检测url是否合法等"""
        self.__checked_count += 1
        # print('check_url: %s' % url)
        # 如果检测通过
        temp = url.strip()
        if len(temp) > 10 and (temp.startswith('ss://') or temp.startswith('vmess://')):
            self.__checked_urls.append(temp)
        if len(self.__load_urls) == self.__checked_count:
            self.__checked_finish = True
            print('已经完成检测')

    def is_checked_finished(self) -> bool:
        """是否已经完成检测"""
        return self.__checked_finish

    def get_checked_urls(self) -> []:
        """已通过检测的url"""
        return self.__checked_urls

    def get_urls(self, is_check=True) -> bool:
        """
        开始加载本地的链接，异步处理结果。
        :param get_path: 本地路径
        :return: True：加载成功
        """
        self.__reset()
        get_path = self.__get_path
        if not os.path.isfile(get_path):
            return False
        try:
            with open(get_path, mode='r') as f:
                for url in f:
                    if url and url not in self.__load_urls:
                        self.__load_urls.append(url)
        except Exception as e:
            print(e)
        finally:
            f.close()
        size = len(self.__load_urls)
        if size == 0:
            print('本地无数据')
            return False
        if is_check:
            # 创建线程池，传入max_workers参数来设置线程池中最多能同时运行的线程数目
            executor = ThreadPoolExecutor(max_workers=3)
            for url in self.__load_urls:
                executor.submit(self.__check_url, url).done()
        else:
            self.__checked_urls = self.__load_urls
            self.__checked_finish = True
        print("已加载数目：%d" % size)
        return True

    def clear_local(self):
        """通过写入空字符实现清除内容"""
        try:
            with open(self.__save_path, mode='w', encoding="utf-8") as f:
                f.write('')
                f.close()
        except Exception as e:
            print(e)

    def save_urls(self, urls, append=True):
        """
        保存节点到本地
        :param urls:
        :param append: 添加到末尾
        :return:
        """
        if not urls:
            return
        all_url = []
        if not append:  # 清空之后再继续
            self.clear_local()
            all_url = urls
        else:  # 把本地的取出来，然后再进行去重
            for url in urls:
                if url not in all_url:
                    all_url.append(url)
            try:
                with open(self.__save_path, mode='r') as f:
                    for url in f:
                        if url and url not in all_url:
                            all_url.append(url)
            except Exception as e:
                print(e)
            finally:
                f.close()
        size = len(all_url)
        print('目前本地总共%d条' % size)
        try:
            self.clear_local()
            with open(self.__save_path, mode='a', encoding="utf-8") as f:
                for url in all_url:
                    url = url.strip().replace('\n', '')
                    if len(url) > 20:
                        f.write(url + '\n')
                f.close()
        except Exception as e:
            print(e)


class DbEnable(object):
    """
    单例模式，提供可用的v2ray对象
    """
    _instance_lock = Lock()

    def __init__(self):
        self.__urls = []
        self.__index = 0
        self.__END = '.back'
        self.__mutex = Lock()
        self.__default_url = 'ss://YWVzLTI1Ni1nY206WWd1c0gyTVdBOFBXYzNwMlZEc1I3QVZ2@81.19.223.189:31764#github.com/freefq%20-%20%E8%8B%B1%E5%9B%BD%20%208'
        self.__config_path = ''
        path = Config.get_v2ray_node_path()
        # 获取本地文件实例？
        parent_dir = os.path.dirname(os.path.abspath(__file__))
        if path:
            parent_dir = path
        if not os.path.exists(parent_dir):
            os.mkdir(parent_dir)
        self.__path = os.path.join(parent_dir, '_db-checked.txt')
        if not os.path.isfile(self.__path):
            open(self.__path, mode='w', encoding="utf-8").write('')

    @classmethod
    def get(cls, *args, **kwargs):
        with DbEnable._instance_lock:
            if not hasattr(DbEnable, "_instance"):
                DbEnable._instance = DbEnable(*args, **kwargs)
        return DbEnable._instance

    def init(self, config_path, def_url=None):
        """
        初始化所需要参数
        :param config_path: 配置文件路径
        :param def_url: 默认使用的 v2ray链接
        :return:
        """
        if def_url is not None:
            self.__default_url = def_url
        if len(config_path) < len('(参考用)config.json'):
            return False
        if not os.path.isfile(config_path):
            return False
        self.__config_path = config_path
        return self.__back_config_json()

    def __back_config_json(self):
        """备份配置文件"""
        if not os.path.isfile(self.__config_path):
            return False
        back_path = self.__config_path + self.__END
        try:
            shutil.copy(self.__config_path, back_path)
        except Exception as e:
            print(e)
            return False
        return True

    def __restore_config_json(self):
        """恢复配置文件"""
        back_path = self.__config_path + self.__END
        if not os.path.isfile(back_path):
            return False
        try:
            if os.path.isfile(self.__config_path):
                os.remove(self.__config_path)
            shutil.copy(back_path, self.__config_path)
        except Exception as e:
            print(e)
            return False
        return True

    def add_url(self, url: str):
        self.__add(url)

    def add_urls(self, url: []):
        self.__adds(url)

    def select_by_order(self):
        """选择下一个代理，并且更新配置文件，让他起作用"""
        url = self.get_by_order()
        return True

    def get_by_order(self):
        """从队列中顺序获取一个v2ray协议实例"""
        def_url = self.__default_url
        if self.__check_and_enable():
            def_url = self.__get(self.__index)
        return def_url

    def __check_and_enable(self):
        """检查是否已到结束，如果是，下一个从0开始"""
        if len(self.__urls) == 0:
            return False
        if len(self.__urls) <= self.__index + 1:
            self.__index = -1
        self.__index += 1
        return True

    def __add(self, url):
        self.__mutex.acquire()
        self.__urls.append(url)
        self.__mutex.release()

    def __adds(self, urls: []):
        self.__mutex.acquire()
        self.__urls.extend(urls)
        self.__mutex.release()

    def __get(self, index):
        self.__mutex.acquire()
        url = self.__urls[index]
        self.__mutex.release()
        return url

    def clear_local(self):
        """通过写入空字符实现清除内容"""
        try:
            with open(self.__path, mode='w', encoding="utf-8") as f:
                f.write('')
                f.close()
        except Exception as e:
            print(e)

    def get_urls(self) -> []:
        """获取截取后的url"""
        urls = []
        try:
            with open(self.__path, mode='r') as f:
                for url in f:
                    url = url.strip().replace('\n', '')
                    if len(url) > 20:
                        urls.append(url.split(',')[0])
        except Exception as e:
            print(e)
        return urls

    def get_infos(self) -> []:
        """获取所有信息，包括ip和地址"""
        infos = []
        try:
            with open(self.__path, mode='r') as f:
                for info in f:
                    info = info.strip().replace('\n', '')
                    if len(info) > 20:
                        infos.append(info)
        except Exception as e:
            print(e)
        return infos

    def de_duplication(self):
        """去重"""
        infos = self.get_infos()
        new_infos = []
        for info in infos:
            if len(info.strip()) <= 0:  # 去空行
                continue
            _in = False
            for n in new_infos:
                if info.split(',')[1] in n:
                    _in = True
                    break
            if not _in:
                new_infos.append(info)
        print('去重前数目：%d，去重后的数目：%d' % (len(infos), len(new_infos)))
        try:
            self.clear_local()
            with open(self.__path, mode='a', encoding="utf-8") as f:
                for url in new_infos:
                    url = url.strip().replace('\n', '')
                    if len(url) > 20:
                        f.write(url + '\n')
                f.close()
        except Exception as e:
            print(e)

    def save_urls(self, urls, append=True):
        """
        保存节点到本地
        :param urls:
        :param append: 添加到末尾
        :return:
        """
        if not urls:
            return
        all_url = []
        if not append:  # 清空之后再继续
            self.clear_local()
            all_url = urls
        else:  # 把本地的取出来，然后再进行去重
            for url in urls:
                if url not in all_url:
                    all_url.append(url)
            try:
                with open(self.__path, mode='r') as f:
                    for url in f:
                        if url and url not in all_url:
                            all_url.append(url)
            except Exception as e:
                print(e)
            finally:
                f.close()
        size = len(all_url)
        print('目前本地总共已检测可用%d条' % size)
        try:
            self.clear_local()
            with open(self.__path, mode='a', encoding="utf-8") as f:
                for url in all_url:
                    url = url.strip().replace('\n', '')
                    if len(url) > 20:
                        f.write(url + '\n')
                f.close()
        except Exception as e:
            print(e)
