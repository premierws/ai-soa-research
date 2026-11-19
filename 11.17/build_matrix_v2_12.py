"""Replace part three with six focused platform capability planning slides."""
from pathlib import Path
from html import escape as E
import json

ROOT=Path(__file__).parent
old=json.loads((ROOT/'matrix_planning_v2_11_content.json').read_text())
base=(ROOT/'matrix_planning_v2_11.html').read_text()
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


def p(n,title,lead,body,notes=''):
 return dict(chapter=f'第4部分 / 4.{n} '+['组织与职责','议题接收与分类','评审决策与实施衔接','成果采用与闭环','冲突协调与上升','日常运营与持续改进'][n-1],title=title,lead=lead,body=body,notes=notes,part=4,cover=False)
org=p(1,'组织运营：以常驻骨干统筹，按专题组织共建',
 '围绕四项能力落实专业负责人，由业务、系统和平台团队共同提出需求、建设与采用。',
 svg('矩阵常驻骨干、四项专题与责任团队',
 box(25,0,1390,100,'常驻骨干：矩阵负责人、SOA专业骨干与TPM',['统筹建设方向、安排议题评审、协调跨团队依赖、维护决策与成果记录'],'dark')+
 ''.join(box(x,155,325,125,t,[a],'teal') for x,t,a in [(25,'场景服务定义范式','FO / SO与服务设计骨干'),(380,'外部交互语义','VCC / NOMI与接口骨干'),(735,'中间件基础能力','平台架构师与平台SWE'),(1090,'自适应编排支撑','系统 / 领域架构与工具SWE')])+
 ''.join(arrow(x,105,x,145) for x in [185,540,895,1250])+
 box(25,345,675,145,'专题组织：一位牵头人，明确共建与采用方',['按议题邀请FO、SO、车型AI、架构师和测试','建设与维护责任由所属团队确认'])+
 box(740,345,675,145,'责任团队：落实人员、实现与工程采用',['SWE实施，测试和使用方验证；DO按需参与','矩阵协调共性方案，不替代业务及软件架构组织'])),
 '组织形式为改进建议。继承原矩阵常驻架构骨干与TPM、其余按议题参与的机制；按现行公司角色更新表达。专题不是新设行政组织，成员投入与责任由所属团队承诺。')
intake=p(2,'议题接收：从业务问题形成可承接的建设任务',
 '沿用议题登记与跟踪机制，将场景需求、接口问题和运行验证结果纳入同一入口。',
 svg('议题来源、登记、分类与承接',
 box(25,20,400,200,'需求与问题来源',['VCC / NOMI：场景与交互需求','FO / SO：系统能力和执行限制','平台与测试：运行、资源及缺陷'])+
 box(520,20,400,200,'TPM登记，专业骨干初审',['明确问题、影响与提出方','确认对应建设方向和责任范围','补齐资料，识别依赖与采用方'],'dark')+
 box(1015,20,400,200,'形成可评审议题',['专题牵头人与相关责任团队','预期成果、验收要求与计划','待决策事项及可选方案'],'teal')+
 arrow(425,115,510,115)+arrow(920,115,1005,115)+
 box(25,320,420,165,'共性能力建设',['归入四项能力建设专题','统一方案，安排试点采用'])+
 box(510,320,420,165,'常规变更与单系统问题',['转既有服务变更或缺陷流程','必要时提取共性改进需求'])+
 box(995,320,420,165,'紧急故障或安全风险',['立即进入责任团队处置流程','矩阵并行支持，不等待例会'])),
 '沿用原议题登记表、材料归档和TPM收集机制。入口统一指统一追踪，不要求新增IT平台或把所有问题都提交矩阵审批。紧急问题由既有故障、安全等流程处理。')
decision=p(3,'评审与实施：先明确方案，再落实责任团队承接',
 '评审同时确认功能边界、实现可行性、性能资源影响和验证方法，避免只形成会议结论。',
 svg('方案评审到责任团队实施的流程',
 box(25,20,420,245,'联合形成方案',['FO / SO：功能与保护边界','VCC / NOMI：使用与反馈要求','架构师 / SWE：可行性与资源','测试：验证范围与判定依据'])+
 box(510,20,420,245,'矩阵评审与决策',['通过：明确成果和承接安排','有条件通过：列明条件和责任','不通过：说明原因，修改重审','超出权限或无法一致：上升决策'],'dark')+
 box(995,20,420,245,'责任团队实施与集成',['所属团队确认投入、计划和接口','按既有需求与研发流程实施','涉及服务发布，衔接变更审批','TPM跟踪依赖与阻塞'],'teal')+
 arrow(445,140,500,140)+arrow(930,140,985,140)+
 box(25,360,1390,125,'评审必须留下：方案版本、决策依据、适用范围、责任人及后续行动',['有条件通过的议题，在条件满足并确认前，不视为可直接实施或发布'])),
 '原章程已有通过、不通过、有条件通过三类结论；原流程要求方案拉齐、影响评估、决策后进入实施，NPT CCB及NDTC发布审批以矩阵结论为输入。这里保留与既有审批衔接，不替代审批权限。软件架构事项交由独立软件架构组织按其职责评估。')
