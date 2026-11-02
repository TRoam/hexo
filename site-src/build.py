# -*- coding: utf-8 -*-
"""Dependency-free static blog build; only explicit public content is emitted."""
from pathlib import Path
from html import escape
from collections import Counter
import json, re, math, hashlib, shutil

ROOT=Path(__file__).resolve().parent
# Final manuscripts are directly editable; previous editorial scripts are historical records.
from types import SimpleNamespace
from datetime import datetime, timezone, timedelta
TODAY=datetime.now(timezone(timedelta(hours=8))).date().isoformat()
POSTS=json.loads((ROOT/'content'/'articles.source.json').read_text())
assert POSTS and len({p['slug'] for p in POSTS})==len(POSTS)
for post in POSTS:
 post['references']=[]
content=SimpleNamespace(POSTS=POSTS,PUBLISHED=TODAY,REFERENCES={})
(ROOT/'content'/'articles.json').write_text(json.dumps(POSTS,ensure_ascii=False,indent=2)+'\n')
OUT=ROOT/'site'/'blog'
# This directory contains generated files only; a clean manual build avoids stale tag pages.
if OUT.exists():shutil.rmtree(OUT)
OUT.mkdir(parents=True,exist_ok=True)
for p in list((OUT/'posts').glob('*/index.html')) if (OUT/'posts').exists() else []: p.unlink()
(OUT/'assets').mkdir(exist_ok=True)
if (OUT/'assets'/'diagrams').exists():shutil.rmtree(OUT/'assets'/'diagrams')
for asset in ['style.css','site.js']:
 shutil.copy2(ROOT/'assets'/asset,OUT/'assets'/asset)
VERSION=hashlib.sha256((ROOT/'assets'/'style.css').read_bytes()+(ROOT/'assets'/'site.js').read_bytes()).hexdigest()[:10]
legacy_namespace={'__file__':str(ROOT/'legacy.py')}
exec(compile((ROOT/'legacy.py').read_text(),str(ROOT/'legacy.py'),'exec'),legacy_namespace)
POSTS=legacy_namespace['load_legacy'](ROOT,OUT)+POSTS

def post_url(p):
 return p.get('url','/blog/posts/'+p['slug']+'/')

ORIGIN='https://www.tgf21.com'
diagram_namespace={'__file__':str(ROOT/'article_visuals.py')}
exec(compile((ROOT/'article_visuals.py').read_text(),str(ROOT/'article_visuals.py'),'exec'),diagram_namespace)

THEME='一个全栈工程师，如何逐步走向 AI 产品设计和 Agent 平台研发。'

def inline(s):
 s=escape(s)
 s=re.sub(r'`([^`]+)`',r'<code>\1</code>',s)
 s=re.sub(r'\*\*([^*]+)\*\*',r'<strong>\1</strong>',s)
 s=re.sub(r'\[([^\]\n]+)\]\((https?://[^\s)]+)\)',r'<a href="\2" target="_blank" rel="noopener noreferrer">\1</a>',s)
 return s

def render(body):
 result=[];toc=[];blocks=body.split('\n\n');i=0
 while i<len(blocks):
  block=blocks[i].strip();i+=1
  if not block:continue
  if block.startswith('```'):
   code=block
   while code.count('```')<2 and i<len(blocks):code+='\n\n'+blocks[i];i+=1
   lines=code.splitlines();language=lines[0][3:].strip()
   result.append('<figure class="code-block"><figcaption>'+escape(language or '示意')+'</figcaption><pre><code>'+escape('\n'.join(lines[1:-1]))+'</code></pre></figure>')
  elif block.startswith('| ') and '\n|' in block:
   rows=[[cell.strip() for cell in line.strip().strip('|').split('|')] for line in block.splitlines()]
   if len(rows)>1 and all(re.fullmatch(r':?-+:?',cell) for cell in rows[1]):
    result.append('<div class="table-scroll"><table><thead><tr>'+''.join('<th>'+inline(cell)+'</th>' for cell in rows[0])+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+inline(cell)+'</td>' for cell in row)+'</tr>' for row in rows[2:])+'</tbody></table></div>')
   else:result.append('<p>'+inline(block)+'</p>')
  elif block.startswith('## '):
   heading=block[3:].strip();anchor='section-'+str(len(toc)+1);toc.append((anchor,heading));result.append(f'<h2 id="{anchor}">{inline(heading)}</h2>')
  elif re.match(r'^\d+\. ',block):result.append('<ol>'+''.join('<li>'+inline(re.sub(r'^\d+\. ','',line))+'</li>' for line in block.splitlines())+'</ol>')
  elif block.startswith('- '):result.append('<ul>'+''.join('<li>'+inline(l[2:])+'</li>' for l in block.splitlines() if l.startswith('- '))+'</ul>')
  elif block.startswith('> '):result.append('<blockquote>'+inline(block[2:])+'</blockquote>')
  else:result.append('<p>'+inline(block.replace('\n',' '))+'</p>')
 return '\n'.join(result),toc

