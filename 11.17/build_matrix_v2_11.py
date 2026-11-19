"""Replace part three with six focused platform capability planning slides."""
from pathlib import Path
from html import escape as E
import json

ROOT=Path(__file__).parent
old=json.loads((ROOT/'matrix_planning_v2_10_content.json').read_text())
base=(ROOT/'matrix_planning_v2_10.html').read_text()
serial=500
def text(x,y,t,size=23,color='#173642',anchor='start'):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" text-anchor="{anchor}">{E(t)}</text>'
def box(x,y,w,h,title,lines=(),kind='normal'):
    fill,stroke,ink={'normal':('#edf1ed','#b9c8c2','#173642'),'dark':('#173642','#173642','#fff'),'teal':('#dfeee7','#17847a','#173642'),'orange':('#f7e7db','#c76b43','#593c2e')}[kind]
    s=f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>'
    s+=f'<text x="{x+22}" y="{y+35}" font-size="25" fill="{ink}" font-weight="650">{E(title)}</text>'
    for i,t in enumerate(lines):s+=text(x+22,y+72+32*i,t,22,ink)
    return '<g class="diagram-node">'+s+'</g>'
def arrow(x1,y1,x2,y2):return f'<path d="M{x1},{y1}L{x2},{y2}" stroke="#17847a" stroke-width="2.7" fill="none" marker-end="url(#ARR)"/>'
def route(d):return f'<path d="{d}" stroke="#17847a" stroke-width="2.7" fill="none" marker-end="url(#ARR)"/>'
def svg(label,s,h=500):
    global serial
    serial+=1
    return f'<svg class="diagram" viewBox="0 0 1440 {h}" role="img" aria-label="{E(label)}"><defs><marker id="arr{serial}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0L10,5L0,10Z" fill="#17847a"/></marker></defs>'+s.replace('#ARR',f'#arr{serial}')+'</svg>'
def note(t):return '<div class="takeaway">'+t+'</div>'
def deliver(a,b,c):return '<div class="deliver">'+''.join(f'<div><b>{k}</b><span>{v}</span></div>' for k,v in [('形成成果',a),('重点支撑',b),('验证与采用',c)])+'</div>'
def page(n,title,lead,body,notes):return dict(chapter=f'第3部分 / 3.{n} '+['能力建设总览','场景服务定义范式','车控Agent外部交互语义','通信中间件基础能力需求','基础服务自适应编排','团队与资源安排'][n-1],title=title,lead=lead,body=body,notes=notes,part=3,cover=False)

agenda='<nav class="chapter-agenda" aria-label="第三部分目录">'+''.join(f'<a href="#s{n}"><b>3.{i}</b><span>{E(title)}</span></a>' for i,(n,title) in enumerate([
    (9,'能力建设总览'),(10,'场景服务定义范式'),(11,'外部交互语义'),(12,'中间件基础能力需求'),(13,'自适应编排能力建设'),(14,'团队与资源安排')],1))+'</nav>'
overview=page(1,'支撑车控Agent，提升四项关键平台能力',
    '第三部分：明确建设目标、现有差距、建设方案，以及所需团队和资源。',
    agenda+'<div class="support-map">'+''.join(f'<article><div class="support-need"><b>{i}</b><div><h3>{a}</h3><p>{b}</p></div></div><i>→</i><div class="support-build"><h3>{c}</h3><p>{d}</p></div></article>' for i,a,b,c,d in [
      ('01','场景服务定义范式','统一描述场景功能与使用规则','支撑场景定义与接入','成果：共用模板、评审要求和参考实例'),
      ('02','车控Agent外部交互语义','明确使用方与Agent怎样交互','支撑NOMI等入口与接入层','成果：请求、状态、结果与取消交互规范'),
      ('03','通信中间件基础能力需求','将运行要求转化为平台建设依据','支撑控制分发与执行反馈','成果：机制及性能需求、改进与验证方案'),
      ('04','基础服务自适应编排能力建设','为受约束的组合提供共同基础','支撑协调、任务管理与系统服务','成果：能力描述、组合规则和查询验证工具')])+'</div>'+
    note('执行条件、保护边界与结果确认贯穿四项建设；共性验证与工程采用纳入各项成果。'),
    '本页合并原第三部分导览与总览，不再单设分隔页。四项能力是矩阵的建设方向，不替代车控Agent业务策略或独立软件架构职责。后续差距表述区分已知IDL不足和待联合调研范围。')

