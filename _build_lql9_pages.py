#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
_build_lql9_pages.py — 由 _lql9_data/*.json 生成 5 个九年级预习闯关页
模板: lql_preview_challenge_math8.html (lql_ 前缀版, 结构同源)
输出: lql_preview_challenge_{math,physics,chinese,english,chemistry}9.html
改动: title / const SUBJECT / WORLDS / BOSS 数据 / LS key 前缀 lql_preview_ → lql_preview9_
"""
import json, os, re

REPO = '/home/administrator/xuci-jiancha'
DATA = os.path.join(REPO, '_lql9_data')
TEMPLATE = os.path.join(REPO, 'lql_preview_challenge_math8.html')

JOBS = [
    ('math',       'lql_preview_challenge_math9.html'),
    ('physics',    'lql_preview_challenge_physics9.html'),
    ('chemistry',  'lql_preview_challenge_chemistry9.html'),
    ('chinese',    'lql_preview_challenge_chinese9.html'),
    ('english',    'lql_preview_challenge_english9.html'),
]

def build(subject, out_name):
    data = json.load(open(os.path.join(DATA, subject + '.json'), encoding='utf-8'))
    h = open(TEMPLATE, encoding='utf-8').read()
    log = []

    # 1) title
    old_t = re.search(r'<title>[^<]*</title>', h).group(0)
    h = h.replace(old_t, f'<title>{data["title"]}</title>', 1)
    log.append('title')

    # 2) SUBJECT
    h = re.sub(r'const SUBJECT = "[^"]*";', f'const SUBJECT = "{data["subject"]}";', h, count=1)
    log.append('subject=' + data['subject'])

    # 3) WORLDS 段替换(到 const BOSS 前)
    i = h.find('const WORLDS = [')
    j = h.find('const BOSS', i)
    assert i >= 0 and j > i
    new_w = 'const WORLDS = ' + json.dumps(data['worlds'], ensure_ascii=False) + ';\n'
    h = h[:i] + new_w + h[j:]
    log.append('WORLDS=%d关' % len(data['worlds']))

    # 4) BOSS 段替换(到 const LS 前)
    i = h.find('const BOSS = {')
    j = h.find('const LS', i)
    assert i >= 0 and j > i
    new_b = 'const BOSS = ' + json.dumps(data['boss'], ensure_ascii=False) + ';\n'
    h = h[:i] + new_b + h[j:]
    log.append('BOSS=%d题' % len(data['boss']['quiz']))

    # 5) LS key 前缀 → lql_preview9_ (与 8 年级同科避免共享)
    for p in ['coins', 'stars', 'unlocked', 'cleared', 'wrong', 'boss']:
        h = h.replace(f"'lql_preview_{p}_'", f"'lql_preview9_{p}_'")

    open(os.path.join(REPO, out_name), 'w', encoding='utf-8').write(h)
    print('✅', out_name, '|', ' | '.join(log))

def main():
    for subject, out_name in JOBS:
        if not os.path.exists(os.path.join(DATA, subject + '.json')):
            print('⚠️ 缺数据:', subject + '.json')
            continue
        try:
            build(subject, out_name)
        except Exception as e:
            print('❌', subject, e)
    # 残差校验
    print('\n--- 残留检查 ---')
    for _, out in JOBS:
        p = os.path.join(REPO, out)
        if not os.path.exists(p):
            continue
        s = open(p, encoding='utf-8').read()
        r = []
        if '八年级' in s: r.append('八年级残留')
        if '北师大' in s: r.append('北师大残留')
        if "'lql_preview_coins_'" in s: r.append('旧key前缀残留')
        print(out, r if r else '✅')

if __name__ == '__main__':
    main()