# Reuse the actual Yilia template and its assets from the preserved published site.
from html.parser import HTMLParser
from urllib.parse import quote
ORIGINAL=ROOT/'theme'
TEMPLATE=(ORIGINAL/'shell.html').read_text()
for asset in ORIGINAL.iterdir():
 if asset.is_file() and asset.suffix in ('.css','.js','.ico'):
  shutil.copy2(asset,OUT/asset.name)
  if asset.suffix=='.js':
   script=asset.read_text().replace('.p="./"','.p="/blog/"')
   if asset.name=='main.43a13c.js':
    assert script.count('if(n(235),window.BJ_REPORT){')==1
    script=script.replace('if(n(235),window.BJ_REPORT){','if(false){')
   (OUT/asset.name).write_text(script)
for folder in ['fonts','images','img']:
 if (ORIGINAL/folder).exists():shutil.copytree(ORIGINAL/folder,OUT/folder,dirs_exist_ok=True)
shutil.copy2(ROOT/'assets'/'original-theme-extra.css',OUT/'assets'/'original-theme-extra.css')
THEME_VERSION=hashlib.sha256((ROOT/'assets'/'original-theme-extra.css').read_bytes()+(OUT/'main.43a13c.js').read_bytes()).hexdigest()[:10]
old_index=json.loads((ROOT/'content'/'history.index.json').read_text())
old_tags={Path(p['path']).stem:[t['name'] for t in p['tags']] for p in old_index}
for p in POSTS:p['tags']=old_tags.get(p['slug'],[p['category']])
POSTS.sort(key=lambda p:(p['month'],p.get('published',''),p['slug']),reverse=True)

def frame(title,description,path,body,active='',article=None):
 # Keep the complete original template shell, including mobile and sidebar behavior.
 page=TEMPLATE.replace('<!-- BLOG_CONTENT -->',body,1)
 head=f'<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{escape(title)} · 小光头禅院</title><link rel="icon" href="/blog/images/avatar.jpg"><meta name="description" content="{escape(description,quote=True)}"><link rel="canonical" href="{ORIGIN+path}"><link rel="alternate" type="application/atom+xml" href="/blog/feed.xml" title="博客订阅"><link rel="stylesheet" href="/blog/main.43a13c.css"><link rel="stylesheet" href="/blog/assets/original-theme-extra.css?v={THEME_VERSION}">'
 page=re.sub(r'<head>.*?</head>',head+'</head>',page,count=1,flags=re.S)
 # Prefix only HTML attributes; leave protocol URLs and inline JavaScript intact.
 page=re.sub(r'(href|src)=("|\')/(?!/|blog/)(.*?)\2',lambda m:m[1]+'='+m[2]+'/blog/'+m[3].removeprefix('./')+m[2],page)
 page=re.sub(r'([=\"])\"/((?:slider|mobile)\.[^\"]+\.js)\"',lambda m:m[1]+'\"/blog/'+m[2]+'\"',page)
 page=re.sub(r'(<div class=\"aboutme-wrap\" id=\"js-aboutme\">).*?(</div>)',lambda m:m[1]+THEME+m[2],page,flags=re.S)
 page=page.replace('js-header-author">undefined','js-header-author">小光头禅院')
 page=page.replace('src="/blog/main.43a13c.js"',f'src="/blog/main.43a13c.js?v={THEME_VERSION}"')
 page=re.sub(r'<section class="tools-section tools-section-friends".*?</section>','',page,flags=re.S)
 page=page.replace('href="/blog/"','href="/"')
 page=page.replace('Roam Tang','小光头禅院').replace('&copy; 2023','&copy; 2026')
 page=page.replace('root: "/"','root: "/blog/"').replace('e.p="./"','e.p="/blog/"')
 page=page.replace('isHome: true','isHome: '+str(active=='home').lower()).replace('isPost: false','isPost: '+str(bool(article)).lower()).replace('isArchive: false','isArchive: '+str(active=='archive').lower())
 # Use the existing sidebar slots for links to the complete archive and introduction.
 page=re.sub(r'<a q-on="click: openSlider\(e, \'friends\'\)"[^>]*>友链</a>','<a href="/blog/archives/">归档</a>',page)
 page=re.sub(r'<a q-on="click: openSlider\(e, \'aboutme\'\)"[^>]*>关于我</a>','<a href="/blog/about/">关于我</a>',page)
 return page