closure=p(4,'成果闭环：以实际采用和验证完成作为关闭依据',
 '平台成果进入业务使用流程，既验证方案是否有效，也明确后续由谁维护。',
 svg('共性成果到工程采用与反馈闭环',
 box(25,10,420,245,'形成可用成果',['场景定义范式：模板与实例','交互语义：规范与典型时序','中间件：需求、改进与验证','自适应编排：规则与工具'])+
 box(510,10,420,245,'由采用方核实有效性',['VCC / NOMI验证接入与反馈','FO / SO验证功能及系统边界','平台团队验证机制、性能与资源','SWE / 测试完成集成及验证'],'dark')+
 box(995,10,420,245,'完成关闭并转入维护',['成果版本可查，适用范围明确','采用方确认，验证证据齐全','遗留项单列并落实责任与计划','维护方确认后续变更和兼容'],'teal')+
 arrow(445,125,500,125)+arrow(930,125,985,125)+
 route('M1205,270 V330 H235 V270')+text(720,318,'采用中的新问题 → 返回专题修订与验证',23,'#17847a','middle')+
 box(25,380,1390,110,'区分两类进度：方案已评审 / 采用已验证',['能力规范以试点应用证明可用；涉及实现的成果还需按范围完成集成和运行验证'])),
 '原矩阵已有端到端闭环及服务验证职责，本次将“决策完成”与“采用验证完成”分开。各议题按其成果性质确认关闭，不要求每项规范必然形成代码。后续横展需求单列，不无限延长首批试点议题。')
escalation=p(5,'冲突上升：按问题性质找到有权决策的责任方',
 '先由专题协调；超出职责、无法达成一致或影响关键计划时，携带事实与备选方案上升。',
 svg('冲突分类协调与上升决策流程',
 box(25,10,1390,90,'专题内协调：明确分歧、影响范围、备选方案及推荐意见',[],'dark')+
 ''.join(arrow(x,110,x,150) for x in [235,720,1205])+
 box(25,160,420,220,'功能与系统边界冲突',['FO / SO与VCC先明确需求','跨系统边界：协同系统架构矩阵','仍无法一致：提交授权技术评审'])+
 box(510,160,420,220,'软件与平台方案冲突',['平台及领域架构师评估影响','涉及软件架构：协同其独立矩阵','重大技术取舍：提交技术决策渠道'])+
 box(995,160,420,220,'资源与计划冲突',['TPM协调所属团队负责人','明确优先级、投入和依赖影响','由资源及业务负责人作出取舍'],'teal')+
 box(25,420,1390,65,'上升结论回写议题：决策人、理由、执行条件、责任团队与后续验证'))+
 note('系统安全与保护要求按既有责任和审批机制处理；矩阵不以多数表决放宽执行边界。'),
 '原白板显示关键技术方案上升VAS技术评审/技术委员会，与系统架构矩阵、软件架构矩阵及SOA架构战队协作；本页按性质分流是改进建议。原资料同时出现VMBC/VAS称谓，现行授权机构及名称需确认，不将旧名称直接宣称为当前制度。')
operation=p(6,'持续运营：让议题、建设计划和成果库保持一致',
 '沿用周或双周例会，以专题推进建设、以采用结果检查成效，避免矩阵只承担会议组织。',
 svg('例会运营与周期复盘',
 box(25,20,420,245,'会前：把需要决策的议题准备好',['TPM维护统一议题台账','牵头人补齐材料与行动进展','提前邀请有权决策和承接的人','一般进展异步更新，阻塞提前暴露'])+
 box(510,20,420,245,'会中：聚焦方案与跨团队阻塞',['评审关键方案及变更影响','确认结论、条件与责任团队','处理依赖；无法解决则上升','确认下一步行动与检查节点'],'dark')+
 box(995,20,420,245,'会后：跟踪采用，更新成果',['TPM记录决定并跟踪行动','牵头人推动实施与联合验证','采用方确认效果与剩余问题','维护方更新规范、实例和工具'],'teal')+
 arrow(445,135,500,135)+arrow(930,135,985,135)+
 box(25,355,675,135,'周期复盘：投入是否支持建设重点',['核查四项建设的资源、依赖与采用进展','根据业务优先级调整专题及参与投入'])+
 box(740,355,675,135,'运营成效：看采用与问题改善',['成果被哪些团队采用，哪些阻塞已解决','反复问题是否减少，未关闭事项为何停滞'])),
 '周/双周为原矩阵例会节奏；专题分工、异步更新和采用成效复盘为建议增强。沿用现有议题表、跟踪票及文档/工具库，不预设新系统、硬性周期指标或人员数量。')
