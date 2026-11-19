"""Build the approved capability-to-SOA executive briefing as a standalone deck."""
from pathlib import Path
from html import escape
import json

ROOT = Path(__file__).parent
FRAME = Path('/home/shaun/projects/soa_matrix/assets')
slides = []
serial = 0
C = ['车辆能力识别','场景组合与执行编排','多入口协调与控制仲裁','执行反馈与结果判断','运行中调整与异常处理','场景复用与持续演进']
U = ['服务能力提升','交互形式升级','状态与结果可信度提升','底座支撑能力升级','架构分析工具升级','验证能力提升']

def e(t): return escape(str(t), quote=True)
def txt(x,y,t,size=23,color='#173642',anchor='start',weight=400):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" text-anchor="{anchor}" font-weight="{weight}">{e(t)}</text>'
def box(x,y,w,h,title,lines=(),kind='normal'):
    fill,stroke,ink={'normal':('#edf1ed','#b9c8c2','#173642'),'dark':('#173642','#173642','#fff'),'teal':('#dfeee7','#17847a','#173642'),'orange':('#f7e7db','#c76b43','#593c2e'),'lime':('#e8edbf','#acb970','#173642')}[kind]
    s=f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>'
    s+=txt(x+22,y+35,title,25,ink,weight=650)
    for i,t in enumerate(lines): s+=txt(x+22,y+70+i*31,t,21,ink)
    return '<g class="diagram-node">'+s+'</g>'
def line(x1,y1,x2,y2,label='',color='#17847a'):
    s=f'<path d="M{x1},{y1} L{x2},{y2}" stroke="{color}" stroke-width="2.5" fill="none" marker-end="url(#ARR)"/>'
    if label:s+=txt((x1+x2)/2,(y1+y2)/2-10,label,19,color,'middle')
    return s
def path(d,color='#17847a',dash=False):
    return f'<path d="{d}" fill="none" stroke="{color}" stroke-width="2.5" {"stroke-dasharray="+chr(34)+"6 5"+chr(34) if dash else ""} marker-end="url(#ARR)"/>'
def svg(label,body,h=470):
    global serial
    serial+=1
    return f'<svg class="diagram" viewBox="0 0 1440 {h}" role="img" aria-label="{e(label)}"><defs><marker id="arr{serial}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0L10,5L0,10Z" fill="#17847a"/></marker></defs>'+body.replace('#ARR',f'#arr{serial}')+'</svg>'
def chips(ids,prefix='C'):
    names=C if prefix=='C' else U
    return '<div class="chips">'+''.join(f'<span class="chip {prefix.lower()}">{prefix}{i} {names[i-1]}</span>' for i in ids)+'</div>'
def result(out,user,check):
    return '<div class="deliver">'+''.join(f'<div><b>{a}</b><span>{b}</span></div>' for a,b in [('形成成果',out),('建设与采用',user),('验证重点',check)])+'</div>'
def note(t):return '<div class="takeaway">'+t+'</div>'
def cards(items):
    return '<div class="cards">'+''.join(f'<article><span class="index">{a}</span><h3>{b}</h3><p>{c}</p></article>' for a,b,c in items)+'</div>'
def add(ch,title,lead,body,notes='',cover=False):
    slides.append(dict(chapter=ch,title=title,lead=lead,body=body,notes=notes,cover=cover))
def flow(items,labels=()):
    w=(1360-(len(items)-1)*48)/len(items); s=''
    for i,(title,details) in enumerate(items):
        x=40+i*(w+48)
        s+=box(x,125,w,180,title,details,'dark' if i==1 else 'teal' if i==0 else 'normal')
        if i:s+=line(x-43,215,x-5,215)
    return svg('功能到工程成果的流程',s)

add('规划建议 · V2.4','让系统能力成为<br>智能化场景的可靠基础','智能化车控导向的服务架构矩阵提升规划',
    '<div class="cover-route"><span>系统服务</span><i>→</i><span>预定义场景</span><i>→</i><span>自适应场景</span></div>'
    '<p class="cover-message">以六条关键能力为牵引，提升SOA服务与运行底座，<br>通过跨组织协作支持VCC等业务团队。</p>'
    '<div class="cover-meta">2026.11.17　｜　能力演进 · 技术提升 · 组织采用</div>',
    '本材料为规划建议。案例用于说明技术及组织建设方法，不代表已批准的产品功能、资源或发布承诺。',True)

add('01 / 能力演进','对外暴露能力：从系统控制，走向场景服务','预定义场景先形成稳定能力；自适应场景在已开放能力和约束内组合、调整。',
    svg('能力暴露层级演进',
      box(40,15,1360,100,'共同使用方：座舱Agent、智驾系统、手机与传统控制入口',['按需求选择精确控制、预定义场景或结构化组合'])+
      box(820,155,580,110,'长期 · 自适应场景能力',['“让孩子更舒服，保持除雾和前排设置”'],'dark')+
      box(420,295,980,90,'短期 · 预定义场景能力',['“后排儿童休息”＋座位、偏好与限制参数'],'teal')+
      box(40,415,1360,90,'现有基础 · 系统服务与可复用系统能力',['空调、座椅、车窗、灯光；保留精确控制，逐步吸收底层实现差异'])+
      path('M210,415 V340 H405')+path('M650,295 V210 H805'),h=525)+
      note('演进的是能力暴露层级。已有系统服务持续复用，预定义与自适应场景长期并存。'),
      '现有服务抽象程度不一，部分已经有场景及偏好接口，不能概括为全部只暴露信号。图表示功能层次，不规定模块或部署。')

cap_questions=['当前车型支持什么？此刻能否用？','需要哪些系统？顺序与依赖是什么？','多入口和人工操作冲突时谁优先？','已受理、执行中和真正完成如何区分？','条件变化后如何继续、调整或退出？','换车型或OTA后还能否正确使用？']
add('01 / 关键能力','场景能够组合与自适应，需要六条能力支撑','短期更多依靠预设流程，长期需要可查询的能力信息和运行中的重新判断。',
    '<div class="cap-grid">'+''.join(f'<article><b>C{i+1}</b><div><h3>{n}</h3><p>{cap_questions[i]}</p></div></article>' for i,n in enumerate(C))+'</div>'+
    note('VCC负责场景任务的整体协调与结果；系统产品负责本域策略、控制和保护。'))

