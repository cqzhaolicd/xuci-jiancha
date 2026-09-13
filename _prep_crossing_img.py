#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""压缩过街安全题图片到 uploads/wrong_bank/"""
from PIL import Image
import os

src = '/home/administrator/.hermes/cache/images/img_274a1e26fc57.jpg'
dst = '/home/administrator/xuci-jiancha/uploads/wrong_bank/physics_crossing_20260913.jpg'
os.makedirs(os.path.dirname(dst), exist_ok=True)
im = Image.open(src)
w, h = im.size
nw = 1000
im2 = im.resize((nw, int(h * nw / w)), Image.LANCZOS) if w > nw else im
im2.save(dst, 'JPEG', quality=82, optimize=True)
print('原图:', (w, h), '→ 输出:', os.path.getsize(dst), 'bytes,', im2.size)
