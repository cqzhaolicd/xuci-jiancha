#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""_build_lql9_math9b.py — 数学九下章页生成 (基座 lql_math8_ch1_interactive.html)
数据: _lql9_data/math9b_ch{n}.json (n=1..3); 输出 lql_math9b_ch{n}_interactive.html
"""
import json, os, re
REPO = '/home/administrator/xuci-jiancha'
BASE = os.path.join(REPO, 'lql_math8_ch1_interactive.html')
def build(n):
    data = json.load(open(os.path.join(REPO, '_lql9_data', f'math9b_ch{n}.json'), encoding='utf-8'))
    h = open(BASE, encoding='utf-8').read()
    out = os.path.join(REPO, f'lql_math9b_ch{n}_interactive.html')
    h = h.replace(re.search(r'<title>[^<]*</title>', h).group(0), f'<title>{data["hero_title"]} · 九年级下数学</title>', 1)
    h = re.sub(r'<h1>.*?</h1>', f'<h1><i class="fas fa-calculator"></i> {data["hero_title"]}</h1>', h, count=1, flags=re.DOTALL)
    nq, nf, ne, nk = len(data['questions']), len(data['flashcards']), len(data['errors']), len(data['knowledge'])
    h = re.sub(r'<div class="meta">.*?</div>', f'<div class="meta">{data["meta_desc"]} · {nq} 题 · {nk} 知识 · {nf} 卡 · {ne} 错</div>', h, count=1, flags=re.DOTALL)
    g0 = h.find('<div class="knowledge-grid">'); g1 = h.find('<div id="tab-quiz"', g0)
    gs = h.find('>', g0) + 1
    items = ''.join(f'<div class="k-item"><h4>{k["t"]}</h4><p>{k["d"]}</p></div>\n      ' for k in data['knowledge'])
    h = h[:gs] + items + '\n  </div></div>' + h[g1:].lstrip('\n ')
    blocks = []
    iq = h.find('const questions=['); ifc = h.find('const flashcards=[', iq+10); ie = h.find('const errors=[', ifc+10)
    m = re.search(r'\nlet curQ', h[ie+10:]); iend = ie + 10 + m.start() if m else h.find('</script>', ie)
    for start, end, decl, arr in sorted([(iq,ifc,'const questions',data['questions']),(ifc,ie,'const flashcards',data['flashcards']),(ie,iend,'const errors',data['errors'])], key=lambda b: -b[0]):
        h = h[:start] + decl + '=' + json.dumps(arr, ensure_ascii=False) + '\n' + h[end:]
    h = h.replace('lql_math8_ch1', f'lql_math9b_ch{n}')
    short = data['hero_title'].replace(' · ', ' ')
    h = re.sub(r"subject:'[^']*'", f"subject:'{short}'", h, count=2)
    h = re.sub(r"tags:'[^']*'", f"tags:'{short},课堂练习'", h, count=1)
    h = h.replace('八年级', '九年级').replace('八上', '九下')
    open(out, 'w', encoding='utf-8').write(h)
    print('OK', os.path.basename(out))
def main():
    for n in range(1, 4):
        p = os.path.join(REPO, '_lql9_data', f'math9b_ch{n}.json')
        if not os.path.exists(p): print('WARN 缺 math9b_ch' + str(n) + '.json'); continue
        try: build(n)
        except Exception as e: print('ERR math9b_ch' + str(n), e)
if __name__ == '__main__': main()
