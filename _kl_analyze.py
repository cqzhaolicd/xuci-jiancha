#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""分析讲义图片版式：检测水平横线（填空线）位置，识别分栏结构"""
from PIL import Image
import numpy as np, os, json

src = '/tmp/mpo_out/frame1.jpg'
im = Image.open(src).convert('L')
w, h = im.size
a = np.array(im)
print('尺寸:', w, h)

# 横线检测：行像素中"较暗"比例高的行（横线通常较长且颜色偏灰/黑）
dark = (a < 150).astype(np.uint8)
row_ratio = dark.sum(axis=1) / w
cand = [(y, round(float(row_ratio[y]), 3)) for y in range(h) if row_ratio[y] > 0.30]
print('候选横线行数:', len(cand))
# 聚类相邻行
groups = []
for y, r in cand:
    if groups and y - groups[-1][-1][0] <= 3:
        groups[-1].append((y, r))
    else:
        groups.append([(y, r)])
lines = []
for g in groups:
    ys = [y for y, _ in g]
    y0, y1 = min(ys), max(ys)
    seg = dark[(y0 + y1) // 2]
    xs = np.where(seg)[0]
    if len(xs) > w * 0.05:
        lines.append({'y': (y0 + y1) // 2, 'x0': int(xs.min()), 'x1': int(xs.max()), 'len': int(len(xs))})
print('检测到水平线:', len(lines))
for l in lines[:40]:
    print(l)
json.dump(lines, open('/tmp/kl_lines.json', 'w'), ensure_ascii=False)