def write(path,text):
 p=OUT/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text)

def tags(p):
 return '<div class="article-tag tagcloud"><i class="icon-price-tags icon"></i><ul class="article-tag-list">'+''.join(f'<li class="article-tag-list-item"><a class="article-tag-list-link color{i%5+1}" href="/blog/tags/{quote(t)}/">{escape(t)}</a></li>' for i,t in enumerate(p['tags']))+'</ul></div>'

def date(p):
 return f'<a href="{post_url(p)}" class="archive-article-date"><time datetime="{p["month"]}" itemprop="datePublished"><i class="icon-calendar icon"></i>{p["month"]}</time></a>'

def heading(p,listing=False):
 title=f'<h1 itemprop="name"><a class="article-title" href="{post_url(p)}">{escape(p["title"])}</a></h1>' if listing else f'<h1 class="article-title" itemprop="name">{escape(p["title"])}</h1>'
 return '<header class="article-header">'+title+date(p)+'</header>'

def article(p,body,listing=False):
 more=f'<a class="article-more-a" href="{post_url(p)}">展开全文 &gt;&gt;</a>' if listing else ''
 return '<article class="article article-type-post '+('article-index' if listing else '')+'" itemscope itemprop="blogPost"><div class="article-inner">'+heading(p,listing)+'<div class="article-entry" itemprop="articleBody">'+body+'</div><div class="article-info '+('article-info-index' if listing else '')+'">'+tags(p)+more+'<div class="clearfix"></div></div></div></article>'

def pagination(base,current,total):
 def url(n):return base if n==1 else base+'page/'+str(n)+'/'
 links=[]
 if current>1:links.append(f'<a class="extend prev" href="{url(current-1)}">&laquo; Prev</a>')
 for n in range(1,total+1):
  links.append(f'<span class="page-number current">{n}</span>' if n==current else f'<a class="page-number" href="{url(n)}">{n}</a>')
 if current<total:links.append(f'<a class="extend next" href="{url(current+1)}">Next &raquo;</a>')
 return '<nav id="page-nav">'+''.join(links)+'</nav>' if total>1 else ''

# Preserve the original home-page excerpts for legacy posts, including their images.
class Excerpts(HTMLParser):
 def __init__(self):super().__init__(convert_charrefs=False);self.slug=None;self.depth=0;self.parts=[];self.found={}
 def handle_starttag(self,t,a):
  d=dict(a)
  if not self.depth and t=='a' and d.get('class')=='article-title':self.slug=Path(d['href']).stem
  if t=='div' and d.get('itemprop')=='articleBody' and not self.depth:self.depth=1;self.parts=[];return
  if self.depth:
   if t=='div':self.depth+=1
   self.parts.append(self.get_starttag_text())
 def handle_endtag(self,t):
  if self.depth:
   if t=='div':
    self.depth-=1
    if not self.depth:self.found[self.slug]=''.join(self.parts);return
   self.parts.append('</'+t+'>')
 def handle_data(self,d):
  if self.depth:self.parts.append(d)
 def handle_entityref(self,n):
  if self.depth:self.parts.append('&'+n+';')
 def handle_charref(self,n):
  if self.depth:self.parts.append('&#'+n+';')
excerpts=json.loads((ROOT/'content'/'history.excerpts.json').read_text())

