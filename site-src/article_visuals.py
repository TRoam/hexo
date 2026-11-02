# -*- coding: utf-8 -*-
"""Explicit editorial placement: sequence, state, ownership and relationship figures."""
from pathlib import Path
from html import escape
import re, runpy
BASE=runpy.run_path(str(Path(__file__).with_name('diagrams.py')))
CATALOG={}

def seq(key,title,actors,messages,caption):
    CATALOG[key]=('sequence',title,(actors,messages),caption)
def graph(key,old_key,title=None,caption=None):
    item=BASE['GRAPHS'][old_key]
    CATALOG[key]=('graph',title or item[0],item,caption or item[3])
def panels(key,title,items,caption):
    CATALOG[key]=('panels',title,items,caption)

seq('stream-timing','同样的产出节奏，在不同层观察',
    ['测试源','代理','浏览器'],[(0,1,'事件 1：立即写入'),(1,2,'观察是否及时到达'),(0,1,'间隔一秒，事件 2'),(1,2,'对比相邻到达间隔'),(0,1,'间隔一秒，事件 3'),(1,2,'不应在结束时才成批出现')],
    '合成测试时序，非实际采样结果。比较本层间隔，不把跨机器时钟差直接算成延迟。')
seq('stream-reconnect','订阅中断以后，从已确认位置继续',
    ['浏览器','任务接口','事件存储'],[(0,1,'创建任务，取得 taskId'),(0,2,'订阅 after=0'),(2,0,'seq=1、2，客户端记住 2'),(0,2,'断线后订阅 after=2'),(2,0,'重放 seq=3 及后续事件'),(0,1,'无终态或游标过期时查询快照')],
    '自定义游标协议示意。持久事件和去重由应用实现，连接恢复本身不提供业务恢复。')
seq('sso-sequence','认证回调与业务目标分开恢复',
    ['浏览器','本站服务','认证服务'],[(0,1,'访问业务链接，会话已过期'),(1,1,'保存一次性登录事务与业务目标'),(1,2,'跳转授权，携带 state 与挑战'),(2,0,'回调带 code 与 state'),(0,1,'提交回调，校验并消费事务'),(1,2,'用 code 与 verifier 换取令牌'),(1,1,'验证身份令牌，建立本站会话'),(1,0,'恢复目标，再做业务授权')],
    '授权码模式的简化时序，省略非关键字段；具体校验遵守使用的认证协议。')
seq('handoff-stale-worker','租约失效以后，旧执行者仍可能回来',
    ['旧执行者','任务数据库','新执行者'],[(0,1,'领取 epoch=7'),(0,1,'续租中断，结果未确定'),(1,1,'核对后允许重新派发'),(2,1,'领取 epoch=8'),(0,1,'迟到提交 epoch=7'),(1,0,'条件不符，拒绝旧结果'),(2,1,'提交 epoch=8'),(1,2,'当前尝试有效，接受结果')],
    '这里只展示任务提交保护。外部副作用还需要执行入口校验、操作键或下游 fencing。')
seq('handoff-outbox','状态提交和待投递事件在同一事务里',
    ['执行器','数据库','投递器','验证成员'],[(0,1,'保存交接与 Outbox，提交事务'),(2,1,'扫描未确认事件'),(2,3,'投递 handoffId'),(3,3,'去重并校验产出版本'),(3,2,'确认接收'),(2,1,'记录 delivered'),(2,3,'确认丢失可重投，同 id 不重做')],
    '事务保证状态与待发送记录一起存在；消息仍可能重复，接收端必须幂等处理。')
seq('acp-cancel-sequence','取消意图与实际结束分开处理',
    ['客户端','协议适配器','执行环境'],[(0,1,'发起取消请求'),(1,1,'记录 cancel_requested'),(1,2,'按协议与运行能力请求停止'),(2,1,'仍可能返回在途更新'),(1,1,'按会话、轮次和工具关联处理'),(2,1,'确认最终结果或标记未知'),(1,0,'反馈执行终态，保留必要核对')],
    '平台处理顺序示意，不是 ACP 原始报文；取消不能自动撤销已经生效的外部动作。')
