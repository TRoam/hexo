---
title: Flex布局学习笔记
date: 2017-04-09 15:51:56
tags:
- Css
- Web
---

布局一直是web页面中的重要话题，以前最常见的就是盒子模型的布局，再加上 `position` 以及 `float` 属性来完成基本的页面布局。当然我们用的最多的，还是由`Bootstrap`封装过的栅格流水式布局，例如：
```CSS
<div class="row">
  <div class="col-md-8">.col-md-8</div>
  <div class="col-md-4">.col-md-4</div>
</div>
<div class="row">
  <div class="col-md-4">.col-md-4</div>
  <div class="col-md-4">.col-md-4</div>
  <div class="col-md-4">.col-md-4</div>
</div>
<div class="row">
  <div class="col-md-6">.col-md-6</div>
  <div class="col-md-6">.col-md-6</div>
</div>
```

但是，并不是每一个项目都需要`Bootstrap`, 而且其本身也存在不少的limitation，其实在2009年，W3C 提出了一种新的方案----Flex 布局，可以简便、完整、响应式地实现各种页面布局。目前，它已经得到了所有浏览器的支持。曾经大致了解过这么一种新的方案，但是并不曾深入，今天正好有机会再次温习和总结一下这种用法。

### Flex简介

Flex 指的是弹性布局，使用它会改变浏览器默认从左往右从上到下的元素平铺方式，提供更加灵活可控的页面布局方式。
任何一个容器或者元素都可以指定为flex布局。
```CSS
.container {
  display: flex;
}

.inline-element {
  display: inline-flex;
}
```

> 当然咯，指定为flex布局以后，子元素的 `float` `clear` `vertical-align` 属性将会失效。

### 概念

Flex的核心概念就是`容器`和`轴`。容器包括外层的 父容器 和内层的 子容器，轴包括 主轴 和 交叉轴，可以说 flex 布局的全部特性都构建在这两个概念上。flex 布局涉及到 12 个 CSS 属性（不含 display: flex），其中父容器、子容器各 6 个。不过常用的属性只有 4 个，父容器、子容器各 2 个。

{% asset_img flexbox.png %}


容器默认存在两根轴：水平的主轴（main axis）和垂直的交叉轴（cross axis）。主轴的开始位置（与边框的交叉点）叫做main start，结束位置叫做main end；交叉轴的开始位置叫做cross start，结束位置叫做cross end