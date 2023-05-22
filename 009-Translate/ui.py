# -*- coding: utf-8 -*-
"""
@Author  : Xhunmon 
@Time    : 2023/4/22 22:31
@FileName: ui.py
@desc: 
"""
from config import *


def loading_show():
    LoadingWin.is_loading = True
    layout = [[sg.Text(conf.loading('Content'), font='ANY 15')],
              [sg.Image(data=conf.config('Loading').encode('utf-8'), key='_IMAGE_')],
              [sg.Button(conf.loading('Cancel'))]
              ]
    window = sg.Window('').Layout(layout)
    while LoadingWin.is_loading:  # Event Loop
        event, values = window.Read(timeout=25)
        if event in (None, 'Exit', conf.loading('Cancel')):
            break
        window.Element('_IMAGE_').UpdateAnimation(conf.config('Loading').encode('utf-8'), time_between_frames=50)
    window.close()


class LoadingWin(object):
    """
    loading dialog
    """
    is_loading = True


def settings_show():
    """
    Show the settings window.
    This is where the folder paths and program paths are set.
    Returns True if settings were changed

    :return: True if settings were changed
    :rtype: (bool)
    """
    global_theme = get_theme()
    proxy_enable = get_cache(Key.PROXY_ENABLE, False)
    translate_enable = get_cache(Key.FULL_TRANSLATE, False)
    restart_enable = get_cache(Key.RESTART_WINDOW, True)

    layout = [
        [sg.T('  ', font='_ 16', size=(40, 1))],
        [sg.T(conf.settings('Proxy'), font='_ 16')],
        [sg.CB(conf.settings('ProxyEnable'), default=proxy_enable, enable_events=True, k=Key.PROXY_ENABLE,
               font='_ 12')],
        [sg.Column([[sg.Input(size=(38, 1), default_text=get_cache(Key.PROXY_INPUT, ''), key=Key.PROXY_INPUT),
                     sg.T(conf.settings('ProxyDesc'), font='_ 12')]],
                   expand_x=True, expand_y=True, k=Key.PROXY_LAYOUT, visible=proxy_enable)],
        [sg.T(conf.settings('Theme'), font='_ 16')],
        [sg.T(conf.settings('ThemeDesc'), font='_ 11'), sg.T(global_theme, font='_ 13')],
        [sg.Combo([''] + sg.theme_list(), get_cache(Key.THEME, ''), readonly=True, k=Key.THEME)],
        [sg.CB(conf.settings('Advanced'), default=get_cache(Key.ADVANCED_MODE, True), font='_ 12',
               k=Key.ADVANCED_MODE)],
        [sg.CB(conf.settings('FullTranslate'), visible=False, default=translate_enable, font='_ 12',
               k=Key.ADVANCED_MODE)],
        [sg.CB(conf.settings('Restart'), default=restart_enable, enable_events=True, k=Key.RESTART_WINDOW,
               font='_ 12')],
        [sg.B(conf.settings('Ok'), bind_return_key=True), sg.B(conf.settings('Cancel')), sg.B(conf.settings('Reset'))],
    ]

    window = sg.Window(conf.settings('Title'), layout, finalize=True)
    settings_changed = False

    while True:
        event, values = window.read()
        if event in (conf.settings('Cancel'), sg.WIN_CLOSED):
            break
        if event == conf.settings('Ok'):
            save_cache(Key.THEME, values[Key.THEME])
            save_cache(Key.ADVANCED_MODE, values[Key.ADVANCED_MODE])
            save_cache(Key.PROXY_ENABLE, proxy_enable)
            save_cache(Key.FULL_TRANSLATE, translate_enable)
            save_cache(Key.PROXY_INPUT, window[Key.PROXY_INPUT].get())
            save_cache(Key.RESTART_WINDOW, window[Key.RESTART_WINDOW].get())
            settings_changed = True
            break
        elif event == conf.settings('Reset'):  # 恢复所有默认设置
            save_cache(Key.THEME, '')
            save_cache(Key.ADVANCED_MODE, False)
            save_cache(Key.PROXY_ENABLE, False)
            save_cache(Key.FULL_TRANSLATE, False)
            save_cache(Key.RESTART_WINDOW, True)
            save_cache(Key.PROXY_INPUT, '')
            settings_changed = True
            break
        elif event == Key.PROXY_ENABLE:
            proxy_enable = values[Key.PROXY_ENABLE]
            window[Key.PROXY_ENABLE].update(value=proxy_enable)
            window[Key.PROXY_LAYOUT].update(visible=proxy_enable)
        elif event == Key.FULL_TRANSLATE:
            translate_enable = values[Key.FULL_TRANSLATE]
            window[Key.FULL_TRANSLATE].update(value=translate_enable)
        elif event == Key.RESTART_WINDOW:
            restart_enable = values[Key.RESTART_WINDOW]
            window[Key.RESTART_WINDOW].update(value=restart_enable)

    window.close()
    return settings_changed, restart_enable