seq('page-context-message','跨窗口交互关联到确定的选区版本',
    ['业务页面','消息桥','助手'],[(0,1,'选区快照与 revision=12'),(1,1,'校验 origin、source 与实例'),(1,2,'发送获准上下文'),(2,1,'请求高亮，引用 revision=12'),(1,0,'检查当前实例与选区版本'),(0,2,'applied 或 stale-context 回执')],
    '界面回执只表示 UI 命令处理结果，不代表业务动作已经完成。')
seq('team-apply-recovery','部分应用失败后，按对象继续协调',
    ['应用器','应用记录','目标资源'],[(0,1,'记录蓝图 revision 与计划'),(0,2,'创建成员，附 managedBy'),(0,1,'成员步骤完成'),(0,2,'绑定依赖失败'),(0,1,'保留失败原因与未完成步骤'),(0,2,'再次应用：核对成员，只补绑定'),(0,1,'全部满足后记录 applied')],
    '同一蓝图重复应用不重复创建。不可逆动作与未知结果需要单独核对。')

panels('roles-model','角色职责与资源范围用绑定关联',[
    ('角色与动作',['role_id → action_key','职责定义可被多处复用']),
    ('主体角色绑定',['tenant + subject + role','scope_type + scope_id']),
    ('资源归属',['tenant + resource_id','resource_type + scope_id'])],
    '最小关系模型，不含继承与显式拒绝。资源范围由服务端读取并参与决策。')
panels('resource-boundaries','一个宿主中的资源分组与保留预算',[
    ('宿主保留',['系统与调度服务','不纳入任务可分配容量']),
    ('任务组 A',['当前计量 + hard limit','所有子进程保持在组内']),
    ('任务组 B',['独立限制与采样身份','不共享 A 的无限资源空间'])],
    '资源归属与预算示意，非实际容量配置。还需要检查父级限制与宿主压力。')
panels('agent-control-runtime','配置发布与执行路径各自管理状态',[
    ('管理与发布',['草稿 → 校验 → 配置版本','依赖声明与绑定版本']),
    ('执行与观察',['Run 固定解析后的配置','工具调用、事件、产出物']),
    ('当前安全条件',['调用前权限与凭证检查','撤销不能被配置快照冻结'])],
    '配置与运行分离，授权仍需持续有效；版本引用不携带秘密值。')
panels('app-release-boundary','发布、环境绑定与用户状态分别持有',[
    ('只读发布包',['源码与入口、提示词版本','依赖与配置 schema']),
    ('目标部署',['包摘要与环境绑定','当前指针、候选与回退']),
    ('运行数据',['会话、用户文件、产出物','升级不直接覆盖或删除'])],
    '切换代码版本只改变部署引用；数据迁移与回退需要独立方案。')
panels('team-dependency-ownership','所有权决定谁能更新与删除',[
    ('研发团队持有',['开发、评审、测试成员','团队归档时按计划清理']),
    ('部署持有',['测试与生产运行实例','随产品部署独立演进']),
    ('外部主体持有',['被调用的服务或 Agent','只管理绑定，不替它删除'])],
    '调用关系不等于所有权。环境、凭证引用与兼容条件由绑定对象明确表达。')

for key,old in [
 ('handoff-stage-boundaries','reliable-agent-handoffs'),('page-change-validation','a-verifiable-page-change'),('rag-retrieval','rag-in-practice'),
 ('data-scope-query','which-data-can-a-user-see'),('authorization-adapter','integrating-authorization'),
 ('template-binding','reusing-data-and-interactions'),('product-expert-routing','a-product-expert-assistant'),
 ('alarm-evidence','from-alarm-to-report'),('team-draft-apply','building-an-agent-team'),
 ('delegation-check','from-rbac-to-agent-delegation')]:graph(key,old)

