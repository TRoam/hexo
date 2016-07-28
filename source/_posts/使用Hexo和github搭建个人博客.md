---
title: 使用Hexo和github搭建个人博客
date: 2016-03-25 13:20:42
tags:
---

> 这篇文章详细描述了，如何使用hexo搭建个人静态博客。

{% asset_img 1.png %}
<br />


## 前言
<br />
我以前的个人博客，是使用 [jekyll](https://jekyllrb.com/) 搭建的，jekyll 是使用ruby开发的，很多的语法和使用习惯都有深深的ruby风格，按理说，作为一个rubyer，应该会喜欢才对呀，我为何要从Jekyll转到[hexo](https://hexo.io/)呢?

> 关于如何使用 jekyll，我推荐阮老师的这篇文章-[使用jekyll和github page 搭建无限量博客](http://www.ruanyifeng.com/blog/2012/08/blogging_with_jekyll.html)

我想主要是这几点吧：

1. Hexo是基于nodejs实现的，就我目前而已，接触JavaScript是比较多一些，也觉得js本地开发方便一些。
2. Hexo是本地编译和`render()`的，拥有本地的调试服务器，不用等到server端，就可以预览自己的博文，而这一点，jekyll是做不到的。
3. Hexo对于分页和文章摘要更加友好，也更加轻量级。
4. Hexo的生态和社区要稍微友好一些，至少漂亮主题是特别的多（纯粹个人感觉）。
5. 搭建静态博客系统，hexo非常的轻便简洁，并且拥有很多的插件和友好的文档。
5. 当然咯，很重要一点，jekyll所拥有的功能，hexo基本都拥有，包括都支持Markdown。

<!-- more -->

## 安装准备

- [Git](https://git-scm.com/)
- [NodeJs](http://nodejs.org/)


> 如果你已经安装了 Nodejs 和 git 请跳过此项

### 安装Node
cURL:

```bash
$ curl https://raw.github.com/creationix/nvm/master/install.sh | sh
```

Wget:

```bash
$ wget -qO- https://raw.github.com/creationix/nvm/master/install.sh | sh
```

安装完成后，重启终端并执行下列命令即可安装 Node.js

```bash
$ nvm install stable
```

或者，也可以下载[安装程序](https://nodejs.org/en/)来安装。

### 安装Git

- Windows: [下载双击安装](https://git-scm.com/download/win)
- Mac: 使用[Homebrew](http://mxcl.github.com/homebrew/)安装。
```bash
$ brew install git
```
- Linux (Ubuntu, Debian): `sudo apt-get install git-core`
- Linux (Fedora, Red Hat, CentOS): `sudo yum install git-core`


## 安装Hexo


所有必备的应用程序安装完成后，即可使用 npm 安装 Hexo。

```bash
$ npm install -g hexo-cli
```

## 创建博客文件夹

在你喜欢的位置,创建你本地博客的文件夹：

```bash
$ mkdir blog && cd $_
```

## 初始化Hexo

在你博客文件夹目录下：

```bash
$ hexo init
```

> 详细初始化以及相关教程，请参考[官方文档](https://hexo.io/docs/configuration.html)

初始化完成后，安装依赖：

```bash
$ npm install
```

## 新建博文

```bash
$ hexo new hello-world
```

> 更多操作，请前往[官网](https://hexo.io/docs/writing.html)

## 本地预览

```bash
$ hexo generate //编译文章
$ hexo server   // 本地服务器
```

可以使用 `hexo g` 代替 `hexo generate`， 使用 `hexo s` 代替 `hexo server`. 如果你想hexo监听你的文件内容修改，可以加上 `watch`

```bash
$ hexo g --watch
```

## 将博客部署到Github Pages

Github提供了免费的静态文件服务，用于展示项目说明或者用于个人静态博客，官网在[这儿](https://pages.github.com/)。

### 注册账号

首先，你得有一个github账号，具体如何注册，这里就不详述了，提供注册[传送门](https://github.com/join)。

### 创建一个仓库

{% asset_img create.png %}
<br />
取名一定要和符合这个格式。[你的账号名].github.io，如图：

{% asset_img name.png %}
<br />

建好就行啦。

### 本地部署配置

根目录下 `_config.yml` 文件，最后一行（如果没做修改的话），添加部署信息：

```yml
# Deployment
## Docs: https://hexo.io/docs/deployment.html
deploy:
  type: git
  repository: https://github.com/TRoam/TRoam.github.io.git
  branch: master
```

### 部署到远程

安装git部署依赖

```bash
npm install hexo-deployer-git --save
```

安装完成以后，重新部署

```bash
$ hexo g
$ hexo d
```

  > 等待upload完成，就可以去远程看看啦，地址一般为： `username.github.io`
当然咯，先要确保你本地和你远程github已经连通，具体配置请参考[github官网](https://help.github.com/articles/set-up-git/).

### 添加个性化域名

1. 注册一个域名，可以选择去[Name.com](https://www.name.com/), 或者[中国万网](https://wanwang.aliyun.com/)
2. 有了域名以后，添加域名DNS解析，解析成`CNAME`类型，保存等待15分钟左右，参考如下：
{% asset_img cname.png %}
<br />
3. 回到本地博客文件夹,进入 `source/`文件夹，创建文件CNAME，并将你的域名直接写入CNAME中。
```bash
$ cd source
$ touch CNAME
```
4. 重新部署：
```bash
$ hexo clean // 有时候，修改一些比如主题，配置等文件，需要先clean原有build
$ hexo g
$ hexo d
```

好了，可以去你的自定义域名看看效果咯。

## 个性化主题

Hexo 官网提供了大量社区开发的主题，可以直接安装，也可以自己参照文件编写，主要运用 JS HTML CSS 完成，这里就不详述了。


## 常见问题

### 内容不更新

先clean，再部署

```
$ hexo clean
```

### 部署到远程没反应

由于国内某些围墙的设置，`https`可能没法访问，所以，需要将 `_config.yml` 中deploy地址，改为 `http` 并使用 `ssh` 访问。

好了，目前就这么多了，有什么遗漏或者不对，请留言。
