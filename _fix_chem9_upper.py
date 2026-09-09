#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""_fix_chem9_upper.py — 重建化学九上 8 页(intro+u1..u7) 修复双层数组 bug
基座: lql_chem9_u8_interactive.html (单层数组, 已验证) ; 数据: chem9_{0..7}.json
"""
import json, os, re

REPO = '/home/administrator/xuci-jiancha'
BASE = os.path.join(REPO, 'lql_chem9_u8_interactive.html')

def build(key, out_sfx):
    data = json.load(open(os.path.join(REPO, '_lql9_data', f'chem9_{key}.json'), encoding='utf-8'))
    h = open(BASE, encoding='utf-8').read()
    out = os.path.join(REPO, f'lql_chem9_{out_sfx}_interactive.html')
    h = h.replace(re.search(r'<title>[^<]*</title>', h).group(0), f'<title>{data["hero_title"]} · 九年级化学</title>', 1)
    h = re.sub(r'<h1>.*?</h1>', f'<h1><i class="fas fa-flask"></i> {data["hero_title"]}</h1>', h, count=1, flags=re.DOTALL)
    nq, nf, ne, nk = len(data['questions']), len(data['flashcards']), len(data['errors']), len(data['knowledge'])
    h = re.sub(r'<div class="meta">.*?</div>', f'<div class="meta">{data["meta_desc"]} · {nq} 题 · {nk} 知识 · {nf} 卡 · {ne} 错</div>', h, count=1, flags=re.DOTALL)
    g0 = h.find('<div class="knowledge-grid">'); g1 = h.find('<div id="tab-quiz"', g0)
    gs = h.find('>', g0) + 1
    items = ''.join(f'<div class="k-item"><h4>{k["t"]}</h4><p>{k["d"]}</p></div>\n      ' for k in data['knowledge'])
    h = h[:gs] + items + '\n  </div></div>' + h[g1:].lstrip('\n ')
    iq = h.find('const questions=['); ifc = h.find('const flashcards=[', iq+10); ie = h.find('const errors=[', ifc+10)
    m = re.search(r'let curQ', h[ie:]); iend = ie + m.start() if m else h.find('</script>', ie)
    assert iq > 0 and ifc > iq and ie > ifc
    for start, end, decl, arr in sorted([(iq,ifc,'const questions',data['questions']),(ifc,ie,'const flashcards',data['flashcards']),(ie,iend,'const errors',data['errors'])], key=lambda b: -b[0]):
        h = h[:start] + decl + '=' + json.dumps(arr, ensure_ascii=False) + '\n' + h[end:]
    h = h.replace('lql_chem9_u8', f'lql_chem9_{out_sfx}')
    short = data['hero_title'].replace(' · ', ' ')
    h = re.sub(r"subject:'[^']*'", f"subject:'{short}'", h, count=2)
    h = re.sub(r"tags:'[^']*'", f"tags:'{short},课堂练习'", h, count=1)
    open(out, 'w', encoding='utf-8').write(h)
    print('✅', os.path.basename(out))

if __name__ == '__main__':
    build(0, 'intro')
    for n in range(1, 8):
        build(n, f'u{n}')
