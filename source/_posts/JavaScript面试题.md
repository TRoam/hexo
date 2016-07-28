---
title: JavaScript面试题
date: 2016-05-10 01:14:34
tags:
- JavaScript
- Web
---
## 前言
看到一个比较涉及知识面较广的一个面试题，在这里给大家分享一下。
所检测的都是JS中比较常见却很容易混淆的知识点，包括：
- 变量作用域
- 变量声明提升
- `this`关键字
- 运算符优先级

## 问题
``` javascript
function Foo() {
    getName = function () { console.log (1); };
    return this;
}
Foo.getName = function () { console.log (2);};
Foo.prototype.getName = function () { console.log (3);};
var getName = function () { console.log (4);};
function getName() { console.log (5);}

//请写出以下输出结果：
Foo.getName();
getName();
Foo().getName();
getName();
new Foo.getName();
new Foo().getName();
new new Foo().getName();
```

<!--more-->

## 答案
```javascript
Foo.getName();//2
getName();//4
Foo().getName();//1
getName();//1
new Foo.getName();//2
new Foo().getName();//3
new new Foo().getName();//3
```

## 问题一
### JavaScript Scoping and Hoisting(变量作用域和声明提升)

```javascript
var foo = 1;
function bar() {
    if (!foo) {
        var foo = 10;
    }
    console.log(foo);
}
bar();
```


```javascript
var a = 1;
function b() {
    a = 10;
    return;
    function a() {}
}
b();
console.log(a);
```

```c
#include <stdio.h>
int main() {
    int x = 1;
    printf("%d, ", x); // 1
    if (1) {
        int x = 2;
        printf("%d, ", x); // 2
    }
    printf("%d\n", x); // 1
}
```
程序输出结果是1, 2, 1。因为C风格的语言有块级作用域（block-level scope）。当函数鱼运行到 if 语句中时，当前作用域中的新变量会被声明，并且不会影响到外部作用域。但在JavaScript中情况并不是这样：

```javascript
var x = 1;
console.log(x); // 1
if (true) {
    var x = 2;
    console.log(x); // 2
}
console.log(x); // 2
```

程序输出结果1, 2, 2。原因是JavaScript支持函数作用域（function-level scope)。if 语句中的代码块并不会创建新的作用域，只有函数才会。

如果你必须在函数中创建一个临时作用域，可以这么做：
```javascript
function foo() {
    var x = 1;
    if (x) {
        (function () {
            var x = 2;
            // some other code
        }());
    }
    // x is still 1.
}
```
<!--more-->


## Declarations, Names, and Hoisting（声明、名称以及变量声明提升/声明时机提升）

### 当访问函数内的变量时，JavaScript会按照下面顺序查找：
  - 语言级别：默认在所用作用域下会定义this、arguments
  - 传入参数：函数命名的参数，作用域是当前函数体
  - 函数声明：例如function foo() {}
  - 变量声明：例如var foo;

函数声明与变量声明经常被JavaScript引擎隐式地提升到当前作用域的顶部，也就是说：
```javascript
function foo() {
    bar();
    var x = 1;
}
```
实际上会被解释成：
```javascript
function foo() {
    var x;
    bar();
    x = 1;
}
```
也就是说，下面两种声明方式是等价的：
```javascript
function foo() {
    if (false) {
        var x = 1;
    }
    return;
    var y = 1;
}
```
```javascript
function foo() {
    var x, y;
    if (false) {
        x = 1;
    }
    return;
    y = 1;
}
```
可以发现，声明语句中的赋值部分并没有被提升声明，只有名称被提升了。两种函数声明方式：

```javascript
function test() {
    foo(); // TypeError "foo is not a function"
    bar(); // "this will run!"
    var foo = function () { // function expression assigned to local variable 'foo'
        console.log("this won't run!");
    }
    function bar() { // function declaration, given the name 'bar'
        console.log("this will run!");
    }
}
test();
```


### Name resolution order（名称解析顺序）

名称解析顺序有4步，一般来说，如果一个名称已经被定义了，它就不会被另一个具有同名称的属性所覆盖。这也就意味着，函数声明会比变量声明优先。并不是名称的赋值操作不会被执行，只是说声明部分被忽略了而已。有些例外：
  - 原生变量arguments特立独行，包含了传递到函数中的参数。如果自定义以arguments为命名的参数，将会阻止原生arguments对象的创建。所以勿使用arguments为名称的参数。
  - 胡乱使用this标识符会引起语法错误。
  - 如果多个参数具有相同的命名，那么最后一个参数会优先于先前的，即时这个参数未定义。