definition=page(2,'场景服务定义范式：明确功能与执行边界',
    '目标：每个场景都能说明提供什么功能、何时可以使用、怎样运行退出，以及如何判断结果。',
    svg('场景服务定义的基础差距与建设方案',
      box(25,25,385,430,'现有基础与待补充',['已有IDL、场景参数和状态接口','部分行为说明在IDL中不完整','进入、保持及退出规则需核实','需核查跨场景说明的一致性'])+
      box(510,80,265,200,'共用模板',['功能与范围','条件与执行约束','运行、退出与异常'],'dark')+
      box(835,80,265,200,'评审要求',['责任边界','状态与结果','兼容与验证'])+
      box(1160,80,255,200,'参考试点',['参考AiCabin','补齐使用说明','按需改造接口'],'teal')+
      arrow(410,170,500,170)+arrow(775,170,825,170)+arrow(1100,170,1150,170)+
      box(510,355,905,100,'建设成果',['场景设计规范、参考定义、评审清单及必要的接口改造']))+
    deliver('共用定义与设计评审方法','场景设计、接入及系统实现','先补完整说明，再按真实缺口改造IDL'),
    '已有AiCabin场景请求、取消表达、推荐与状态接口。已知当前IDL对result取值、部分偏好适用和逐请求反馈等说明不足；不推断公司全部功能文档缺失。以联合调研确认完整差距，具体业务策略由FO/SO/VCC负责。')

interaction=page(3,'车控Agent外部交互语义：统一请求与执行反馈',
    '目标：使用方能够明确发起、跟踪、调整和结束任务，正确理解实际执行结果。',
    svg('外部交互与待核查差距及建设方案',
      box(25,0,365,60,'NOMI、手机及其他入口')+
      box(1040,0,375,60,'车控Agent接入层',kind='dark')+
      '<path d="M205,75 V295 M1225,75 V295" stroke="#bacbbf" stroke-dasharray="6 6"/>'+
      arrow(205,115,1225,115)+text(715,100,'场景请求或明确的基础能力请求',23,'#17847a','middle')+
      arrow(1225,195,205,195)+text(715,180,'接受或拒绝；执行进度与结果',23,'#17847a','middle')+
      arrow(205,275,1225,275)+text(715,260,'修改或取消请求',23,'#17847a','middle')+
      box(25,335,650,160,'待核查差距',['请求关联、部分完成与退出确认是否完整','重复请求、取消及多入口规则是否一致'])+
      box(765,335,650,160,'建设方案',['分别定义场景与基础能力交互','统一任务响应、状态与结果语义','形成典型时序及参考接口说明'],'teal'),h=520)+
    deliver('外部交互规范、时序与参考接口','用户意图识别层与Agent接入层','接受不等于完成，取消请求不等于已停止'),
    '本页区别于场景定义：定义使用方与服务之间的交互，而非重述场景内部策略。基于已有接口核查任务关联、取消对象、部分结果等是否足够，不直接宣称现有框架均不支持。图示第三条为修改/取消请求，实际处理结果沿向上的反馈通道返回。')

