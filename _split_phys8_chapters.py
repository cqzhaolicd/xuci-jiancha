#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把 physics8_interactive.html（八上早背晚默全册）拆成 6 个章节互动页。"""
import re, sys

SRC = 'physics8_interactive.html'
h = open(SRC, encoding='utf-8').read()

# ============ 1. 提取数据 ============
def split_objs(text, prefix):
    """逐段提取 {prefix...} 对象（对象内不含裸 }）"""
    objs, pos = [], 0
    while True:
        m = re.search(r'\{%s:.*?\}' % prefix, text[pos:], re.DOTALL)
        if not m:
            break
        objs.append(m.group(0))
        pos += m.end()
    return objs

qs = re.search(r'const questions=\[(.*?)\n\];', h, re.DOTALL).group(1)
q_objs = split_objs(qs, 'q')
fs = re.search(r'const flashcards=\[(.*?)\n\];', h, re.DOTALL).group(1)
f_objs = split_objs(fs, 'front')
es = re.search(r'const errors=\[(.*?)\n\];', h, re.DOTALL).group(1)
e_objs = split_objs(es, 'title')
print('题目:%d 卡牌:%d 易错:%d' % (len(q_objs), len(f_objs), len(e_objs)))
assert len(q_objs) == len(f_objs) == 342 and len(e_objs) == 6

# 章节序列（按卡牌 back 的章节标签，数组顺序）
chapters = []
for o in f_objs:
    m = re.search(r'back:\'<strong>第\d+条 · ([^<]+)</strong>', o)
    chapters.append(m.group(1).strip())
print('章节分布:', {c: chapters.count(c) for c in dict.fromkeys(chapters)})

# ============ 2. 章节配置 ============
# 每章：数组下标范围（按章节标签连续段）
ranges = []  # (start, end_exclusive)
cur = None
for i, c in enumerate(chapters):
    if c != cur:
        if cur is not None:
            ranges[-1] = (ranges[-1][0], i)
        cur = c
        ranges.append((i, None))
ranges[-1] = (ranges[-1][0], len(chapters))
print('章节下标范围:', ranges)

# 知识卡（knowledge-grid 中 6 张卡）
grid_orig = open('/tmp/grid_orig.html').read()
k_cards = re.findall(r'<div class="knowledge-card c\d">.*?</div>\n', grid_orig, re.DOTALL)
print('知识卡数:', len(k_cards))
assert len(k_cards) == 6

# 易错点标题（用于确认对应章节）
for i, e in enumerate(e_objs):
    t = re.search(r'title:\'([^\']+)', e).group(1)
    print('  易错[%d]: %s' % (i, t))

CHS = [
    {'n': 1, 'name': '机械运动',   'kcard': 0, 'err': 0,
     'frame': '<strong>1️⃣ 机械运动</strong> — 单位换算 + 刻度尺 + v=s/t'},
    {'n': 2, 'name': '声现象',     'kcard': 1, 'err': 1,
     'frame': '<strong>2️⃣ 声现象</strong> — 振动产生 + 三特性 + 回声计算'},
    {'n': 3, 'name': '物态变化',   'kcard': 2, 'err': 2,
     'frame': '<strong>3️⃣ 物态变化</strong> — 六种变化 + 晶体/非晶体 + 吸放热'},
    {'n': 4, 'name': '光现象',     'kcard': 3, 'err': 3,
     'frame': '<strong>4️⃣ 光现象</strong> — 反射定律 + 平面镜 + 折射规律'},
    {'n': 5, 'name': '透镜及其应用', 'kcard': 4, 'err': 4,
     'frame': '<strong>5️⃣ 透镜</strong> — 成像规律（u、f关系）+ 眼睛矫正'},
    {'n': 6, 'name': '质量与密度', 'kcard': 5, 'err': 5,
     'frame': '<strong>6️⃣ 质量与密度</strong> — ρ=m/V + 天平使用 + 反常膨胀'},
]

# ============ 3. 段边界（基于原页） ============
t_i = h.find('<div class="teacher-talk">')
t_end = h.find('</div>\n\n    <div class="knowledge-grid">', t_i) + 6
g_i = h.find('<div class="knowledge-grid">')
g_end = h.find('    </div>\n\n    <div class="card">', g_i) + len('    </div>')
c_i = h.find('<div class="card"><div class="card-title"><i class="fas fa-star"')
c_end = h.find('</div>\n    </div>\n\n  <div id="tab-quiz"', c_i) + 6
assert all(x > 0 for x in (t_i, t_end, g_i, g_end, c_i, c_end))
print('段边界 OK: teacher-talk(%d-%d) grid(%d-%d) frame(%d-%d)' % (t_i, t_end, g_i, g_end, c_i, c_end))

