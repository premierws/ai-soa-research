"""Build the source-grounded executive briefing around four support directions."""
from pathlib import Path
from html import escape
import json

ROOT=Path(__file__).parent
slides=[]
serial=200
def e(t): return escape(str(t),quote=True)
def text(x,y,t,size=23,color='#173642',anchor='start'):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" text-anchor="{anchor}">{e(t)}</text>'
def box(x,y,w,h,title,lines=(),kind='normal'):
    fill,stroke,ink={'normal':('#edf1ed','#b9c8c2','#173642'),'dark':('#173642','#173642','#fff'),'teal':('#dfeee7','#17847a','#173642'),'orange':('#f7e7db','#c76b43','#593c2e')}[kind]
    s=f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>'
    s+=f'<text x="{x+22}" y="{y+35}" font-size="25" font-weight="650" fill="{ink}">{e(title)}</text>'
    for i,t in enumerate(lines): s+=text(x+22,y+71+i*32,t,22,ink)
    return '<g class="diagram-node">'+s+'</g>'
def arrow(x1,y1,x2,y2):
    return f'<path d="M{x1},{y1} L{x2},{y2}" stroke="#17847a" stroke-width="2.7" fill="none" marker-end="url(#ARR)"/>'
def route(d): return f'<path d="{d}" fill="none" stroke="#17847a" stroke-width="2.7" marker-end="url(#ARR)"/>'
def svg(label,body,h=500):
    global serial
    serial+=1
    return f'<svg class="diagram" viewBox="0 0 1440 {h}" role="img" aria-label="{e(label)}"><defs><marker id="arr{serial}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0L10,5L0,10Z" fill="#17847a"/></marker></defs>'+body.replace('#ARR',f'#arr{serial}')+'</svg>'
def note(t): return '<div class="takeaway">'+t+'</div>'
def deliver(a,b,c):
    return '<div class="deliver">'+''.join(f'<div><b>{k}</b><span>{v}</span></div>' for k,v in [('矩阵建设',a),('共同参与',b),('支持业务',c)])+'</div>'
def add(ch,title,lead,body,notes='',cover=False):
    slides.append(dict(chapter=ch,title=title,lead=lead,body=body,notes=notes,cover=cover))
def direction(n,title):return f'<div class="direction"><b>{n}</b><span>{title}</span></div>'

VCC='VCC功能架构WIP：业务场景表、功能块职责定义及预期近车解锁白板。'
PLAN='本页为基于已讨论目标提出的矩阵建设建议，不表示具体平台组件、投入或车型计划已经冻结。'

add('提升规划 · V2.6','面向智能化车控的<br>服务架构矩阵提升规划',
    '基于现有SOA基础，提升服务能力、平台支撑能力与跨组织协作能力。',
    '<div class="cover-route"><span>系统能力服务化</span><i>＋</i><span>跨系统场景协同</span></div>'
    '<p class="cover-message">支持预定义场景建设，<br>逐步扩展受约束的自适应场景。</p>'
    '<div class="cover-meta">V2.6 审阅版　｜　2026.11.17</div>',
    '依据VCC业务规划、SDV演进材料、已有服务接口调研和本轮讨论组织。本文是矩阵提升规划，不把WIP场景写成已量产功能，不定义新的接口字段。',True)

add('01 / 业务目标','在已有系统服务基础上，扩展场景协同能力',
    '短期把预定义场景做完整，长期支持在已知能力和约束内按需组合与调整。',
    svg('已有服务支撑预定义和自适应场景',
      box(25,5,1390,90,'使用方：座舱Agent、智驾系统、手机及其他控制入口',['既可调用单项系统功能，也可请求场景能力'])+
      box(25,155,625,145,'预定义场景',['流程、参与系统与允许变化预先设计','复用既有系统能力完成功能'],'teal')+
      box(790,155,625,145,'自适应场景',['结合需求、车辆状态和用户差异','在允许范围内选择、组合与调整'],'dark')+
      box(25,380,1390,100,'共同基础：系统能力、服务接口和确定性控制',['系统产品保留本域策略、控制与保护；场景协同建立在这些能力之上'])+
      arrow(335,380,335,310)+arrow(1105,380,1105,310))+
    note('提升的是场景组织与协同能力；已有SOA服务继续复用，精确控制继续保留。'),
    'SDV材料提出SOA—能力—Agent的演进方向；本轮讨论明确预定义和受约束自适应场景并存。图表示功能层次，不是新增进程或部署方案。')

