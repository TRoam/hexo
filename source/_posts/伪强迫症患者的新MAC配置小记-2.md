---
title: 伪强迫症患者的新MAC配置小记-开发环境篇
date: 2017-12-20 09:14:33
tags:
- 编辑器
- Mac
- 环境
---

经过前排一篇的安装和设置之后，感觉笔记本在手上顺手多了，我可以打开电脑，打上一直兴奋剂，music up，就可以美美的开始工作啦！！！

等等，工作？！ 哇，原始的terminal，糟糕的界面，各种缺失。 作为一个程序员，为了赏心悦目的开发环境，又需要做些什么呢？

## 必备工具安装


### Xcode command line tools 

既然是在mac里，XCode是必不可少的啦。去 Mac App Store 下载最新版的 Xcode，然后再运行下面的命令！

```
xcode-select --install
```

### Homebrew

方便的安装和管理我们需要的各种软件和工具，安装mac的包管理工具 `Homebrew`.官方称之为The missing package manager for OS X

```
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```

具体情况请参见官网。

有了 brew 以后，要下载工具，比如 MySQL、Gradle、Maven、Node.js 等工具，就不需要去网上下载了，只要一行命令就能搞定:

```
brew install mysql gradle maven node
```

### Homebrew Cask

brew-cask 允许你使用命令行安装 OS X 应用。比如你可以这样安装 Chrome：brew cask install google-chrome。还有 Evernote、Skype、Sublime Text、VirtualBox 等都可以用 brew-cask 安装。

brew-cask 是社区驱动的，如果你发现 brew-cask 上的应用不是最新版本，或者缺少你某个应用，你可以自己提交 pull request。

安装步骤见官网。

应用也可以通过 App Store 安装，而且有些应用只能通过 App Store 安装，比如 Xcode 等一些 Apple 的应用。App Store 没有对应的命令行工具，还需要 Apple ID。倒是更新起来很方便。

几乎所有常用的应用都可以通过 brew-cask 安装，而且是从应用的官网上下载，所以你要安装新的应用时，建议用 brew-cask 安装。如果你不知道应用在 brew-cask 中的 ID，可以先用brew cask search命令搜索。


<!--more-->

### Iterm2

然后，就是将系统自带的terminal替换成使用更加方便，特性十足的Iterm2了，丰富的主题，漂亮的界面，让我毫不犹豫的抛弃了terminal。

感谢 brew-cask，我们可以通过命令行自动安装 iTerm2 了：

```
brew cask install iterm2
```

在打开新的窗口/标签页的时候，默认情况下新窗口总是 HOME 目录，还需要我每次敲命令才能进入工作目录。如果想要这个新窗口在打开的时候就自动进入工作目录，需要如下设置：

选择Iterm菜单 > Preferences > Profiles，选择你在使用的 Profile（默认是Default），在General标签页中的Working Directory部分中选择Reuse previous seesion's directory。

至此，Terminal 应用已经出色的完成了其历史使命。后面命令行就交给 iTerm2 啦。

在 iTerm2 中双击会自动选中对应的词，三击会选中对应的整行。选中的内容会自动进入剪贴板，不需要再按⌘C复制

### Oh My Zsh

默认的 Bash 是黑白的，没有色彩。而 Oh My Zsh 可以带你进入彩色时代。Oh My Zsh 同时提供一套插件和工具，可以简化命令行操作。后面我们会看到很多介绍，你会看到我爱死这家伙了

安装：

```
$ sh -c "$(curl -fsSL https://raw.github.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"
```

在 Z shell 中，~/.zshrc是最重要的配置文件。Oh My Zsh 在安装的时候会把当前环境的$PATH写入~/.zshrc中。这并不是我期望的行为，因为使用了 brew，我们基本不再需要去定制$PATH，而 Oh My Zsh 提供的默认$PATH值$HOME/bin:/usr/local/bin:$PATH是非常合适的一个值，它把$HOME/bin加入了$PATH，可以让我们把自己用的脚本放到$HOME/bin下。

所以建议把~/.zshrc重置。

```
cp ~/.oh-my-zsh/templates/zshrc.zsh-template ~/.zshrc
```

### Dash

开发过程中，少不了需要各种各样的文档等，我推荐Dash。可以使用 cask 安装。

### Vim

系统自带有vim，但是版本更不上，而且很多设置都不存在的，所以，额外再次安装新的vim。

```
brew install vim
```

然后就是设置Vim工作环境啦，这里面又是一大段内容，如何把VIM设置成多彩方便的IDE呢，可以参照我前面的文章！

### Vscode

如果用不习惯Vim，或者嫌弃终端输入太麻烦，那么我强烈推荐VScode，继承了VS studio 的一贯优势，而且有微软严谨逼格高的特点，相比于 `atom` `sublime` 来说，我觉得总体评分都要高！

```
brew cask install vscode
```

或者去官网下载啦， 对于想使用vim mode的小伙伴，可以安装vim插件，不过别忘了增加一个设置。

