# v2ray节点代理池
学习python爬虫过程中，我们需要一些代理。而本项目则是通过收集网上公开的节点，来实现自己的代理请求的过程！

## v2ray是什么？如何使用？
- [v2ray官方指导](https://www.v2ray.com/index.html)
  
- [v2ray wiki](https://zh.wikipedia.org/wiki/V2Ray)

## v2ray客户端推荐
- [window：v2rayN](https://github.com/2dust/v2rayN/releases)
- [macOS：V2rayU](https://github.com/yanue/V2rayU/releases)
- [android：v2rayNG](https://github.com/2dust/v2rayNG/releases)
- ios推荐Shadowrocket（俗称小火箭，注意不是shadowrocket VPN），但需要付费的，可以通过找"美区apple id共享2021小火箭"，找共享的账号下载软件，但是会有风险，请一定要注意。

## v2ray服务端推荐
有些应用场景会需要到用到专用的ip代理，如Tik Tok、亚马逊和Facebook等。这是，我们通过购买国外的服务器或者vps来搭建代理服务器，从而实现专有ip代理。

推荐使用[x-ui](https://github.com/vaxilu/x-ui) 进行非常简单的"一键式"搭建开源框架。 

#本项目主要知识点
学习本项目需要先了解代理原理，以及v2ray实现的原理。

## 实现思路
![实现思路图](./doc/v2ray.jpg)

## v2ray内核使用
我们找的是v2ray节点，所以这些协议只能运行在v2ray特有程序中。因此，我们要找[v2ray内核](https://github.com/v2ray/v2ray-core/releases) 。 这里就以macOS系统举例说明：
1. 下载[v2ray-core-v4.31.0](https://github.com/v2fly/v2ray-core/releases/download/v4.31.0/v2ray-macos-64.zip)
2. 配置解压目录的路径：
```python
Config.set_v2ray_core_path('xxx/Downloads/v2ray-macos-64')
```
3. 查看是否能正常启动：
```python
client.Creator().v2ray_start('ss://YWVzLTI1Ni1nY206WXlDQmVEZFlYNGNhZEhwQ2trbWRKTHE4@37.120.144.211:43893#github.com/freefq%20-%20%E7%BD%97%E9%A9%AC%E5%B0%BC%E4%BA%9A%20%2041')
```

## 2021-12-30检测可用测试节点(注意去掉后面","开始的内容)：
```shell
ss://Y2hhY2hhMjAtaWV0Zi1wb2x5MTMwNTpzRjQzWHQyZ09OcWNnRlg1NjNAMTQxLjk1LjAuMjY6ODI2#%E4%BA%8C%E7%88%B7%E7%BF%BB%E5%A2%99%E7%BD%91+https%3A%2F%2F1808.ga,54.38.217.138,德国黑森
trojan://8cf83f44-79ff-4e50-be1a-585c82338912@t1.ssrsub.com:8443#github.com/freefq%20-%20%E5%8A%A0%E6%8B%BF%E5%A4%A7%20%209,142.47.89.64,加拿大安大略
ss://YWVzLTI1Ni1nY206UENubkg2U1FTbmZvUzI3@198.57.27.218:8090#github.com/freefq%20-%20%E5%8C%97%E7%BE%8E%E5%9C%B0%E5%8C%BA%20%2016,198.57.27.218,加拿大多伦多
ss://YWVzLTI1Ni1nY206ZzVNZUQ2RnQzQ1dsSklk@38.75.136.93:5003#github.com/freefq%20-%20%E7%BE%8E%E5%9B%BD%E5%8D%8E%E7%9B%9B%E9%A1%BFCogent%E9%80%9A%E4%BF%A1%E5%85%AC%E5%8F%B8%2017,38.75.136.93,美国加利福尼亚洛杉矶 Cogent
ss://YWVzLTI1Ni1nY206UENubkg2U1FTbmZvUzI3@46.29.218.6:8091#github.com/freefq%20-%20%E6%8C%AA%E5%A8%81%20%2021,46.29.218.6,挪威
trojan://8cf83f44-79ff-4e50-be1a-585c82338912@t2.ssrsub.com:8443#github.com/freefq%20-%20%E4%BF%84%E7%BD%97%E6%96%AF%20%2028,195.133.53.209,俄罗斯莫斯科
vmess://ew0KICAidiI6ICIyIiwNCiAgInBzIjogIkBTU1JTVUItVjA2LeS7mOi0ueaOqOiNkDpzdW8ueXQvc3Nyc3ViIiwNCiAgImFkZCI6ICJzaGN1MDEuaXBsYzE4OC5jb20iLA0KICAicG9ydCI6ICIxMDAwNCIsDQogICJpZCI6ICI2NWNhYzU2ZC00MTU1LTQzYzgtYmFlMC1mMzY4Y2IyMWY3NzEiLA0KICAiYWlkIjogIjEiLA0KICAic2N5IjogImF1dG8iLA0KICAibmV0IjogInRjcCIsDQogICJ0eXBlIjogIm5vbmUiLA0KICAiaG9zdCI6ICJzaGN1MDEuaXBsYzE4OC5jb20iLA0KICAicGF0aCI6ICIiLA0KICAidGxzIjogIiIsDQogICJzbmkiOiAiIg0KfQ==,61.216.19.199,中国台湾台北 中華電信
vmess://ew0KICAidiI6ICIyIiwNCiAgInBzIjogIkBTU1JTVUItVjIyLeS7mOi0ueaOqOiNkDpzdW8ueXQvc3Nyc3ViIiwNCiAgImFkZCI6ICIxOTguMjAwLjUxLjE4IiwNCiAgInBvcnQiOiAiNjAwIiwNCiAgImlkIjogIjQyZjdlYWJlLTBkM2YtMTFlYy04NTliLTAwMTYzY2FmNDgxYyIsDQogICJhaWQiOiAiMCIsDQogICJzY3kiOiAiYXV0byIsDQogICJuZXQiOiAidGNwIiwNCiAgInR5cGUiOiAibm9uZSIsDQogICJob3N0IjogIjE5OC4yMDAuNTEuMTgiLA0KICAicGF0aCI6ICIiLA0KICAidGxzIjogIiIsDQogICJzbmkiOiAiIg0KfQ==,198.200.51.18,美国加利福尼亚圣何塞
vmess://ew0KICAidiI6ICIyIiwNCiAgInBzIjogIkBTU1JTVUItVjUyLeS7mOi0ueaOqOiNkDpzdW8ueXQvc3Nyc3ViIiwNCiAgImFkZCI6ICIxMTIuMzMuMzIuMTM2IiwNCiAgInBvcnQiOiAiMTAwMDMiLA0KICAiaWQiOiAiNjVjYWM1NmQtNDE1NS00M2M4LWJhZTAtZjM2OGNiMjFmNzcxIiwNCiAgImFpZCI6ICIxIiwNCiAgInNjeSI6ICJhdXRvIiwNCiAgIm5ldCI6ICJ0Y3AiLA0KICAidHlwZSI6ICJub25lIiwNCiAgImhvc3QiOiAiMTEyLjMzLjMyLjEzNiIsDQogICJwYXRoIjogIiIsDQogICJ0bHMiOiAiIiwNCiAgInNuaSI6ICIiDQp9,114.43.115.38,中国台湾新北 中華電信
vmess://ew0KICAidiI6ICIyIiwNCiAgInBzIjogIkBTU1JTVUItVjUzLeS7mOi0ueaOqOiNkDpzdW8ueXQvc3Nyc3ViIiwNCiAgImFkZCI6ICJzaGNuMi0wNmIuaXBsYzE4OC5jb20iLA0KICAicG9ydCI6ICIxMDAwNCIsDQogICJpZCI6ICI2NWNhYzU2ZC00MTU1LTQzYzgtYmFlMC1mMzY4Y2IyMWY3NzEiLA0KICAiYWlkIjogIjEiLA0KICAic2N5IjogImF1dG8iLA0KICAibmV0IjogInRjcCIsDQogICJ0eXBlIjogIm5vbmUiLA0KICAiaG9zdCI6ICJzaGNuMi0wNmIuaXBsYzE4OC5jb20iLA0KICAicGF0aCI6ICIiLA0KICAidGxzIjogIiIsDQogICJzbmkiOiAiIg0KfQ==,3.67.104.121,德国法兰克福 亚马逊云
vmess://ew0KICAidiI6ICIyIiwNCiAgInBzIjogImh0dHBzOi8vZ2l0aHViLmNvbS9BbHZpbjk5OTkvbmV3LXBhYy93aWtpIOS/hOe9l+aWr2czIiwNCiAgImFkZCI6ICIxOTQuMTU2LjEyMC41MiIsDQogICJwb3J0IjogIjQxMDAyIiwNCiAgImlkIjogImViYjkzZTg0LTViYjctMTFlYy04YmM2LTZhNWM2ZTA1NGU0ZCIsDQogICJhaWQiOiAiMCIsDQogICJuZXQiOiAidGNwIiwNCiAgInR5cGUiOiAibm9uZSIsDQogICJob3N0IjogIiIsDQogICJwYXRoIjogIiIsDQogICJ0bHMiOiAiIiwNCiAgInNuaSI6ICIiDQp9,194.156.120.52,俄罗斯新西伯利亚
```

注意：本程序虽可跨平台，但因博主能力有限，无法在更多系统上去尝试和改进，望谅解！

-------

如有可用节点增加，请推荐给博主吧：xhunmon@gmail.com