# Deliberately separate primary mappings from full many-to-many relationships.
map_pairs=[('C1 能力识别','U1 服务能力提升 / U5 架构分析工具升级'),('C2 组合编排','U1 服务能力提升 / U2 交互形式升级'),('C3 入口仲裁','U2 交互形式升级 / U6 验证能力提升'),('C4 结果判断','U3 状态与结果可信度 / U6 验证能力提升'),('C5 运行调整','U2 交互形式升级 / U4 底座支撑能力'),('C6 场景复用','U5 架构分析工具 / U6 验证能力提升')]
add('01 / 总体对照','每项矩阵提升，都要回答支撑哪条车控能力','业务目标牵引技术提升；技术成果最终由业务、系统与平台团队采用。',
    '<div class="mapping"><div class="map-goal"><span>能力暴露升级</span><h3>预定义场景<br>↓<br>自适应场景</h3><p>在有限能力和<br>明确约束内演进</p></div><div class="map-links">'+''.join(f'<div><b>{a}</b><i>→</i><span>{b}</span></div>' for a,b in map_pairs)+'</div><div class="map-dual"><b>SOA双线协同</b><p>业务服务能力<br>功能 · 条件 · 反馈</p><p>运行底座能力<br>通信 · 时效 · 恢复</p><strong>共同验证场景结果</strong></div></div>'+
    note('这里只列主要支撑关系；六项提升共同服务六条能力，后续逐页展开成果、采用方与验证。'))

add('02 / U1 服务能力提升','从信号与执行器接口，提升为可组合的系统能力','不仅补充接口说明，还要复用、改造或重新封装已有服务。',
    chips([1,2,4])+
    svg('系统能力封装前后对照',
      box(25,30,420,190,'现有接口抽样：氛围灯',['AmbLiParamReq仍含','zone / node / seg数组','上层可能需了解灯光布局'])+
      box(510,30,410,190,'系统内提炼与封装',['区域到执行器映射','效果执行、资源与请求仲裁','保留底层控制及保护'],'dark')+
      box(985,30,430,190,'建议：区域照明效果能力',['区域、亮度、颜色与过渡','可用条件、实际状态与结果','与其他系统能力组合'],'teal')+
      line(445,125,500,125)+line(920,125,975,125)+
      box(25,300,420,120,'复用并补全',['已有功能完整，补条件和反馈'])+
      box(510,300,410,120,'改造现有接口',['调整职责、参数或结果语义'])+
      box(985,300,430,120,'重新封装',['由系统吸收稳定的控制细节']))+
    result('能力映射、改造清单、接口与兼容方案','系统团队建设；VCC及其他入口采用','减少上层底层依赖，不重复控制策略'),
    '事实：StaAmbLiActu为执行器接口，AmbLiMgr参数包含区域、节点、分段。右侧是建议能力，不是现有完整实现。座椅已有空间与姿态相关抽象，优先复用；具体改造需核查实现。soa_adaptor只承担桥接与平台隔离，不承载这些系统业务。')

add('02 / U2 交互形式升级','从单次调用，扩展到多入口与持续任务交互','按实际需要定义异步反馈、修改、取消和接管，精确控制保留简洁路径。',
    chips([2,3,5])+
    svg('多入口异步任务交互时序',
      ''.join(box(x,0,280,55,t,(),k) for x,t,k in [(25,'座舱 / 手机','normal'),(570,'VCC任务协调','dark'),(1115,'系统服务','normal')])+
      ''.join(f'<path d="M{x},65 V435" stroke="#c2cec8" stroke-dasharray="5 5"/>' for x in [165,710,1255])+
      line(165,110,710,110,'请求：对象、参数、来源与约束')+
      line(710,180,1255,180,'系统能力请求 / 关联信息')+
      line(1255,250,710,250,'受理或拒绝；后续状态与结果')+
      line(165,320,710,320,'另一入口：修改 / 取消 / 接管')+
      line(710,390,1255,390,'确认权限与冲突后调整执行'))+
    result('交互模式、请求关联与取消接管规则','VCC、入口和系统团队共同采用','重试不重复执行，取消与接管无歧义'),
    '图为异步语义示意，RR、FF、Event、Field按实际使用选择，不要求所有接口增加完整任务模型。任务接收成功不等于物理执行完成。')

add('02 / U3 状态与结果可信度提升','从链路正常，提升到数据可用、结果可判断','建立证据链，区分接口调用、有效数据、执行过程与业务效果。',
    chips([1,4,5])+
    svg('任务结果证据链与未知分支',
      box(25,40,290,125,'通信证据',['调用返回、连接与传输','不能证明执行完成'])+
      box(390,40,290,125,'数据证据',['读取结果、时效和质量','缓存不等于新数据'])+
      box(755,40,290,125,'执行证据',['本域受理与执行状态','关联到对应请求'])+
      box(1120,40,295,125,'效果证据',['满足约定目标条件','仍需检查可信程度'],'teal')+
      line(315,103,380,103)+line(680,103,745,103)+line(1045,103,1110,103)+
      box(25,285,420,115,'证据充分',['报告达成或明确的执行结果'],'teal')+
      box(510,285,420,115,'明确失败 / 中断',['保留原因及受影响范围'],'orange')+
      box(995,285,420,115,'证据不足',['报告无法确认，不补造成功'])+
      path('M1265,165 V230 H235 V275')+path('M1265,230 H720 V275')+path('M1265,230 H1205 V275'))+
    result('质量使用规则、结果语义与证据要求','系统/VCC/平台/验证团队采用','旧值不当新帧，受理不当完成，未知不当成功'),
    '无history queue的SM可能始终返回buffer当前值。读取成功与新帧到达需区分；底座没有提供的时间、更新或E2E状态不能伪造。E2E暴露和业务处理按功能配置，不统一强制丢弃。')

