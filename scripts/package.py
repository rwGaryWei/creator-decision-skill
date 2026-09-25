"""Build an allowlisted alpha ZIP. Does not publish anything."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import zipfile

ROOT=Path(__file__).resolve().parents[1]
TOP={'skills','scripts','tests','evaluations','examples','docs','.github'}
ROOT_FILES={'README.md','README.zh-CN.md','CONTRIBUTING.md','SECURITY.md','CHANGELOG.md','LICENSE','.gitignore','.gitattributes'}
EXT={'.py','.md','.json','.yml','.yaml','.txt'}


def files():
    result=[]
    for p in sorted(ROOT.rglob('*')):
        rel=p.relative_to(ROOT)
        if rel.parts[0] not in TOP and rel.as_posix() not in ROOT_FILES: continue
        if '__pycache__' in rel.parts or p.is_dir(): continue
        if p.suffix not in EXT and rel.as_posix() not in ROOT_FILES: continue
        if p.is_symlink(): raise ValueError('No symlinks in package')
        raw=p.read_bytes()
        if re.search(rb'(gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,}|-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----)',raw):
            raise ValueError('Possible credential in '+rel.as_posix())
        result.append((rel.as_posix(),raw))
    return result


def package(output):
    output=Path(output)
    if output.exists() or output.is_symlink(): raise ValueError('output already exists')
    contents=files()
    manifest={name:hashlib.sha256(raw).hexdigest() for name,raw in contents}
    output.parent.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(output,'x',compression=zipfile.ZIP_DEFLATED) as z:
        for name,raw in contents:
            info=zipfile.ZipInfo('creator-decision-skill/'+name,date_time=(2026,9,25,0,0,0))
            info.compress_type=zipfile.ZIP_DEFLATED
            z.writestr(info,raw)
        z.writestr('creator-decision-skill/PACKAGE-SHA256.json',json.dumps(manifest,indent=2)+'\n')
    with zipfile.ZipFile(output) as z:
        if z.testzip() is not None: raise ValueError('archive integrity failure')
    return {'path':str(output),'files':len(contents),'sha256':hashlib.sha256(output.read_bytes()).hexdigest()}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__); p.add_argument('--output',required=True); args=p.parse_args()
    print(json.dumps(package(args.output),indent=2))
