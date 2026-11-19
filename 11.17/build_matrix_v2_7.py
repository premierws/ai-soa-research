"""Add explicit report parts and transition slides without changing the argument."""
from pathlib import Path
from html import escape
import json

ROOT=Path(__file__).parent
old=json.loads((ROOT/'matrix_planning_v2_6_content.json').read_text())
base=(ROOT/'matrix_planning_v2_6.html').read_text()
parts=[
    dict(name='业务目标与建设主线',start=2,end=4,
         question='车控智能化要实现什么，需要从哪些方向建设能力？',
         topics=['已有系统服务与场景协同的关系','VCC规划中的三个实际业务场景','四个建设方向与矩阵支撑的总体对应']),
    dict(name='矩阵平台能力提升',start=5,end=11,
         question='为了支撑场景能力，服务架构矩阵需要推动哪些平台提升？',
         topics=['2.1 服务升级与封装：形成系统能力与场景接口','2.2 高效可靠协同：完善运行方法与底座支撑','2.3 自适应交互：评估SOA框架和通信机制的演进','2.4 动态组合：明确能力边界与组合规则']),
    dict(name='实际业务案例',start=12,end=14,
         question='这些平台提升，怎样支持已有VCC业务规划？',
         topics=['近车解锁开门：跨系统场景协同','主驾自适应模式：结合用户差异协调执行','阳光直射场景：感知环境并响应热舒适需求']),
    dict(name='组织形式与协作方式',start=15,end=16,
         question='矩阵如何组织共性建设，业务和工程团队如何共同参与？',
         topics=['以SOA为核心的虚拟能力中心及职责边界','从业务需求到平台改进、实施采用和验证','专业角色、专题协作与成果维护']),
    dict(name='首批试点与推进建议',start=17,end=18,
         question='从哪些业务启动，形成什么成果，怎样逐步推广？',
         topics=['首批场景、建设成果、共建与采用团队','服务完善、协同验证和自适应支撑的推进重点','需要确认的责任团队、投入和推广安排']),
]
labels={2:'1.1 业务目标',3:'1.2 实际业务',4:'1.3 建设主线',
        5:'2.1 服务升级与封装',6:'2.1 服务升级与封装',
        7:'2.2 高效可靠协同',8:'2.2 高效可靠协同',
        9:'2.3 自适应交互支撑',10:'2.3 自适应交互支撑',11:'2.4 边界内动态组合',
        12:'3.1 近车解锁开门',13:'3.2 主驾自适应模式',14:'3.3 阳光直射场景',
        15:'4.1 组织定位',16:'4.2 协作方式',17:'5.1 首批建设',18:'5.2 推进建议'}
slides=[old[0].copy()]
slides[0]['chapter']='提升规划 · V2.7'
slides[0]['body']=slides[0]['body'].replace('V2.6','V2.7')
for i,p in enumerate(parts,1):
    roadmap='<div class="part-roadmap">'+''.join(f'<div class="{"current" if j==i else ""}"><span>{j:02}</span><b>{escape(q["name"])}</b></div>' for j,q in enumerate(parts,1))+'</div>'
    body='<div class="part-intro"><div class="part-number">'+f'{i:02}'+'</div><div class="part-topics"><h3>接下来说明</h3><ol>'+''.join('<li>'+escape(t)+'</li>' for t in p['topics'])+'</ol></div></div>'+roadmap
    slides.append(dict(chapter=f'第{i}部分 / 内容导览',title=f'{i:02}　{p["name"]}',lead=p['question'],body=body,notes='本页为章节分隔，说明接下来内容的范围和目的。',cover=False,divider=True,part=i))
    for n in range(p['start'],p['end']+1):
        s=old[n-1].copy();s['chapter']=f'第{i}部分 / '+labels[n];s['part']=i
        slides.append(s)

before,tail=base.split('<main>',1);_,after=tail.split('</main>',1)
css='''
.part-divider{background:#e8ede4}.part-divider h2{font-size:clamp(35px,3.5vw,68px)}.part-divider .lead{font-size:clamp(17px,1.55vw,30px);color:var(--ink);max-width:92%}.part-divider .body{justify-content:space-evenly;gap:4vh}.part-intro{display:grid;grid-template-columns:22% 1fr;gap:4vw;align-items:center}.part-number{font-family:Georgia,serif;font-size:clamp(100px,12vw,230px);line-height:1;color:#17847a;letter-spacing:-.07em;border-right:1px solid #adc4b5}.part-topics h3{color:var(--teal);font-size:clamp(14px,1.1vw,22px);margin-bottom:2vh}.part-topics ol{list-style:none;padding:0;margin:0;display:flex;flex-direction:column;gap:1.7vh}.part-topics li{font-size:clamp(17px,1.55vw,30px);line-height:1.65}.part-topics li:before{content:'—';color:var(--teal);margin-right:.7em}.part-roadmap{display:grid;grid-template-columns:repeat(5,1fr);gap:1.1vw}.part-roadmap>div{border-top:3px solid #b9c9bd;padding:1.7vh .8vw;color:#61766c;display:flex;flex-direction:column;gap:.8vh}.part-roadmap>div.current{border-top-color:var(--teal);background:#173642;color:white}.part-roadmap span{font-size:clamp(11px,.9vw,18px);color:#17847a}.part-roadmap .current span{color:#dbe8a9}.part-roadmap b{font-size:clamp(12px,1.08vw,21px);font-weight:500;line-height:1.5}
@media(max-width:800px){.part-intro{grid-template-columns:1fr;gap:25px}.part-number{font-size:90px;border:0}.part-divider .body{gap:35px}.part-roadmap{grid-template-columns:1fr 1fr}.part-topics li{font-size:17px}.part-divider h2{font-size:32px}}
@media print{.part-divider h2{font-size:31pt}.part-divider .lead{font-size:15pt}.part-topics li{font-size:14pt}.part-topics h3{font-size:11pt}.part-number{font-size:95pt}.part-roadmap b{font-size:10pt}.part-roadmap span{font-size:8pt}}
'''
rendered=[]
for i,s in enumerate(slides,1):
    tag='h1' if s['cover'] else 'h2'
    cls='slide'+(' cover' if s['cover'] else '')+(' part-divider' if s.get('divider') else '')
    rendered.append(f'<section class="{cls}" id="s{i}" data-title="{escape(s["title"].replace("<br>"," "),quote=True)}" data-chapter="{escape(s["chapter"],quote=True)}" data-part="{s.get("part",0)}" aria-labelledby="t{i}"><div class="eyebrow"><span>{i:02}</span>{escape(s["chapter"])}</div><{tag} id="t{i}">{s["title"]}</{tag}><p class="lead">{escape(s["lead"])}</p><div class="body">{s["body"]}</div><aside class="notes">{escape(s["notes"])}</aside></section>')
html=(before+'<main>'+''.join(rendered)+'</main>'+after).replace('V2.6','V2.7').replace('</style>',css+'</style>')
assert len(slides)==23
ROOT.joinpath('matrix_planning_v2_7.html').write_text(html)
ROOT.joinpath('matrix_planning_v2_7_content.json').write_text(json.dumps(slides,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'slides':len(slides),'parts':len(parts),'divider_pages':[i for i,s in enumerate(slides,1) if s.get('divider')],'bytes':len(html.encode())}))
