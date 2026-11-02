# -*- coding: utf-8 -*-
"""Small, article-specific vector diagrams with no remote rendering dependency."""
from html import escape

# node = (id, column, row, heading, detail, kind). Positions express each actual model.
GRAPHS={
'from-implementation-to-product':('跨组件筛选的状态与请求版本',[('nav',0,0,'导航器输入','选择、清空与恢复','actor'),('param',1,0,'页面参数','选择值 + revision','data'),('deps',2,0,'依赖组件','按参数版本发起请求','system'),('result',3,0,'响应校验','仅更新当前版本结果','gate')],[('nav','param',''),('param','deps',''),('deps','result','')],'筛选需求的简化数据流。权限范围仍在服务端验证，旧响应不覆盖当前选择。'),
'roles-and-resources':('角色、范围与授权判断',[
 ('u',0,0,'用户','当前身份','actor'),('r',1,0,'角色','一类业务职责','data'),('p',2,0,'动作权限','读取 / 修改 / 发布','data'),
 ('s',1,1,'资源范围','当前空间与资源归属','data'),('a',2,1,'授权判断','动作 + 范围 + 约束','gate'),('o',3,1,'资源服务','允许执行或拒绝','system')],
 [('u','r',''),('r','p',''),('u','s',''),('p','a',''),('s','a',''),('a','o','')],
 '简化授权模型。角色、资源范围和业务状态分别表达，在执行侧汇合。'),
'sso-after-login':('登录回跳的两类地址',[
 ('entry',0,0,'原业务链接','页面与筛选条件','actor'),('auth',1,0,'认证入口','保存受限的业务目标','system'),('cb',2,0,'固定回调地址','接收并校验认证结果','gate'),('target',3,0,'恢复业务页面','再次判断访问权限','system'),
 ('invalid',2,1,'权限或目标无效','显示可处理的状态','data')],
 [('entry','auth','会话过期'),('auth','cb','完成认证'),('cb','target','目标有效'),('cb','invalid','不满足条件')],
 '回调地址负责交接认证结果；业务目标负责恢复页面，二者都需要约束。'),
'which-data-can-a-user-see':('示例系统中的数据范围计算',[
 ('direct',0,0,'直接授权','设备 A','data'),('group',0,1,'用户组授权','设备 B','data'),('org',0,2,'组织规则','设备 C','data'),
 ('union',1,1,'用户集合 U','A、B、C','system'),('app',2,0,'应用范围 A','A、B、D','data'),('scope',2,2,'业务范围 O','A、C、D','data'),('result',3,1,'求交集','本例可访问 A','gate')],
 [('direct','union',''),('group','union',''),('org','union',''),('union','result',''),('app','result',''),('scope','result','')],
 '说明用集合示例。显式拒绝、临时授权等其他策略未画入，实际以系统决策规则为准。'),
'integrating-authorization':('统一入口与业务执行的责任分工',[
 ('user',0,0,'用户入口','选择应用与组织','actor'),('sdk',1,0,'界面与 SDK','菜单和动作展示','system'),('request',2,0,'业务请求','身份 + 动作 + 资源','data'),
 ('policy',2,1,'统一授权判断','核对范围与操作','gate'),('service',3,1,'业务服务','执行并返回结果','system'),('task',1,2,'后台任务','专用服务身份','actor')],
 [('user','sdk',''),('sdk','request',''),('request','policy',''),('task','policy',''),('policy','service','')],
 '应用集成示意。后台任务与用户请求使用各自的身份，执行侧均有授权边界。'),
'too-many-settings':('沿用户任务组织配置',[
 ('data',0,0,'确认数据','数据集 / 字段 / 时间','data'),('result',1,0,'得到基本结果','默认展示与反馈','system'),('style',2,0,'调整外观','字号 / 颜色 / 布局','data'),('advanced',3,0,'扩展行为','联动 / 自定义逻辑','gate')],
 [('data','result',''),('result','style',''),('style','advanced','按需进入')],
 '任务顺序示意，并非要求固定采用四个页签。影响数据含义的默认值需单独确认。'),
'reusing-data-and-interactions':('模板复用的显式依赖',[
 ('template',0,1,'模板定义','结构与参数声明','data'),('params',1,0,'页面参数','设备 / 时间范围','data'),('style',1,1,'外观配置','主题与布局','data'),('deps',1,2,'交互依赖','对象引用与事件','data'),
 ('bind',2,1,'实例化校验','绑定参数并检查依赖','gate'),('page',3,1,'目标页面','形成独立或关联实例','system')],
 [('template','params',''),('template','style',''),('template','deps',''),('params','bind',''),('style','bind',''),('deps','bind',''),('bind','page','')],
 '模板不是一张截图。参数、外观与交互分别检查，实例更新方式需要明确约定。'),
'a-product-expert-assistant':('产品专家助手需要的三类信息',[
 ('question',0,1,'用户问题','功能 / 状态 / 操作','actor'),('docs',1,0,'产品资料','版本与出处','data'),('context',1,1,'页面上下文','选中对象与当前模式','data'),('tools',1,2,'工具结果','实时状态与授权范围','data'),
 ('answer',2,1,'按证据处理','回答 / 澄清 / 提议动作','gate'),('verify',3,1,'结果核对','出处或实际变更状态','system')],
 [('question','docs',''),('question','context',''),('question','tools','按需读取'),('docs','answer',''),('context','answer',''),('tools','answer',''),('answer','verify','')],
 '功能方案示意。资料、现场状态和操作结果各自有来源，模型不能自行补齐缺失事实。'),
'rag-in-practice':('把检索增强拆成可排查的链路',[
 ('docs',0,0,'原始资料','版本 / 标题 / 来源','data'),('parts',1,0,'切分与索引','保留条件和上下文','system'),('query',0,1,'用户问题','附必要检索条件','actor'),('retrieve',1,1,'候选检索','先检查证据是否命中','system'),
 ('context',2,1,'组织上下文','选择与标注资料','gate'),('answer',3,1,'生成与核对','回答对应具体出处','system')],
 [('docs','parts',''),('parts','retrieve',''),('query','retrieve',''),('retrieve','context',''),('context','answer','')],
 '常见应用层实现的诊断示意，与原始论文的训练结构并不等同。'),
'a-verifiable-page-change':('一次页面变更的执行边界',[
 ('input',0,0,'指令 + 选区','确定目标对象','actor'),('intent',1,0,'形成变更','受约束的动作和参数','data'),('check',2,0,'执行前校验','权限 / 版本 / 语义','gate'),('apply',3,0,'应用变更','复用编辑器写入路径','system'),
 ('history',1,1,'变更历史','记录前后版本','data'),('readback',3,1,'读回与展示','核对结果或报告部分失败','system')],
 [('input','intent',''),('intent','check',''),('check','apply',''),('apply','readback',''),('apply','history','')],
 '设计示意。撤销依赖真实变更历史，版本冲突需要另行处理，不能盲目覆盖旧快照。'),
'low-code-after-generation':('三条生成路线与共同交付边界',[
 ('task',0,1,'同一个任务','创建、修改并交付看板','actor'),('manual',1,0,'人工配置','编辑器 → 配置','system'),('schema',1,1,'AI 生成配置','约束校验 → 渲染器','system'),('code',1,2,'AI 生成代码','自由布局与交互','system'),
 ('contract',2,1,'共同约束','数据 / 身份 / 版本','gate'),('delivery',3,1,'持续使用','修改、发布、维护','data')],
 [('task','manual',''),('task','schema',''),('task','code',''),('manual','contract',''),('schema','contract',''),('code','contract',''),('contract','delivery','')],
 '路线比较图。评价范围覆盖后续维护，并非只比较第一次生成速度。'),
'why-the-stream-stalled':('逐层定位流式响应停顿',[
 ('upstream',0,0,'上游任务','是否产生第一条事件','system'),('backend',1,0,'应用服务','是否及时写入并刷新','system'),('proxy',2,0,'代理链路','缓冲 / 压缩 / 超时','gate'),('browser',3,0,'浏览器','事件解析与界面更新','actor'),
 ('direct',1,1,'直接观察后端','记录接收时间与边界','data'),('full',2,1,'观察完整路径','比较同条件事件到达','data')],
 [('upstream','backend',''),('backend','proxy',''),('proxy','browser',''),('backend','direct','旁路验证'),('proxy','full','全链路验证')],
 '通用排查拓扑，不表示实际采样时序。分别记录产生、转发、接收与渲染。'),
'evaluating-ai-analysis-tools':('一份数据走到交付的检查点',[
 ('file',0,0,'输入数据','字段、单位与缺失','data'),('meaning',1,0,'确认计算口径','范围、粒度与聚合','gate'),('compute',2,0,'执行与中间结果','用已知答案核对','system'),('report',3,0,'报告与导出','保留数据依据','data'),
 ('change',2,1,'继续修改条件','检查会话约定是否保留','actor')],
 [('file','meaning',''),('meaning','compute',''),('compute','report',''),('report','change',''),('change','compute','再次验证')],
 '调研任务路径。中间结果与后续修改同样属于产品评估范围。'),
'agents-in-enterprise-systems':('Agent 与企业系统的接入分层',[
 ('user',0,0,'业务用户','应用与当前身份','actor'),('platform',1,0,'平台配置','Agent / 工具 / 知识','system'),('runtime',2,0,'Agent 运行','协议事件与任务状态','system'),
 ('auth',2,1,'工具执行边界','动作、资源与凭证','gate'),('business',3,1,'业务接口','结果与业务错误','data'),('audit',3,2,'关联记录','任务与执行证据','data')],
 [('user','platform',''),('platform','runtime',''),('runtime','auth',''),('auth','business',''),('business','audit','')],
 '逻辑分层示意，不对应某个实际网络拓扑。发现能力不等于获得业务权限。'),
'acp-and-platform-boundaries':('ACP 会话交互与平台责任',[
 ('client',0,0,'客户端','界面与用户选择','actor'),('protocol',1,0,'ACP 通信','会话、更新、权限请求','system'),('agent',2,0,'Agent 实现','内部框架与执行','system'),
 ('govern',1,1,'平台治理','身份、范围与审计','gate'),('tools',3,0,'工具和业务','按已授权身份调用','data')],
 [('client','protocol',''),('protocol','agent',''),('agent','tools',''),('govern','protocol','约束交互'),('govern','tools','约束执行')],
 '职责示意。协议消息约定与平台业务授权分别处理，具体能力按协议版本协商。'),
'from-alarm-to-report':('业务助手的证据与决策流程',[
 ('alarm',0,0,'读取告警详情','固定资源与时间范围','data'),('facts',1,0,'查询相关数据','区分缺失、失败、正常','system'),('analysis',2,0,'分析与候选方案','记录依据和不确定性','system'),
 ('review',2,1,'用户决策','批准、修改或补查','gate'),('act',3,1,'执行与读回','处理超时和重复提交','system'),('report',3,2,'处理报告','区分建议与实际结果','data')],
 [('alarm','facts',''),('facts','analysis',''),('analysis','review',''),('review','act',''),('act','report','')],
 '通用告警流程。演示连通性与长期业务验证是不同层次的证据。'),
'where-chat-belongs':('按任务选择交互入口',[
 ('user',0,1,'用户当前任务','看状态 / 做决定 / 共创','actor'),('cockpit',1,0,'业务驾驶舱','状态、告警与待处理','system'),('chat',1,1,'主对话工作区','长任务与产出物共创','system'),('assistant',1,2,'伴随式助手','解释当前页面内容','system'),('shared',2,1,'共同上下文','对象、权限与任务状态','data')],
 [('user','cockpit',''),('user','chat',''),('user','assistant',''),('cockpit','shared',''),('chat','shared',''),('assistant','shared','')],
 '交互形态的设计比较，不要求每种应用同时具备全部入口。'),
'conversation-to-recurring-work':('从一次对话到重复执行',[
 ('chat',0,0,'完成一次任务','确定计算与输出方式','actor'),('template',1,0,'沉淀模板','参数与输出约定','data'),('schedule',2,0,'定时或手动触发','固定执行身份与版本','system'),
 ('run',2,1,'独立执行记录','开始、进度、结束状态','system'),('artifact',3,1,'产出物与历史','关联输入与执行结果','data'),('feedback',1,2,'检查与修订','模板更新不改旧结果','gate')],
 [('chat','template',''),('template','schedule',''),('schedule','run',''),('run','artifact',''),('artifact','feedback',''),('feedback','template','')],
 '模板、任务和产出物各自有生命周期。暂停与补跑规则需要明确约定。'),
'delivering-an-ai-app':('从构建工作空间到可交付应用',[
 ('build',0,0,'构建工作空间','开发、试验与测试','actor'),('package',1,0,'发布模板','冻结版本与依赖声明','data'),('bind',2,0,'目标环境绑定','模型、工具与凭证槽位','gate'),('runtime',3,0,'用户运行实例','独立状态与访问入口','system'),
 ('check',2,1,'发布前验证','依赖、权限与运行检查','gate')],
 [('build','package',''),('package','bind',''),('bind','check',''),('check','runtime','')],
 '交付模型示意。模板携带依赖描述，目标环境提供实际凭证，用户运行状态独立保存。'),
'one-agent-per-user':('共享模板与每用户独立状态',[
 ('template',0,1,'发布模板 vN','指令与依赖声明','data'),('a',1,0,'用户 A 实例','会话、文件与执行状态','system'),('b',1,2,'用户 B 实例','会话、文件与执行状态','system'),
 ('idA',2,0,'用户 A 授权','当前允许的业务范围','gate'),('idB',2,2,'用户 B 授权','当前允许的业务范围','gate'),('api',3,1,'共享业务服务','逐次校验身份与动作','data')],
 [('template','a','启用'),('template','b','启用'),('a','idA',''),('b','idB',''),('idA','api',''),('idB','api','')],
 '实例隔离与业务授权是两层边界，独立会话不能替代接口侧的权限判断。'),
'page-context-and-agent':('页面选区与 Agent 的双向交互',[
 ('page',0,0,'页面选区','对象、筛选与数据引用','actor'),('bridge',1,0,'宿主消息桥','校验来源、实例和结构','gate'),('agent',2,0,'当前 Agent','提问、解释或请求动作','system'),
 ('command',2,1,'受限界面命令','定位、高亮或刷新','data'),('result',0,1,'页面回执','当前实例的处理结果','system')],
 [('page','bridge','用户确认'),('bridge','agent',''),('agent','command',''),('command','bridge',''),('bridge','result','')],
 '交互协议示意。页面传入数据是上下文，不自动构成业务授权。'),
'building-an-agent-team':('构建台与运行团队分离',[
 ('owner',0,0,'构建者','用业务语言描述目标','actor'),('builder',1,0,'构建助手','维护同一份草稿','system'),('draft',2,0,'蓝图与差异','角色、依赖与审批策略','data'),('apply',3,0,'确认应用','版本化变更','gate'),
 ('runtime',3,1,'运行团队','使用已应用版本','system'),('manual',1,1,'表单编辑','精调同一草稿','actor')],
 [('owner','builder',''),('builder','draft',''),('manual','draft',''),('draft','apply',''),('apply','runtime','')],
 '产品方案示意。构建助手修改草稿，经确认的变更才进入运行配置。'),
'team-product-and-dependencies':('三种工作空间的生命周期',[
 ('team',0,0,'研发团队成员','开发、评审与测试','actor'),('staging',1,0,'产品测试实例','随产品版本验证','system'),('prod',1,2,'产品运行实例','服务业务用户','system'),('external',2,1,'外部依赖','由其他主体维护','data'),('binding',3,1,'显式依赖绑定','调用方 + 能力 + 环境','gate')],
 [('team','staging','开发与验证'),('team','prod','按授权发布'),('team','binding',''),('staging','binding',''),('prod','binding',''),('external','binding','')],
 '对象分类示意。成员身份、产品运行角色和依赖访问关系不混为一类。'),
'reliable-agent-handoffs':('带批准与证据的任务交接',[
 ('issue',0,0,'外部工作项','数据与任务入口','data'),('review',1,0,'有效人工批准','固定任务与操作范围','gate'),('dev',2,0,'开发阶段','产出版本与自查证据','system'),('qa',3,0,'验证阶段','检查指定版本与结果','system'),
 ('rework',2,1,'退回与重做','保留尝试记录','data'),('done',3,2,'完成与回写','按终态证据更新','gate')],
 [('issue','review',''),('review','dev',''),('dev','qa','交接'),('qa','rework','不通过'),('rework','dev',''),('qa','done','通过')],
 '通用状态流。外部标签或机器凭证不能代替人的批准，文件交付与任务流转分别验收。'),
'from-rbac-to-agent-delegation':('一次受约束的委托执行',[
 ('user',0,0,'用户意图','具体任务与当前身份','actor'),('scope',1,0,'委托范围','动作、资源和有效期','data'),('policy',2,0,'执行前判断','权限与必要审批','gate'),('business',3,0,'业务调用','使用对应身份和凭证','system'),
 ('audit',2,1,'证据与审计','谁批准、做了什么','data'),('readback',3,1,'结果核对','提交与生效分开','gate')],
 [('user','scope',''),('scope','policy',''),('policy','business',''),('business','readback',''),('policy','audit',''),('readback','audit','')],
 '委托执行模型示意。提示词中的“允许”不能替代执行侧校验。'),
'resource-runaway':('资源失控的扩散路径与控制点',[
 ('missing',0,0,'受支持接口缺失','工具路径返回失败','data'),('fallback',1,0,'Agent 自行探查','异常命令持续耗资源','system'),('unbounded',2,0,'缺少有效限制','资源压力越出工作负载','gate'),('impact',3,0,'宿主与其他服务','调度受阻、上游超时','data'),
 ('admission',1,1,'执行前预算','身份明确的资源预留','gate'),('limit',2,1,'运行时限制','内存、进程与持续观测','gate'),('recovery',3,1,'恢复与核对','确认终态再释放预算','gate')],
 [('missing','fallback',''),('fallback','unbounded',''),('unbounded','impact',''),('admission','limit',''),('limit','recovery','')],
 '依据事故记录抽象的因果链，环境标识与精确容量已省略。下方是分阶段治理方向。'),
'notes-to-personal-knowledge':('记录、结论与查询保持来源关系',[
 ('raw',0,0,'原始记录','保留日期和出处','data'),('weekly',1,0,'周记录与项目页','任务与阶段进展','system'),('facts',2,0,'可复用知识','事实、判断与草案分开','gate'),('query',3,0,'查询与引用','先找证据再作回答','actor'),
 ('proposal',2,1,'更新建议','明确差异与影响','data'),('review',1,1,'人工检查','确认后写入结论','gate')],
 [('raw','weekly',''),('weekly','facts',''),('facts','query',''),('query','proposal',''),('proposal','review',''),('review','facts','')],
 '个人知识库流程示意。原始材料保留，新的结论不覆盖历史依据。'),
}

