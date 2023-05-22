# -*- coding: utf-8 -*-
"""
@Author  : Xhunmon 
@Time    : 2023/4/18 14:47
@FileName: load_srt.py
@desc: 从本地加载srt字幕文件
"""
import os
import threading
import time


class Tag:
    def __init__(self):
        self.num = None
        self.duration = None
        self.msg = ''


class Translator(object):
    STATUS_SUCCESS = 1
    STATUS_FAIL = -1

    def __init__(self):
        # TODO --> 一定要对应自己的代理，可以为None
        self.proxy_user = {"socks5": "socks5://127.0.0.1:7890"}
        # 翻译平台，deepl尝试3次，失败后，用google尝试2次，再失败后，用百度尝试3次，当所有尝试都失败了，表示该次翻译失败
        self.translators = {"deepl": 3, "google": 2, "baidu": 3}
        # 是否支持翻译
        self.__supports = ['.srt', '.txt']
        # 需翻译的语音，可以为自动：auto
        self.__from_language = 'zh'
        # 目标语言
        self.__to_language = 'en'
        # 一次性翻译的字符串数组长度
        self.__one_length = 1024
        # 某些场景需要休眠时间，再进行尝试
        self.__user_sleep = 2
        # 监听的事件
        self.__listener = None
        # 需要被翻译的文件路径
        self.__list = []

    def __callback(self, status, src, dst, msg=None):
        """
        翻译结果回调
        :param status: 1成功，2失败
        :param src: 返回需要翻译的路径
        :param dst: 返回翻译后的文件路径
        :param msg: 返回提示信息
        """
        if self.__listener:
            self.__listener(status, src=src, dst=dst, msg=msg)

    def __support_file(self, src: str):
        """
        判断源文件是否支持被翻译
        :param src: 文件路径
        :return:
        """
        for item in self.__supports:
            if src.endswith(item):
                return True
        return False

    def __deal_file(self):
        """
        从队列取出文件，进行相关判断和操作
        :return: （是否成功，源文件路径，目标文件路径，操作信息，临时文件路径）
        """
        item = self.__list.pop(0)
        src, dst = item[0], item[1]
        temp = None
        if not os.path.exists(src):
            return False, src, dst, "源文件不存在", temp
        if not self.__support_file(src):
            return False, src, dst, "源文件格式不支持", temp
        # try:
        #     folder = os.path.dirname(src)
        #     filename, ext = os.path.splitext(src)
        #     if dst is None:
        #         dst = os.path.join(folder, '{}_out{}'.format(filename, ext))
        #     else:
        #         folder = os.path.dirname(dst)
        #         if not os.path.exists(folder):
        #             os.mkdir(folder)
        #     temp = os.path.join(folder, '{}_temp{}'.format(filename, ext))
        # except Exception as e:
        #     return False, src, dst, str(e), temp
        if dst is None or dst == '':
            folder = os.path.dirname(src)
            filename, ext = os.path.splitext(src)
            dst = os.path.join(folder, '{}_out{}'.format(filename, ext))
        if os.path.exists(dst):
            os.remove(dst)
        return True, src, dst, '成功', temp

    def __parse_srt(self, src: str):
        """
        获取srt文件内容，一行一行的
        :param src: 路径
        :return: [Line,Line...]
        """
        i = 0
        # 遇到空一行方为一组
        tags = []
        tag = Tag()
        with open(src, 'r', encoding="utf-8") as f:
            for line in f:
                line = line.strip().replace('\n', '')
                if line == '':  # 结束了
                    tags.append(tag)
                    i = 0
                    tag = Tag()
                    continue
                if i == 0:
                    tag.num = line
                elif i == 1:
                    tag.duration = line
                else:
                    tag.msg += line
                i += 1
        return tags

    def __parse_file(self, src: str):
        """
        一行一行获取文件内容
        :param src: 文件路径
        :return: 返回[Line, Line...]
        """
        if src.endswith('.srt'):
            return self.__parse_srt(src)
        return []

    def __merge_content(self, tags):
        """
        合并需要翻译的内容，为了避免请求其次太多，将整个文件的内容进行分组翻译
        :param tags:
        :return:
        """
        result = []
        item = ''
        for tag in tags:
            if item == '':
                item = tag.msg
            else:
                item = item + '\n' + tag.msg
            if len(item) > self.__one_length:  # 开启下一组
                result.append(item)
                item = ''
        if item != '':  # 最后一组数据
            result.append(item)
        return result

    def __request_item(self, content):
        """
        真正的请求网络进行翻译
        :param content: 翻译内容
        :return: 是否成功，翻译后的内容
        """
        for key, value in self.translators.items():
            for i in range(1, value + 1):  # 每个失败后尝试的次数
                try:
                    print('使用 {} 翻译，进行次数{}'.format(key, i))
                    import translators as ts
                    item = ts.translate_text(content, translator=key, from_language=self.__from_language,
                                             to_language=self.__to_language, proxies=self.proxy_user)
                    return True, item
                except Exception as e:
                    print(e)
                    time.sleep(self.__user_sleep)

        return False, '翻译失败'

    def __request_list(self, contents):
        """
        拆分列表中的数据
        :param contents:
        :return:
        """
        results = []
        for content in contents:
            success, item = self.__request_item(content)
            if not success:
                return False, results
            for x in item.split('\n'):
                results.append(x)
        return True, results

    def __merge_file(self, tags, items, dst):
        with open(dst, 'w', encoding="utf-8") as f:
            for tag in tags:
                f.write(f'{tag.num}\n')
                f.write(f'{tag.duration}\n')
                f.write(f'{items.pop(0)}\n')
                f.write('\n')

    def __translate(self):
        """
        子线程不断监听翻译文件，进行翻译
        """
        success, src, dst, msg, temp = self.__deal_file()
        if not success:
            self.__callback(Translator.STATUS_FAIL, src=src, dst=dst, msg=msg)
            return
        # 解析得到一行行数据
        tags = self.__parse_file(src)
        if len(tags) <= 0:
            self.__callback(Translator.STATUS_FAIL, src=src, dst=dst, msg="解析文件内容失败")
            return
            # 将一行行待翻译的文件进行合并，减少翻译次数
        contents = self.__merge_content(tags)
        success, results = self.__request_list(contents)
        if not success:
            # # 缓存已翻译的数据
            # if len(result) > 0:
            #     self.__merge_file(tags, result, temp)
            self.__callback(Translator.STATUS_FAIL, src=src, dst=dst, msg='翻译失败')
            return
        self.__merge_file(tags, results, dst)
        self.__callback(Translator.STATUS_SUCCESS, src=src, dst=dst, msg="成功")

    def add_callback(self, listener):
        """
        添加监听器，
        :param listener: 监听器设计模式如：method_listener(status,**kwargs)
        :return:
        """
        self.__listener = listener

    def translate_file(self, src, dst=None, from_lang='zh', to_lang='en'):
        """
        对外只需要知道传入的文件即可，其余全部在本翻译器处理，较少参数传递
        @param dst: 必传，需要进行翻译的文件。
        @param src: 如果不传，自动根据src所在的目录生成同后缀名的文件
        @param from_lang: 从什么语言翻译
        @param to_lang: 翻译目标语言
        """
        self.__from_language = from_lang
        self.__to_language = to_lang
        item = (src, dst)
        self.__list.append(item)
        # self.__event.set()  # 唤醒线程
        self.__translate()
