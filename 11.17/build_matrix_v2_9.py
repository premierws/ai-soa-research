"""Integrate agent responsibilities, execution constraints and COE support."""
from pathlib import Path
from html import escape as E
import json
import re

ROOT=Path(__file__).parent
old=json.loads((ROOT/'matrix_planning_v2_8_content.json').read_text())
base=(ROOT/'matrix_planning_v2_8.html').read_text()
slides=[];serial=300
def text(x,y,t,size=23,color='#173642',anchor='start'):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" text-anchor="{anchor}">{E(t)}</text>'
def box(x,y,w,h,title,lines=(),kind='normal'):
    fill,stroke,ink={'normal':('#edf1ed','#b9c8c2','#173642'),'dark':('#173642','#173642','#fff'),'teal':('#dfeee7','#17847a','#173642'),'orange':('#f7e7db','#c76b43','#593c2e')}[kind]
    s=f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>'
    s+=f'<text x="{x+22}" y="{y+35}" font-size="25" font-weight="650" fill="{ink}">{E(title)}</text>'
    for i,t in enumerate(lines):s+=text(x+22,y+72+32*i,t,22,ink)
    return '<g class="diagram-node">'+s+'</g>'
def arrow(x1,y1,x2,y2):return f'<path d="M{x1},{y1} L{x2},{y2}" stroke="#17847a" stroke-width="2.7" fill="none" marker-end="url(#ARR)"/>'
def route(d):return f'<path d="{d}" stroke="#17847a" stroke-width="2.7" fill="none" marker-end="url(#ARR)"/>'
def svg(label,s,h=500):
    global serial
    serial+=1
    return f'<svg class="diagram" viewBox="0 0 1440 {h}" role="img" aria-label="{E(label)}"><defs><marker id="arr{serial}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0L10,5L0,10Z" fill="#17847a"/></marker></defs>'+s.replace('#ARR',f'#arr{serial}')+'</svg>'
def note(t):return '<div class="takeaway">'+t+'</div>'
def deliver(a,b,c):return '<div class="deliver">'+''.join(f'<div><b>{k}</b><span>{v}</span></div>' for k,v in [('矩阵建设',a),('共同参与',b),('支持业务',c)])+'</div>'
def new(title,lead,body,notes=''):
    return dict(title=title,lead=lead,body=body,notes=notes,cover=False)
def reuse(n,title=None,lead=None,replacements=(),extra=None):
    s=old[n-1].copy();s.pop('divider',None)
    if title:s['title']=title
    if lead:s['lead']=lead
    for a,b in replacements:s['body']=s['body'].replace(a,b)
    if extra is not None:
        s['body']=re.sub(r'<div class="takeaway">.*?</div>',note(extra),s['body'])
    return s

agent=new('车控Agent：理解车辆条件，协调场景并跟踪结果',
 '在NOMI理解和表达用户需求的基础上，减少反复调节与跨系统协调负担。',
 svg('车控Agent业务过程与持续反馈',
   ''.join(box(x,45,250,165,t,ls,'dark' if i==2 else 'normal') for i,(x,t,ls) in enumerate([
     (25,'理解当前状态',['乘员、空间与环境','系统能力与执行限制']),
     (310,'判断需求',['接收明确请求','识别场景与所需效果']),
     (595,'组织执行方案',['选择适用功能','检查条件与系统冲突']),
     (880,'管理场景运行',['协调系统任务','处理变化与异常']),
     (1165,'跟踪实际结果',['判断完成范围','反馈并按需调整'])]))+
   ''.join(arrow(x,125,x+25,125) for x in [280,565,850,1135])+
   route('M1290,210 V360 H1005 V220')+
   box(25,305,770,125,'系统产品提供执行基础',['本域控制、执行校验与保护持续保留'],'teal')+
   text(1060,395,'持续状态与执行反馈',23,'#17847a'),h=470)+
 note('预定义与自适应组合服务于上述过程；简单规则、自动控制与已有记忆能力继续复用。'),
 '依据VCC功能块的状态表达、意图理解、任务管理、跨域规划与系统反馈归纳。不要求所有过程由大模型实现，也不据此证明必须新增独立软件部署。')

