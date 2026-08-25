# -*- coding: utf-8 -*-
"""升级 math8_ch1 赵爽弦图:知识卡进阶 + 3道弦图题 + 2张卡 + 1易错 + 横幅同步"""
import re, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

P = 'math8_ch1_interactive.html'
h = open(P, encoding='utf-8').read()
orig = h

# ---------- 1. 知识图谱"赵爽弦图"卡升级 ----------
old_kp = '<div class="k-item"><h4>赵爽弦图</h4><p>四个全等直角三角形拼成正方形。外弦图：(a+b)²=c²+4×½ab；内弦图：(a-b)²+4×½ab=c²。</p></div>'
new_kp = ('<div class="k-item"><h4>赵爽弦图·进阶</h4><p><strong>构图</strong>：四个全等直角三角形（直角边a、b，斜边c）拼成正方形，用<strong>等面积法</strong>证勾股定理。<br>'
          '<strong>外弦图</strong>（三角在外）：大正方形边长 <strong>a+b</strong>，中间小正方形边长 <strong>c</strong>（由斜边构成），'
          'S大=(a+b)²=c²+4×½ab → a²+b²=c²。<br>'
          '<strong>内弦图</strong>（三角在内）：大正方形边长 <strong>c</strong>（由斜边构成），中间小正方形边长 <strong>|a−b|</strong>，'
          'c²=(a−b)²+4×½ab → a²+b²=c²。<br>'
          '<strong>历史</strong>：三国·赵爽为《周髀算经》作注时创制，是最早的勾股定理严格证明之一。<br>'
          '<strong>考法</strong>：①给面积反求边长（列方程）；②弦图+坐标系求点坐标。</p></div>')
assert old_kp in h, '知识卡未找到'
h = h.replace(old_kp, new_kp)
print('1. 知识卡替换 OK')

# ---------- 2. questions 末尾追加 3 道弦图题 ----------
qi = h.index('const questions=') + len('const questions=')
# 找 questions 数组闭合:第一个 "}]" 且后面是 \nconst flashcards
qf = h.index('\nconst flashcards=', qi)
qseg_end = h.rindex('}]', qi, qf)  # 指向原数组最后对象 } 的位置（不含）
assert qseg_end > qi, 'questions 闭合未找到'

new_qs = [
'{"q": "赵爽内弦图中，四个全等直角三角形拼成的大正方形边长为 c（斜边），中间小正方形边长为", "opts": ["A. a+b", "B. |a-b|", "C. c", "D. 2ab"], "ans": 1, "exp": "内弦图：斜边 c 构成外面的大正方形，中间留出的小正方形边长 = 两条直角边之差 = |a-b|（a、b 大小不定，须加绝对值）。"}',
'{"q": "赵爽弦图中，四个全等直角三角形的直角边为 3 和 4，外弦图大正方形的面积是", "opts": ["A. 49", "B. 25", "C. 12", "D. 37"], "ans": 0, "exp": "外弦图大正方形边长 = a+b = 7，面积 = 7² = 49。验证：c²=25，4×½×3×4=24，25+24=49 ✓"}',
'{"q": "赵爽弦图（内弦图）中，大正方形面积为 25，中间小正方形面积为 1，则直角三角形较短的直角边为", "opts": ["A. 2", "B. 3", "C. 4", "D. 5"], "ans": 1, "exp": "大正方形面积 = c² = 25 → c=5；小正方形面积 = (a-b)² = 1 → |a-b|=1；由 a²+b²=25 且 a-b=1 解得 a=4、b=3，较短直角边 = 3。"}'
]
h = h[:qseg_end] + '},\n' + ',\n'.join(new_qs) + h[qseg_end+1:]
print('2. questions 追加', len(new_qs), '题 OK')

# ---------- 3. flashcards 升级赵爽弦图卡 + 追加2张 ----------
old_fc = '{"q": "赵爽弦图", "a": "外弦图：(a+b)²=c²+4×½ab → a²+b²=c²"}'
new_fc = '{"q": "赵爽弦图", "a": "四个全等Rt△拼正方形，等面积法证勾股定理。外弦图：(a+b)²=c²+4×½ab；内弦图：c²=(a-b)²+4×½ab → 均得 a²+b²=c²"}'
assert old_fc in h, '赵爽弦图卡未找到'
h = h.replace(old_fc, new_fc)
print('3a. 赵爽弦图卡替换 OK')

# 替换后再定位数组（长度已变，必须重新 index）
fi = h.index('const flashcards=') + len('const flashcards=')
fe = h.index('\nconst errors=', fi)
fseg_end = h.rindex('}]', fi, fe)
assert fseg_end > fi, 'flashcards 闭合未找到'

new_fcs = [
'{"q": "外弦图 vs 内弦图", "a": "外弦图（三角在外）：大正方形边长 a+b、小正方形边长 c。内弦图（三角在内）：大正方形边长 c、小正方形边长 |a-b|。记法：谁在外面，谁定大正方形边长。"}',
'{"q": "弦图求边长", "a": "经典题：大正方形面积=25 → c=5；小正方形面积=1 → |a-b|=1；a²+b²=25 且 a-b=1 → 解得 a=4、b=3。"}'
]
h = h[:fseg_end] + '},\n' + ',\n'.join(new_fcs) + h[fseg_end+1:]
print('3b. flashcards 追加', len(new_fcs), '张 OK')

# ---------- 4. errors 末尾追加 1 条弦图易错 ----------
ei = h.index('const errors=') + len('const errors=')
# errors 数组后紧跟 let curQ
em = re.search(r'\}\]\nlet curQ', h[ei:])
assert em, 'errors 闭合未找到'
eobj_end = ei + em.start()  # 指向原数组最后对象 } 的位置（不含）

new_es = '{"title": "弦图小正方形边长记错", "wrong": "以为外弦图中间小正方形边长是 a-b。", "right": "外弦图（三角在外）中间小正方形由斜边 c 构成，面积=c²；内弦图（三角在内）中间小正方形边长才是 |a-b|。记法：谁在外面谁定大正方形边长。"}'
h = h[:eobj_end] + '},\n' + new_es + h[eobj_end+1:]
print('4. errors 追加 1 条 OK')

# ---------- 5. 横幅同步 ----------
new_banner = '第1章 勾股定理 · 20 题 · 14 卡牌'
h = re.sub(r'第1章 勾股定理 · \d+ 题 · \d+ 卡牌', new_banner, h, count=1)
print('5. 横幅 OK')

open(P, 'w', encoding='utf-8').write(h)
print('DONE 写回')

# ---------- 校验 ----------
h2 = open(P, encoding='utf-8').read()
qi2 = h2.index('const questions=') + len('const questions=')
fi2 = h2.index('const flashcards=') + len('const flashcards=')
ei2 = h2.index('const errors=') + len('const errors=')
print('题:', len(re.findall(r'\{[^{]*"q"', h2[qi2:fi2-1])))
print('卡:', len(re.findall(r'\{[^{]*"q"', h2[fi2:ei2-1])))
print('错:', len(re.findall(r'\{[^{]*"title"', h2[ei2:])))
print('横幅:', re.findall(r'第1章 勾股定理[^<]*', h2))