# ============ 4. 生成 6 页 ============
for ch, (lo, hi) in zip(CHS, ranges):
    n, name = ch['n'], ch['name']
    nq = hi - lo
    # 4.1 数组切分
    q_part = ',\n'.join(q_objs[lo:hi])
    f_part = ',\n'.join(f_objs[lo:hi])
    e_part = e_objs[ch['err']]
    # 4.2 从副本开始
    o = h[:]
    # 4.2.1 段替换（每步基于当前 o 动态定位，防止前一步长度变化导致索引错位）
    new_tt = ('    <div class="teacher-talk">\n'
              '      <h4><i class="fas fa-chalkboard-teacher"></i> 使用说明</h4>\n'
              '      <p>本页聚焦《八上物理必考知识38天早背晚默》<strong>第%d章 %s</strong>，共 %d 个必考知识点。通过知识图谱速览 → 闯关测验自测 → 知识卡牌记忆 → 易错自检巩固，按章节系统掌握八上物理核心内容。</p>\n'
              '      <p style="margin-top:.5rem"><strong>⚠️ 完成本章知识卡牌学习后，配合闯关测验检验掌握程度，用易错自检标记薄弱点反复练习。</strong></p>\n'
              '    </div>') % (n, name, nq)
    t_i = o.find('<div class="teacher-talk">')
    t_end = o.find('</div>\n\n    <div class="knowledge-grid">', t_i) + 6
    o = o[:t_i] + new_tt + o[t_end:]
    new_grid = '    <div class="knowledge-grid">\n\n      %s\n    </div>' % k_cards[ch['kcard']].rstrip('\n')
    g_i = o.find('<div class="knowledge-grid">')
    g_end = o.find('    </div>\n\n    <div class="card">', g_i) + len('    </div>')
    o = o[:g_i] + new_grid + o[g_end:]
    new_frame = ('    <div class="card"><div class="card-title"><i class="fas fa-star" style="color:var(--warning)"></i> 第%d章 %s · 核心复习框架</div>\n'
                 '      <p style="font-size:.9rem;line-height:2;background:#f0f0ff;padding:1rem;border-radius:var(--radius-sm)">\n'
                 '        %s<br>\n'
                 '        ⚠️ 每天早背晚默，坚持38天，八上物理不丢分！\n'
                 '      </p>\n'
                 '    </div>') % (n, name, ch['frame'])
    c_i = o.find('<div class="card"><div class="card-title"><i class="fas fa-star"')
    c_end = o.find('</div>\n    </div>\n\n  <div id="tab-quiz"', c_i) + 6
    o = o[:c_i] + new_frame + o[c_end:]
    # 4.2.2 数组替换（动态定位）
    qi = o.find('const questions=[')
    qj = o.find('\n];', qi)
    o = o[:qi] + 'const questions=[' + '\n' + q_part + '\n];' + o[qj + 3:]
    fi = o.find('const flashcards=[')
    fj = o.find('\n];', fi)
    o = o[:fi] + 'const flashcards=[' + '\n' + f_part + '\n];' + o[fj + 3:]
    ei = o.find('const errors=[')
    ej = o.find('\n];', ei)
    o = o[:ei] + 'const errors=[' + '\n' + e_part + '\n];' + o[ej + 3:]
    # 4.2.3 文本替换（replace 全量，不依赖索引）
    o = o.replace('<title>📐 初中物理·八上早背晚默 · 互动学习</title>',
                  '<title>📐 初中物理·八上早背晚默 · 第%d章 %s</title>' % (n, name))
    o = o.replace(' 物理 · 八上早背晚默</a>', ' 物理 · 八上早背晚默 · 第%d章</a>' % n)
    o = o.replace('<h1><i class="fas fa-calculator"></i> 初中物理·八上早背晚默 · 互动学习</h1>',
                  '<h1><i class="fas fa-calculator"></i> 初中物理·八上早背晚默 · 第%d章 %s</h1>' % (n, name))
    o = o.replace('<p>38天早背晚默 · 6大章节 · ⭐⭐⭐⭐⭐</p>',
                  '<p>38天早背晚默 · 第%d章 %s · ⭐⭐⭐⭐⭐</p>' % (n, name))
    o = o.replace('342道测验题', '%d道测验题' % nq)
    o = o.replace('342张知识卡', '%d张知识卡' % nq)
    o = o.replace('6大易错点', '1大易错点')
    o = o.replace('共342张知识卡', '共%d张知识卡' % nq)
    o = o.replace('数学 · 八上物理早背晚默互动学习',
                  '物理 · 八上早背晚默 · 第%d章 %s' % (n, name))
    o = o.replace('<div class="quiz-stats" id="quizStats">0 / 30</div>',
                  '<div class="quiz-stats" id="quizStats">0 / %d</div>' % nq)
    # localStorage keys 独立化
    o = o.replace("WRONG_HISTORY_KEY='quiz_phys8_wrong'",
                  "WRONG_HISTORY_KEY='quiz_phys8_ch%d_wrong'" % n)
    o = o.replace("QUIZ_PROG_KEY='quiz_progress_physics8'",
                  "QUIZ_PROG_KEY='quiz_progress_physics8_ch%d'" % n)
    o = o.replace("'physics8_check'", "'physics8_ch%d_check'" % n)
    # 写文件
    out = 'physics8_ch%d_interactive.html' % n
    open(out, 'w', encoding='utf-8').write(o)
    print('✅ 生成 %s  %s: %d题/%d卡/1易错' % (out, name, nq, nq))

print('全部生成完毕')