add('02 / U4 底座支撑能力升级','从通用通信优化，扩展到智能化场景运行保障','由场景行为推导底座机制与性能要求，再由平台团队评估承接方案。',
    chips([1,2,4,5])+
    svg('业务场景推导底座要求',
      box(25,10,360,105,'场景需要什么',['发现变化、及时调整、准确反馈'],'dark')+
      box(25,185,360,165,'可测量的运行要求',['变化检测与响应时延','并发请求及状态分发规模','异常与唤醒后的恢复行为'],'teal')+
      line(205,115,205,175,'需求分解')+
      box(480,10,450,140,'候选机制',['服务可用性、质量与时效','请求关联、队列、取消传播'])+
      box(480,235,450,140,'性能预算',['时延与抖动、带宽','CPU / RAM及故障恢复时间'])+
      path('M385,260 H430 V80 H470')+path('M430,260 V305 H470')+
      box(1030,90,385,205,'平台评估与验证',['复用已有机制或补齐缺口','联合系统与VCC实测','达标后纳入平台演进'],'teal')+
      line(930,80,1020,150)+line(930,305,1020,230))+
    result('有业务来源的机制需求、性能预算和差距','平台及底软建设；VCC/系统联合验收','在目标资源与异常条件下满足任务需要'),
    '不在本材料中预设统一新协议或新中间件，性能数字需建立基线后确认。软件运行与部署方案由对应架构责任组织确认。')

add('02 / U5 架构分析工具升级','从查看服务关系，扩展到功能依赖与变更影响','让工程师查到“场景依赖什么、车型能否用、改动影响谁”。',
    chips([1,2,6])+
    svg('能力与服务车型版本依赖网络',
      box(25,180,295,125,'个人 / 预定义场景',['所需能力与使用约束'],'dark')+
      box(435,35,340,115,'系统能力',['功能、资源及依赖条件'],'teal')+
      box(435,300,340,115,'验证用例',['目标、异常与兼容验证'])+
      box(930,0,480,110,'服务与接口',['IDL、调用关系、反馈与版本'])+
      box(930,170,480,110,'实例、配置与车型',['设备配置、服务实例和部署信息'])+
      box(930,340,480,110,'变更影响查询',['受影响能力、场景和回归范围'],'orange')+
      line(320,225,425,100,'依赖')+line(320,265,425,350,'验证')+
      line(775,85,920,55)+line(775,105,920,215)+line(775,355,920,390)+
      path('M1410,55 H1430 V390 H1420')+path('M1170,280 V330'))+
    result('能力映射、车型适用性与变更分析查询','工具团队建设；系统/VCC/架构/测试采用','用真实变更核对影响范围与回归用例'),
    '现有service_arch数据可作为静态追溯基础，静态支持和依赖关系不自动证明运行时在线或当前可执行。')

add('02 / U6 验证能力提升','从接口连通测试，扩展到组合行为与结果验证','验证该做的动作，也验证约束被遵守、失败被准确识别。',
    chips([1,2,3,4,5,6])+
    svg('组合场景测试路径',
      box(25,165,285,125,'同一场景请求',['对象、目标、硬约束'],'dark')+
      box(435,10,380,110,'条件与权限不满足',['拒绝、说明原因，不越界'],'orange')+
      box(435,175,380,110,'可执行且条件稳定',['正确调用，检查实际结果'],'teal')+
      box(435,340,380,110,'执行中发生变化',['冲突、故障、人工介入'])+
      line(310,200,425,70)+line(310,230,425,230)+line(310,260,425,395)+
      box(965,20,450,110,'约束检查',['前排不变、保护优先等'])+
      box(965,185,450,110,'结果误判检查',['旧值、反馈缺失、部分完成'])+
      box(965,350,450,110,'版本与车型检查',['配置变化、不兼容和回归'])+
      line(815,65,955,75)+line(815,230,955,240)+line(815,395,955,405))+
    result('故障注入方法、场景用例与回归集合','验证牵头；VCC、系统和平台共同使用','约束不破坏，部分失败不被包装为整体成功'),
    '主机Mock检查逻辑与错误分支；SDK集成检查真实接口；台架/实车检查通信、时序及物理效果。各层证据不能互相替代。')

add('02 / 双线汇合','同一个业务目标，同时牵引服务和底座提升','以“后排休息，不影响前排”为例，两条建设线共同接受业务验证。',
    '<div class="dual-lanes"><div class="lane-label">共同目标<br><strong>后排休息<br>前排不变</strong></div><div class="lane-content"><article><b>业务服务能力线</b><div><span>区域控制范围</span><i>→</i><span>共享资源与限制</span><i>→</i><span>反馈及完成条件</span></div><p>系统团队提供可复用能力，VCC选择并协调。</p></article><article><b>运行底座能力线</b><div><span>及时获得状态</span><i>→</i><span>质量与请求关联</span><i>→</i><span>异常通知和恢复</span></div><p>平台团队提供满足业务需求的机制与性能。</p></article></div><div class="lane-end">共同验收<br><strong>目标可判断<br>约束被遵守<br>失败可解释</strong></div></div>'+
    note('不能只定义“后排可调温”，也不能只验证“消息能到达”；需要证明二者共同支持场景。'))

