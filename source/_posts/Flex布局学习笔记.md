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

## Flex简介

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

## 概念

Flex的核心概念就是`容器`和`轴`。容器包括外层的 父容器 和内层的 子容器，轴包括 主轴 和 交叉轴，可以说 flex 布局的全部特性都构建在这两个概念上。flex 布局涉及到 12 个 CSS 属性（不含 display: flex），其中父容器、子容器各 6 个。不过常用的属性只有 4 个，父容器、子容器各 2 个。

{% asset_img flexbox.png %}


容器默认存在两根轴：水平的主轴（main axis）和垂直的交叉轴（cross axis）。主轴的开始位置（与边框的交叉点）叫做main start，结束位置叫做main end；交叉轴的开始位置叫做cross start，结束位置叫做cross end.

## 属性

容器上有六个属性

```
flex-direction
flex-wrap
flex-flow
justify-content
align-items
align-content
```

### flex-direction

决定主轴 元素的排列方向

```
.container {
  flex-direction: row | row-reverse | column | column-reverse;
}
```

四个可能值分别是：
* row（默认值）：主轴为水平方向，起点在左端。
* row-reverse：主轴为水平方向，起点在右端。
* column：主轴为垂直方向，起点在上沿。
* column-reverse：主轴为垂直方向，起点在下沿。

### flex-wrap

此属性是定义在元素一行排不下的时候的行为。

```
.container {
  flex-wrap: nowrap | wrap | wrap-reverse;
}
```

三个可能值：
* nowrap（默认）：不换行。
* wrap：换行，向下拓展。
* wrap-reverse: 换行, 向上拓展。

### flex-flow

此属性是 `flex-direction` 和 `flex-wrap` 的简写形式，默认值是row nowrap

```
.container {
  flex-flow: <flex-direction> || <flex-wrap>;
}
```

### justify-content

定义了元素在主轴上的对齐方式

```
.container {
  justify-content: flex-start | flex-end | center | space-between | space-around;
}
```

五个可能值：

* flex-start（默认值）：左对齐
* flex-end：右对齐
* center： 居中
* space-between：两端对齐，项目之间的间隔都相等。
* space-around：每个项目两侧的间隔相等。所以，项目之间的间隔比项目与边框的间隔大一倍。

### align-items

定义了元素在交叉轴的对齐方式

```
.container {
  align-items: flex-start | flex-end | center | baseline | stretch;
}
```

五个可能值：

* flex-start：交叉轴的起点对齐。
* flex-end：交叉轴的终点对齐。
* center：交叉轴的中点对齐。
* baseline: 项目的第一行文字的基线对齐。
* stretch（默认值）：如果项目未设置高度或设为auto，将占满整个容器的高度。

### align-content

定义了多跟轴线的对其方式

```
.container {
  align-content: flex-start | flex-end | center | space-between | space-around | stretch;
}
```

可能有6个取值：

* flex-start：与交叉轴的起点对齐。
* flex-end：与交叉轴的终点对齐。
* center：与交叉轴的中点对齐。
* space-between：与交叉轴两端对齐，轴线之间的间隔平均分布。
* space-around：每根轴线两侧的间隔都相等。所以，轴线之间的间隔比轴线与边框的间隔大一倍。
* stretch（默认值）：轴线占满整个交叉轴。


## 元素自己的属性

元素上也有六个属性

```
order
flex-grow
flex-shrink
flex-basis
flex
align-self
```

### order

属性定义项目的排列顺序。数值越小，排列越靠前，默认为0

```
.item {
  order: <integer>;
}
```

### flex-grow

属性定义项目的放大比例，默认为0，即如果存在剩余空间，也不放大。

```
.item {
  flex-grow: <number>; /* default 0 */
}
```

如果所有项目的flex-grow属性都为1，则它们将等分剩余空间（如果有的话）。如果一个项目的flex-grow属性为2，其他项目都为1，则前者占据的剩余空间将比其他项多一倍。

### flex-shrink

属性定义了项目的缩小比例，默认为1，即如果空间不足，该项目将缩小

```
.item {
  flex-shrink: <number>; /* default 1 */
}
```

如果所有项目的flex-shrink属性都为1，当空间不足时，都将等比例缩小。如果一个项目的flex-shrink属性为0，其他项目都为1，则空间不足时，前者不缩小。

### flex-basis

属性定义了在分配多余空间之前，项目占据的主轴空间（main size）。浏览器根据这个属性，计算主轴是否有多余空间。它的默认值为auto，即项目的本来大小.


```
.item {
  flex-basis: <length> | auto; /* default auto */
}
```

它可以设为跟width或height属性一样的值（比如350px），则项目将占据固定空间

### flex

flex属性是flex-grow, flex-shrink 和 flex-basis的简写，默认值为0 1 auto。后两个属性可选

```
.item {
  flex: none | [ <'flex-grow'> <'flex-shrink'>? || <'flex-basis'> ]
}
```

该属性有两个快捷值：auto (1 1 auto) 和 none (0 0 auto)。

建议优先使用这个属性，而不是单独写三个分离的属性，因为浏览器会推算相关值

### align-self

属性允许单个项目有与其他项目不一样的对齐方式，可覆盖align-items属性。默认值为auto，表示继承父元素的align-items属性，如果没有父元素，则等同于stretch

```
.item {
  align-self: auto | flex-start | flex-end | center | baseline | stretch;
}
```

该属性可能取6个值，除了auto，其他都与align-items属性完全一致.