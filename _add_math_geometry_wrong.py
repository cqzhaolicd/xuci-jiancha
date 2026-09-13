#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""_add_math_geometry_wrong.py — 几何改错本大题录入赵若琳错题库"""
from PIL import Image
import os

REPO = '/home/administrator/xuci-jiancha'
WB = f'{REPO}/wrong_bank.html'
IMG_SRC = '/home/administrator/.hermes/cache/images/img_d7544fbc305d.jpg'
IMG_REL = 'uploads/wrong_bank/math_geometry_20260913.jpg'
IMG_DST = f'{REPO}/{IMG_REL}'

os.makedirs(os.path.dirname(IMG_DST), exist_ok=True)
im = Image.open(IMG_SRC)
w, h = im.size
nw = 1200
if w > nw:
    im = im.resize((nw, int(h * nw / w)), Image.LANCZOS)
im.save(IMG_DST, 'JPEG', quality=84, optimize=True)
print('图片:', im.size, os.path.getsize(IMG_DST), 'bytes')

CHAPTER = '几何证明综合（等腰·全等·辅助线）'

items = [
    dict(key='mathgeometry_20260913_q1', difficulty=5, error_reason='辅助线不会作',
         content='【改错本·几何证明综合题】在△ABC中，AB=AC，点E在AB上、点H在AC上，AE与BH交于点F，∠ABH=∠CAE。\n(1) 如图1，求证：∠AFB = 2∠ABC；\n(2) 如图2，连接FC，若E为AB中点，求证：AH = CH；\n(3) 如图3，在(2)的条件下，点D在BC的延长线上，∠ACD + 3∠EFC = 180°，若 AE+BF = 14，BH+AF = 16，求 HF 的长。',
         correct_answer='(1) 证明：∵ AB = AC ∴ ∠ABC = ∠ACB；设 ∠ABH = ∠CAE = x。\n在△ABF 中：∠AFB = 180° − ∠BAF − ∠ABF = 180° − (∠BAC − x) − (∠ABC − x)\n= 180° − ∠BAC − ∠ABC + 2x。又 ∠BAC = 180° − 2∠ABC，代入得 ∠AFB = 2∠ABC。\n\n(2) 证明（作垂线构造全等）：过 C 作 CG⊥AE 于 G、CP⊥FH 于 P，过 A 作 AM⊥BH 于 M。\n由 ∠ABH = ∠CAE 与 AB = AC 可证 △ABM ≌ △ACG（AAS）→ AM = AG；\n再证 △AMP ≌ △AGP（HL）→ AP 平分 ∠FAC，即 ∠CAG = ∠CAH。\n结合 ∠BAF = ∠BAC − ∠CAH、∠CAH = ∠BAF（等腰与角平分关系）→ ∠BAF = ½∠BAC；\n又 E 为 AB 中点 → AE = ½AB = ½AC，在△AEF 中推得 AH = CH。\n\n(3) HF = 2。\n关键：由 ∠ACD + 3∠EFC = 180° → ∠EFC = (180° − ∠ACD)/3，结合(1)(2)的结论可推出 **AF = AE**（△AEF 为等腰）。\n再利用 BH = BF + FH：\n(BH + AF) − (AE + BF) = (BF + FH + AF) − (AE + BF) = FH + (AF − AE) = FH\n∴ HF = 16 − 14 = **2**。',
         my_answer='（改错本订正）原错因：① 不会利用等腰三角形性质（AB=AC → 两底角相等）；② 忘了作垂线构造辅助线；③ 全等找对应角、对应边不严谨——“缺边或缺角就乱画”。',
         tags='数学,几何证明,等腰三角形,全等,辅助线,压轴题,改错本'),
]

h = open(WB, encoding='utf-8').read()
anchor = "image_path:'uploads/wrong_bank/english_quiz_20260913.jpg'}\n];"
assert anchor in h, '未找到锚点'

def esc(s):
    return s.replace('\\', '\\\\').replace("'", "\\'").replace('\r', '').replace('\n', '\\n')

blocks = []
for it in items:
    blocks.append(
        "{key:'%s',subject:'数学',chapter:'%s',\n"
        "content:'%s',\n"
        "correct_answer:'%s',\n"
        "my_answer:'%s',\n"
        "error_reason:'%s',tags:'%s',source:'改错本',difficulty:%d,\n"
        "image_path:'%s'}" % (
            it['key'], esc(CHAPTER), esc(it['content']), esc(it['correct_answer']),
            esc(it['my_answer']), esc(it['error_reason']), esc(it['tags']), it['difficulty'], IMG_REL))

new_block = "image_path:'uploads/wrong_bank/english_quiz_20260913.jpg'},\n" + ',\n'.join(blocks) + "\n];"
h = h.replace(anchor, new_block, 1)
open(WB, 'w', encoding='utf-8').write(h)
print('已写入 1 条几何错题')
