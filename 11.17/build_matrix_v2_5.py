"""Revise the briefing language while preserving the approved scope and mapping."""
from pathlib import Path
from html import escape
import json
import re

ROOT = Path(__file__).parent
slides = json.loads((ROOT/'matrix_planning_v2_4_content.json').read_text())
base = (ROOT/'matrix_planning_v2_4.html').read_text()
serial = 100
C = ['车辆能力识别','场景组合与执行编排','多入口协调与控制仲裁','执行反馈与结果判断','运行中调整与异常处理','场景复用与持续演进']
U = ['服务能力提升','交互形式升级','状态与反馈能力提升','底座支撑能力升级','架构分析工具升级','验证能力提升']
def e(t): return escape(str(t),quote=True)
def text(x,y,t,size=23,color='#173642',anchor='start'):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" text-anchor="{anchor}">{e(t)}</text>'
def box(x,y,w,h,title,lines=(),kind='normal'):
    fill,stroke,ink={'normal':('#edf1ed','#b9c8c2','#173642'),'dark':('#173642','#173642','#fff'),'teal':('#dfeee7','#17847a','#173642'),'orange':('#f7e7db','#c76b43','#593c2e')}[kind]
    s=f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>'
    s+=f'<text x="{x+22}" y="{y+35}" font-size="25" font-weight="650" fill="{ink}">{e(title)}</text>'
    for i,t in enumerate(lines): s+=text(x+22,y+70+i*31,t,21,ink)
    return '<g class="diagram-node">'+s+'</g>'
def arrow(x1,y1,x2,y2,label=''):
    s=f'<path d="M{x1},{y1} L{x2},{y2}" stroke="#17847a" stroke-width="2.5" fill="none" marker-end="url(#ARR)"/>'
    if label:s+=text((x1+x2)/2,(y1+y2)/2-12,label,19,'#17847a','middle')
    return s
def svg(label,body,h=470):
    global serial
    serial+=1
    return f'<svg class="diagram" viewBox="0 0 1440 {h}" role="img" aria-label="{e(label)}"><defs><marker id="arr{serial}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0L10,5L0,10Z" fill="#17847a"/></marker></defs>'+body.replace('#ARR',f'#arr{serial}')+'</svg>'
def chips(ids,prefix='C'):
    names=C if prefix=='C' else U
    return '<div class="chips">'+''.join(f'<span class="chip {prefix.lower()}">{prefix}{i} {names[i-1]}</span>' for i in ids)+'</div>'
def note(t):return '<div class="takeaway">'+t+'</div>'
def result(out,user,check):
    return '<div class="deliver">'+''.join(f'<div><b>{a}</b><span>{b}</span></div>' for a,b in [('建设成果',out),('责任与采用',user),('预期作用',check)])+'</div>'
def setslide(n,title,lead,body=None,notes=None):
    s=slides[n-1];s.update(title=title,lead=lead)
    if body is not None:s['body']=body
    if notes is not None:s['notes']=notes

# Apply terminology corrections consistently to inherited diagrams and summaries.
replacements={
 '状态与结果可信度提升':'状态与反馈能力提升',
 'U3 状态与结果可信度':'U3 状态与反馈能力提升',
 '后排休息，前排不变':'后排休息，保持前排设置',
 '后排休息，不影响前排':'后排休息，保持前排设置',
 '前排不变':'前排设置不变',
 '保护有效':'除雾功能按要求运行',
 '保证信息可用':'提供所需状态与通信支持',
 '不新增层层串行审批；':'',
 '不能与模型工程师混淆':'按公司车型架构职责参与',
 '不另建包办业务交付的开发部门':'与所属团队明确参与时间和维护责任',
 '按年份要求所有能力一次到位':'统一设定所有功能的完成时间',
}
for s in slides:
    for key in ['chapter','body','notes']:
        for a,b in replacements.items():s[key]=s[key].replace(a,b)

setslide(1,'面向智能化车控的<br>服务架构矩阵提升规划',
 '基于现有SOA基础，提升服务能力、平台支撑能力与跨组织协作能力。',
 '<div class="cover-route"><span>系统能力服务化</span><i>＋</i><span>跨系统场景协同</span></div>'
 '<p class="cover-message">支持VCC等业务团队建设预定义场景，<br>逐步扩展受约束的自适应场景。</p>'
 '<div class="cover-meta">V2.5 审阅版　｜　2026.11.17</div>')
slides[0]['chapter']='提升规划 · V2.5'

