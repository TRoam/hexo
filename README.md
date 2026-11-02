# 个人博客源码

这个仓库用于保存文章、主题与手动构建程序，不自动生成或发布网页。

## 目录

- `site-src/content/articles.source.json`：当前新增文章的可编辑正文。
- `site-src/content/history.json`：已发表文章的保留正文及路径，历史文章地址保持不变。
- `site-src/content/history.index.json`、`history.excerpts.json`：历史文章元数据和摘要输入。
- `site-src/build.py`：手动构建，使用 Python 标准库。
- `site-src/overview.py`：首页介绍与日期标题列表。
- `site-src/article_visuals.py`、`diagrams.py`：按正文插入的图示及 SVG 生成。
- `site-src/assets/`：当前页面的补充样式和资源。
- `site-src/theme/`：当前使用的 Yilia 主题模板、脚本、样式和字体。
- `site-src/media/history/`：已发表文章引用的图片与演示资源。
- `source/_posts/`、`themes/` 等原 Hexo 目录保留历史内容。当前手动构建直接读取 `site-src`，不会自动转换或覆盖原 Markdown。

## 本地手动构建与预览

```bash
python3 site-src/build.py
python3 -m http.server 4173 --bind 127.0.0.1 --directory site-src/site
```

访问 `http://127.0.0.1:4173/`。构建目录 `site-src/site/` 被 Git 忽略，不提交生成网页。

仅在需要检查或发布时运行构建。Git 提交和推送不会调用构建程序，也不会上传服务器。仓库没有自动部署工作流；原 Hexo 的 `deploy` 配置已置空。

## 内容维护

正文保留文章的年月与固定 slug，避免改变已有地址。正文中的 `[[diagram:标识]]` 对应图示定义，图示不统一放在开头。文章不输出参考资料区；代码仅用于关键结构、算法和复现，不以示例罗列代替说明。

文章和页面的改动完成后手动预览。需要发布时，由操作者明确提交已检查的静态文件到服务器。服务器备份、密钥、私有原始材料、部署包与本地工作记录不进入这个公开源码仓库。

## 主题与资源

当前页面使用 Yilia 主题，并保留主题署名。主题上游：<https://github.com/litten/hexo-theme-yilia>。该目录保留页面需要的主题静态依赖，文章配图与演示资源用于维持原有访问路径。