add('01 / 实际业务','用已有业务规划说明智能化车控的价值',
    '选取VCC材料中的三个场景，分别体现多系统协同、个体适应和环境响应。',
    '<div class="case-three">'+''.join(f'<article><span>{k}</span><h3>{title}</h3><p>{desc}</p><div class="case-systems">{systems}</div><strong>{value}</strong></article>' for k,title,desc,systems,value in [
      ('业务案例一','近车解锁开门','结合钥匙位置、用户设置及车辆状态，组织上车迎宾。','门锁、电动门、后视镜、灯光、座椅、方向盘、踏板等','价值：多个系统共同完成上车场景'),
      ('业务案例二','主驾自适应模式','结合主驾眼点、记忆设置、空间位置与车辆配置。','座椅、方向盘、后视镜','价值：适应不同用户的驾驶位置需求'),
      ('业务案例三','阳光直射场景','结合乘客光斑、日照强度、占位及外界环境。','空调、电动出风口、遮阳帘、变色玻璃','价值：识别局部热舒适需求并响应')])+'</div>'+
    note('案例取自VCC功能架构规划；具体控制策略、车型范围和完成条件由业务与系统团队确认。'),VCC)

add('02 / 建设主线','围绕四个方向，形成矩阵的平台支撑能力',
    '以场景业务为牵引，将服务升级、运行保障和自适应支撑连接起来。',
    '<div class="support-map">'+''.join(f'<article><div class="support-need"><b>{i}</b><div><h3>{a}</h3><p>{b}</p></div></div><i>→</i><div class="support-build"><h3>{c}</h3><p>{d}</p></div></article>' for i,a,b,c,d in [
      ('01','场景能力供给','外部能够按场景请求完整功能','服务升级与封装','系统能力提炼、场景接口与兼容规范'),
      ('02','高效可靠协同','多个系统按要求共同完成执行','组合运行方法与底座优化','执行依赖、资源协调、通信与性能验证'),
      ('03','自适应交互支撑','能够了解能力并跟踪、调整任务','SOA框架与中间件演进','能力查询、异步反馈和任务调整机制'),
      ('04','边界内动态组合','在已知能力与约束内形成场景','能力描述与组合规则','使用条件、依赖约束、查询和组合验证')])+'</div>'+
    note('业务团队决定场景策略；矩阵组织共性建设，系统和平台团队实现并共同验证。'),PLAN)

add('03 / 服务升级与封装','完善系统能力封装，再形成场景能力接口',
    '区分可复用的系统功能与跨系统场景，避免上层反复操作底层信号和设备。',
    direction('01','场景能力供给')+
    svg('系统能力与场景能力的分层封装',
      box(320,5,800,110,'对外：场景能力接口',['VCC管理跨系统任务，汇总进度与结果'],'dark')+
      box(25,225,420,140,'车身等系统能力',['明确功能、条件与执行反馈','屏蔽具体设备和信号差异'])+
      box(510,225,420,140,'座椅等系统能力',['完善已有接口；按需重新封装','保持本域策略与保护'],'teal')+
      box(995,225,420,140,'热管理等系统能力',['提供可复用功能','承担本系统具体执行'])+
      box(25,435,1390,65,'共同基础：SOA服务、状态与事件，以及既有确定性控制')+
      route('M720,115 V165 H235 V215')+route('M720,165 V215')+route('M720,165 H1205 V215')+
      arrow(235,435,235,375)+arrow(720,435,720,375)+arrow(1205,435,1205,375))+
    deliver('能力划分方法、接口规范与兼容要求','SO、FO、VCC、架构师及系统SWE','形成可复用的系统能力和场景入口'),
    VCC+' 分层为功能职责表达，不规定接口名称或实现模块。现有服务抽象程度不一，先复用，按真实缺口改造。系统能力重新封装不由soa_adaptor承担业务策略。')