setslide(2,'在已有系统能力基础上，提供跨系统场景能力',
 '系统能力已通过服务接口提供；进一步提升的是多个系统围绕场景需求协同工作的能力。',
 svg('系统能力支撑两类场景能力',
     box(25,5,1390,85,'面向座舱Agent、智驾系统、手机及其他使用方',['可调用单项功能，也可请求多个系统共同完成场景'])+
     box(25,135,620,155,'短期：预定义场景',['示例：“后排儿童休息”','按设计好的流程执行','允许配置座位、偏好和操作限制'],'teal')+
     box(795,135,620,155,'长期：自适应场景',['示例：“孩子休息，不移动座椅”','在已有能力和规则内组合功能','根据车辆状态变化调整执行'],'dark')+
     box(25,365,1390,90,'共同基础：已有系统服务及进一步完善的系统能力',['空调调节、座椅调整、车窗控制、灯光调节等；系统负责各自的控制策略与执行'])+
     arrow(335,365,335,300,'组合系统能力')+arrow(1105,365,1105,300,'按需组合与调整'))+
 note('预定义场景与自适应场景共同复用系统能力；单项功能调用继续保留。'),
 '场景是围绕某一使用需求组织的一组功能，例如儿童休息；预定义是流程和允许分支预先设计，自适应是在已开放能力与约束内选择、组合和调整。这里讨论功能层级，不定义新的服务分类或协议。现有接口中已经包含部分场景与偏好控制能力。')

setslide(3,'实现智能化场景，需要六项关键能力',
 '从了解车辆能力，到协调执行、判断结果和复用场景，形成完整的业务过程。')
slides[2]['body']=slides[2]['body'].replace('已受理、执行中和真正完成如何区分？','各系统是否执行？场景是否达到预期？').replace('需要哪些系统？顺序与依赖是什么？','需要哪些系统？如何配合执行？').replace('短期更多依靠预设流程','短期更多依靠预设流程')

setslide(4,'围绕六项关键能力，确定矩阵提升重点',
 '以业务需要为依据，协同提升系统服务、SOA底座、工程工具和验证方法。')
slides[3]['body']=slides[3]['body'].replace('能力暴露升级','智能化场景演进').replace('运行底座能力','SOA底座支撑').replace('业务服务能力','系统服务能力')
slides[3]['body']=re.sub(r'<div class="takeaway">.*?</div>',note('六项提升相互配合；下文说明每项工作形成什么成果、由谁采用、支撑什么业务能力。'),slides[3]['body'])

setslide(5,'服务能力提升：完善系统能力封装，支持跨系统组合',
 '复用已有服务，按需改造接口和系统实现，让上层按功能使用能力，减少对底层控制细节的依赖。',
 chips([1,2,4])+
 svg('系统能力封装的提升重点',
     box(25,30,420,175,'现有基础与提升空间',['已有控制、状态和部分场景接口','部分调用仍需了解设备布局','不同系统的抽象程度不一'])+
     box(510,30,420,175,'系统团队完善能力封装',['吸收底层设备与信号差异','明确可用条件与执行反馈','保留本系统控制与保护'],'dark')+
     box(995,30,420,175,'上层按系统功能组合',['例如：调节后排照明','由灯光系统处理设备映射','VCC与其他功能协调使用'],'teal')+
     arrow(445,120,500,120)+arrow(930,120,985,120)+
     box(25,290,420,110,'已有能力完整：复用补全',['补充使用条件与反馈说明'])+
     box(510,290,420,110,'功能表达不足：改造接口',['完善参数、职责和执行反馈'])+
     box(995,290,420,110,'上层操作过细：重新封装',['在系统内封装稳定控制逻辑']))+
 result('能力清单、接口改造与兼容方案','矩阵组织评审；系统实现；VCC采用','减少重复适配，形成可复用组合单元'),
 slides[4]['notes']+' 调研实例：AmbLiParamReq仍含zone/node/seg亮度与颜色数组。座椅已有空间检查和姿态偏好接口，应优先复用。需要改造的比例和工作量尚未全量评估。')

