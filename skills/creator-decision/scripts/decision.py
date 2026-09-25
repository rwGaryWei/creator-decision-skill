#!/usr/bin/env python3
"""Local evidence/decision tools. No network, model calls, or implicit approval."""
from __future__ import annotations

import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import hashlib
import html
import json
import os
from pathlib import Path
import re
import sys
import tempfile
from urllib.parse import urlsplit

VERSION = '0.1.0-alpha'
SCHEMA = '1.0'
MAX_BYTES = 8 * 1024 * 1024
ID = re.compile(r'[A-Za-z][A-Za-z0-9_-]{0,79}\Z')
DOMAINS = {'web_tool', 'video', 'short_drama', 'game'}
STAGES = {'idea', 'prototype', 'feedback'}
KINDS = {'user_statement', 'observation', 'external', 'inference'}
ACTIONS = {'continue', 'expand', 'narrow', 'change', 'test', 'pause'}


class Invalid(ValueError):
    pass


def need(ok, message):
    if not ok:
        raise Invalid(message)


def text(value, label, empty=False):
    need(isinstance(value, str) and (empty or bool(value.strip())), f'{label}: expected nonempty text')
    return value


def ident(value, label='id'):
    text(value, label)
    need(bool(ID.fullmatch(value)), f'{label}: use a letter followed by letters, digits, _ or - (max 80)')
    need(value.upper() not in {'CON', 'PRN', 'AUX', 'NUL', *[f'COM{i}' for i in range(1,10)], *[f'LPT{i}' for i in range(1,10)]}, f'{label}: reserved name')
    return value


def obj(value, label):
    need(isinstance(value, dict), f'{label}: expected object')
    return value


def arr(value, label):
    need(isinstance(value, list), f'{label}: expected array')
    return value


def strings(value, label):
    for item in arr(value, label):
        text(item, label)
    return value


def enum(value, choices, label):
    need(isinstance(value, str) and value in choices, f'{label}: expected one of {sorted(choices)}')


def timestamp(value, label):
    text(value, label)
    try:
        dt = datetime.fromisoformat(value.replace('Z', '+00:00'))
        need(dt.tzinfo is not None, f'{label}: timezone required')
    except ValueError as exc:
        raise Invalid(f'{label}: invalid timestamp') from exc


def unique(pairs):
    out = {}
    for key, value in pairs:
        need(key not in out, f'duplicate JSON key: {key}')
        out[key] = value
    return out


def parse(raw):
    need(len(raw) <= MAX_BYTES, 'input exceeds 8 MiB')
    try:
        return json.loads(raw.decode('utf-8-sig'), object_pairs_hook=unique,
            parse_constant=lambda s: (_ for _ in ()).throw(Invalid(f'invalid constant: {s}')))
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise Invalid('invalid UTF-8 JSON') from exc


def read(path):
    p = Path(path)
    need(p.stat().st_size <= MAX_BYTES, 'input exceeds 8 MiB')
    return parse(p.read_bytes())


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def encode(data):
    return (json.dumps(data, ensure_ascii=False, indent=2, allow_nan=False) + '\n').encode('utf-8')


def now():
    return datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')


def safe_url(url):
    text(url, 'url')
    need(not any(ord(c) <= 32 for c in url), 'url contains whitespace/control characters')
    try:
        parts = urlsplit(url)
        need(parts.scheme in {'http', 'https'} and bool(parts.hostname), 'url must be http(s) with a host')
        need(parts.username is None and parts.password is None, 'credentials in URLs are not permitted')
        _ = parts.port
    except ValueError as exc:
        raise Invalid('invalid URL') from exc
    return url


