"""Revise only the opening architecture and boundary pages for user review."""
from pathlib import Path
from html import escape as E
import json

ROOT=Path(__file__).parent
old=json.loads((ROOT/'matrix_planning_v2_9_content.json').read_text())
base=(ROOT/'matrix_planning_v2_9.html').read_text()
serial=400
LAYERS=['用户意图识别层','车控Agent接入层','Agent组织协调仲裁层','任务分解与运行管理层','系统执行层']
def text(x,y,t,size=22,color='#173642',weight=400):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" font-weight="{weight}">{E(t)}</text>'
def box(x,y,w,h,title,lines=(),kind='normal'):
    fill,stroke,ink={'normal':('#edf1ed','#b9c8c2','#173642'),'dark':('#173642','#173642','#fff'),'teal':('#dfeee7','#17847a','#173642'),'orange':('#f7e7db','#c76b43','#593c2e')}[kind]
    s=f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>'
    s+=text(x+22,y+35,title,25,ink,650)
    for i,t in enumerate(lines):s+=text(x+22,y+72+32*i,t,22,ink)
    return '<g class="diagram-node">'+s+'</g>'
def arrow(x1,y1,x2,y2,dashed=False):
    return f'<path d="M{x1},{y1} L{x2},{y2}" stroke="#17847a" stroke-width="2.7" fill="none" {"stroke-dasharray="+chr(34)+"7 5"+chr(34) if dashed else ""} marker-end="url(#ARR)"/>'
def route(d,dashed=False):
    return f'<path d="{d}" stroke="#17847a" stroke-width="2.7" fill="none" {"stroke-dasharray="+chr(34)+"7 5"+chr(34) if dashed else ""} marker-end="url(#ARR)"/>'
def svg(label,s,h=500):
    global serial
    serial+=1
    return f'<svg class="diagram" viewBox="0 0 1440 {h}" role="img" aria-label="{E(label)}"><defs><marker id="arr{serial}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0L10,5L0,10Z" fill="#17847a"/></marker></defs>'+s.replace('#ARR',f'#arr{serial}')+'</svg>'
def note(t):return '<div class="takeaway">'+t+'</div>'
def mini(active):
    s=''
    for i,title in enumerate(LAYERS):
        y=10+100*i;fill='#173642' if i in active else '#e6ece3';ink='#fff' if i in active else '#61766c'
        s+='<g class="diagram-node">'+f'<rect x="25" y="{y}" width="355" height="65" rx="10" fill="{fill}" stroke="#bacbbf"/>'+text(43,y+40,title,22,ink,650)+'</g>'
        if i<4:s+=arrow(175,y+65,175,y+90)+arrow(225,y+90,225,y+65)
    return s
def page(index,title,lead,body,notes,chapter):
    s=old[index-1].copy();s.update(title=title,lead=lead,body=body,notes=notes,chapter=chapter);return s

rows=[
 ['NOMI：理解需求，澄清对象与偏好','向下提出场景或明确控制请求，向用户解释结果'],
 ['场景能力服务：近车迎宾、主驾自适应、阳光直射温控','基础能力接口：明确功能请求的接入与反馈'],
 ['判断场景可行性，处理任务冲突、资源和优先关系','选择已有场景或形成允许范围内的执行方案'],
 ['任务分解、执行跟踪、中断退出与结果汇总','运行管理包含异常、故障和条件变化处理'],
 ['门锁、座椅、方向盘、后视镜、空调、出风口等服务','本域校验、控制与保护；反馈状态、限制和结果']
]
s=''
for i,(title,details) in enumerate(zip(LAYERS,rows)):
    y=5+i*125;fill='#173642' if i in [2,3] else '#e3ede1';ink='#fff' if i in [2,3] else '#173642'
    s+='<g class="diagram-node">'+f'<rect x="260" y="{y}" width="1030" height="105" rx="10" fill="{fill}" stroke="#a6bdad"/>'
    s+=text(280,y+58,title,25,ink,650)
    s+=text(650,y+40,details[0],21,ink)+text(650,y+77,details[1],21,'#dce7a9' if i==3 else ink)+'</g>'
    if i<4:s+=arrow(750,y+105,750,y+115)
