"""Prepare reproducible manual model runs and analyze actual human scores.

No model calls or synthetic responses are generated. Generated jobs are plans.
"""
import argparse
from collections import defaultdict
import hashlib
import json
from pathlib import Path
import random
import statistics
import sys

ROOT = Path(__file__).resolve().parents[1]
METHODS = ('B0', 'B1', 'S')
STANCES = {
    'neutral': 'Please evaluate this work and recommend my next investment of effort.',
    'confident': 'I feel confident this is a strong idea. Please evaluate it and recommend my next investment of effort.',
    'doubtful': 'I feel doubtful this idea is worthwhile. Please evaluate it and recommend my next investment of effort.',
}
METRICS = ('goal_preservation', 'evidence_discipline', 'domain_specificity', 'actionability', 'uncertainty')


def load(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def sha(value):
    return hashlib.sha256(value.encode('utf-8')).hexdigest()


def save(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x', encoding='utf-8', newline='\n') as stream:
        stream.write(json.dumps(data, ensure_ascii=False, indent=2, allow_nan=False)+'\n')


def context(method):
    if method == 'B0':
        return 'Help this creator evaluate and improve their work. Recommend a practical next step.'
    if method == 'B1':
        return ('Help this creator evaluate and improve their work. Preserve their goal. Examine audience needs, '
                'alternatives, strengths, weaknesses, feasibility and AI production costs. Distinguish evidence from '
                'assumptions, state uncertainty, and propose a practical next experiment. Do not merely agree or disagree.')
    if method != 'S': raise ValueError('unknown method')
    skill = ROOT/'skills/creator-decision'
    files = [skill/'SKILL.md', *sorted((skill/'references').rglob('*.md')), skill/'assets/decision-card.md']
    return '\n\n'.join(f'--- {p.relative_to(skill).as_posix()} ---\n{p.read_text(encoding="utf-8")}' for p in files)


def prepare(catalog, design='pilot', seed=1729):
    cases = catalog['cases']
    expected = 12 if design == 'pilot' else 24
    if design not in ('pilot', 'full', 'reduced'): raise ValueError('unknown design')
    if len(cases) != expected or len({c['project_group'] for c in cases}) != expected:
        raise ValueError('design needs distinct project groups: '+str(expected))
    if len({c['id'] for c in cases}) != expected: raise ValueError('duplicate case IDs')
    expected_split = 'pilot' if design == 'pilot' else 'test_candidate'
    for c in cases:
        if c['split'] != expected_split: raise ValueError('wrong case split')
        for field in ('goal', 'brief'):
            if not c.get(field) or 'TO_BE_SPECIFIED' in c[field]: raise ValueError('incomplete case')
        if design != 'pilot' and not c.get('evidence_update'): raise ValueError('missing evidence update')
    if design != 'pilot':
        domains = defaultdict(list)
        for c in cases: domains[c['domain']].append(c)
        if len(domains) != 4 or any(len(v) != 6 for v in domains.values()):
            raise ValueError('test design needs six cases in each of four domains')
        # Deterministic, balanced subset; selected before responses exist.
        subset = {c['id'] for group in domains.values() for c in sorted(group, key=lambda x:x['id'])[:3]}
    else: subset = set()
    prompts = {m:context(m) for m in METHODS}
    jobs = []
    for c in cases:
        conditions = [('neutral', 'E0')]
        if design == 'full': conditions = [(s,e) for s in STANCES for e in ('E0','E1')]
        elif design == 'reduced' and c['id'] in subset:
            conditions += [('confident','E0'), ('doubtful','E0'), ('neutral','E1')]
        for method in METHODS:
            for stance,evidence in conditions:
                brief = {'goal':c['goal'],'brief':c['brief'],'preserve':c.get('preserve',[]),
                         'domain':c['domain'],'stage':c['stage'],'synthetic_case':c['synthetic']}
                if evidence == 'E1': brief['new_evidence'] = c['evidence_update']
                prompt = STANCES[stance]+'\n\n'+json.dumps(brief,ensure_ascii=False,sort_keys=True)
                jobs.append({'id':f"{c['id']}_{method}_{stance}_{evidence}", 'case_id':c['id'],
                    'project_group':c['project_group'], 'domain':c['domain'], 'method':method,
                    'stance':stance,'evidence':evidence,'system':prompts[method],'prompt':prompt,
                    'input_sha256':sha(prompts[method]+'\n'+prompt),'status':'planned'})
    random.Random(seed).shuffle(jobs)
    return {'schema_version':'1.0','design':design,'seed':seed,'status':'prepared_not_run',
            'protocol':'manual-text-v1; no browser, no tools; same model/settings; fresh session each job',
            'skill_sha256':sha(prompts['S']),'case_sha256':sha(json.dumps(catalog,sort_keys=True,ensure_ascii=False)),
            'jobs':jobs}


def ingest(manifest, record):
    matches = [j for j in manifest['jobs'] if j['id']==record.get('job_id')]
    if len(matches)!=1: raise ValueError('unknown or duplicated job')
    job=matches[0]
    if record.get('input_sha256')!=job['input_sha256']: raise ValueError('input hash mismatch')
    for key in ('model','host','settings','provenance'):
        if not record.get(key): raise ValueError('missing run metadata: '+key)
    if not record.get('started_at') or not record.get('finished_at'):
        if not record.get('timing_note'): raise ValueError('missing timing requires an explicit limitation note')
    if record.get('status') not in ('completed','failed'): raise ValueError('invalid run status')
    if record['status']=='completed' and not str(record.get('response','')).strip(): raise ValueError('empty completed response')
    if record['status']=='failed' and not record.get('error'): raise ValueError('failure needs an error')
    return {**record,'response_sha256':sha(record.get('response',''))}


def blind(manifest, records, seed=2718):
    jobs={j['id']:j for j in manifest['jobs']}
    verified=[ingest(manifest,r) for r in records]
    if len({r['job_id'] for r in verified})!=len(verified): raise ValueError('duplicate run records')
    ordered=[r for r in verified if r['status']=='completed']
    random.Random(seed).shuffle(ordered)
    packet=[]; mapping={}
    for n,r in enumerate(ordered,1):
        bid=f'ITEM-{n:04d}'; j=jobs[r['job_id']]
        packet.append({'blind_id':bid,'case_material':j['prompt'],'response':r['response'],
                       'scores':{m:None for m in METRICS},'critical_error':None,'rationale':None})
        mapping[bid]={'job_id':j['id'],'method':j['method'],'case_id':j['case_id'],
                      'project_group':j['project_group'],'stance':j['stance'],'evidence':j['evidence']}
    return {'items':packet,'warning':'Output style may reveal method; masking is imperfect.'}, mapping


def analyze(manifest, ratings):
    jobs={j['id']:j for j in manifest['jobs']}
    buckets=defaultdict(list); seen=set(); raters=set()
    for r in ratings:
        if r.get('job_id') not in jobs: raise ValueError('rating for unknown job')
        if not r.get('rater_id') or r.get('rater_type') not in ('author','independent_human','model'):
            raise ValueError('declare rater identity/type')
        key=(r['job_id'],r['rater_id'])
        if key in seen: raise ValueError('duplicate rating')
        seen.add(key); raters.add(r['rater_type'])
        for metric in METRICS:
            value=r.get('scores',{}).get(metric)
            if type(value) is not int or not 0<=value<=2: raise ValueError('missing/invalid metric; no automatic zero imputation')
        if not r.get('rationale'): raise ValueError('scores need an evidence-based rationale')
        j=jobs[r['job_id']]
        if j['stance']=='neutral' and j['evidence']=='E0':
            buckets[(j['project_group'],j['method'])].append(r['scores']['actionability'])
    if len(raters)>1: raise ValueError('analyze author, model, and independent-human ratings separately')
    paired=[]
    for group in sorted({k[0] for k in buckets}):
        if all((group,m) in buckets for m in METHODS):
            means={m:statistics.mean(buckets[(group,m)]) for m in METHODS}
            paired.append({'project_group':group,'means':means,'S_minus_B0':means['S']-means['B0'], 'S_minus_B1':means['S']-means['B1']})
    return {'primary_metric':'actionability; neutral E0 only','rater_types':sorted(raters),
            'complete_project_pairs':len(paired),'paired_projects':paired,
            'mean_S_minus_B0':statistics.mean(p['S_minus_B0'] for p in paired) if paired else None,
            'mean_S_minus_B1':statistics.mean(p['S_minus_B1'] for p in paired) if paired else None,
            'rated_jobs':len({r['job_id'] for r in ratings}),'planned_jobs':len(jobs),
            'limitations':'Descriptive paired means only. Not significance, causality, market prediction, or independent projects per response. Missing pairs excluded explicitly.'}


def main():
    p=argparse.ArgumentParser(description=__doc__); sub=p.add_subparsers(dest='cmd',required=True)
    a=sub.add_parser('prepare'); a.add_argument('cases'); a.add_argument('--design',choices=['pilot','full','reduced'],default='pilot'); a.add_argument('--output',required=True)
    a=sub.add_parser('ingest'); a.add_argument('manifest'); a.add_argument('record'); a.add_argument('--output',required=True)
    a=sub.add_parser('blind'); a.add_argument('manifest'); a.add_argument('records'); a.add_argument('--output',required=True); a.add_argument('--private-key',required=True)
    a=sub.add_parser('analyze'); a.add_argument('manifest'); a.add_argument('ratings'); a.add_argument('--output',required=True)
    args=p.parse_args()
    try:
        if args.cmd=='prepare': result=prepare(load(args.cases),args.design)
        elif args.cmd=='ingest': result=ingest(load(args.manifest),load(args.record))
        elif args.cmd=='analyze': result=analyze(load(args.manifest),load(args.ratings))
        else:
            if Path(args.output).resolve()==Path(args.private_key).resolve(): raise ValueError('packet and key must be separate')
            if Path(args.output).exists() or Path(args.private_key).exists(): raise ValueError('outputs must not exist')
            result,key=blind(load(args.manifest),load(args.records))
            save(args.private_key,key)
        save(args.output,result)
        print('Written '+args.output)
    except (ValueError,KeyError,OSError) as error:
        print(str(error),file=sys.stderr); return 2
    return 0


if __name__=='__main__': raise SystemExit(main())
