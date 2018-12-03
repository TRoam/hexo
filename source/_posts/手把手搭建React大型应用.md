---
title: 'React:手把手搭建React大型应用'
tags:
  - JavaScript
  - React
  - Webpack
  - Unit Test
  - CSS Module
  - PostCSS
  - Karma
  - chai
  - mocha
  - enzyme
  - sinon
  - React Router
  - NodeJs
  - PhantomJs
  - Font-Awesome
abbrlink: 66849a10
date: 2016-07-10 10:53:01
---

# 前言

最近正在奋力研究React中，被它的魅力深深的吸引了。 关于如何使用React和外部API搭建大型应用，看到一遍非常好的文章，于是乎翻译了一份，方便大家一起学习。

> 本文会一步一步演示如何搭建一个完整的React的项目，将要建立的项目名为：**Clone Yelp** 完整的代码在[这里](https://github.com/fullstackreact/react-yelp-clone) [试试效果吧](http://fullstackio.github.io/yelp-clone/#/?_k=h57lso)

{% asset_img app-screenshot.jpg %}

在本博文中，我们会涉及到这些内容：

- 如何从零开始搭建一个React项目
- 如何创建一个基础React组件
- 如何使用`postcss`编写模块化CSS
- 如何React编写测试
- 如何利用`React-Route`做页面跳转
- 如何和Google地图集成
- 如何创建基于Google地图的React组件
- 如何创建五星React组件

在本文中，会运用React的很多属性和模块，手把手教大家搭建完整的React应用，不论你的前端知识了解多深！ 好了，让我们系好安全带，准备起飞啦！！！

<!-- more -->

# 目录

- [环境配置](#setup)

  - [真正的一步到位](#quick-start)
  - [Babel](#babel)
  - [webpack](#webpack)
  - [React](#react)
  - [创建 app.js](#create-app)
  - [演示: Basic app.js](#demo-app)
  - [postcss](#postcss)
  - [CSS modules](#css-modules)
  - [演示: CSS Modules](#demo-css-modules)
  - [Configuring Multiple Environments](#config-m-env)
  - [Font Awesome](#font-awsome)
  - [Webpack Tip: Relative requires](#webpack-tips)


- [配置测试环境](#test-env)

  - [建立测试骨架](#test-skeleton)
  - [测试模式](#test-model)


- [路由](#routing)

  - [建立路由表](#routes)
  - [主页以及其嵌套路由](#main-page)
  - [演示: Routing to Container Content](#demo-container-router)
  - [Maps 的路由](#map-router)


- [获取位置清单](#places-list)


- [创建侧边栏](#sidebar)

  - [内联样式](#inline-css)
  - [CSS 变量](#css-variables)


- [组件的分割和设计](#components)

  - [Business Listing 组件](#list-component)
  - [Item 组件](#item-component)
  - [Rating 组件](#rating-component)


- [创建地图主页](#main-pane)

  - [创建地图标记](#markers)
  - [更新所有<mapcomponent> 子组件</mapcomponent>](#component-children)

  - [点击标记](#click-markers)
  - [为标记增加详细内容](#add-details)

  - [响应式布局](#responsive)

    - [display: flex](#flex)
    - [flex-direction](#flex-direction)
    - [order](#order)


- [结尾](#conclusion)

# <span id="setup">环境配置</span>

千里之行，始于足下。搭建开发环境以及创建项目的骨架子往往是完成整个项目最痛苦的一部分。我们将借助以下的一些工具帮助我们~

> 最终版本的配置文件：`package.json`和`webpack.config.js` 可以在[这里](github.com/fullstackreact/react-yelp-clone)找到哦！

## <span id="quick-start">真正的一步到位</span>

虽然有一打的模板可以供我们使用，但是直接运用模板往往会让我们更加的困惑，得不偿失。在本文中，让我们亲自尝试构建所有的东西吧。我相信，做完这些以后，我们对如何从零开始创建React项目会有一个更加清楚明确的认识。

> 如果你想跳过这些复杂配置，你也可以使用[yeoman generator](https://www.npmjs.com/package/generator-react-gen)工具获得完整的配置，并且直接跳到[路由](#routing)章节。

> 载入工具

> ```
$  npm install -g yo generator-react-gen
```

> 运行

> ```shell
$ yo react-gen
```

在整个开发过程中，我们将使用例如ES6，inline css modules, async module loading, test等相关知识。并且，我们使用[Webpack](https://webpack.github.io/)作为我们的构建工具。

> 为了你能够顺利的起飞，请确保你的机器以及安装了[Node.js](https://nodejs.org/)，并且已经配置好了**npm**。 如果你对ES6不是很熟悉，我推荐[阮一峰](http://www.ruanyifeng.com/home.html)老师的[入门教程](http://es6.ruanyifeng.com/#docs/intro)。 同样的，Webpack的教程可以阅读这个系列:[Webpack傻瓜式指南](https://zhuanlan.zhihu.com/p/20367175)。

以下是我们的项目目录结构：

{% asset_img tree-structure.jpg %}

我们首先创建一个新的`node`项目，打开我们的终端，创建主要目录结构。

```zsh
$ mkdir yelp && cd $_
$ mkdir -p src/{components,containers,styles,utils,views}\
  && touch webpack.config.js
```

在这个文件夹下面，我们使用`npm init`来初始化我们的`node`项目。初始化中会要求回答一些问题，填好答案完成初始化以后，会自动生成一个`package.json`的配置文件，我们可以直接修改此文件更改项目配置。

> 如何回答初始化中的这些问题其实并不重要啦，我们可以随时更改`package.json`文件滴。

> 此外，可以使用`npm init -y`命令代替`npm init`, 这样的话，所有的问题都会按照默认的答案完成初始化。

```shell
$ npm init
```

{% asset_img npm-init.jpg %}

在我们项目运行起来之前，需要添加一些必要的依赖。

## <span id="babel">Babel</span>

[Babel](https://babeljs.io/) 是一个 JavaScript 编译器，让我们可以使用下一代 JavaScript 语法编写代码，目前来说，也就是ES6啦。

同时，也需要安装一些babel的其他插件，例如es-2015deng:

```shell
$ npm install --save-dev babel-core babel-preset-es2015 babel-preset-react babel-preset-react-hmre babel-preset-stage-0
```

{% asset_img npm-install-babel,jpg %}

我们需要添加一些配置，辅助babel更好的解析的我们的代码。非常简单，只要在根目录下新建一个`.babelrc`文件并添加一些代码就可以啦。

```json
 {
    "presets": ["es2015", "stage-0", "react"]
  }
```

Babel给我们提供了一个`env`的属性，以便于我们可以针对_不同的运行环境_添加不同的配置。 在此，我们将只在开发环境下，引入`babel-hmre`插件（我们在生产环境不需要热加载功能）。

```json
{
  "presets": ["es2015", "stage-0", "react"],
  "env": {
    "development": {
      "presets": ["react-hmre"]
    }
  }
}
```

让我们也给生产和测试环境也添加上预留上一些配置吧，方便以后添加:

```json
{
  "presets": ["es2015", "stage-0", "react"],
  "env": {
    "development": {
      "presets": ["react-hmre"]
    },
    "production": {
      "presets": []
    },
    "test": {
      "presets": []
    }
  }
}
```

## <span id="webpack">webpack</span>

原生的Webpack的配置和使用是相当的复杂的。不过不用担心，在这儿，给大家介绍一款配置webpack的神器[hjs-webpack](https://github.com/HenrikJoreteg/hjs-webpack)，它可以帮助我们省去很多的工作。

hjs-webpack 会帮我们把常用的生产和开发环境下需要的配置(loaders)工作做好，包括hot reloading, minification, ES6 templates 等。

让我们安装 _webpack_ 和 _hjs-webpack_ 吧。

```shell
$ npm install --save-dev hjs-webpack webpack
```

如果不添加一些插件和设置，webpack用处就比较小啦。让我们开始添加我们项目需要的插件吧，诸如babel-loader, css/styles等。 当然，也包括URL以及file loader（font-loading 以及内置在hjs-webpack了）。

```json
$ npm install --save-dev babel-loader css-loader style-loader postcss-loader url-loader file-loader
```

{% asset_img npm-loaders.jpg %}

## <span id="react">React</span>

既然是React应用，当然要引入React和它的一些依赖啦。和前面的那些不同，React以及相关的一些依赖仅仅是为了开发才需要的，而是我们的APP的组成部分。

```shell
$ npm install --save react react-dom
```

我们也需要使用React-Router来处理我们项目的路由和跳转。

```shell
$ npm install --save react-router
```

下载和保存依赖包的缩写命令：

```shell
$ npm i -S [dependencies]
```

那么，前面的命令可以写成这样:

```shell
$ npm i -S react react-dom
```

下载和保存用于开发的依赖包，只需要把`-S`替换成`-D`，比如:

```shell
$ npm i -D [dependencies]
```

{% asset_img npm-react.jpg %}

## <span id="create-app">创建 app.js</span>

好了，我们可以开始建立我们的项目入口文件啦，就如前面webpack中配置的一样,并且建立一个顶层的容器，我们项目所有的流程以及和服务器的交互都会建立在此基础上。

首先，我们在 `app.js` 中简创建一个简单的React App。 新建 `src/app.js`

```shell
$ touch src/app.js
```

在这个文件里，让我们建立一个简单的React容器，在这个容器中仅仅包含一个输出一些文字的组件。首先，利用webpack引入一些必要的库：

```javascript
import React from 'react'
import ReactDOM from 'react-dom'

const App = React.createClass({
  render: function() {
    return (<div>Text text text</div>);
  }
});
```

## <span id="demo-app">演示: Basic app.js</span>

<div class="demo">
  <h2>Demo</h2>
  <p>Text Text Text</p>
</div>

`<App />`组件已经添加好了，为了让它能够显示在页面上，我们需要让它和页面的某一个Dom节点关联起来，那么，在哪里呢？

`hjs-webpack`内置了一个简单的`index.html`文件，如果不做特别的配置的话（在配置文件中修改`html`属性, 这个文件会被自动加载。`hjs-webpack`内置的这个文件完全满足我们的需要，所以我们不需要自己额外的配置一个HTML 文件。为了满足单页面应用的需求（简称SPA），在这个HTML 中，只包含了一个id为`root`的`div`节点。

这样的话，我们可以把`<App />`组件和这个HTML中的Div关联起来啦，修改`src/app.js`文件：

```javascript
import React from 'react'
import ReactDOM from 'react-dom'

const App = React.createClass({
  render: function() {
    return (<div>Text text text</div>)
  }
});

const mountNode = document.querySelector('#root');
ReactDOM.render(<App />, mountNode);
```

`src/app.js`已经写好了，让我们准备跑起来试试吧。 `hjs-webpack`自带了一个用于开发的node服务器，我们只需要运行一下命令就可以启动啦！

```shell
$ NODE_ENV=development ./node_modules/.bin/hjs-dev-server
```

设置node的环境变量`NODE_ENV` 是个非常好的习惯，就像我们这边做的一样。

{% asset_img dev-server.jpg %}

服务器启动成功以后，会告诉我们它所监听的地址，我们只要通过这个URL就能访问我们的APP啦。打开我们的浏览器（我们会使用[Google Chrome](https://www.google.com/chrome/)）并且访问`http://localhost:3000`

{% asset_img browser-first-look.jpg %}
<br />
虽然看起来不怎么样，至少在我们的努力下，我们的项目算是初步跑起来了啦！


> 使用`Ctrl+C`来停止服务器

要启动我们的服务器，需要记住这一长串的命令，实在是不容易。我们可以在`package.json`中添加一些配置，让启动过程变得简单好记！

`package.json`允许我们在`scripts`属性中，添加一些自定义的脚步，我们把启动服务器的命令添加到这里去吧。

```json
 {
  "name": "yelp",
  "version": "1.0.0",
  "description": "",
  "scripts": {
    "start": "NODE_ENV=development ./node_modules/.bin/hjs-dev-server",
    "test": "echo \"Error: no test specified\" && exit 1"
  },
  /* ... */
}
```

做了以上的一些配置，现在我们只需要用`npm run start`就可以启动我们的服务器啦。

针对于`start`和`test`脚步，`package.json`做了一些特殊的定义，所以，我们可以直接省略`run`关键字。

比如：

```shell
$ npm start
```

所有的其他脚步命令都不能省略`run`哦！

## <span id="postcss">postcss</span>

这么难看的页面，肯定没人喜欢的，为了让我们的页面变得更加的漂亮，我们添加[postcss](http://postcss.org/)和CSS modules 来帮助我们增加和管理样式！

PostCSS是CSS变成JavaScript的数据，使它变成可操作。PostCSS是基于JavaScript插件，然后执行代码操作。PostCSS自身并不会改变CSS，它只是一种插件，为执行任何的转变铺平道路。PostCSS可以作为预处理器或者后处理器，类似于[lesscss](http://lesscss.org/)和[sass](http://sass-lang.com/)一样，当然，它的功能更加强大，详情的用法有机会我会另起博文介绍。

只要我们安装了[autoprefixer](https://github.com/postcss/autoprefixer)，`hjs-webpack`就会加载需要的loader，不需要我们在webpack中做任何额外的配置。

```shell
$ npm install --save-dev autoprefixer
```

我们也会添加两个PostCSS的插件，来帮助我们Postcss管理和维护项目的CSS。一个是[precss](https://jonathantneal.github.io/precss/) [package](https://github.com/jonathantneal/precss), 用来帮助做一些css的预处理。另外一个是[cssnano](http://cssnano.co/),帮助处理用于生产环境的css的压缩等。

```shell
$ npm i -D precss cssnano
```

{% asset_img npm-postcss-processors.jpg %}

hjs-webpack 会自动给 autoprefixer 添加需要的配置，但是对于这两个插件并没有做任何的配置支持。所以，我们需要手动的添加一些配置来支持这个插件的运行。

很关键的，hjs-webpack帮我们创建好了一个webpack的配置对象。我们只需要扩展这个对象就能添加我们多需要的配置。

在webpack的配置中，`postcss-loader` 对应于一个叫做`postcss`的属性。所以，我们只需要在属性内容的前面和后面增加配置，就如以下代码所显示的一样：

```javascript
// ...
var config = getConfig({
  // ...
})

config.postcss = [].concat([
  require('precss')({}),
  require('autoprefixer')({}),
  require('cssnano')({})
])
```

> 每一个postcss的插件都会输出一个返回postcss processor的方法，因此我们有机会改变这些配置

> 虽然在本项目中，我们没有在方法中添加任何的配置。

> 以下是这些插件的文档：

> - [precss](https://github.com/jonathantneal/precss)
> - [autoprefixer](https://github.com/postcss/autoprefixer)
> - [cssnano](http://cssnano.co/)

## <span id="css-modules">CSS modules</span>

[CSS modules](http://glenmaddern.com/articles/css-modules)可以使我们为不同的页面部分定义不同的生效范围CSS，从而避免了全局CSS所带来的混淆和难以维护。

在最终生成的CSS中，css module会为每一条css添加于其作用域和生命周期相关的名字，让我们来看看实际的代码。

对于某一个实例，假设我们有一个css文件，并且包含一个`container`的类：

```css
.container {
  border: 1px solid red;
}
```

如果没有CSS modules，类名`.container`将会是一个非常普通的名字，它将会被应用到所有带有`container`类的Dom对象上。这样的话，可能会带来一些不必要的冲突，以及在项目后期会变得非常难以维护和扩展。CSS modules帮我们解决了这个问题！

为了在`<App />`组件中使用`.container`类，我们需要import文件和内容。

```javascript
import React from 'react'
import ReactDOM from 'react-dom'

import styles from './styles.module.css'

const App = React.createClass({
  // ...
});
```

以上的样式会产生一个以css类名作为Key，以插件生成的一个特殊的css的类名作为Value的对象： 比如：

```
"container" = "src-App-module__container__2vYsV"
```

把生成好的特殊类名加入到组建的`className`里：

```javascript
// ...
import styles from './styles.module.css'

const App = React.createClass({
  render: function() {
    return (
      <div className={styles['container']}>
        Text text text
      </div>
    );
  }
});
// ...
```

## <span id="demo-css-modules">演示: CSS Modules</span>

<div class="demo">
  <h2>Demo</h2>
  <p style="border: 1px solid red;">Text Text Text</p>
</div>

为了让CSS module工作起来，我们需要给webpack增加一些配置，配置有一点点复杂，慢慢来。

> [css modules](http://glenmaddern.com/articles/css-modules)的文档写的非常不错，可以从中学到很多css modules 的最佳实践。

我们可以使用`postcss-loader` 提供的一些选项来配置我们的css modules。我们需要告诉webpack我们准备给我们的css modules取什么样的名字。在开发环境下，我们需要让我们的css模块更加的通俗易懂，然而在生产环境中，并不需要。

在配置文件`webpack.config.js` 中，我们给css模块定义一个命名规则，如下：

```javascript
// ...
const cssModulesNames = `${isDev ? '[path][name]__[local]__' : ''}[hash:base64:5]`;
// ...
```

`hjs-webpack`帮助我们简化了webpack的配置，内置了css的loader。但是对于css modules来说，我们不仅仅需要添加一个用于load css modules的loader，而且也需要维护已经存在的那个。

让我们使用简单的正则表达式，在`config.module.loaders`里找出已经配置好的那个loader：

```javascript
const matchCssLoaders = /(^|!)(css-loader)($|!)/;

const findLoader = (loaders, match) => {
  const found = loaders.filter(l => l &&
      l.loader && l.loader.match(match));
  return found ? found[0] : null;
}
// existing css loader
const cssloader =
  findLoader(config.module.loaders, matchCssLoaders);
```

好在，在已经存在的loaders中找出了css loader，接下来，我们为css modules新建一个loader。

> 添加和维护已经存在的css loader，可以让我们很方便的应用全局的css样式。

回到`webpack.config.js`， 让我们创建一个新的css loader:

```javascript
// ...
const newloader = Object.assign({}, cssloader, {
  test: /\.module\.css$/,
  include: [src],
  loader: cssloader.loader
    .replace(matchCssLoaders,
    `$1$2?modules&localIdentName=${cssModulesNames}$3`)
})
config.module.loaders.push(newloader);
cssloader.test =
  new RegExp(`[^module]${cssloader.test.source}`)
cssloader.loader = newloader.loader
// ...
```

在我们新的loader中， 仅仅去load在src文件夹中的css文件。 其他的css文件，比如[font-awsome](http://fontawesome.io/), 将会使用另外的一个不做css modules处理的css loader来加载。

```javascript
config.module.loaders.push({
  test: /\.css$/,
  include: [modules],
  loader: 'style!css'
})
```

Css loader配置好了以后，让我们创建一个全局的css文件 `src/app.css`：

```shell
$ echo "body{ border: 1px solid red;}" > src/app.cs
```

可以在`src/app.js`中载入这些样式了：

```javascript
// ...
import './app.css'
// ...
```

使用`npm start`启动服务器，并且刷新浏览器，我们将看到预期中的页面：

{% asset_img browser-with-app-css.jpg %}

为了验证我们的css modules已经可以很好地工作了，让我们在 `src/` 文件夹下面创建一个 `styles.module.css` 文件，并且添加一个 `.wrapper` 类：

```javascript
// In src/styles.module.css
.wrapper {
  background: blue;
}
```

在 `src/app.js` 中引入刚刚创建的css modules 文件，并且把 `.wrapper` 类加入到 `<div />`中：

```javascript
// ...
import './app.css'
import styles from './styles.module.css'

const App = React.createClass({
  render: function() {
    return (
      <div className={styles.wrapper}>
        Text text text
      </div>
    )
  }
});
// ...
```

启动服务器，并且刷新浏览器页面，让我们看看效果吧：

{% asset_img browser-with-css-modules.jpg %}

## <span id="config-m-env">Configuring Multiple Environments</span>

在我们的App中，我们需要和Google API 做集成。 把keys直接写在一个发布了的项目中是不值得推荐的，我们需要让我们能够配置不同的方式在不同的环境中，读取到这些些关键的keys。

处理这些keys的一个有效的方式就是使用系统环境变量和我们的key绑定在一起。借助于 `webpack.DefinePlugin()` 和 `dotenv`, 我们可以建立一个支持多环境的机制：

首先， 我们需要加载 `dotenv` 依赖包：

```shell
$ npm i -D dotenv && touch .env
```

我们在项目的根目录下创建 `.env` 文件，在此文件中配置和我们项目有关的环境变量。借助于[dotenv](https://github.com/motdotla/dotenv)，我们可以配置一些脚本并且使得项目有权限读取这些变量。

使用 `dotenv` 读取环境变量是一件非常简单的事，让我们在 `webpack.config.js` 中引用 `.env` 文件：

```javascript
// ...
const dotenv = require('dotenv');

const dotEnvVars = dotenv.config();
```

一般来说，我们可以将全局环境变量保存在 `.env` 文件中。 为了区分不同的运行环境，我们将创建一个文件夹 `config/`， 并且增加不同环境的配置文件 `[env].config.js`。

为了加载这些配置文件，我们将会使用同一个方法。在 `webpack.config.js`文件中，我们需要添加以下的一些方法：

```javascript
// ...
const NODE_ENV = process.env.NODE_ENV;
const dotenv = require('dotenv');

// ...

const dotEnvVars = dotenv.config();
const environmentEnv = dotenv.config({
  path: join(root, 'config', `${NODE_ENV}.config.js`),
  silent: true,
});
```

我们可以将这两个对象合并到一起：

```javascript
// ...
const dotEnvVars = dotenv.config();
const environmentEnv = dotenv.config({
  path: join(root, 'config', `${NODE_ENV}.config.js`),
  silent: true,
});
const envVariables =
    Object.assign({}, dotEnvVars, environmentEnv);
```

`envVariables` 变量现在包含了所有环境变量和全局的环境变量，为了将它们和我们的的App联系起来，我们需要授予项目访问这个变量的权限。

Webpack包含一部分通过的插件，包括 `DefinePlugin()`, `DefinePlugin()` 可以在项目渲染到到浏览器之前，利用正则表达式替换某些对象的键-值。

按照惯例，我们给将要被替换的变量前后加上（`--`），例如，我们通过`__NODE_ENV__` 来访问`NODE_ENV`变量。

在我们的`webpack.config.js` 文件中，我们通过 `reduce()` 方法创建一个包含传统变量的对象：

```javascript
// ...
const envVariables =
    Object.assign({}, dotEnvVars, environmentEnv);

const defines =
  Object.keys(envVariables)
  .reduce((memo, key) => {
    const val = JSON.stringify(envVariables[key]);
    memo[`__${key.toUpperCase()}__`] = val;
    return memo;
  }, {
    __NODE_ENV__: JSON.stringify(NODE_ENV)
  });
```

然后，将 `defines` 对面作为配置参数传给 `DefinePlugin()`, 再将配置告诉webpack。

```javascript
// ...
const defines =
// ...

config.plugins = [
  new webpack.DefinePlugin(defines)
].concat(config.plugins);

// ...
```

好了，我们可以验证我们的配置是否成功啦，我们可以使用 `<App />`组件来展示我们配置的变量。比如： 我们可以修改 `render()`方法，来展示 `__NODE_ENV__`变量的值。

```javascript
//...
const App = React.createClass({
  render: function() {
    return (
      <div className={styles.wrapper}>
        <h1>Environment: {__NODE_ENV__}</h1>
      </div>
    )
  }
});
// ...
```

同样的，重启服务器，刷新页面，就可以看到效果啦。（我们是使用`NODE_ENV=development`来启动我们的项目的）。

{% asset_img browser-replace.jpg %}

## <span id="font-awsome">Font Awesome</span>

我们将会使用Font awsome显示评分星星。引入font-awsome的大部分配置工作都在前面的章节中做好了，我们只需要安装一下就可以啦。

使用`npm`安装：

```shell
$ npm i -S font-awesome
```

使用Font Awesome提供的图标，我们只需要在相应的节点上添加相应的类就行了，详细请参考[官方文档](http://fontawesome.io/)。

将font awesome的css引入到我们的项目中非常简单。因为我们需要全局使用，所以我们可以在`src/app.js`中引入：

```javascript
import React from 'react'
import ReactDOM from 'react-dom'

import 'font-awesome/css/font-awesome.css'
// ...
```

验证一下，修改 `render()` 方法，给我们的环境变量添加一个小图标：

```javascript
// ...

import 'font-awesome/css/font-awesome.css'
// ...

const App = React.createClass({
  render: function() {
    return (
      <div className={styles.wrapper}>
        <h1>
          <i className="fa fa-star"></i>
          Environment: {__NODE_ENV__}</h1>
      </div>
    )
  }
});
```

刷新浏览器，看看效果吧：

{% asset_img font-awesome-star.jpg %}

## <span id="webpack-tips">Webpack Tip: Relative requires</span>

我们使用了webpack来管理我们的app，它也可以帮助我们更简单的管理相关联的其他需求。比如，我们可以设置一个alias，来替代那些需要根据相对路径引入一些其他依赖文件的方式。

让我们将目录 `node_modules/` 和 `src/` 命名为 `root`，在添加一些其他的alias 对于我们已经创建的一些文件夹：

```javascript
var config = getConfig({
  // ...
})
// ...
config.resolve.root = [src, modules]
config.resolve.alias = {
  'css': join(src, 'styles'),
  'containers': join(src, 'containers'),
  'components': join(src, 'components'),
  'utils': join(src, 'utils')
}
```

在我们的源代码里，我们可以直接使用 `require(‘containers/some/app’)` 来替代相对路径的引用了。

# <span id="test-env">配置测试环境</span>

React提供很多的测试方式，让我们用测试来保证我们的功能能够正常工作。我们甚至可以打开浏览器并且刷新页面（我们配置了热加载，刷新都可能不需要）来验证。

虽然，在开发中可以及时从浏览器得到反馈是非常不错的。但是为了我们能够方便以及覆盖面更加全面，写一些程序化测试时非常必要的，可以快速有效并且可靠的告诉我们项目是否如期工作。

在这个环节中，我们写的大部分代码都是测试驱动的，就是先写测试，然后在补全功能，这样可以确保我们的能够测试我们的代码。

React team 使用的是 [jest](https://facebook.github.io/jest/)测试框架，我们将会使用一些列工具的组合：

- [karma](https://karma-runner.github.io/0.13/index.html) 作为测试运行框架
- [chai](http://chaijs.com/) 作为expectation库
- [mocha](https://mochajs.org/) 作为测试框架
- [enzyme](http://airbnb.io/enzyme/) react测试的扩展包
- [sinon](http://sinonjs.org/) 作为模拟沙箱

首先，让我们把这些都安装起来吧，并且安装一个ES6的依赖

```shell
$ npm i -D mocha chai enzyme chai-enzyme expect sinon babel-register babel-polyfill react-addons-test-utils
```

我们将会使用一个叫做 `enzyme` 的库，来帮助我们编写react测试变得更加简单和有趣。为了正确的使用它，我们需要添加一些webpack的配置。我们需要安装 `json-loader` 来load json格式的文件。（hjs-webpack以及帮助我们配置好了json-load 所需的修改，我们只要安装就行啦）。

```shell
$ npm i -D json-loader
```

我们将会使用karma来运行我们的测试，所以我们需要安装karma的一些依赖。使用karma是因为karma和react有很好的集成，当然咯，还是需要一些配置的。

让我们安装这些依赖吧：

```shell
$ npm i -D karma karma-chai karma-mocha karma-webpack karma-phantomjs-launcher phantomjs-prebuilt phantomjs-polyfill
$ npm i -D karma-sourcemap-loader
```

> 我们将会使用 [phantomJS] 来测试我们的文件。这样就不需要打开浏览器新窗口了。 PhantomJS是一个轻量级的，Webkit驱动的，使用JS接口的，可以使用我们在后台运行的模拟浏览器。

> 当然咯，如果你更喜欢使用Google Chrome来运行测试的话，可以将 ·、`karma-phantomjs-launcher` 替换成 `karma-chrome-launcher`.

可以去喝一杯咖啡等待安装完成了，这需要几分钟的。 一旦安装完成，我们需要创建两个配置文件，一个用来配置karma，一个用来配置我们的测试。

让我们通过karma来建立我们的webpack测试环境吧。最简单的方式就是使用karma提供的 `karma init`命令。首先，我们需要安装karma-cli，以及一些相关依赖。

```shell
$ npm install -g karma-cli
$ npm i -D karma karma-chai karma-mocha karma-webpack karma-phantomjs-launcher phantomjs-prebuilt phantomjs-polyfill
```

安装完成以后，可以运行karma init 了。

```
$ karma init
```

回答一些问题以后，命令会帮忙生成一个 `karma.conf.js` 的配置文件。文件中的大部分内容我们都会去修改，所以，在这里，可以一路按确定键了。

{% asset_img karma-init.jpg %}

<br>

> 我们也可以自己创建这个配置文件

> ```
>  $ touch karma.conf.js
> ```

配置文件创建好了，我们需要去添加一些配置选项，大部分的配置都自动添加好了。

```javascript
module.exports = function(config) {
  config.set({
    // ...
    basePath: '',
    preprocessors: {},
    port: 9876,
    colors: true,
    logLevel: config.LOG_INFO,
    browsers: ['Chrome'],
    concurrency: Infinity,
    plugins: []
  });
}
```

我们需要告诉karma，我们将会使用mocha和chai作为我们的测试框架，所以我们需要修改`frameworks: []` 属性，也需要添加支持这两个框架的插件：

```javascript
module.exports = function(config) {
  config.set({
    frameworks: ['mocha', 'chai'],
    basePath: '',
    plugins: [
      'karma-mocha',
      'karma-chai'
    ],
    // ...
  });
}
```

我们使用了webpack打包我们的所有文件，所以，我们也需要告诉karma我们的webpack配置。

```javascript
var webpackConfig = require('./webpack.config');

module.exports = function(config) {
  config.set({
    frameworks: ['mocha', 'chai'],
     webpack: webpackConfig,
     webpackServer: {
       noInfo: true
     },
    // ...
  });
}
```

也需要告诉karma如何运用webpack的配置，我们可以给plugins添加一个webpack的插件：

```javascript
module.exports = function(config) {
  config.set({
    frameworks: ['mocha', 'chai'],
    webpack: webpackConfig,
    webpackServer: {
      noInfo: true
    },
    plugins: [
      'karma-mocha',
      'karma-chai',
      'karma-webpack'
    ],
    // ...
  });
}
```

让我们修改一些可以让测试变得更加友好的东西吧。使用`spec-reporter`替换默认的 `progress`，将浏览器从`chrome` 改为`PhantomJS`.

首先， 让我们安装spec reporter：

```shell
$ npm i -D karma-spec-reporter
```

回到配置文件，将插件添加并且更改浏览器：

```javascript
module.exports = function(config) {
  config.set({
    reporters: ['spec'],
    plugins: [
      'karma-mocha',
      'karma-chai',
      'karma-webpack',
      'karma-phantomjs-launcher',
      'karma-spec-reporter'
    ],
    browsers: ['PhantomJS']
    // ...
  });
}
```

最后，我们需要告诉karma去哪儿找到测试的源文件。我们不直接告诉karma，而是采用一个中间件，告诉webpack我们的测试文件在哪里，然后再又webpack的配置告诉karma去哪儿找到打包好的测试文件。

```javascript
module.exports = function(config) {
  config.set({
    files: [
      'tests.webpack.js'
    ],
    // ...
  })
}
```

在这儿暂停一下，我们需要让kamar知道，需要从webpack中寻找测试文件`tests.webpack.js`。并且告诉它，需要使用sourcemap 预处理器来运行测试，这样的话可以便于我们调试。

```javascript
module.exports = function(config) {
  config.set({
    files: [
      'tests.webpack.js'
    ],
    preprocessors: {
      'tests.webpack.js': ['webpack', 'sourcemap']
    },
    plugins: [
      'karma-mocha',
      'karma-chai',
      'karma-webpack',
      'karma-phantomjs-launcher',
      'karma-spec-reporter',
      'karma-sourcemap-loader'
    ],
    // ...
  });
}
```

让我们创建 `tests.webpack.js` 文件，这个文件将会作为中间件联系webpack和karma。Karma将会更加这个文件加载所有被webpack打包好的测试文件。

这个文件内容很简单：

```javascript
require('babel-polyfill');
var context = require.context('./src', true, /\.spec\.js$/);
context.keys().forEach(context);
```

当karma运行这个文件的时候，它将会在`src/`文件加下面寻找所有以 `.spec.js`结尾的文件，并且将他们当做测试文件执行。在这里，我们可以创建任何我们想用到全局的帮助方法。

既然我们想使用全局使用一个叫做 `chai enzyme` 的帮助库，我们可以在这里配置他们：

```javascript
require('babel-polyfill');
// some setup first

var chai = require('chai');
var chaiEnzyme = require('chai-enzyme');

chai.use(chaiEnzyme())

var context = require.context('./src', true, /\.spec\.js$/);
context.keys().forEach(context);
```

好了，到目前为止，我们的karma配置文件就是这个样子了：

```javascript
var path = require('path');
var webpackConfig = require('./webpack.config');

module.exports = function(config) {
  config.set({
    basePath: '',
    frameworks: ['mocha', 'chai'],
    files: [
      'tests.webpack.js'
    ],

    preprocessors: {
      // add webpack as preprocessor
      'tests.webpack.js': ['webpack', 'sourcemap'],
    },

    webpack: webpackConfig,
    webpackServer: {
      noInfo: true
    },

    plugins: [
      'karma-mocha',
      'karma-chai',
      'karma-webpack',
      'karma-phantomjs-launcher',
      'karma-spec-reporter',
      'karma-sourcemap-loader'
    ],

    reporters: ['spec'],
    port: 9876,
    colors: true,
    logLevel: config.LOG_INFO,
    browsers: ['PhantomJS']
  })
};
```

我们差不多做好了所有的Karma测试的环境配置了，然是我们少了最后两步。在完成karma的配置之前，让我们创建一个简单的测试样例，来验证我们的配置是否完成吧。

我们将使用我们前面所创建的 `<App />` 组件作为我们项目的根组件吧。我们需要创建一个 `containers/App/App.spec.js` 测试文件。

```shell
$ mkdir src/containers/App && touch src/containers/App/App.spec.js
```

在这个测试文件中，我们将添加一个简单的测试，来测试我们的节点上是不是存在一个叫做 wrapper的样式。

这个测试仅仅用于验证我们的配置，所以我们只需要借助mocha和chai做简单的测试：

```javascript
import React from 'react'
import { expect } from 'chai'
import { shallow } from 'enzyme'

import App from './App'
import styles from './styles.module.css'

describe('<App />', function () {
  let wrapper;
  beforeEach(() => {
    wrapper = shallow(<App />)
  })

  it('has a single wrapper element', () => {
    expect(wrapper.find(`.${styles.wrapper}`))
            .to.have.length(1);
  });
});
```

<br>

> 在后面的内容中，我们会详细讲解如何测试我们的项目。这儿，你可以直接将测试代码复制到你的文件中去。

为了让测试跑起来，我们需要新建两个文件。 `src/containers/App.js`和css modules 的文件 `src/containers/styles.module.css`. 我们不需要使得我们的测试通过，仅仅让他们跑起来。

让我们创建一个 `App.js`文件，并且将 `scr/styles.modul.css` 移动到container文件夹下面：

```javascript
$ touch src/containers/App/App.js
$ mv src/styles.module.css \
     src/containers/App/styles.module.css
```

并且，把`src/app.js` 中的 `<App />` 的定义移动到新建的文件中去 `src/containers/App/App.js`：

```javascript
import React from 'react'
import ReactDOM from 'react-dom'

import styles from './styles.module.css'

const App = React.createClass({
  render: function() {
    return (
      <div className={styles.wrapper}>
        <h1>
          <i className="fa fa-star"></i>
          Environment: {__NODE_ENV__}</h1>
      </div>
    )
  }
});

module.exports = App;
```

最后我们需要在`src/app.js`中 引入 `<App />`组件：

```javascript
// ...
import './app.css'

import App from 'containers/App/App'

const mountNode = document.querySelector('#root');
ReactDOM.render(<App />, mountNode);
```

使用以下命令运行我们的测试：

```shell
$ NODE_ENV=test \
   ./node_modules/karma/bin/karma start karma.conf.js
```

{% asset_img npm-test-error.jpg %}

噢，天哪！什么东西出了错！别担心，这在预料之中的。。。

这个错误告诉我两件事。第一，webpack试图找到我们的测试框架并且和我们的测试绑定在一起。Webpack希望通过分析一个静态文件找到我们所有的依赖以及我们的源代码，然而，enzyme使用了一些动态的文件，所以就是失败咯。

显然，我们不希望这么做，因为我们并不需要给生产环境添加任何的测试框架。我们可以主动的告诉webpack让它忽略我们的测试框架，并且假设我们可以将它设置为一个_外部_依赖！

在我们 `webpack.config.js` 文件中，让我们添加一些enzyme需要的外部依赖：

```javascript
// ./webpack.config.js
// ...
var config = getConfig({
  isDev,
  in: join(src, 'app.js'),
  out: dest,
  clearBeforeBuild: true
});

config.externals = {
  'react/lib/ReactContext': true,
  'react/lib/ExecutionEnvironment': true,
  'react/addons': true
}
// ...
```

第二个错误是，有一些生产环境的插件和我们的测试混淆在一起没法区分。这样的话，我们需要在测试环境下，不加载那些插件。所以，让我们给测试环境做一些特殊的设置。

首先，我们可以通过 `NODE_ENV` 或者 是否运行在 `karma` 中来判断是否为测试环境。 让我们在 `webpack.config.js` 最上面添加一个 `isTest`的标记吧:

```javascript
require('babel-register');

const NODE_ENV = process.env.NODE_ENV;
const isDev  = NODE_ENV === 'development';
const isTest = NODE_ENV === 'test';
// ...
```

这样的话，我们就可以在我们的配置文件中，添加一些只在测试环境需要的配置啦。

将我们刚刚添加的那些_外部_依赖移动到测试里去吧，更新后的 `webpack.config.js` 文件如下：

```javascript
// ./webpack.config.js
// ...
var config = getConfig({
// ...
});

if (isTest) {
  config.externals = {
    'react/lib/ReactContext': true,
    'react/lib/ExecutionEnvironment': true
  }

  config.plugins = config.plugins.filter(p => {
    const name = p.constructor.toString();
    const fnName = name.match(/^function (.*)\((.*\))/)

    const idx = [
      'DedupePlugin',
      'UglifyJsPlugin'
    ].indexOf(fnName[1]);
    return idx < 0;
  })
}
// ...
```

现在，我们再次运行我们的测试，我们只是会得到没有通过的提示啦：

```shell
$ NODE_ENV=test \
   ./node_modules/karma/bin/karma start karma.conf.js
```

{% asset_img karma-2.jpg %}<br>

下面，让我们致力于让测试通过吧。

首先，让我们把在 `package.json` 中添加运行测试的脚步吧，省的我们每次都要输入一串长长的命令：

```json
{
  "name": "yelp",
  "version": "1.0.0",
  "description": "",
  "scripts": {
    "start": "./node_modules/.bin/hjs-dev-server",
    "test": "NODE_ENV=test ./node_modules/karma/bin/karma start karma.conf.js"
  },
  // ...
}
```

这样的话，我们只需要运行 `npm test` 就可以启动我们的测试啦：

```shell
 $ npm test
```

我们前面的测试没有通过是因为，虽然我们定义了一个 `.wrapper{}` 类，但是这个类确实空的，所以webpack会忽略它。那么通过 `styles.wrapper` 引用到的就是 undefined了。所以，我们只需要给类添加一些内容：

```css
.wrapper {
  display: flex;
}
```

同时，我们也把 `src/styles.module.css` 中的内容清楚吧。

在我们的App中，我们将会使用 [flexbox](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Flexible_Box_Layout/Using_CSS_flexible_boxes) 布局，所以我们可以添加 `display: flex;` 到我们css 类的描述中。

这次，我们使用 `npm test` 再次运行我们的测试，所有测试都通过啦！

{% asset_img karma-3.jpg %}

<br>

来回在我们的编辑器和终端之间切换，是一个很烦的事情。如何当我们修改了代码，测试能自动更新并且报告错误的话，那就好了！非常幸运，karma提供了非常简答的方式。

只需要在我们的测试启动脚本后面，加上 `--watch` 就行啦，让我们同样把他加到 `package.json` 中去吧：

```json
{
  "name": "yelp",
  "version": "1.0.0",
  "description": "",
  "scripts": {
    "start": "./node_modules/.bin/hjs-dev-server",
    "test": "NODE_ENV=test ./node_modules/karma/bin/karma start karma.conf.js",
    "test:watch": "npm run test -- --watch"
  },
  // ...
}
```

如此，我们需要使用 `npm run test:watch` 来代替 `npm test` 启动我们的测试。我们也需要告诉karma（通过配置 `karma.conf.js` 文件），让它帮忙监听文件的修改。

Karma 使用配置对象中的 `singleRun` 属性来处理这个。我们将借助与Node的 [`yargs`](http://www.kancloud.cn/kancloud/command-line-with-node/48652) 来实现：

```shell
$ npm i -D yargs
```

在 `karma.conf.js` 文件中，我们可以使用 `singleRun` 以及 `yargs` 来检查 `--watch` 标记。

```javascript
var argv = require('yargs').argv;
// ...
module.exports = function(config) {
  config.set({
    basePath: '',
    frameworks: ['mocha', 'chai'],
    // ...
    singleRun: !argv.watch
  });
}
```

好了，当我们运行 `npm run test:watch` 命令。修改和保存了一个文件以后，我们的测试就会被触发。让我们的测试驱动开发，非常方便！

## <span id="test-skeleton">建立测试骨架</span>

让我们先把我们app的地基建立起来吧。我们的 `<App />` 容器将会包含我们的所以页面，并且负责负责页面间的跳转和路由。

作为一名优秀的开发者，让我们首先创建测试，来确保我们的实现了我们的设想。首先，我们要确保我们有一个 `<Router />` 组件。

我们也可以顺便构建我们的测试结构。

在 `src/containers/App/App.spec.js` 中，让我们开始创建我们的测试样例。首先，我们要引用我们的库以及要测试的源文件：

```javascript
import { expect } from 'chai'
import { shallow } from 'enzyme'

import App from './App'

describe('<App />', () => {
  // define our tests in here
})
```

我们将会是用 `expect()` 来确保我们的测试期望。使用 `shallow()`（来自 enzyme） 来渲染被测试的元素到我们的测试浏览器中。

## <span id="test-model">测试模式</span>

无论使用是什么语言，测试什么样的代码，我们的原则都是相同的。我们希望：

1. 定义核心功能
2. 设置一个期待结果
3. 对比运行结果和期待结果

在Jasmine中，以上的步骤都非常容易实现：

1. 使用 `describe()/it()` 来定义核心功能
2. 使用 `expect()` 来设定期待输出结果
3. 使用 `beforeEach()`以及 matchers 来验证输出

在我们的测试中，需要假装 `<App />` 已经在浏览器中渲染好了。Enzyme 可以轻松的做到这一点，无论是深度渲染还是浅渲染（后面将会涉及这两点的区别）。

```javascript
// ...
describe('<App />', () => {
  // define our tests in here
  let wrapper; // "dom" node wrapper element
  beforeEach(() => {
    wrapper = shallow(<App />);
  })
})
```

我们可以开始测试 `<App />` 里是否有一个 `<Router />` 组件啦，通过使用 `find()` 方法在我们的wrapper实例中查找router。

```javascript
// ...
describe('<App />', () => {
  // ...

  it('has a Router component', () => {
    expect(wrapper.find('Router'))
        .to.have.length(1);
  })
})
```

然后，我们就可以跑起来试试啦：

{% asset_img npm-test-one.jpg %}

因为我们还没有实现 `<App />` 组件，所以，我们的测试挂啦！

# <span id="routing">路由</span>

在实现routes之前，让我们快速的谈谈如何建立我们的路由吧！

我们的React App，可以通过 `children` 组件的特性来控制我们的路由。不同的子组件对于不同的路由。 我们有一个标题栏，我们希望它可以一直在页面上显示，每次更换路由，仅仅改变标题栏以下的页面内容。

我们将会在App中创建一个 `<Router />` 组件，根据不同的路由渲染这个组件不同的内容，该如何显示如何切换都又路由内容决定。`<App />`将会变成一个非常的容器，仅仅用来安放 路由组件，不在显示和处理任何的页面元素。

在 `src/containers/App/App.js` 中，我们首先确实我们引入了 `react-router` 库：

```javascript
import React,{ PropTypes } from 'react'
import { Router } from 'react-router'

// ...
```

然后，按照惯例，让我们来创建React组件吧（无论是使用`createClass({})`,还是ES6 提供的继承。

```javascript
import React, { PropTypes } from 'react';
import { Router } from 'react-router';

class App extends React.Component {
  render() {
    return (<div>Content</div>)
  }
}
```

我喜欢使用 getter/setter 方法来创建class类容，这仅仅是个人习惯

```javascript
import React, { PropTypes } from 'react'
import { Router } from 'react-router'

class App extends React.Component {
  // class getter
  get content() {
    return (<Router />)
  }

  render() {
    return (
      <div style={ { height: '100%' } }>
        {this.content}
      </div>
    )
  }
}
```

我们将会使用app 容器返回 `<Router />` 组件的一个实例。`<Router />` 组件需要我们传入一个记录历史记录的对象，以此来告诉我们浏览器如何监听浏览历史和地址变化。历史记录会告诉我们的react如何跳转。

目前，有许多种不同的记录历史记录的方式可以供我们使用，最流行是两种， `browserHistory` 和 `hashHistory`。 `browserHistory` 使用的是原生的HTML5 react路由，表现形式和服务器路由一样。

另外一种，是使用 `#` 来标记不同的浏览记录。基于浏览器哈希的方式，一个支持所有浏览器的客户端路由的老把戏。

我们将会使用  `browserHistory` 的方式。我们将 `browserHistory` 作为一个属性传给`<Router />`组件以此来告诉它我们的决定。

```javascript
import React, { PropTypes } from 'react';
import { Router } from 'react-router';

class App extends React.Component {
  static propTypes = {
    history: PropTypes.object.isRequired
  }

  // class getter
  get content() {
    return (
      <Router history={this.props.history} />
    )
  }

  render() {
    return (
      <div style={ { height: '100%' } }>
        {this.content}
      </div>
    )
  }
}
```

路由的基础差不多搭好了，我们只需要传入我们自定义的路由就行啦。

```javascript
import React, { PropTypes } from 'react';
import { Router } from 'react-router';

class App extends React.Component {
  static propTypes = {
    routes: PropTypes.object.isRequired,
    history: PropTypes.object.isRequired
  }

  // class getter
  get content() {
    return (<Router
        routes={this.props.routes}
        history={this.props.history} />)
  }

  render() {
    return (
      <div style={ { height: '100%' } }>
        {this.content}
      </div>
    )
  }
}
```

为了真正的使用上我们的路由，当我们渲染 `<App />` 组件的时候，我们需要告诉它路由需要的两个信息：

- history： 我们将会在 `react-router` 中引入 `browserHistory` 对象，并且直接传给App。
- routers： 我们会传入一个 JSX。

回到 `src/app.js` 文件，我们直接传入引入的 history：

```javascript
import React from 'react'
import ReactDOM from 'react-dom'

import 'font-awesome/css/font-awesome.css'
import './app.css'

import {browserHistory} from 'react-router'

import App from 'containers/App/App'

const mountNode = document.querySelector('#root');
ReactDOM.render(
  <App history={browserHistory} />, mountNode);
```

然后，我们需要建立一些路由规则。首先，我们需要在浏览器中得到一些信息。让我们根据我们要显示的页面，建立一个独立的路由吧（我们很快就会改变它）。

我们需要访问这些组件：

- `<Router />` 组件
- `<Route />` 组件
- 自定义的路由组件

`Router` 以及 `Route` 组件可以直接从 `react-router` 中引入：

```javascript
import React from 'react'
import ReactDOM from 'react-dom'

import 'font-awesome/css/font-awesome.css'
import './app.css'

import {browserHistory, Router, Route} from 'react-router'

import App from 'containers/App/App'

const mountNode = document.querySelector('#root');
ReactDOM.render(
  <App history={browserHistory} />, mountNode);
```

我们可以创建这两个组件的JSX实例来实现自定义的路由：

```javascript
// ...
import './app.css'

import {browserHistory, Router, Route} from 'react-router'

const routes = (
  <Router>
    <Route path="/" component={Home} />
  </Router>
)
//...
```

因为我们没有创建 `Home` 组件，所以前面的例子是错误的，让我们来创建一个简单的组件，让上面的代码能够工作：

```javascript
// ...
import './app.css'

import {browserHistory, Router, Route} from 'react-router'

const Home = React.createClass({
  render: function() {
    return (<div>Hello world</div>)
  }
})
const routes = (
  <Router>
    <Route path="/" component={Home} />
  </Router>
)
//...
```

最后，我们可以将 `routes` 对象传给 `<App />`组件啦，然后刷新浏览器，如果一切都没用搞错的话，我们将会在页面上看到 “Hello World”啦。

{% asset_img hello-world-browser.jpg %}

同样的，我们会发现，测试也通过了！

{% asset_img npm-test-success-1.jpg %}
<br />

## <span id="routes">建立真实路由表</span>

到目前为止，我们仅仅给我们的项目创建了一个用于演示的单独的路由。让我们把路由分割到单独的文件吧，这样可以使得我们的项目结构更加清晰。

```shell
$ touch src/routes.js
```

在 `src/routes.js` 文件中，让我们创建并且输出一个用于创建不同路由的方法。将 `src/app.js` 中的一部分代表搬移过来，并且做一些修改：

```javascript
import React from 'react'
import {browserHistory, Router, Route, Redirect} from 'react-router'

const Home = React.createClass({
  render: function() {
    return (<div>Hello world</div>)
  }
})

export const makeRoutes = () => (
    <Router>
      <Route path="/" component={Home} />
      <Redirect from="*" to="/" />
    </Router>
  )

export default makeRoutes
```

我们可以在 `src/app.js` 文件中用输出的 `makeRoutes` 方法替代 `routes` 的声明！

```javascript
mport React from 'react'
import ReactDOM from 'react-dom'

import 'font-awesome/css/font-awesome.css'
import './app.css'

import App from 'containers/App/App'

import {browserHistory} from 'react-router'
import makeRoutes from './routes'

const routes = makeRoutes()

const mountNode = document.querySelector('#root');
ReactDOM.render(
  <App history={browserHistory}
        routes={routes} />, mountNode);
```

我们可以看看测试结果，来确保我们的修改是否可以正常的工作。


## <span id="main-page">主页以及其嵌套路由</span>

路由建立好了，我们开始创建我们的主页吧。这个页面用来展示我们的主要地图，并且列出一些餐厅。这就是我们的主页。

因为我们将会搭建一个复杂的项目，我们会将路由切分开来，让需要使用到的组件自己去维护自己的路由。换句话说，我们的主页的视图仅仅包含它的子路由，而不是一个巨大的路由文件，嵌套的组件将会创建他们自己的视图。

让我们在根目录下创建一个新的文件夹 `views`， 并且按照路由的名字来命名子文件夹，目前，我们要创建一个 `Main/` 路由的视图：

```shell
$ mkdir -p src/views/Main
```

在这个 `Main/` 文件夹里，创建两个文件：

- routes.js    : 用于定义 `Main/` 视图下的路由规则
- Container.js : 用于定于路由本身容器中的文件

```shell
$ touch src/views/Main/{Container,routes}.js
```

{% asset_img main-container.jpg %}
<br />

让我们在 `src/views/Main/routes.js` 中为视图容器创建一个简单的路由。

```javascript
import React from 'react'
import {Route} from 'react-router'
import Container from './Container'

export const makeMainRoutes = () => {

  return (
    <Route path="/" component={Container} />
  )
}

export default makeMainRoutes;
```

当我们在主路由文件中，引入刚刚创建的这个路由时，我们需要创建一个子元素。但是，我们现在仅仅需要验证我们的机制是否正确，我们可以创建一个非常简单的内容，代码如下：

```javascript
// in src/views/Main/Container.js
import React from 'react'

export class Container extends React.Component {
  render() {
    return (
      <div>
        Hello from the container
      </div>
    )
  }
}

export default Container
```

定义好了内容，让我们回到 `src/routes.js ` 文件载入这个新的子路由。 因为我们期待的是一个方法而不是一个对象，所以我们要确保我们展示的是这个方法的返回值而不是方法本身。

修改最初的 `src/routes.js` 文件，移除 `Home` 组件，并且引入我们的新的路由，我们的文件变成了这样：

```javascript
import React from 'react'
import {browserHistory, Router, Route, Redirect} from 'react-router'

import makeMainRoutes from './views/Main/routes'

export const makeRoutes = () => {
  const main = makeMainRoutes();

  return (
    <Route path=''>
      {main}
    </Route>
  )
}

export default makeRoutes
```

定义了子路由以后，我们应该很少会去修改主路由了。我们可以根据相同的步骤，创建其他的顶级路由。

## <span id="demo-container-router">演示: Routing to Container Content</span>

<div class="demo">
   <h2>Demo</h2><p>Hello from the container</p>
</div>

{% asset_img hello-container.jpg %}
<br />

## <span id="map-router">Maps 的路由</span>

让我们把 `<Map />` 组件添加到我们的页面上来，在前面的文章中，我们讲解了如何创建一个google API 的地图组件。我们可以将这个地图模块用到我们的项目中。

让我们安装这个 `npm` 吧：

```shell
$ npm install --save google-maps-react
```

在我们的 `<Container />` 组件中，我们将这页面上放一个隐藏的地图组件。这个地图组件将会加载Google APIs, 并且创建一个Google 地图的实例。我们会将这个实例交给所有的子组件使用，但是本身不会再页面上显示。因为我们将需要显示一系列的地址信息但是不要地图在页面显示出来。

在我们可以使用 `<Map />` 组件之前，我们需要申请一个Google API key。在本文的第一章节中，我们使用 `WebpackDefinePlugin()` 来处理存放这些key的相关程序。 所以我们可以将我们的Google Api key 放在 `.env` 中：

```
GAPI_KEY=abc123
```

在项目中，我们通过访问 `__GAPI_KEY__` 来读取这个key。

下面一步，我们需要告诉google Api 插件，我们的key：

```javascript
import React from 'react'
import Map, {GoogleApiWrapper} from 'google-maps-react'

export class Container extends React.Component {
  // ...
}

export default GoogleApiWrapper({
  apiKey: __GAPI_KEY__
})(Container)
```

现在，当我们在页面上载入 `<Container />` 组件，我们可以看到我们的google api 实例被加载了：

{% asset_img google-api-script.jpg %}
<br />

既然，Google API 已经加载了，我们可以将 `<Map />` 组件加入到 `<Container />` 组件中了。

```javascript
import React from 'react'
import Map, {GoogleApiWrapper} from 'google-maps-react'

export class Container extends React.Component {
  render() {
    return (
      <div>
        Hello from the container
        <Map
          google={this.props.google} />
      </div>
    )
  }
}
```

{% asset_img google-maps-simple.jpg %}
<br />

# <span id="places-list">获取位置清单</span>

经过我们的努力，终于把地图加载到我们页面上了，让我们使用google api 显示一个很多位置的列表吧。当 `<Map />` 组件在页面上加载好了以后，回调函数 `onReady()` 会被触发。我们将会利用这个函数来向google api 做一些请求。

让我们修改 `src/views/Main/Container.js` 文件， 定义一个 `onReady()` 的实现：

```javascript
export class Container extends React.Component {
  onReady(mapProps, map) {
    // When the map is ready and mounted
  }
  render() {
    return (
      <div>
        <Map
          onReady={this.onReady.bind(this)}
          google={this.props.google} />
      </div>
    )
  }
}
```

在这儿，我们可以直接使用Google Api 而不用做任何其他的设置。我们先创建一个帮助方法来运行google api 的命令。让我们在 `src/utils` 文件夹下面创建一个新的文件 `googleApiHelpers.js`. 我们可以把所有的和google api 有关的方法和命令都放在这儿，便于管理，并且返回一个promise。

```javascript
export function searchNearby(google, map, request) {
  return new Promise((resolve, reject) => {
    const service = new google.maps.places.PlacesService(map);

    service.nearbySearch(request, (results, status, pagination) => {
      if (status == google.maps.places.PlacesServiceStatus.OK) {

        resolve(results, pagination);
      } else {
        reject(results, status);
      }
    })
  });
}
```

现在，我们可以在 `onReady` 方法里调用google api的这个帮助方法了：

```javascript
import {searchNearby} from 'utils/googleApiHelpers'

export class Container extends React.Component {
  onReady(mapProps, map) {
    const {google} = this.props;
    const opts = {
      location: map.center,
      radius: '500',
      types: ['cafe']
    }
    searchNearby(google, map, opts)
      .then((results, pagination) => {
        // We got some results and a pagination object
      }).catch((status, result) => {
        // There was an error
      })
  }
  render() {
    return (
      <div>
        <Map
          onReady={this.onReady.bind(this)}
          google={this.props.google} />
      </div>
    )
  }
}
```

因为我们要改变 `<Container />` 组件的状态，便于我们将api的结果更新给组件，所以：

```javascript
export class Container extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      places: [],
      pagination: null
    }
  }
  // ...
```

现在，当请求到google api的结果以后，我们可以更新在组件的state里面了，让我们更新 `onReady()` 方法吧：

```javascript
export class Container extends React.Component {
  onReady(mapProps, map) {
    const {google} = this.props;
    const opts = {
      location: map.center,
      radius: '500',
      types: ['cafe']
    }
    searchNearby(google, map, opts)
      .then((results, pagination) => {
        this.setState({
          places: results,
          pagination
        })
      }).catch((status, result) => {
        // There was an error
      })
  }
  // ...
}
```

有了这些state了，我们可以再次更新我们的 `render()`方法：

```javascript
export class Container extends React.Component {
  // ...
  render() {
    return (
      <div>
        Hello from the container
        <Map
          google={this.props.google}
          onReady={this.onReady.bind(this)}
          visible={false}>

          {this.state.places.map(place => {
            return (<div key={place.id}>{place.name}</div>)
          })}

        </Map>
      </div>
    )
  }
}
```

演示结果如下：

{% asset_img places-list-simple.jpg %}
<br />

# <span id="sidebar">创建侧边栏</span>


在本章节中，我们将为我们的项目添加一个侧边栏，让他更加的潮流一些。

为了实现这一部分，我们将增加一些内联样式并且使用react 原生的数据流。

首先，让我们安装一个叫做 [classnames](https://www.npmjs.com/package/classnames) 的npm 模块。它的[说明文档](https://github.com/JedWatson/classnames/blob/master/README.md) 非常详细的阐述了这个模块的用法和主要功能，这里就不详述了：

``` bash
$ npm install --save classnames
```

现在，让我们跳出App，开始进入到组件的内容中来吧。首先，我们要创建一个 `<Header />` 组件。

因为我们创建的是一个共享的组件（并不是那种只用在特定页面的），通常比较推荐的存放地点是 `src/components/Header` 文件夹，让我们来创建这个文件夹以及相关的测试文件吧：

```bash
$ mkdir src/components/Header
$ touch src/components/Header/{Header.js,Header.spec.js}
```

{% asset_img header-component-tree.jpg %}
<br />


我们的 `<Header />` 非常简单。就是用来显示我们项目的名字和一些导航菜单。按照惯例，我们首先创建测试。

在 `src/components/Header.spec.js` 文件中，让我们来创建测试：

```javascript
import React from 'react'
import { expect } from 'chai'
import { shallow } from 'enzyme'

import Header from './Header'

describe('<Header />', () => {
  let wrapper;
  beforeEach(() => {
    wrapper = shallow(<Header />)
  });

  // These show up as pending tests
  it('contains a title component with yelp');
  it('contains a section menu with the title');
})
```

{% asset_img header-test-pending.jpg %}
<br />

测试也比较简单，我们仅仅期待这个组件包含一些文本：

```javascript
import React from 'react'
import { expect } from 'chai'
import { shallow } from 'enzyme'

import Header from './Header'

describe('<Header />', () => {
  let wrapper;
  beforeEach(() => {
    wrapper = shallow(<Header />)
  });

  it('contains a title component with yelp', () => {
    expect(wrapper.find('h1').first().text())
        .to.equal('Yelp')
  });

  it('contains a section menu with the title', () => {
    expect(wrapper.find('section').first().text())
        .to.equal('Fullstack.io')
  });
})
```

这时候运行测试，肯定是挂的，因为我们根本还没有实现任何可以使得测试通过的功能。

所以，让我给组件添加一些代码吧：

```javascript
import React from 'react'
import {Link} from 'react-router'

export class Header extends React.Component {
  render() {
    return (
      <div>
        <Link to="/"><h1>Yelp</h1></Link>
        <section>
          Fullstack.io
        </section>
      </div>
    )
  }
}

export default Header
```

再次运行测试，就能通过啦：

{% asset_img header-test-passing.jpg %}
<br />

然而，刷新浏览器，并没有看到我们所期待的东西。让我们确保，我们在我们的顶级容器中包含了这个新建的组件：

在 `src/views/Main/Container.js` 中：

```javascript
// our webpack alias allows us to reference `components`
// relatively to the src/ directory
import Header from 'components/Header/Header'

// ...
export class Container extends React.Component {
  // ...
  render() {
    return (
      <div>
        <Map
          visible={false}>
          <Header />
          {/* ... */}
        </Map>
      </div>
    )
  }
}
```

再次刷新浏览器：

{% asset_img header-no-styles.jpg %}
<br />

## <span id="inline-css">内联样式</span>

我们可以直接给 `<Header />` 添加样式。不使用CSS Modules的话，我们可以创建一个特殊css标识，引入一个全局css 文件，并且将它应用到  `<Header />` 组件中去。既然我们使用了css modules，那么让我们创建一个css modules 文件来处理 `header` 相关的样式吧。

让我们在 `header` 文件夹下面创建一个后缀为 `.module.css` 的css文件吧：

``` bash
$ touch src/components/Header/styles.module.css
```

让我们创建一个名为 `topbar` 的简单类，并且添加一些描述：

``` css
/* In `src/components/Header/styles.module.css `*/
.topbar {
  border: 1px solid red;
}
```

我们可以引入这个文件来使用这个样式：

```javascript
import React from 'react'
import {Link} from 'react-router'

import styles from './styles.module.css';

export class Header extends React.Component {
  render() {
    return (
      <div className={styles.topbar}>
        {/* ... */}
      </div>
    )
  }
}
```

将 `styles.topbar` 类添加到 `<Header />` 组件以后，我们可以看到，我们的标题栏被边框框起来啦、

{% asset_img header-styles-border.jpg %}
<br />

让我们继续添加一些样式，让标题栏变得更加漂亮：

```css
/* In `src/components/Header/styles.module.css `*/
.topbar {
  position: fixed;
  z-index: 10;
  top: 0;
  left: 0;
  background: #48b5e9;
  width: 100%;
  padding: 0 25px;
  height: 80px;
  line-height: 80px;
  color: #fff;

  a {
    text-transform: uppercase;
    text-decoration: none;
    letter-spacing: 1px;

    line-height: 40px;
    h1 { font-size: 28px; }
  }
  section {
    position: absolute;
    top: 0px;
    right: 25px;
  }
}
```

并且在 `app.css` 中添加一些全局样式（一些全局起作用的样式）。

```css
*,
*:after,
*:before {
    box-sizing: border-box;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    font-smoothing: antialiased;
    text-rendering: optimizeLegibility;
    font-size: 16px;
}

body {
  color: #333333;
  font-weight: lighter;
  font: 400 15px/22px 'Open Sans', 'Helvetica Neue', Sans-serif;
  font-smoothing: antialiased;
  padding: 0;
  margin: 0;
}
```

{% asset_img header-topbar-style.jpg %}
<br />

现在，我们的标题栏终于说的上漂亮啦。但是，给标题栏添加了一些样式以后，我们的主要内容被遮掉了一些。我让我们给主页添加一些样式来修复吧。

同样的，我们可以给 `<Container />` 组件创建一个css modules 样式文件。

```bash
$ touch src/views/Main/styles.module.css
```

再添加一些css：

```css
.wrapper {
  overflow-y: scroll;
  display: flex;
  margin: 0;
  padding: 15px;

  height: 100vh;
  -webkit-box-orient: horizontal;
  -o-box-orient: horizontal;
}

.content {
  position: relative;
  flex: 2;
  top: 80px;
}
```

> 给内容设置 `flex: 2` 是为了让它去两个元素的最大者（sidebar vs content），关于这个后面会有更详细的描述

同样的，在组件中加载这些样式：

```JavaScript

import styles from './styles.module.css'

export class Container extends React.Component {
  // ...
  render() {
    return (
        <Map
          visible={false}
          className={styles.wrapper}>
          <Header />
          <div className={styles.content}>
            {/* contents */}
          </div>
        </Map>
      </div>
    )
  }
}
```

{% asset_img header-topbar-style-content.jpg %}
<br />

## <span id="css-variables">CSS 变量</span>

我们注意到，上面的css中有很多值是写死的，比如说 `topbar` 中的高度属性。

```css
/* In `src/components/Header/styles.module.css `*/
.topbar {
  /* ... */
  background: #48b5e9;
  height: 80px;
  line-height: 80px;
  /* ... */
}
```

PostCSS 中，非常有价值的一部分功能就是可以在我们的css中使用变量。 在CSS中使用变量有好几种的解决方案，我们将会使用postcss 所提供的方法。

我们可以在变量前面加上两个  `-` 作为前缀定义变量。比如：

```css
.topbar {
  --height: 80px;
}
```

> 注意： 当我添加一个自定义的属性（或者是变量）的时候，我们也要遵循css的语法规则。


这样的话，我们就可以在后续的css中使用这个变量了。用 `var()` 方法调用变量，比如说：

```css
/* In `src/components/Header/styles.module.css `*/
.topbar {
  --height: 80px;
  /* ... */
  background: #48b5e9;
  height: var(--height);
  line-height: var(--height);
  /* ... */
}
```

虽然这样已经很好了，但是我们仍然只能在 `.topbar` 类中使用这些变量。为了可以在其他的样式里面也是用这个变量，比方说，在 `content` 类中使用，我们需要把变量放在更高层次的DOM结构中。

比如说，我们可以把变量定义在 `wrapper` 类中。但是，postcss 有一个更加聪明的办法，我们使用 `:root` 选择器将变量放在一个根节点中。

```css
/* In `src/components/Header/styles.module.css `*/
:root {
  --height: 80px;
}
.topbar {
  /* ... */
  height: var(--height);
  line-height: var(--height);
  /* ... */
}
```

我们可以创建一个通用的css文件，把css变量都放在里面，是的所有的css都可以使用到我们定义的变量，比如，创建一个文件 `src/styles/base.css`:

```bash
$ touch src/styles/base.css
```

然后，我们将 `:root` 定义搬到 `base.css` 中：

```css
:root {
  --topbar-height: 80px;
}
```

在我们其他的css modules中使用这些变量，首先要引入这个文件。

回到我们 `src/components/Header/styles.module.css`， 我们可以将 `:root` 定义替换为引用文件：

```css
@import url("../../styles/base.css");
/* ... */
.topbar {
  /* ... */
  height: var(--height);
  line-height: var(--height);
  /* ... */
}
```

现在，我们有一个可以统一修改高度的地方啦。

# <span id="components">组件的分割和设计</span>

标题栏创建好了，让我们继续我们的主页面。我们的项目包含一个侧边栏和一个根据内容变化的主要页面。就是说，我们的页面首先显示的是一张地图，当用户点击地图上某一个点的时候，我们将会更新页面内容，显示用户点击的地点的详细信息。

让我们先从显示位置列表的侧边栏开始吧，其中最艰难的工作我们已经完成了。 **React** 推荐的方式，我们定义一个组件来包含多个相同的组件。简单地说，就是我们将会建立的 `<Listing />` 组件用来列举一个个单独的一项。这样的话，我们可以集中关注在每一列的内容上，而不用考虑更加高层次的东西。

让我们从我们简单的列表扩展到一个 `<Sidebar>` 组件。因为我们创建的这个组件是可以共享的，所以将它放在 `src/components/`,同时创建CSS，

```bash
$ mkdir src/components/Sidebar
$ touch src/components/Sidebar/{Sidebar.js,styles.module.css}
```

在我们的 `src/views/Main/Container.js ` 中：

```javascript
import Sidebar from 'components/Sidebar/Sidebar'

export class Container extends React.Component {
  // ...
  render() {
    return (
      <Map
        visible={false}
        className={styles.wrapper}>
        <Header />
        <Sidebar />
        {/* contents */}
      </Map>
    )
  }
}
```

当然，我们也需要传一些属性给 `<Sidebar />` 组件。它的职责就是列举我们的位置，所以组件需要知道我们从google API 拿到了哪些位置。这些信息现在存放在 `<Container />` 组件的state中。回到这个文件：

```javascript
import Sidebar from 'components/Sidebar/Sidebar'

export class Container extends React.Component {
  // ...
  render() {
    return (
        <Map
          visible={false}
          className={styles.wrapper}>
          <Header />
          <Sidebar
            title={'Restaurants'}
            places={this.state.places}
            />
          {/* contents */}
        </Map>
      </div>
    )
  }
}
```

现在，让我们开始添加侧边栏组件的内容吧：

```javascript
import React, { PropTypes as T } from 'react'
import styles from './styles.module.css'

export class Sidebar extends React.Component {
  render() {
    return (
      <div className={styles.sidebar}>
        <div className={styles.heading}>
          <h1>{this.props.title}</h1>
        </div>
      </div>
    )
  }
}

export default Sidebar
```

添加一些样式:

```css
@import url("../../styles/base.css");

.sidebar {
  height: 100%;
  top: var(--topbar-height);
  left: 0;
  overflow: hidden;

  position: relative;
  flex: 1;
  z-index: 0;

  .heading {
    flex: 1;
    background: #fff;
    border-bottom: 1px solid #eee;
    padding: 0 10px;

    h1 {
      font-size: 1.8em;
    }
  }
}
```

{% asset_img sidebar-no-style.jpg %}
<br />

到目前为止，我们的 `<Sidebar />` 组件基本建立好了，但是仅仅是渲染了标题信息。我们暂时就不再花更多时间在这个组件上，让我们继续进入到一个新的 `<Listing />` 组件中去。


> 我们可以直接在 `<Sidebar>` 里面列举位置清单，但是这不是 **React** 推荐的方式。


让我们创建一个 `<Listing />` 组件来列举每个地点。我们将利用另一个附加的组件 `<Item />` 来显示每一个单独的地点。

```bash
$ mkdir src/components/Listing
$ touch src/components/Listing/{Listing.js,Item.js,styles.module.css}
$ touch src/components/Listing/{Listing.spec.js,Item.spec.js}
```

既然我们是遵从测试驱动开发的模式，那么让我们首先关注 `Listing.spec.js` 文件吧。我们对这个组件的期望是，有预期中的样式，并且包含一些列的 `<Item />` 组件。所以，测试应该是这样：

```javascript
import React from 'react'
import { expect } from 'chai'
import { shallow } from 'enzyme'

import Listing from './Listing'
import styles from './styles.module.css'

describe('<Listing />', () => {
  let wrapper;
  const places = [{
    name: 'Chicago'
  }, {
    name: "San Francisco"
  }];

  beforeEach(() => {
    wrapper = shallow(<Listing places={places} />)
  });

  it('wraps the component in a listing css class')
  it('has an item for each place in the places prop')
})
```

让我们继续，并且完善我们的测试。

```javascript
import React from 'react'
import { expect } from 'chai'
import { shallow } from 'enzyme'

import Listing from './Listing'
import styles from './styles.module.css'

describe('<Listing />', () => {
  let wrapper;
  const places = [{
    name: 'Chicago'
  }, {
    name: "San Francisco"
  }];
  beforeEach(() => {
    wrapper = shallow(<Listing title={'Cafes'}
                      places={places} />)
  });

  it('wraps the component in a listing css class', () => {
    expect(wrapper.find(`.${styles.container}`))
      .to.be.defined;
  })
  it('has an item for each place in the places prop', () => {
    expect(wrapper.find('Item').length)
      .to.equal(places.length);
  })
})
```

## <span id="list-component">Business Listing 组件</span>
`<Listing />` 组件的测试已经写好了，让我们来补充我们的组件，让测试通过。和 `<Sidebar />` 类似，有一个样式文件需要载入，并且需要包装一个 `<Item />` 组件。

也非常简单：

```javascript
import React, { PropTypes as T } from 'react'
import classnames from 'classnames'

import Item from './Item';
import styles from './styles.module.css'

export class Listing extends React.Component {
  render() {
    return (
      <div className={classnames(styles.container)}>
      {this.props.places.map(place => {
        return (
          <Item place={place}
                onClick={this.props.onClick}
                key={place.id} />
        )
      })}
      </div>
    )
  }
}

export default Listing
```

并且创建样式：

```css
.container {
  height: 100%;
  overflow: auto;
  padding-bottom: 60px;
  margin: 0;
}
```

组件中使用到了 `<Item />`， 所以我们也需要创建 `<Item />` 组件。
## <span id="item-component">Item 组件</span>

对于 `<Item />` 组件，我们期待它能够显示地点的名称，并且能够显示一个评分。当然，样式也是必不可少的。所以，在我们的 `src/components/Listing/Item.spec.js` 测试文件中：

```javascript
import React from 'react'
import { expect } from 'chai'
import { shallow } from 'enzyme'

import Item from './Item'
import styles from './styles.module.css'

describe('<Item />', () => {
  let wrapper;
  const place = {
    name: 'San Francisco'
  }
  beforeEach(() => {
    wrapper = shallow(<Item place={place} />)
  });

  it('contains a title component with yelp')
  it('wraps the component with an .item css class')
  it('contains a rating')
})
```

并且将测试内容填好：

```javascript
// ...
it('contains a title component with yelp', () => {
  expect(wrapper.find('h1').first().text())
    .to.equal(place.name)
});

it('wraps the component with an .item css class', () => {
  expect(wrapper.find(`.${styles.item}`))
    .to.have.length(1);
})

it('contains a rating', () => {
  expect(wrapper.find('Rating'))
    .to.be.defined;
});
```

显而易见，我们还会创建一个处理从google api 得到的关于地点评分信息的组件 `<Rating />`。但是，我们现在先让测试通过吧。

在 `src/components/Listing/Item.js` 中，我们的 `<Item />` 组件不用关心如何去得到一个地点的信息，这些信息都又上一个组件传递下来了。组件需要显示一个标题，显示一个评分。

```javascript
import React, { PropTypes as T } from 'react'
import classnames from 'classnames'

import Rating from 'components/Rating/Rating';
import styles from './styles.module.css'

export class Item extends React.Component {
  render() {
    const {place} = this.props;
    return (
      <div
        className={styles.item}>
          <h1 className={classnames(styles.title)}>{place.name}</h1>
          <span>{place.rating/5}</span>
      </div>
    )
  }
}

export default Item
```

{% asset_img sidebar-listing-number-rating.jpg %}
<br />

为了能够对 `<Item />` 组件添加样式，让我们增加一个 `.item` 类吧。

```css
/* ... */
.item {
  display: flex;
  flex-direction: row;
  border-bottom: 1px solid #eeeeee;
  padding: 10px;
  text-decoration: none;

  h1 {
    flex: 2;
    &:hover {
      color: $highlight;
    }
  }

  .rating {
    text-align: right;
    flex: 1;
  }

  &:last-child {
    border-bottom: none;
  }
}
```

好了，回到我们的浏览器，你可以看到：

{% asset_img sidebar-listing-number-rating-style.jpg %}
<br />

## <span id="rating-component">Rating 组件</span>
让我们使评分更加的漂亮一些，使用星星来代替数值的显示。我们准备把这个组件放在 `src/components/` 目录下面，让我们来创建必要文件吧:

```bash
$ mkdir src/components/Rating
$ touch src/components/Rating/{Rating.js,styles.module.css}
$ touch src/components/Rating/Rating.spec.js
```

添加测试：

```javascript
// ...
it('fills the percentage as style', () => {
  let wrapper = shallow(<Rating percentage={0.10} />)
  expect(wrapper.find(`.${styles.top}`))
    .to.have.style('width', '10%');

  wrapper = shallow(<Rating percentage={0.99} />)
  expect(wrapper.find(`.${styles.top}`))
    .to.have.style('width', '99%')

  let rating = 4;
  wrapper = shallow(<Rating percentage={rating/5} />)
  expect(wrapper.find(`.${styles.top}`))
      .to.have.style('width', '90%')
});

it('renders bottom and top star meters', () => {
  let wrapper = shallow(<Rating percentage={0.99} />)
  expect(wrapper.find(`.${styles.top}`)).to.be.present;
  expect(wrapper.find(`.${styles.bottom}`)).to.be.present;
})
```

根据测试，创建我们的组件，在文件夹 `src/components/Rating/Rating.js` 中：

```javascript
import React, { PropTypes as T } from 'react'
import styles from './styles.module.css';

const RatingIcon = (props) => (<span>★</span>)

export class Rating extends React.Component {
  render() {
    // ...
  }
}

export default Rating
```

> `<RatingIcon>` 组件不需要依赖任何数据的注入，仅仅是显示一个 `*`

用样式来控制显示 `*` 的个数。

```javascript
export class Rating extends React.Component {
  render() {
    const {percentage} = this.props;
    const style = {
      width: `${(percentage || 0) * 100}%`
    }
    return (
      <div className={styles.sprite}>
        <div className={styles.top} style={style}>
            <RatingIcon />
            <RatingIcon />
            <RatingIcon />
            <RatingIcon />
            <RatingIcon />
        </div>
        <div className={styles.bottom}>
          <RatingIcon />
          <RatingIcon />
          <RatingIcon />
          <RatingIcon />
          <RatingIcon />
        </div>
      </div>
    )
  }
}
```

如果没有添加样式，看起来就不像一个评分了。

{% asset_img sidebar-listing-number-rating-style-one.jpg %}
<br />

让我们来添加样式，分离底层和顶层的显示


```css
.sprite {
  unicode-bidi: bidi-override;
  color: #404040;
  font-size: 25px;
  height: 25px;
  width: 100px;
  margin: 0 auto;
  position: relative;
  padding: 0;
  text-shadow: 0px 1px 0 var(--light-gray);
}

.top {
  color: #48b5e9;
  padding: 0;
  position: absolute;
  z-index: 1;
  display: block;
  top: 0;
  left: 0;
  overflow: hidden;
}

.bottom {
  padding: 0;
  display: block;
  z-index: 0;
  color: #a2a2a2;
}
```

在继续前进之前，让我们确保我们将颜色都变成都变量。这样的话，我们可以保证，在我们的整个项目中，所有的颜色都能够保持一致。创建一个 `src/styles/colors.css`
文件来保存所有的这些颜色变量。

在 `src/styles/colors.css`, 

```css
:root {
  --dark: #404040;
  --light-gray: #a2a2a2;
  --white: #ffffff;
  --highlight: #48b5e9;
  --heading-color: var(--highlight);
}
```

更改 `<Rating />` 组件的内容：

```css
@import "../../styles/colors.css";

.sprite {
  unicode-bidi: bidi-override;
  color: var(--dark);
  font-size: 25px;
  height: 25px;
  width: 100px;
  margin: 0 auto;
  position: relative;
  padding: 0;
  text-shadow: 0px 1px 0 var(--light-gray);
}

.top {
  color: var(--highlight);
  padding: 0;
  position: absolute;
  z-index: 1;
  display: block;
  top: 0;
  left: 0;
  overflow: hidden;
}

.bottom {
  padding: 0;
  display: block;
  z-index: 0;
  color: var(--light-gray);
}

```

{% asset_img sidebar-listing-number-rating-style-two.jgp %}
<br />

现在，我们的 `<Sidebar />` 总算完成了！ 

# <span id="main-pane">创建地图主页</span>
<br />
我们的 `<Sidebar />`
组件实现了,现在让我们来实现我们的主要元素吧，就是我们的地图和地图的详细信息。因为，我们希望这些页面都是可以被点击的，也就是说，我们希望用户可以复制和粘贴URL地址。所以，我们会根据URL来建设我们的主页。

我们需要修改我们的路由，使得它使用这些地图元素的跳转。目前，我们的路由只是设置了一个单个路由，显示一个 `<Container />`
组件。让我们修改我们的路由，让它也可以对 `Map` 组件做一些处理。

作为对照，我们目前的路由文件是这样的：

```javascript
import React from 'react'
import {Route} from 'react-router'
import Container from './Container'

export const makeMainRoutes = () => {

  return (
    <Route path="" component={Container} />
  )
}

export default makeMainRoutes;
```

让我们修改 `makeMatinRoutes` 方法，让它可以包含一个子路由。

```javascript
export const makeMainRoutes = () => {

  return (
    <Route path="" component={Container}>
      {/* child routes in here */}
    </Route>
  )
}
```

再把 `<Map />` 组件作为容器加进来：

```javascript
import Map from './Map/Map'
export const makeMainRoutes = () => {

  return (
    <Route path="" component={Container}>
      <Route path="map" component={Map} />
    </Route>
  )
}
```

在浏览器中加载新的路由，我们看不到任何东西，除非我们进入 `/map`
中，并且实现我们的组件。为了简便起见，我们先创建一个简单的组件来确保我们的路由是能够正常工作的。

就像我们做过很多次的一样，创建js文件，测试文件，模块演示文件。

```bash
$ mkdir src/views/Main/Map
$ touch src/views/Main/Map/{styles.module.css,Map.js}
```

创建一个带有静态文字的简单组件：

```javascript
import React, { PropTypes as T } from 'react'
import classnames from 'classnames'

import styles from './styles.module.css'

export class MapComponent extends React.Component {
  render() {
    return (
      <div className={styles.map}>
        MAP!
      </div>
    )
  }
}

export default MapComponent
```

回到浏览器，我们可以看到。。。等等，还是空白的，为什么呢？我们忘记告诉 `<Container />` 组件，什么时候，如何去渲染子路由。那么，我们需要告诉这个组件我们的期望!

React 推荐的方式来达到这个目的是采用 `children` 属性。我们将会使用这个属性，来告诉容器，我们想显示什么样的子路由。

为了使用children属性，我们需要对这个组件做一些修改：

```javascript
export class Container extends React.Component {
  // ...
  render() {
    return (
        <Map
          visible={false}
          className={styles.wrapper}>
          <Header />
          <Sidebar />
          <div className={styles.content}>
            {/* Setting children routes to be rendered*/}
            {this.props.children}
          </div>
        </Map>
      </div>
    )
  }
}
```

这样的话，我们再次刷新浏览器，可以看到效果啦！

{% asset_img map-content-block.jpg %}
<br />
在外层组件中，已经成功的加载了 `<Map />`
组件，我们就可以处理从google得到的关联关系转变成一个地图的实例。我们可以将这个关联关系作为一个children属性，传递下去，克隆一份children属性，并且创建一个新的。

使用 `React.cloneElement()` 方法，可以使得上面所说的方式变得非常简单。

```javascript
export class Container extends React.Component {
  // ...
  render() {
    let children = null;
    if (this.props.children) {
      // We have children in the Container component
      children = this.props.children;
    }
    return (
      {/* shortened for simplicity */}
      <div className={styles.content}>
        {/* Setting children routes to be rendered*/}
        {children}
      </div>
    )
  }
}
```

加上google信息，可能children：

```javascript
export class Container extends React.Component {
  // ...
  render() {
    let children = null;
    if (this.props.children) {
      // We have children in the Container component
      children = React.cloneElement(
        this.props.children,
        {
          google: this.props.google
        });
    }
    return (
      {/* shortened for simplicity */}
      <div className={styles.content}>
        {/* Setting children routes to be rendered*/}
        {children}
      </div>
    )
  }
}
```

现在，`<Container />` 组件的孩子们可以接受到 `google` 的属性了。当然，我们也需要传递 `places`.

```javascript
export class Container extends React.Component {
  // ...
  render() {
    let children = null;
    if (this.props.children) {
      // We have children in the Container component
      children = React.cloneElement(
        this.props.children,
        {
          google: this.props.google,
          places: this.state.places,
          loaded: this.props.loaded
        });
    }
    return (
      {/* shortened for simplicity */}
      <div className={styles.content}>
        {/* Setting children routes to be rendered*/}
        {children}
      </div>
    )
  }
}
```

现在，让我们更新我们的 `<MapComponent />` 组件。

```javascript
import React, { PropTypes as T } from 'react'
import classnames from 'classnames'
import Map from 'google-maps-react'

import styles from './styles.module.css'

export class MapComponent extends React.Component {
  render() {
    return (
      <Map google={this.props.google}
            className={styles.map}
            >
      </Map>
    )
  }
}

export default MapComponent
```

`<MapComponent>` 组件能够和我们预期的一样工作了。

## <span id="markers">创建地图标记</span>
让我们在我们的地图上做一些标记吧，我们可以将 `<Marker />` 作为地图组件的子组件渲染,并且可以采取和前面一样的策略。

```javascript
export class MapComponent extends React.Component {
  renderMarkers() {

  }
  render() {
    return (
      <Map google={this.props.google}
            className={styles.map}>
        {this.renderMarkers()}
      </Map>
    )
  }
}
``` 

让我们从`google-maps-react ` 模块中引用 `<Marker />` 组件吧。

 ```javascript
import Map, { Maker } from 'google-maps-react'
```

现在，让我们完善 `renderMarkers()` 方法吧。

```javascript
export class MapComponent extends React.Component {
  renderMarkers() {
    if(!this.props.places){ renturn null; }
    return this.props.places.map(place =>{
      return <Marker key={place.id}
                name={place.id}
                place={place}
                position={place.geometry.location}
              />
    })
  }
  // ...
}
```

刷新浏览器，看看效果：

{% asset_img map-with-markers.jpg%}
<br />

现在我们为每一个地点在地图上做好了标记，下面，我们开始致力于添加更加详细的信息吧。

## <span id="component-children">更新所有 <mapcomponent> 子组件</mapcomponent></span>

因为我们不仅仅需要更新地图组件中的标记，而是要更新所有的子组件，所以，是时候对这些子组件的渲染方式做一个改进了。

让我们在 `<MpConponect />` 组件中创建一个 `renderChildren()` 方法, 来负责我们所有的子组件的更新和渲染。

```javascript
export class MapComponent extends React.Component {
  renderChildren() {
    const {children} = this.props;
    // ...
  }
  renderMarkers() {
    // ...
  }
  render() {
    return (
      <Map google={this.props.google}
            className={styles.map}>
        {this.renderChildren()}
      </Map>
    )
  }
}
```

## <span id="click-markers">点击标记</span>

我们可以监听每一个标记的点击事件，来处理当用户点击了标记时更新我们的页面，跳转到一个显示地点详细信息的路由中去。

我们将我们的大部分逻辑都放在了 `<Container />`  组件中，而将 `<MapComponent />` 组件当做是一个无状态的组件使用。 所以，我们将点击事件的逻辑放到 `<Comtainer />`
组件中，并且以此来触发地图页面的更新。

就像我们可以将数据利用 `props` 属性传递一样，我们也能将方法的引用传递下去。让我们使用 `React.cloneElement()` 借口，并且将点击处理事件取名叫做 `onMarkerClick()`.

回到 `<Container />` 组件：

```javascript
export class Container extends React.Component {
  // ...
  onMarkerClick(item) {

  }

  render() {
    let children = null;
    if (this.props.children) {
      // We have children in the Container component
      children = React.cloneElement(
        this.props.children,
        {
          google: this.props.google,
          places: this.state.places,
          loaded: this.props.loaded,
          onMarkerClick: this.onMarkerClick.bind(this)
        });
    }
    // ...
  }
}
```

我们将会将这个方法绑定在 `<Marker />` 组件的 `onClick()` 事件上。

```javascript
export class MapComponent extends React.Component {
  renderMarkers() {
    return this.props.places.map(place =>{
      return <Marker key={place.id}
                name={place.id}
                place={place}
                onClick={this.props.onMarkerClick.bind(this)}
                position={place.geometry.location}
              />
    })
  }
  // ...
}
```

现在，每当一个标记被点击了，都会触发 `<Comtainer />` 组件中的 `onMarkerClick()` 方法。同样的，可以改变要传下来的地点信息。

```javascript
export class Container extends React.Component {
  // ...
  onMarkerClick(item) {
    const {place} = item; // place prop
  }
  // ...
}
```

当我们的用户点击标记，我们希望可以引导他们进入一个新的路由，详细信息路由。

```javascript
export class Container extends React.Component {
  // ...
  onMarkerClick(item) {
    const {place} = item; // place prop
    const {push} = this.context.router;
    push(`/map/detail/${place.place_id}`)
  }
}
Container.contextTypes = {
  router: React.PropTypes.object
}
```

这样的话，点击一个标记，会把用户跳转到一个新的路由 `/map/detail/${place.place_id}`

## <span id="add-details">为标记增加详细内容</span>

让我们来创建 `/detail/:placeId` 路由。当用户访问类似于 `/detail/abc123`
的地址是，我们希望给用户显示id是abc123的地点的详细信息。这种规则，可以让用户复制和粘贴这个地址，随时可以直接访问单独的详细地址页面。

先让我们创建新路由吧：

```javascript
export const makeMainRoutes = () => {

  return (
    <Route path="" component={Container}>
      <Route path="map" component={Map} />
      <Route path="detail/:placeId"
            component={Detail} />
    </Route>
  )
}
```

继续创建 `Detail` 组件。

```bash
$ mkdir src/views/Main/Detail
$ touch src/views/Main/Detail/{styles.module.css,Detail.js}
```

让我们创建一个API处理器，来获取地点的详细信息，在文件 `src/utils/googleApiHelpers.js` 中：

```javascript
export function getDetails(google, map, placeId) {
  return new Promise((resolve, reject) => {
    const service = new google.maps.places.PlacesService(map);
    const request = {placeId}

    service.getDetails(request, (place, status) => {
      if (status !== google.maps.places.PlacesServiceStatus.OK) {
        return reject(status);
      } else {
        resolve(place);
      }
    })
  })
}
```

让我们开始建立详细信息组件吧，并且确保引用了刚刚建立的新的帮助方法：

```javascript
import React, { PropTypes as T } from 'react'
import {getDetails} from 'utils/googleApiHelpers'
import styles from './styles.module.css'

export class Detail extends React.Component {
  constructor(props, context) {
    super(props, context)

    this.state = {
      loading: true,
      place: {},
      location: {}
    }
  }
  componentDidMount() {
    if (this.props.map) {
      this.getDetails(this.props.map);
    }
  }
  componentDidUpdate(prevProps) {
    if (this.props.map &&  // make sure we have a map
      (prevProps.map !== this.props.map ||
      prevProps.params.placeId !== this.props.params.placeId)) {
        this.getDetails(this.props.map);
    }
  }
  getDetails(map) {}
  // ...
  render() {
    if (this.state.loading) {
      return (<div className={styles.wrapper})>
                Loading...
              </div>);
    }
    // We're no longer loading when we get here
    const {place} = this.state;
    return (
      <div className={styles.wrapper}>
        <h2>{place.name}</h2>
      </div>
    )
  }
}

export default Detail
```

我们添加了 `componentDidMount()` 以及 `componentDidUpdate()` 方法， 并且了增加了一个自己的属性，来帮助更新组件内容。

{% asset_img details-name.jpg %}

<br />

在继续前进之前，让我们给我们的 <Detail /> 组件添加一些样式吧。我们需要把 `<h2>` 放在一个叫做 `header` 的类里面，以便于维护页面的样式。

```javascript
export class Detail extends React.Component {
  // ...
  render() {
    if (this.state.loading) {
      return (<div className={styles.wrapper})>
                Loading...
              </div>);
    }
    // We're no longer loading when we get here
    const {place} = this.state;
    return (
      <div className={styles.wrapper}>
        <div className={styles.header}>
          <h2>{place.name}</h2>
        </div>
      </div>
    )
  }
}
```

回到 `src/views/Main/Detail/styles.module.css` 文件，添加 header 类：

```css
.header {
  padding: 0 25px;
  h2 {
    font-size: 1.5em;
  }
}
```

别忘了，我们可以使用相同的padding数值，所以，相比于直接写死在代码中，然我们引入我们的css变量文件,并且使用 `--padding` 变量。

```css
@import url("../../../styles/base.css");

.header {
  padding: 0 var(--padding);
  h2 {
    font-size: 1.5em;
  }
}
```

{% asset_img details-name-style.jpg %}
<br />

虽然看起来没有太多的提升，但是，至少，我们证明了我们的css模块在这边是工作的。

Google API 的返回类容中，包含了很多有趣的东西，比如说图片。让我们将他们显示在我们的页面中吧。
我们可以把 `photos` 加入到 `render()` 方法中。Google Api 并没有给我们返回图片的连接，所以，我们需要向google 请求这些图片的连接地址。非常幸运的是，Google JS SDK
给我们提供了一个方法，可是使我们得到图片的最大宽度和最大高度，我们将使用这个来生成URL。

我们建立一个图片的渲染方法来代替直接在render方法中添加,并且要考虑到有一些地点并没有图片。

```javascript
export class Detail extends React.Component {
  // ...
  renderPhotos(place) {
       if (!place.photos || place.photos.length == 0) return;
  }
  render() {
    // ...
    const {place} = this.state;
    return (
      <div className={styles.wrapper}>
        <div className={styles.header}>
          <h2>{place.name}</h2>
        </div>
        <div className={styles.details}>
          {this.renderPhotos(place)}
        </div>
      </div>
    )
  }
}
```

每一个地点，得到的都是一个图片数组，我们需要将他们都render在页面上：

```javascript 
export class Detail extends React.Component {
  // ...
  renderPhotos(place) {
    if (!place.photos || place.photos.length == 0) return;
    const cfg = {maxWidth: 100, maxHeight: 100}
    return (<div className={styles.photoStrip}>
      {place.photos.map(p => {
        const url = `${p.getUrl(cfg)}.png`
        return (<img key={url} src={url} />)
      })}
    </div>)
  }
}
```

刷新浏览器，可以看到：

{% asset_img details-photos-without-style.jpg %}
<br />

看起来不是很好，添加一些样式，让图片不转行吧：

```css 
.details {
  /* a little bit of padding */
  padding: 0 var(--padding);
  .photoStrip {
    flex: 1;
    display: flex;
    overflow: auto;
  }
}
```

{% asset_img details-photos-with-flex-style.jpg %}
<br />

让我们隐藏起那个下面的滚动条吧，添加 `::-webkit-scrollbar` :

```css 
.details {
  padding: 0 var(--padding);

  ::-webkit-scrollbar {
    width: 0px;
    background: transparent;
  }
  /* ... */
}
```

最后，让每个图片之间，添加一个写间距：

```css 
.details {
  /* a little bit of padding */
  padding: 0 var(--padding);
  .photoStrip {
    flex: 1;
    display: flex;
    overflow: auto;

    img {
      margin: 0 1px;
    }
  }
}
```

{% asset_img details-photos-with-flex-style-and-margin.jpg %}
<br />

## <span id="responsive">响应式布局</span>

在中屏以及大屏幕上，我们的引用看起来很不错，但是，如果在小屏幕上呢？

{% asset_img ugly-non-responsive-mobile.jpg %}
<br />

看起来就不好了，让我们着手添加一些响应式的布局吧。我们仍然希望能够在页面上显示地点列表以及附近的一些推荐。但是，当窗口比较小的时候，地点列表显示在下面，图片显示在上面会比较合理的。

我们将会是一个一些 media queries 属性来更改我们的样式：

```css
body { font-size: 18px; }
/* Media query for printing */
@media (print) {
  font-size: 12px;
}
/* ... */
```

在我们前面配置postcss的时候，我们使用了 *precss* 插件，可以帮助我们很轻松的添加 [postcss-custom-media](https://github.com/postcss/postcss-custom-media)插件到我们的代码中。这个插件允许我们定义一些 media queries 变量。

在移动端优先的设计中，我们应该首先让我们的样式满足移动端的渲染，再更具一些media queries 适应大屏幕。

  1. 设计和实现对移动端友好的样式。
  2. 再添加适应大屏幕的样式。


在这种思想下，我们将我们的主要页面作为页面内容的第一块，列表作为第二块来设计。

为了让我们的应用使用 Flexbox 的布局，让我们先了解一下Flexbox的其中三个知识点。想要更加详细的了解什么是flex，并且如何使用flex，可以参考Chris Coyier
所写的一遍[非常棒的指导](https://css-tricks.com/snippets/css/a-guide-to-flexbox/)，我们这边仅仅是为了能让我们的项目够用！

### <span id="flex">display: flex</span>

想要让浏览器知道，我们想要使用Flex 布局，我们需要给我们的父节点设置 `display: flex` 属性。

对于本项目来说，我们将要在入口页面中的 `wrapper` 类添加这个属性，在前面的文章中，我们已经设置好了。

### <span id="flex-direction">flex-direction</span>

`flex-direction` 属性将会告诉浏览器，我们想要如何显示我们的布局，可以使水平的也可以是垂直的。设置 `flex-direction: column`
属性，浏览器会将元素从上往下一个个渲染。因为我们希望我们的页面在移动端的时候，是垂直显示的，所以：

```css
/* In src/views/Main/styles.module.css */
.wrapper {
  overflow-y: scroll;
  display: flex;
  margin: 0;
  padding: 15px;

  height: 100vh;
  -webkit-box-orient: horizontal;
  -o-box-orient: horizontal;

  /* Added these rules */
  flex-direction: column;
  flex: 1;
}
/* ... */
```

{% asset_img flex-direction-column.jpg %}
<br />

刷新浏览器，我们可以看到，我们的布局从水平变成了垂直。 添加 `flex: 1` 可以均衡移动端页面的显示。

现在，如果我们回到桌面屏幕大小，我们会发现，垂直是不合时宜的，有点不好看。让我们添加第一个 media query 来修复这个问题。

首先，我们比较喜欢让他们自己定义自己的media变量。虽然可以直接写在 base.css 文件中，但是比较好的做法是，新建一个文件：

```bash
$ touch src/styles/queries.css
```

在这个文件中，让我们使用 `@custom-media` 来定义不同屏幕的样式：

```css
@custom-media --screen-phone (width <= 35.5em);
@custom-media --screen-phone-lg (width > 35.5em);
```

在文件 `src/views/Main/styles.module.css`

```css
/* In src/views/Main/styles.module.css */
.wrapper {
  overflow-y: scroll;
  display: flex;
  margin: 0;
  padding: 15px;

  height: 100vh;
  -webkit-box-orient: horizontal;
  -o-box-orient: horizontal;

  flex-direction: column;
  flex: 1;

  @media (--screen-phone-lg) {
    /* applied when the screen is larger */
    flex-direction: row;
  }
}
/* ... */
```

{% asset_img flex-direction-lg.jpg %}

<br />
好了，现在不管是大屏幕还是小屏幕，都能比较友好的显示啦！

### <span id="order">order</span>

Flexbox 也允许我们设置区块的排序方式，比如现在， `content` 和 `sidebar`  区块都被设置为了顺序是1
的优先级，所以，先显示了content区块，因为它先被定义。为了手动修改显示的顺序，我们可以给样式添加 `order` 属性。

```css
/* In src/views/Main/styles.module.css */
.wrapper {
  overflow-y: scroll;
  display: flex;
  margin: 0;
  padding: 15px;

  height: 100vh;
  -webkit-box-orient: horizontal;
  -o-box-orient: horizontal;

  flex-direction: column;
  flex: 1;

  @media (--screen-phone-lg) {
    /* applied when the screen is larger */
    flex-direction: column;
  }
}
.content {
  position: relative;
  top: var(--topbar-height);
  left: 0;

  flex: 1;
  order: 1;

  @media (--screen-phone-lg) {
    flex: 2;
    order: 2;
  }
}
/* ... */
```

对于 `sidebar` 区块，让我们采取相同的方式设置吧：

```css
@import url("../../styles/base.css");
@import url("../../styles/queries.css");

.sidebar {
  /* ... */

  flex-direction: column;
  order: 2;
  flex: 1;

  @media (--screen-phone-lg) {
    display: block;
    flex-direction: row;
    order: 1;
  }

  .heading {
    /* ... */
  }
}
```

现在再回到浏览器，刷新页面，我们可以看到，不管是大屏幕还是小屏幕，都看起来非常好看了。

# <span id="conclusion">总结</span>
我们创建了一个完整的React 应用,
添加了大量的路由，复杂的项目关联，甚至引入了响应式布局，这是一段漫长的旅程。

我们将代码放在的github上面，可以在这里获得 [fullstackreact/react-yelp-clone](https://github.com/fullstackreact/react-yelp-clone).

# 小光头总结

经历了长达大半个月的时间，终于完成了这篇博客的翻译，从这次经历中体会到：

  1. 并没有涵盖所有知识，Redux 等知识没有涉及。
  2. 自己理解与表达给他人，其中差了N行代码的距离，还需要非常多的练习
  3. 时间，时间，时间！
  4. 学习，学习，学习，感觉不知道的东西太多。

第一次翻译，肯定有非常非常多的不足，任何建议请留言或者联系我哦，不过，至少迈出了一步，加油，小光头！！！

>英文原文地址： <https://www.fullstackreact.com/articles/react-tutorial-cloning-yelp/>