s+=box(10,133,205,145,'明确控制输入',['硬开关经适配','GUI等入口'],kind='normal')
s+=arrow(215,180,250,180)
s+=route('M260,210 H240 V557 H250',True)+text(10,345,'基础能力调用',21,'#17847a')+text(10,377,'按必要路径执行',21,'#17847a')
s+=arrow(1340,605,1340,15)+text(1360,290,'执行',22,'#17847a')+text(1360,325,'反馈',22,'#17847a')
s+=text(520,640,'向下控制分发；向上执行反馈',23,'#17847a')
architecture=page(5,'车控Agent功能架构：承接需求，组织场景执行',
 '以场景能力服务为主要入口，向下分发控制任务，向上汇总状态与执行结果。',
 svg('NOMI与车控Agent的五层功能架构',s,h=650)+
 note('明确控制输入可调用基础能力接口，按必要路径仲裁和执行；任务运行管理包含异常与故障处理。'),
 '五层为功能职责，不规定软件进程与部署。基础能力虚线表示明确控制不必触发完整场景规划，但仍需必要权限、仲裁和系统校验。硬开关经既有适配形成明确请求，不表示所有实时硬件链路改经Agent。系统保护不等待Agent批准。场景和系统例子取自已有VCC规划。',
 '第1部分 / 1.2 五层功能架构')

external=page(7,'对外接口：场景能力为主，兼容明确的基础控制',
 '用户意图识别层通过服务接口接入；明确控制输入也可直接调用基础能力。',
 svg('接入层的场景服务和基础能力两类接口',mini({0,1})+
   text(480,45,'车控Agent接入层提供两类服务接口',25,'#17847a')+
   box(480,95,440,290,'场景能力服务接口',['请求场景、对象及必要参数','按业务需要修改或取消','配套定义进入条件与执行约束','执行过程、退出与异常处理','提供状态和结果反馈'],'dark')+
   box(985,95,430,290,'基础能力调用接口',['硬开关经适配、GUI、明确指令','门窗、座椅等基础功能调用','按必要路径仲裁、执行并反馈','不自动扩展为其他场景'],'teal')+
   box(480,420,935,65,'共同接入：请求来源、权限、参数检查，以及状态和执行结果反馈'))+
 note('条件与规则写入接口定义及使用说明，不要求每次请求传入整套规则；执行侧仍进行相应校验。'),
 '接口形态为服务调用及必要的状态/结果反馈；具体METHOD、EVENT、FIELD组合按业务设计。可参考AiCabin已有场景请求、取消表达、推荐和状态接口，但不推定现有状态语义与请求关联已经完整。NOMI提供需求与确认，不作为车辆可执行性的唯一检查者。',
 '第2部分 / 2.1 对外接口')

internal=page(8,'内部协同：协调层定方案，任务层管理，系统层执行',
 '场景请求逐层落实为系统任务，系统状态与限制逐层支撑判断和结果汇总。',
 svg('五层架构中的协调任务和系统执行职责',mini({2,3,4})+
   box(480,5,860,125,'组织协调仲裁：判断整体可行性，确定执行方案',['结合车辆状态、进入条件与约束','处理场景冲突、共享资源和优先关系'],'dark')+
   box(480,185,860,125,'任务分解与运行管理：组织执行，处理异常',['分解系统任务，跟踪进度和实际结果','管理中断退出；异常时按需请求协调层调整方案'],'dark')+
   box(480,365,860,125,'系统执行：完成本域控制，反馈状态与结果',['校验本域条件，承担控制、实时保护和故障处理','向上报告可用性、执行限制、保护变化与结果'],'teal')+
   arrow(850,130,850,175)+text(490,163,'场景执行方案',20,'#17847a')+
   arrow(850,310,850,355)+text(490,343,'系统任务与控制请求',20,'#17847a')+
   arrow(1360,440,1360,45)+text(1385,245,'执行',22,'#17847a')+text(1385,277,'反馈',22,'#17847a'))+
 note('整体场景判断通过不替代系统校验；基础控制路径可以简化，但不绕过必要仲裁和本域保护。'),
 '协调层处理跨系统整体方案，任务层处理执行组织、状态与异常流转；任务层可依据反馈请求协调层重新决策。系统内部时序和实时保护留在系统产品。不是所有响应都要依次等待五层处理。',
 '第2部分 / 2.2 内部职责与交互')

abnormal=page(9,'运行管理：依据系统反馈，调整、中断或退出场景',
 '异常与故障处理位于任务运行管理层，并与协调层决策、系统本域保护配合。',
 svg('沿五层架构处理拒绝执行中断和结果反馈',mini({3})+
   box(480,5,860,125,'进入前：条件不满足，不进入并反馈原因',['协调层综合判断场景可行性','经接入层返回，由NOMI等入口完成必要提示'])+
   box(480,185,860,125,'运行中：故障、保护或条件变化',['任务层识别影响，协调层按需调整整体方案','系统执行本域保护；按业务规则部分中断或整体退出'],'dark')+
   box(480,365,860,125,'结束后：确认实际结果，再向上反馈',['任务层核对系统是否停止及剩余功能、控制权','经接入层反馈，NOMI等入口解释原因和实际完成范围'],'teal')+
   arrow(1360,435,1360,45)+text(1385,245,'结果',22,'#17847a')+text(1385,277,'反馈',22,'#17847a'))+
 note('系统实时保护不等待Agent批准；退出请求不等于已经停止，条件恢复后是否恢复场景需重新判断。'),
 '三种情况是按五层职责展开的场景行为说明，不是发生任何异常都退出。按影响和业务规则处置；信息不足不伪造可执行或完成。条件、策略与时限由业务和系统确认。',
 '第2部分 / 2.3 运行反馈与异常处理')

