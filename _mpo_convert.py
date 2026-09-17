#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把 MPO 图片转成标准 JPEG（支持多帧提取）"""
from PIL import Image
import os

src = '/home/administrator/.hermes/cache/images/img_916c919307db.jpg'
outdir = '/tmp/mpo_out'
os.makedirs(outdir, exist_ok=True)
im = Image.open(src)
print('格式:', im.format, '尺寸:', im.size, '模式:', im.mode)
n = getattr(im, 'n_frames', 1)
print('帧数:', n)
for i in range(min(n, 6)):
    try:
        im.seek(i)
    except EOFError:
        break
    frame = im.convert('RGB')
    p = f'{outdir}/frame{i+1}.jpg'
    frame.save(p, 'JPEG', quality=92)
    print(p, frame.size, os.path.getsize(p), 'bytes')
