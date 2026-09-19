#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成汉译英答案 PDF + DOCX（人教版八上 Unit 1 过关单）"""
import fitz, os

OUT_PDF = '/home/administrator/若琳英语八上U1_过关单汉译英答案_20260919.pdf'
OUT_DOCX = '/home/administrator/若琳英语八上U1_过关单汉译英答案_20260919.docx'

REG = '/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc'
BOLD = '/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc'

TITLE = '人教版英语八年级上册 Unit 1《Happy Holiday》'
SUB = '过关单 · 汉译英答案（第五 ~ 第七课时）'
NOTE = '核对依据：人教版（2024新版）八上 Unit 1 词汇表 + Section B 课文原文'

# (kind, text)  kind: h1 节标题, h2 小节, item 条目(中文), ans 答案(英文), tip 提示
BLOCKS = [
    ('h1', '第五课时  Section B (2a~2c)'),
    ('h2', '一、重点单词'),
    ('pair', '1. 塔；塔楼  n.', 'tower'),
    ('pair', '2. 可能；可以  modal v.', 'might'),
    ('pair', '3. 预算  n. / 把……编入预算；精打细算  v.', 'budget'),
    ('pair', '4. 护照  n.', 'passport'),
    ('pair', '5. 健忘的；好忘事的  adj.', 'forgetful'),
    ('pair', '6. 远方的；遥远的  adj.', 'faraway'),
    ('h2', '二、词形变化'),
    ('pair', '平常的；有规律的  adj.', 'regular  →  有规律地 adv.  regularly'),
    ('h2', '三、重点语块'),
    ('pair', '1. 在阳光下', 'in the sun'),
    ('pair', '2. 超出预算', 'go over budget'),
    ('pair', '3. 处于平静、安宁的状态', 'at peace'),
    ('pair', '4. 回到你平常的生活状态', 'go back to your regular life'),
    ('h2', '四、重点句式'),
    ('sent', '1. 那令人惊叹的景色让他们露出笑容，忘却烦恼。',
     'The amazing scenery makes them smile and forget their worries.'),
    ('sent', '2. 然而，假期最重要的部分在于让身心得到休息。',
     'However, the most important part of a holiday is to rest your mind and body.'),
    ('h1', '第六、七课时  Section B (3a~Project & Reflecting)'),
    ('h2', '一、重点单词'),
    ('pair', '乡村；农村  n.', 'countryside'),
    ('h2', '二、词形变化'),
    ('sent', '1. 惊奇的；惊讶的  adj. surprised',
     '惊奇；惊讶 n. surprise  →  使感到意外 v. surprise  →  令人吃惊的；出人意料的 adj. surprising'),
    ('pair', '2. 鹿  n.  deer', '（复数）deer'),
    ('sent', '3. 很可能；大概  adv. probably', '很可能发生（或存在等）的 adj. probable'),
    ('h2', '三、重点语块'),
    ('pair', '1. 在乡下', 'in the countryside'),
    ('pair', '2. 在房子旁边', 'beside the house'),
    ('pair', '3. 发出噪音；弄出声响', 'make a noise'),
    ('pair', '4. 转身；翻转', 'turn around'),
    ('pair', '5. 做某事感到惊讶', 'be surprised to do sth'),
    ('pair', '6. 寻找', 'look for'),
    ('h2', '四、重点句式'),
    ('sent', '1. 去年秋天，我们一家乘火车去苏格兰度假了。',
     'Last autumn, my family took a train to Scotland for a holiday.'),
    ('sent', '2. 我拥有了一次多么美妙的经历啊！', 'What a wonderful experience I had!'),
    ('h2', '★ 易错提醒'),
    ('tip', '· “超出预算”用 go over budget，不能说 over the budget；'),
    ('tip', '· “处于平静、安宁的状态”是 at peace，介词固定用 at；'),
    ('tip', '· deer 单复数同形，复数不加 -s。'),
]


