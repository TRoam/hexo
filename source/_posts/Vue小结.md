---
title: Vue小结
tags:
  - JavaScript
  - Vue
  - 前端
abbrlink: fb918704
date: 2016-11-24 18:40:51
---

试着用Vue做了一个小东西，总结一下，很多都是官网有的，只是记录下了作为一个学习笔记吧。

## Vuejs 组件

组件的使用，需要先注册再使用。

```
Vue.component('componentName',{ /*component*/ })；
```

```
Vue.component('mine',{
           template:'#mineTpl',
           props:['name','title','city','content']
        });

 var v=new Vue({
      el:'#vueInstance',
      data:{
          name:'zhang',
          title:'this is title',
         city:'Beijing',
         content:'these are some desc about Blog'
     }
});
```

## 指令

指令是指带有v-前缀的特殊属性，当表达式的值改变时，将其产生的连带影响，响应式的作用于DOM，指令可以有参数（指令只有以冒号表示）和修饰符（以.修饰）

```
var myHeader = {
    template: "<p v-html = 'test' v-on:keydown.enter = ''><my-header-child></my-header-child></p>",
    components:{
        "my-header-child":myHeaderChild
    }
}
```

<!--more-->

## 指令keep-alive

如果把切换出去的组件保留在内存中，可以保留它的状态或避免重新渲染。为此可以添加一个keep-alive指令

```
<component :is='curremtView' keep-alive></component>
```

## 属性

### 计算属性

computed计算属性 选项会被缓存
也可以通过调用方法来计算属性，使得每次的属性都是重新调用生成的
watch–监听属性变化

```
<input type = "text" v-model = "myVal">
{{ myValueWithoutNum }}
{{ getMyValWithoutNum() }}
export default {
    data () {
        return {
            myVal:''
        }
    },
    watch:{
        myVal:function(val,oldVal) {
            console.log(val,oldVal);
        }
    },
    computed:{
        myValueWithoutNum () {
            return this.myVal.replace(/\d/g,'');//删掉所有数字
        }
    },
    methods:{
        getMyValWithoutNum (){
            return this.myVal.replace(/\d/g,'');//删掉所有数字
        }
    }
}
```

### 事件绑定

```
<button @click="addItem">addItem</button>
<button @click="toogle">toogle</button>
export default {
    data () {
        return {
            hello:'<span>hello world</span>',
            link:'http://www.baidu.com',
            className:['red-font','big-font'],
            hasError:false,
            classA:'hello',
            classB:'world',
            isPartA:true,
            list:[
                {
                    name: 'apple',
                    price: 34
                },
                {
                    name: 'banana',
                    price: 34
                },
            ]
        }
    },
    methods:{
        addItem () {//es6缩写，原为：addItem:function(){}
            Vue.set(this.list,1,{
                name:'pinaapple',
                price:231
            })
        },
        toggle () {
            this.isPartA = !this.isPartA
        }
    }
}
```

## css只在当前组件中起作用

在每一个vue组件中都可以定义各自的css，js，如果希望组件内写的css只对当前组件起作用，只需要在style中写入scoped，即

```
<style scoped></style>
```

## vuejs循环插入图片

```
<div class="bio-slide" v-for="item in items">   
    <img v-bind:src="item.image">
</div>
```

## vuejs中过渡动画

```
.zoom-transition {
        width:60%;
        height:auto;
        position: absolute;
        left:50%;
        top:50%;
        transform: translate(-50%,-50%);
        -webkit-transition: all .3s ease;
        transition: all .3s ease;
    }
.zoom-enter, .zoom-leave {
    width:150px;
    height:auto;
    position: absolute;
    left:20px;
    top:20px;
    transform: translate(0,0);
}

```

就这样吧，有时间把Vuex Vue Router 一起写一篇详细的。