middleware=page(4,'通信中间件基础能力：以场景运行要求牵引提升',
    '目标：可靠传递控制、状态与结果，满足异常处置所需时序，并合理使用资源。',
    svg('中间件能力需求评估与建设过程',
      box(25,25,420,310,'现有基础与待核查',['已有SOA通信和运行机制','核查状态时效与响应要求','评估并发、通信异常及恢复','核对计算、存储和通信开销'])+
      box(510,25,420,310,'建设方案',['从真实场景形成运行需求','分析机制、性能和资源差距','优先配置优化与能力复用','确有缺口时扩展框架'],'dark')+
      box(995,25,420,310,'建设成果',['中间件需求清单','性能与资源要求','平台改进方案','联合验证结论'],'teal')+
      arrow(445,175,500,175)+arrow(930,175,985,175)+
      box(25,405,1390,65,'共同验证：条件变化通知、中断退出确认、通信故障与恢复，以及执行效率'))+
    deliver('有业务来源的平台机制与性能需求','各层控制分发、执行反馈与异常协调','系统保护独立保留，平台方案联合验收'),
    '场景协调不替代本域实时保护。具体需求可涉及服务可用性、事件/状态传递、请求关联、队列、QoS、端到端时序和失效行为。现有能力是否满足须通过目标环境测量。不预设新协议或中间件，不编造性能数字。')

composition=page(5,'基础服务自适应编排：建设能力与约束的共同基础',
    '目标：基础服务可识别、可组合，车控Agent能够在允许范围内选择方案并按变化调整。',
    svg('基础服务自适应编排的差距与共用建设',
      box(25,25,405,410,'现有基础与待核查',['已有系统服务与部分高层能力','部分接口仍依赖设备和信号','核查适用条件、依赖与冲突','核查执行限制及反馈完整性'])+
      box(520,25,405,155,'完善基础能力信息',['提炼功能与稳定能力接口','明确条件、限制和执行反馈'],'dark')+
      box(520,290,405,155,'建立组合规则',['说明依赖、冲突及允许范围','支持变化后的重新判断'])+
      box(1015,150,400,200,'形成共用工具与参考实现',['能力查询、依赖与约束检查','场景组合验证与参考编排','供VCC及相关团队采用'],'teal')+
      route('M430,195 H475 V100 H510')+route('M475,195 V365 H510')+
      arrow(925,100,1005,205)+arrow(925,365,1005,295))+
    note('矩阵建设描述、规则与工具；系统供给能力和约束；VCC负责具体场景的方案选择与运行决策。'),
    '原平台IDL显示抽象层次不一，部分仍体现底层布局，已有空间与热舒适高层接口应复用。矩阵不包办Agent规划算法，也不将基础服务改造成自由调用且无约束的动作库。参考实现不预设新增独立运行平台。')

resources=page(6,'团队与资源：按专题共建，明确投入与维护责任',
    '四项能力需要业务、系统和平台共同建设，并落实到责任人、参与时间和验证环境。',
    svg('共建团队与所需资源',
      box(25,10,420,270,'业务与系统共建',['VCC、NOMI等使用方代表','FO：需求、规则及验收条件','SO：系统能力与执行边界','车型AI：配置与车型适用性'])+
      box(510,10,420,270,'平台与工程建设',['SOA专业负责人','平台及领域软件架构师','系统、平台和工具SWE','完成规范、评估和必要实现'],'dark')+
      box(995,10,420,270,'验证与工程采用',['测试与业务联合验证','TPM协调依赖、责任与节点','DO在集成发布时参与','采用团队提供实际反馈'],'teal')+
      box(25,365,650,125,'所需资源',['明确的参与时间、试点和实现资料','工具开发投入与集成、台架验证环境'])+
      box(765,365,650,125,'运营与维护',['每项成果明确建设和维护责任人','投入数量与排期由责任团队评估确认']))+
    note('虚拟矩阵组织共性建设；不替代业务开发、系统保护责任或独立软件架构组织。'),
    '本页明确资源种类和协作责任，不编造人数、工时或交付日期。各专题应有业务负责人、技术负责人、采用团队、评审/验证出口及成果维护安排。平台与领域架构师按既有组织分工协作。')

