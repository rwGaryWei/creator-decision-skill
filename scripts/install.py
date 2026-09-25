"""Install the bundled skill into an explicitly chosen project. No network."""
import argparse
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]


def install(project):
    project = Path(project).resolve(strict=True)
    if not project.is_dir():
        raise ValueError('project must be an existing directory')
    target = project / '.agents' / 'skills' / 'creator-decision'
    for part in (project/'.agents', project/'.agents/skills', target):
        if part.is_symlink():
            raise ValueError('installation path contains a symlink')
    if target.exists():
        raise ValueError('skill already exists; review it before replacing anything')
    source = ROOT / 'skills' / 'creator-decision'
    if any(p.is_symlink() for p in source.rglob('*')):
        raise ValueError('source contains a symlink')
    shutil.copytree(source, target, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
    return target


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project', required=True, help='Existing project folder chosen by you')
    args = parser.parse_args()
    try:
        print(install(args.project))
    except (OSError, ValueError) as error:
        print(f'Installation failed: {error}', file=sys.stderr)
        raise SystemExit(2)