def validate(data):
    """Validate structure and literal quotes, not semantic support or factual truth."""
    obj(data, 'report')
    need(data.get('schema_version') == SCHEMA, 'unsupported schema_version; keep original, migrate explicitly')
    p = obj(data.get('project'), 'project')
    ident(p.get('id'), 'project.id')
    for name in ('title', 'goal', 'current_decision'):
        text(p.get(name), 'project.'+name)
    enum(p.get('domain'), DOMAINS, 'project.domain')
    enum(p.get('stage'), STAGES, 'project.stage')
    strings(p.get('constraints'), 'project.constraints')
    strings(p.get('preserve'), 'project.preserve')
    r = obj(data.get('report'), 'report')
    ident(r.get('id'), 'report.id')
    need(type(r.get('revision')) is int and r['revision'] > 0, 'report.revision: positive integer required')
    timestamp(r.get('created_at'), 'report.created_at')
    enum(r.get('mode'), {'live','snapshot','offline'}, 'report.mode')
    text(r.get('summary'), 'report.summary')
    strings(r.get('observed_scope'), 'report.observed_scope')
    strings(r.get('limitations'), 'report.limitations')
    if r.get('parent_report_id') is not None:
        ident(r['parent_report_id'], 'report.parent_report_id')
        need(r['parent_report_id'] != r['id'], 'report cannot be its own parent')
    for cap, state in obj(r.get('capabilities'), 'report.capabilities').items():
        ident(cap, 'capability')
        enum(state, {'available','unavailable','unverified'}, 'capability state')
    for secret in ('decisions', 'approved', 'human_accepted'):
        need(secret not in data, 'human decisions belong in a separately bound journal')

    groups = {}
    all_ids = {p['id'], r['id']}
    need(len(all_ids)==2, 'project/report IDs must be distinct')
    for group in ('artifacts','sources','claims','assumptions','recommendations','experiments'):
        groups[group] = {}
        for item in arr(data.get(group), group):
            obj(item, group)
            item_id=ident(item.get('id'), group+'.id')
            need(item_id not in all_ids, f'duplicate object ID: {item_id}')
            all_ids.add(item_id)
            groups[group][item_id]=item
            if 'project_id' in item:
                need(item['project_id']==p['id'], 'cross-project object reference')

    def refs(values, allowed, label):
        strings(values,label)
        need(len(set(values))==len(values), label+': duplicate reference')
        need(set(values)<=set(allowed), label+': unknown reference')

    warnings=[]
    for a in groups['artifacts'].values():
        for key in ('title','version','kind'):
            text(a.get(key), 'artifact.'+key)
        enum(a.get('access'), {'full','partial','failed','not_inspected'}, 'artifact.access')
        strings(a.get('observed'), 'artifact.observed')
        strings(a.get('not_observed'), 'artifact.not_observed')
        if a['access'] in {'failed','not_inspected'}:
            need(not a['observed'], 'failed/uninspected artifact cannot claim observations')
    for s in groups['sources'].values():
        text(s.get('title'),'source.title')
        enum(s.get('kind'), {'user','public','observation','synthetic'}, 'source.kind')
        need(type(s.get('synthetic')) is bool, 'source.synthetic: boolean required')
        need(s['synthetic'] == (s['kind']=='synthetic'), 'synthetic source must be labeled consistently')
        enum(s.get('access'), {'full','partial','failed','not_inspected'}, 'source.access')
        text(s.get('content'),'source.content',empty=True)
        text(s.get('redistribution'),'source.redistribution')
        timestamp(s.get('retrieved_at'),'source.retrieved_at')
        need(s.get('sha256')==digest(s['content'].encode('utf-8')), 'source content hash mismatch')
        if s.get('url') is not None: safe_url(s['url'])
        if s['access'] in {'failed','not_inspected'}:
            need(not s['content'], 'failed/uninspected source cannot contain purported captured text')
    for c in groups['claims'].values():
        text(c.get('text'),'claim.text')
        enum(c.get('kind'), KINDS, 'claim.kind')
        enum(c.get('status'), {'supported','contested','unverified'}, 'claim.status')
        strings(c.get('limitations'),'claim.limitations')
        evidence=arr(c.get('evidence'),'claim.evidence')
        if c['kind']=='external' and c['status']!='unverified':
            need(bool(evidence), 'supported/contested external claim needs evidence')
        for ref in evidence:
            obj(ref,'evidence reference')
            sid=ref.get('source_id')
            need(isinstance(sid,str) and sid in groups['sources'], 'unknown source_id')
            source=groups['sources'][sid]
            quote=text(ref.get('quote'),'quote')
            need(source['access'] in {'full','partial'}, 'quote uses uninspected source')
            need(quote in source['content'], 'quote not present in captured source text')
            text(ref.get('location'),'quote.location')
            if source['synthetic']:
                need(c['kind'] in {'inference','user_statement'}, 'synthetic evidence cannot support real-world observation/external claim')
                need(c['status']=='unverified', 'synthetic claim must remain unverified externally')
        if c['status']=='unverified': warnings.append(c['id']+': unverified; not a fact certification')
    for a in groups['assumptions'].values():
        text(a.get('text'),'assumption.text')
        enum(a.get('state'), {'unknown','supported','weakened','inconclusive'}, 'assumption.state')
        refs(a.get('claim_ids'),groups['claims'],'assumption.claim_ids')
        text(a.get('change_condition'),'assumption.change_condition')
    need(bool(groups['recommendations']), 'at least one recommendation required')
    for rec in groups['recommendations'].values():
        enum(rec.get('action'),ACTIONS,'recommendation.action')
        for key in ('target','reason','tradeoff','condition'):
            text(rec.get(key),'recommendation.'+key)
        strings(rec.get('keep'),'recommendation.keep')
        refs(rec.get('rationale_ids'),set(groups['claims'])|set(groups['assumptions']),'recommendation.rationale_ids')
        need(bool(rec['rationale_ids']), 'recommendation needs traceable rationale')
    for exp in groups['experiments'].values():
        refs(exp.get('assumption_ids'),groups['assumptions'],'experiment.assumption_ids')
        need(bool(exp['assumption_ids']),'experiment must test an assumption')
        for key in ('task','observe','decision_rule','resource_limit'):
            text(exp.get(key),'experiment.'+key)
        enum(exp.get('status'),{'planned','running','completed','cancelled'},'experiment.status')
        if exp['status'] in {'planned','cancelled'}:
            need(exp.get('results') is None, 'planned/cancelled experiment cannot contain results')
        if exp['status']=='completed': text(exp.get('results'),'experiment.results')
    return {'valid':True,'checks':'structure, IDs, relationships, source hashes and literal quotes only',
        'semantic_support':'not_checked','warnings':warnings}