boundary=new('车控Agent管理整体场景，系统执行层保留本域保护',
 '系统状态与执行限制，是场景进入和持续运行判断的重要依据。',
 svg('交互入口、场景管理与系统执行的责任边界',
   box(25,15,370,180,'NOMI等交互入口',['理解需求与偏好','必要时确认并解释结果','其他入口遵循同一场景规则'])+
   box(530,15,400,180,'车控Agent',['判断整体场景能否进入','管理协同、调整与退出','汇总结果并向入口反馈'],'dark')+
   box(1065,15,350,180,'系统执行层',['提供状态、限制和结果','校验本域执行条件','完成控制与实时保护'],'teal')+
   arrow(395,105,520,105)+arrow(930,105,1055,105)+
   route('M1240,195 V295 H730 V205')+
   text(1010,280,'状态、限制、故障及保护反馈',22,'#17847a','middle')+
   box(25,365,1390,100,'分层负责、持续配合',['场景检查通过不替代系统校验；系统需要立即保护时，不等待车控Agent批准']),h=490)+
 note('具体检测、响应时间和失效行为按功能要求分配；权限由相应可信机制核验。'),
 '基于用户明确的边界与VCC规划：Agent管理整体任务，系统保留域内执行及保护。不是将所有风险判断集中到Agent。')

lifecycle=new('进入前判断、执行中协调、退出后确认',
 '条件与风险会随执行变化，场景需要持续获得系统反馈。',
 svg('场景全过程中的Agent与系统交互',
   text(25,32,'车控Agent：整体场景管理',24,'#17847a')+
   box(25,65,420,145,'进入前',['检查场景所需条件与限制','不满足时不进入并说明原因'],'dark')+
   box(510,65,420,145,'执行中',['判断状态变化影响哪些任务','按规则调整、部分中断或退出'],'dark')+
   box(995,65,420,145,'退出后',['确认系统实际处理结果','明确剩余功能与控制权'],'dark')+
   arrow(445,138,500,138)+arrow(930,138,985,138)+
   box(25,325,420,140,'系统提供依据',['功能可用性、空间与乘员状态','执行条件和当前限制'])+
   box(510,325,420,140,'系统持续校验与反馈',['运行状态、故障和保护变化','必要时执行本域限制或停止'],'teal')+
   box(995,325,420,140,'系统返回实际结果',['已完成、受限、停止或失败','反馈原因和当前状态'])+
   arrow(235,325,235,220)+arrow(720,325,720,220)+arrow(1205,325,1205,220))+
 note('中断或退出请求发出，不等于系统已经停止；条件恢复后，是否恢复场景需要重新判断。'),
 '三列是责任和信息交互概览，不是一套适用于所有接口的强制状态机。退出后的保持、释放或恢复行为由业务与系统明确。')

abnormal=new('故障或条件变化时，按影响范围处理场景',
 '必须遵守的限制决定执行边界；舒适度等目标在允许范围内协调优化。',
 svg('异常情况下的场景处置选择',
   box(25,155,330,170,'获得系统状态与限制',['空间干涉、乘员状态','故障、保护和功能可用性','检查信息有效性与时效'],'dark')+
   box(500,155,400,170,'车控Agent判断整体影响',['按业务明确的处置规则','识别受影响目标与可行范围','保留系统保护决定'])+
   arrow(355,240,490,240)+
   box(1045,5,370,115,'不满足进入条件',['不进入场景，反馈原因'],'orange')+
   box(1045,190,370,115,'运行中部分受影响',['按规则调整或部分继续'],'teal')+
   box(1045,375,370,115,'必须结束的情况',['中断或退出，确认并提示'])+
   route('M900,205 H965 V65 H1035')+arrow(900,240,1035,240)+route('M900,285 H965 V435 H1035'))+
 note('不同异常不统一按“全部退出”处理；信息不足时采用业务规定的处置，不把未知当成可执行。'),
 '空间限制与保护可能属于硬约束，舒适度通常为优化目标；乘员状态为判断依据，其可靠性和推导规则需明确。系统本域保护不依赖本图决策链。')