add('03 / 组织定位','以SOA为核心的虚拟能力中心，组织共同提升','矩阵提供专业方法与共用成果；业务和工程团队负责实现、采用与维护。',
    svg('虚拟能力中心与责任组织的关系',
      box(455,140,530,180,'服务架构矩阵 · COE',['系统能力抽象与接口规范','SOA运行要求、工具与验证方法','组织共性议题与联合试点'],'dark')+
      box(25,0,360,115,'VCC与消费入口',['提出场景需求，采用共用能力'])+
      box(25,345,360,115,'系统产品团队',['建设能力、策略、控制和保护'])+
      box(1055,0,360,115,'平台与底层软件',['评估并实现运行机制'])+
      box(1055,345,360,115,'独立软件架构组织',['软件架构、运行与部署协同'])+
      line(385,70,445,180)+line(445,280,385,395)+line(995,180,1045,70)+line(1045,395,995,280))+
    note('不改变各团队的产品与交付责任；每项共用成果仍需明确负责人、投入时间和实际采用方。'),
    '软件架构由另一个独立虚拟组织运营，本矩阵不扩张为统管所有软件架构的组织。图中箭头为主要工作输入输出，协作实际双向。')

add('03 / 工作流','从场景需求到业务采用，形成跨组织工作闭环','不新增层层串行审批；把关键设计输入、实施责任与验证出口连接起来。',
    '<div class="swim"><div class="swim-head"><span>参与角色</span><b>需求与条件</b><b>缺口与方案</b><b>实现与采用</b><b>联合验证</b></div>'+''.join('<div class="swim-row"><strong>'+a+'</strong>'+''.join('<span>'+x+'</span>' for x in b)+'</div>' for a,b in [
      ('FO / VCC',['场景、约束、验收','明确整体任务职责','编排接入与业务采用','评估目标和异常行为']),
      ('SO / 车型AI',['能力、配置与分配','确认系统与车型边界','推动系统侧承接','确认适用范围']),
      ('矩阵 / 架构师',['识别共性需求','服务方案与底座要求','指导接口和工具使用','沉淀规则与样例']),
      ('SWE / 平台',['实现可行性输入','评估改造与资源','系统、底座和工具实现','修正问题及性能差距']),
      ('测试 / TPM / DO',['测试入口与依赖','用例、责任与节点','跟踪依赖；按需集成','验证；发布环节DO参与'])])+'</div>'+
    note('FO负责需求和详细功能设计，SO负责系统；车型AI负责车型架构，不能与模型工程师混淆。'))

add('03 / 资源与运营','稳定核心＋领域代表＋限期专题组','虚拟组织依靠明确投入和成果维护运行，不另建包办业务交付的开发部门。',
    '<div class="org-layout"><div class="org-core"><span>稳定核心</span><h3>SOA专业负责人<br>平台 / 领域架构代表</h3><p>维护方向、规范和共用成果<br>组织议题筛选与技术评审</p></div><div class="org-branches"><article><b>领域代表 · 持续参与</b><p>SO、FO、车型AI、SWE、测试及VCC代表<br>提供需求、边界、工程反馈和采用承诺</p></article><article><b>专题小组 · 按问题组建</b><p>系统、底软、工具和专项专家<br>完成限期试验与共性问题解决</p></article><article><b>运营与交付界面</b><p>TPM跟踪责任、依赖和节点；DO在集成发布时参与<br>人数、工时及工程排期由责任团队评估</p></article></div></div>'+
    note('议题进入条件：有业务影响、有责任团队、有采用对象、有验证办法。成果发布后保留维护责任。'))

add('03 / 演进策略','先做实预定义场景，再逐步扩大自适应范围','以验证结果推进，不按年份要求所有能力一次到位。',
    '<div class="stairs">'+''.join(f'<article style="--step:{i}"><span>阶段 {i+1}</span><h3>{a}</h3><p>{b}</p><strong>进入下一阶段：{c}</strong></article>' for i,(a,b,c) in enumerate([
      ('能力可用、结果可判断','案例A：复用或改造系统能力，形成预定义场景。','调用、拒绝与结果证据通过验证'),
      ('运行中可以正确调整','案例B：冲突、故障和人工介入，保持保护有效。','时序、仲裁与异常结果可解释'),
      ('受控组合与持续复用','案例C：扩展允许组合，检查版本与车型适用性。','组合边界、复用规则和回归有效')]))+'</div>'+
    note('规则、流程、规划算法与LLM按收益选择。跨系统协调责任明确后，再评估独立Agent与动态规划的必要性。'))

add('04 / 案例A · 场景组合','后排儿童休息：组合能力，保持前排与座椅不变','需求：改善后排热舒适、降低灯光亮度；不改变前排设置，不移动座椅。',
    chips([1,2,4])+chips([1,3,5,6],'U')+
    svg('后排休息的功能组合与约束',
      box(25,110,315,180,'VCC场景任务',['匹配预定义流程','检查车型与区域能力','禁止座椅动作'],'dark')+
      box(500,10,420,150,'热舒适系统能力',['检查分区与共享资源','系统决定本域温控策略'],'teal')+
      box(500,270,420,150,'区域灯光能力',['优先复用；必要时重新封装','系统负责灯节点映射'],'teal')+
      box(1080,110,335,180,'场景结果',['分别判断子目标','核查前排约束','不能满足则明确反馈'])+
      line(340,150,490,80,'选择能力')+line(340,250,490,340,'选择能力')+
      line(920,80,1070,155,'执行反馈')+line(920,340,1070,250,'执行反馈')),
    '区域独立控制和主观舒适的评价方式需FO/SO确认。保持设置不变与实际热环境不变不是同一承诺，硬约束的具体含义应事先说明。')

add('04 / 案例A · 跨组织承接','用接口改造与真实采用，检验服务能力提升','首批成果具体到能力边界、接口差距和可验证结果。',
    flow([('FO / SO',['定义“改善”与限制','确认区域共享资源']),('矩阵 / 架构师',['复用、改造或封装','明确接口和反馈']),('系统SWE / 平台',['实现能力及必要机制','兼容原有消费方']),('VCC / 验证',['集成场景并联合测试','检查子目标和硬约束'])])+
    result('区域能力说明＋改造清单＋结果用例','热舒适/灯光团队建设；VCC采用','无座椅动作、前排约束正确、失败不漏报'),
    '矩阵不直接承诺系统实现排期；工程团队评估投入。能力封装不仅修改IDL，还需控制逻辑、兼容迁移和反馈实现。')

