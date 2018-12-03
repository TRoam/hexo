---
title: 让你的Vim支持ES6和React
tags:
  - Vim
  - React
  - ES6
  - Syntastic
abbrlink: 26f2ab8a
date: 2016-09-30 22:04:27
---

开始进入到了全民ES6的时代了，React 也越来越火，作为码农神器的Vim怎么能掉队呢？

自从开始使用 ES6 和 React 以来，vim的高亮和语法检查就不听话了，很多ES6的新特性都不认识了，怎么办呢？

## JSX 语法高亮

作为码农神器的vim以及其社区总是不甘落后的，我们可以使用 [mxw的JSX语法高亮插件](https://github.com/mxw/vim-jsx):

- 安装插件（Vundle）
打开 `.vimrc` 文件，在插件区域添加以下代码
```vimrc
Plugin 'mxw/vim-jsx'
```
  保存以后，运行:
```bash
$ vim +PluginInstall
```
<!-- more -->

- 配置

  如果你也需要在 `.js` 文件中添加 `.jsx`， 可以在 `.vimrc` 中加入以下配置：

  ```vimrc
let g:jsx_ext_required = 0 
```

## 语法检查

我使用的是 [Syntastic](https://github.com/scrooloose/syntastic) 插件作来为我做语法检查，作者在15年就做了更新了。

> **Update 3/30/15: I've added instructions on using ESLint instead of the old wrapper package**

- 安装 `eslint` 和 `babel-eslint`
```bash
$ npm install -g eslint babel-eslint
```
  `babel-eslint` 是为支持ES6的。

- 安装[eslint-plugin-react](https://github.com/yannickcr/eslint-plugin-react)
专门为支持React语法的插件
```bash
$ npm install eslint-plugin-react
```

* 创建配置文件
安装好了插件和支持以后，需要创建一个全局的配置文件，告诉eslint检查语法的规则,创建`~/.eslintrc`文件：
```bash
$ touch ~/.eslintrc
```
  添加配置
  ```json
{
    "parser": "babel-eslint",
    "env": {
        "browser": true,
        "node": true
    },
    "settings": {
        "ecmascript": 6,
        "jsx": true
    },
    "plugins": [
        "react"
    ],
    "rules": {
        "strict": 0,
        "quotes": 0,
        "no-unused-vars": 0,
        "camelcase": 0,
        "no-underscore-dangle": 0
    }
}
```

* 告诉vim和syntastic，需要使用eslint来做jsx的语法检查,在`.vimrc`文件中：

  ```
let g:syntastic_javascript_checkers = ['eslint']
```

可以达到预想效果了吧，又可以安心码代码而不用被一推错误烦恼了！

> 任何建议或者问题，请留言！