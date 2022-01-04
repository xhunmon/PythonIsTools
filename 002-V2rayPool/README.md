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

## 2022-1-4检测可用测试节点(注意去掉后面","开始的内容)：
```shell
vmess://ew0KICAidiI6ICIyIiwNCiAgInBzIjogIkBTU1JTVUItVjMyLeS7mOi0ueaOqOiNkDpzdW8ueXQvc3Nyc3ViIiwNCiAgImFkZCI6ICIxMzcuMTc1LjMwLjI1MSIsDQogICJwb3J0IjogIjExMSIsDQogICJpZCI6ICI3N2NkNzc1Yy0xYzBhLTExZWMtYTFhOC0wMDE2M2MxMzkzYTgiLA0KICAiYWlkIjogIjAiLA0KICAic2N5IjogImF1dG8iLA0KICAibmV0IjogInRjcCIsDQogICJ0eXBlIjogIm5vbmUiLA0KICAiaG9zdCI6ICIxMzcuMTc1LjMwLjI1MSIsDQogICJwYXRoIjogIiIsDQogICJ0bHMiOiAiIiwNCiAgInNuaSI6ICIiDQp9,137.175.30.251,美国加利福尼亚圣何塞
vmess://ew0KICAidiI6ICIyIiwNCiAgInBzIjogImh0dHBzOi8vZ2l0aHViLmNvbS9BbHZpbjk5OTkvbmV3LXBhYy93aWtpIOS/hOe9l+aWr2czIiwNCiAgImFkZCI6ICIxOTQuMTU2LjEyMC41MiIsDQogICJwb3J0IjogIjQxMDAyIiwNCiAgImlkIjogImViYjkzZTg0LTViYjctMTFlYy04YmM2LTZhNWM2ZTA1NGU0ZCIsDQogICJhaWQiOiAiMCIsDQogICJuZXQiOiAidGNwIiwNCiAgInR5cGUiOiAibm9uZSIsDQogICJob3N0IjogIiIsDQogICJwYXRoIjogIiIsDQogICJ0bHMiOiAiIiwNCiAgInNuaSI6ICIiDQp9,194.156.120.52,俄罗斯新西伯利亚
vmess://eyJ2IjoiMiIsInBzIjoi57+75aKZ5YWaZmFucWlhbmdkYW5nLmNvbV9DTl8xMiIsImFkZCI6InNoY24yLTAxLmlwbGMxODguY29tIiwicG9ydCI6IjEwMDE2IiwiaWQiOiI4OTdhMTlmMC04ZGYxLTRiYTEtYTRhOC0wNTMzMWE4MmMyYWIiLCJhaWQiOiIwIiwic2N5IjoiYXV0byIsIm5ldCI6InRjcCIsInR5cGUiOiJub25lIiwiaG9zdCI6InNoY24yLTAxLmlwbGMxODguY29tIiwicGF0aCI6Ii8iLCJ0bHMiOiIiLCJzbmkiOiIifQ==,44.242.96.255,美国俄勒冈波特兰 亚马逊云
vmess://eyJ2IjoiMiIsInBzIjoi57+75aKZ5YWaZmFucWlhbmdkYW5nLmNvbV9DTl8xNCIsImFkZCI6InNoY24yLTAxLmlwbGMxODguY29tIiwicG9ydCI6IjEwMDEyIiwiaWQiOiI4OTdhMTlmMC04ZGYxLTRiYTEtYTRhOC0wNTMzMWE4MmMyYWIiLCJhaWQiOiIwIiwic2N5IjoiYXV0byIsIm5ldCI6InRjcCIsInR5cGUiOiJub25lIiwiaG9zdCI6InVzYS1idWZmYWxvLmx2dWZ0LmNvbSIsInBhdGgiOiIvd3MiLCJ0bHMiOiIiLCJzbmkiOiIifQ==,136.175.179.25,美国加利福尼亚洛杉矶
vmess://eyJ2IjoiMiIsInBzIjoi57+75aKZ5YWaZmFucWlhbmdkYW5nLmNvbV9DTl8xNiIsImFkZCI6InNoY24yLTAxLmlwbGMxODguY29tIiwicG9ydCI6IjEwMDE0IiwiaWQiOiI4OTdhMTlmMC04ZGYxLTRiYTEtYTRhOC0wNTMzMWE4MmMyYWIiLCJhaWQiOiIwIiwic2N5IjoiYXV0byIsIm5ldCI6InRjcCIsInR5cGUiOiJub25lIiwiaG9zdCI6InY5LnNzcnN1Yi5jb20iLCJwYXRoIjoiL3NzcnN1YiIsInRscyI6IiIsInNuaSI6IiJ9,3.70.63.126,德国法兰克福 亚马逊云
vmess://eyJ2IjoiMiIsInBzIjoi57+75aKZ5YWaZmFucWlhbmdkYW5nLmNvbV9DTl8yMyIsImFkZCI6InNoY24yLTAxLmlwbGMxODguY29tIiwicG9ydCI6IjEwMDExIiwiaWQiOiI4OTdhMTlmMC04ZGYxLTRiYTEtYTRhOC0wNTMzMWE4MmMyYWIiLCJhaWQiOiIxIiwic2N5IjoiYXV0byIsIm5ldCI6InRjcCIsInR5cGUiOiJub25lIiwiaG9zdCI6IiIsInBhdGgiOiIiLCJ0bHMiOiIiLCJzbmkiOiIifQ==,103.138.75.27,中国香港
<p><font face="宋体">v2ray客户端电脑版最新版本可添加trojan及vless,114.43.135.233,中国台湾台北 中華電信
```

注意：本程序虽可跨平台，但因博主能力有限，无法在更多系统上去尝试和改进，望谅解！

-------

如有可用节点增加，请推荐给博主吧：xhunmon@gmail.com
