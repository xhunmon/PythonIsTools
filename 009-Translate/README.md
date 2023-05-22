# 多平台免费翻译神器

## 1. 输入框翻译

直接在输入框输入内容，选择目标语言，翻译平台即可。


## 2.文件翻译

- 1.支持txt翻译，但是文本内容不宜过大

- 2.支持html翻译

- 3.定制版srt字幕文件翻译，自定义修改[load_srt.py](load_srt.py)

- 4.其他文本文件也是可以的，但是肯定有bug


## 3.打包应用程序

可以自行打包 exe和Mac平台的app。打包脚本参考[doc/pyinstall.sh](doc/pyinstaller.sh)，注意window平台的路径反斜杠更改。


> 主要引入：translators