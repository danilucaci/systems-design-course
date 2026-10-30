"""Render the nine authored Module 1 diagrams as offline SVG equivalents.

Geometry is deliberately authored per figure; this is not a general Mermaid renderer.
Labels and source identity come from canonical Markdown to prevent text drift.
"""
import html
import json
import re
import textwrap
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'course-ui/diagrams'
W,H=220,88


def snake(names):
    coordinates=[(20,20),(310,20),(600,20),(600,220),(310,220)]
    return dict(zip(names,coordinates))


LAYOUTS={
    '01': (320, {'Browser':(20,190),'DNS':(20,20),'Edge':(310,190),'API':(600,190),'DB':(600,20)},'API',{}),
    '02': (340,snake(['Client','Auth','Transaction','Journey','Commit']),'Transaction',{}),
    '03': (360,{'User':(20,135),'Journey':(310,20),'Stop':(600,20),'Request':(310,245)},'Journey',{}),
    '04': (360,{'Reader':(20,50),'Cache':(310,50),'Origin':(600,50),'Writer':(310,245)},'Cache',{
        ('Cache','Origin'):((530,75),(600,75),(565,25)),
        ('Origin','Cache'):((600,115),(530,115),(565,165)),
        ('Writer','Origin'):((530,289),(710,138),(710,210)),
    }),
    '05': (340,snake(['Owner','Freeze','Copy','Cutover','Fence']),'Copy',{}),
    '06': (340,snake(['Key','Hash','Ring','Owner','Transfer']),'Ring',{}),
    '07': (360,{'Partition':(20,135),'Write':(310,135),'Strong':(600,20),'Local':(600,245),'Heal':(310,245)},'Write',{}),
    '08': (340,snake(['Query','Planner','Scan','Heap','Result']),'Scan',{}),
    '09': (340,{'Intent':(20,20),'Attempts':(310,20),'Concurrency':(600,20),'Capacity':(600,220),'Writes':(20,220),'Storage':(310,220)},'Attempts',{}),
}


def endpoints(a,b):
    ax,ay=a; bx,by=b
    if abs(bx-ax)>abs(by-ay):
        return ((ax+W,ay+H/2),(bx,by+H/2)) if bx>ax else ((ax,ay+H/2),(bx+W,by+H/2))
    return ((ax+W/2,ay+H),(bx+W/2,by)) if by>ay else ((ax+W/2,ay),(bx+W/2,by+H))


def render(source,title,prefix,layout):
    height,positions,primary,overrides=layout
    labels=dict(re.findall(r'(\w+)\[([^\]]+)\]',source))
    edges=[]
    for line in source.splitlines()[1:]:
        match=re.fullmatch(r'\s*(\w+)(?:\[[^\]]+\])?\s*-->(?:\|([^|]+)\|)?\s*(\w+)(?:\[[^\]]+\])?\s*',line)
        if not match: raise ValueError(f'Unsupported authored edge: {line}')
        start,label,end=match.groups(); edges.append((start,end,label))
    if set(labels)!=set(positions): raise ValueError(f'Layout does not match source: {title}')
    escape=html.escape
    description=' '.join(f'{labels[a]} leads to {labels[b]}'+(f' ({label})' if label else '')+'.' for a,b,label in edges)
    svg=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 840 {height}" role="img" aria-labelledby="{prefix}-title {prefix}-desc">',
         f'<title id="{prefix}-title">{escape(title)}</title><desc id="{prefix}-desc">{escape(description)}</desc>',
         f'<defs><marker id="{prefix}-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path class="arrow-head" d="M0 0 10 5 0 10z"/></marker></defs>']
    for a,b,label in edges:
        start,end=endpoints(positions[a],positions[b]); label_at=None
        if (a,b) in overrides: start,end,label_at=overrides[(a,b)]
        x1,y1=start; x2,y2=end
        svg.append(f'<path class="edge" d="M{x1} {y1}L{x2} {y2}" marker-end="url(#{prefix}-arrow)"/>')
        if label:
            x,y=label_at or ((x1+x2)/2,(y1+y2)/2-12)
            # A quiet backing keeps edge labels readable where a diagonal passes beneath.
            svg.append(f'<text class="edge-label" x="{x}" y="{y}" text-anchor="middle" style="font-size:17px;paint-order:stroke;stroke:var(--paper);stroke-width:6px;stroke-linejoin:round">{escape(label)}</text>')
    for name,(x,y) in positions.items():
        kind='node-primary' if name==primary else 'node'
        svg.append(f'<rect class="{kind}" x="{x}" y="{y}" width="{W}" height="{H}" rx="7"/>')
        lines=textwrap.wrap(labels[name],width=19,break_long_words=False)
        if len(lines)>3: raise ValueError(f'Too many label lines: {labels[name]}')
        initial=y+H/2-(len(lines)-1)*12+7
        for number,line in enumerate(lines):
            svg.append(f'<text class="{kind}-label" x="{x+W/2}" y="{initial+number*24}" text-anchor="middle" style="font-size:20px">{escape(line)}</text>')
    return '\n'.join(svg+['</svg>'])+'\n'


if __name__=='__main__':
    manifest_path=OUT/'manifest.json'
    manifest=[entry for entry in json.loads(manifest_path.read_text()) if not Path(entry['path']).name.startswith('module1-')]
    for lesson in sorted((ROOT/'lessons/module-01').glob('*.md')):
        source=re.search(r'```mermaid\n([\s\S]*?)\n```',lesson.read_text()).group(1).strip()
        number=lesson.name[:2]; title=lesson.read_text().splitlines()[0][2:]
        filename=f'module1-{number}.svg'
        (OUT/filename).write_text(render(source,title,f'm1-{number}',LAYOUTS[number]))
        manifest.append({'title':f'1.{number} · {title}','path':f'course-ui/diagrams/{filename}','source':source})
    manifest_path.write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n')
    print('Rendered 9 authored Module 1 SVGs; retained existing diagrams.')