# State diagrams use a different notation from architecture boxes: small status nodes,
# a highlighted uncertainty state and explicit labels on transitions.
STATES={
 'resource-release':('停止确认以后才归还预算',
  [('running',0,0,'running'),('stopping',1,0,'stopping'),('stopped',2,0,'stopped'),('released',3,0,'released'),('uncertain',1,1,'uncertain')],
  [('running','stopping','停止请求'),('stopping','stopped','确认无残留'),('stopped','released','按代次释放'),('stopping','uncertain','失联'),('uncertain','stopped','核对与清理')],
  '运行资源清理与外部业务副作用分别核对。旧代次不得归还新代次的预算。'),
 'recurring-run':('一次计划运行拥有独立状态',
  [('queued',0,0,'queued'),('running',1,0,'running'),('generated',2,0,'generated'),('delivered',3,0,'delivered'),('unknown',2,1,'outcome_unknown')],
  [('queued','running','领取'),('running','generated','固定产物'),('generated','delivered','确认通知'),('generated','unknown','发送超时'),('unknown','delivered','核对已生效')],
  '报告生成与对外发送分开记录。未知结果不自动等同失败重做。'),
 'user-instance-lifecycle':('逻辑实例与执行资源有不同生命周期',
  [('creating',0,0,'creating'),('ready',1,0,'ready'),('suspended',2,0,'suspended'),('deleting',3,0,'deleting'),('execution',1,1,'execution'),('stopped',2,1,'stopped')],
  [('creating','ready','初始化'),('ready','suspended','暂停'),('suspended','ready','恢复'),('suspended','deleting','删除'),('ready','execution','分配计算'),('execution','stopped','回收计算')],
  '运行资源回收不删除逻辑实例的持久状态。图中省略错误与恢复分支。'),
}
for key,(title,nodes,edges,caption) in STATES.items():CATALOG[key]=('state',title,(nodes,edges),caption)
panels('rag-evaluation','三个检查点分别定位召回、组装和回答错误',[
 ('候选集合',['requiredEvidence 是否召回','记录检索与融合参数']),
 ('实际上下文',['前提、例外是否仍然存在','记录过滤与裁剪过程']),
 ('最终答案',['结论、拒答、引用是否正确','不能用召回率代替答对率'])],
 '每次实验固定题集与资料快照。无答案问题独立检查错误肯定回答。')

def text(x,y,value,size=14,fill='#444',anchor='middle'):
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{size}" fill="{fill}" font-family="sans-serif">{escape(value)}</text>'
def sequence_svg(title,data,caption):
    actors,messages=data;width=max(720,len(actors)*230);height=115+len(messages)*60
    xs=[80+i*(width-160)/(len(actors)-1) for i in range(len(actors))]
    parts=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc"><title id="title">{escape(title)}</title><desc id="desc">{escape(caption)}</desc><defs><marker id="arrow" markerWidth="9" markerHeight="8" refX="8" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8" fill="none" stroke="#687f95"/></marker></defs><rect width="100%" height="100%" fill="#fff"/>']
    for x,actor in zip(xs,actors):
        parts.extend([f'<rect x="{x-65}" y="12" width="130" height="36" rx="3" fill="#edf2f6" stroke="#bdcbd6"/>',text(x,35,actor),f'<path d="M{x},48 V{height-15}" stroke="#c6cdd3" stroke-dasharray="4 5"/>'])
    for index,(a,b,label) in enumerate(messages):
        y=90+index*60;x1,x2=xs[a],xs[b]
        if a==b:
            parts.append(f'<path d="M{x1},{y-8} h48 v22 h-48" fill="none" stroke="#687f95" marker-end="url(#arrow)"/>');parts.append(text(x1+58,y+8,label,12,anchor='start'))
        else:
            parts.extend([f'<path d="M{x1},{y} H{x2}" stroke="#687f95" marker-end="url(#arrow)"/>',text((x1+x2)/2,y-10,label,12)])
    return ''.join(parts)+'</svg>',width,height