add('04 / 案例B · 运行调整','除雾启动、用户手动操作后，场景如何变化','持续任务必须认识到外部条件和控制权发生变化。',
    chips([3,4,5])+chips([2,3,4,6],'U')+
    svg('运行中事件与任务调整时间轴',
      line(60,210,1380,210)+
      ''.join(f'<circle cx="{x}" cy="210" r="9" fill="#17847a"/>' for x in [120,510,900,1300])+
      box(25,20,300,130,'① 休息场景运行',['热舒适与灯光目标','任务仍受持续约束'],'teal')+
      box(405,275,300,150,'② 除雾启动',['系统维持保护功能','VCC判断影响范围','调整受影响目标'],'orange')+
      box(785,20,300,150,'③ 用户手动介入',['系统上报已知变化','按规则让出控制','不误判原任务完成'])+
      box(1110,275,305,150,'④ 条件再次变化',['检查权限及当前条件','决定恢复或结束','反馈部分结果']),h=470)+
    note('恢复需要重新检查，不默认重放原始指令；系统产品始终保留本域保护和实时控制。'))

add('04 / 案例B · 联合验证','VCC协调任务，系统执行保护，平台保证信息可用','把竞争、延迟与缺失反馈纳入同一业务测试。',
    '<div class="responsibility"><article><span>业务与系统</span><h3>定义优先关系</h3><p>FO明确除雾、人工操作与休息需求关系；SO确认系统可承诺的行为。</p></article><article><span>VCC与平台</span><h3>处理变化与关联</h3><p>VCC调整任务；平台评估状态时效、请求关联及取消传播。</p></article><article><span>验证团队</span><h3>检查错误路径</h3><p>注入延迟、丢失和竞争，检查保护有效、接管正确及结果准确。</p></article></div>'+
    svg('异常路径验收',box(25,40,420,130,'及时反馈',['正确调整；报告受影响目标'],'teal')+box(510,40,420,130,'反馈缺失或过期',['无法确认；不伪造结束状态'],'orange')+box(995,40,420,130,'介入后请求恢复',['重新检查；不覆盖人工设置']),h=205)+
    note('成果：控制权与中断规则、运行需求及竞争用例。采用方：VCC、相关系统、平台和验证团队。'))

add('04 / 案例C · 场景复用','OTA之后，个人场景能否继续使用？','保存能力需求与限制，结合当前车型和版本重新判断，避免回放失效动作。',
    chips([1,6])+chips([1,5,6],'U')+
    svg('个人场景版本变化后的复用决策',
      box(25,155,320,150,'已有个人场景',['目标、对象、偏好和限制','依赖能力及适用信息'],'dark')+
      box(470,155,410,150,'检查能力、配置和版本',['工具报告变化影响','系统确认语义兼容性','VCC检查当前条件'])+
      line(345,230,460,230,'准备复用')+
      box(1020,5,395,110,'继续使用',['兼容且当前可用'],'teal')+
      box(1020,180,395,110,'调整并重新验证',['允许替代，保留硬约束'],'orange')+
      box(1020,355,395,110,'停止复用并说明',['不兼容或约束无法满足'])+
      line(880,185,1010,65)+line(880,230,1010,235)+line(880,275,1010,405)),
    '不承诺跨车型自动迁移所有偏好和控制参数；场景修改和替代需遵守既定授权，不擅自放宽硬约束。')

add('04 / 案例C · 持续演进','从个人复用，走向经过验证的产品场景','伴生与反馈用于发现需求，产品化仍需筛选、设计和验证。',
    flow([('记录与反馈',['需求、条件与执行结果','按授权收集使用反馈']),('个人场景复用',['检查当前能力与版本','保持目标和硬约束']),('产品化评估',['高频价值与可推广性','系统能力与投入可行性']),('预定义场景',['产品设计与联合验证','维护版本和回归集合'])])+
    result('能力兼容信息、依赖分析和回归用例','系统维护；工具提供分析；VCC采用','发现不兼容变化，阻止失效场景继续执行'),
    'DO在进入版本集成发布时参与。一次成功不是通用产品能力；伴生具体数据、权限及采集范围由相应业务规则明确。')

rows=[
('后排休息，前排不变','C1 / C2 / C4','U1 / U3 / U5 / U6','区域能力、接口改造与结果用例','热舒适/灯光建设；VCC采用','约束被遵守，子目标结果可判断'),
('除雾及人工操作后调整','C3 / C4 / C5','U2 / U3 / U4 / U6','控制权规则、时效需求与竞争用例','VCC/系统定义；平台与测试支撑','保护有效，接管正确，不错误恢复'),
('OTA后复用个人场景','C1 / C6','U1 / U5 / U6','兼容信息、影响查询与回归集合','系统/工具建设；VCC采用；DO按需参与','发现变化，调整或阻止失效复用')]
add('05 / 需求追溯','需求、成果和采用方，必须能够相互追溯','三组首批案例将六条关键能力与六项提升落到实际工作对象。',
    '<table class="trace"><thead><tr>'+''.join('<th>'+s+'</th>' for s in ['业务需求','关键能力','矩阵提升','具体成果','建设与采用方','验证依据'])+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+s+'</td>' for s in r)+'</tr>' for r in rows)+'</tbody></table>'+
    note('C为业务所需能力，U为矩阵提升方向。专题启动时进一步明确负责人、版本、投入与验证环境。'))

add('05 / 成效评价','技术做成、团队采用、业务有效，分别衡量','用首批案例建立基线，再评价收益；不以接口数量或规范数量代替成效。',
    cards([('01','SOA技术能力','能力抽象与反馈是否完整；时效与异常机制是否达标；变更影响是否查全。'),('02','组织采用效果','VCC和系统是否实际采用；重复适配和重复策略是否减少；问题是否更早发现。'),('03','车控业务效果','场景是否满足需求；用户纠正是否减少；冲突、部分失败和介入是否被正确处理。')])+
    note('先测现状，再比较改造后的效果。Mock、SDK、台架与实车测试分别提供对应层次的证据。'))

