#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""_add_english_quiz_wrong.py — 英语小测错题录入赵若琳错题库（暑期C班双语第1讲）"""
from PIL import Image
import os

REPO = '/home/administrator/xuci-jiancha'
WB = f'{REPO}/wrong_bank.html'
IMG_SRC = '/home/administrator/.hermes/cache/images/img_c6ecacd5ddc8.jpg'
IMG_REL = 'uploads/wrong_bank/english_quiz_20260913.jpg'
IMG_DST = f'{REPO}/{IMG_REL}'

os.makedirs(os.path.dirname(IMG_DST), exist_ok=True)
im = Image.open(IMG_SRC)
w, h = im.size
nw = 1100
if w > nw:
    im = im.resize((nw, int(h * nw / w)), Image.LANCZOS)
im.save(IMG_DST, 'JPEG', quality=84, optimize=True)
print('图片:', im.size, os.path.getsize(IMG_DST), 'bytes')

CHAPTER = '英语C班双语第1讲（词汇与不定代词）'

items = [
    dict(key='englishquiz_20260913_q1', difficulty=2, error_reason='拼写错误',
         content='英语小测·汉译英：奇怪的；陌生的 adj. —— 学生写成 strang。',
         correct_answer='strange\n\n【解析】形容词“奇怪的、陌生的”= **strange**（/streɪndʒ/），学生漏写词尾字母 e。\n记忆链：strange（形容词）→ stranger（陌生人，+r）→ strangely（副词，奇怪地）。\n同类易错：breath（名词，一口气）vs breathe（动词，呼吸）——词性不同，拼写不同。',
         my_answer='strang（漏写词尾 e）',
         tags='英语,词汇,拼写,strange'),
    dict(key='englishquiz_20260913_q2', difficulty=3, error_reason='概念不清',
         content='不定代词填空：Of the two new films, ______ interests me much. I’d rather stay at home and read.',
         correct_answer='neither\n\n【解析】前文 **two** new films（两部电影）→ 表示“两者都不”用 **neither**（后接单数动词 interests ✓）。\n后半句“I’d rather stay at home and read”表明对两部电影都不感兴趣 → 故选 neither。\n⚠️ everything 表示“一切事物”，与“两部电影”的范围不符；若为三者以上“都不”则用 none。',
         my_answer='everything',
         tags='英语,不定代词,neither,两者,语境判断'),
    dict(key='englishquiz_20260913_q3', difficulty=4, error_reason='概念不清',
         content='不定代词辨析（两题）：① ______ Tom nor his parents have been to Paris, but they all dream of visiting it one day. ② —Which of the three dresses do you like? —______. They are either too long or too expensive.',
         correct_answer='① Neither　② None\n\n【辨析】\n• **neither**：两者都不（neither of the two；固定结构 Neither...nor）\n• **none**：三者或三者以上都不（none of the three，可指人或物）\n① 填 **Neither**——“Neither Tom nor his parents have been to Paris”，neither...nor 为固定关联连词，动词随就近主语 his parents 用 have。\n② 填 **None**——three dresses（三件）属三者以上；且 No one 只指人、也不能回答 which 对物的选择问。\n⚠️ 卷面红笔批注为 ①None／②Neither，与标准答案相反，建议课上再向老师确认一遍（上述为标准英语用法）。',
         my_answer='① 学生写 Neither（卷面红笔批注 None）② 学生写 No one（卷面红笔批注 Neither）',
         tags='英语,不定代词,neither,none,易混辨析'),
]

h = open(WB, encoding='utf-8').read()
anchor = "image_path:'uploads/wrong_bank/math_quiz_20260913.jpg'}\n];"
assert anchor in h, '未找到锚点'

def esc(s):
    return s.replace('\\', '\\\\').replace("'", "\\'").replace('\r', '').replace('\n', '\\n')

blocks = []
for it in items:
    blocks.append(
        "{key:'%s',subject:'英语',chapter:'%s',\n"
        "content:'%s',\n"
        "correct_answer:'%s',\n"
        "my_answer:'%s',\n"
        "error_reason:'%s',tags:'%s',source:'小测',difficulty:%d,\n"
        "image_path:'%s'}" % (
            it['key'], esc(CHAPTER), esc(it['content']), esc(it['correct_answer']),
            esc(it['my_answer']), esc(it['error_reason']), esc(it['tags']), it['difficulty'], IMG_REL))

new_block = "image_path:'uploads/wrong_bank/math_quiz_20260913.jpg'},\n" + ',\n'.join(blocks) + "\n];"
h = h.replace(anchor, new_block, 1)
open(WB, 'w', encoding='utf-8').write(h)
print('已写入 3 条英语错题')
