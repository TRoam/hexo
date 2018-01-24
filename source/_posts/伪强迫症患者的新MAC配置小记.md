---
title: 伪强迫症患者的新MAC配置小记 - 工具篇
date: 2017-12-24 17:49:25
tags:
- 编辑器
- Mac
- 环境
---

最近到手2017 Mac Book Pro， 还真有点小兴奋呢。

{% asset_img 1.png %}

经过大概两天闲暇时间的折腾，终于可以让我满意的用来工作啦，那么面对一台全新的mac，作为程序员的我，到底做了些什么呢？

## 系统设置

### 设置 Trackpad（触摸板）轻触为单击

作为一个懒人，能触摸一下解决问题的当然不愿意需要花力气去按压了。

打开`System Preferences`，点击`Trackpad`图标，勾选`Tap to click`选项，现在手指轻轻一碰触摸板，就达到鼠标单击的顺滑效果.

### 将Dock设置为自动隐藏

我喜欢更大更全面的使用到屏幕，讨厌Dock占据一定比例，使得屏幕总感觉很短。于是将Dock设置为不使用的时候隐藏，而且作为Aifred重度用户，dock使用的真的不多。

### 全键盘控制模式

Vim 的重度用户，越来越少的使用鼠标了，希望所有的东西都能通过快捷键来完成。Mac 有基本的全键盘模式，什么意思呢，借用别人的截图。

全键盘控制模式是什么？ 举一个例子，如下图所示，我正在写一个文档，此文档还没有保存，也没有文件名，如果不不小心点了关闭按钮，将会弹出一个对话框

{% asset_img 2.jpg %}

当前，`[Save]`按钮处于默认激活状态，按回车将会弹出保存对话框。但是如果我不想保存呢？ 只能通过鼠标或者触摸板来移动光标后点击`[Don't Save]`来取消保存。那我能不能通过键盘控制光标激活`[Don't Save]`按钮呢？ 答案是肯定的，做一个简单设置就好

如图，首先打开`System Preferences`，点击`Keyboard`图标，选择`Shortcuts`这个 Tab, 选中All controls
{% asset_img 3.jpg %}

现在当我再次试图关闭一个未保存的文件时，新弹出的对话框如下，有了些许变化，在[Don't Save]按钮上多了一个蓝色的外框，当你按键盘上的tab键的时候，蓝色的外框会在 3 个按钮间切换。 假设现在蓝色的外框在[Don't Save]按钮上，你按下回车，却发现系统依然进入了保存文件对话框，为什么蓝色的外框不起作用呢？那是因为蓝色的外框选中的按钮是由空格键触发的，当你按下空格键，系统就会不保存文件直接退出。 这样当你不方便使用鼠标和触摸板的时候，可以更快速的和你的 MacBook 交互。

{% asset_img 4.jpg %}

### 快捷锁定屏幕

常常需要离开电脑前面，这个时候就需要能够快速的锁定屏幕了。
打开`System Preferences`，点击`Desktop & Screen Saver`图标，选择`Screen Saver`这个 Tab，再点击`Hot Corners...`，在弹出的如下界面里面，右下角选择`Put Display to Sleep`，点击 `OK` 确定。

{% asset_img 5.jpg %}

再打开System Preferences，点击`Security & Privacy`图标，在GeneralTab 内，勾选Require password[immediately] after sleep or screen save begins。

{% asset_img 6.jpg %}

现在当你离开电脑前时，记得`一摸触摸板`或者`一甩鼠标`将光标快速的移到屏幕的右下角，MacBook 将立刻进入Screen Saver模式并且需要密码才能进入桌面。

## 安装日常软件

有那么一些工具，让我换了电脑以后，及其的怀念，离开了就无法工作的感觉！

### 万能查找文件和应用程序的 – Alfred

Mac 自带有Spotlight， 但是Alfred要比自带的强大太多太多，可以直接下载免费版安装使用，Alfred 另外还提供了更强大的工作流(Workflows)和剪切板(Clipboard)管理等高级功能，需要购买 Powerpack。对于日常的操作，免费版已经足够使用了,可以直接google搜索下载。

因为 Alfred 可以完全取代 Spotlight，下面先删除 Spotlight 占用的快捷键command + 空格，以供 Alfred 将来使用

打开`System Preferences`，选择`Keyboard`，切换到`Shortcuts`这个 Tab 下，点击 Spotlight，取消对应的 2 个快捷键设置。

{% asset_img 7.jpg %}

打开 Alfred，在菜单栏点击 Alfred 图标，打开Preferences...

如下图所示，设置 Alfred 的快捷键为`command + 空格`

{% asset_img 8.jpg %}

这样就可以开启你的无限可能了！

### 来一支兴奋剂 -- amphetamine

常常遇到需要做演示或者开会的时候，屏幕就自动休眠了，为了避免这种尴尬，之前一直用的是 `Caffeine`， 最近发现一款比 `Caffeine` 强大一些的工具 `amphetamine`，用了以后，让我非常满意！ 一个是咖啡因 一个是安非 于是我选择了兴奋剂！

{% asset_img 9.jpg %}

设置几个条件，或者在需要的时候，轻轻点击一下，再也不尴尬！！！

### 窗口随意变化 -- Spectacle

Spectacle是一款易用的通过键盘快捷键修改或移动窗口位置的组织工具，使用Spectacle可以快速将窗口放置于屏幕中心，逐步扩展窗口大小（至全屏），瞬间缩小窗口至原尺寸的一半大小并移至窗口上下左右角四个位置，有了他我们就可以在有限的Mac屏幕下快速调用窗口或是组织更多的窗口显示在我们的眼前，绝对提高使用效率

{% asset_img 10.png %}

### Vscode

最离开怕是编辑器了吧，之前VIM 用的比较多，知道我遇到了VScode， 真的是良心之作！

### 其他工具及软件推荐

上面那些都是爱不释手的，再推荐一些日常使用的。

* Evernote： 笔记工具，之前用过很多各种各样的，包括 OneNote WizNote 等等， 要说其中的好坏又是一个长篇大论
* 有道词典： 总是会有遇到不认识的单词或者语句吧！
* 网易云音乐： 作为程序员，音乐总是少不了的！
* chrome： 最好的浏览器，没有之一！