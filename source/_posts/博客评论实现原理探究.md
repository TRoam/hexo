---
title: 博客评论工具Gitment实现原理探究
date: 2018-02-08 15:46:38
tags:
- gitment
- comment
- OAuth
---

> 最近对博客又折腾了一轮，换了一个简洁一些的主题，并且对博客SEO和评论系统做了一些优化。 
  之前的使用的是[Disqus](https://disqus.com/)作为评论系统，但是由于大家都懂的原因,在墙内无法访问，总是造成页面的持续lodaing。 
  在多方面的对比下，选择了[Giement](https://github.com/imsun/gitment), 同时也对这个工具的实现做了一些研究。

具体的安装和使用方法，我就不在这里赘述了，请参考作者[Shiquan Sun](https://github.com/imsun)的[说明文档](https://imsun.net/posts/gitment-introduction/)。 
感谢作者的热心开发和共享，我主要从这些方面做了实现探究：

* 基本原理与思想
* 评论区域的渲染
* 用户登陆
* 初始化评论
* 数据以及状态管理(Bobx)
* 创建评论
* 自定义主题的支持
* 点赞/删除/预览等功能的实现

<!-- more -->

### 基本原理与思想

主要利用了Github的issues功能，把每一篇文章当做是一个open的issue，然后读者评论其实就是给
特定issue添加回复。当然这一切都是通过api来实现的，用户登录和认证则是通过Github的OAuth以及
相关接口来实现的。 这种对github的使用，可谓精妙绝伦！

### 评论区域的渲染

从使用方式中来看，在每个博客页面，添加如下代码。 

```JavaScript
<div id="container"></div>
<link rel="stylesheet" href="https://imsun.github.io/gitment/style/default.css">
<script src="https://imsun.github.io/gitment/dist/gitment.browser.js"></script>
<script>
var gitment = new Gitment({
  id: '页面 ID', // 可选。默认为 location.href
  owner: '你的 GitHub ID',
  repo: '存储评论的 repo',
  oauth: {
    client_id: '你的 client ID',
    client_secret: '你的 client secret',
  },
})
gitment.render('container')
```

除去初始化，填写owner、repo、oauth等信息不提，大概分成两步走。

1. 创建一个Id为`container`的容器。
2. 调用Gitment的`render`函数，并且将容器的ID告诉它。

那么，`render` 函数到底做了什么呢，可以先来看看源代码，在[默认Theme](https://github.com/imsun/gitment/blob/master/src/theme/default.js)文件

```JavaScript
function render(state, instance) {
  const container = document.createElement('div')
  container.lang = "en-US"
  container.className = 'gitment-container gitment-root-container'
  container.appendChild(instance.renderHeader(state, instance))
  container.appendChild(instance.renderComments(state, instance))
  container.appendChild(instance.renderEditor(state, instance))
  container.appendChild(instance.renderFooter(state, instance))
  return container
}

export default { render, renderHeader, renderComments, renderEditor, renderFooter }
```

暂时不去考虑这里的`Render`函数是如何加到Gitment Class的原型链上的，render大概做了这些事情：

{% asset_img 2018-02-09_14-23-04.png %}

具体的某一部分渲染，以render主题comments作为例子，详细看一下。

```JavaScript
function renderComments({ meta, comments, commentReactions, currentPage, user, error }, instance) {
  const container = document.createElement('div')
  //...
  comments.forEach(comment => {
    const createDate = new Date(comment.created_at)
    const updateDate = new Date(comment.updated_at)
    const commentItem = document.createElement('li')
    commentItem.className = 'gitment-comment'
    commentItem.innerHTML = `
      <a class="gitment-comment-avatar" href="${comment.user.html_url}" target="_blank">
        <img class="gitment-comment-avatar-img" src="${comment.user.avatar_url}"/>
      </a>
      <div class="gitment-comment-main">
        <div class="gitment-comment-header">
          <a class="gitment-comment-name" href="${comment.user.html_url}" target="_blank">
            ${comment.user.login}
          </a>
  // ...
     `
       container.appendChild(pagination)
    }
  }

  return container 
```

贴出了一部分代码，除去一些容错处理，大概就是:
1. 创建Root DOM 节点
2. 根据传入的评论数据，循环并创建相应的HTML文本，并且将内容Append到创建的DOM节点上。
3. 同时绑定相关事件，添加Like Vote等操作一系列其他操作
4. 绘制分页等
5. 再将创建的DOM 添加到Container上。 

其他几部分的绘制，思想和实现大同小异，不再更加详细的在这里记录了。

### 用户登录

先看看代码吧。

获取登陆的LINK
```JavaScript
get loginLink() {
    const oauthUri = 'https://github.com/login/oauth/authorize'
    const redirect_uri = this.oauth.redirect_uri || window.location.href

    const oauthParams = Object.assign({
      scope,
      redirect_uri,
    }, this.oauth)

    return `${oauthUri}${Query.stringify(oauthParams)}`
}
```

执行登陆

```JavaScript
login() {
  window.location.href = this.loginLink
}
```

获取用户信息

```JavaScript
if (!this.accessToken) {
  this.logout()
  return Promise.resolve({})
}

return http.get('/user')
  .then((user) => {
    this.state.user = user
    localStorage.setItem(LS_USER_KEY, JSON.stringify(user))
    return user
  })
```

基本就是利用OAuth，将Github作为IDP, 在GITHUB上注册的OAuth APP作为SP 的SSO了，具体相关内容不再这篇文章里面详述。
Gitment主要是将用户信息存入localstroage，再根据localstroy里面的信息去判断是否登录。

### 初始化评论

在每一篇文章中，都需要作者登陆自己的账户，然后实行Comment 初始化动作，这是为什么呢，这一步都做了什么呢？
Gitment的基本思想就是将每一篇文章作为一个issue，显而易见，当一篇新的博文上线了以后，在GITHUB的项目里面并没有这一条issue，
由于issue的权限控制，只能又拥有者去创建，所以，必须本人登陆自己的账号，去创建一条open的issue了，实现中主要是以下代码。

先尝试load和文章关联的issue，如果没有，则显示ERROR。
```JavaScript
  getIssue() {
    if (this.state.meta.id) return Promise.resolve(this.state.meta)

    return this.loadMeta()
  }

  loadMeta() {
  const { id, owner, repo } = this
  return http.get(`/repos/${owner}/${repo}/issues`, {
      creator: owner,
      labels: id,
    })
    .then(issues => {
      if (!issues.length) return Promise.reject(NOT_INITIALIZED_ERROR)
      this.state.meta = issues[0]
      return issues[0]
    })
  }
```

Owner主动创建issue。
```JavaScript
  createIssue() {
    const { id, owner, repo, title, link, desc, labels } = this

    return http.post(`/repos/${owner}/${repo}/issues`, {
      title,
      labels: labels.concat(['gitment', id]),
      body: `${link}\n\n${desc}`,
    })
      .then((meta) => {
        this.state.meta = meta
        return meta
      })
  }
```

### 数据以及状态管理(Mobx)

数据的载入和更新也是比较简单的，使用Mobx作为状态管理工具，在构造函数里，判断是否是分页，在根据分页信息，
调用`update`函数，更新数据！

```JavaScript
 update() {
    return Promise.all([this.loadMeta(), this.loadUserInfo()])
      .then(() => Promise.all([
        this.loadComments().then(() => this.loadCommentReactions()),
        this.loadReactions(),
      ]))
      .catch(e => this.state.error = e)
  }
```

关于状态管理和更新等，不做详细解释，有兴趣可以去查看[MOBX](https://mobx.js.org/getting-started.html).

### 创建评论

通过API创建评论：

```JavaScript
 post(body) {
    return this.getIssue()
      .then(issue => http.post(issue.comments_url, { body }, ''))
      .then(data => {
        this.state.meta.comments++
        const pageCount = Math.ceil(this.state.meta.comments / this.perPage)
        if (this.state.currentPage === pageCount) {
          this.state.comments.push(data)
        }
        return data
      })
  }
```

### 自定义主题的支持

 Gitment的实现，将Class数据等交互操作和页面渲染，做了非常松的耦合，非常便于使用者开发自己的Theme。
 具体实现是这样的，提供使用对应Theme的借口。

 ```JavaScript
   useTheme(theme = {}) {
    this.theme = theme

    const renderers = Object.keys(this.theme)
    renderers.forEach(renderer => extendRenderer(this, renderer))
  }
 ```
 
 从Default theme中，可以看到，export这些：

 ```JavaScript
 export default { render, renderHeader, renderComments, renderEditor, renderFooter }
 ```

 再讲这些Theme的方法，一个个加入到Gitment的Instance上。

 ```JavaScript
 function extendRenderer(instance, renderer) {
  instance[renderer] = (container) => {
    const targetContainer = getTargetContainer(container)
    const render = instance.theme[renderer] || instance.defaultTheme[renderer]

    autorun(() => {
      const e = render(instance.state, instance)
      if (targetContainer.firstChild) {
        targetContainer.replaceChild(e, targetContainer.firstChild)
      } else {
        targetContainer.appendChild(e)
      }
    })

    return targetContainer
  }
}
 ```

 非常方便的实现了主题绘制和数据的分离，赞！

### 点赞/删除/预览等功能的实现

 还有一些例如 lIke Vote 等操作，大同小异，并没有太多的技术含量，不做过多的描述，当然MARKDOWN的支持和预览可以有一些探讨，
 但是并不想在这里深入。

### 结束

Gitment非常巧妙的利用了GITHUB的一些功能，以及他的设计与实现，对我启发也比较大，如何发散思维，利用现有的轮子做更多的事情，
真的非常值得学习和思考。

> 以上都是个人见解，如有错误和不妥之处，非常欢迎指正，谢谢！