def panels_svg(title,items,caption):
    width=930;height=245
    parts=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc"><title id="title">{escape(title)}</title><desc id="desc">{escape(caption)}</desc><rect width="100%" height="100%" fill="#fff"/>']
    for i,(name,lines) in enumerate(items):
        x=18+i*306
        parts.extend([f'<rect x="{x}" y="22" width="282" height="198" rx="4" fill="#fafbfc" stroke="#bfcbd4"/>',f'<path d="M{x},72 h282" stroke="#bfcbd4"/>',text(x+141,52,name,16)])
        for j,line in enumerate(lines):parts.append(text(x+141,116+j*36,line,13,'#687581'))
    return ''.join(parts)+'</svg>',width,height

def state_svg(title,data,caption):
    nodes,edges=data;lookup={n[0]:n for n in nodes}
    dx,dy,w,h,pad=270,150,160,54,55
    width=pad*2+max(n[1] for n in nodes)*dx+w
    height=pad*2+max(n[2] for n in nodes)*dy+h
    def pos(node):return pad+node[1]*dx,pad+node[2]*dy
    parts=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc"><title id="title">{escape(title)}</title><desc id="desc">{escape(caption)}</desc><defs><marker id="arrow" markerWidth="9" markerHeight="8" refX="8" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 Z" fill="#879587"/></marker></defs><rect width="100%" height="100%" fill="#fff"/>']
    for a,b,label in edges:
        na,nb=lookup[a],lookup[b];ax,ay=pos(na);bx,by=pos(nb)
        if nb[1]>na[1]:
            x1,y1=ax+w,ay+h/2;x2,y2=bx,by+h/2
            mid=(x1+x2)/2
            path=f'M{x1},{y1} C{mid},{y1} {mid},{y2} {x2-3},{y2}'
            tx,ty=mid,(y1+y2)/2-10
        elif nb[1]<na[1]:
            x1,y1=ax+w/2,ay;x2,y2=bx+w/2,by
            top=min(ay,by)-30
            path=f'M{x1},{y1} V{top} H{x2} V{y2-3}'
            tx,ty=(x1+x2)/2,top-9
        else:
            x1,y1=ax+w/2,ay+h;x2,y2=bx+w/2,by
            path=f'M{x1},{y1} V{y2-3}'
            tx,ty=x1+28,(y1+y2)/2
        parts.append(f'<path d="{path}" fill="none" stroke="#879587" stroke-width="1.4" marker-end="url(#arrow)"/>')
        parts.append(text(tx,ty,label,11,'#687568'))
    for node in nodes:
        x,y=pos(node);uncertain='unknown' in node[3] or 'uncertain' in node[3]
        fill='#f5e9df' if uncertain else '#edf1ed'
        parts.extend([f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="27" fill="{fill}" stroke="#bfc9bf"/>',text(x+w/2,y+33,node[3],13)])
    return ''.join(parts)+'</svg>',width,height

def insert_diagram(post,rendered,out):
    def replace(match):
        key=match.group(1)
        if key not in CATALOG:raise ValueError(f'unknown diagram {key}')
        kind,title,data,caption=CATALOG[key]
        if kind=='sequence':source,w,h=sequence_svg(title,data,caption)
        elif kind=='panels':source,w,h=panels_svg(title,data,caption)
        elif kind=='state':source,w,h=state_svg(title,data,caption)
        else:source,w,h=BASE['svg'](key,data)
        target=out/'assets'/'diagrams'/f'{key}.svg';target.parent.mkdir(parents=True,exist_ok=True);target.write_text(source)
        src='/blog/assets/diagrams/'+key+'.svg'
        return f'<figure class="diagram diagram-{kind}"><div class="diagram-head"><strong>{escape(title)}</strong><a href="{src}" target="_blank" rel="noopener">放大图示 ↗</a></div><div class="diagram-scroll"><img src="{src}" alt="{escape(title,quote=True)}" width="{w}" height="{h}" loading="lazy"></div><figcaption>{escape(caption)}</figcaption></figure>'
    return re.sub(r'<p>\[\[diagram:([a-z0-9-]+)\]\]</p>',replace,rendered)
