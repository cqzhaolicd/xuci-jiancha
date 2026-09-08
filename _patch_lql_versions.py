#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""刘秋灵入口 liuqiuling_index.html 版本修正:
1) GRADE9 数学 → 北师大章 (9上6章 + 9下3章)
2) GRADE9 物理 → 沪科版章 (12-20章)
3) 移除 8年级上备用区 物理 (人教, 与沪科不符; 无沪科素材暂不配)
4) 移除 7年级备用区 物理课堂笔记
5) section 标题去掉误导性"(人教版教材以课本为准)"
"""
P = '/home/administrator/xuci-jiancha/liuqiuling_index.html'
s = open(P, encoding='utf-8').read()
log = []
def rep(old, new, tag):
    global s
    n = s.count(old)
    if n == 0:
        raise SystemExit(f'❌ 未找到: {tag}\n{old[:100]}...')
    s = s.replace(old, new)
    log.append(f'{tag}: {n}')

# 1) 数学北师 (9上6章+9下3章)
old_math = "'数学': ['第21章 一元二次方程(九上)', '第22章 二次函数(九上)', '第23章 旋转(九上)', '第24章 圆(九上)', '第25章 概率初步(九上)', '第26章 反比例函数(九下)', '第27章 相似(九下)', '第28章 锐角三角函数(九下)', '第29章 投影与视图(九下)'],"
new_math = "'数学': ['第1章 特殊平行四边形(九上)', '第2章 一元二次方程(九上)', '第3章 概率的进一步认识(九上)', '第4章 图形的相似(九上)', '第5章 投影与视图(九上)', '第6章 反比例函数(九上)', '九下 第1章 直角三角形的边角关系', '九下 第2章 二次函数', '九下 第3章 圆'],"
rep(old_math, new_math, '数学→北师大章目')

# 2) 物理沪科 (九全 12-20章)
old_phy = "'物理': ['第13章 内能', '第14章 内能的利用', '第15章 电流和电路', '第16章 电压 电阻', '第17章 欧姆定律', '第18章 电功率', '第19章 生活用电', '第20章 电与磁', '第21章 信息的传递', '第22章 能源与可持续发展'],"
new_phy = "'物理': ['第12章 温度与物态变化', '第13章 内能与热机', '第14章 了解电路', '第15章 探究电路', '第16章 电流做功与电功率', '第17章 从指南针到磁浮列车', '第18章 电能从哪里来', '第19章 走进信息时代', '第20章 能源、材料与社会'],"
rep(old_phy, new_phy, '物理→沪科章目')

# 3) 8年级上备用区移除物理块 (整块含7 lectures)
i0 = s.find("    { id: 'g8-物理', name: '物理', icon: 'fa-flask', cls: 'subject-physics', lectures: [")
i1 = s.find("    { id: 'g8-生物'", i0)
assert i0 > 0 and i1 > i0, 'g8-物理块边界未找到'
s = s[:i0] + s[i1:]
log.append('移除8年级上备用物理块(人教→沪科不匹配)')

# 4) 7年级备用区移除物理
rep("    G7('物理', 'lql_物理_7grade_interactive.html'),\n", '', '移除7年级备用物理')

# 5) section 标题
rep("renderSection('学校学习 · 人教版教材(以课本为准)'", "renderSection('学校学习 · 教材按校版本'", 'section标题修正')

open(P, 'w', encoding='utf-8').write(s)
print('✅ 版本修正完成')
for l in log:
    print(' ', l)
