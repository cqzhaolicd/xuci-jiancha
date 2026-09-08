#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
_build_lql9_chinese.py — 语文九上单元互动页生成
基座: lql_chinese8_u1_interactive.html (刘秋灵 lql_ 前缀轻量4-tab模板, 已 key 独立)
数据: _lql9_data/chinese9_u{n}.json (子代理产出)
输出: lql_chinese9_u{n}_interactive.html
"""
import json, os, re

REPO = '/home/administrator/xuci-jiancha'
BASE = os.path.join(REPO, 'lql_chinese8_u1_interactive.html')

def build(n):
    data = json.load(open(os.path.join(REPO, '_lql9_data', f'chinese9_u{n}.json'), encoding='utf-8'))
    h = open(BASE, encoding='utf-8').read()
    log = []
    out = os.path.join(REPO, f'lql_chinese9_u{n}_interactive.html')

    # 1) title
    t_old = re.search(r'<title>[^<]*</title>', h).group(0)
    h = h.replace(t_old, f'<title>{data["hero_title"]} · 九年级上语文</title>', 1)
    log.append('title')

    # 2) hero h1
    h = re.sub(r'<h1><i class="fas fa-book-open"></i>[^<]*</h1>',
               f'<h1><i class="fas fa-book-open"></i> {data["hero_title"]}</h1>', h, count=1)
    log.append('h1')

    # 3) hero meta (数字用实际计数)
    nq, nf, ne = len(data['questions']), len(data['flashcards']), len(data['errors'])
    nk = len(data['knowledge'])
    m_old = re.search(r'<div class="meta">[^<]*</div>', h).group(0)
    h = h.replace(m_old, f'<div class="meta">{data["meta_desc"]} · {nq} 题 · {nk} 知识 · {nf} 卡 · {ne} 错</div>', 1)
    log.append(f'meta {nq}题/{nk}知/{nf}卡/{ne}错')

    # 4) knowledge-grid 内容: 每个 .k-item 由 JSON 生成(定位 grid 起始到闭合前)
    i = h.find('<div class="knowledge-grid">')
    assert i >= 0, 'knowledge-grid 未找到'
    j = h.find('</div>', i)  # grid 内容第一个闭合是首 k-item 的? 不可靠, 找 </div> 后跟 tab-content 结构
    # 更稳: knowledge-grid 段结束 = 其容器 tab-knowledge 的闭合前; 但 grid 后有 </div>(tab-knowledge)
    # 用结构: <div class="knowledge-grid"> ... </div>  </div>(tab-knowledge闭合)
    # 找 k-item 循环起止: 从 i 起第一个 '</div>' 是首 item 结束; 换策略:
    # 直接找 k-item 开始与 tab-quiz 开始之间为 grid 内容区
    # grid 外再包一层 div(可能): 数 grid 后闭合层数
    # 简化: grid 内容 = 从 grid 开标签后到 "    </div>\n    <div id=\"tab-quiz\"" 前; 该段以 '>' 后内容即 items
    k_start = h.find('>', i) + 1
    k_end = h.find('<div id="tab-quiz"', i)
    assert k_start > 0 and k_end > k_start, 'grid 区间未找到'
    items_html = ''.join(f'<div class="k-item"><h4>{k["t"]}</h4><p>{k["d"]}</p></div>\n      ' for k in data['knowledge'])
    items_html += '\n  </div></div>'   # 闭合 knowledge-grid + tab-knowledge
    # 若原段尾部已含 </div></div> 需避免重复 — k_end 定位到 tab-quiz 前，原闭合已被整体替换
    # 若原 grid 段内容以 <div class="k-item">... 重复多次, 且末尾可能有注释/换行 — 直接替换区间
    h = h[:k_start] + items_html + h[k_end:].lstrip('\n ')
    log.append(f'knowledge {nk}')

    # 5) 三数组替换 (压缩 JSON 风格与源一致)
    segs = [
        ('const questions', data['questions']),
        ('const flashcards', data['flashcards']),
        ('const errors', data['errors']),
    ]
    for decl, arr in segs:
        # 源里 questions 可能是 'const questions=[' 或 'const questions = [' 或 'const questions=[']
        for pat in [decl + '=[', decl + ' = [', decl + '=[']:
            idx = h.find(pat)
            if idx >= 0:
                # 基座模板数组为单行 JSON, 行末 ']' 即闭合 (无 '];' 结尾)
                eol = h.find('\n', idx)
                assert eol > idx, f'{decl} 行尾未找到'
                # pat 自带 '[' 开头, json.dumps 也有 '[' — 去掉 pat 末尾 '[' 避免 '[[' 重复
                new = pat[:-1] + json.dumps(arr, ensure_ascii=False) + ';'
                h = h[:idx] + new + h[eol:]
                log.append(f'{decl} {len(arr)}')
                break
        else:
            raise SystemExit(f'{decl} 声明未找到')

    # 6) localStorage key 文件名段
    h = h.replace('lql_chinese8_u1', f'lql_chinese9_u{n}')
    log.append('key段→lql_chinese9_u' + str(n))

    # 7) footer 若出现 "八上" 字样修正
    h = h.replace('八年级上册', '九年级上册').replace('八上', '九上')
    open(out, 'w', encoding='utf-8').write(h)
    print('✅', out)
    for l in log:
        print('  ', l)

def main():
    for n in range(1, 7):
        p = os.path.join(REPO, '_lql9_data', f'chinese9_u{n}.json')
        if not os.path.exists(p):
            print('⚠️ 缺数据 chinese9_u' + str(n) + '.json')
            continue
        try:
            build(n)
        except Exception as e:
            print('❌ u' + str(n), e)

if __name__ == '__main__':
    main()