add('05 / 建议决策','先确认首批案例和协作投入，把方向变成证据','用真实采用验证矩阵提升，再决定扩展范围和后续平台建设。',
    cards([('A','确认业务与系统负责人','以案例A为起点，明确能力范围、约束和结果；同步准备案例B/C的验证输入。'),('B','确认共建团队与投入','FO、SO、VCC、架构、SWE、平台、工具与测试按专题参与，维护责任明确。'),('C','确认试验与推广出口','形成接口与实现改造、底座需求和联合验证记录；通过后纳入规范与工程计划。')])+
    '<div class="closing">从“有接口可调用”，提升到<br><strong>“有系统能力可组合，有执行结果可判断”。</strong></div>',
    '虚拟能力中心不替代业务开发、项目发布及独立软件架构组织。独立Agent、动态规划和LLM分别根据收益与代价判断，不由技术趋势直接推导必要性。')

CSS = '''
:root{--paper:#f5f3ed;--ink:#173642;--muted:#5f7478;--teal:#17847a;--line:#cbd6ce;--orange:#bf6944;--sans:"Microsoft YaHei","Noto Sans CJK SC",sans-serif}*{box-sizing:border-box}html{scroll-snap-type:y mandatory}body{margin:0;font-family:var(--sans);color:var(--ink);background:var(--paper)}h1,h2,h3,p{margin:0}button{font:inherit;cursor:pointer}a{color:inherit;text-decoration:none}.slide{height:100svh;min-height:650px;padding:7.5vh 7.2vw 8vh 5.8vw;display:flex;flex-direction:column;overflow:hidden;position:relative;scroll-snap-align:start;scroll-snap-stop:always}.slide:after{content:"";height:1px;position:absolute;left:5.8vw;right:7.2vw;bottom:6.2vh;background:var(--line)}.eyebrow{font-size:clamp(11px,.87vw,17px);color:var(--teal);letter-spacing:.09em;margin-bottom:1.5vh;font-weight:650}.eyebrow span{margin-right:1.4em}h1{font-size:clamp(48px,4.7vw,90px);line-height:1.18;letter-spacing:-.035em}h2{font-size:clamp(27px,2.75vw,54px);line-height:1.22;letter-spacing:-.035em}h3{font-size:clamp(18px,1.65vw,32px);line-height:1.4}.lead{font-size:clamp(14px,1.25vw,25px);line-height:1.55;color:var(--muted);margin-top:1.5vh}.body{flex:1;min-height:0;display:flex;flex-direction:column;justify-content:center;gap:1.7vh;margin-top:2.8vh}.diagram{width:100%;flex:1;min-height:0;display:block;font-family:var(--sans)}.takeaway{border-left:4px solid var(--teal);background:#e5ece2;padding:1.3vh 1.3vw;font-size:clamp(13px,1.13vw,22px);line-height:1.55;flex-shrink:0}.chips{display:flex;flex-wrap:wrap;gap:.45vw;flex-shrink:0}.chip{padding:.2em .65em;font-size:clamp(10px,.85vw,16px);border:1px solid #b1cbc0;background:#e3eee5;color:#246157;border-radius:20px}.chip.u{background:#f0e7dc;border-color:#d6bca8;color:#835138}.deliver{display:grid;grid-template-columns:1fr 1.08fr 1.1fr;gap:1.5vw;border-top:1px solid var(--line);padding-top:1.2vh;flex-shrink:0}.deliver b{display:block;color:var(--teal);font-size:clamp(10px,.8vw,15px);margin-bottom:.5vh}.deliver span{font-size:clamp(12px,1vw,19px);line-height:1.5}.cover{justify-content:center}.cover .body{flex:0;gap:3vh;margin-top:4vh}.cover .lead{font-size:clamp(18px,1.7vw,34px);margin-top:3vh}.cover-route{display:flex;align-items:center;gap:1.4vw;font-size:clamp(16px,1.5vw,29px)}.cover-route span{border-bottom:3px solid var(--teal);padding:.45em 0}.cover-route i{font-style:normal;color:var(--teal)}.cover-message{font-size:clamp(15px,1.4vw,27px);line-height:1.65;color:var(--muted)}.cover-meta{font-size:clamp(11px,.95vw,18px);color:var(--muted)}.cap-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:2vh 2vw}.cap-grid article{display:flex;gap:1.3vw;border-top:2px solid var(--line);padding:2vh 0}.cap-grid b{font-size:clamp(27px,3vw,58px);font-weight:400;color:var(--teal);line-height:1.1}.cap-grid p{font-size:clamp(12px,1.05vw,21px);color:var(--muted);margin-top:.8vh}.mapping{display:grid;grid-template-columns:19% 59% 22%;align-items:stretch;min-height:0}.map-goal,.map-dual{background:var(--ink);color:white;padding:2.2vh 1.5vw;display:flex;flex-direction:column;justify-content:center;gap:2vh}.map-goal span,.map-dual b{color:#d8e9af;font-size:clamp(12px,1.1vw,21px)}.map-goal p,.map-dual p{font-size:clamp(12px,1.1vw,21px);line-height:1.7}.map-dual{background:#e0eadd;color:var(--ink)}.map-dual b{color:var(--teal)}.map-dual strong{font-size:clamp(12px,1vw,20px);border-top:1px solid #b5c7b9;padding-top:1.5vh}.map-links{padding:0 1.8vw;display:flex;flex-direction:column;justify-content:space-between}.map-links>div{display:grid;grid-template-columns:29% 5% 66%;align-items:center;padding:1.45vh 0;border-bottom:1px solid var(--line);font-size:clamp(11px,1vw,20px);line-height:1.6}.map-links i{color:var(--teal);font-style:normal}.map-links span{padding-left:.8vw}.dual-lanes{display:grid;grid-template-columns:19% 62% 19%;align-items:stretch}.lane-label,.lane-end{background:var(--ink);color:#c0d6cb;padding:3vh 1.4vw;display:flex;flex-direction:column;justify-content:center;font-size:clamp(13px,1.2vw,24px);line-height:1.8}.lane-label strong,.lane-end strong{font-size:clamp(18px,1.65vw,32px);color:white}.lane-end{background:#dce8d8;color:var(--teal)}.lane-end strong{color:var(--ink)}.lane-content{padding:0 1.5vw;display:flex;flex-direction:column;gap:2vh}.lane-content article{padding:2.3vh 1.5vw;border:1px solid var(--line);background:#eef0e8}.lane-content b{font-size:clamp(17px,1.4vw,27px);color:var(--teal)}.lane-content article>div{display:flex;gap:.7vw;align-items:center;margin:1.5vh 0;font-size:clamp(12px,1.05vw,20px)}.lane-content span{border-bottom:2px solid #adc5b6;padding:.5em 0}.lane-content i{font-style:normal;color:var(--teal)}.lane-content p{font-size:clamp(11px,.95vw,18px);color:var(--muted)}.swim{display:flex;flex-direction:column;gap:1vh}.swim-head,.swim-row{display:grid;grid-template-columns:17% repeat(4,1fr);gap:.7vw;align-items:stretch}.swim-head{font-size:clamp(11px,1vw,20px);color:var(--teal);padding-bottom:1vh}.swim-row strong,.swim-row span{padding:1.5vh .8vw;font-size:clamp(11px,.97vw,19px);line-height:1.65;background:#e8ede5}.swim-row strong{background:var(--ink);color:white;font-size:clamp(11px,.95vw,18px);display:flex;align-items:center}.org-layout{display:grid;grid-template-columns:38% 62%;min-height:0}.org-core{background:var(--ink);color:white;padding:4vh 2.2vw;display:flex;flex-direction:column;justify-content:center;gap:2vh;border-right:8px solid var(--teal)}.org-core span{color:#dbe8a4;font-size:clamp(13px,1.1vw,21px)}.org-core p{font-size:clamp(12px,1.1vw,21px);line-height:1.8;color:#c9d8d1}.org-branches{display:flex;flex-direction:column;gap:1.5vh;padding-left:2vw}.org-branches article{border-left:3px solid #98b9a5;background:#e8ede3;padding:1.8vh 1.4vw}.org-branches b{font-size:clamp(16px,1.3vw,25px)}.org-branches p{font-size:clamp(12px,1vw,20px);line-height:1.65;color:var(--muted);margin-top:.8vh}.stairs{display:grid;grid-template-columns:repeat(3,1fr);gap:2vw;align-items:start;padding-top:1vh}.stairs article{margin-top:calc((2 - var(--step))*3.6vh);padding:2.6vh 1.5vw;background:#e3eadd;border-top:5px solid var(--teal)}.stairs span{color:var(--teal);font-size:clamp(12px,.95vw,18px)}.stairs h3{margin:1.5vh 0}.stairs p{font-size:clamp(12px,1.05vw,20px);line-height:1.7;color:var(--muted)}.stairs strong{display:block;font-size:clamp(11px,.9vw,18px);line-height:1.6;border-top:1px solid #bdccb9;margin-top:2.5vh;padding-top:1.5vh}.responsibility,.cards{display:grid;grid-template-columns:repeat(3,1fr);gap:2vw}.responsibility article,.cards article{border-top:3px solid var(--teal);padding:2vh 1.3vw;background:#e8ede4}.responsibility span,.index{font-size:clamp(12px,1vw,20px);color:var(--teal)}.index{font-size:clamp(30px,3.3vw,64px)}.responsibility h3,.cards h3{margin:1.3vh 0}.responsibility p,.cards p{font-size:clamp(12px,1.1vw,21px);line-height:1.8;color:var(--muted)}.trace{width:100%;border-collapse:collapse;font-size:clamp(11px,.99vw,19px);line-height:1.8}.trace th{text-align:left;color:var(--teal);padding:1.3vh .7vw;border-bottom:2px solid var(--ink);font-size:.92em}.trace td{vertical-align:top;padding:2.6vh .7vw;border-bottom:1px solid var(--line)}.trace th:nth-child(1){width:17%}.trace th:nth-child(2){width:12%}.trace th:nth-child(3){width:17%}.trace th:nth-child(4){width:18%}.trace th:nth-child(5){width:20%}.closing{font-size:clamp(23px,2.2vw,43px);line-height:1.55;margin-top:2vh}.closing strong{color:var(--teal)}.notes{display:none}.topbar{position:fixed;top:2.2vh;left:5.8vw;right:4vw;z-index:10;display:flex;justify-content:space-between;color:var(--muted);font-size:clamp(10px,.78vw,15px)}.footer{position:fixed;left:5.8vw;right:23vw;bottom:2.2vh;z-index:10;display:flex;justify-content:space-between;font-size:clamp(10px,.8vw,15px);color:var(--muted);pointer-events:none}.controls{position:fixed;right:2vw;bottom:1.8vh;display:flex;gap:.5vw;z-index:30}.controls button{border:1px solid var(--line);background:var(--paper);color:var(--ink);border-radius:50%;width:34px;height:34px;font-size:14px}.controls button:hover{background:#dce7b7}button:focus-visible,a:focus-visible{outline:3px solid var(--orange);outline-offset:3px}.rail{position:fixed;right:2.5vw;top:50%;transform:translateY(-50%);display:flex;flex-direction:column;gap:6px;z-index:20}.rail button{border:0;background:#afc2b8;border-radius:3px;width:5px;height:5px;padding:0}.rail button.active{height:19px;background:var(--teal)}.progress{height:3px;background:var(--teal);position:fixed;top:0;left:0;z-index:40}.overview{position:fixed;inset:0;background:#173642fa;color:white;z-index:60;padding:6vh 6vw;overflow:auto}.overview[hidden],.notes-panel[hidden]{display:none}.overview-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:1.3vw;margin-top:3vh}.overview-grid button{background:#ffffff0b;color:white;border:1px solid #ffffff33;text-align:left;padding:1.5vh 1.2vw;font-size:clamp(12px,1vw,20px)}.overview-grid span{display:block;color:#dce7b7;margin-bottom:1vh;font-size:.85em}.overview-close{position:absolute;right:3vw;top:3vh;border:0;background:transparent;color:white;font-size:28px}.notes-panel{position:fixed;z-index:50;bottom:8vh;left:6vw;right:8vw;padding:2.5vh 2vw;color:white;background:#173642fa;border-top:4px solid #dce7b7;font-size:clamp(13px,1.1vw,21px);line-height:1.7;max-height:45vh;overflow:auto}.notes-panel h3{color:#dce7b7;font-size:1em}.toast{position:fixed;bottom:10vh;left:35vw;padding:15px;background:var(--ink);color:white;z-index:80}
@media(max-width:800px){html{scroll-snap-type:none}.slide{height:auto;min-height:100svh;padding:85px 7vw 95px;overflow:visible}.slide:after{left:7vw;right:7vw;bottom:65px}.body{min-height:0;flex:none;gap:22px;margin-top:25px}.diagram{flex:none;min-height:0;width:100%;height:auto}.deliver,.cards,.responsibility,.cap-grid,.mapping,.dual-lanes,.org-layout,.stairs{grid-template-columns:1fr}.deliver{gap:15px}.takeaway{font-size:14px}.map-links{padding:15px 0}.map-links>div{font-size:12px}.map-goal,.map-dual,.lane-label,.lane-end{padding:20px}.map-goal h3 br,.lane-label strong br,.lane-end strong br{display:none}.lane-content{padding:20px 0}.org-core{padding:25px}.org-branches{padding:20px 0}.stairs article{margin-top:0}.cap-grid{gap:12px}.cap-grid article{padding:15px 0;gap:15px}.chips{gap:7px}.chip{font-size:10px}.topbar{left:7vw;font-size:9px}.footer{left:7vw;font-size:9px}.overview-grid{grid-template-columns:1fr 1fr}.trace{font-size:10px;line-height:1.6}.trace td,.trace th{padding:12px 5px}.swim-row span,.swim-row strong{font-size:10px;padding:8px 5px}.cover-route{gap:12px;flex-wrap:wrap}.cover .lead{font-size:20px}.cover-message{font-size:16px}.closing{font-size:24px}.rail{right:2vw}}
@media(prefers-reduced-motion:reduce){*{scroll-behavior:auto!important;transition:none!important}}
@media print{@page{size:297mm 167mm;margin:0}html{scroll-snap-type:none}body{-webkit-print-color-adjust:exact;print-color-adjust:exact}.slide{width:297mm;height:167mm;min-height:0;padding:12mm 18mm 14mm;break-after:page;overflow:hidden}.slide:after{bottom:10mm;left:18mm;right:18mm}.topbar,.footer,.controls,.rail,.progress,.overview,.notes-panel{display:none!important}h1{font-size:38pt}h2{font-size:26pt}.lead{font-size:12pt}.eyebrow{font-size:8pt}.body{margin-top:5mm;gap:3mm}.takeaway{font-size:10pt;padding:2mm 3mm}.chip{font-size:8pt}.deliver b{font-size:7pt}.deliver span{font-size:9pt}.cards h3,.cap-grid h3,.org-core h3{font-size:16pt}.cards p,.responsibility p,.org-branches p{font-size:10pt}.trace{font-size:9pt}.trace td{padding:3mm 2mm}.map-links>div{font-size:9pt}.map-goal h3{font-size:18pt}.map-goal p,.map-dual p{font-size:10pt}.closing{font-size:21pt}}
'''

