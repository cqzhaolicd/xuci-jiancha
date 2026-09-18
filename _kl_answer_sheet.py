#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成讲义答案版图片：中文提示 + 画线处填写英文翻译（红色）"""
from PIL import Image, ImageDraw, ImageFont
import os

CN = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
CNB = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
F_TITLE = ImageFont.truetype(CNB, 62, index=2)
F_SEC = ImageFont.truetype(CNB, 46, index=2)
F_CN = ImageFont.truetype(CN, 40, index=2)
F_EN = ImageFont.truetype(CNB, 42, index=2)
F_EN_S = ImageFont.truetype(CNB, 36, index=2)

LEFT = [
    ('sec', '重点单词'),
    ('item', '1. 广场；正方形 n.／正方形的；平方的 adj.', 'square'),
    ('item', '2. 在……期间 prep.', 'during'),
    ('item', '3. 胜利；成功 n.', 'victory'),
    ('item', '4. 反对；与……相反；紧靠 prep.', 'against'),
    ('item', '5. 艺术作品；插图 n.', 'artwork'),
    ('item', '6. 眼泪；泪水 n.', 'tear'),
    ('item', '7. 提醒；使想起 v.', 'remind'),
    ('item', '8. 正午；中午 n.', 'noon'),
    ('item', '9. 地下铁道系统 n.', 'subway'),
    ('item', '10. 车站；所；局 n.', 'station'),
    ('item', '11. 王宫；宫殿 n.', 'palace'),
    ('item', '12. 手风琴 n.', 'accordion'),
    ('sec', '词形变化'),
    ('item', '1. 俄罗斯的；俄罗斯人的 adj.／俄罗斯人；俄语 n.', 'Russian'),
    ('sub', '→ 俄罗斯 n.', 'Russia'),
    ('item', '2. 战斗；搏斗；斗争 n.／打仗；打架 v.', 'fight'),
    ('sub', '→ （过去式）', 'fought'),
    ('item', '3. 和平；太平 n.', 'peace'),
    ('sub', '→ 和平的；安静的；平静的 adj.', 'peaceful'),
    ('item', '4. 容易地；轻易地 adv.', 'easily'),
    ('sub', '→ 容易的；轻易的 adj.', 'easy'),
    ('item', '5. 忘记；遗忘 v.', 'forget'),
    ('sub', '→ （过去式）', 'forgot'),
    ('sub', '→ 健忘的；好忘事的 adj.', 'forgetful'),
    ('item', '6. 恶心的；生病的 adj.', 'sick'),
]

RIGHT = [
    ('sec', '重点语块'),
    ('item', '1. 假期/旅行经历', 'travel experience'),
    ('item', '2. 做……感到兴奋', 'be excited about doing sth.'),
    ('item', '3. 与……作战；与……作斗争', 'fight against / with'),
    ('item', '4. 走过大厅', 'walk through the hall'),
    ('item', '5. 导游', 'tour guide'),
    ('item', '6. 数以千计的；成千上万的', 'thousands of'),
    ('item', '7. 想要做某事', 'want to do sth.'),
    ('item', '8. 感到恶心；感到不舒服', 'feel sick'),
    ('item', '9. 睡个好觉', 'have/get a good sleep'),
    ('item', '10. 清新凉爽', 'fresh and cool'),
    ('item', '11. 四处逛逛；到处旅行', 'travel around'),
    ('item', '12. 地铁站', 'subway station'),
    ('item', '13. 拿出；取出', 'take out'),
    ('item', '14. 聚会；相聚', 'get together'),
    ('sec', '重点句式'),
    ('item', '1. 在一个展厅里，我看到了一幅作品，上面有成千上万滴', None),
    ('sub', '玻璃“眼泪”正在落下。', None),
    ('ans', 'In one of the halls, I saw a work of art with thousands', ''),
    ('ans', 'of glass "tears" falling down.', ''),
    ('item', '2. 它提醒我们，战争是可怕的，和平来之不易。', None),
    ('ans', 'It reminds us that war is terrible and peace', ''),
    ('ans', "doesn't come easily.", ''),
    ('item', '3. 我觉得我好像走在一座宫殿里。', None),
    ('ans', 'I felt like I was walking in a palace.', ''),
]

W = 2900
COL_W = 1330
PAD = 40
TOP = 150
LINE_H = 118
SEC_GAP = 30

img = Image.new('RGB', (W, 6000), 'white')
d = ImageDraw.Draw(img)

# 标题
d.text((PAD, 40), '第四课时 Section B (1a~1d) · 词汇与句式（答案版）', font=F_TITLE, fill=(20, 20, 20))
d.line([(PAD, 122), (W - PAD, 122)], fill=(60, 60, 60), width=3)

def draw_col(items, x0):
    y = TOP
    for kind, *rest in items:
        if kind == 'sec':
            d.text((x0, y), rest[0], font=F_SEC, fill=(11, 61, 145))
            tw = d.textlength(rest[0], font=F_SEC)
            d.line([(x0, y + 60), (x0 + tw + 20, y + 60)], fill=(11, 61, 145), width=3)
            y += LINE_H + SEC_GAP
        elif kind == 'item':
            cn, en = rest[0], rest[1]
            d.text((x0, y), cn, font=F_CN, fill=(25, 25, 25))
            y += 70
            if en is not None:
                d.text((x0 + 30, y - 8), en, font=F_EN, fill=(200, 20, 20))
                tw = d.textlength(en, font=F_EN)
                lw = max(260, tw + 40)
                d.line([(x0 + 26, y + 48), (x0 + 26 + lw, y + 48)], fill=(120, 120, 120), width=3)
                y += LINE_H - 20
            else:
                y += 10
        elif kind == 'sub':
            cn, en = rest[0], rest[1]
            d.text((x0 + 30, y), cn, font=F_CN, fill=(25, 25, 25))
            y += 62
            if en is None:
                y += 10
            else:
                d.text((x0 + 60, y - 6), en, font=F_EN_S, fill=(200, 20, 20))
                tw = d.textlength(en, font=F_EN_S)
                lw = max(220, tw + 36)
                d.line([(x0 + 56, y + 42), (x0 + 56 + lw, y + 42)], fill=(120, 120, 120), width=3)
                y += LINE_H - 30
        elif kind == 'ans':
            txt = rest[0]
            d.text((x0 + 30, y - 6), txt, font=F_EN, fill=(200, 20, 20))
            y += 60
    return y

yl = draw_col(LEFT, PAD)
yr = draw_col(RIGHT, PAD + COL_W + 90)
# 中缝分隔线
d.line([(PAD + COL_W + 45, TOP - 20), (PAD + COL_W + 45, max(yl, yr) + 20)], fill=(200, 200, 210), width=3)

H = max(yl, yr) + 90
img = img.crop((0, 0, W, H))
out = '/tmp/kl_answer_sheet.jpg'
img.save(out, 'JPEG', quality=90)
print('生成:', out, img.size, os.path.getsize(out), 'bytes')