add('03 / 服务升级与封装','近车迎宾：从多个系统功能，形成完整场景入口',
    '对外承接上车场景，对内仍由各系统完成自己的功能。',
    direction('01','场景能力供给')+
    svg('近车迎宾的场景接口与系统能力',
      box(25,50,365,315,'已有系统功能',['门锁与电动门','后视镜、踏板','灯光','座椅、方向盘'])+
      box(535,50,390,315,'VCC迎宾场景',['理解人员接近与车辆状态','建立并管理整车任务','向相关系统提出目标','汇总执行结果'],'dark')+
      box(1070,50,345,315,'系统产品',['判断是否允许执行','自主完成本域控制','保留防夹等保护','返回结果与原因'],'teal')+
      arrow(390,210,525,210)+arrow(925,210,1060,210))+
    note('矩阵推动能力边界、目标与结果表达的一致性；具体迎宾流程和系统策略由业务团队设计。'),
    VCC+' 原文“近车解锁开门”及预期近车解锁白板列出相关系统，并区分VCC整车任务与系统域内执行。本页概括其职责，不新增接口字段、动作先后顺序或时限。')

add('04 / 高效可靠协同','明确执行依赖与资源约束，提高协同效率',
    '在满足功能与安全要求的前提下，合理安排顺序和并行，减少等待与重复调用。',
    direction('02','高效可靠协同')+
    svg('有依赖的顺序执行与允许的并行执行',
      box(25,165,300,140,'接收场景请求',['确认执行条件','识别依赖和资源限制'],'dark')+
      box(460,25,350,120,'存在功能依赖',['按要求顺序执行'])+
      box(460,335,350,120,'允许并行的功能',['减少不必要的串行等待'],'teal')+
      box(965,25,450,120,'系统执行',['系统内部处理控制时序'])+
      box(965,335,450,120,'汇总执行结果',['处理异常及未完成的部分'])+
      route('M325,210 H385 V85 H450')+route('M385,210 V395 H450')+
      arrow(810,85,955,85)+arrow(810,395,955,395)+arrow(1190,145,1190,325))+
    deliver('服务组合方法、依赖与资源分析方法','VCC、系统、平台与软件架构团队','提高响应效率和资源利用率'),
    PLAN+' 本图为通用组织方法，未规定近车迎宾等具体案例的动作顺序。不承诺全局效率最高或资源绝对最优。跨系统协调属于VCC，系统内部时序和控制属于系统产品。')

add('04 / 高效可靠协同','以业务运行要求牵引SOA底座优化',
    '同时考虑通信可靠性、响应性能和资源开销，通过联合试验确认方案。',
    direction('02','高效可靠协同')+
    '<div class="runtime-triangle"><article><span>通信稳定可靠</span><p>状态与结果及时传递<br>断连、故障与恢复可处理</p></article><article><span>响应满足要求</span><p>明确端到端响应目标<br>识别等待与拥塞影响</p></article><article><span>资源合理使用</span><p>控制消息与重复处理开销<br>评估计算和通信资源</p></article></div>'+
    svg('运行要求到平台方案与联合验证',
      box(25,35,420,120,'场景提出运行要求',['明确业务需要与运行条件'],'dark')+
      box(510,35,420,120,'平台评估与改进',['复用已有机制，补齐实际缺口'])+
      box(995,35,420,120,'联合验证与采用',['确认性能、可靠性和资源开销'],'teal')+
      arrow(445,95,500,95)+arrow(930,95,985,95),h=190)+
    note('矩阵汇总共性需求并推动评估；平台和底软团队负责技术方案，业务与系统团队共同验收。'),
    PLAN+' 包括QoS、消息调度、状态时效、异常恢复和资源预算等候选工程要求；具体指标需测量和评估，不填写未经确认的性能数字。')