support=new('把执行约束与结果确认，融入四项平台提升',
 '状态与约束服务作为共同基础，支撑接口封装、可靠协同及自适应组合。',
 '<div class="common-base"><b>共同基础：可使用的状态与约束信息</b><span>空间关系、乘员状态、功能限制及其有效性和时效</span></div>'+
 '<div class="support-four">'+''.join(f'<article><span>{i}</span><h3>{a}</h3><p>{b}</p></article>' for i,a,b in [
   ('01','服务升级与封装','明确能力范围、进入保持条件、保护责任和结果说明。'),
   ('02','高效可靠协同','协调依赖与资源，满足状态更新、异常响应和退出确认要求。'),
   ('03','自适应交互支撑','完善条件变化、限制执行、中断取消与结果反馈的交互。'),
   ('04','边界内动态组合','依据当前能力与约束选择方案，并在变化后重新判断。')])+'</div>'+
 '<div class="common-base light"><b>共同验证：正常、受限、异常与恢复</b><span>用依赖分析、过程追踪和联合测试，验证场景及系统行为</span></div>',
 '保留此前四个建设方向，将状态约束和验证作为横向共同基础，不重新造一套并列能力分类。矩阵牵引规范、方法与工具，系统和平台实施，VCC采用。')

state=new('完善状态与约束服务，让场景判断有可靠依据',
 '把分散的状态组织成业务可使用的信息，明确能力覆盖与使用边界。',
 svg('状态和约束信息供给及责任',
   box(25,25,405,340,'系统与感知信息',['空间位置和干涉关系','乘员占位、姿态等状态','系统故障、功能与保护状态','提供方对相应信息负责'])+
   box(520,25,405,340,'共用服务与使用说明',['统一对象、含义和作用范围','说明有效性、时效与限制','明确变化通知和信息不足处理','由相关团队维护'],'teal')+
   box(1015,25,400,340,'车控Agent使用',['判断进入与保持条件','识别跨系统冲突','选择允许方案并跟踪变化','不能取代系统本域保护'],'dark')+
   arrow(430,195,510,195)+arrow(925,195,1005,195))+
 deliver('状态与约束规范、服务差距及共用查询','SO/FO、感知、系统、平台与架构团队','场景判断采用一致且适用的信息'),
 '已有CabinSpacePlanner定义空间检查、干涉、腿部/头部空间及舒适度相关接口。需要核查覆盖范围、精度、更新速度和失效行为，接口存在不等于符合某项保护要求。矩阵不包办感知或空间算法。')

runtime=new('用运行要求保障状态反馈与异常处置',
 '按功能明确时序与通信要求，使场景协调和系统保护各自有效工作。',
 svg('业务运行要求到平台方案与联合验收',
   box(25,20,420,170,'业务与系统提出要求',['状态变化多快需要被获知','限制或中断如何反馈确认','失联、重启后各方怎样处理'],'dark')+
   box(510,20,420,170,'平台与架构团队评估',['复用或完善通信和调度机制','评估响应、可靠性和资源','明确职责及失效处理方案'])+
   box(995,20,420,170,'联合验证与业务采用',['验证条件变化和故障响应','核对实际系统处理结果','确认平台机制满足业务要求'],'teal')+
   arrow(445,105,500,105)+arrow(930,105,985,105)+
   box(25,320,650,130,'效率与资源优化',['在功能及安全要求下优化顺序、并行和开销'])+
   box(765,320,650,130,'保护与场景协调分层',['本域及时保护；Agent协调整体影响及退出']))+
 note('矩阵推动可验证的运行要求；不预设所有处置都经过Agent，也不以新协议替代功能设计。'),
 '运行要求可涉及状态时效、请求反馈关联、事件通知、并发和队列、通信异常、休眠唤醒等。具体指标按功能确认，无统一性能数字或全局最优承诺。')