slides=[dict(s) for s in old[:14]]
parts=['业务目标与车控Agent能力','执行边界与关键交互','矩阵关键能力建设','矩阵运营与协作机制']
def roadmap(active):
 return '<div class="part-roadmap">'+''.join(f'<div class="{ "current" if i==active else ""}"><span>{i:02}</span><b>{t}</b></div>' for i,t in enumerate(parts,1))+'</div>'
import re
for s in slides:
 if s.get('divider'):s['body']=re.sub(r'<div class="part-roadmap">.*$',roadmap(s['part']),s['body'])
divider=dict(title='04　矩阵运营与协作机制',chapter='第4部分 / 内容导览',lead='围绕四项能力建设，明确如何组织、如何承接议题，以及如何推动成果采用和问题闭环。',body='<div class="part-intro"><div class="part-number">04</div><div class="part-topics"><h3>接下来说明</h3><ol><li>组织与职责：常驻统筹、专题共建</li><li>工作闭环：接收、评审、实施与采用</li><li>运营机制：冲突上升、日常跟踪与复盘</li></ol></div></div>'+roadmap(4),notes='合并原第四、第五部分，依据原服务架构矩阵章程及工作流提出运营改进；本部分为建议机制，现行授权与资源承诺需由责任组织确认。',cover=False,divider=True,part=4)
slides += [divider,org,intake,decision,closure,escalation,operation]
for s in slides:
 s['chapter']=s['chapter'].replace('V2.11','V2.12');s['body']=s['body'].replace('V2.11','V2.12')
before,tail=base.split('<main>',1);_,after=tail.split('</main>',1)
rendered=[]
for i,s in enumerate(slides,1):
 tag='h1' if s['cover'] else 'h2';cls='slide'+(' cover' if s['cover'] else '')+(' part-divider' if s.get('divider') else '')
 rendered.append(f'<section class="{cls}" id="s{i}" data-title="{E(s["title"].replace("<br>"," "),quote=True)}" data-chapter="{E(s["chapter"],quote=True)}" data-part="{s.get("part",0)}" aria-labelledby="t{i}"><div class="eyebrow"><span>{i:02}</span>{E(s["chapter"])}</div><{tag} id="t{i}">{s["title"]}</{tag}><p class="lead">{E(s["lead"])}</p><div class="body">{s["body"]}</div><aside class="notes">{E(s["notes"])}</aside></section>')
css='.part-roadmap{grid-template-columns:repeat(4,1fr)}@media(max-width:800px){.part-roadmap{grid-template-columns:1fr 1fr}}'
html=(before+'<main>'+''.join(rendered)+'</main>'+after).replace('V2.11','V2.12').replace('</style>',css+'</style>')
ROOT.joinpath('matrix_planning_v2_12.html').write_text(html)
ROOT.joinpath('matrix_planning_v2_12_content.json').write_text(json.dumps(slides,ensure_ascii=False,indent=2)+'\n')
ROOT.joinpath('matrix_v2_12_revision_notes.md').write_text('''# V2.12 矩阵运营与协作机制

合并原第四、第五部分，形成第四部分：1页目录、6页正文（第15—21页）。前三部分正文保留，仅更新封面版本、分隔页四部分目录。

## 改版内容

常驻骨干与四项专题共建；统一议题登记与分类承接；方案评审及实施衔接；成果采用与验证闭环；按职责冲突协调与上升；例会及周期复盘。

矩阵定位虚拟COE，提供共性方案和协调，不接管业务、系统保护、软件架构及发布职责。各所属团队承诺投入并实施。规范类成果以试点采用验证，涉及代码类成果按范围完成集成验证。

## 依据与新增建议

原矩阵章程：references/organization/service_architecture_matrix_charter_snapshot_2026-11-13.md；原工作流及协作白板：references/organization/whiteboards/text_index_2026-11-13.md。

沿用原资料的常驻/按议题参与、TPM运营、议题登记、三类评审结论、影响评估、关键方案上升、决策回BU实施、发布审批衔接和周/双周例会。新增四项专题承接、采用验证关闭条件、按冲突性质分流与运营成效检查。

新组织设置与优化机制均为建议；旧资料中的VAS/VMBC技术决策渠道名称不直接当作现行授权规定。当前审批主体、成员及投入由责任组织确认。HTML不设置参考材料和附录页。
''')
assert len(slides)==21
for i in range(1,14):
 if not old[i].get('divider'):assert slides[i]==old[i]
print(json.dumps({'slides':len(slides),'bytes':len(html.encode()),'part4_start':15}))
