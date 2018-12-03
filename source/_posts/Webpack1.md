---
title: Webpack优化系列 -- js&css模块分离
abbrlink: 3af31a87
date: 2018-10-27 10:53:40
tags:
- webpack
- 优化
- ExtractTextPlugin
- MiniCssExtractPlugin
---

Webpack将所有的静态资源都视为模块，比如JavaScript，scss，图片等，从而引入对应的loader去
加载相应的资源，并且处理成相应的模块。和大多数包管理器不一样的是，Webpack的加载器之间可以进行串联，一个加载器的输出可以成为另一个加载器的输入。

> 如下图，Less资源首先通过`less-loader`模块加载器加载为css资源，然后通过`css-loader`模块加载器转化为css模块，最后再更加`style-loader`编译转化为适合特定浏览器的最终可适用样式资源。

{% asset_img css-loader.png %}

<!-- more -->

## 常见loader

一般我们项目中，常用的一些模块加载器包括。

```bash
npm install file-loader css-loader style-loader sass-loader html-loader babel-loader url-loader --save-dev
```
在webpack中添加相关的配置: 

```js
{
test: /\.(js|mjs|jsx)$/,
enforce: 'pre',
use: [
    {
    options: {
        formatter: require.resolve('react-dev-utils/eslintFormatter'),
        eslintPath: require.resolve('eslint')
    },
    loader: require.resolve('eslint-loader')
    }
    ],
    include: paths.appSrc
},
{
    test: [/\.bmp$/, /\.gif$/, /\.jpe?g$/, /\.png$/],
    loader: require.resolve('url-loader'),
    options: {
        limit: 10000,
        name: 'static/media/[name].[hash:8].[ext]'
    }
    },
{
    // Exclude `js` files to keep "css" loader working as it injects
    // its runtime that would otherwise be processed through "file" loader.
    // Also exclude `html` and `json` extensions so they get processed
    // by webpacks internal loaders.
    exclude: [/\.(js|mjs|jsx|ts|tsx)$/, /\.html$/, /\.json$/],
    loader: require.resolve('file-loader'),
    options: {
        name: 'static/media/[name].[hash:8].[ext]'
    }
    }
// 其他规则类似，不在这一一列举
```

随后，使用webpack打包，再看输出的文件，只有一个js文件以及几个图片大小超过10kb的图片，并没有打包出独立的css文件，所以:

* webpack 会把所有的资源都糅合打包成一个js文件，图片如果小于一定大小，会转化为base64的url
* 如果内容比较多，打包出来的js文件可能会非常大。

当遇到大型项目的时候，这样做显然对性能会有一定的影响，那么如何优化呢？ 

## mini-css-extract-plugin 分离css静态资源

在`webpack < 4`版本中，使用[`extract-text-webpack-plugin`](https://github.com/webpack-contrib/extract-text-webpack-plugin), 4以上的版本，已经不推荐使用此插件处理css了。

> Since webpack v4 the extract-text-webpack-plugin should not be used for css. Use [mini-css-extract-plugin](https://github.com/webpack-contrib/mini-css-extract-plugin) instead.

安装

```bash
npm install --save-dev mini-css-extract-plugin
```

配置webpack, 最简单的例子：

```js
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
module.exports = {
  plugins: [
    new MiniCssExtractPlugin({
      filename: "[name].css",
      chunkFilename: "[id].css"
    })
  ],
  module: {
    rules: [
      {
        test: /\.css$/,
        use: [
          {
            loader: MiniCssExtractPlugin.loader,
            options: {
              // you can specify a publicPath here
              // by default it use publicPath in webpackOptions.output
              publicPath: '../'
            }
          },
          "css-loader"
        ]
      }
    ]
  }
}
```

需要区别是开发或者生产环境： 

```js
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const devMode = process.env.NODE_ENV !== 'production'

module.exports = {
  plugins: [
    new MiniCssExtractPlugin({
      // Options similar to the same options in webpackOptions.output
      // both options are optional
      filename: devMode ? '[name].css' : '[name].[hash].css',
      chunkFilename: devMode ? '[id].css' : '[id].[hash].css',
    })
  ],
  module: {
    rules: [
      {
        test: /\.(sa|sc|c)ss$/,
        use: [
          devMode ? 'style-loader' : MiniCssExtractPlugin.loader,
          'css-loader',
          'postcss-loader',
          'sass-loader',
        ],
      }
    ]
  }
}
```

在生产环境，对css文件进行压缩和乱化：

```js
minimizer: [
      new UglifyJsPlugin({
        cache: true,
        parallel: true,
        sourceMap: true // set to true if you want JS source maps
      }),
      new OptimizeCSSAssetsPlugin({})
    ]
```

当我们需要把所有的css都在一个文件时, 利用webpack splitChunks功能：

```js
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
module.exports = {
  optimization: {
    splitChunks: {
      cacheGroups: {
        styles: {
          name: 'styles',
          test: /\.css$/,
          chunks: 'all',
          enforce: true
        }
      }
    }
  },
  plugins: [
    new MiniCssExtractPlugin({
      filename: "[name].css",
    })
  ],
  module: {
    rules: [
      {
        test: /\.css$/,
        use: [
          MiniCssExtractPlugin.loader,
          "css-loader"
        ]
      }
    ]
  }
}
```

再次打包，会发现：

* css单独抽离，打包成单独的css文件
* html自动引用css文件
* 小于10k的图片，转成base64 格式的 dataUrl

## extract-text-webpack-plugin 分离css静态资源

现阶段，很多项目，还是使用的是webpack@3 的版本，所以要完成上面的步骤，还是使用`extract-text-webpack-plugin` 插件的。

安装插件：

```
npm install extract-text-webpack-plugin --save-dev
```

修改相关配置：

```js
var ExtractTextPlugin = require('extract-text-webpack-plugin');
var extractCSS = new ExtractTextPlugin('css/[name].css?[contenthash]')
var cssLoader = extractCSS.extract(['css'])
var sassLoader = extractCSS.extract(['css', 'sass'])

plugins.push(extractCSS);
......
//conf - module - loaders
{test: /\.css$/, loader: cssLoader},
{test: /\.scss$/, loader: sassLoader}
```

有写的不当之处，欢迎指正，谢谢~