validation=new('验证重点：受限和异常情况下，场景仍能正确处理',
 '除了正常完成，还要验证不能执行、必须停止和无法确认时的行为。',
 svg('跨系统联合验证范围',
   box(25,155,330,165,'从真实场景及约束出发',['明确条件、目标与限制','区分场景协调和系统保护','形成可判断的预期行为'],'dark')+
   box(510,0,420,130,'进入前不满足条件',['检查拒绝或不进入的行为','确认原因能被反馈'])+
   box(510,185,420,130,'执行中发生变化',['干涉、故障、人工介入','检查调整与保护行为'],'teal')+
   box(510,370,420,130,'信息或执行反馈异常',['延迟、缺失、矛盾与失联','检查未知、中断与恢复规则'],'orange')+
   box(1085,155,330,165,'检查整体与系统结果',['约束是否被遵守','退出是否得到确认','是否准确反馈实际结果'])+
   route('M355,205 H430 V65 H500')+arrow(355,240,500,240)+route('M355,285 H430 V435 H500')+
   route('M930,65 H1015 V205 H1075')+arrow(930,250,1075,250)+route('M930,435 H1015 V290 H1075'))+
 deliver('共用场景用例、过程追踪与回归方法','VCC、系统、平台、测试及架构团队','不误报完成，不漏掉跨系统异常影响'),
 '主机、SDK、台架和实车验证分层提供证据。矩阵组织验证方法和工具，具体安全与功能验收由责任团队按项目要求完成，不保证所有风险由单个工具消除。')

goal=reuse(3,lead='在NOMI理解和表达用户需求的基础上，提高车辆对实际使用条件的适应能力。',
 extra='减少反复调节与跨系统协调负担，使体验更合适、稳定、可控；组合与编排是实现手段。')
cap=reuse(7,extra='矩阵组织能力封装与边界评审；系统保留执行校验与保护，并提供场景所需状态和结果。')
cap['notes']+=' 场景及系统能力要说明进入、保持条件和执行限制，不因上层已有检查取消本域检查。'
interface=reuse(8,replacements=[('明确冲突、人工介入及退出后处理','明确保护责任、人工介入与退出确认')])
adaptive=reuse(13,lead='支持当前条件查询、执行限制通知，以及中断退出后的实际结果确认。',
 replacements=[('持续反馈执行状态、结果与原因','反馈执行状态、限制、保护及实际结果'),('根据变化调整或结束任务','根据变化调整或退出，并确认结果')])
dynamic=reuse(15,lead='基于当前系统能力与执行限制组织方案，条件变化后重新判断可行范围。',
 replacements=[('功能、适用条件、依赖与冲突','功能、保持条件、限制与冲突'),('检查约束，按变化调整','持续检查条件，按规则调整'),('反馈结果或限制','反馈结果、限制或保护')])

welcome=reuse(17,lead='从状态与执行限制出发管理迎宾任务，系统完成本域控制并反馈结果。',
 replacements=[('形成用户接近的上下文','提供进入判断所需信息'),('识别上车场景并管理任务','判断是否允许进入迎宾场景'),('组织各系统目标与结果','管理执行变化并汇总结果'),('各自完成域内执行','域内校验、执行及保护'),('场景接口、协同要求','状态约束、场景接口'),('交互规范、能力与组合规则','限制反馈、退出确认与验证')],
 extra='具体进入条件、保护与退出规则由业务及系统定义；Agent管理整体任务，系统保证本域执行边界。')
driver=reuse(18,lead='结合用户与空间状态形成调节需求，按相关系统的可执行范围协调座椅、方向盘和后视镜。',
 replacements=[('空间状态与任务','空间状态与执行约束'),('完成本系统执行与反馈','提供限制、执行及保护反馈')],
 extra='矩阵重点：空间评估与状态服务、系统能力限制、条件变化交互，以及干涉和人工介入验证。')
driver['notes']+=' 空间评估及干涉处理是本轮提出的重点检查要求，不说明原场景全部保护已实现。不得由示意图推导运动范围或响应时限。'
sun=reuse(19,lead='用乘员与环境信息判断局部热舒适需求，在系统允许范围内协调调节。',
 extra='舒适度是需要改善的目标；系统限制与保护决定允许范围，不能为了舒适目标突破执行边界。')
sun['notes']+=' 约束处理属于本轮规划要求，不新增原文未描述的设备动作或温度阈值。'

org=reuse(21,lead='组织共用的状态约束、接口、运行与验证建设，系统和业务团队承担具体功能责任。',
 replacements=[('方法 · 规范 · 共用工具','状态 · 接口 · 共用工具'),('技术评估 · 联合验证','边界评审 · 联合验证')])