parts=[]
for i,s in enumerate(slides,1):
    tag='h1' if s['cover'] else 'h2'
    title=s['title'].replace('<br>',' ')
    parts.append(f'<section class="slide{" cover" if s["cover"] else ""}" id="s{i}" data-title="{e(title)}" data-chapter="{e(s["chapter"])}" aria-labelledby="t{i}"><div class="eyebrow"><span>{i:02}</span>{e(s["chapter"])}</div><{tag} id="t{i}">{s["title"]}</{tag}><p class="lead">{e(s["lead"])}</p><div class="body">{s["body"]}</div><aside class="notes">{e(s["notes"])}</aside></section>')
html='<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>智能化车控导向的服务架构矩阵提升规划 · V2.4</title><style>'+CSS+'</style></head><body><div class="progress" id="progress"></div><header class="topbar"><span>SOA MATRIX / 智能化车控</span><span>V2.4 · 2026.11.17</span></header><main>'+''.join(parts)+'</main><footer class="footer"><span id="chapter-name"></span><span id="page-number"></span></footer><nav class="controls" aria-label="演示控制"><button id="prev" aria-label="上一页">↑</button><button id="next" aria-label="下一页">↓</button><button id="overview-toggle" aria-label="目录">目</button><button id="notes-toggle" aria-label="讲述提示" aria-pressed="false">注</button><button id="fullscreen-toggle" aria-label="全屏">⛶</button></nav><nav id="rail" class="rail" aria-label="页面跳转"></nav><aside class="notes-panel" id="notes-panel" hidden></aside><div class="overview" id="overview" role="dialog" aria-modal="true" aria-label="报告目录" hidden><button class="overview-close" id="overview-close" aria-label="关闭目录">×</button><h2>报告目录</h2><div class="overview-grid" id="overview-grid"></div></div><script>'+FRAME.joinpath('deck.js').read_text()+'</script></body></html>'
assert len(slides)==24
ROOT.joinpath('matrix_planning_v2_4.html').write_text(html)
ROOT.joinpath('matrix_planning_v2_4_content.json').write_text(json.dumps(slides,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'slides':len(slides),'diagrams':serial,'tables':html.count('<table'),'bytes':len(html.encode())}))
