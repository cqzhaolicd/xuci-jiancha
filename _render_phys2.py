#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""渲染备课笔记 PDF 为 PNG（供识别）"""
import fitz, os

src = '/home/administrator/.hermes/cache/documents/doc_1123e37c7fe9_初二秋季备课笔记2.pdf'
outdir = '/tmp/phys2_pages'
os.makedirs(outdir, exist_ok=True)
d = fitz.open(src)
for i, p in enumerate(d):
    pix = p.get_pixmap(dpi=200)
    out = f'{outdir}/page{i+1}.png'
    pix.save(out)
    print(out, pix.width, 'x', pix.height, os.path.getsize(out), 'bytes')
d.close()
