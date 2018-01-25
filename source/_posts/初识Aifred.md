---
title: 初识Aifred
date: 2016-03-25 16:11:20
tags:
---

第一次知道AIfred，就被它强大的能力深深的吸引了！

### 小TIPs
1. 安装（不说了去 Google 吧）

2. 基础快捷键：option+space

3. 打开应用程序：Alfred 几乎是一切程序的入口，你再也不需要找妈妈要开始菜单了。用快捷键呼出Alfred，输入任何一款应用程序的中文或英文名称，即可快速定位程序，回车打开。

4. 简单查找文件：用快捷键呼出Alfred，键入空格，输入你要查找文件名，即可定位文件，回车打开，command+回车打开文件所在文件夹。

5. 复杂操作文件：通过find、open、in等关键词搜索文件。find是定位文件，open是定位并打开文件，in是在文件中进行全文检索，三种检索方式基本上可以找到任何你想找的文件。

6. 直接当做计算器使用。

7. 操作Shell：输入>即可直接运行shell命令。比如>cat *.py | grep print，可以直接打开终端并查找当前py文件中包含 print 的语句。

8. 输入iTunes，会出现一个 iTunes mini play，打开可以通过 Alfred 控制音乐播放。用快捷键也能完成这个功能：shift+option+command+p

9. 输入email，后面跟邮件地址，可以直接打开写邮件的界面

10. 定义文字片段，在 Alfred 的设置-Features 选中Clipboard，在Snippets里定义自己常用的文字片段，比如代码、地址等等等，之后以option+command+c 呼出界面，输入文字片段的关键字回车即可。

11. 在option+command+c 呼出的界面里还包括剪贴板历史，输入关键字自动匹配。

12. 简单搜索：直接输入你要查询的内容，回车即可打开默认浏览器进行搜索。

13. 自定义搜索，这个稍微复杂些，打开设置窗口，点击Features-Custom Search，在右侧栏添加自定义搜索。举几个例子帮助大家理解下规则：
* 搜索iOS App：
  ```
  Search URL：itunes://ax.search.itunes.apple.com/WebObjects/MZSearch.woa/wa/search?term={query}Title：iOS App
  Keyword：ios
  ```
* C搜索MacApp：  
  ```
  Search URL：macappstore://ax.search.itunes.apple.com/WebObjects/MZSearch.woa/wa/search?q={query}  Title：MacApp  
  Keyword：mac 
  ```
  设置完之后，呼出Alfred，输入mac dash或 ios 多看，看看什么效果（3）翻译：Search URL：`http://translate.google.cn/#auto/zh-CN/{query}`Title：英译中Keyword：en

  设置完之后，呼出Alfred，输入en awesome，看看什么效果

  大家可以据此自定义各种快捷查询、翻译、打开特定网页等功能。

### 编写自己的插件

Alfred2的推出伴随的是成熟的workflow插件机制，这部分内容就更加复杂一些，这次就不做详细介绍了,因为我也没有！！！
