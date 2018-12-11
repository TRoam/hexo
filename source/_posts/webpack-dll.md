---
title: webpack-dll(五) --- DllPlugin处理外部依赖
abbrlink: 36cda913
date: 2018-12-02 15:40:04
tags:
- webpack
- 前端
- 优化
---

我们可能已经遇到了这个问题，webpack已经区别出业务模块和公共模块的代码，为了利用浏览器缓存
我们也添加了hash，然而又有了这些问题： 

> * 每次打包，公共组件的hash都会变化，浏览器缓存形同虚设
> * 打包时间越来越长，特别是在多页面应用的项目中

当然劳动人民的智慧是无限的，为了优化这些问题，可以从这些方面着手

> * 公共模块等提出来单独打包，每次只打包业务模块
> * 将打包出来的公共模块作为外部依赖重新引入

<!-- more -->
于是有了webpack的[`DllPlugin`](https://webpack.docschina.org/plugins/dll-plugin/)，Dll这个概念应该是借鉴了Windows系统的dll。一个dll包，就是一个纯纯的依赖库，它本身不能运行，是用来给你的app引用的，打包dll的时候，Webpack会将所有包含的库做一个索引，写在一个manifest文件中，而引用dll的代码在打包的时候，只需要读取这个manifest文件，就可以了，这么一来好处可想而知。

> * Dll打包以后是独立存在的，只要其包含的库没有增减、升级，hash也不会变化，因此线上的dll代码不需要随着版本发布频繁更新。
> * App部分代码修改后，只需要编译app部分的代码，dll部分，只要包含的库没有增减、升级，就不需要重新打包。这样也大大提高了每次编译的速度。
> * 假设你有多个项目，使用了相同的一些依赖库，它们就可以共用一个dll。

### 增加第三方依赖配置文件

将需要单独打包为dll的依赖专门列出来，在`vendor.js`中，如果不同环境，如dev prod需要不同的配置，那么也可以分开配置

```js
module.exports = [
  'react',
  'react-dom',
  'lodash',
  'antd',
  'crypto-js',
  'moment',
  'fetch-mock',
  'url',
  'qs',
  'postal',
  'rc-calendar',
  'rc-pagination',
  'react-error-overlay',
  'regenerator-runtime'
];
```

### 添加webpack dll配置文件

引入`vendor`， 并且将他们打包成一个单独的文件，当然生产的话别忘记了压缩和混淆。

```js
const vendors = require('./vendors');
const ROOT_PATH = path.resolve(__dirname);

const webpackConfig = {
  entry: {
    vendors: vendors
  },
  output: {
    path: path.resolve(ROOT_PATH, '../dll/prod'),
    filename: 'vendors_[hash:8].js',
    library: 'vendors_[hash:8]'
  },
  plugins: [
    new webpack.DefinePlugin({
      'process.env': {
        NODE_ENV: JSON.stringify('production')
      }
    }),
    new webpack.DllPlugin({
      path: path.resolve(ROOT_PATH, '../dll/prod/vendors-manifest.json'),
      name: 'vendors_[hash:8]',
      context: __dirname
    }),
    new UglifyJsPlugin({
      parallel: true,
      uglifyOptions: {
        compress: {
          warnings: false,
          comparisons: false
        },
        mangle: {
          safari10: true
        },
        output: {
          comments: false,
          ascii_only: true
        }
      },
      sourceMap: false
    })
  ]
};

module.exports = webpackConfig;
```

运行webpack，对它进行打包，可以看到，生成了两个文件,一个是vendor.js，一个就是manifest.json。
Webpack将每个库都进行了编号索引，之后的dll使用者可以读取这个文件，直接用id来引用。

### dll 使用者webpack配置

```js
  plugins: [
    new webpack.DllReferencePlugin({
      context: __dirname,
      manifest: require('../dll/prod/vendors-manifest.json'),
    }),
  ]
  // DllReferencePlugin的选项中，context需要跟之前保持一致，这个用来指导Webpack匹配manifest中库的路径；manifest用来引入刚才输出的manifest文件
```

再次运行，明显感觉到，不仅速度快了，每个文件的体积也变小了，大功告成！！！

然而，每次运行都需要打包命令两次，如何继承到同样的一条命令呢？

>* [Webpack优化系列(一) -- 性能分析可视化](/post/c3fa870e.html)
* [Webpack优化系列(二) -- Js&css模块分离](/post/3af31a87.html)
* [Webpack优化系列(三) --- 公共模块与业务模块隔离](/post/1092a999.html)
* [Webpack优化系列(四) --- 减肥:压缩和混淆代码](/post/1092a999.html)
* [Webpack-Dll(五) --- DllPlugin处理外部依赖](/post/36cda913.html)