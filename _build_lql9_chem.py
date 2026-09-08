#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""_build_lql9_chem.py — 化学九上单元页生成 (基座 lql_bio8_ch1_interactive.html 理科4-tab模板)
数据: _lql9_data/chem9_{0..7}.json (0=绪言, 1-7=单元)
输出: lql_chem9_intro_interactive.html + lql_chem9_u1..u7_interactive.html
"""
import json, os, re

REPO = '/home/administrator/xuci-jiancha'
BASE = os.path.join(REPO, 'lql_bio8_ch1_interactive.html')

JOBS = [(0, 'intro', '绪言'), (1, 'u1', '第一单元'), (2, 'u2', '第二单元'), (3, 'u3', '第三单元'),
        (4, 'u4', '第四单元'), (5, 'u5', '第五单元'), (6, 'u6', '第六单元'), (7, 'u7', '第七单元')]

def build(key, out_sfx):
    data = json.load(open(os.path.join(REPO, '_lql9_data', f'chem9_{key}.json'), encoding='utf-8'))
    h = open(BASE, encoding='utf-8').read()
    log = []
    out = os.path.join(REPO, f'lql_chem9_{out_sfx}_interactive.html')

    # 1) title (基座 title 形如 "第1章 ... · 8年级上生物")
    m = re.search(r'<title>[^<]*</title>', h)
    h = h.replace(m.group(0), f'<title>{data["hero_title"]} · 九年级化学</title>', 1)
    log.append('title')

    # 2) hero h1 (+ icon → fa-flask)
    m = re.search(r'<h1>.*?</h1>', h, re.DOTALL)
    h = h.replace(m.group(0), f'<h1><i class="fas fa-flask"></i> {data["hero_title"]}</h1>', 1)
    log.append('h1')

    # 3) meta
    nq, nf, ne, nk = len(data['questions']), len(data['flashcards']), len(data['errors']), len(data['knowledge'])
    m = re.search(r'<div class="meta">.*?</div>', h, re.DOTALL)
    h = h.replace(m.group(0), f'<div class="meta">{data["meta_desc"]} · {nq} 题 · {nk} 知识 · {nf} 卡 · {ne} 错</div>', 1)
    log.append(f'meta {nq}题/{nk}知/{nf}卡/{ne}错')

    # 4) knowledge-grid 替换 (含 grid+tab-knowledge 两个闭合 div)
    g0 = h.find('<div class="knowledge-grid">')
    g1 = h.find('<div id="tab-quiz"', g0)
    assert g0 > 0 and g1 > g0, 'knowledge-grid 未找到'
    gs = h.find('>', g0) + 1
    items = ''.join(f'<div class="k-item"><h4>{k["t"]}</h4><p>{k["d"]}</p></div>\n      ' for k in data['knowledge'])
    h = h[:gs] + items + '\n  </div></div>' + h[g1:].lstrip('\n ')
    log.append(f'knowledge {nk}')

    # 5) 三数组 (const xxx= 无空格风格)
    for decl, arr in [('const questions', data['questions']), ('const flashcards', data['flashcards']), ('const errors', data['errors'])]:
        for pat in [decl + '=[', decl + ' = [']:
            idx = h.find(pat)
            if idx >= 0:
                j2 = h.find('];', idx)
                assert j2 > idx, decl
                h = h[:idx] + pat + json.dumps(arr, ensure_ascii=False) + '];' + h[j2 + 2:]
                log.append(f'{decl.split()[-1]} {len(arr)}')
                break
        else:
            raise SystemExit(decl + ' 未找到')

    # 6) localStorage key 段 与 autoImport subject 残留
    h = h.replace('lql_bio8_ch1', f'lql_chem9_{out_sfx}')
    # bio8 autoImport 硬编码 subject 残留 -> hero 短名
    old_subj = re.search(r"subject:'[^']*'", h)
    if old_subj and ('动物' in old_subj.group(0) or '生物' in old_subj.group(0)):
        short = data['hero_title'].replace(' · ', ' ')
        h = re.sub(r"subject:'[^']*'", f"subject:'{short}'", h, count=2)
        log.append('subject残留→' + short)

    # 7) 年级文本与 footer
    h = h.replace('八年级', '九年级').replace('八上', '九上').replace('生物', '化学')
    open(out, 'w', encoding='utf-8').write(h)
    print('✅', os.path.basename(out))
    for l in log:
        print('  ', l)

def main():
    for key, sfx, _ in JOBS:
        p = os.path.join(REPO, '_lql9_data', f'chem9_{key}.json')
        if not os.path.exists(p):
            print('⚠️ 缺数据 chem9_' + str(key) + '.json')
            continue
        try:
            build(key, sfx)
        except Exception as e:
            print('❌ chem9_' + str(key), e)

if __name__ == '__main__':
    main()
