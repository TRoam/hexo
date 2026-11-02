# 当前站点源文件

从仓库根目录手动执行 `python3 site-src/build.py`。输出在 `site-src/site/`，该目录不提交 Git。

所有构建输入均在本目录，不依赖服务器备份或 JL 的其他目录。

`content/articles.source.json` 为新增正文来源；`content/history.json` 保留已发表正文，`media/history/` 保存其资源；`theme/shell.html` 是不包含首页文章列表的主题模板。不要把服务器配置、密钥或本地操作日志加入这些内容。
