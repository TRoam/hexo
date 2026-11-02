# -*- coding: utf-8 -*-
"""Introduction and compact chronological rows inside the original theme."""
from html import escape

def overview(posts, post_url, render_card=None):
    intro='''<main class="overview" id="overview-main"><section class="overview-intro"><h1>从全栈研发，走向 AI 产品设计<br>和 Agent 平台研发</h1><p>做过全栈研发和架构设计，也转向产品经理，负责团队与产品交付。<br>现在开发企业级 AI Agent 平台，把产品设计和核心研发放在一起。</p><p>这里记录开发中遇到的问题、设计方案时的取舍，也写一些还在尝试的想法。</p><a href="/blog/about/">关于我 →</a></section>'''
    rows=''.join(f'<li><time datetime="{p["month"]}">{p["month"]}</time><a href="{post_url(p)}">{escape(p["title"])}</a></li>' for p in posts[:14])
    return intro+'<section class="overview-recent"><div class="overview-section-heading"><h2>最新文章</h2><a href="/blog/articles/">全部文章 →</a></div><ul>'+rows+'</ul></section></main>'
