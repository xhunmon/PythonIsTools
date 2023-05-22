#!/bin/bash


#pyinstaller --windowed --name GPT-UI --add-data "config.ini:."  --icon logo.ico main.py gpt.py utils.py

pyinstaller --windowed --name Super86翻译 --add-data "asset/config.ini:asset" --add-data  "asset/ch.ini:asset" --add-data "asset/en.ini:asset" --add-data "asset/language.json:asset"  --icon asset/logo.png main.py config.py core.py utils.py ui.py load_srt.py

#https://blog.csdn.net/COCO56/article/details/117452383
#if use --onefile, the build file is small, but star very slow.
#pyinstaller --onefile --windowed --name GPT-UI --add-data "config.ini:."  --icon logo.ico main.py gpt.py utils.py.py


pyinstaller --windowed --name Super86翻译 --add-data "asset/config.ini:asset" --add-data  "asset/ch.ini:asset" --add-data "asset/en.ini:asset" --add-data "asset/language.json:asset"  --icon asset/logo.png main.py config.py core.py utils.py ui.py load_srt.py -p package --paths /Library/Frameworks/Python.framework/Versions/3.9/lib/python3.9/site-packages