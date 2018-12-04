---
title: Webpack优化系列 -- 性能分析可视化
abbrlink: c3fa870e
date: 2018-10-26 15:28:28
tags:
- webpack-bundle-analyzer
- webpack
- 优化
---

{% asset_img ana.png %}

最近觉得项目的打包速度异常的慢，于是利用webpack插件`webpack-bundle-analyzer`查看打包出来的各个模块的体积已经路径，寻找优化的方向，这里做简单的总结：

<!-- more -->
### 安装 

```
npm install --save-dev webpack-bundle-analyzer
```

### 配置

webpack配置文件，添加环境变量判断，只有`BUILD_ANALYSIS=true`的时候：

```js
const runReport = process.env.BUILD_ANALYSIS === 'true';
```

将插件加入配置中： 

```js
if (runReport) {
  const BundleAnalyzerPlugin = require('webpack-bundle-analyzer').BundleAnalyzerPlugin;
  webpackConfigOptions.plugins.push(new BundleAnalyzerPlugin());
}
```

### 执行查看分析

在命令行执行命令：

```
BUILD_ANALYSIS=true npm run build 
```

build截图，就可以看到我们最开始的那个分析网页了，可以点击查看具体的信息。

在`package.json`加入这个命令持久化： 

```js
"scripts": {
    "start": "node scripts/start.js",
    "build": "node scripts/build.js",
    "analysis": "BUILD_ANALYSIS=true npm run build"
  }
```

再次运行，就只需要： 

```
npm run analysis
```

### 更多设置

可以在插件中，添加自定义设置。
```js
new BundleAnalyzerPlugin({
  //  可以是`server`，`static`或`disabled`。
  //  在`server`模式下，分析器将启动HTTP服务器来显示软件包报告。
  //  在“静态”模式下，会生成带有报告的单个HTML文件。
  //  在`disabled`模式下，你可以使用这个插件来将`generateStatsFile`设置为`true`来生成Webpack Stats JSON文件。
  analyzerMode: 'server',
  //  将在“服务器”模式下使用的主机启动HTTP服务器。
  analyzerHost: '127.0.0.1',
  //  将在“服务器”模式下使用的端口启动HTTP服务器。
  analyzerPort: 8888, 
  //  路径捆绑，将在`static`模式下生成的报告文件。
  //  相对于捆绑输出目录。
  reportFilename: 'report.html',
  //  模块大小默认显示在报告中。
  //  应该是`stat`，`parsed`或者`gzip`中的一个。
  //  有关更多信息，请参见“定义”一节。
  defaultSizes: 'parsed',
  //  在默认浏览器中自动打开报告
  openAnalyzer: true,
  //  如果为true，则Webpack Stats JSON文件将在bundle输出目录中生成
  generateStatsFile: false, 
  //  如果`generateStatsFile`为`true`，将会生成Webpack Stats JSON文件的名字。
  //  相对于捆绑输出目录。
  statsFilename: 'stats.json',
  //  stats.toJson（）方法的选项。
  //  例如，您可以使用`source：false`选项排除统计文件中模块的来源。
  //  在这里查看更多选项：https：  //github.com/webpack/webpack/blob/webpack-1/lib/Stats.js#L21
  statsOptions: null,
  logLevel: 'info' 日志级别。可以是'信息'，'警告'，'错误'或'沉默'。
})
```

参考：[webpack-bundle-analyzer](https://github.com/webpack-contrib/webpack-bundle-analyzer)