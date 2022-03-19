#!/bin/bash

pyinstaller -F -i res/logo.ico main.spec main.py  -w \
-p type_enum.py \
-p ui.py \
-p utils.py \
-p ff_util.py \
-p editors.py \
-p ff_cut.py