"""Add executive-level scene interface guidance and the grounded AiCabin example."""
from pathlib import Path
from html import escape as E
import json

ROOT=Path(__file__).parent
slides=json.loads((ROOT/'matrix_planning_v2_7_content.json').read_text())
base=(ROOT/'matrix_planning_v2_7.html').read_text()
def text(x,y,t,size=23,color='#173642'):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}">{E(t)}</text>'
def box(x,y,w,h,title,lines=(),dark=False):
    fill,ink=('#173642','#fff') if dark else ('#e5eee3','#173642')
    s=f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{fill}" stroke="#9fbead"/>'
    s+=f'<text x="{x+22}" y="{y+36}" font-size="26" fill="{ink}" font-weight="650">{E(title)}</text>'
    for i,t in enumerate(lines):s+=text(x+22,y+75+34*i,t,22,ink)
    return '<g class="diagram-node">'+s+'</g>'
def arrow(x1,y1,x2,y2):
    return f'<path d="M{x1},{y1}L{x2},{y2}" fill="none" stroke="#17847a" stroke-width="2.5" marker-end="url(#sceneArrow)"/>'
def svg(label,s,n):
    return f'<svg class="diagram" viewBox="0 0 1440 500" role="img" aria-label="{E(label)}"><defs><marker id="sceneArrow{n}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0L10,5L0,10Z" fill="#17847a"/></marker></defs>'+s.replace('#sceneArrow)',f'#sceneArrow{n})')+'</svg>'
def note(t):return '<div class="takeaway">'+t+'</div>'

definition=dict(chapter='第2部分 / 2.1 服务升级与封装',part=2,cover=False,
 title='场景接口：统一功能、交互、行为与验收说明',
 lead='接口不仅提供启动入口，还应说明何时能用、怎样运行、怎样退出，以及如何判断结果。',
 body=svg('场景服务接口与使用说明的四项共同内容',
   box(25,15,650,175,'场景能力说明',['解决什么需求，作用于哪些对象','明确功能范围、可配置内容与适用条件'],True)+
   box(765,15,650,175,'交互接口定义',['请求进入、必要的修改与取消','明确响应、状态、结果和可选推荐'])+
   box(25,300,650,175,'运行行为规则',['触发、进入、保持与退出条件','明确冲突、人工介入及退出后处理'])+
   box(765,300,650,175,'典型使用与验收用例',['正常执行、条件不满足和异常','明确预期行为、反馈及判断依据']),1)+
   note('矩阵提供共用模板与评审方法；业务和系统团队定义具体策略。先补齐说明，再按实际缺口改造IDL。'),
 notes='本页是共用设计范式，不要求四项内容全部编码进IDL，也不要求每种交互新增独立RPC。场景说明需补充车型、配置、版本、必要的时序与兼容要求。结果须区分接受、执行、效果达成；持续场景达到效果后可能仍需维持。')

example=dict(chapter='第2部分 / 2.1 服务升级与封装',part=2,cover=False,
 title='AiCabin示例：明确场景条件与使用责任',
 lead='以已有阳光直射温控为基础，补充进入、运行、退出和反馈的使用说明。',
 body=svg('NOMI、场景执行方和系统产品的责任，以及完整使用过程',
   box(25,10,420,145,'NOMI等入口',['理解需求、确定作用对象','必要时澄清或向用户确认'])+
   box(510,10,420,145,'车控Agent / 场景执行方',['统一判断是否接受场景','管理运行、调整和退出'],True)+
   box(995,10,420,145,'相关系统产品',['检查本域是否允许执行','负责控制、保护与反馈'])+
   text(25,225,'建议明确的场景使用过程',25,'#17847a')+
   ''.join(box(x,285,250,145,t,ls) for x,t,ls in [
      (25,'触发需求',['用户请求','或业务场景识别']),
      (310,'进入检查',['条件、权限','及其他任务冲突']),
      (595,'运行与调整',['状态变化','及用户手动操作']),
      (880,'退出与处理',['取消、完成或异常','明确设置与控制权']),
      (1165,'结果反馈',['实际完成范围','以及原因'])])+
   ''.join(arrow(x,355,x+25,355) for x in [280,565,850,1135]),2)+
   note('现有AiCabin已提供场景请求与取消表达、推荐和状态接口；完整行为规则需结合功能设计与实现确认。'),
 notes='依据本地srv.thermal.hvac.aicabinfuncmgr.proto：ThmSceneMode支持scene_id=8阳光直射温控，on_off_req=1进入、2取消，seat_position指定位置。推荐为EVENT，状态为只读FIELD。现有result的取值含义未在该文件说明，状态不回传request_id，偏好适用规则、精确取消和完成依据不能直接推定。上方是建议责任划分，AiCabin与VCC的具体软件归属需核实。触发不等于允许执行；保持条件需区别启动检查；退出不等于反向动作或全部恢复。权限由可信机制校验，系统保护不因上层检查而取消。')

# Insert directly after the existing system/scene capability architecture page.
slides[7:7]=[definition,example]
for s in slides:
    if s['cover']:
        s['chapter']=s['chapter'].replace('V2.7','V2.8')
        s['body']=s['body'].replace('V2.7','V2.8')
    if s.get('divider') and s.get('part')==2:
        s['body']=s['body'].replace('2.1 服务升级与封装：形成系统能力与场景接口','2.1 服务升级与封装：完善能力、场景接口与使用规范')

before,tail=base.split('<main>',1);_,after=tail.split('</main>',1)
rendered=[]
for i,s in enumerate(slides,1):
    tag='h1' if s['cover'] else 'h2'
    cls='slide'+(' cover' if s['cover'] else '')+(' part-divider' if s.get('divider') else '')
    rendered.append(f'<section class="{cls}" id="s{i}" data-title="{E(s["title"].replace("<br>"," "),quote=True)}" data-chapter="{E(s["chapter"],quote=True)}" data-part="{s.get("part",0)}" aria-labelledby="t{i}"><div class="eyebrow"><span>{i:02}</span>{E(s["chapter"])}</div><{tag} id="t{i}">{s["title"]}</{tag}><p class="lead">{E(s["lead"])}</p><div class="body">{s["body"]}</div><aside class="notes">{E(s["notes"])}</aside></section>')
html=(before+'<main>'+''.join(rendered)+'</main>'+after).replace('V2.7','V2.8')
assert len(slides)==25
ROOT.joinpath('matrix_planning_v2_8.html').write_text(html)
ROOT.joinpath('matrix_planning_v2_8_content.json').write_text(json.dumps(slides,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'slides':len(slides),'added_pages':[8,9],'parts':5,'bytes':len(html.encode())}))
