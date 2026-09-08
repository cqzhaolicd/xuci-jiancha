#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
_patch_lql_index.py — liuqiuling_index.html 预习闯关分区: 八上 → 九上 + 新增化学闯关
"""
import re, os

P = '/home/administrator/xuci-jiancha/liuqiuling_index.html'
s = open(P, encoding='utf-8').read()
log = []

def rep(old, new, tag):
    global s
    n = s.count(old)
    if n == 0:
        raise SystemExit(f'❌ 未找到: {tag}')
    s = s.replace(old, new)
    log.append(f'{tag}: {n}')

# 1) 分区标题
rep("renderSection('预习闯关 · 八上'", "renderSection('预习闯关 · 九上'", '分区标题九上')

# 2) 4 卡 URL 与描述
cards = {
    'math8': ('math9', '北师大八上 · 勾股定理→一次函数', '人教九上 · 一元二次方程→概率初步'),
    'physics8': ('physics9', '人教八上 · 机械运动→质量密度', '人教九全 · 内能→电功率'),
    'chinese8': ('chinese9', '统编八上 · 新闻→文言文', '统编九上 · 诗歌→古典小说'),
    'english8': ('english9', '人教八上 · 假期→条件句', '人教九全 · Unit1-6 语法直通'),
}
for old_sfx, (new_sfx, old_desc, new_desc) in cards.items():
    rep(f'lql_preview_challenge_{old_sfx}.html', f'lql_preview_challenge_{new_sfx}.html', f'卡{old_sfx}→{new_sfx}')
    rep(old_desc, new_desc, f'desc {new_sfx}')

# 3) 新增化学闯关卡: 在英语卡后面追加
anchor = '''      <a href="lql_preview_challenge_english9.html" class="tool-card t-add ${isLearned('lql_preview_challenge_english9.html') ? 'learned' : ''}">
        <span class="learn-badge" style="display:${isLearned('lql_preview_challenge_english9.html') ? 'inline-flex' : 'none'}"><i class="fas fa-check"></i> 已学习</span>
        <div class="t-icon"><i class="fas fa-language"></i></div>
        <div class="t-name">英语闯关</div>
        <div class="t-desc">人教九全 · Unit1-6 语法直通</div>
        ${learnedBtn('lql_preview_challenge_english9.html')}
      </a>'''
chem_card = anchor + '''
      <a href="lql_preview_challenge_chemistry9.html" class="tool-card t-analysis ${isLearned('lql_preview_challenge_chemistry9.html') ? 'learned' : ''}">
        <span class="learn-badge" style="display:${isLearned('lql_preview_challenge_chemistry9.html') ? 'inline-flex' : 'none'}"><i class="fas fa-check"></i> 已学习</span>
        <div class="t-icon"><i class="fas fa-flask"></i></div>
        <div class="t-name">化学闯关</div>
        <div class="t-desc">人教九上 · 走进化学世界→碳和碳的氧化物</div>
        ${learnedBtn('lql_preview_challenge_chemistry9.html')}
      </a>'''
rep(anchor, chem_card, '新增化学闯关卡')

open(P, 'w', encoding='utf-8').write(s)
print('✅ 入口已更新')
for l in log:
    print(' ', l)
