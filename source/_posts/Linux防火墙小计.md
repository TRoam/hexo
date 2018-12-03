---
title: Linux iptables 防火墙
tags:
  - Linux
  - iptables
  - 防火墙
abbrlink: 37a12b05
date: 2018-11-24 10:54:50
---

最近把服务器更新成了阿里云的Centos， 于是倒腾了系列防火墙的东东 ~~

Centos中默认的防火墙并不是iptables， 而是firewall，因此需要自己安装iptables服务。
<!-- more  -->
### 禁用原有的`firewall`服务

先查看`firewall`的状态

> systemctl status firewalld


如果是active的话，关闭再禁用服务

> systemctl stop firewalld
systemctl disable firewalld 

### 安装iptables

> yum install -y iptables-services

启动服务
> systemctl enable iptables
systemctl start iptables 
或者 
service iptables start

### 常用命令 

>启动指令:service iptables start  
重启指令:service iptables restart  
关闭指令:service iptables stop  
  
### 配置

>vim /etc/sysconfig/iptables  

>然后进去修改即可，修改完了怎么办？这里很多人会想到/etc/rc.d/init.d/iptables save指令，但是一旦你这么干了你刚才的修改内容就白做了。。。  
具体方法是：  
只修改/etc/sysconfig/iptables 使其生效的办法是修改好后先service iptables restart，然后才调用/etc/rc.d/init.d/iptables save，  
因为/etc/rc.d/init.d/iptables save会在iptables服务启动时重新加载，要是在重启之前直接先调用了/etc/rc.d/init.d/iptables save那么你  
的/etc/sysconfig/iptables 配置就回滚到上次启动服务的配置了，这点必须注意！！！ 

### 常见指令

假设需要开发80端口，那么在配置文件中加入此条命令：

```
-A INPUT -p tcp -m tcp --dport 80 -j ACCEPT
```

或者直接在命令行输入 

```
iptables -A INPUT -p tcp -m tcp --dport 80 -j ACCEPT
```

这条命令做了些什么呢？ 
> -A：指定链名  
-p：指定协议类型  
-d：指定目标地址  
--dport：指定目标端口（destination port 目的端口）  
--sport：指定源端口（source port 源端口）  
-j：指定动作类型  

如果需要正对某个IP单独开放某端口：

```
如果我需要对内网某机器单独开放mysql端口，应该如下配置：  
iptables -A INPUT -s 192.168.2.1 -p tcp -m tcp --dport 3306 -j ACCEPT  
iptables -A OUTPUT -d 192.168.2.1 -p tcp -m tcp --sport 3306 -j ACCEPT
```

如果针对某IP进行全端口开放无限制:
```
-A INPUT -s 192.168.2.1/32 -j ACCEPT  
-A OUTPUT -d 192.168.2.1/32 -j ACCEPT 
```

彻底禁止某IP访问： 
```
#屏蔽单个IP的命令是  
iptables -I INPUT -s 47.91.213.10 -j DROP  
#封整个段即从123.0.0.1到123.255.255.254的命令  
iptables -I INPUT -s 123.0.0.0/8 -j DROP  
#封IP段即从123.45.0.1到123.45.255.254的命令  
iptables -I INPUT -s 124.45.0.0/16 -j DROP  
#封IP段即从123.45.6.1到123.45.6.254的命令是  
iptables -I INPUT -s 123.45.6.0/24 -j DROP  
指令I是insert指令 但是该指令会insert在正确位置并不像A指令看你自己的排序位置，因此用屏蔽因为必须在一开始就要加载屏蔽IP，所以必须使用I命令加载，然后注意执行/etc/rc.d/init.d/iptables save进行保存后重启服务即可
```

### 我自己的配置实例

```
*filter
:INPUT ACCEPT [0:0]
:FORWARD ACCEPT [0:0]
:OUTPUT ACCEPT [0:0]
-A INPUT -p udp -m state --state NEW -m udp --dport 8989 -j ACCEPT
-A INPUT -p tcp -m state --state NEW -m tcp --dport 8989 -j ACCEPT
-A INPUT -m state --state RELATED,ESTABLISHED -j ACCEPT
-A INPUT -p icmp -j ACCEPT
-A INPUT -i lo -j ACCEPT
-A INPUT -s 127.0.0.1/32 -d 127.0.0.1/32 -j ACCEPT
-A INPUT -s 192.168.2.200/32 -d 192.168.2.200/32 -j ACCEPT
-A INPUT -p tcp -m tcp --dport 22 -j ACCEPT
-A INPUT -p tcp -m tcp --dport 80 -j ACCEPT
-A INPUT -p tcp -m tcp --dport 3306 -j ACCEPT
-A INPUT -p tcp -m tcp --dport 11211 -j ACCEPT
-A INPUT -p tcp -m tcp --dport 11212 -j ACCEPT
-A INPUT -p tcp -m tcp --dport 53 -j ACCEPT
-A INPUT -p udp -m udp --dport 53 -j ACCEPT
-A INPUT -p tcp -m state --state NEW -m tcp --dport 8989 -j ACCEPT
-A INPUT -p tcp -m state --state NEW -m tcp --dport 21 -j ACCEPT
-A INPUT -p tcp -m state --state NEW -m tcp --dport 30000:30999 -j ACCEPT
-A FORWARD -j REJECT --reject-with icmp-host-prohibited
-A OUTPUT -p icmp -j ACCEPT
-A OUTPUT -s 127.0.0.1/32 -d 127.0.0.1/32 -j ACCEPT
-A OUTPUT -s 192.168.2.200/32 -d 192.168.2.200/32 -j ACCEPT
-A OUTPUT -p tcp -m tcp --dport 22 -j ACCEPT
-A OUTPUT -p tcp -m tcp --sport 22 -j ACCEPT
-A OUTPUT -p tcp -m tcp --dport 80 -j ACCEPT
-A OUTPUT -p tcp -m tcp --dport 53 -j ACCEPT
-A OUTPUT -p udp -m udp --dport 53 -j ACCEPT
-A OUTPUT -p tcp -m tcp --dport 465 -j ACCEPT
-A OUTPUT -p tcp -m tcp --dport 25 -j ACCEPT
-A OUTPUT -p tcp -m tcp --dport 110 -j ACCEPT
-A OUTPUT -p tcp -m tcp --sport 80 -j ACCEPT
-A OUTPUT -p tcp -m tcp --sport 3306 -j ACCEPT
-A OUTPUT -p tcp -m tcp --sport 11211 -j ACCEPT
-A OUTPUT -p tcp -m tcp --sport 11212 -j ACCEPT
COMMIT
```