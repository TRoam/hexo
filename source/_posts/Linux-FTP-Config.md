---
title: Linux(centos) FTP 服务配置
date: 2018-12-01 10:55:59
tags:
- Linux
- FTP
---

最近需要把服务器从腾讯云，迁移到了阿里云（主要是阿里云11月的两折优惠啦），重新折腾了一下部署方式，启用服务器的FTP功能，做一个小记录。
Linux上最著名的FTP要数vsftpd了，小巧轻快，简单易用。

## 准备工作

### 安装vsftpd
```shell
which vsftpd
# /usr/bin/which: no vsftpd in (/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/root/bin)
```

如上表示并没有找到任何vsftpd的，那么就运行一下命令安装~

```shell
yum install vsftpd
```
<!-- more -->

### 设置开机启动服务

```shell
systemctl enable vsftpd.service
```

### 启动等相关命令

```shell
service vsftpd start

停止vsftpd:  service vsftpd stop

重启vsftpd:  service vsftpd restart
```

安装完后，有/etc/vsftpd/vsftpd.conf 文件，用来配置，还有新建了一个ftp用户和ftp的组，指向home目录为/var/ftp,默认是nologin（不能登录系统）

可以用下面命令查看用户

```
cat /etc/passwd
```

## 其他配置

### 安装客户端组件

```shell
yum -y install ftp
```

登录本地
```shell
ftp localhost
```
输入用户名，密码都可以，这里是运行匿名的，登录成功就表示FTP服务可以用了。

{% asset_img ftp_log.png %}

### 配置防火墙

以上步骤之后，说明ftp服务器可以用了，但是，外网还无法访问，这就是需要配置防火墙了。

FTP是`21`端口，系统并没有默认开启，打开并修改iptables配置文件

```
vi /etc/sysconfig/iptables
```

添加这行代码：
```
-A RH-Firewall-1-INPUT -m state --state NEW -m tcp -p tcp --dport 21 -j ACCEPT
```

然后重启iptables，再保存设置

```
service iptables restart
service iptables save
```
> 一定要先重启再保存，具体原因请参照上一篇博文

### 配置FTP

打开FTP配置文件
```
vi /etc/vsftpd/vsftpd.conf
```

#### 取消匿名登录 

把第一行的 `anonymous_enable=YES` 改为 `NO`。
修改随后三行

```
chroot_list_enable=YES
# (default follows)
chroot_list_file=/etc/vsftpd/chroot_list
```

再重启服务
```
service vsftpd restart
```

### 增加用户`ftpuser`，指向目录特定目录`/home/ftp`,禁止登录SSH权限

```
useradd -d /home/ftp -g ftp -s /sbin/nologin ftpuser
```

设置口令 `passwd ftpuser`,编辑 `chroot_list`

```
vi /etc/vsftpd/chroot_list
```

每个用户一行，如
```
roam
```

推荐使用centos的官方脚本管理： http://wiki.centos.org/HowTos/Chroot_Vsftpd_with_non-system_users

### 修改selinux

```
setsebool -P allow_ftpd_full_access 1   

setsebool -P ftp_home_dir off 1

service vsftpd restart
```

### 开启passive模式

默认是开启的，但是要指定一个端口范围，打开vsftpd.conf文件，在后面加上

```
pasv_min_port=30000   
pasv_max_port=30999 
```

### tips

提示错误： 

```
500 OOPS: vsftpd: refusing to run with writable root inside chroot()
```

解决方法： 

在配置文件中加入： 

allow_writeable_chroot=YES