workflow=reuse(22,replacements=[('场景、参与系统、使用条件与预期效果','场景、约束、保护责任与预期效果'),('服务改造、交互规则、底座与工具要求','状态约束、接口、运行与验证要求')])
trial=reuse(24,replacements=[('场景与系统接口规范、协同运行及结果反馈要求','进入与保持条件、系统限制反馈、退出确认'),('系统能力描述、空间状态与执行接口改进','空间评估、系统能力限制、变化与保护交互'),('感知状态服务、系统能力与场景验证用例','状态有效性、系统限制与受限调节验证'),('任务与系统分工清楚，协同与反馈符合设计','边界清楚；拒绝、中断与结果符合设计'),('不同用户与车辆配置下按业务要求执行','空间受限、人工介入时按要求处理'),('感知、需求识别与执行链路满足功能要求','状态变化和能力受限时行为可解释')])
road=reuse(25,replacements=[('完善能力封装、场景接口及执行反馈','完善状态约束、能力接口及执行反馈'),('验证执行效率、资源使用、通信与异常处理','验证保护分工、退出确认及运行要求'),('完善能力描述、组合规则与交互机制，验证允许范围','依据能力和约束完善组合规则，验证允许范围')])

groups=[
 ('业务目标与车控Agent能力','车控智能化要改善什么体验，车控Agent承担什么能力？',
  ['系统服务基础与用户体验目标','已有VCC业务场景','车控Agent从状态理解到结果跟踪的业务过程'],
  [('1.1 业务目标',goal),('1.2 实际业务',reuse(4)),('1.3 车控Agent能力',agent)]),
 ('执行边界与关键交互','车控Agent如何依靠系统状态判断，并与系统执行层共同处理变化？',
  ['NOMI、车控Agent与系统执行层的职责边界','进入前、执行中和退出后的持续交互','条件不满足、故障与风险下的场景处置'],
  [('2.1 责任边界',boundary),('2.2 全过程交互',lifecycle),('2.3 受限与异常处理',abnormal)]),
 ('矩阵平台能力建设','哪些共用能力支撑上述业务责任和执行边界？',
  ['状态与约束服务作为共同基础','服务封装与场景接口使用规范','可靠协同、自适应交互与边界内组合','贯穿正常、受限、异常与恢复的联合验证'],
  [('3.1 建设总览',support),('3.2 状态与约束服务',state),('3.3 服务升级与封装',cap),('3.3 场景接口范式',interface),('3.4 协同运行支撑',runtime),('3.5 自适应交互',adaptive),('3.6 边界内动态组合',dynamic),('3.7 验证工具与方法',validation)]),
 ('实际业务中的协同与支撑','用已有业务案例核对Agent职责、系统边界和矩阵建设。',
  ['近车解锁开门：状态判断与整车任务','主驾自适应：空间条件与系统执行范围','阳光直射：舒适目标与系统限制'],
  [('4.1 近车解锁开门',welcome),('4.2 主驾自适应模式',driver),('4.3 阳光直射场景',sun)]),
 ('组织协作与试点推进','由谁共同建设，形成什么成果，怎样验证并推广？',
  ['虚拟能力中心与正式责任团队','从需求及保护分工到实现、采用和验证','首批试点、阶段重点与投入安排'],
  [('5.1 组织定位',org),('5.2 协作方式',workflow),('5.3 首批试点',trial),('5.4 推进建议',road)])
]
cover=old[0].copy();cover['chapter']='提升规划 · V2.9';cover['body']=cover['body'].replace('V2.8','V2.9');slides.append(cover)
for part,(name,question,topics,content) in enumerate(groups,1):
    nav='<div class="part-roadmap">'+''.join(f'<div class="{"current" if i==part else ""}"><span>{i:02}</span><b>{E(g[0])}</b></div>' for i,g in enumerate(groups,1))+'</div>'
    body=f'<div class="part-intro"><div class="part-number">{part:02}</div><div class="part-topics"><h3>接下来说明</h3><ol>'+''.join('<li>'+E(t)+'</li>' for t in topics)+'</ol></div></div>'+nav
    slides.append(dict(title=f'{part:02}　{name}',chapter=f'第{part}部分 / 内容导览',lead=question,body=body,notes='本页说明章节范围与业务逻辑。',cover=False,divider=True,part=part))
    for label,s in content:
        s=s.copy();s['chapter']=f'第{part}部分 / {label}';s['part']=part;s.pop('divider',None);slides.append(s)

