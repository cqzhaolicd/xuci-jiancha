#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""在「带答案全文」tab 的每个英文段落后插入一行中文大意（老师/老板要求 2026-09-11）"""
FN = 'english26q_read1_interactive.html'
h = open(FN, encoding='utf-8').read()

START = '<div id="tab-quiz" class="tab-content">'
END = '<div class="quiz-mode-bar" id="quizModeBar">'
i, j = h.find(START), h.find(END)
assert i > 0 and j > i, 'tab2 区间未找到'
seg = h[i:j]

GISTS = [
    ('depend on</strong> it too much? The government',
     '如果经常和 AI 聊天，你会不会把它当成真朋友、过度依赖？——政府已为 AI 陪伴机器人出台新规。'),
    ('Wang Zhechen from Fudan University told <em>China Daily</em>.',
     'AI 陪伴机器人（玩具或 App 形态）已融入很多人的日常，它们总是友好又有耐心；但有些年轻人花大量时间陪它，反而疏远了现实中的朋友。'),
    ('expert Liu Xiaochun explained to <em>China Daily</em>.',
     '新规要求：AI 不得鼓励用户长时间使用，连续两小时后必须弹窗提醒「休息一下」，并且要讲清楚——这是机器，不是真人。'),
    ('<strong>Now, the rules stop this.</strong>',
     '新规还要求 AI 安全、友善：不许撒谎、泄露隐私或危害国家安全；过去 AI 会用你的情绪信息推送玩具、糖果广告，现在被规则叫停。'),
    ('At the same time, AI won\'t give you unsafe advice just to make you happy.',
     '未满 18 岁打开 AI App 会自动开启青少年模式，家长可以查看聊天时长；AI 也不能为了讨好你而给出不安全的建议。'),
]

STYLE = 'margin:.15rem 0 .75rem;color:#8a94a6;font-size:.86rem;line-height:1.7'
added = 0
for anchor, gist in GISTS:
    k = seg.find(anchor)
    assert k > 0, f'anchor not found: {anchor[:40]}'
    p_end = seg.find('</p>', k)
    assert p_end > 0, f'</p> not found after: {anchor[:40]}'
    insert = f'\n      <p style="{STYLE}">💡 <strong>中文大意</strong>：{gist}</p>'
    seg = seg[:p_end + 4] + insert + seg[p_end + 4:]
    added += 1

h = h[:i] + seg + h[j:]
h = h.replace('<i class="fas fa-clipboard-check" style="color:#27ae60"></i> 带答案全文 · 文章 + 题目 + 答案 + 解析',
              '<i class="fas fa-clipboard-check" style="color:#27ae60"></i> 带答案全文 · 文章（含中文大意）+ 题目 + 答案 + 解析', 1)
h = h.replace('<h3 style="margin:0 0 .5rem;font-size:1.05rem;color:#667eea">一、文章原文（含答案版标注）</h3>',
              '<h3 style="margin:0 0 .5rem;font-size:1.05rem;color:#667eea">一、文章原文（含答案版标注 + 每段中文大意）</h3>', 1)
open(FN, 'w', encoding='utf-8').write(h)
print(f'已插入 {added} 行中文大意 | 文件 {len(h)} bytes')
