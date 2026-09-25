"""Check packaged examples, references and split integrity without a model or network."""
import importlib.util
import hashlib
import json
from pathlib import Path
import re
import sys

ROOT=Path(__file__).resolve().parents[1]


def check(root=ROOT):
    root=Path(root).resolve(); errors=[]
    required=['README.md','README.zh-CN.md','CONTRIBUTING.md','SECURITY.md','CHANGELOG.md',
              'skills/creator-decision/SKILL.md','docs/validation.md','docs/task-progress.json']
    for name in required:
        if not (root/name).is_file(): errors.append('Missing: '+name)
    spec=importlib.util.spec_from_file_location('decision_release',root/'skills/creator-decision/scripts/decision.py')
    decision=importlib.util.module_from_spec(spec); spec.loader.exec_module(decision)
    examples=sorted((root/'examples').glob('*/*.json'))
    if len(examples)!=12: errors.append('Expected 12 authored report examples')
    for p in examples:
        try:
            data=decision.read(p); decision.validate(data)
            if p.with_suffix('.md').read_text(encoding='utf-8')!=decision.render(data):
                errors.append('Example rendering out of date: '+str(p.relative_to(root)))
            if not all(s['synthetic'] for s in data['sources']): errors.append('Unlabeled fictional example source')
        except (ValueError,OSError) as exc: errors.append(str(exc))
    groups=set()
    for split,count in [('development',12),('pilot',12),('test-candidates',24)]:
        try:
            data=json.loads((root/f'evaluations/cases/{split}.json').read_text(encoding='utf-8'))
            ids={c['project_group'] for c in data['cases']}
            if len(ids)!=count or len(data['cases'])!=count: errors.append('Wrong size/duplicate project: '+split)
            if ids & groups: errors.append('Project split overlap: '+split)
            groups |= ids
            if not all(c.get('synthetic') is True for c in data['cases']): errors.append('Case provenance missing: '+split)
        except (ValueError,OSError,KeyError) as exc: errors.append(str(exc))
    for p in root.rglob('*.md'):
        if any(x in {'.git','dist','private-work','private-evaluations'} for x in p.relative_to(root).parts): continue
        text=p.read_text(encoding='utf-8')
        for target in re.findall(r'\]\(([^)]+)\)',text):
            if re.match(r'[a-zA-Z][a-zA-Z0-9+.-]*:',target) or target.startswith('#'): continue
            target=target.split('#',1)[0].strip('<>')
            if target and not (p.parent/target).exists(): errors.append(f'Broken local link in {p.relative_to(root)}: {target}')
    if (root/'docs/task-progress.json').exists():
        data=json.loads((root/'docs/task-progress.json').read_text(encoding='utf-8'))
        tasks=data['tasks']
        if len(tasks)!=64 or len({t['id'] for t in tasks})!=64: errors.append('Task ledger must contain 64 unique items')
        for t in tasks:
            for evidence in t['evidence']:
                if not (root/evidence).exists(): errors.append('Missing task evidence: '+evidence)
    for folder in (root/'evaluations/results').glob('*'):
        if not folder.is_dir(): continue
        try:
            spec=importlib.util.spec_from_file_location('evaluation_release',root/'evaluations/harness.py')
            harness=importlib.util.module_from_spec(spec); spec.loader.exec_module(harness)
            manifest=harness.load(folder/'manifest.json'); records=harness.load(folder/'records.json')
            jobs={j['id'] for j in manifest['jobs']}
            if len({r['job_id'] for r in records})!=len(records): errors.append('Duplicate actual run record')
            if {r['job_id'] for r in records}!=jobs: errors.append('Run records do not cover manifest')
            for record in records:
                harness.ingest(manifest,record)
                raw=(folder/(record['job_id']+'.md')).read_bytes()
                if raw.decode('utf-8')!=record['response']: errors.append('Raw response text mismatch')
                if hashlib.sha256(raw).hexdigest()!=record['raw_file_sha256']: errors.append('Raw response hash mismatch')
        except (ValueError,OSError,KeyError) as exc: errors.append(str(exc))
    return {'checks':'package integrity only; not behavioral acceptance or research effectiveness',
            'examples':len(examples),'errors':errors,'passed':not errors}


if __name__=='__main__':
    result=check(); print(json.dumps(result,ensure_ascii=False,indent=2)); raise SystemExit(0 if result['passed'] else 1)
