#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
_build_lql9_chinese9b.py — 语文九下单元互动页生成 (九上语文脚本变体)
基座: lql_chinese8_u1_interactive.html
数据: _lql9_data/chinese9b_u{n}.json (n=1..6)
输出: lql_chinese9b_u{n}_interactive.html (localStorage key 带 lql_chinese9b_ 前缀)
"""
import json, os, re

REPO = '/home/administrator/xuci-jiancha'
BASE = os.path.join(REPO, 'lql_chinese8_u1_interactive.html')

def build(n):
    data = json.load(open(os.path.join(REPO, '_lql9_data', f'chinese9b_u{n}.json'), encoding='utf-8'))
    h = open(BASE, encoding='utf-8').read()
    log = []
    out = os.path.join(REPO, f'lql_chinese9b_u{n}_interactive.html')

    t_old = re.search(r'<title>[^<]*</title>', h).group(0)
    h = h.replace(t_old, f'<title>{data["hero_title"]} · 九年级下语文</title>', 1)
    h = re.sub(r'<h1><i class="fas fa-book-open"></i>[^<]*</h1>',
               f'<h1><i class="fas fa-book-open"></i> {data["hero_title"]}</h1>', h, count=1)

    nq, nf, ne = len(data['questions']), len(data['flashcards']), len(data['errors'])
    nk = len(data['knowledge'])
    m_old = re.search(r'<div class="meta">[^<]*</div>', h).group(0)
    h = h.replace(m_old, f'<div class="meta">{data["meta_desc"]} · {nq} 题 · {nk} 知识 · {nf} 卡 · {ne} 错</div>', 1)
    log.append(f'hero {data["hero_title"]}')

    i = h.find('<div class="knowledge-grid">')
    k_start = h.find('>', i) + 1
    k_end = h.find('<div id="tab-quiz"', i)
    items_html = ''.join(f'<div class="k-item"><h4>{k["t"]}</h4><p>{k["d"]}</p></div>\n      ' for k in data['knowledge'])
    items_html += '\n  </div></div>'
    h = h[:k_start] + items_html + h[k_end:].lstrip('\n ')
    log.append(f'knowledge {nk}')

    for decl, arr in [('const questions', data['questions']), ('const flashcards', data['flashcards']), ('const errors', data['errors'])]:
        for pat in [decl + '=[', decl + ' = [', decl + '=[']:
            idx = h.find(pat)
            if idx >= 0:
                eol = h.find('\n', idx)
                new = pat[:-1] + json.dumps(arr, ensure_ascii=False) + ';'
                h = h[:idx] + new + h[eol:]
                log.append(f'{decl.split()[-1]} {len(arr)}')
                break
        else:
            raise SystemExit(f'{decl} 声明未找到')

    h = h.replace('lql_chinese8_u1', f'lql_chinese9b_u{n}')
    # autoImport subject/tags 残留 ('第一单元 新闻阅读')
    short = data['hero_title'].replace(' · ', ' ')
    h = re.sub(r"subject:'第一单元 新闻阅读'", f"subject:'{short}'", h)
    h = re.sub(r"tags:'第一单元 新闻阅读[^']*'", f"tags:'{short},课堂练习'", h)
    h = h.replace('八年级上册', '九年级下册').replace('八上', '九下')
    open(out, 'w', encoding='utf-8').write(h)
    print('✅', os.path.basename(out))
    for l in log:
        print('  ', l)

def main():
    for n in range(1, 7):
        p = os.path.join(REPO, '_lql9_data', f'chinese9b_u{n}.json')
        if not os.path.exists(p):
            print('⚠️ 缺数据 chinese9b_u' + str(n) + '.json')
            continue
        try:
            build(n)
        except Exception as e:
            print('❌ u' + str(n), e)

if __name__ == '__main__':
    main()
