# 这些脚本你肯定会有用到的

### 操作已打开的chrome浏览器

场景：某些情况我们获取怎么都获取不到cookie，但我们可以使用先在浏览器上登录，然后进行自动化操作。

操作指南：

```shell
需要以该方式启动的浏览器：
win: chrome.exe --remote-debugging-port=9222
mac：/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome  --remote-debugging-port=9222&
```

实现脚本：[chrome.py](./chrome.py)

### excel表的常规操作

场景：word文档生活使用就不用多说了，学会定能给生活带来很大的便利。

操作指南：使用 pandas 开源库实现。

实现脚本：① 考勤统计实现 [kaoqin.py](./kaoqin.py) 。②从excel表取数据翻译后重新写入[gtransfer.py](./gtransfer.py)

### 用ffmpeg批量修改视频的md5值

场景：短视频搬运专用。

操作指南：需要安装ffmpeg环境。

实现脚本：[ff_video.py](./ff_video.py)

### 文件相关操作：json读写、文件子目录文件获取、html转word等

场景：文件的一些操作。

操作指南：略。

实现脚本：[file_util.py](./file_util.py)

### 其他站点爬虫与解析

场景：注意学会BeautifulSoup解析，取属性值等。

操作指南：略。

实现脚本：[other_site.py](./other_site.py)