def escape(value):
    # Escape Markdown structure and HTML. Render URLs as text, not executable links.
    s=html.escape(str(value),quote=True).replace('\r',' ').replace('\n',' ')
    for c in '\\`*_{}[]()#+-.!|>': s=s.replace(c,'\\'+c)
    return s


def render(data):
    validate(data)
    p=data['project']; r=data['report']
    lines=[f'# {escape(p["title"])}', '', f'**Goal:** {escape(p["goal"])}',
        f'**Decision now:** {escape(p["current_decision"])}','',escape(r['summary']),'',
        '**Human decision:** pending; see the separately bound journal for recorded decisions.','',
        '## Recommendations','']
    for rec in data['recommendations']:
        lines += [f'### {escape(rec["action"])} — {escape(rec["target"])}',
            f'- Why: {escape(rec["reason"])}', f'- Preserve: {escape("; ".join(rec["keep"]))}',
            f'- Tradeoff: {escape(rec["tradeoff"])}', f'- Conditions: {escape(rec["condition"])}',
            f'- Rationale: {escape(", ".join(rec["rationale_ids"]))}','']
    lines+=['## Next experiments','']
    for e in data['experiments']:
        lines += [f'### {escape(e["id"])} · {escape(e["status"])}',f'- Task: {escape(e["task"])}',
            f'- Observe: {escape(e["observe"])}',f'- Decision rule: {escape(e["decision_rule"])}',
            f'- Resource limit: {escape(e["resource_limit"])}', f'- Results: {escape(e.get("results") or "not recorded")}', '']
    lines+=['## Observed scope','']+[f'- {escape(s)}' for s in r['observed_scope']]
    lines+=['','## Limitations','']+[f'- {escape(s)}' for s in r['limitations']]
    lines+=['','## Claims and evidence','']
    for c in data['claims']:
        lines += [f'- {escape(c["id"])} [{escape(c["kind"])} / {escape(c["status"])}]: {escape(c["text"])}']
        for ev in c['evidence']:
            lines += [f'  - {escape(ev["source_id"])} / {escape(ev["location"])}: “{escape(ev["quote"])}”']
    lines+=['','## Sources','']
    for s in data['sources']:
        lines += [f'- {escape(s["id"])}: {escape(s["title"])}; {escape(s["kind"])}; captured {escape(s["retrieved_at"])}; {escape(s.get("url") or "supplied material")}.',
            f'  - Redistribution: {escape(s["redistribution"])}']
    lines+=['','Validation checks structure and literal quotations, not truth, semantic support or market acceptance.','']
    return '\n'.join(lines)


