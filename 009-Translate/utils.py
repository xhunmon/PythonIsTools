# -*- coding: utf-8 -*-
"""
@Author  : Xhunmon 
@Time    : 2023/4/22 21:54
@FileName: utils.py
@desc: 
"""
import PySimpleGUI as sg


def get_cache(key: str, default=None):
    """
    获取本地的数据
    :param key:
    :param default:
    :return:
    """
    cache = sg.user_settings_get_entry(key, default)
    if cache is None or cache == '':
        return default
    return cache


def save_cache(key: str, value):
    """
    将数据保存到本地
    :param key:
    :param value:
    :return:
    """
    sg.user_settings_set_entry(key, value)


def read(file_path) -> str:
    '''读取txt文本内容'''
    content = None
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            f.close()
    except Exception as e:
        print(e)
    return content


def write(content, file_path):
    '''写入txt文本内容'''
    try:
        with open(file_path, mode='w', encoding='utf-8') as f:
            f.write(content)
    except Exception as e:
        print(e)


def get_theme():
    """
    Get the theme to use for the program
    Value is in this program's user settings. If none set, then use PySimpleGUI's global default theme
    :return: The theme
    :rtype: str
    """
    theme = get_cache(Key.THEME, '')
    if theme == '':
        theme = sg.OFFICIAL_PYSIMPLEGUI_THEME  # 默认主题
    return theme


class Key:
    """
    统一管理本地字符串
    """
    PROXY_ENABLE = 'proxy_enable'  # settings
    PROXY_LAYOUT = 'proxy_layout'  # settings
    PROXY_INPUT = 'proxy_input'  # settings
    THEME = 'theme'  # settings
    RESTART_WINDOW = 'restart_window'  # settings
    ADVANCED_MODE = 'advanced_mode'  # settings
    FULL_TRANSLATE = 'full_translate'  # settings
    LANGUAGE = 'language'  # config

    # main
    M_CLEAR = 'Clear'
    M_RUN = 'Run'
    M_COPY = 'Copy'
    M_FILE = 'File'
    M_SETTINGS = 'Settings'
    M_EXIT = 'Exit'
