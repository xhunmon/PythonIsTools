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

## 2021-10-08检测可用测试节点：
```shell
#,194.36.178.185,欧洲
vmess://eyJhZGQiOiIxOTQuMzYuMTc4LjE4NSIsImFpZCI6IjAiLCJob3N0IjoiIiwiaWQiOiI5MDU5YzJiMy01NGI2LTRlMTgtYzc4OS04NjA0ODY2MTUwN2IiLCJuZXQiOiJ0Y3AiLCJwYXRoIjoiIiwicG9ydCI6NTM2NjEsInBzIjoiU1NSVE9PTC5DT00iLCJ0bHMiOiJub25lIiwidHlwZSI6Im5vbmUiLCJ2IjoiMiJ9
#,45.140.88.192,美国加利福尼亚洛杉矶
vmess://eyJhZGQiOiI0NS4xNDAuODguMTkyIiwiYWlkIjoiMCIsImhvc3QiOiIiLCJpZCI6IjkxOTRiYTkxLWZlOGQtNDU1Ny1lN2I5LTJkYWQ4MTNlODk5YiIsIm5ldCI6InRjcCIsInBhdGgiOiIiLCJwb3J0IjoxNjM4OSwicHMiOiJTU1JUT09MLkNPTSIsInRscyI6Im5vbmUiLCJ0eXBlIjoibm9uZSIsInYiOiIyIn0=
#,89.238.130.228,英国英格兰曼彻斯特
ss://YWVzLTI1Ni1nY206c3V1Y1NlVkxtdDZQUUtBUDc3TnRHdzl4@89.238.130.227:49339#github.com/freefq%20-%20%E8%8B%B1%E5%9B%BD%E6%9B%BC%E5%BD%BB%E6%96%AF%E7%89%B9M247%E7%BD%91%E7%BB%9C%201
#,193.118.60.171,英国英格兰伦敦
ss://YWVzLTI1Ni1nY206UENubkg2U1FTbmZvUzI3@193.118.60.171:8091#github.com/freefq%20-%20%E8%8B%B1%E5%9B%BD%20%202
#,66.115.177.137,美国乔治亚亚特兰大
ss://YWVzLTI1Ni1nY206c3V1Y1NlVkxtdDZQUUtBUDc3TnRHdzl4@66.115.177.136:49339#github.com/freefq%20-%20%E7%BE%8E%E5%9B%BD%20%204
#,213.59.118.168,美国加利福尼亚洛杉矶
trojan://683ec608-5af9-4f91-bd5b-ce493307fe56@t2.ssrsub.com:8443#github.com/freefq%20-%20%E4%BF%84%E7%BD%97%E6%96%AF%20%205
```

> 如上面不可用，更多请留意：[db/_db-checked.txt](./db/_db-checked.txt)

注意：本程序虽可跨平台，但因博主能力有限，无法在更多系统上去尝试和改进，望谅解！

-------

如有可用节点增加，请推荐给博主吧：xhunmon@gmail.com
