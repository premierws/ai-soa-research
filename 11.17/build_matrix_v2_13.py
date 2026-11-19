"""Replace part three with six focused platform capability planning slides."""
from pathlib import Path
from html import escape as E
import json

ROOT=Path(__file__).parent
old=json.loads((ROOT/'matrix_planning_v2_12_content.json').read_text())
base=(ROOT/'matrix_planning_v2_12.html').read_text()
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



slides=[dict(s) for s in old[:14]]
slides[0]['lead']='以智能化车控需求为牵引，明确平台能力建设方向，完善矩阵组织与运营机制。'
slides[0]['body']='<div class="cover-route"><span>车控Agent能力与执行边界</span><i>→</i><span>矩阵平台能力建设</span><i>→</i><span>组织运营与成果闭环</span></div><p class="cover-message">以SOA为基础，支撑场景能力建设；<br>以专题共建和成果采用，推动能力落地。</p><div class="cover-meta">V2.13 审阅版　｜　2026.11.18</div>'
# Draw the three-layer Agent group before all existing nodes and arrows.
s=slides[3];s['body']=s['body'].replace('</defs>','</defs><rect x="248" y="120" width="1054" height="375" rx="16" fill="#d6e8df" stroke="#17847a" stroke-width="3"/>',1)
s['body']=s['body'].replace('</svg>','<text x="10" y="435" font-size="25" fill="#17847a" font-weight="650">车控Agent</text><text x="10" y="470" font-size="22" fill="#17847a">主体范围</text><path d="M175,444 H243" stroke="#17847a" stroke-width="2" fill="none"/></svg>',1)
s['notes']+=' 接入、组织协调仲裁、任务分解与运行管理三层共同组成车控Agent主体，使用统一背景框表示；用户意图识别层与系统执行层在主体外。'
slides[5]['body']=slides[5]['body'].replace('基础能力调用接口','基础能力服务接口')
parts=['业务目标与车控Agent能力','执行边界与关键交互','矩阵关键能力建设','矩阵运营与协作机制']
def roadmap(active):
 return '<div class="part-roadmap">'+''.join(f'<div class="{ "current" if i==active else ""}"><span>{i:02}</span><b>{t}</b></div>' for i,t in enumerate(parts,1))+'</div>'
third=dict(title='03　矩阵关键能力建设',chapter='第3部分 / 内容导览',lead='从场景定义、外部交互、通信运行和服务编排四个方面，形成支撑车控Agent的共性能力。',body='<div class="part-intro"><div class="part-number">03</div><div class="part-topics"><h3>接下来说明</h3><ol><li>定义与交互：规范场景服务，统一请求与执行反馈</li><li>运行与编排：提出中间件要求，支持受约束的服务组合</li><li>共建与采用：落实团队、投入和验证责任</li></ol></div></div>'+roadmap(3),notes='增加独立第三部分分隔页，概括四项建设与资源承接，详细总览与六页正文保留。',cover=False,divider=True,part=3)
slides.insert(8,third)
# Existing overview links move forward one page; change them exactly once.
import re
slides[9]['body']=re.sub(r'href="#s(\d+)"',lambda m:f'href="#s{int(m[1])+1}"',slides[9]['body'])
slides[9]['body']=re.sub(r'<nav class="chapter-agenda"[^>]*>.*?</nav>','',slides[9]['body'],count=1)
slides[9]['lead']='围绕四项能力明确目标、差距和建设方案，落实成果采用及所需资源。'
slides[9]['notes']=slides[9]['notes'].replace('本页合并原第三部分导览与总览，不再单设分隔页。','本页为第三部分能力建设总览，前置独立分隔页。')
divider=dict(old[14]);divider['body']=divider['body'].replace('<li>工作闭环：接收、评审、实施与采用</li>','<li>议题闭环：接收、评审、实施与采用</li>').replace('<li>运营机制：冲突上升、日常跟踪与复盘</li>','<li>协调运营：冲突上升、日常跟踪与复盘</li>')
org=dict(old[15]);org['chapter']='第4部分 / 4.1 组织与职责'
org['body']=org['body'].replace('矩阵负责人、SOA专业骨干与TPM','矩阵负责人、SOA专业骨干')
org['notes']=org['notes'].replace('与TPM','')
workflow=dict(chapter='第4部分 / 4.2 议题接收与成果闭环',title='议题闭环：从需求接收到成果采用',lead='沿用议题登记、方案评审和责任团队实施流程，补强采用验证与成果维护。',body=svg('议题接收评审实施采用闭环',
box(25,20,300,270,'01 接收与分类',['TPM登记业务与平台问题','明确问题、影响和采用方','归入四项能力建设专题','常规变更转既有流程'])+
box(395,20,300,270,'02 评审与决策',['专题牵头联合形成方案','评估边界、可行性及资源','明确通过条件与责任人','有分歧按权限上升'],'dark')+
box(765,20,300,270,'03 实施与验证',['所属团队确认投入与计划','SWE实现、测试联合验证','VCC及系统团队试点采用','涉及发布衔接既有审批'])+
box(1135,20,280,270,'04 关闭与维护',['采用方确认效果','验证证据与版本可查','遗留项落实责任与计划','维护方承接后续变更'],'teal')+
arrow(325,150,385,150)+arrow(695,150,755,150)+arrow(1065,150,1125,150)+
route('M1275,305 V355 H175 V305')+text(720,343,'采用中发现共性问题，返回专题修订与验证',23,'#17847a','middle')+
box(25,410,1390,70,'关闭依据：成果可用、采用已验证、维护有责任；方案评审通过仅是过程节点'))+note('紧急故障与安全风险立即进入责任团队处置流程，矩阵并行支持，不等待例会。'),notes='合并原接收、评审、采用三页。继承原三类评审结论（通过、有条件通过、不通过），不通过回到方案修订；有条件通过需满足对应条件。矩阵决策不替代既有服务变更和发布审批。成果按性质安排验证，规范类以试点使用验证，代码类按范围完成集成运行验证。',part=4,cover=False)
coord=dict(chapter='第4部分 / 4.3 冲突上升与日常运营',title='协调运营：冲突有决策路径，行动有跟踪闭环',lead='专题内先协调，超出权限或影响关键计划时上升；TPM维护统一记录，责任团队落实行动。',body=svg('按冲突类型上升与例会运营机制',
box(25,10,420,225,'功能与系统边界分歧',['FO / SO与VCC先明确需求','跨系统事项协同系统架构矩阵','仍无法一致，提交授权技术评审'])+
box(510,10,420,225,'软件与平台方案分歧',['平台及领域架构师评估影响','按职责协同独立软件架构矩阵','重大取舍提交技术决策CCB'],'dark')+
box(995,10,420,225,'资源与计划冲突',['TPM协调所属团队负责人','提出优先级与计划调整选项','由资源及业务负责人决策'],'teal')+
box(25,315,420,170,'会前：材料与分歧准备好',['登记问题、影响及备选方案','邀请有决策权及承接责任的人'])+
box(510,315,420,170,'会中：决策与行动说清楚',['聚焦方案、依赖及阻塞','明确结论、条件、责任与节点'])+
box(995,315,420,170,'会后：实施与采用跟到底',['回写决策，跟踪实施与验证','更新成果库，复盘采用和投入'])+
arrow(445,400,500,400)+arrow(930,400,985,400))+
note('沿用周或双周例会；安全与保护要求按既有责任机制处理，不以矩阵表决放宽。'),notes='以原矩阵例会、TPM运营、关键技术方案上升和跨矩阵协作为基础。分流路径及改进运营为建议机制；现行授权组织名称与责任人需确认。决策记录包含理由、适用条件、责任及后续验证。周期复盘以四项能力投入、采用进展和反复问题改善为依据，不新增强交付职责。',part=4,cover=False)
slides += [divider,org,workflow,coord]
assert len(slides)==19
assert len([s for s in slides if s.get('part')==4])==4
for s in slides:
 s['chapter']=s['chapter'].replace('V2.12','V2.13');s['body']=s['body'].replace('V2.12','V2.13')
