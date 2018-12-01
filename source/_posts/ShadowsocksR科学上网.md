---
title: ShadowsocksR科学上网
date: 2018-11-17 10:54:31
tags:
- shadowsocks
- software
---

> 此文仅仅用于技术交流，科学的进行技术交流所用！！！

之前一直使用国外的供应商的VPS，速度已经稳定率都非常的让人担忧。最近发现阿里爸爸提供了海外的ECS，经过测试之后，发现稳定性非常高，延迟维持在50ms以内。正好赶上双十一活动，毫不犹豫的入手了。
想着再次搭建自己SS VPN，便于学习科学技术，发现了以为大神的纯一键化脚本，简单好用，于是记录并且分享一下~~

> 大神教程地址： https://doub.io/ss-jc42/ 

<!-- more -->

简单的说说步骤，想要详细解释清移步原文：

### 安装Server 

```
wget -N --no-check-certificate https://raw.githubusercontent.com/ToyoDAdoubi/doubi/master/ssr.sh && chmod +x ssr.sh && bash ssr.sh
```

然后一路按照自己的习惯往下走就行啦~

### 服务端安装

以下网站，罗列了各种平台的版本与方法

> https://ssr.tools/175

### 配置防火墙

脚本会帮忙配置相关的防火墙，但是想要详细的了解，可以参考我这篇文章。

> [Linux Iptables 防火墙](//2018/11/24/Linux防火墙小计/)

### 阿里云安全组配置

需要登录服务器控制台，在安全组中，添加相应的端口规则，这个可以详细参考官方文档，以下是简要步骤。

{% asset_img WX20181201.png %}

{% asset_img WX20181202.png %}

然后就可以开心的学习了！