add('05 / 自适应交互支撑','评估自适应场景对SOA交互方式的新要求',
    '场景需要根据状态变化继续决策，交互需支持能力查询、执行反馈和任务调整。',
    direction('03','自适应交互支撑')+
    svg('自适应场景的交互需求',
      box(25,0,330,60,'VCC场景管理',(), 'dark')+box(1055,0,360,60,'系统与平台服务')+
      '<path d="M190,75 V450 M1235,75 V450" stroke="#c6d0c8" stroke-dasharray="6 6"/>'+
      arrow(190,115,1235,115)+text(720,100,'了解当前可用能力与使用条件',24,'#17847a','middle')+
      arrow(190,205,1235,205)+text(720,190,'提出功能目标与约束',24,'#17847a','middle')+
      arrow(1235,295,190,295)+text(720,280,'持续反馈执行状态、结果与原因',24,'#17847a','middle')+
      arrow(190,385,1235,385)+text(720,370,'根据变化调整或结束任务',24,'#17847a','middle'))+
    deliver('交互需求、现状差距与框架演进建议','VCC、系统、平台及架构团队','支持执行过程中的判断和调整'),
    VCC+' 目标和结果交互方向来自文档，能力查询与相应框架评估来自本轮规划讨论。图为交互语义示意，不是已冻结的API或完整时序。')

add('05 / 自适应交互支撑','先明确交互需求，再决定框架和通信机制如何升级',
    '区分业务表达、交互过程和底层通信，优先评估现有SOA的承载能力。',
    svg('交互与通信演进的三个层次',
      box(25,25,420,350,'业务表达',['请求什么功能','有哪些条件和限制','返回什么执行结果'],'dark')+
      box(510,25,420,350,'交互过程',['查询与请求','状态和事件反馈','修改、中断与取消'],'teal')+
      box(995,25,420,350,'框架与通信支撑',['评估已有SOA机制','识别需要补充的能力','验证性能与可靠性'])+
      arrow(445,200,500,200)+arrow(930,200,985,200))+
    note('可能需要新的交互模式；是否需要新通信协议或中间件，应由需求和验证结果决定。'),
    PLAN+' 不预设MCP、Agent协议或新中间件作为车辆内部执行方案。外部Agent接入与内部系统协同分别评估，现有服务调用和事件通知继续可用。')

add('06 / 边界内动态组合','让已有能力在明确规则内按需组合',
    '自由组合需要清楚的能力边界、使用条件、依赖和约束，组合后的场景才能执行与验证。',
    direction('04','边界内动态组合')+
    svg('能力与规则支撑受约束的动态组合',
      '<rect x="405" y="5" width="615" height="475" rx="16" fill="#edf1e7" stroke="#adc2b0" stroke-dasharray="8 5"/>'+
      text(712,40,'组合边界：已开放能力与允许的使用规则',25,'#17847a','middle')+
      box(25,160,300,155,'需求与当前状态',['用户需求与场景识别','人、车、环境状态'],'dark')+
      box(450,80,525,120,'能力信息与规则',['功能、适用条件、依赖与冲突'])+
      box(450,285,525,150,'VCC选择与组合',['结合目标形成方案','检查约束，按变化调整'],'teal')+
      box(1110,160,305,155,'系统执行与反馈',['系统完成本域任务','反馈结果或限制'])+
      arrow(325,235,440,355)+arrow(712,200,712,275)+arrow(975,355,1100,235)+
      route('M1260,315 V480 H712 V445')+text(1035,465,'执行反馈，支持后续调整',21,'#17847a','middle'),h=520)+
    deliver('能力描述、组合规则、查询与验证工具','矩阵提供方法；系统供给能力；VCC编排','从固定流程逐步扩展到受约束的组合'),
    PLAN+' 原文有任务建立、子系统任务定义、仲裁与跨域规划，以及无固定功能场景的智能快捷场景。本页为平台支撑的归纳，不声明现有案例已经支持任意生成新场景。')