def build_pdf():
    doc = fitz.open()
    W, H, M = 595, 842, 56          # A4
    y = M
    page = doc.new_page(width=W, height=H)
    page.insert_font(fontname='cjk', fontfile=REG)
    page.insert_font(fontname='cjkb', fontfile=BOLD)

    def newpage():
        nonlocal page, y
        page = doc.new_page(width=W, height=H)
        page.insert_font(fontname='cjk', fontfile=REG)
        page.insert_font(fontname='cjkb', fontfile=BOLD)
        y = M

    def need(h):
        nonlocal y
        if y + h > H - M:
            newpage()

    # 标题
    page.insert_text((M, y + 14), TITLE, fontname='cjkb', fontsize=15, color=(0.1, 0.15, 0.35))
    y += 26
    page.insert_text((M, y + 8), SUB, fontname='cjkb', fontsize=12, color=(0.15, 0.3, 0.6))
    y += 18
    page.insert_text((M, y + 6), NOTE, fontname='cjk', fontsize=8.5, color=(0.45, 0.45, 0.45))
    y += 12
    page.draw_line(fitz.Point(M, y), fitz.Point(W - M, y), color=(0.7, 0.75, 0.85), width=1)
    y += 18

    for b in BLOCKS:
        kind = b[0]
        if kind == 'h1':
            need(34)
            page.draw_rect(fitz.Rect(M - 8, y - 12, W - M + 8, y + 12), color=(0.85, 0.89, 0.96),
                           fill=(0.94, 0.96, 0.99))
            page.insert_text((M, y + 5), b[1], fontname='cjkb', fontsize=11.5, color=(0.1, 0.2, 0.45))
            y += 30
        elif kind == 'h2':
            need(22)
            page.insert_text((M, y + 4), b[1], fontname='cjkb', fontsize=10.5, color=(0.2, 0.25, 0.4))
            y += 19
        elif kind == 'pair':
            need(20)
            page.insert_text((M + 10, y + 4), b[1], fontname='cjk', fontsize=10.5)
            ans = b[2]
            page.insert_text((360, y + 4), ans if len(ans) < 26 else ans[:26], fontname='cjkb',
                             fontsize=10.5, color=(0.75, 0.12, 0.12))
            if len(ans) >= 26:
                y += 16
                page.insert_text((360, y + 4), ans[26:], fontname='cjkb', fontsize=10.5,
                                 color=(0.75, 0.12, 0.12))
            y += 20
        elif kind == 'sent':
            need(46)
            page.insert_text((M + 10, y + 4), b[1], fontname='cjk', fontsize=10.5)
            y += 17
            body = '→ ' + b[2]
            page.insert_text((M + 26, y + 4), body if len(body) < 52 else body[:52], fontname='cjkb',
                             fontsize=10.5, color=(0.75, 0.12, 0.12))
            if len(body) >= 52:
                y += 16
                page.insert_text((M + 26, y + 4), body[52:], fontname='cjkb', fontsize=10.5,
                                 color=(0.75, 0.12, 0.12))
            y += 22
        elif kind == 'tip':
            need(18)
            page.insert_text((M + 10, y + 4), b[1], fontname='cjk', fontsize=9.5,
                             color=(0.35, 0.35, 0.35))
            y += 17
    doc.subset_fonts()
    doc.save(OUT_PDF, garbage=4, deflate=True)
    doc.close()
    print('PDF 已生成:', OUT_PDF, os.path.getsize(OUT_PDF), 'bytes')


def build_docx():
    from docx import Document
    from docx.shared import Pt, RGBColor
    from docx.oxml.ns import qn

    d = Document()
    st = d.styles['Normal']
    st.font.name = 'Times New Roman'
    st.font.size = Pt(10.5)
    st.element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')

    def para(text, size=10.5, bold=False, color=None, indent=0):
        p = d.add_paragraph()
        p.paragraph_format.left_indent = Pt(indent)
        r = p.add_run(text)
        r.font.size = Pt(size)
        r.bold = bold
        if color:
            r.font.color.rgb = RGBColor(*color)
        r.font.name = 'Times New Roman'
        r._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')
        return p

    para(TITLE, 15, True, (0x1A, 0x26, 0x59))
    para(SUB, 12, True, (0x26, 0x4D, 0x99))
    para(NOTE, 8.5, False, (0x73, 0x73, 0x73))
    for b in BLOCKS:
        if b[0] == 'h1':
            para(b[1], 11.5, True, (0x1A, 0x33, 0x73))
        elif b[0] == 'h2':
            para(b[1], 10.5, True, (0x33, 0x40, 0x66))
        elif b[0] == 'pair':
            p = d.add_paragraph()
            p.paragraph_format.left_indent = Pt(10)
            r1 = p.add_run(b[1] + '\t')
            r1.font.size = Pt(10.5)
            r2 = p.add_run(b[2])
            r2.bold = True
            r2.font.size = Pt(10.5)
            r2.font.color.rgb = RGBColor(0xBF, 0x1F, 0x1F)
        elif b[0] == 'sent':
            para(b[1], 10.5, False, None, 10)
            para('→ ' + b[2], 10.5, True, (0xBF, 0x1F, 0x1F), 26)
        elif b[0] == 'tip':
            para(b[1], 9.5, False, (0x59, 0x59, 0x59), 10)
    d.save(OUT_DOCX)
    print('DOCX 已生成:', OUT_DOCX, os.path.getsize(OUT_DOCX), 'bytes')


if __name__ == '__main__':
    try:
        build_pdf()
    except Exception as e:
        print('PDF 生成失败:', e)
    build_docx()