def contained(root, *parts):
    base=Path(root).resolve()
    target=base.joinpath(*parts).resolve()
    need(target.is_relative_to(base), 'path escapes project root')
    # Reject existing symlink segments rather than trusting their present destinations.
    cur=base
    for part in parts:
        cur=cur/part
        need(not cur.is_symlink(), 'symlink storage paths are not supported')
    return target


@contextmanager
def lock(folder):
    folder=Path(folder); folder.mkdir(parents=True,exist_ok=True)
    marker=folder/'.write.lock'
    try:
        fd=os.open(marker,os.O_CREAT|os.O_EXCL|os.O_WRONLY,0o600)
    except FileExistsError as exc:
        raise Invalid('store locked; inspect active writer before manually removing stale .write.lock') from exc
    try:
        with os.fdopen(fd,'w') as stream: stream.write(str(os.getpid()))
        yield
    finally:
        marker.unlink(missing_ok=True)


def atomic(path, raw, replace=False):
    path=Path(path)
    need(not path.is_symlink(),'refusing symlink output')
    need(replace or not path.exists(),'output exists; choose a new version/path')
    path.parent.mkdir(parents=True,exist_ok=True)
    fd,tmp=tempfile.mkstemp(prefix='.pending-',dir=path.parent)
    try:
        with os.fdopen(fd,'wb') as f:
            f.write(raw); f.flush(); os.fsync(f.fileno())
        if replace: os.replace(tmp,path)
        else:
            # Hard-link creates the destination atomically without replacing a rival writer.
            os.link(tmp,path)
    except FileExistsError as exc:
        raise Invalid('output exists; choose a new version/path') from exc
    finally:
        Path(tmp).unlink(missing_ok=True)


def save_report(root, input_path):
    need(Path(input_path).stat().st_size <= MAX_BYTES, 'input exceeds 8 MiB')
    raw=Path(input_path).read_bytes(); data=parse(raw); validate(data)
    pid=data['project']['id']; rid=data['report']['id']
    folder=contained(root,pid)
    with lock(folder):
        dest=contained(root,pid,'reports',rid+'.json')
        parent=data['report'].get('parent_report_id')
        if parent:
            old=read(contained(root,pid,'reports',parent+'.json')); validate(old)
            need(old['project']['id']==pid,'parent project mismatch')
            need(data['report']['revision']>old['report']['revision'],'revision must increase')
        atomic(dest,raw)
    return {'path':str(dest),'sha256':digest(raw),'human_decision':'pending'}


def journal_read(path):
    path=Path(path)
    if not path.exists(): return []
    need(path.stat().st_size <= MAX_BYTES,'journal exceeds 8 MiB')
    raw=path.read_bytes()
    need(len(raw)<=MAX_BYTES,'journal exceeds 8 MiB')
    need(not raw or raw.endswith(b'\n'),'journal incomplete: preserve original and recover explicitly')
    records=[]; previous=None
    for line in raw.splitlines():
        row=obj(parse(line),'journal row')
        need(row.get('previous_hash')==previous,'journal chain mismatch')
        content={k:v for k,v in row.items() if k!='event_hash'}
        need(row.get('event_hash')==digest(encode(content)),'journal event hash mismatch')
        need(row.get('role')=='human' and row.get('explicit_confirmation') is True,'invalid human decision record')
        ident(row.get('project_id')); ident(row.get('report_id')); ident(row.get('recommendation_id'))
        timestamp(row.get('created_at'),'decision.created_at')
        text(row.get('user_statement'),'decision.user_statement')
        enum(row.get('decision'),{'accept','modify','reject','defer'},'decision')
        need(re.fullmatch(r'[0-9a-f]{64}',str(row.get('report_sha256'))) is not None,'invalid report hash')
        if row['decision']=='modify': text(row.get('replacement'),'decision.replacement')
        previous=row['event_hash']; records.append(row)
    return records