before,tail=base.split('<main>',1);_,after=tail.split('</main>',1)
extra='''
.common-base{background:#173642;color:white;padding:1.4vh 1.4vw;display:flex;justify-content:space-between;align-items:center;gap:2vw}.common-base b{font-size:clamp(14px,1.2vw,24px)}.common-base span{font-size:clamp(12px,1vw,20px);color:#d0dfd4;line-height:1.6}.common-base.light{background:#dfebda;color:var(--ink)}.common-base.light span{color:var(--muted)}.support-four{display:grid;grid-template-columns:1fr 1fr;gap:1.5vh 1.8vw}.support-four article{background:#e7ece2;border-left:3px solid var(--teal);padding:1.5vh 1.2vw}.support-four span{font-size:clamp(12px,.9vw,18px);color:var(--teal)}.support-four h3{font-size:clamp(18px,1.45vw,29px);margin:.5vh 0}.support-four p{font-size:clamp(12px,1.02vw,20px);line-height:1.6;color:var(--muted)}
@media(max-width:800px){.common-base{flex-direction:column;align-items:flex-start;padding:18px}.support-four{grid-template-columns:1fr}.support-four article{padding:18px}}
@media print{.common-base b{font-size:11pt}.common-base span,.support-four p{font-size:9pt}.support-four h3{font-size:14pt}}
'''
rendered=[]
for i,s in enumerate(slides,1):
    tag='h1' if s['cover'] else 'h2';cls='slide'+(' cover' if s['cover'] else '')+(' part-divider' if s.get('divider') else '')
    rendered.append(f'<section class="{cls}" id="s{i}" data-title="{E(s["title"].replace("<br>"," "),quote=True)}" data-chapter="{E(s["chapter"],quote=True)}" data-part="{s.get("part",0)}" aria-labelledby="t{i}"><div class="eyebrow"><span>{i:02}</span>{E(s["chapter"])}</div><{tag} id="t{i}">{s["title"]}</{tag}><p class="lead">{E(s["lead"])}</p><div class="body">{s["body"]}</div><aside class="notes">{E(s["notes"])}</aside></section>')
html=(before+'<main>'+''.join(rendered)+'</main>'+after).replace('V2.8','V2.9').replace('</style>',extra+'</style>')
assert len(slides)==27
ROOT.joinpath('matrix_planning_v2_9.html').write_text(html)
ROOT.joinpath('matrix_planning_v2_9_content.json').write_text(json.dumps(slides,ensure_ascii=False,indent=2)+'\n')
ROOT.joinpath('matrix_v2_9_revision_notes.md').write_text('''# V2.9 逻辑重组说明

按业务目标与Agent能力、执行边界与交互、矩阵平台建设、真实业务案例、组织推进五部分重组，共27页。标题保持不变。

状态与约束为共同基础，原四项平台建设方向继续保留；系统保护、异常中断、退出确认和未知结果处理贯穿接口、运行机制、验证与试点。明确舒适目标、硬限制和乘员状态信息的区别。

合并重复的迎宾入口示例和AiCabin责任页；场景接口范式保留并放入能力封装章节。AiCabin的实际定义和未确认项仍保留在讲述提示，不新增字段或动作参数。

案例只沿用近车解锁开门、主驾自适应、阳光直射。新补充的约束检查及验证范围作为规划建议，不描述为已有实现。矩阵组织规范与共用平台建设，系统/平台实现，VCC采用；独立软件架构组织边界保留。

验证桌面三种尺寸、SVG文字边界及碰撞、五部分章节、目录和翻页；核查打印27页。新版独立部署，不覆盖旧版或修改平台IDL。
''')
print(json.dumps({'slides':len(slides),'parts':len(groups),'diagrams':html.count('<svg'),'bytes':len(html.encode())}))
