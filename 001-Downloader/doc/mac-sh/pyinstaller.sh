#!/bin/bash

pyinstaller -F -i res/logo.ico main.spec main.py  -w \
-p type_enum.py \
-p ui.py \
-p utils.py \
-p downloader.py \
-p douyin/dy_download.py \
-p kuaishou/ks_download.py