setslide(6,'交互形式升级：完善多入口协同与场景执行交互',
 '让不同使用方能够发起、跟踪和结束场景，并明确人工操作或其他请求介入时的处理规则。',
 chips([2,3,5])+
 svg('场景请求和执行反馈',
     ''.join(box(x,0,300,55,t,(),k) for x,t,k in [(25,'座舱 / 手机等入口','normal'),(570,'VCC场景协调','dark'),(1115,'相关系统','normal')])+
     ''.join(f'<path d="M{x},65 V435" stroke="#c2cec8" stroke-dasharray="5 5"/>' for x in [175,720,1265])+
     arrow(175,115,720,115,'提出场景需求和操作限制')+
     arrow(720,190,1265,190,'调用系统能力')+
     arrow(1265,265,720,265,'反馈是否执行、进展与结果')+
     arrow(175,340,720,340,'调整需求或结束场景')+
     arrow(720,415,1265,415,'按约定规则协调后续执行'))+
 result('场景交互规范与控制冲突处理规则','VCC、入口及系统团队共同定义','场景进展可跟踪，调整与退出行为一致'),
 slides[5]['notes']+' 需要按业务明确请求身份与关联、取消权限、重试与去重、人工接管。现有SOA支持多种接口类型，不能概括为只有单次调用；本轮是补齐场景协同所需语义。')

slides[6]['chapter']='02 / U3 状态与反馈能力提升'
setslide(7,'状态与反馈能力提升：支持执行跟踪与结果判断',
 '完善系统状态、执行进展和异常反馈，使VCC能够说明场景完成了什么、还有什么未完成。',
 chips([1,4,5])+
 svg('场景执行过程与结果反馈',
     box(25,45,380,150,'确认能否执行',['系统检查使用条件','明确接受或拒绝及原因'])+
     box(530,45,380,150,'跟踪执行过程',['获得系统状态与进展','识别异常或人工中断'],'dark')+
     box(1035,45,380,150,'判断场景结果',['按事先明确的条件判断','汇总各系统执行结果'],'teal')+
     arrow(405,120,520,120)+arrow(910,120,1025,120)+
     box(25,300,420,110,'达到预期',['说明已经完成的内容'],'teal')+
     box(510,300,420,110,'部分完成或执行中断',['说明影响与后续处理'],'orange')+
     box(995,300,420,110,'暂时无法确认',['说明状态不足，不误报完成']))+
 result('状态与结果说明、反馈改进及验证用例','系统提供反馈；VCC综合判断','及时发现异常，避免把请求成功当作效果达成'),
 slides[6]['notes']+' 工程实施需要分别检查API读取结果、数据有效性与时效、请求关联和效果证据。无history queue的buffer读取不提供新帧标识时，不能伪造更新状态。详细SM、E2E与缓存机制仅用于工程设计核查。')

setslide(8,'底座支撑能力升级：满足多系统协同的运行要求',
 '根据场景需要明确通信、状态反馈、响应时间与异常恢复要求，形成平台演进依据。',
 chips([1,2,4,5])+
 svg('场景需求到平台改进的关系',
     box(25,115,360,180,'场景提出运行要求',['及时获得车辆状态','协调多个系统执行','异常后能够正确处理'],'dark')+
     box(520,15,390,155,'评估现有底座能力',['已有机制能否满足','性能和资源是否足够','哪些要求仍有缺口'])+
     box(520,280,390,155,'明确平台改进项',['优先复用已有能力','按实际缺口完善机制','与软件架构团队协同'],'teal')+
     box(1045,115,370,180,'联合试验与验收',['平台、系统和VCC参与','验证运行与资源要求','形成可采用的平台方案'])+
     arrow(385,170,510,95)+arrow(715,170,715,270)+arrow(910,350,1035,240))+
 result('平台需求、差距分析与改进验证结果','矩阵汇总需求；平台/底软评估实施','使场景在实际运行条件下稳定执行'),
 slides[7]['notes']+' 技术要求可包含状态时效、端到端时延与抖动、并发规模、队列和请求关联、故障恢复及CPU/RAM预算；具体数值由试点建立基线后确认，不预设统一新协议。')

setslide(9,'架构分析工具升级：支持依赖查询与变更分析',
 '帮助团队回答：某个场景依赖哪些系统能力，适用哪些车型，软件变化会影响什么。')
slides[8]['body']=slides[8]['body'].replace('IDL、调用关系、反馈与版本','接口、功能行为及版本').replace('实例、配置与车型','车型与系统配置').replace('设备配置、服务实例和部署信息','设备支持、配置与适用范围').replace('能力映射、车型适用性与变更分析查询','能力依赖、适用范围与变更分析工具')

