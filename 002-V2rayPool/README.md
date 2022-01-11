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
Config.set_v2ray_core_path('xxx/v2ray-macos-64')
```
3. 查看是否能正常启动：
```python
client.Creator().v2ray_start('xxx')
#如果需要开启全局代理
client.Creator().v2ray_start('xxx',True)
```

## 2022-1-11检测可用测试节点(注意去掉后面","开始的内容)：
```shell
ss://YWVzLTI1Ni1nY206MWY2YWNhM2NlYmQyMWE0Y2Q1YTgwNzE4ZWQxNmI3NGNAMTIwLjIzMi4yMTQuMzY6NTAwMg#%F0%9F%87%B8%F0%9F%87%ACSingapore,8.25.96.100,美国 Level3
ss://YWVzLTI1Ni1nY206Y2RCSURWNDJEQ3duZklO@139.99.62.207:8119#github.com/freefq%20-%20%E6%96%B0%E5%8A%A0%E5%9D%A1OVH%201,139.99.62.207,新加坡 OVH
ss://YWVzLTI1Ni1nY206UmV4bkJnVTdFVjVBRHhH@167.88.61.60:7002#github.com/freefq%20-%20%E7%91%9E%E5%85%B8%20%203,167.88.61.60,美国加利福尼亚圣克拉拉
ss://YWVzLTI1Ni1nY206WTZSOXBBdHZ4eHptR0M@38.143.66.71:3389#github.com/freefq%20-%20%E7%BE%8E%E5%9B%BD%E5%8D%8E%E7%9B%9B%E9%A1%BFCogent%E9%80%9A%E4%BF%A1%E5%85%AC%E5%8F%B8%204,38.143.66.71,美国华盛顿西雅图 Cogent
trojan://e6c36d58-6070-4b55-a437-146e6b53ec57@t1.ssrsub.com:8443#github.com/freefq%20-%20%E5%8A%A0%E6%8B%BF%E5%A4%A7%20%2012,142.47.89.64,加拿大安大略
ss://YWVzLTI1Ni1nY206ZTRGQ1dyZ3BramkzUVk@172.99.190.87:9101#github.com/freefq%20-%20%E7%BE%8E%E5%9B%BD%20%2013,172.99.190.87,美国乔治亚亚特兰大
ss://YWVzLTI1Ni1nY206UENubkg2U1FTbmZvUzI3@46.29.218.6:8091#github.com/freefq%20-%20%E6%8C%AA%E5%A8%81%20%2019,46.29.218.6,挪威
```

注意：本程序虽可跨平台，但因博主能力有限，只在macos系统操作过，无法在更多系统上去尝试和改进，望谅解！

-------

如有可用节点增加，请推荐给博主吧：xhunmon@gmail.com
