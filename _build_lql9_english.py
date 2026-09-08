#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""_build_lql9_english.py — 英语九全 Unit 页 (基座 lql_chinese8_u1_interactive.html)
数据: _lql9_data/english9_u{n}.json (n=1..14); 输出 lql_english9_u{n}_interactive.html
"""
import json, os, re

REPO = '/home/administrator/xuci-jiancha'
BASE = os.path.join(REPO, 'lql_chinese8_u1_interactive.html')

def build(n):
    data = json.load(open(os.path.join(REPO, '_lql9_data', f'english9_u{n}.json'), encoding='utf-8'))
    h = open(BASE, encoding='utf-8').read()
    out = os.path.join(REPO, f'lql_english9_u{n}_interactive.html')
    h = h.replace(re.search(r'<title>[^<]*</title>', h).group(0), f'<title>{data["hero_title"]} · 九年级英语</title>', 1)
    h = re.sub(r'<h1>.*?</h1>', f'<h1><i class="fas fa-book-open"></i> {data["hero_title"]}</h1>', h, count=1, flags=re.DOTALL)
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
    h = h.replace('lql_chinese8_u1', f'lql_english9_u{n}')
    short = data['hero_title'].replace(' · ', ' ').replace('"', '\\"')
    h = re.sub(r"subject:'第一单元 新闻阅读'", f'subject:"{short}"', h)
    h = re.sub(r"tags:'第一单元 新闻阅读[^']*'", f'tags:"{short},课堂练习"', h)
    h = h.replace('八年级上册', '九年级全一册').replace('八上', '九全')
    open(out, 'w', encoding='utf-8').write(h)
    print('✅', os.path.basename(out))

def main():
    for n in range(1, 15):
        p = os.path.join(REPO, '_lql9_data', f'english9_u{n}.json')
        if not os.path.exists(p):
            print('⚠️ 缺数据 english9_u' + str(n) + '.json')
            continue
        try:
            build(n)
        except Exception as e:
            print('❌ english9_u' + str(n), e)

if __name__ == '__main__':
    main()