replacements={5:architecture,7:external,8:internal,9:abnormal}
slides=[]
for n,source in enumerate(old,1):
    if n==4:continue
    s=replacements.get(n,source.copy())
    if n==1:
        s['chapter']=s['chapter'].replace('V2.9','V2.10');s['body']=s['body'].replace('V2.9','V2.10').replace('2026.11.17','2026.11.18')
    if n==2:
        s['lead']='车控Agent怎样承接上层需求，并组织系统完成场景执行？'
        s['body']=s['body'].replace('系统服务基础与用户体验目标','已有系统服务与场景协同目标').replace('已有VCC业务场景','NOMI、车控Agent与系统执行的五层架构').replace('车控Agent从状态理解到结果跟踪的业务过程','场景能力与基础能力两类请求，以及控制与反馈')
    if n==6:
        s['lead']='围绕五层功能架构，说明对外接口、内部执行分工和异常反馈。'
        s['body']=s['body'].replace('NOMI、车控Agent与系统执行层的职责边界','用户意图识别层与接入层：两类服务接口').replace('进入前、执行中和退出后的持续交互','协调层、任务层与系统层：控制分发与执行反馈').replace('条件不满足、故障与风险下的场景处置','任务运行管理：不进入、中断退出与结果提示')
    slides.append(s)

# Scope invariant: all source content from chapter three onward is untouched.
assert slides[8:]==old[9:]
assert len(slides)==26
before,tail=base.split('<main>',1);_,after=tail.split('</main>',1)
rendered=[]
for i,s in enumerate(slides,1):
    tag='h1' if s['cover'] else 'h2';cls='slide'+(' cover' if s['cover'] else '')+(' part-divider' if s.get('divider') else '')
    rendered.append(f'<section class="{cls}" id="s{i}" data-title="{E(s["title"].replace("<br>"," "),quote=True)}" data-chapter="{E(s["chapter"],quote=True)}" data-part="{s.get("part",0)}" aria-labelledby="t{i}"><div class="eyebrow"><span>{i:02}</span>{E(s["chapter"])}</div><{tag} id="t{i}">{s["title"]}</{tag}><p class="lead">{E(s["lead"])}</p><div class="body">{s["body"]}</div><aside class="notes">{E(s["notes"])}</aside></section>')
html=(before+'<main>'+''.join(rendered)+'</main>'+after).replace('V2.9','V2.10')
# Only the presentation header date changes; chapter-three body content stays intact.
html=html.replace('V2.10 · 2026.11.17','V2.10 · 2026.11.18')
ROOT.joinpath('matrix_planning_v2_10.html').write_text(html)
ROOT.joinpath('matrix_planning_v2_10_content.json').write_text(json.dumps(slides,ensure_ascii=False,indent=2)+'\n')
ROOT.joinpath('matrix_v2_10_revision_notes.md').write_text('''# V2.10 修改范围

按用户已review的方案：删除V2.9原第4页，不再将三个传统可实现功能用作智能化独有价值论证；原第5页改为五层架构，现第4页。原第7—9页改为对外接口、内部职责和异常反馈，现第6—8页。

第一、二部分分隔导览同步。第三章及之后的内容字典与V2.9逐项相等，只有显示页号及目录位置自动前移。总页数26，保留5部分结构。

五层：用户意图识别、车控Agent接入、Agent组织协调仲裁、任务分解与运行管理、系统执行。场景接口为主，基础接口服务明确控制；向下分发、向上反馈；异常处理在任务运行层，系统保护独立保留。接口说明的条件规则不要求每次请求携带整套规则。

独立发布matrix-v210，不修改V2.9或第三章正文。验证五层文字、三种桌面尺寸、图中文字边界/碰撞、目录和翻页、26页打印及线上页面指纹。
''')
print(json.dumps({'slides':len(slides),'changed_pages':[4,6,7,8],'third_chapter_onward_unchanged':True,'bytes':len(html.encode())}))
