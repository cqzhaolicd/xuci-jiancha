#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""用 PIL 渲染汉译英答案 → 小体积多页 PDF + PNG（手机可看）"""
import sys, os
sys.path.insert(0, '/home/administrator/xuci-jiancha')
from PIL import Image, ImageDraw, ImageFont
from _make_answer_file import BLOCKS, TITLE, SUB, NOTE

OUT_PDF = '/home/administrator/若琳英语八上U1_过关单汉译英答案_20260919.pdf'
OUT_PNG = '/home/administrator/若琳英语八上U1_过关单汉译英答案_20260919.png'

REG = '/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc'
BOLD = '/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc'
DPI = 200
W, H, M = int(8.27 * DPI), int(11.69 * DPI), int(0.62 * DPI)   # A4

F_TITLE = ImageFont.truetype(BOLD, 46, index=0)
F_SUB = ImageFont.truetype(BOLD, 38, index=0)
F_NOTE = ImageFont.truetype(REG, 24, index=0)
F_H1 = ImageFont.truetype(BOLD, 34, index=0)
F_H2 = ImageFont.truetype(BOLD, 31, index=0)
F_BODY = ImageFont.truetype(REG, 30, index=0)
F_ANS = ImageFont.truetype(BOLD, 30, index=0)
F_TIP = ImageFont.truetype(REG, 27, index=0)

NAVY = (26, 38, 89)
BLUE = (38, 77, 153)
GREY = (115, 115, 115)
RED = (191, 31, 31)
DARK = (30, 30, 30)

pages = []
img = Image.new('RGB', (W, H), 'white')
dr = ImageDraw.Draw(img)
y = M


def newpage():
    global img, dr, y
    pages.append(img)
    img = Image.new('RGB', (W, H), 'white')
    dr = ImageDraw.Draw(img)
    y = M


def need(h):
    if y + h > H - M:
        newpage()


def wrap(text, font, maxw):
    lines, cur = [], ''
    for ch in text:
        if dr.textlength(cur + ch, font=font) <= maxw:
            cur += ch
        else:
            lines.append(cur)
            cur = ch
    if cur:
        lines.append(cur)
    return lines


# 标题区
dr.text((M, y), TITLE, font=F_TITLE, fill=NAVY); y += 54
dr.text((M, y), SUB, font=F_SUB, fill=BLUE); y += 46
dr.text((M, y), NOTE, font=F_NOTE, fill=GREY); y += 34
dr.line([(M, y), (W - M, y)], fill=(190, 200, 220), width=3); y += 30

for b in BLOCKS:
    k = b[0]
    if k == 'h1':
        need(90)
        dr.rectangle([M - 14, y - 10, W - M + 14, y + 52], fill=(238, 243, 252))
        dr.text((M, y), b[1], font=F_H1, fill=NAVY); y += 68
    elif k == 'h2':
        need(60)
        dr.text((M, y), b[1], font=F_H2, fill=(51, 64, 102)); y += 45
    elif k == 'pair':
        need(50)
        dr.text((M + 16, y), b[1], font=F_BODY, fill=DARK)
        ans = b[2]
        ax = M + int((W - 2 * M) * 0.52)
        ls = wrap(ans, F_ANS, W - M - ax)
        dr.text((ax, y), ls[0], font=F_ANS, fill=RED)
        y += 39
        for extra in ls[1:]:
            dr.text((ax, y), extra, font=F_ANS, fill=RED); y += 39
    elif k == 'sent':
        need(120)
        ls = wrap(b[1], F_BODY, W - 2 * M - 16)
        for ln in ls:
            dr.text((M + 16, y), ln, font=F_BODY, fill=DARK); y += 39
        body = '→ ' + b[2]
        ls2 = wrap(body, F_ANS, W - 2 * M - 40)
        for ln in ls2:
            dr.text((M + 40, y), ln, font=F_ANS, fill=RED); y += 39
        y += 8
    elif k == 'tip':
        need(44)
        dr.text((M + 16, y), b[1], font=F_TIP, fill=(90, 90, 90)); y += 38

pages.append(img)

# 写页码
total = len(pages)
for i, p in enumerate(pages, 1):
    d2 = ImageDraw.Draw(p)
    d2.text((W // 2 - 40, H - M + 10), f'{i} / {total}', font=F_NOTE, fill=GREY)

pages[0].save(OUT_PDF, 'PDF', resolution=DPI, save_all=True, append_images=pages[1:])
pages[0].save(OUT_PNG, 'PNG')
print('PDF:', OUT_PDF, round(os.path.getsize(OUT_PDF) / 1024), 'KB', f'({total} 页)')
print('PNG:', OUT_PNG, round(os.path.getsize(OUT_PNG) / 1024), 'KB')
