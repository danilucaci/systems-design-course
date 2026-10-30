"""Check canonical lesson coverage, answer coverage, local links, diagrams, and listings."""
import json
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit
from xml.etree import ElementTree

ROOT=Path(__file__).resolve().parents[1]
SECTIONS=[
    'A. Learning objectives and prerequisites','B. Mental model and intuition',
    'C. Deep technical explanation','D. Architecture and data flow','E. Real-world examples',
    'F. Executable example','G. Architectural decisions and trade-offs','H. Common failures and debugging',
    'I. Practical exercise','J. Interview and senior-engineering assessment','Assessment solutions',
    'K. Key takeaways and navigation',
]


def without_fences(text): return re.sub(r'^```[^\n]*\n.*?^```\s*$', '', text, flags=re.M|re.S)
def word_count(text): return len(without_fences(text).split())


def check_links(path):
    count=0
    for _,destination in re.findall(r'\[([^\]]+)\]\(([^)]+)\)',without_fences(path.read_text())):
        target=urlsplit(destination)
        if target.scheme or target.netloc: continue
        resolved=(path.parent/unquote(target.path)).resolve() if target.path else path
        assert resolved.is_file(),f'{path.relative_to(ROOT)}: missing file {destination}'
        if target.fragment:
            contents=without_fences(resolved.read_text())
            explicit=set(re.findall(r'<a\s+id="([^"]+)"',contents))
            headings={re.sub(r'[^\w -]','',value.lower()).replace(' ','-') for value in re.findall(r'^#+ (.+)$',contents,re.M)}
            assert target.fragment in explicit|headings,f'{path.relative_to(ROOT)}: missing anchor {destination}'
        count+=1
    return count


def validate():
    manifest=json.loads((ROOT/'course-manifest.json').read_text())
    assert len(manifest['lessons'])==manifest['expected_lesson_count']==98
    assert len({x['id'] for x in manifest['lessons']})==98
    assets=json.loads((ROOT/'course-ui/diagrams/manifest.json').read_text())
    sources={asset['source']:asset for asset in assets}
    assert len(sources)==len(assets),'duplicate diagram registrations'
    results=[]
    for lesson in manifest['lessons']:
        if lesson['status']!='complete':
            assert not (ROOT/lesson['path']).exists(),f'{lesson["id"]}: planned record has an unexpected lesson file'
            continue
        path=ROOT/lesson['path']; text=path.read_text(); prose=without_fences(text)
        assert re.findall(r'^## (.+)$',prose,re.M)==SECTIONS,f'{lesson["id"]}: section contract'
        questions=prose.split('## J. Interview and senior-engineering assessment\n',1)[1].split('## Assessment solutions',1)[0]
        answers=prose.split('## Assessment solutions\n',1)[1].split('## K.',1)[0]
        qids=re.findall(r'^(\d+)\. ',questions,re.M); aids=re.findall(r'^### (\d+)\. ',answers,re.M)
        assert qids==aids==[str(i) for i in range(1,len(qids)+1)] and 5<=len(qids)<=10,f'{lesson["id"]}: question/answer coverage'
        words=word_count(text)
        assert lesson['word_count']==words,f'{lesson["id"]}: stale manifest word count'
        warnings=[]
        if lesson['module_id']=='module-1' and not 2000<=words<=3500:
            warnings.append(f'{words} prose words: review depth manually against the core-concept target')
        links=check_links(path)+check_links(ROOT/lesson['exercise_solution_path'])
        diagrams=re.findall(r'```mermaid\n([\s\S]*?)\n```',text)
        for diagram in diagrams:
            asset=sources.get(diagram.strip()); assert asset,f'{lesson["id"]}: missing SVG equivalent'
            ElementTree.parse(ROOT/asset['path'])
        blocks=re.findall(r'```(?:python|sql)\n([\s\S]*?)\n```',text)
        for filename in lesson.get('code_listing_paths',[]):
            assert (ROOT/filename).read_text().strip() in [block.strip() for block in blocks],f'{lesson["id"]}: listing drift for {filename}'
        for filename in lesson['executable_paths']: assert (ROOT/filename).is_file(),f'missing executable {filename}'
        results.append({'id':lesson['id'],'prose_words':words,'questions':len(qids),'answers':len(aids),'diagrams':len(diagrams),'local_links':links,'warnings':warnings})
    assert manifest['verified_canonical_lesson_count']==len(results),'stale written lesson count'
    assert manifest['total_lesson_word_count']==sum(result['prose_words'] for result in results),'stale total word count'
    for export in manifest['exports'].values():
        assert export['lesson_count']==len(results),'stale export lesson count'
    assert manifest['exports']['html']['embedded_diagrams']==sum(result['diagrams'] for result in results),'stale diagram count'
    return results


if __name__=='__main__':
    results=validate()
    print(json.dumps({'written':len(results),'planned':98-len(results),'lessons':results},indent=2))
