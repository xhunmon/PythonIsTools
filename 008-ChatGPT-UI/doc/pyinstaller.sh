#!/bin/bash


pyinstaller --windowed --name GPT-UI --add-data "config.ini:."  --icon logo.ico main.py gpt.py utils.py

#if use --onefile, the build file is small, but star very slow.
#pyinstaller --onefile --windowed --name GPT-UI --add-data "config.ini:."  --icon logo.ico main.py gpt.py utils.py
