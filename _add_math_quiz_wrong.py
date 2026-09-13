#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""_add_math_quiz_wrong.py — 把 2026秋初二博学班第1次小测（数学，4/10）6 题录入赵若琳错题库"""
from PIL import Image
import os, re

REPO = '/home/administrator/xuci-jiancha'
WB = f'{REPO}/wrong_bank.html'
IMG_SRC = '/home/administrator/.hermes/cache/images/img_fe4d8a4806c9.jpg'
IMG_REL = 'uploads/wrong_bank/math_quiz_20260913.jpg'
IMG_DST = f'{REPO}/{IMG_REL}'

os.makedirs(os.path.dirname(IMG_DST), exist_ok=True)
im = Image.open(IMG_SRC)
w, h = im.size
nw = 1100
if w > nw:
    im = im.resize((nw, int(h * nw / w)), Image.LANCZOS)
im.save(IMG_DST, 'JPEG', quality=84, optimize=True)
print('图片:', im.size, os.path.getsize(IMG_DST), 'bytes')

CHAPTER = '第2讲小测（二次根式与代数式求值）'
COMMON = f"subject:'数学',chapter:'{CHAPTER}',source:'小测',difficulty:4,image_path:'{IMG_REL}'"

items = [
    dict(key='mathquiz_20260913_q1', difficulty=4,
         content='1.（2026秋初二博学班第1次小测·第2讲用）已知 √((x-10)²) + (√(8-x))² = 20，y = √(m+15) + √(2m-2) + √(1-m)，则 y+x 的平方根是 ____。',
         correct_answer='±√3\n\n【解析】由 √(8-x) 有意义得 x ≤ 8，故 |x-10| = 10-x：\n(10-x) + (8-x) = 20 → 18-2x = 20 → x = -1。\n由 y 的三个根式都有意义：m+15≥0、2m-2≥0、1-m≥0 → m≥1 且 m≤1 → m = 1，代入 y = √16+√0+√0 = 4。\n所以 y+x = 4+(-1) = 3，其平方根为 **±√3**。',
         my_answer='±√2（x 求解出错 / 根式有意义条件没抓准）',
         error_reason='概念不清', tags='数学,二次根式,绝对值化简,根式有意义,平方根,取值范围'),
    dict(key='mathquiz_20260913_q2', difficulty=4,
         content='2. 如图（数轴：a 在 -2 与 -1 之间且靠近 -2，b 在 1 与 2 之间且靠近 1），化简 √((a+b)²) - √((a-1)²) + ∛((b-2)³) 的结果是 ____。',
         correct_answer='-3\n\n【解析】由数轴可知 a ∈ (-2,-1)、b ∈ (1,2)，且 |a| > |b| → a+b < 0；又 a-1 < 0、b-2 < 0。\n原式 = |a+b| - |a-1| + (b-2) = -(a+b) - (1-a) + (b-2) = -3。\n（注意：立方根 ∛((b-2)³) = b-2，符号与被开方数一致，不加绝对值！）',
         my_answer='-2b+2a（没有先判断 a+b 的符号，∛ 的处理也不对）',
         error_reason='思路错误', tags='数学,数轴,绝对值化简,立方根,分类讨论'),
    dict(key='mathquiz_20260913_q3', difficulty=4,
         content='3. 计算：(1) √(4-2√3) = ____；(2) √(9+6√2) = ____；(3) √(4-√7) = ____。',
         correct_answer='(1) √3-1　(2) 3+√6　(3) (√14-√2)/2\n\n【解析】都是"完全平方开方"（√(a±2√b) 型）：\n(1) 4-2√3 = (√3-1)² → √(4-2√3) = √3-1（≈0.732）。\n(2) 9+6√2 = 9+2·3√2 = (3+√6)² → √(9+6√2) = 3+√6（≈5.449）。\n(3) 4-√7 = 4-2·(√7/2)：设 (√x-√y)² = x+y-2√(xy) = 4-√7 → x+y=4、4xy=7 → x、y = (4±3)/2? 直接配方：(√14-√2)/2 的平方 = (14+2-2√28)/4 = (16-4√7)/4 = 4-√7 ✓，故 √(4-√7) = (√14-√2)/2（≈1.164）。',
         my_answer='√3-1；(√6-3 或 √6+3 混写)；2（第3空）',
         error_reason='公式应用错误', tags='数学,二次根式,完全平方公式,配方开方'),
    dict(key='mathquiz_20260913_q4', difficulty=4,
         content='4. 已知 a+b = -4，ab = 3，则 √(a/b) + √(b/a) 的值为 ____。',
         correct_answer='4√3/3\n\n【解析】由 ab = 3 > 0、a+b = -4 < 0 → a、b 同为负数（a=-1, b=-3），故 √(a/b) = |a|/√(ab)、√(b/a) = |b|/√(ab)。\n√(a/b) + √(b/a) = (|a|+|b|)/√(ab) = -(a+b)/√(ab) = 4/√3 = **4√3/3**。\n（注意：不能直接用 (a+b)/√(ab)，符号会错。）',
         my_answer='10√3/3（把 a²+b² = 10 当作 a+b 用了）',
         error_reason='公式应用错误', tags='数学,二次根式,韦达定理,符号判断'),
    dict(key='mathquiz_20260913_q5', difficulty=4,
         content='5. 已知 √(13+x) - √(11-x) = 4，则 √(13+x) + √(11-x) = ____。',
         correct_answer='4√2\n\n【解析】设 A = √(13+x)、B = √(11-x)，则：\nA² + B² = (13+x) + (11-x) = 24，A - B = 4。\n由 (A-B)² = A² + B² - 2AB → 16 = 24 - 2AB → AB = 4。\n再由 (A+B)² = A² + B² + 2AB = 24 + 8 = 32 → A+B = **4√2**。',
         my_answer='48（第二步 2AB 算成 -8，又把 (A+B)² 算成 16+32）',
         error_reason='计算错误', tags='数学,二次根式,整体代换,完全平方变形'),
    dict(key='mathquiz_20260913_q6', difficulty=5,
         content='6. 若 a = (√2+1)/(√2-1)，求 2a³ - 13a² + 8a + 5 的值。',
         correct_answer='6\n\n【解析】a = (√2+1)/(√2-1) = (√2+1)²/((√2)²-1) = 3+2√2（分母有理化）。\na² = (3+2√2)² = 17+12√2；a³ = a·a² = (3+2√2)(17+12√2) = 99+70√2。\n代入：2(99+70√2) - 13(17+12√2) + 8(3+2√2) + 5\n= (198-221+24+5) + (140-156+16)√2 = 6 + 0 = **6**。\n（技巧：也可用 a² - 6a + 1 = 0 降次简化。）',
         my_answer='56√2-76（分母有理化后 a 的化简出错，后续计算量过大）',
         error_reason='计算错误', tags='数学,二次根式,分母有理化,代数式求值,降次'),
]

h = open(WB, encoding='utf-8').read()
anchor = "image_path:'uploads/wrong_bank/physics_crossing_20260913.jpg'}\n];"
assert anchor in h, '未找到锚点'

def esc(s):
    """转义为 JS 单引号字符串安全形式"""
    return s.replace('\\', '\\\\').replace("'", "\\'").replace('\r', '').replace('\n', '\\n')

blocks = []
for it in items:
    blocks.append(
        "{key:'%s',subject:'数学',chapter:'%s',\n"
        "content:'%s',\n"
        "correct_answer:'%s',\n"
        "my_answer:'%s',\n"
        "error_reason:'%s',tags:'%s',source:'小测',difficulty:%d,\n"
        "image_path:'%s'}" % (
            it['key'], esc(CHAPTER), esc(it['content']), esc(it['correct_answer']),
            esc(it['my_answer']), esc(it['error_reason']), esc(it['tags']), it['difficulty'], IMG_REL))

new_block = "image_path:'uploads/wrong_bank/physics_crossing_20260913.jpg'},\n" + ',\n'.join(blocks) + "\n];"
h = h.replace(anchor, new_block, 1)
open(WB, 'w', encoding='utf-8').write(h)
print('已写入 6 条数学错题')