add('07 / 贯穿案例','近车解锁开门：场景入口、系统协同与结果汇总',
    '沿用VCC规划中的迎宾任务，说明四个建设方向如何共同支撑业务。',
    svg('近车解锁的业务输入、场景和系统职责',
      box(25,25,340,400,'业务输入',['蓝牙 / UWB钥匙位置','用户账户与车辆设置','门锁与防盗状态','形成用户接近的上下文'])+
      box(490,25,440,165,'VCC迎宾任务',['识别上车场景并管理任务','组织各系统目标与结果'],'dark')+
      box(490,295,440,130,'矩阵支撑',['场景接口、协同要求','交互规范、能力与组合规则'],'teal')+
      box(1055,25,360,400,'相关系统',['门锁、门把手与电动门','后视镜、踏板','灯光','座椅、方向盘','各自完成域内执行'])+
      arrow(365,110,480,110)+arrow(930,110,1045,110)+arrow(710,295,710,200))+
    note('整车任务由VCC管理，域内策略由系统产品负责；按共同定义的完成条件汇总结果。'),
    VCC+' 近车解锁系统清单及输入来自原文；任务与域内执行边界来自预期近车解锁白板。矩阵支撑内容为规划建议。未给定动作顺序、自动开门权限或响应数字。')

add('07 / 对照案例','主驾自适应模式：结合用户差异协调多个系统',
    '使用原文中的眼点、记忆设置、空间位置和车辆配置，支撑驾驶位置调整。',
    svg('主驾自适应的输入、状态理解与系统执行',
      box(25,10,400,185,'用户与交互信息',['主驾眼点位置','用户账户记忆设置','HMI交互请求'])+
      box(25,285,400,185,'车辆与空间信息',['座椅 / 方向盘空间位置','座椅占位、车辆配置','门状态'])+
      '<circle cx="720" cy="235" r="125" fill="#173642"/>'+
      text(720,212,'主驾自适应',28,'#fff','middle')+text(720,254,'空间状态与任务',24,'#fff','middle')+
      box(1015,100,400,270,'相关系统',['座椅控制','方向盘控制','后视镜控制','完成本系统执行与反馈'],'teal')+
      arrow(425,115,590,175)+arrow(425,375,590,295)+arrow(855,235,1005,235))+
    note('矩阵重点：系统能力封装、空间状态接口、使用条件与执行反馈，支持业务团队实现自适应策略。'),
    VCC+' 输入与下游系统来自主驾自适应模式场景行。原文包含空间舒适分计算及舱内空间关系；具体算法、调节参数和控制目标不在本材料中新增。')

add('07 / 对照案例','阳光直射场景：从环境感知识别热舒适需求',
    '以乘客光斑、日照强度、占位与外界环境为输入，识别局部热舒适需求。',
    svg('阳光直射业务的感知、识别与响应',
      '<circle cx="120" cy="110" r="45" fill="#e7bc64"/>'+
      ''.join(f'<path d="M{x1},{y1} L{x2},{y2}" stroke="#c59243" stroke-width="3"/>' for x1,y1,x2,y2 in [(120,30,120,5),(40,110,15,110),(175,55,195,35),(175,165,195,185)])+
      box(245,15,1170,100,'感知与环境信息',['OMS乘客光斑、日照强度、乘员占位，以及隧道、地库、林荫等外界环境'])+
      box(25,235,400,180,'识别局部热舒适需求',['结合乘员与环境状态','形成阳光直射场景任务'],'dark')+
      box(530,235,400,180,'局部精准送风',['联动空调与电动出风口','由相关系统完成具体控制'],'teal')+
      box(1035,235,380,180,'原文涉及系统',['空调、电动出风口','遮阳帘、变色玻璃'])+
      route('M830,115 V175 H225 V225')+arrow(425,325,520,325))+
    note('矩阵重点：感知与状态服务、系统能力描述、及时交互与场景验证；业务团队负责识别和调节策略。'),
    VCC+' 原文任务为局部精准送风，相关系统列有空调、电动出风口、遮阳帘与变色玻璃。本图不表示所有设备必须同时动作，也不新增遮阳或变色策略及效果指标。')

