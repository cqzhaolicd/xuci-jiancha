#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""检测讲义中的填空横线（长连续暗像素段）"""
from PIL import Image
import numpy as np, json

im = Image.open('/tmp/mpo_out/frame1.jpg').convert('L')
w, h = im.size
a = np.array(im)
dark = a < 200

rows = []
for y in range(h):
    row = dark[y]
    if row.sum() < 100:
        continue
    # 最长连续 True 段
    idx = np.where(row)[0]
    splits = np.split(idx, np.where(np.diff(idx) > 2)[0] + 1)
    longest = max(splits, key=len)
    if len(longest) >= 120 and len(longest) / max(1, row.sum()) > 0.55:
        rows.append({'y': int(y), 'x0': int(longest[0]), 'x1': int(longest[-1]), 'len': int(len(longest))})

# 合并相邻 y（同一横线可能占几行像素）
merged = []
for r in rows:
    if merged and r['y'] - merged[-1]['y'] <= 4 and abs(r['x0'] - merged[-1]['x0']) < 200:
        m = merged[-1]
        merged[-1] = {'y': (m['y'] + r['y']) // 2,
                      'x0': min(m['x0'], r['x0']), 'x1': max(m['x1'], r['x1']),
                      'len': max(m['len'], r['len'])}
    else:
        merged.append(dict(r))

print('检测到横线:', len(merged))
for i, l in enumerate(merged):
    col = 'L' if l['x0'] < w * 0.45 else ('R' if l['x0'] > w * 0.45 else 'M')
    print(f"{i+1:3d} y={l['y']:5d} x={l['x0']:5d}-{l['x1']:5d} len={l['len']:5d} {col}")
json.dump(merged, open('/tmp/kl_lines2.json', 'w'), ensure_ascii=False)
