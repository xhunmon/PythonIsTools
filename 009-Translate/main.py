# -*- coding: utf-8 -*-
"""
@Author  : Xhunmon 
@Time    : 2023/4/21 23:03
@FileName: guiv2.py
@desc: 
"""
import PySimpleGUI as sg

from core import *
from ui import *
from ui import settings_show
from utils import *


class MainWin(object):
    def __init__(self):
        self.tl = Translation()
        self.lw = LoadingWin()

    def advanced_ui(self, window):
        # 高级才显示的UI
        advanced_mode = get_cache(Key.ADVANCED_MODE, False)
        window[Key.PROXY_ENABLE].update(visible=advanced_mode)

    def make_window(self):
        """
        Creates the main window
        :return: The main window object
        :rtype: (sg.Window)
        """
        sg.theme(get_theme())

        left_col = sg.Column([
            [sg.Multiline(size=(50, 25), write_only=True, expand_x=True, expand_y=True, key='IN_TEXT',
                          reroute_stdout=True,
                          echo_stdout_stderr=True, reroute_cprint=True)],
            [sg.B(conf.main(Key.M_RUN)), sg.B(conf.main(Key.M_CLEAR)), sg.B(conf.main(Key.M_COPY)),
             sg.Input('', key="_FILEBROWSE_", enable_events=True, visible=False),
             sg.FileBrowse(conf.main(Key.M_FILE), file_types=(('ALL files', '.*')),
                           target='_FILEBROWSE_')],
            [sg.CB(conf.main('EnableProxy'), default=get_cache(Key.PROXY_ENABLE, False), font='_ 12',
                   enable_events=True, k=Key.PROXY_ENABLE)]], element_justification='l', expand_x=True, expand_y=True)

        right_col = [
            [sg.Multiline(size=(70, 25), write_only=True, expand_x=True, expand_y=True, key='OUT_TEXT',
                          reroute_stdout=True,
                          echo_stdout_stderr=True, reroute_cprint=True)],
            [sg.B(conf.main(Key.M_SETTINGS)), sg.Button(conf.main(Key.M_EXIT))],
            [sg.T(conf.main('Version') + conf.config('Version'))]
        ]
        operation_at_bottom = sg.pin(sg.Column([[sg.T(conf.main('Business'), font='Default 12', pad=(0, 0)),
                                                 sg.T(conf.main('Email') + conf.config('Email') + '  ',
                                                      font='Default 12', pad=(0, 0)),
                                                 sg.T(conf.main('RedBook') + conf.config('RedBook') + '  ',
                                                      font='Default 12',
                                                      pad=(0, 0))]],
                                               pad=(0, 0), k='-OPTIONS BOTTOM-', expand_x=True, expand_y=False),
                                     expand_x=True, expand_y=False)
        self.tl.select_translator = get_cache('PLATFORM_TYPES', 'baidu')
        self.tl.set_from_lang(get_cache('INPUT_TYPES'))
        self.tl.set_to_lang(get_cache('OUTPUT_TYPES'))
        self.tl.check_select_language()
        lgs1 = self.tl.get_languages()
        lgs1.insert(0, '自动') if is_zh_language() else lgs1.insert(0, 'auto')
        choose_type_at_top = sg.pin(
            # sg.user_settings_get_entry('INPUT_TYPES', lgs1)
            sg.Column([[sg.Combo(values=lgs1, default_value=self.tl.select_from_lang, size=(50, 30),
                                 key='IN_TYPE', enable_events=True, readonly=True),
                        # sg.Combo(sg.user_settings_get_entry('OUTPUT_TYPES', lgs2),
                        sg.Combo(values=self.tl.get_languages(), default_value=self.tl.select_to_lang,
                                 size=(50, 30), key='OUT_TYPE', enable_events=True, readonly=True),
                        # sg.Combo(sg.user_settings_get_entry('PLATFORM_TYPES', tls),
                        sg.Combo(values=self.tl.get_translators(), default_value=self.tl.select_translator,
                                 size=(20, 30), key='PLATFORM_TYPE', enable_events=True, readonly=True)
                        ]], pad=(0, 0), k='-FOLDER CHOOSE-'))

        # ----- Full layout -----

        layout = [
            [sg.Text(conf.main('Description'), font='Any 15', pad=(0, 5))],
            [choose_type_at_top],
            [sg.Pane(
                [sg.Column([[left_col]], element_justification='l', expand_x=True, expand_y=True),
                 sg.Column(right_col, element_justification='c', expand_x=True, expand_y=True)], orientation='h',
                relief=sg.RELIEF_SUNKEN, expand_x=True, expand_y=True, k='-PANE-')],
            [operation_at_bottom, sg.Sizegrip()]]

        # --------------------------------- Create Window ---------------------------------
        window = sg.Window(conf.main('Title'), layout, finalize=True, resizable=True, use_default_focus=False)
        window.set_min_size(window.size)

        window.bind('<F1>', 'Exit')
        # window.bind("<Enter>", 'Enter')
        window['IN_TEXT'].bind('<Return>', ' Return')
        self.advanced_ui(window)

        window.bring_to_front()
        return window

    def show(self):
        """
            The main program that contains the event loop.
            It will call the make_window function to create the window.
            """
        global python_only
        # icon = sg.EMOJI_BASE64_HAPPY_WINK
        icon = conf.config('Logo').encode('utf-8')
        # icon = os.path.join(os.path.dirname(__file__), 'doc', 'logo.ico')
        # sg.user_settings_filename('psgdemos.json')
        sg.set_options(icon=icon)
        window = self.make_window()
        window.force_focus()
        counter = 0

        while True:
            event, values = window.read()
            # print(event, values)

            counter += 1
            if event in (sg.WINDOW_CLOSED, conf.main(Key.M_EXIT)):
                break
            elif event == conf.main(Key.M_SETTINGS):
                change, restart = settings_show()
                if change:  # settings 可能更改的内容：主题，代理，高级
                    if restart:
                        window.close()
                        window = self.make_window()
                    else:
                        self.advanced_ui(window)

            elif event == conf.main(Key.M_RUN) or event == 'IN_TEXT Return':  # IN_TEXT 的回车键监听, 需要从input获取到数据，然后进行翻译
                sg.threading.Thread(target=self.tl.translate, args=(window, window['IN_TEXT'].get(), False),
                                    daemon=True).start()
                loading_show()
                # result = ts.translate_text(text, translator='deepl', from_language='zh', to_language='en')
                # window['OUT_TEXT'].update(result)
                # pw.close()
            elif event == conf.main(Key.M_CLEAR):
                window['IN_TEXT'].update('')
                window['OUT_TEXT'].update('')
            elif event == conf.main(Key.M_COPY):
                sg.clipboard_set(window['OUT_TEXT'].get())
            elif event == '_FILEBROWSE_':
                file_path: str = values['_FILEBROWSE_']
                # 不判断了，能解析就用
                # if file_path.endswith('.txt') or file_path.endswith('.html'):
                content = read(file_path)
                window['IN_TEXT'].update(file_path)
                sg.threading.Thread(target=self.tl.translate,
                                    args=(window, content, file_path.endswith('.html'), file_path), daemon=True).start()
                loading_show()
            elif event == 'IN_TYPE':  # 输入
                type1 = values['IN_TYPE']
                self.tl.select_from_lang = type1
                get_cache('INPUT_TYPES', type1)
            elif event == 'OUT_TYPE':  # 输出
                type1 = values['OUT_TYPE']
                self.tl.select_to_lang = type1
                save_cache('OUTPUT_TYPES', type1)
            elif event == 'PLATFORM_TYPE':  # 选择平台后，更新输入输出的可选
                type1 = values['PLATFORM_TYPE']
                self.tl.select_translator = type1
                save_cache('PLATFORM_TYPES', type1)
                window.close()
                window = self.make_window()
            elif event == 'Version':
                sg.popup_scrolled(sg.get_versions(), keep_on_top=True, non_blocking=True)
            elif event == Key.PROXY_ENABLE:  # 高级时在本窗口开启或关闭代理，但是需要在设置中设置代理地址
                proxy_enable = values[Key.PROXY_ENABLE]
                save_cache(Key.PROXY_ENABLE, proxy_enable)
                window[Key.PROXY_ENABLE].update(value=proxy_enable)
        window.close()


if __name__ == '__main__':
    MainWin().show()
