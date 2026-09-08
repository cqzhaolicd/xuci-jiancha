#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""_build_lql9_math.py — 数学北师九上章页生成 (基座 lql_math8_ch1_interactive.html 理科4-tab模板)
数据: _lql9_data/math9_ch{n}.json (n=1..6)
输出: lql_math9_ch{n}_interactive.html
"""
import json, os, re

REPO = '/home/administrator/xuci-jiancha'
BASE = os.path.join(REPO, 'lql_math8_ch1_interactive.html')

def build(n):
    data = json.load(open(os.path.join(REPO, '_lql9_data', f'math9_ch{n}.json'), encoding='utf-8'))
    h = open(BASE, encoding='utf-8').read()
    log = []
    out = os.path.join(REPO, f'lql_math9_ch{n}_interactive.html')

    m = re.search(r'<title>[^<]*</title>', h)
    h = h.replace(m.group(0), f'<title>{data["hero_title"]} · 九年级数学</title>', 1)
    m = re.search(r'<h1>.*?</h1>', h, re.DOTALL)
    h = h.replace(m.group(0), f'<h1><i class="fas fa-calculator"></i> {data["hero_title"]}</h1>', 1)
    nq, nf, ne, nk = len(data['questions']), len(data['flashcards']), len(data['errors']), len(data['knowledge'])
    m = re.search(r'<div class="meta">.*?</div>', h, re.DOTALL)
    h = h.replace(m.group(0), f'<div class="meta">{data["meta_desc"]} · {nq} 题 · {nk} 知识 · {nf} 卡 · {ne} 错</div>', 1)
    log.append(f'hero {data["hero_title"]}')

    g0 = h.find('<div class="knowledge-grid">')
    g1 = h.find('<div id="tab-quiz"', g0)
    gs = h.find('>', g0) + 1
    items = ''.join(f'<div class="k-item"><h4>{k["t"]}</h4><p>{k["d"]}</p></div>\n      ' for k in data['knowledge'])
    h = h[:gs] + items + '\n  </div></div>' + h[g1:].lstrip('\n ')
    log.append(f'knowledge {nk}')

    # 5) 三数组 — 整段替换 [声明, 下一锚点) (源数组格式不定: 单行/多行/有无分号)
    blocks = []
    iq = h.find('const questions=[')
    if iq < 0: iq = h.find('const questions = [')
    ifc = h.find('const flashcards=[', iq + 10)
    if ifc < 0: ifc = h.find('const flashcards = [', iq + 10)
    ie = h.find('const errors=[', ifc + 10)
    if ie < 0: ie = h.find('const errors = [', ifc + 10)
    m = re.search(r'\nlet curQ', h[ie + 10:])
    iend = ie + 10 + m.start() if m else h.find('</script>', ie)
    assert iq > 0 and ifc > iq and ie > ifc, f'数组声明定位失败 iq={iq} ifc={ifc} ie={ie}'
    blocks = [(iq, ifc, 'const questions', data['questions']),
              (ifc, ie, 'const flashcards', data['flashcards']),
              (ie, iend, 'const errors', data['errors'])]
    # 从后往前替换避免偏移
    for start, end, decl, arr in sorted(blocks, key=lambda b: -b[0]):
        new_block = decl + '=' + json.dumps(arr, ensure_ascii=False) + '\n'
        h = h[:start] + new_block + h[end:]
        log.append(f'{decl.split()[-1]} {len(arr)}')

    # key 段与 subject/tags 残留
    h = h.replace('lql_math8_ch1', f'lql_math9_ch{n}')
    short = data['hero_title'].replace(' · ', ' ')
    h = re.sub(r"tags:'[^']*'", f"tags:'{short},课堂练习'", h, count=1)
    old = re.search(r"subject:'[^']*'", h)
    if old:
        short = data['hero_title'].replace(' · ', ' ')
        h = re.sub(r"subject:'[^']*'", f"subject:'{short}'", h, count=2)
    h = h.replace('八年级', '九年级').replace('八上', '九上')
    open(out, 'w', encoding='utf-8').write(h)
    print('✅', os.path.basename(out))
    for l in log:
        print('  ', l)

def main():
    for n in range(1, 7):
        p = os.path.join(REPO, '_lql9_data', f'math9_ch{n}.json')
        if not os.path.exists(p):
            print('⚠️ 缺数据 math9_ch' + str(n) + '.json')
            continue
        try:
            build(n)
        except Exception as e:
            print('❌ math9_ch' + str(n), e)

if __name__ == '__main__':
    main()