setslide(10,'验证能力提升：加强场景协同与异常处理验证',
 '在已有功能和接口测试基础上，加强多系统组合、操作冲突及软件变化后的验证。',
 chips([1,2,3,4,5,6])+
 svg('场景验证范围',
     box(25,155,320,150,'从同一业务场景出发',['明确预期效果','明确不能违反的限制'],'dark')+
     box(510,5,420,115,'正常协同',['各系统执行，场景达到预期'],'teal')+
     box(510,175,420,115,'冲突与异常',['条件变化、设备故障、人工操作'],'orange')+
     box(510,345,420,115,'车型与版本变化',['配置差异、接口变化及兼容性'])+
     box(1095,155,320,150,'检查整体行为',['限制是否被遵守','结果是否被准确反馈'])+
     arrow(345,190,500,65)+arrow(345,230,500,235)+arrow(345,270,500,405)+
     arrow(930,65,1085,190)+arrow(930,235,1085,235)+arrow(930,405,1085,270))+
 result('场景验证方法、异常用例和回归集合','验证团队组织；VCC/系统/平台参与','提高协同正确性，减少变更引入的问题'),
 slides[9]['notes'])

setslide(11,'服务与底座协同提升，共同支持场景执行',
 '系统服务说明能做什么、怎样反馈；SOA底座提供执行所需的运行支撑。')
slides[10]['body']=slides[10]['body'].replace('前排设置不变','保持前排<br>设置').replace('质量与请求关联','状态质量与执行反馈').replace('不能只定义“后排可调温”，也不能只验证“消息能到达”；需要证明二者共同支持场景。','以“后排休息、保持前排设置”为例，分别明确系统功能要求和平台运行要求，再共同验证。')

setslide(12,'组织定位：以SOA为核心的虚拟能力中心',
 '组织共性技术建设，支持业务团队采用，同时保持系统、平台和软件架构各自的责任。')
setslide(13,'工作流程：业务提出需求，多团队共同建设与验证',
 '矩阵组织连接需求、技术方案和工程团队，推动共用成果进入实际业务。')
setslide(14,'组织运营：稳定核心、领域参与、专题推进',
 '核心成员维护方向与规范，领域代表连接实际需求，专题团队集中解决共性问题。')
slides[13]['body']=slides[13]['body'].replace('限期专题组','专题协作组').replace('议题进入条件：有业务影响、有责任团队、有采用对象、有验证办法。成果发布后保留维护责任。','每个专题明确业务需求、责任人、参与投入、采用团队和验证方式；共用成果持续维护。')

setslide(15,'演进策略：先验证预定义场景，再扩大自适应范围',
 '分阶段验证能力和业务收益，逐步扩展可组合范围与运行中调整能力。')
slides[14]['body']=re.sub(r'<div class="takeaway">.*?</div>',note('以试点验证结果决定扩展范围，结合业务收益选择规则、流程、规划算法或模型。'),slides[14]['body'])

setslide(16,'案例A：以“后排儿童休息”验证跨系统组合',
 '改善后排热舒适、降低灯光亮度，同时保持前排设置、不移动座椅。')
slides[15]['body']=slides[15]['body'].replace('检查车型与区域能力','检查车辆是否支持').replace('优先复用；必要时重新封装','系统提供区域调节能力').replace('系统负责灯节点映射','内部处理设备差异').replace('核查前排约束','检查前排设置限制')
slides[15]['notes']+=' 本案例不承诺前排实际温度、噪声或体感完全不受物理耦合影响；热舒适评价和前排设置限制应由FO/SO具体定义。'
setslide(17,'案例A分工：系统提供能力，VCC组合使用',
 '通过具体场景识别接口缺口，形成系统改进、业务采用和联合验证。')
slides[16]['body']=slides[16]['body'].replace('无座椅动作、前排约束正确、失败不漏报','不移动座椅，保持前排设置，准确反馈结果')

setslide(18,'案例B：车辆状态或人工操作变化时，调整场景',
 '休息场景运行中出现除雾需求或人工操作，按约定优先关系处理受影响功能。')
slides[17]['body']=slides[17]['body'].replace('系统维持保护功能','空调系统执行除雾策略').replace('系统上报已知变化','获得相关操作与状态').replace('系统产品始终保留本域保护和实时控制','各系统保留本域控制与保护职责')
setslide(19,'案例B分工：明确优先关系，联合验证调整行为',
 '业务确定处理原则，VCC协调受影响任务，系统和平台分别提供执行与运行支持。')
slides[18]['body']=slides[18]['body'].replace('处理变化与关联','协调任务调整').replace('平台评估状态时效、请求关联及取消传播','平台提供所需通信与状态支持').replace('检查错误路径','验证异常行为').replace('注入延迟、丢失和竞争，检查除雾功能按要求运行、接管正确及结果准确','检查除雾按要求运行，人工操作得到尊重，场景结果反馈准确').replace('不覆盖人工设置','按规则处理人工设置')

