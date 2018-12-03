---
title: hexo进阶以及常见问题
tags:
  - hexo
abbrlink: 951e94ad
date: 2015-12-30 10:11:29
---


本文主要包括一些hexo的进阶功能，比如自定义主题，静态网页，评论，统计，RSS等等。。。

> Hexo基础知识，请浏览本博客前面的文章-[如何使用hexo搭建个人博客](/2016/03/25/%E4%BD%BF%E7%94%A8Hexo%E5%92%8Cgithub%E6%90%AD%E5%BB%BA%E4%B8%AA%E4%BA%BA%E5%8D%9A%E5%AE%A2/)。

## heox进阶

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
<!-- more -->
4. 重新部署：
```bash
$ hexo clean // 有时候，修改一些比如主题，配置等文件，需要先clean原有build
$ hexo g
$ hexo d
```

好了，可以去你的自定义域名看看效果咯。

### 主题
看着别人的博客那么漂亮，自然也会心痒痒啦。主题可以根据[官方指南](https://hexo.io/zh-cn/docs/themes.html)自己开发个性主题，当然咯，hexo社区非常活跃，已经有很多可以直接使用的漂亮主题，刷选一下，就可以不用自己动手了。

1. 选择主题
Hexo的github上收集了非常多的主题，你可以前往[这儿](https://github.com/hexojs/hexo/wiki/Themes)找到你自己喜欢的主题。
知乎上也有收集的，可以[去看看](https://www.zhihu.com/question/24422335)。

2. 安装主题
选好主题啦，就可以开始安装咯，进入你的博客目录,就以[这款](https://github.com/hustcer/hexo-theme-air)为例。
```bash
$ git clone https://github.com/hustcer/hexo-theme-air
```

3. 使用主题
安装好了以后，你会发现，在themes文件夹下，多出了一个air的目录。
打开根目录下面的 `_config.yml`文件，修改如下：
```yml
theme: air
```

4. 部署主题
为确保使用成功，需要先clean 在build。
```bash
$ hexo clean
$ hexo g
```

4. 更新主题
如何主题有了更新，这时候，就可以拉取最新修改了：
```bash
$ cd themes/air // 进入你使用的主题目录
$ git pull // 拉取代码，再重新部署
```

### 添加静态页面
有时候，希望某一些目录或者文件不被hexo解析，仅仅只要拷贝到public文件夹中。比如说，添加`readme.md` 文件或者为某些博文添加一些demo程序。
我们可以使用 `skip_render` 配置来解决，比如说，在 `source/` 文件夹下面，有一个 `readme.md` 文件，和一个 `demo` 文件夹，都不想要hexo处理，可以这么做：

1. 添加配置
进入 `_config.yml` 配置文件，添加
```yml
skip_render: 
  - readme.md
  - demo/** 
```

2. 规则
hexo按照[这个](https://en.wikipedia.org/wiki/Glob_(programming)规则匹配，简单描述几种情况：
  - 单个文件目录下所有文件： `skip_render: text/*`
  - 单个目录指定类型,比如说html文件：  `skip_render: text/*.html`
  - 单个文件目录下所有文件以及子目录： `skip_render: text/**`
  - 多种复杂情况：
```yml
skip_render:
  - text/**
  - *.html
#.....
```

## 常见问题

### 内容不更新

先clean，再部署

```
$ hexo clean
```

### 部署到远程没反应

由于国内某些围墙的设置，`https`可能没法访问，所以，需要将 `_config.yml` 中deploy地址，改为 `http` 并使用 `ssh` 访问。

> 持续更新，有什么其他情况也可以留言哦。