def excerpt(p):
 if p.get('legacy') and p['slug'] in excerpts:
  text=excerpts[p['slug']]
  text=re.sub(r'(src|href)="/(post|images|img|demo)/',r'\1="/blog/legacy-assets/\2/',text)
  text=re.sub(r'href="/blog/legacy-assets/post/([^"/]+\.html)',r'href="/blog/post/\1',text)
  return text
 return ''.join('<p>'+inline(b)+'</p>' for b in p['body'].split('\n\n')[:2] if not b.startswith(('##','```')))

def archive_entries(posts):
 text=''
 for year in sorted({p['month'][:4] for p in posts},reverse=True):
  text+=f'<section class="archives-wrap"><div class="archive-year-wrap"><a href="/blog/archives/{year}/" class="archive-year">{year}</a></div><div class="archives">'
  for p in posts:
   if p['month'][:4]!=year:continue
   text+='<article class="archive-article archive-type-post"><div class="archive-article-inner"><header class="archive-article-header"><div class="article-meta">'+date(p)+'</div><h1 itemprop="name"><a class="archive-article-title" href="'+post_url(p)+'">'+escape(p['title'])+'</a></h1><div class="article-info info-on-right">'+tags(p)+'</div><div class="clearfix"></div></header></div></article>'
  text+='</div></section>'
 return text

def listing(posts,base,archive=False,title='小光头禅院'):
 total=max(1,math.ceil(len(posts)/7))
 for page in range(1,total+1):
  selection=posts[(page-1)*7:page*7]
  body=archive_entries(selection) if archive else ''.join(article(p,excerpt(p),True) for p in selection)
  body+=pagination(base,page,total)
  url=base if page==1 else base+'page/'+str(page)+'/'
  write(url.removeprefix('/blog/')+'index.html',frame(title,THEME,url,body,'archive' if archive else 'home'))

write('2016/03/25/使用Hexo和github搭建个人博客/index.html','<!doctype html><meta charset=\"utf-8\"><meta http-equiv=\"refresh\" content=\"0;url=/blog/post/fc33988f.html\"><a href=\"/blog/post/fc33988f.html\">使用Hexo和github搭建个人博客</a>')
listing(POSTS,'/blog/articles/')
for number in range(2,max(1,math.ceil(len(POSTS)/7))+1):
 write(f'page/{number}/index.html',(OUT/f'articles/page/{number}/index.html').read_text())
overview_namespace={}
exec(compile((ROOT/'overview.py').read_text(),str(ROOT/'overview.py'),'exec'),overview_namespace)
write('index.html',frame('全栈研发、AI 产品与 Agent 平台',THEME,'/',overview_namespace['overview'](POSTS,post_url,lambda p:article(p,excerpt(p),True)),'home'))
listing(POSTS,'/blog/archives/',True,'归档')
for year in sorted({p['month'][:4] for p in POSTS}):listing([p for p in POSTS if p['month'].startswith(year)],'/blog/archives/'+year+'/',True,year+' 年文章')
for tag in sorted({tag for p in POSTS for tag in p['tags']}):listing([p for p in POSTS if tag in p['tags']],'/blog/tags/'+quote(tag)+'/',True,tag)
# Hexo serves decoded UTF-8 folder names; URLs remain percent-encoded.
for path in sorted(OUT.rglob('*'),reverse=True):
 if '%' in path.name:
  from urllib.parse import unquote
  dest=path.with_name(unquote(path.name))
  if not dest.exists():path.rename(dest)

ABOUT=[
 '这些年，我做过研发和架构，也转向产品与团队管理。现在又把产品设计和研发放在了一起。',
 '最初做全栈研发和架构设计，喜欢弄明白技术原理，也享受亲手搭起一个系统的过程。后来转向产品经理，负责整个团队，更多时间用来理解业务、规划产品、协调研发和推动交付。实现之外，还得判断功能为什么要做，以及怎样带着团队做好。',
 '开始使用 AI 之后，我又花了很多时间亲手做产品、写代码。以前在研发、架构、产品和团队管理中积累的经验，现在可以一起用上：发现问题、设计方案，再动手开发、验证和迭代。很多想法能自己试，也更快看得到结果。',
 '最近在开发企业级 AI Agent 平台，同时负责产品设计和核心研发。我也在摸索怎样借助 AI，从产品判断到实现，独立推动更多事情，把“超级个体”变成日常做事的方式。',
 '这个博客记录的，就是这段变化。',
 '这里会有产品设计中的取舍、架构和开发中的具体问题，也会有走过的弯路，以及一些还没想清楚的事情。写下来，留给以后回看，也和有相似经历的人交流。',
]