```
defaults write com.microsoft.VSCode ApplePressAndHoldEnabled -bool false         # For VS Code
defaults write com.microsoft.VSCodeInsiders ApplePressAndHoldEnabled -bool false # For VS Code Insider
defaults delete -g ApplePressAndHoldEnabled                                      # If necessary, reset global default
```

推荐插件的话： 

`Git histroy` `VIM` `Vscode-icon` `vetur` `git lens` `code spell checker` 等。

个人一些设置：

```
{
    "window.zoomLevel": 1,
    "editor.minimap.enabled": true,
    "editor.formatOnSave": false,
    "workbench.iconTheme": "vscode-icons",
    "vim.disableAnnoyingNeovimMessage": true,
    "editor.fontSize": 14,
    "editor.tabSize": 2,
    "emmet.includeLanguages": {
        "hbs": "html"
    },
    "explorer.autoReveal": false,
    "vim.useSystemClipboard": true,
    "sync.gist": "0fb6a85d3697c5053733a3fcc8f14c78",
    "sync.lastUpload": "2017-08-02T05:34:37.083Z",
    "sync.autoDownload": false,
    "sync.autoUpload": false,
    "sync.lastDownload": "",
    "sync.forceDownload": false,
    "sync.anonymousGist": false,
    "sync.host": "",
    "sync.pathPrefix": "",
    "sync.quietSync": false,
    "sync.askGistName": false,
    "gitlens.blame.line.enabled": false,
    "cSpell.enabledLanguageIds": [
        "c",
        "cpp",
        "csharp",
        "go",
        "handlebars",
        "javascript",
        "javascriptreact",
        "json",
        "latex",
        "markdown",
        "php",
        "plaintext",
        "python",
        "ruby",
        "text",
        "typescript",
        "typescriptreact",
        "yml"
    ],
    "cSpell.ignorePaths": [
        "**/node_modules/**",
        "**/vscode-extension/**",
        "**/.git/**",
        ".vscode",
        "typings",
        "**/tmp/**"
    ],
    "cSpell.userWords": [
        "Resque",
        "constantize",
        "downcase",
        "eval",
        "openssl",
        "printf",
        "realtime",
        "sprintf",
        "strftime",
        "tableize",
        "uuid",
        "uuids"
    ],
    "gitlens.statusBar.enabled": false,
    "window.openFilesInNewWindow": "on",
    "editor.autoIndent": true,
    "gitlens.codeLens.locations": [
        "document"
    ],
    "gitlens.advanced.messages": {
        "suppressCommitHasNoPreviousCommitWarning": false,
        "suppressCommitNotFoundWarning": false,
        "suppressFileNotUnderSourceControlWarning": false,
        "suppressGitVersionWarning": false,
        "suppressLineUncommittedWarning": false,
        "suppressNoRepositoryWarning": false,
        "suppressUpdateNotice": true,
        "suppressWelcomeNotice": false
    }
}
```

### Git 常用alias设置

git绝对是开发中用的最多的。设置一些快捷别名，很有必要。

Oh My Zsh 提供了一套系统别名（alias），来达到相同的功能。比如gst作为git status的别名。而且 Git 插件是 Oh My Zsh 默认启用的，相当于你使用了 Oh My Zsh，你就拥有了一套高效率的别名，而且还是全球通用的。是不是棒棒哒？

完整列表请参考：https://github.com/robbyrussell/oh-my-zsh/wiki/Plugin:git


## 语言相关

### rbenv 

Ruby 版本和包管理器。rbenv 就是这样一个轻量级工具，它可以通过 brew 安装。

安装：

```
brew install rbenv ruby-build
```

然后在~/.zshrc中加上rbenv插件。否则你需要手动添加eval "$(rbenv init -)"到~/zshrc或者~/.zprofile文件里。

有时候项目会依赖一些奇怪的版本号，比如ruby-2.1.0，这个时候你需要 rbenv-aliases 帮忙

```
brew install rbenv-aliases
```

替代品有 RVM、chruby。因为 RVM 不能通过 brew 安装，并且安装的时候会没有节操的修改一堆文件，所以被我早早的弃用了

### node 包管理

Node 的版本管理工具有很多，常用的会有以下几个：

* nodenv
该工具是一个类似 rbenv 的工具，命令和其完全一样，安装和配置也一样。
```
brew install nodenv
```
你需要手动添加以下配置到~/.zshrc或者~/.zprofile文件里。
```
export PATH="$HOME/.nodenv/bin:$PATH"
eval "$(nodenv init -)"
```

* nvm
该工具是一个类似 RVM 的工具，命令安装方式也基本一样，可以参考官方文档



还有一些设置，就和工作和特定语言有关了，这就不赘述了。

工欲善其事，必先利其器，经过一些小小的设置，让你的工作效率流畅了很多，何乐而不为呢，当然也不要为了工具而工具！！！

好了，这次的小记，就算结束了，以后有更多的东西，再来补充！