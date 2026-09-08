#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""重建 math9/physics9 闯关页为实际教材版本(北师/沪科)"""
import json, re, os

REPO = '/home/administrator/xuci-jiancha'
TEMPLATE = os.path.join(REPO, 'lql_preview_challenge_math8.html')

JOBS = [
    ('math_bsd',  'lql_preview_challenge_math9.html',    '九年级上册 · 北师大版'),
    ('physics_hk','lql_preview_challenge_physics9.html', '九年级全一册 · 沪科版'),
]

def build(subject, out_name, version):
    data = json.load(open(os.path.join(REPO, '_lql9_data', subject + '.json'), encoding='utf-8'))
    h = open(TEMPLATE, encoding='utf-8').read()
    # title
    h = re.sub(r'<title>[^<]*</title>', f'<title>{data["title"]}</title>', h, count=1)
    # SUBJECT
    h = re.sub(r'const SUBJECT = "[^"]*";', f'const SUBJECT = "{data["subject"]}";', h, count=1)
    # VERSION
    h = re.sub(r'const VERSION = "[^"]*";', f'const VERSION = "{version}";', h, count=1)
    # WORLDS
    i = h.find('const WORLDS = ['); j = h.find('const BOSS', i)
    h = h[:i] + 'const WORLDS = ' + json.dumps(data['worlds'], ensure_ascii=False) + ';\n' + h[j:]
    # BOSS
    i = h.find('const BOSS = {'); j = h.find('const LS', i)
    h = h[:i] + 'const BOSS = ' + json.dumps(data['boss'], ensure_ascii=False) + ';\n' + h[j:]
    # LS 前缀
    for p in ['coins','stars','unlocked','cleared','wrong','boss']:
        h = h.replace(f"'lql_preview_{p}_'", f"'lql_preview9_{p}_'")
    open(os.path.join(REPO, out_name), 'w', encoding='utf-8').write(h)
    print('✅', out_name, '|', version, '| WORLDS', len(data['worlds']), 'BOSS', len(data['boss']['quiz']))

for sub, out, ver in JOBS:
    build(sub, out, ver)
