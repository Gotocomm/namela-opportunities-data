#!/usr/bin/env python3
"""Validate data/opportunities.json before it is pushed. The website refuses a file that fails these checks,
so run this after every change:  python3 tools/validate.py"""
import json, re, sys, datetime
from urllib.parse import urlparse

DATE = re.compile(r'^\d{4}-\d{2}-\d{2}$')
ID = re.compile(r'^[a-z0-9]+(-[a-z0-9]+)*$')
ENUM = {
    'cat': {'study', 'work', 'business', 'abroad'},  # the website's filters only know these four
    'who': {'learner', 'student', 'jobseeker', 'business', 'org'},
    'diff': {'Low', 'Medium', 'High'},
    'conf': {'High', 'Medium', 'Low'},
    'tags': {'value', 'gem'},
}
REQUIRED = ['id', 'title', 'type', 'cat', 'who', 'by', 'elig', 'get', 'diff', 'conf', 'step', 'link', 'checked']
TEXT = ['title', 'type', 'by', 'elig', 'get', 'step', 'note', 'needs', 'next', 'closeText', 'prov']
MAXLEN = {'title': 120, 'type': 40, 'by': 160, 'elig': 400, 'get': 400, 'step': 400, 'note': 400, 'needs': 300, 'next': 300, 'closeText': 120, 'prov': 40}

def check(path):
    errors = []
    try:
        data = json.load(open(path, encoding='utf-8'))
    except Exception as e:
        return [f'{path}: not valid JSON ({e})']
    if not isinstance(data, dict) or not isinstance(data.get('items'), list):
        return [f'{path}: must be an object with an "items" list']
    if path.endswith('opportunities.json'):
        if not DATE.match(str(data.get('scanned', ''))):
            errors.append('"scanned" must be a YYYY-MM-DD date')
        if not 5 <= len(data['items']) <= 200:
            errors.append(f'expected between 5 and 200 items, found {len(data["items"])}')
    seen = set()
    for i, o in enumerate(data['items']):
        where = f'item {i} ({o.get("id", "?")})'
        for k in REQUIRED:
            if k not in o or o[k] in ('', None, []):
                errors.append(f'{where}: missing {k}')
        if not ID.match(str(o.get('id', ''))): errors.append(f'{where}: id must be lowercase-with-hyphens')
        if o.get('id') in seen: errors.append(f'{where}: duplicate id')
        seen.add(o.get('id'))
        for k, allowed in ENUM.items():
            v = o.get(k)
            if v is None: continue
            vals = v if isinstance(v, list) else [v]
            bad = [x for x in vals if x not in allowed]
            if bad: errors.append(f'{where}: {k} has invalid value(s) {bad}; allowed {sorted(allowed)}')
        for k in ('open', 'close', 'checked', 'added'):
            if k in o and not DATE.match(str(o[k])): errors.append(f'{where}: {k} must be YYYY-MM-DD')
        for k in ('link', 'source'):
            if k in o:
                u = urlparse(str(o[k]))
                if u.scheme != 'https' or not u.netloc: errors.append(f'{where}: {k} must be a full https:// address')
        for k in TEXT:
            v = o.get(k)
            if v is None: continue
            if not isinstance(v, str): errors.append(f'{where}: {k} must be text'); continue
            if '<' in v or '>' in v: errors.append(f'{where}: {k} must not contain HTML')
            if len(v) > MAXLEN[k]: errors.append(f'{where}: {k} is longer than {MAXLEN[k]} characters')
            if '—' in v or '–' in v: errors.append(f'{where}: {k} contains a dash; use commas, colons or full stops')
        if not o.get('rolling') and not o.get('close') and not o.get('expected'):
            errors.append(f'{where}: needs a close date, "rolling": true or "expected": true (the website hides items without one)')
        for k in ('rolling', 'estimate', 'expected'):
            if k in o and not isinstance(o[k], bool): errors.append(f'{where}: {k} must be true or false')
    return errors

if __name__ == '__main__':
    errs = check('data/opportunities.json') + check('data/archive.json')
    if errs:
        print('\n'.join(errs)); sys.exit(1)
    print('OK')