add('08 / 组织定位','以SOA为核心的虚拟能力中心，推动共性平台建设',
    '矩阵组织专业协作，业务与工程团队负责具体功能、实现和采用。',
    svg('虚拟能力中心与正式责任团队',
      '<circle cx="720" cy="250" r="155" fill="#173642"/>'+
      text(720,205,'服务架构矩阵',30,'#fff','middle')+text(720,255,'方法 · 规范 · 共用工具',23,'#fff','middle')+text(720,300,'技术评估 · 联合验证',23,'#fff','middle')+
      box(25,5,420,145,'VCC与业务团队',['定义场景目标与策略','采用能力并管理整体任务'])+
      box(995,5,420,145,'系统团队',['提供系统能力与接口','负责本域控制和保护'],'teal')+
      box(25,350,420,145,'平台与底层软件',['评估框架和运行机制','完成平台改进与维护'])+
      box(995,350,420,145,'软件架构与验证团队',['协同运行与部署方案','验证整体行为与工程要求'])+
      arrow(445,100,565,175)+arrow(875,175,985,100)+arrow(445,420,565,325)+arrow(875,325,985,420))+
    note('SOA仍是核心专业能力；整体软件架构继续由独立的软件架构组织负责。'),
    '沿用用户明确的组织边界：虚拟COE，不承担所有业务交付。图为主要协作关系，技术评估与采用反馈实际双向。')

add('08 / 协作方式','围绕真实业务，把需求、平台改进和采用连接起来',
    '每个专题明确业务负责人、技术责任人、参与投入和验证方式。',
    '<div class="work-ribbon">'+''.join(f'<article><span>{i}</span><h3>{a}</h3><p>{b}</p><strong>{c}</strong></article>' for i,a,b,c in [
      ('1','明确业务需求','场景、参与系统、使用条件与预期效果','FO、VCC、SO与车型AI'),
      ('2','形成共性方案','服务改造、交互规则、底座与工具要求','矩阵、平台及领域架构师'),
      ('3','实施并业务采用','系统/平台实现，VCC接入场景','SWE、系统与平台团队'),
      ('4','验证并推广','联合验证，更新规范、工具和用例','测试、业务与矩阵共同参与')])+'</div>'+
    '<div class="operation-band"><b>稳定核心＋领域代表＋专题协作</b><p>SOA负责人维护方向与共用成果；TPM协调依赖与节点；DO在进入集成发布时参与。</p></div>'+
    note('SO负责系统，FO负责功能需求与详细设计，AI负责车型架构；专业角色按专题参与，不改变所属团队职责。'),
    '组织形式来自本轮已经明确的虚拟COE分工。平台与领域软件架构师共同参与，但不替代独立软件架构组织。人数和工时由责任团队确认。')

add('09 / 首批建设','从三个真实业务场景启动，形成可采用的成果',
    '以业务试点识别共性缺口，再决定接口、工具和平台能力的建设范围。',
    '<table class="trace"><thead><tr><th>实际业务</th><th>重点建设成果</th><th>共建与采用方</th><th>主要验证内容</th></tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+x+'</td>' for x in row)+'</tr>' for row in [
      ['近车解锁开门','场景与系统接口规范、协同运行及结果反馈要求','VCC、车身及相关系统、平台；VCC采用','任务与系统分工清楚，协同与反馈符合设计'],
      ['主驾自适应模式','系统能力描述、空间状态与执行接口改进','VCC、座椅/方向盘/后视镜、感知及平台团队','不同用户与车辆配置下按业务要求执行'],
      ['阳光直射场景','感知状态服务、系统能力与场景验证用例','VCC、感知、热管理及相关系统；业务团队采用','感知、需求识别与执行链路满足功能要求']
    ])+'</tbody></table>'+
    note('具体缺口通过业务与接口调研确认；上表为建议的首批建设范围，不是已经完成的交付清单。'),
    VCC+PLAN+' 原始业务清单保留在第3、12—14页，矩阵组织首批建设建议在本页集中表达。')

