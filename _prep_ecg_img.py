#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""压缩错题图片并放入 uploads/wrong_bank/"""
from PIL import Image
import os

src = '/home/administrator/.hermes/cache/images/img_5d918dc8b3b2.jpg'
dst = '/home/administrator/xuci-jiancha/uploads/wrong_bank/physics_ecg_20260913.jpg'
os.makedirs(os.path.dirname(dst), exist_ok=True)
im = Image.open(src)
w, h = im.size
nw = 1000
im2 = im.resize((nw, int(h * nw / w)), Image.LANCZOS)
im2.save(dst, 'JPEG', quality=82, optimize=True)
print('输出:', os.path.getsize(dst), 'bytes,', im2.size)