def decide(root,pid,rid,recid,choice,statement,confirmed=False,replacement=None):
    ident(pid); ident(rid); ident(recid)
    enum(choice,{'accept','modify','reject','defer'},'decision')
    need(confirmed is True,'explicit human confirmation required; silence remains pending')
    text(statement,'actual user statement')
    if choice=='modify': text(replacement,'replacement')
    folder=contained(root,pid)
    with lock(folder):
        report_path=contained(root,pid,'reports',rid+'.json')
        raw=report_path.read_bytes(); data=parse(raw); validate(data)
        need(data['project']['id']==pid and data['report']['id']==rid,'report identity mismatch')
        need(recid in {r['id'] for r in data['recommendations']},'unknown recommendation')
        logfile=contained(root,pid,'decisions.jsonl')
        records=journal_read(logfile)
        for row in records:
            need(row['project_id']==pid,'journal belongs to another project')
        event={'project_id':pid,'report_id':rid,'report_revision':data['report']['revision'],
            'report_sha256':digest(raw),'recommendation_id':recid,'decision':choice,
            'user_statement':statement,'replacement':replacement,'role':'human','explicit_confirmation':True,
            'created_at':now(),'previous_hash':records[-1]['event_hash'] if records else None}
        duplicate=next((e for e in reversed(records) if all(e.get(k)==event.get(k) for k in ('report_sha256','recommendation_id','decision','user_statement','replacement'))),None)
        if duplicate: return {'duplicate':True,'event_hash':duplicate['event_hash']}
        event['event_hash']=digest(encode(event))
        blob=b''.join(encode(e).replace(b'\n',b' ') .rstrip()+b'\n' for e in records+[event])
        # Journal hashing uses parsed values, independent of the compact line serialization.
        atomic(logfile,blob,replace=True)
    return event


def decisions_for(root,pid,rid):
    ident(pid); ident(rid)
    raw=contained(root,pid,'reports',rid+'.json').read_bytes(); data=parse(raw); validate(data)
    need(data['project']['id']==pid and data['report']['id']==rid,'report identity mismatch')
    report_hash=digest(raw)
    records=journal_read(contained(root,pid,'decisions.jsonl'))
    need(all(e['project_id']==pid for e in records),'cross-project journal')
    return [{'recommendation_id':r['id'], 'decision': next((e['decision'] for e in reversed(records)
        if e['report_id']==rid and e['report_sha256']==report_hash and e['recommendation_id']==r['id']), 'pending')}
        for r in data['recommendations']]


def compare(old,new):
    validate(old); validate(new)
    need(old['project']['id']==new['project']['id'],'cannot compare different projects')
    result={}
    for key in ('project','claims','assumptions','recommendations','experiments'):
        if old[key]!=new[key]: result[key]={'before':old[key],'after':new[key]}
    return {'changed':result,'interpretation':'Structural difference only; explain evidence/goal changes separately.'}


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--version',action='version',version=VERSION)
    sub=parser.add_subparsers(dest='cmd',required=True)
    for name in ('validate','render','save'):
        p=sub.add_parser(name); p.add_argument('report')
        if name=='render': p.add_argument('--output',required=True)
        if name=='save': p.add_argument('--root',required=True)
    p=sub.add_parser('diff'); p.add_argument('old'); p.add_argument('new')
    p=sub.add_parser('decide'); p.add_argument('--root',required=True); p.add_argument('--project',required=True)
    p.add_argument('--report',required=True); p.add_argument('--recommendation',required=True)
    p.add_argument('--decision',required=True,choices=['accept','modify','reject','defer'])
    p.add_argument('--statement',required=True); p.add_argument('--confirmed-human',action='store_true')
    p.add_argument('--replacement')
    p=sub.add_parser('status'); p.add_argument('--root',required=True); p.add_argument('--project',required=True); p.add_argument('--report',required=True)
    args=parser.parse_args(argv)
    try:
        if args.cmd=='validate': result=validate(read(args.report))
        elif args.cmd=='render':
            atomic(args.output,render(read(args.report)).encode('utf-8')); result={'written':args.output}
        elif args.cmd=='save': result=save_report(args.root,args.report)
        elif args.cmd=='diff': result=compare(read(args.old),read(args.new))
        elif args.cmd=='decide': result=decide(args.root,args.project,args.report,args.recommendation,args.decision,args.statement,args.confirmed_human,args.replacement)
        else: result=decisions_for(args.root,args.project,args.report)
        print(json.dumps(result,ensure_ascii=False,indent=2)); return 0
    except (Invalid,OSError) as exc:
        print(f'Error: {exc}',file=sys.stderr); return 2


if __name__=='__main__':
    raise SystemExit(main())
