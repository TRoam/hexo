---
title: Webpack优化系列(四) --- 减肥:压缩和混淆代码
abbrlink: aa6507f5
date: 2018-12-01 19:14:39
tags:
- webpack
- 前端
- 优化
---

前面通过使用`CommonsChunkPlugin`插件，将公共模块与业务模块分开处理，但是打包输入的文件任然体积比较大，。
浏览器从服务器访问网页时，需要下载这些源文件，文件越大传输时间就越长。 为了提升网页加速速度和减少网络传输流量， 可以对这些资源进行压缩和混淆。 

除了通过GZIP以外，还可以对文件本身进行优化，提升网络速度，并且由于压缩后的代码可读性非常差 就算别人下载到网页的代码，也大大增加了代码分析和改造的难度。

Webpack中最常用的压缩和混淆的js插件就是`UglifyJsPlugin`，对css使用的比较多的工具则是`cssnano`。

<!-- more -->
### `UglifyJsPlugin`压缩js代码

`UglifyJsPlugin`会分析JavaScript的代码语法树，理解代码含义，从而能做到诸如去掉无效代码，去掉日志输出代码，缩短变量名等优化

一般配置如下： 

```js
new webpack.optimize.UglifyJsPlugin({
      compress: {
        // 在UglifyJs删除没有用到的代码时不输出警告
        warnings: false,
        // 删除所有的 `console` 语句，可以兼容ie浏览器
        drop_console: true,
        // 内嵌定义了但是只用到一次的变量
        collapse_vars: true,
        // 提取出出现多次但是没有定义成变量去引用的静态值
        reduce_vars: true,
      },
      output: {
        // 最紧凑的输出
        beautify: false,
        // 删除所有的注释
        comments: false,
      }
    })
```


大概有以下常用配置项： 

* sourceMap：是否为压缩后的代码生成对用的SourceMap， 默认不生成，开启后耗时会大大增加。一般不会把压缩后的代码SouceMap发送给网站用户的浏览器，而是用于内部开发人员调试线上代码时使用。
* beautify：是否输出可读性较强的代码，会保留空格和制表符，默认为是，为了达到更好的压缩效果，可以设置为false。
* comments：是否保留代码中的注释， 默认保留， 为了达到压缩更好的压缩效果，可以设置为false。
* compress.warnings：是否在UglifyJS删除没有用到的代码时输出警告信息，默认为输出。可以设置为false以关闭这些不大的警告。
* drop_console：是否剔除代码中所有的console语句，默认不剔除，开启后不仅可以提升代压缩效果，也可以兼容不支持console语句IE浏览器。
* collapse_vars:是否内嵌定义了但是只永达一次的变量，例如把var x=5; y=x抓换成 y=5, 默认不转换。为了达到更好的压缩效果，可以设置为false。
* reduce_vars：是否提取出出现多次但是没有定义成变量去引用的静态值。

### `cssnano`压缩css

CSS同样可以进行瘦身和混淆，给予Postcss的css压缩工具`csssnano`能够理解css代码含义，去除不必要的规则等。
使用也是非常的简单，它已经在`css-loader`中内置了，只需要开启`minimize`选项，回顾前面对css优化的总结中，可以看到如下代码：

```js
module: {
    rules: [
      {
        test: /\.css/,// 增加对 CSS 文件的支持
        // 提取出 Chunk 中的 CSS 代码到单独的文件中
        use: ExtractTextPlugin.extract({
          // 通过 minimize 选项压缩 CSS 代码
          use: ['css-loader?minimize']
        }),
      },
    ]
  },
 plugins: [
    // ...
    new ExtractTextPlugin({
      filename: `[name]_[contenthash:8].css`,// 给输出的 CSS 文件名称加上 Hash 值
    })
    /// ...
  ],
```

至此，再看打包出来的文件，应该就达到预期了， 那么打包时间过长，每次开发都开始等的久了，并且每次打包hash都跟着变化，应该怎么优化呢?


>* [Webpack优化系列(一) -- 性能分析可视化](/post/c3fa870e.html)
* [Webpack优化系列(二) -- Js&css模块分离](/post/3af31a87.html)
* [Webpack优化系列(三) --- 公共模块与业务模块隔离](/post/1092a999.html)
* [Webpack优化系列(四) --- 减肥:压缩和混淆代码](/post/1092a999.html)
* [Webpack-Dll(五) --- DllPlugin处理外部依赖](/post/36cda913.html)