add('09 / 推进建议','先形成业务可用成果，再扩大自适应组合范围',
    '以实际采用与验证结果推进，兼顾业务效果、技术能力和团队复用。',
    '<div class="progression">'+''.join(f'<article><span>{i}</span><h3>{a}</h3><p>{b}</p></article>' for i,a,b in [
      ('第一步','服务与场景做完整','选定试点，完善能力封装、场景接口及执行反馈。'),
      ('第二步','协同运行做可靠','验证执行效率、资源使用、通信与异常处理。'),
      ('第三步','自适应支撑逐步扩展','完善能力描述、组合规则与交互机制，验证允许范围。')])+'</div>'+
    '<div class="decision"><b>本轮建议确认</b><span>首批业务与责任团队</span><span>必要投入和联合试验</span><span>共用成果的维护与推广</span></div>'+
    '<div class="closing">以已有SOA为基础，<strong>支撑场景协同，逐步扩展自适应能力。</strong></div>',
    PLAN+' 预定义与自适应能力可以并行研究，阶段表达重点及成熟度，不是排他的时间表。评价技术成立、团队采用和业务效果，不编造收益或性能数字。')

base=(ROOT/'matrix_planning_v2_5.html').read_text()
before,tail=base.split('<main>',1);_,after=tail.split('</main>',1)
css='''
.direction{display:flex;gap:1vw;align-items:center;flex-shrink:0;font-size:clamp(12px,.95vw,19px);color:#256c60}.direction b{border:1px solid #9cbbab;border-radius:20px;padding:.1em .7em}.case-three{display:grid;grid-template-columns:repeat(3,1fr);gap:2vw}.case-three article{border-top:4px solid var(--teal);padding:2.5vh 1.4vw;background:#e8ede4;display:flex;flex-direction:column;gap:1.6vh}.case-three article>span{color:var(--teal);font-size:clamp(11px,.9vw,18px)}.case-three p{font-size:clamp(13px,1.1vw,22px);line-height:1.75;color:var(--muted)}.case-systems{font-size:clamp(12px,1vw,20px);line-height:1.7;border-top:1px solid #bccbbc;padding-top:1.6vh}.case-three strong{font-size:clamp(13px,1.05vw,21px);color:var(--teal);line-height:1.6}.support-map{display:flex;flex-direction:column;gap:1.4vh}.support-map article{display:grid;grid-template-columns:47% 6% 47%;align-items:stretch}.support-need{display:flex;gap:1.4vw;background:#173642;color:white;padding:1.6vh 1.5vw;align-items:center}.support-need>b{font-size:clamp(28px,2.8vw,55px);color:#d9e5a9;font-weight:400}.support-need h3,.support-build h3{font-size:clamp(18px,1.5vw,30px)}.support-need p,.support-build p{font-size:clamp(12px,1.02vw,20px);line-height:1.6;margin-top:.5vh}.support-need p{color:#c8d7d2}.support-map article>i{display:flex;align-items:center;justify-content:center;font-size:28px;color:var(--teal);font-style:normal}.support-build{background:#e0ebdf;padding:1.6vh 1.5vw}.runtime-triangle{display:grid;grid-template-columns:repeat(3,1fr);gap:2vw}.runtime-triangle article{border-top:3px solid var(--teal);padding:1.8vh 1.5vw;background:#e9ede3}.runtime-triangle span{font-size:clamp(18px,1.6vw,31px);font-weight:650}.runtime-triangle p{font-size:clamp(13px,1.1vw,21px);line-height:1.7;margin-top:1vh;color:var(--muted)}.work-ribbon{display:grid;grid-template-columns:repeat(4,1fr);gap:1.7vw}.work-ribbon article{position:relative;border-top:4px solid var(--teal);background:#e8ede3;padding:2vh 1.2vw;display:flex;flex-direction:column;gap:1.6vh}.work-ribbon article:not(:last-child):after{content:'→';position:absolute;right:-1.4vw;top:14vh;color:var(--teal)}.work-ribbon article>span{font-size:clamp(28px,3vw,58px);line-height:1;color:var(--teal)}.work-ribbon h3{font-size:clamp(17px,1.45vw,29px)}.work-ribbon p{font-size:clamp(12px,1vw,20px);line-height:1.7;color:var(--muted)}.work-ribbon strong{font-size:clamp(11px,.9vw,18px);line-height:1.6;border-top:1px solid #bdccbc;padding-top:1.5vh}.operation-band{background:#173642;color:white;padding:2vh 1.6vw}.operation-band b{font-size:clamp(15px,1.25vw,25px)}.operation-band p{font-size:clamp(12px,1vw,20px);color:#c9d9d0;line-height:1.7;margin-top:1vh}.progression{display:grid;grid-template-columns:repeat(3,1fr);gap:2vw}.progression article{border-top:4px solid var(--teal);padding:2vh 1.4vw;background:#e6ecdf}.progression span{font-size:clamp(12px,1vw,20px);color:var(--teal)}.progression h3{margin:1.5vh 0;font-size:clamp(18px,1.55vw,31px)}.progression p{font-size:clamp(13px,1.05vw,21px);line-height:1.75;color:var(--muted)}.decision{display:flex;gap:1.8vw;align-items:center;flex-wrap:wrap;font-size:clamp(12px,1vw,20px);padding:1.5vh 0;border-bottom:1px solid var(--line)}.decision b{color:var(--teal)}.trace th:nth-child(1){width:18%}.trace th:nth-child(2){width:29%}.trace th:nth-child(3){width:29%}.trace th:nth-child(4){width:24%}.trace td{padding:2.4vh .8vw}.closing{font-size:clamp(22px,2vw,39px)}
@media(max-width:800px){.case-three,.runtime-triangle,.work-ribbon,.progression{grid-template-columns:1fr}.support-map article{grid-template-columns:1fr}.support-map article>i{padding:10px;transform:rotate(90deg)}.case-three article{padding:20px}.work-ribbon article:not(:last-child):after{display:none}.operation-band{padding:20px}.support-build,.support-need{padding:18px}.decision{gap:12px}.trace{font-size:10px}.trace td{padding:12px 5px}}
@media print{.case-three h3,.runtime-triangle span,.support-map h3,.work-ribbon h3,.progression h3{font-size:15pt}.case-three p,.runtime-triangle p,.support-map p,.work-ribbon p,.progression p,.case-systems{font-size:10pt}.case-three strong{font-size:10pt}.operation-band b{font-size:12pt}.operation-band p,.decision{font-size:9pt}.work-ribbon strong{font-size:8pt}.support-need>b{font-size:25pt}.direction{font-size:8pt}.closing{font-size:19pt}}
'''
parts=[]
for i,s in enumerate(slides,1):
    tag='h1' if s['cover'] else 'h2'
    parts.append(f'<section class="slide{" cover" if s["cover"] else ""}" id="s{i}" data-title="{e(s["title"].replace("<br>"," "))}" data-chapter="{e(s["chapter"])}" aria-labelledby="t{i}"><div class="eyebrow"><span>{i:02}</span>{e(s["chapter"])}</div><{tag} id="t{i}">{s["title"]}</{tag}><p class="lead">{e(s["lead"])}</p><div class="body">{s["body"]}</div><aside class="notes">{e(s["notes"])}</aside></section>')
html=(before+'<main>'+''.join(parts)+'</main>'+after).replace('V2.5','V2.6').replace('</style>',css+'</style>')
assert len(slides)==18
ROOT.joinpath('matrix_planning_v2_6.html').write_text(html)
ROOT.joinpath('matrix_planning_v2_6_content.json').write_text(json.dumps(slides,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'slides':len(slides),'diagrams':html.count('<svg'),'tables':html.count('<table'),'bytes':len(html.encode())}))