setslide(20,'案例C：软件更新后，检查个人场景能否继续使用',
 '依据当前车型、配置和功能变化判断适用性，避免原有场景失效后仍按旧方式执行。')
slides[19]['body']=slides[19]['body'].replace('系统确认语义兼容性','系统确认功能是否兼容').replace('依赖能力及适用信息','所需功能和适用条件')
setslide(21,'案例C演进：从个人场景中发现可推广的功能需求',
 '记录使用反馈，筛选有共性的需求，经过产品设计和验证后纳入预定义场景。')
setslide(22,'首批工作：明确建设成果、采用团队和验证依据',
 '用三组案例连接业务需求与矩阵提升，便于确定责任、投入和工程计划。')
slides[21]['body']=slides[21]['body'].replace('后排休息，保持前排设置','后排休息，保持前排设置及座椅不动')
setslide(23,'成效评价：技术能力、团队采用与业务效果',
 '既评价共用技术是否有效，也评价是否被实际使用，以及是否改善场景体验。')
slides[22]['body']=slides[22]['body'].replace('变更影响是否查全','变更影响是否识别完整').replace('先测现状，再比较改造后的效果。Mock、SDK、台架与实车测试分别提供对应层次的证据。','先建立试点基线，再比较改进效果；由业务、系统、平台和验证团队共同评价。')
setslide(24,'推进建议：确定试点、责任团队与必要投入',
 '以首批场景验证建设方向，将有效做法逐步纳入共用规范、工具和平台演进。')
slides[23]['body']=slides[23]['body'].replace('确认试验与推广出口','确认试点与推广安排')
slides[23]['body']=re.sub(r'<div class="closing">.*?</div>',
 '<div class="closing">以SOA为基础完善系统能力与协同支撑，<br><strong>支持预定义场景，逐步扩展自适应场景。</strong></div>',slides[23]['body'])

# Keep detailed facts and implementation cautions in speaker notes, not executive summaries.
for s in slides:
    s['body']=s['body'].replace('U3 状态与结果可信度','U3 状态与反馈能力提升')
    assert '场景服务' not in s['title']

parts=[]
for i,s in enumerate(slides,1):
    tag='h1' if s['cover'] else 'h2'
    parts.append(f'<section class="slide{" cover" if s["cover"] else ""}" id="s{i}" data-title="{e(s["title"].replace("<br>"," "))}" data-chapter="{e(s["chapter"])}" aria-labelledby="t{i}"><div class="eyebrow"><span>{i:02}</span>{e(s["chapter"])}</div><{tag} id="t{i}">{s["title"]}</{tag}><p class="lead">{e(s["lead"])}</p><div class="body">{s["body"]}</div><aside class="notes">{e(s["notes"])}</aside></section>')
before,tail=base.split('<main>',1)
_,after=tail.split('</main>',1)
html=(before+'<main>'+''.join(parts)+'</main>'+after).replace('V2.4','V2.5').replace('智能化车控导向的服务架构矩阵提升规划 · V2.5','面向智能化车控的服务架构矩阵提升规划 · V2.5')
html=html.replace('</style>', '.cover h1{font-size:clamp(44px,4.2vw,82px)}.cover .body{flex:0 0 auto;min-height:auto}@media print{.cover h1{font-size:35pt}}'+'</style>')
ROOT.joinpath('matrix_planning_v2_5.html').write_text(html)
ROOT.joinpath('matrix_planning_v2_5_content.json').write_text(json.dumps(slides,ensure_ascii=False,indent=2)+'\n')
ROOT.joinpath('matrix_v2_5_revision_notes.md').write_text('''# V2.5 汇报口径调整

固定标题为《面向智能化车控的服务架构矩阵提升规划》。保留24页结构、六项能力与六项提升的对应关系、三组案例和跨组织职责。

本轮重写全部页面标题和引导结论，重绘能力演进及U1/U2/U3/U4/U6页面。明确系统能力原本已经服务化，场景能力是对多个系统的协调组合。避免用未经证实的“从……到……”概括现有能力不足。

接口字段、SM缓存、E2E和底座机制等细节放入讲述提示。氛围灯调研在主页面解释其业务含义，保留原始事实供讲述核查。

案例A仅要求保持已明确的前排设置、不移动座椅，不扩大为前排物理环境完全不受影响。案例B分别明确VCC、系统和平台职责。

不修改V2.4、飞书文档、平台IDL或软件实现。新版独立发布，供用户审阅。
''')
print(json.dumps({'slides':len(slides),'bytes':len(html.encode()),'diagrams':html.count('<svg'),'tables':html.count('<table')}))