about_body=''.join('<p>'+escape(t)+'</p>' for t in ABOUT[:5])+f'<blockquote>{THEME}</blockquote>'+''.join('<p>'+escape(t)+'</p>' for t in ABOUT[5:])
about='<article class="article article-type-page"><div class="article-inner"><header class="article-header"><h1 class="article-title">关于我</h1></header><div class="article-entry">'+about_body+'</div></div></article>'
write('about/index.html',frame('关于我',THEME,'/blog/about/',about,'about'))
for index,p in enumerate(POSTS):
 if p.get('legacy'):rendered=p['htmlBody']
 else:
  rendered,_=render(p['body']);rendered=diagram_namespace['insert_diagram'](p,rendered,OUT)

 body=article(p,rendered)
 neighbors=[]
 for pos,label in [(index-1,'上一篇'),(index+1,'下一篇')]:
  if 0<=pos<len(POSTS):q=POSTS[pos];neighbors.append(f'<a href="{post_url(q)}"><small>{label}</small>{escape(q["title"])}</a>')
 body+='<nav class="article-nav">'+''.join(neighbors)+'</nav>'
 write(post_url(p).removeprefix('/blog/')+('index.html' if not p.get('legacy') else ''),frame(p['title'],p['excerpt'],post_url(p),body,article=p))
write('content.json',json.dumps([{'title':p['title'],'date':p['month']+'-01T00:00:00.000Z','path':post_url(p).removeprefix('/blog/'),'tags':[{'name':t,'slug':t,'permalink':'/blog/tags/'+quote(t)+'/'} for t in p['tags']]} for p in POSTS],ensure_ascii=False))
(ROOT/'site'/'index.html').write_text((OUT/'index.html').read_text())
from xml.sax.saxutils import escape as xml
feed='<?xml version="1.0" encoding="utf-8"?><feed xmlns="http://www.w3.org/2005/Atom"><title>小光头禅院</title><id>'+ORIGIN+'/blog/</id><link href="'+ORIGIN+'/blog/"/><link rel="self" href="'+ORIGIN+'/blog/feed.xml"/><updated>'+content.PUBLISHED+'T22:00:00+08:00</updated><author><name>小光头禅院</name></author>'
for p in reversed(POSTS):
 url=ORIGIN+post_url(p)
 feed+='<entry><title>'+xml(p['title'])+'</title><id>'+url+'</id><link href="'+url+'"/><published>'+p['published']+'T22:00:00+08:00</published><updated>'+p['updated']+'T22:00:00+08:00</updated><summary>'+xml(p['excerpt'])+'</summary></entry>'
write('feed.xml',feed+'</feed>')
write('atom.xml',feed+'</feed>')
paths=['/','/blog/articles/','/blog/about/','/blog/archives/']+[post_url(p) for p in POSTS]
write('sitemap.xml','<?xml version="1.0" encoding="utf-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join('<url><loc>'+ORIGIN+x+'</loc><lastmod>'+content.PUBLISHED+'</lastmod></url>' for x in paths)+'</urlset>')
write('404.html',frame('这一页没有找到','可以回到文章列表继续看看。','/blog/404.html','<main id="main" class="narrow page-heading"><p class="eyebrow">404</p><h1>这一页没有找到。</h1><p>链接可能已经变了，回到文章列表看看吧。</p><a class="text-link" href="/blog/">所有文章 ↗</a></main>'))
write('release.json',json.dumps({'builtAt':content.PUBLISHED,'articleCount':len(POSTS),'legacyCount':sum(bool(p.get('legacy')) for p in POSTS),'newCount':len(content.POSTS),'articles':[{'slug':p['slug'],'title':p['title'],'month':p['month']} for p in POSTS]},ensure_ascii=False,indent=2))
print(json.dumps({'articles':len(POSTS),'characters':sum(len(re.findall(r'[\u4e00-\u9fff]',p['body'])) for p in POSTS),'output':str(OUT),'years':dict(Counter(p['month'][:4] for p in POSTS))},ensure_ascii=False))
