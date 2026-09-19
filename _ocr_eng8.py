#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""OCR 人教版英语八上课本，定位含预算/塔楼/护照等的 Section B 课文页"""
import fitz, io, sys
import numpy as np
from PIL import Image
import easyocr

PDF = '/home/administrator/textbooks8/英语_人教/英语八上.pdf'
START, END = int(sys.argv[1]) if len(sys.argv) > 1 else 11, int(sys.argv[2]) if len(sys.argv) > 2 else 24

doc = fitz.open(PDF)
reader = easyocr.Reader(['en', 'ch_sim'], gpu=False, verbose=False)
HITS = ['budget', 'tower', 'passport', 'scotland', 'scenery', 'forgetful', 'faraway']
for i in range(START, min(END, len(doc))):
    try:
        pix = doc[i].get_pixmap(dpi=190)
        img = Image.open(io.BytesIO(pix.tobytes('png'))).convert('RGB')
        res = reader.readtext(np.array(img), detail=0, paragraph=True)
        txt = '\n'.join(res)
        open(f'/tmp/oce_pg{i}.txt', 'w', encoding='utf-8').write(txt)
        low = txt.lower()
        hit = [k for k in HITS if k in low]
        print(f'--- PDF页 {i} ({len(txt)} 字符) 命中: {hit}', flush=True)
        if hit:
            print(txt[:2500], flush=True)
    except Exception as e:
        print(f'页 {i} 失败: {e}', flush=True)
print('OCR 完成', flush=True)