COLORS={'actor':('#e9efe7','#45634c'),'data':('#f6f0e4','#856345'),'system':('#eef0eb','#53645a'),'gate':('#f3e9e0','#955b35')}
def svg(slug,graph):
 title,nodes,edges,caption=graph;node_by_id={n[0]:n for n in nodes};cols=max(n[1] for n in nodes)+1;rows=max(n[2] for n in nodes)+1
 dx,dy,w,h,pad=290,145,184,68,28;width=pad*2+(cols-1)*dx+w;height=pad*2+(rows-1)*dy+h
 def pos(n):return pad+n[1]*dx,pad+n[2]*dy
 parts=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc"><title id="title">{escape(title)}</title><desc id="desc">{escape(caption)}</desc><defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 Z" fill="#8b9587"/></marker></defs><rect width="100%" height="100%" fill="#fffefa"/>']
 for a,b,label in edges:
  na,nb=node_by_id[a],node_by_id[b];ax,ay=pos(na);bx,by=pos(nb)
  if nb[1]>na[1]:
   x1,y1=ax+w,ay+h/2;x2,y2=bx,by+h/2
   mid=(x1+x2)/2;d=f'M{x1},{y1} C{mid},{y1} {mid},{y2} {x2-5},{y2}'
  elif nb[1]<na[1]:
   x1,y1=ax,ay+h/2;x2,y2=bx+w,by+h/2;mid=(x1+x2)/2;d=f'M{x1},{y1} C{mid},{y1} {mid},{y2} {x2+5},{y2}'
  else:
   x1,y1=ax+w/2,ay+(h if nb[2]>na[2] else 0);x2,y2=bx+w/2,by+(0 if nb[2]>na[2] else h);d=f'M{x1},{y1} L{x2},{y2-(5 if nb[2]>na[2] else -5)}'
  parts.append(f'<path d="{d}" fill="none" stroke="#8b9587" stroke-width="1.4" marker-end="url(#arrow)"/>')
  if label:
   mx,my=(x1+x2)/2,(y1+y2)/2-7
   parts.append(f'<text x="{mx}" y="{my}" text-anchor="middle" font-size="10" fill="#6f786c" font-family="sans-serif">{escape(label)}</text>')
 for n in nodes:
  x,y=pos(n);fill,stroke=COLORS[n[5]]
  parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="5" fill="{fill}" stroke="{stroke}" stroke-opacity=".35"/><text x="{x+w/2}" y="{y+28}" text-anchor="middle" font-family="sans-serif" font-size="14" font-weight="600" fill="#303f34">{escape(n[3])}</text><text x="{x+w/2}" y="{y+49}" text-anchor="middle" font-family="sans-serif" font-size="11" fill="#70766c">{escape(n[4])}</text>')
 return ''.join(parts)+'</svg>',width,height

def insert_diagram(post,rendered,out):
 slug=post['slug']
 if slug not in GRAPHS:return rendered
 graph=GRAPHS[slug];image,width,height=svg(slug,graph)
 target=out/'assets'/'diagrams'/f'{slug}.svg';target.parent.mkdir(parents=True,exist_ok=True);target.write_text(image)
 src=f'/blog/assets/diagrams/{slug}.svg'
 figure=f'<figure class="diagram"><div class="diagram-head"><strong>{escape(graph[0])}</strong><a href="{src}" target="_blank" rel="noopener">放大图示 ↗</a></div><div class="diagram-scroll"><img src="{src}" alt="{escape(graph[0],quote=True)}" width="{width}" height="{height}" loading="lazy"></div><figcaption>{escape(graph[3])}</figcaption></figure>'
 marker='<h2 '
 i=rendered.find(marker)
 return rendered[:i]+figure+rendered[i:] if i>=0 else figure+rendered
