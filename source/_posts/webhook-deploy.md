---
title: 基于GitHub/Webhook的简单自动化部署架构
tags:
  - deploy
  - linux
  - nodejs
abbrlink: fc66e3c5
date: 2018-12-09 15:45:04
---

每次个人项目更新以后，都需要通过FTP将代码传到服务器，或者登录服务器上运行部署命令，个人的小项目，又不愿意安装Jenkins等复杂管理工具，能不能达到如下图的自动部署流程呢？

{% asset_img webhook.png %}

<!-- more -->

> - 当有更新时，`PUSH`代码到相应代码库
> - GitHub通知服务器，有更新啦！
> - 服务器知道有更新以后，从代码库拉取代码
> - 执行部署相关操作

### git hooks & Github Webhook

> Like many other Version Control Systems, Git has a way to fire off custom scripts when certain important actions occur. There are two groups of these hooks: client-side and server-side. Client-side hooks are triggered by operations such as committing and merging, while server-side hooks run on network operations such as receiving pushed commits. You can use these hooks for all sorts of reasons.

如git官方文档所说，git提供了相应的钩子程序，能在特定的重要动作发生时触发自定义脚本程序。 有两组这样的钩子：客户端的和服务器端的。 客户端钩子由诸如提交和合并这样的操作所调用，而服务器端钩子作用于诸如接收被推送的提交这样的联网操作。 你可以随心所欲地运用这些钩子。

具体详细使用说明，可以参考文档[Git Hooks](https://git-scm.com/book/en/v2/Customizing-Git-Git-Hooks)。

GitHub利用此特性提供了基于API的Webhooks服务，简单来说，就是可以向GitHub注册相应的钩子，当指定动作发生时，GitHub会向你注册的地址发送相应的请求，正好可以契合我的需求,在GitHub中,添加一个hook，配置十分简单： 


{% asset_img hooks.png %}


> 在相应的仓库中，`setting --> webhooks`， 所创建的hooks都会在此列出~


{% asset_img hooks1.png %}


> 如上图，创建一个`webhook`, 需要一个能够接受Github发送过来信息的服务，如有需要，还可以设置相应的秘钥,那么我们也需要创建一个相应的服务。


### Nodejs 创建webhook接口服务


上一步中，注册了一个push的hook，GitHub发送过来的消息大致是这样的，完整信息请参考[官网](https://developer.github.com/v3/activity/events/types/#pushevent)

```json
{
  // ...
  "head_commit": null,
  "repository": {
    "id": 135493233,
    "node_id": "MDEwOlJlcG9zaXRvcnkxMzU0OTMyMzM=",
    "name": "Hello-World",
    "full_name": "Codertocat/Hello-World",
    "owner": {
      "name": "Codertocat",
      "email": "21031067+Codertocat@users.noreply.github.com",
      "login": "Codertocat",
      "id": 21031067,
     // ...
    },
    "private": false,
    "html_url": "https://github.com/Codertocat/Hello-World",
    "description": null,
    "fork": false,
    "url": "https://github.com/Codertocat/Hello-World",
    "forks_url": "https://api.github.com/repos/Codertocat/Hello-World/forks",
    // ...
```

使用node创建一个简单的服务，监听GitHub发送过来的action，并且根据信息做简单判别，代码如下：

```JS
var express = require('express');
var bodyParser = require('body-parser');
var app = express();
app.use(bodyParser.urlencoded({extended: false}));
var hostName = '127.0.0.1';
var port = 8080;

app.all('*', function(req, res, next) {
  res.header('Access-Control-Allow-Origin', '*');
  res.header(
    'Access-Control-Allow-Headers',
    'Origin, X-Requested-With, Content-Type, Accept'
  );
  res.header('Access-Control-Allow-Methods', 'PUT,POST,GET,DELETE,OPTIONS');
  res.header('X-Powered-By', ' 3.2.1');
  res.header('Content-Type', 'application/json;charset=utf-8');
  next();
});

app.post('/post', function(req, res) {
  console.log('请求参数：', req.body);
  if(/* 验证请求是来自GitHub的逻辑 */) {

  }else{

  }
});

app.listen(port, hostName, function() {
  console.log(`服务运行在http://${hostName}:${port}`);
});
```

启动上述服务

```
node app.js
```

当然，在服务器上，推荐使用`pm2`管理node服务，并且配置`nginx`统一域名端口负载等。

### 利用`exec`执行部署

好了，现在代码有了更新，服务器也知道得到了消息，接下来的工作就是，拉取目标代码，部署相应服务了。

#### 配置权限

* 创建web服务器用户目录,我使用的是`nginxUser`作为web访问用户，那么需要给这个用户添加相应的能够操作的权限。

```
sudo mkdir /home/www/.ssh
sudo chown -R nginxUser /home/www/.ssh
```

* 配置GIT SSH 公钥和私钥

```
ssh-keygen -t rsa -C "liulangdewoniu@gmail.com"
```

* 部署公钥

```
sudo -Hu nginxUser ssh-keygen -t rsa
```

* 配置公钥到GitHub服务器，具体配置流程就不在这里详细说明了，可以参考[官方文档](https://help.github.com/articles/connecting-to-github-with-ssh/)。

* 给用户配置git信息

```
sudo -Hu nginxUser git config --global credential.helper store
sudo -Hu nginxUser git config --global user.name "Roam" 
sudo -Hu nginxUser git config --global user.email "liulangdewoniu@gmail.com"
```

通过上面的配置，在服务器上，以`nginxuser`就有权限拉取对应GitHub仓库中的代码了

#### 拉取部署代码

当hook服务接收到有更新时，可以使用nodejs子进程，执行shell脚本，更新目标代码库中的代码，如下：

```js
let {exec} = require('child_process');

app.post('/post', function(req, res) {
  console.log('请求参数：', req.body);
  exec(
      'cd /home/www/tgf21 && git pull origin master',
      function(err, stdout, stderr) {
        if (err) {
          console.log(err)
          res.send(err);
        }
        console.log(stdout);
        res.send(stdout);
      }
    );
});
```

当需要重启服务器，连接数据库等操作时，同样可以在`exec`中调用相应的shell脚本，此例子中就不做详细的讲述啦。

至此，我们一开始设想的步骤，完全达到了，从此只需要关心代码的更新，push代码就会自动的触发一系列的操作，将更新部署到我们的服务器上，肯定有同学说，不想每次push都部署怎么办？那就多设置几个分支呗！