before,tail=base.split('<main>',1);_,after=tail.split('</main>',1)
rendered=[]
for i,s in enumerate(slides,1):
 tag='h1' if s['cover'] else 'h2';cls='slide'+(' cover' if s['cover'] else '')+(' part-divider' if s.get('divider') else '')
 rendered.append(f'<section class="{cls}" id="s{i}" data-title="{E(s["title"].replace("<br>"," "),quote=True)}" data-chapter="{E(s["chapter"],quote=True)}" data-part="{s.get("part",0)}" aria-labelledby="t{i}"><div class="eyebrow"><span>{i:02}</span>{E(s["chapter"])}</div><{tag} id="t{i}">{s["title"]}</{tag}><p class="lead">{E(s["lead"])}</p><div class="body">{s["body"]}</div><aside class="notes">{E(s["notes"])}</aside></section>')
html=(before+'<main>'+''.join(rendered)+'</main>'+after).replace('V2.12','V2.13')
ROOT.joinpath('matrix_planning_v2_13.html').write_text(html)
ROOT.joinpath('matrix_planning_v2_13_content.json').write_text(json.dumps(slides,ensure_ascii=False,indent=2)+'\n')
ROOT.joinpath('matrix_v2_13_revision_notes.md').write_text('''# V2.13 汇报结构与版式调整

1. 保留主标题，封面副标题及概述改为车控Agent能力边界—四项平台能力—矩阵运营和成果闭环主线。
2. 第4页以统一背景框，将接入、组织协调仲裁、任务分解与运行管理三层纳入车控Agent主体；NOMI与系统执行层保留在外。
3. 第6页基础能力调用接口改为基础能力服务接口。
4. 第8页后增加第三部分分隔页，归纳定义与交互、运行与编排、共建与采用；原第三部分正文后移并修正目录锚点。
5. 第四部分压缩为第16—19页，共4页含分隔页：组织职责、议题与成果闭环、冲突上升及日常运营。原机制和职责边界保留；详细内容合并，非新增制度。

全稿19页。原版保留，独立发布matrix-v213。依据仍为原服务架构矩阵章程、工作流和已确认讨论；不改服务代码和IDL。
''')
print(json.dumps({'slides':len(slides),'bytes':len(html.encode()),'part4_pages':[16,17,18,19]}))