### Named Function Expressions（函数命名表达式）

你可以通过函数表达式给函数命名，语法上看起来像是函数声明，实则不是。
spam(); // ReferenceError "spam is not defined"

### How to Code With This Knowledge（如何编码）

切记，使用var表达式创建变量，在此强烈建议在代码块顶部使用一个var表达式来创建变量。然而，这么做的同时也导致很难对当前作用域下实际被声明的变量进行跟踪。我建议开发者使用JSLint来进行验证：
```javascript
/*jslint onevar: true [...] */
function foo(a, b, c) {
    var x = 1,
        bar,
        baz = "something";
}
```

## 问题二：

```javascript
function Foo() {
    getName = function () { console.log (1); };
    return this;
}
var getName;//只提升变量声明
function getName() { console.log (5);}//提升函数声明，覆盖var的声明

Foo.getName = function () { console.log (2);};
Foo.prototype.getName = function () { console.log (3);};
getName = function () { console.log (4);};//最终的赋值再次覆盖function getName声明

getName();//最终输出4
```
## 问题三、四

主要涉及到 作用域以及This指向的问题！

### 调用形式         this指向
  - 普通函数         全局对象window
  - 对象的方法    该对象
  - 构造函数         新构造的对象

### 普通函数调用
这是函数的最通常用法，属于全局性调用，因此this就代表全局对象Global
```javascript
function test(){
　　　　this.x = 1;
　　　　console.log(this.x);
　　}
　　test(); // 1

OR

var x = 1;
　　function test(){
　　　　console.log(this.x);
　　}
　　test(); // 1

OR

var x = 1;
　　function test(){
　　　　this.x = 0;
　　}
　　test();
　　console.log(x); //0
```

### 对象的成员方法
函数还可以作为某个对象的方法调用，这时this就指这个上级对象。

```javascript
function test(){
　　　　console.log(this.x);
}
　　var o = {};
　　o.x = 1;
　　o.m = test;
　　o.m(); // 1
```

### 作为构造函数调用
所谓构造函数，就是通过这个函数生成一个新对象（object）。这时，this就指这个新对象


```javascript
function test(){
　　　　this.x = 1;
　　}
　　var o = new test();
　　console.log(o.x); // 1

等价于

var x = 2;
　function test(){
　　　　this.x = 1;
 }
var o = new test();
console.log(x); //2
```

### apply 调用
apply()是函数对象的一个方法，它的作用是改变函数的调用对象，它的第一个参数就表示改变后的调用这个函数的对象。因此，this指的就是这第一个参数。
在Ember里边有等价的方法，bind ，jquery里面叫做 jquery.proxy（）

```javascript
   var x = 0;
　　function test(){
　　　　console.log(this.x);
　　}
　　var o={};
　　o.x = 1;
　　o.m = test;
　　o.m.apply(); //0
```
apply()的参数为空时，默认调用全局对象。因此，这时的运行结果为0，证明this指的是全局对象。
如果把最后一行代码修改为
`o.m.apply();//1`

## 问题五

js的运算符优先级问题

点（.）的优先级高于new操作，遂相当于是:

`new (Foo.getName)();`
所以实际上将getName函数作为了构造函数来执行，遂弹出2。

## 问题六-构造函数返回值

`new Foo().getName()` ，首先看运算符优先级括号高于new，实际执行为

`(new Foo()).getName()`
遂先执行Foo函数，而Foo此时作为构造函数却有返回值，所以这里需要说明下js中的构造函数返回值问题。

在传统语言中，构造函数不应该有返回值，实际执行的返回值就是此构造函数的实例化对象。
而在js中构造函数可以有返回值也可以没有。

1、没有返回值则按照其他语言一样返回实例化对象
2.若有返回值则检查其返回值是否为引用类型。如果是非引用类型，如基本类型（string,number,boolean,null,undefined）则与无返回值相同，实际返回其实例化对象。
3.若返回值是引用类型，则实际返回值为这个引用类型
```javascript
function F (){
    return {a:1}
}

new F(); // {a:1}
```

原题中，返回的是this，而this在构造函数中本来就代表当前实例化对象，遂最终Foo函数返回实例化对象。

之后调用实例化对象的getName函数，因为在Foo构造函数中没有为实例化对象添加任何属性，遂到当前对象的原型对象（prototype）中寻找getName，找到了。

遂最终输出3

## 问题七

第七问, new new Foo().getName(); 同样是运算符优先级问题。

最终实际执行为：
```
new ((new Foo()).getName)();
```
先初始化Foo的实例化对象，然后将其原型上的getName函数作为构造函数再次new。

遂最终结果为3
