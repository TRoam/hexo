---
title: Webpack优化系列(三) --- 公共模块与业务模块隔离
abbrlink: 1092a999
date: 2018-12-01 13:55:12
tags:
- webpack
- 前端
- 优化
---

在我们实际的项目中，模块大致可以分为业务相关的模块，以及公共基础模块，比如第三方的依赖模块（React， lodash， echart）等。
并不会常常更新，而且相对来说体积都比较大。如果和业务代码一起打包，不容易利用缓存。每次更新都引起重新打包和下载。
如果能够把公用模块和业务模块分开打包，那么对于性能来说，会有不小的提升。

webpack的`CommonsChunkPlugin`插件帮我们完美的解决了这个问题。
<!-- more -->
### CommonsChunkPlugin

设置公共模块入口：

```JS
entry:{
    vendors:['react',
    'redux',
    'react-dom',
    'react-redux',
    'react-router',
    'antd/dist/antd.min.css',
    'lodash'],
    // other entries
}
```

利用`CommonsChunkPlugin`将公共模块过滤出来，并且打包成为一个单独的文件~

```js
plugins: [
    new webpack.optimize.CommonsChunkPlugin({
        name: 'vendors', // 入口名称
        filename: 'js/[name].js', // 输入文件名称
        warn:false
    })，
    new ExtractTextPlugin({
        filename:'css/[name].css',
        allChunks: true
    })
]
```

重新打包，就得到分离出来的两个不同的出口文件了，然而，打包时间和体积都不小，并且编译过后会重新打包，这个又改如何优化呢？