replacement=[overview,definition,interaction,middleware,composition,resources]
slides=old[:8]+replacement+old[17:]
cover=slides[0].copy();cover['chapter']=cover['chapter'].replace('V2.10','V2.11');cover['body']=cover['body'].replace('V2.10','V2.11');slides[0]=cover
assert len(slides)==23
assert len([s for s in slides if s.get('part')==3])==6
assert slides[14:]==old[17:]
assert slides[1:8]==old[1:8]
# The user additionally requested the chapter directory entries to be updated.
# Only the third-part label within each transition page navigation is changed.
for i,s in enumerate(slides):
    if s.get('divider'):
        s=s.copy();s['body']=s['body'].replace('<b>矩阵平台能力建设</b>','<b>矩阵关键能力建设</b>');slides[i]=s
before,tail=base.split('<main>',1);_,after=tail.split('</main>',1)
rendered=[]
for i,s in enumerate(slides,1):
    tag='h1' if s['cover'] else 'h2';cls='slide'+(' cover' if s['cover'] else '')+(' part-divider' if s.get('divider') else '')
    rendered.append(f'<section class="{cls}" id="s{i}" data-title="{E(s["title"].replace("<br>"," "),quote=True)}" data-chapter="{E(s["chapter"],quote=True)}" data-part="{s.get("part",0)}" aria-labelledby="t{i}"><div class="eyebrow"><span>{i:02}</span>{E(s["chapter"])}</div><{tag} id="t{i}">{s["title"]}</{tag}><p class="lead">{E(s["lead"])}</p><div class="body">{s["body"]}</div><aside class="notes">{E(s["notes"])}</aside></section>')
css='''.chapter-agenda{display:grid;grid-template-columns:repeat(6,1fr);gap:.65vw;flex-shrink:0}.chapter-agenda a{border-top:2px solid var(--teal);background:#e6ece0;padding:.7vh .6vw;display:flex;gap:.55vw;align-items:center;font-size:clamp(10px,.83vw,16px);line-height:1.45}.chapter-agenda b{color:var(--teal);font-weight:500}.chapter-agenda a:hover{background:#d6e7d0}@media(max-width:800px){.chapter-agenda{grid-template-columns:1fr 1fr;gap:8px}.chapter-agenda a{padding:10px;font-size:11px}}@media print{.chapter-agenda a{font-size:8pt;padding:1.5mm}.chapter-agenda{gap:2mm}}'''
html=(before+'<main>'+''.join(rendered)+'</main>'+after).replace('V2.10','V2.11').replace('</style>',css+'</style>')
ROOT.joinpath('matrix_planning_v2_11.html').write_text(html)
ROOT.joinpath('matrix_planning_v2_11_content.json').write_text(json.dumps(slides,ensure_ascii=False,indent=2)+'\n')
ROOT.joinpath('matrix_v2_11_revision_notes.md').write_text('''# V2.11 第三部分六页改版

仅替换V2.10原第9—17页第三部分，合并分隔页与总览，替换为六页：关键能力总览、场景服务定义范式、车控Agent外部交互语义、通信中间件基础能力需求、基础服务自适应编排能力建设、团队与资源安排。现为第9—14页。

每项展开包含目标、现有基础与待核查差距、建设方案、成果与采用对象。区分已知IDL说明不足和待调研范围，不宣称全部能力缺失。编排共用基础由矩阵组织建设，业务规划决策保留在VCC。

第一、二部分正文与第四、五部分正文逐项保持一致，页号自动调整；用户追加要求后，仅将各分隔页底部导航中的第三部分名称改为矩阵关键能力建设。封面与页眉仅更新版本。全稿23页，五部分保留，第三部分不额外占分隔页；首张总览提供六个可点击目录条目。

团队包含业务/系统/平台/软件架构/实现/验证及TPM、按需DO；资源说明参与时间、试点资料、工具投入和集成台架环境，不编造数量与排期。独立发布matrix-v211。
''')
print(json.dumps({'slides':len(slides),'part_three_pages':[9,10,11,12,13,14],'outside_part_three_preserved':True,'bytes':len(html.encode())}))
