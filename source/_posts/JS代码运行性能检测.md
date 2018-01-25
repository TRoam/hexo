---
title: JS代码运行性能检测
date: 2017-01-28 14:59:31
tags:
- JavaScript
- Performance
- 性能
---

有时候需要检测一段代码的性能，怎么做呢？ 借用chrome检测可以帮忙检测。

### 启动chrome

通过命令行：
```
chrome –enable-memory-info 
```
启动chrome

### 创建一个HTML： 

```HTML
<script>  
var i = 0;  
setInterval(function(){  
    var before = window.performance.memory.usedJSHeapSize;  
    // Start  
    //这里输入运行的代码 
    // End  
    var diff = window.performance.memory.usedJSHeapSize - before;  
    console.log(diff);  
}, 100);  
</script>
```

### 结果：

通过以上的方式，可以得出运行的代码所分配的内存，特别是可以在循环中用上可以检查性能～！
