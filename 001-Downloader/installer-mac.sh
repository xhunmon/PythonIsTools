#!/bin/bash

pyinstaller -F -i res/logo.ico main.spec -w main.py \
-p type_enum.py \
-p ui.py \
-p utils.py \
-p downloader.py \
-p douyin/dy_download.py \
-p kuaishou/ks_download.py \
-p pytube/captions.py \
-p pytube/cipher.py \
-p pytube/cli.py \
-p pytube/exceptions.py \
-p pytube/extract.py \
-p pytube/helpers.py \
-p pytube/innertube.py \
-p pytube/itags.py \
-p pytube/metadata.py \
-p pytube/monostate.py \
-p pytube/parser.py \
-p pytube/query.py \
-p pytube/request.py \
-p pytube/streams.py \
-p pytube/version.py \
-p pytube/__init__.py \
-p pytube/__main__.py \
-p pytube/contrib/__init__.py \
-p pytube/contrib/channel.py \
-p pytube/contrib/playlist.py \
-p pytube/contrib/search.py