#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""裁剪讲义局部放大，用于确认横线位置"""
from PIL import Image

im = Image.open('/tmp/mpo_out/frame1.jpg')
crops = {
    'top_left': (0, 250, 1500, 1100),
    'top_right': (1350, 250, 2864, 1100),
    'mid_left': (0, 1500, 1500, 2350),
    'bottom_right': (1350, 3000, 2864, 3900),
}
for name, box in crops.items():
    c = im.crop(box)
    # 放大 1.4 倍便于查看
    c = c.resize((int(c.width * 1.4), int(c.height * 1.4)), Image.LANCZOS)
    p = f'/tmp/kl_crop_{name}.jpg'
    c.save(p, 'JPEG', quality=88)
    print(p, c.size)
