---
title: React多页应用
date: 2018-10-21 10:49:13
tags:
  - JavaScript
  - React
  - 前端
  - webpack
---

### 前言

> 工作遇到这样的需求，相同的项目中，需要打包出多个单页应用，但是又希望能够在开发和维护中共享很多配置或者组件。
于是乎，使用 webpack 做了一些简单配置


项目 tree 结构大致如下：

{% asset_img we.png %}

预期目标是， 在`routes`目录下，每有一个文件夹，就代表一个独立的单页应用，也就是一个出口文件。

<!-- more -->

### 更改 webpack 配置

获取 routes 列表

```JavaScript
const path = require('path');
const fs = require('fs');

const folderPath = path.resolve(fs.realpathSync(process.cwd()), 'src/routes');
const getEntities = () => {
  const entries = {};
  const plugins;
  fs.readdirSync(folderPath).forEach((entry) => {
    const currentPath = `${folderPath}/${entry}`;
    const cFolder = fs.statSync(currentPath);
    if (cFolder.isDirectory()) {
      // some other logic
    }
  });

  return { entries, plugins };
}
```

添加entry， 也就是在上面code other logic里面, 把每个路由左右一个独立的入口文件。

```js
entires[entry] = [
          '${currentPath}/index.js'
      ];
```

借助 `webpack-html-plugin` 生成网页文件

```js
plugins.push(
          new HtmlWebpackPlugin({
            inject: true,
            template: paths.appHtml,
            chunks: [entry],
            filename: `${entry}.html`
      }))
```

这样，准备工作就做好了，下面就需要让webpack知道我们上面所做的配置。
修改 webpack 入口：

```javascript

const { entries, plugins } = getEntities();

module.exports = {
  // other code
  entry: entries
  // other code
};
```

将plugins加入到webpack的plugins里面：

```js
module.exports = {
  // other code
  plugins: [
      ...plugins
  ]
  // other code
};
```

重新build，在看看build文件夹，是不是就按照预想的输入呢？

> 至此算是大功告成，但是这样的话，就会发现，每次更新的时候，速度变慢了很多。
这当然是情有可原的，毕竟之前只要打包一个出口文件，现在所有的东西，都是指数增长的，那么我们有什么办法可以提升打包和加载速度吗？
我们相信，webpack是异常强大的，至于如何做，在下一篇博客文章中，有详细介绍~
