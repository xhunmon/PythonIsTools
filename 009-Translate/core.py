# -*- coding: utf-8 -*-
"""
@Author  : Xhunmon 
@Time    : 2023/4/22 22:29
@FileName: core.py
@desc: 
"""
import translators as ts

from config import *
from ui import LoadingWin


class Language(object):

    def __init__(self, id_name, full_name, zh_name=None, google=True, yandex=True, bing=True, baidu=True, alibaba=True,
                 tencent=True, youdao=True, sogou=True, deepl=True, caiyun=True, argos=True):
        self.id_name = id_name
        self.zh_name = zh_name if zh_name else full_name
        self.full_name = full_name
        self.google = google
        self.yandex = yandex
        self.bing = bing
        self.baidu = baidu
        self.alibaba = alibaba
        self.tencent = tencent
        self.youdao = youdao
        self.sogou = sogou
        self.deepl = deepl
        self.caiyun = caiyun
        self.argos = argos

    def is_enable(self, translator: str):
        return eval('self.' + translator)


class Translation(object):
    def __init__(self):
        self.is_full = get_cache(Key.FULL_TRANSLATE, False)  # 显示所有翻译平台和语言，但是未校验
        self.is_zh = is_zh_language()  # 是否是中文
        self.select_translator = 'baidu'
        self.select_from_lang = '自动' if self.is_zh else 'auto'
        self.select_to_lang = '英语' if self.is_zh else 'english'
        self.languages = conf.translate()
        # self.languages.append(Language('en', 'english', '英语'))
        # self.languages.append(Language('zh', 'chinese', '中文'))
        # self.languages.append(Language('ar', 'arabic', '阿拉伯语', deepl=False, caiyun=False))
        # self.languages.append(Language('ru', 'russian', '俄语'))
        # self.languages.append(Language('fr', 'french', '法语'))
        # self.languages.append(Language('de', 'german', '德语', alibaba=False, caiyun=False))
        # self.languages.append(Language('es', 'spanish', '西班牙语'))
        # self.languages.append(Language('pt', 'portuguese', '葡萄牙语', caiyun=False))
        # self.languages.append(Language('it', 'italian', '意大利语', caiyun=False))
        # self.languages.append(Language('ja', 'japanese', '日本语', alibaba=False))
        # self.languages.append(Language('ko', 'korean', '朝鲜语', alibaba=False, deepl=False, caiyun=False))
        # self.languages.append(
        #     Language('el', 'greek', '希腊语', alibaba=False, tencent=False, youdao=False, caiyun=False, argos=False))

    def set_to_lang(self, lang):
        if lang:
            self.select_to_lang = lang

    def set_from_lang(self, lang):
        if lang:
            self.select_from_lang = lang

    def check_select_language(self):
        languages = self.get_languages()
        has_from = False
        has_to = False
        for lg in languages:  # lg为full_name
            if lg == self.select_from_lang:
                has_from = True
            if lg == self.select_to_lang:
                has_to = True
        if not has_from:
            self.select_from_lang = '自动' if self.is_zh else 'auto'
        if not has_to:
            self.select_to_lang = '英语' if self.is_zh else 'english'

    def get_translators(self):
        # 'google', 'yandex', 'bing', 'baidu', 'alibaba', 'tencent', 'youdao', 'sogou', 'deepl', 'caiyun', 'argos',
        # 'apertium', 'cloudYi', 'elia', 'iciba', 'iflytek', 'iflyrec', 'itranslate', 'judic', 'languageWire',
        # 'lingvanex', 'niutrans', 'mglip', 'modernMt', 'myMemory', 'papago', 'qqFanyi', 'qqTranSmart', 'reverso',
        # 'sysTran', 'tilde', 'translateCom', 'translateMe', 'utibet', 'volcEngine', 'yeekit'
        # {"en_name": "Chinese(简体)", "id_name": "zh-CHS", "zh_name": "简体", "google": "zh-CN", "yandex": "zh", "bing": "zh-Hans", "baidu": "zh", "alibaba": "zh", "tencent": "zh", "youdao": "Y", "sogou": "Y", "deepl": "zh", "caiyun": "zh", "argos": "zh"}
        tors = list(self.languages[0].keys())
        tors.remove('en_name')
        tors.remove('id_name')
        tors.remove('zh_name')
        return tors

    def get_languages(self):
        support = []
        for lg in self.languages:  # 取出字典
            if lg[self.select_translator] == '':  # 不支持
                continue
            if self.is_zh:
                support.append(lg['zh_name'])
            else:
                support.append(lg['en_name'])
        return support

    def choose_translator(self, tl):
        self.select_translator = tl

    def _search_id_name(self, is_from=True):
        key = self.select_from_lang if is_from else self.select_to_lang
        for lg in self.languages:  # 取出字典
            if self.is_zh:  # 查找出 zh_name 对应的
                if lg['zh_name'] == key:
                    if lg[self.select_translator] == '':
                        continue
                    elif lg[self.select_translator] == 'Y':
                        return lg['id_name']
                    else:
                        return lg[self.select_translator]
            else:
                if lg['en_name'] == key:
                    if lg[self.select_translator] == '':
                        continue
                    elif lg[self.select_translator] == 'Y':
                        return lg['id_name']
                    else:
                        return lg[self.select_translator]
        return None

    def get_id_name(self, is_from=True):
        if is_from:
            from_key = self.select_from_lang
            if from_key == '自动' or from_key == 'auto':
                return 'auto'
            search = self._search_id_name(True)
            return search if search else 'auto'
        else:  # to_ 目标
            search = self._search_id_name(False)
            return search if search else 'en'  # 最后还是没有，默认英语

    def translate(self, window, content, is_html=False, file_path: str = None):
        try:
            if file_path and file_path.endswith('.srt'):
                from load_srt import Translator
                import utils, os
                filename, ext = os.path.splitext(file_path)
                out_path = f'{filename}_output{ext}'
                tl = Translator()
                proxy = get_cache(Key.PROXY_INPUT, None) if get_cache(Key.PROXY_ENABLE, False) else None
                if proxy:
                    proxy_real = proxy.replace(' ', '').replace('\n', '')
                    proxy_spit = proxy_real.split('://')
                    proxy_user = {proxy_spit[0]: proxy_real}
                    tl.proxy_user = proxy_user
                else:
                    tl.proxy_user = None
                tl.translators = {self.select_translator: 3}
                tl.translate_file(file_path, out_path, self.get_id_name(is_from=True), self.get_id_name(is_from=False))
                window['OUT_TEXT'].update(f'输出文件：{out_path}')
            else:
                # ts.preaccelerate()
                # 是否使用了代理 export https_proxy=http://127.0.0.1:7890 http_proxy=http://127.0.0.1:7890 all_proxy=socks5://127.0.0.1:7890
                proxy = get_cache(Key.PROXY_INPUT, None) if get_cache(Key.PROXY_ENABLE, False) else None
                proxy_user = None
                if proxy:
                    proxy_real = proxy.replace(' ', '').replace('\n', '')
                    proxy_spit = proxy_real.split('://')
                    proxy_user = {proxy_spit[0]: proxy_real}
                if is_html:
                    # result = ts.translate_html(content, translator=self.select_translator,
                    #                            from_language=self.get_id_name(is_from=True),
                    #                            to_language=self.get_id_name(is_from=False), proxies=proxy_user)
                    result = ts.translate_html(content, translator=self.select_translator,
                                               from_language=self.get_id_name(is_from=True),
                                               to_language=self.get_id_name(is_from=False), proxies=proxy_user,
                                               if_ignore_empty_query=True, if_show_time_stat=True)
                else:
                    result = ts.translate_text(content, translator=self.select_translator,
                                               from_language=self.get_id_name(is_from=True),
                                               to_language=self.get_id_name(is_from=False), proxies=proxy_user)
                if file_path is not None:
                    import utils, os
                    filename, ext = os.path.splitext(file_path)
                    out_path = f'{filename}_output{ext}'
                    utils.write(result, out_path)
                    window['OUT_TEXT'].update(f'输出文件：{out_path}')
                else:
                    window['OUT_TEXT'].update(result)
        except Exception as e:
            result = str(e)
        LoadingWin.is_loading = False
