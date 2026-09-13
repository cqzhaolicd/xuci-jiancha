#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""_build_english_lesson3.py — 英语课 智能设备阅读 + 不定代词/比较级巩固
来源: 20260912 课堂录音笔记（英语部分）
基座: english_lesson2_interactive.html
输出: english_lesson3_interactive.html
"""
import re, json, subprocess

REPO = '/home/administrator/xuci-jiancha'
BASE_F = f'{REPO}/english_lesson2_interactive.html'
OUT_F = f'{REPO}/english_lesson3_interactive.html'

KNOW = [
    ("c1", "📐 智能设备阅读：总分总结构", [
        "首段：以<strong class=\"hl\">科技快速发展的社会背景</strong>引出核心话题 <strong class=\"hl\">Smart devices（智能设备）</strong>",
        "中间三段：分别介绍<strong class=\"hl\">智能安全设备、智能温度控制器、智能音箱</strong>三类产品",
        "尾段：总结作者对智能设备的<strong class=\"hl\">看法 + 对未来智能家居的期待</strong>",
    ]),
    ("c2", "✨ 高分句型（作文可套用）", [
        "<strong class=\"hl\">With the rapid development of science and technology</strong>…（万能背景引入句）",
        "可用于<strong class=\"hl\">科技、社交媒体</strong>等主题的作文开篇",
        "<strong class=\"hl\">a growing number of</strong> = 越来越多的（替换 more and more）",
    ]),
    ("c3", "🔤 核心词汇（阅读高频）", [
        "<strong class=\"hl\">observe</strong> v. 注意，观察；<strong class=\"hl\">constantly</strong> adv. 经常地",
        "<strong class=\"hl\">intelligent</strong> adj. 聪明的；<strong class=\"hl\">device</strong> n. 设备",
        "<strong class=\"hl\">convenient</strong> adj. 方便的；<strong class=\"hl\">innovation</strong> n. 创新",
        "<strong class=\"hl\">rapid</strong> adj. 迅速的；<strong class=\"hl\">remarkable</strong> adj. 显著的",
        "<strong class=\"hl\">desire</strong> v. 渴望；<strong class=\"hl\">request</strong> v./n. 请求；<strong class=\"hl\">contribute to</strong> 有助于，促成",
        "<strong class=\"hl\">AI</strong> = artificial intelligence 人工智能",
    ]),
    ("c4", "🧩 语法点：定语从句与被动语态", [
        "阅读中考查<strong class=\"hl\">非限制性定语从句</strong>（用逗号隔开，补充说明）",
        "<strong class=\"hl\">被动语态</strong>：be + 过去分词（智能设备被使用/被设计）",
        "识别句子主干，先抓主谓宾再看从句/修饰成分",
    ]),
    ("c5", "🕵️ 阅读干扰项：“张冠李戴”", [
        "干扰选项常把<strong class=\"hl\">A 事物的特点安到 B 事物身上</strong>",
        "细节题排除法：回原文<strong class=\"hl\">逐项核对主语与特征</strong>，不凭印象",
        "注意<strong class=\"hl\">范围词</strong>（all / some / never）与原文是否一致",
    ]),
    ("c6", "📦 不定代词：范围分类", [
        "<strong class=\"hl\">两者</strong>范围：both（都）/ either（任一）/ neither（都不）",
        "<strong class=\"hl\">三者及以上</strong>：all（都）/ none（都不）/ any（任一）/ every（每一个）",
        "解题：先判断<strong class=\"hl\">指代范围</strong>，再结合语境推理答案",
    ]),
    ("c7", "🚫 复合不定代词：不能与 of 连用", [
        "复合不定代词（someone/something/anyone/nothing…）是普通不定代词的特殊形式",
        "⚠️ <strong class=\"hl\">不能和 of 搭配</strong>：不能说 some of someone",
        "对比：<strong class=\"hl\">none of them / neither of them</strong> 可以接 of（普通不定代词）",
    ]),
    ("c8", "⚖️ 比较级修饰词与固定句式", [
        "可修饰比较级：<strong class=\"hl\">much / a lot / far / even / a little / a bit</strong>",
        "固定句式：<strong class=\"hl\">the + 比较级, the + 比较级</strong>（越……就越……）",
        "⚠️ <strong class=\"hl\">very 和 more 不能修饰比较级</strong>",
    ]),
    ("c9", "📏 同级比较 as...as", [
        "结构：<strong class=\"hl\">as + 原级 + as</strong>（和……一样）",
        "中间用<strong class=\"hl\">形容词还是副词，取决于所修饰的动词</strong>：",
        "修饰 be 动词/系动词用形容词（as tall as）；修饰实义动词用副词（as carefully as）",
    ]),
    ("c10", "📝 单词巩固：note / waste 等多义词", [
        "<strong class=\"hl\">note</strong>：笔记（take notes）/ 纸币（a £5 note）/ 证明书（a sick note）/ 音符（high notes）",
        "<strong class=\"hl\">waste</strong>：v. 浪费（waste time）/ n. 垃圾（同 rubbish）",
        "教材第 20 页单词短语：开火车过词，注意<strong class=\"hl\">词性转换与固定搭配</strong>",
    ]),
    ("c11", "🎯 课堂作业要求", [
        "优先完成学校布置的<strong class=\"hl\">高质量月考卷</strong>；负担过重时针对性做薄弱模块",
        "所有错题需<strong class=\"hl\">撰写解析</strong>；语境理解类错题需<strong class=\"hl\">录制语音讲解题逻辑</strong>",
        "完成智能设备主题阅读的<strong class=\"hl\">剩余配套习题</strong>",
    ]),
    ("c12", "💡 学习方法引导", [
        "“听懂知识点”和“会做题”是两回事 → 遵循<strong class=\"hl\">基础复习 → 做题演练 → 错题反思</strong>循环",
        "不要盲目刷题；所有必背知识点都要通过<strong class=\"hl\">默写检验</strong>过关",
        "文理科底层逻辑一致：反复巩固、逐步扩大<strong class=\"hl\">知识储备池</strong>（“像扩大池塘，至少要有水可舀”）",
    ]),
]

QUIZ = [
    ("智能设备（Smart devices）这篇阅读文本的整体结构是", ["A. 总分总", "B. 分总", "C. 总分", "D. 并列"], 0,
     "典型<strong>总分总</strong>结构：首段引出话题 → 中间三段分类介绍 → 尾段总结与展望。"),
    ("该阅读首段的主要作用是", ["A. 直接罗列产品价格", "B. 以科技发展背景引出核心话题 Smart devices", "C. 讲述作者个人经历", "D. 对比中外产品"], 1,
     "首段以<strong>科技快速发展的社会背景</strong>引出核心话题“Smart devices”。"),
    ("文章中间三个自然段分别介绍的三类产品是", ["A. 智能手表、智能电视、智能冰箱", "B. 智能安全设备、智能温度控制器、智能音箱", "C. 智能手机、智能眼镜、扫地机器人", "D. 智能门锁、智能灯泡、智能窗帘"], 1,
     "三类产品：<strong>智能安全设备、智能温度控制器、智能音箱</strong>。"),
    ("尾段的主要内容是", ["A. 介绍第四类产品", "B. 总结作者看法并表达对未来智能家居的期待", "C. 批评智能设备的缺点", "D. 给出购买建议"], 1,
     "尾段总结作者对智能设备的<strong>看法</strong>与对<strong>未来智能家居的期待</strong>。"),
    ("“With the rapid development of science and technology” 这个句型的用途是", ["A. 结尾总结", "B. 作文开篇的万能背景引入句", "C. 表达个人观点", "D. 举例说明"], 1,
     "这是<strong>万能背景引入句型</strong>，可用于科技、社交媒体等主题的作文开篇。"),
    ("可以替换 more and more（越来越多）的高级表达是", ["A. a growing number of", "B. a great deal of", "C. plenty of", "D. a bit of"], 0,
     "<strong>a growing number of</strong> = 越来越多的（后接可数名词复数）。"),
    ("observe 的词性与词义是", ["A. n. 观察", "B. v. 注意，观察", "C. adj. 明显的", "D. adv. 明显地"], 1,
     "<strong>observe v. 注意，观察</strong>。"),
    ("constantly 的词性与词义是", ["A. adj. 恒定的", "B. adv. 经常地", "C. n. 常数", "D. v. 保持不变"], 1,
     "<strong>constantly adv. 经常地</strong>（constant adj. 恒定的）。"),
    ("intelligent 的词义是", ["A. 聪明的", "B. 勤快的", "C. 内向的", "D. 有耐心的"], 0,
     "<strong>intelligent adj. 聪明的</strong>（intelligence n. 智力）。"),
    ("device 的词义是", ["A. 发明", "B. 设备", "C. 设计", "D. 装置图"], 1,
     "<strong>device n. 设备</strong>（如 smart devices 智能设备）。"),
    ("AI 的全称是", ["A. Artificial Intelligence", "B. Automatic Internet", "C. Advanced Invention", "D. Active Interface"], 0,
     "<strong>AI = artificial intelligence</strong> 人工智能。"),
    ("convenient 的词义是", ["A. 方便的", "B. 昂贵的", "C. 复杂的", "D. 可靠的"], 0,
     "<strong>convenient adj. 方便的</strong>；反义 inconvenient。"),
    ("innovation 的词义是", ["A. 创新", "B. 投资", "C. 邀请", "D. 发明家"], 0,
     "<strong>innovation n. 创新</strong>（innovate v. 创新）。"),
    ("desire 的词义是", ["A. 拒绝", "B. 渴望", "C. 描述", "D. 装饰"], 1,
     "<strong>desire v. 渴望</strong>（n. 愿望）。"),
    ("contribute to 的意思是", ["A. 有助于，促成", "B. 贡献给某人", "C. 分配给", "D. 联系"], 0,
     "<strong>contribute to</strong> = 有助于，促成（也可表“向……投稿/捐赠”）。"),
    ("request 的词性是", ["A. 只作动词", "B. v./n. 请求", "C. 只作名词", "D. adj. 要求的"], 1,
     "<strong>request v./n. 请求</strong>（比 ask 正式）。"),
    ("rapid 的词义是", ["A. 迅速的", "B. 缓慢的", "C. 稳定的", "D. 罕见的"], 0,
     "<strong>rapid adj. 迅速的</strong>；rapid development 快速发展。"),
    ("remarkable 的词义是", ["A. 显著的", "B. 可标记的", "C. 普通的", "D. 难以描述的"], 0,
     "<strong>remarkable adj. 显著的</strong>（remark v. 评论）。"),
    ("阅读中遇到非限制性定语从句时，正确的处理方式是", ["A. 忽略从句", "B. 用逗号隔开、作补充说明，先抓句子主干", "C. 把从句当主句翻译", "D. 只看从句"], 1,
     "<strong>非限制性定语从句</strong>用逗号隔开，起<strong>补充说明</strong>作用；先抓主干再理解从句。"),
    ("被动语态的基本构成是", ["A. do + 过去分词", "B. be + 过去分词", "C. have + 过去分词", "D. be + 现在分词"], 1,
     "<strong>be + 过去分词</strong>：如 Smart devices are widely used.（智能设备被广泛使用）"),
    ("阅读细节题中常见的干扰选项类型是", ["A. 无中生有", "B. 张冠李戴", "C. 以偏概全", "D. 以上都是"], 3,
     "常见干扰：<strong>张冠李戴</strong>（把 A 的特点安到 B 上）、无中生有、以偏概全等；用回原文逐项核对主语的排除法。"),
    ("判断不定代词用法的第一步是", ["A. 先看时态", "B. 先判断指代范围（两者还是三者以上）", "C. 先看词性", "D. 先数句子数量"], 1,
     "解题时优先<strong>判断指代范围</strong>，再结合语境推理答案。"),
    ("下列属于“两者”范围的不定代词是", ["A. both / either / neither", "B. all / none / any", "C. every / each / some", "D. none / any / some"], 0,
     "<strong>两者</strong>：both（都）/ either（任一）/ neither（都不）。"),
    ("下列属于“三者及以上”范围的不定代词是", ["A. both / either", "B. neither / both", "C. all / none / any / every", "D. either / neither"], 2,
     "<strong>三者及以上</strong>：all / none / any / every。"),
    ("关于复合不定代词，下列说<u>错误</u>的是", ["A. 复合不定代词不能和 of 搭配", "B. something 是复合不定代词", "C. someone of them 是正确表达", "D. 复合不定代词是普通不定代词的特殊形式"], 2,
     "复合不定代词<strong>不能与 of 连用</strong>，故 someone of them 错误；应用 <strong>none of them / neither of them</strong>。"),
    ("下列单词中，可以修饰比较级的是", ["A. very", "B. more", "C. much", "D. so"], 2,
     "可修饰比较级：<strong>much / a lot / far / even / a little / a bit</strong>；very 和 more 不能修饰比较级。"),
    ("“The more you read, the more you know.” 这一句式表示", ["A. 越……就越……", "B. 一边……一边……", "C. 虽然……但是……", "D. 不是……而是……"], 0,
     "<strong>the + 比较级, the + 比较级</strong> = 越……就越……。"),
    ("在 as...as 同级比较结构中，中间用形容词还是副词取决于", ["A. 句子长短", "B. 所修饰的动词属性", "C. 主语单复数", "D. 时态"], 1,
     "取决于<strong>所修饰的动词</strong>：修饰系动词/be 用形容词（as tall as），修饰实义动词用副词（as carefully as）。"),
    ("教材第 20 页单词巩固中，note 的多个释义不包括", ["A. 笔记", "B. 纸币", "C. 证明书", "D. 假期"], 3,
     "note 的词义：笔记（take notes）/ 纸币（a £5 note）/ 证明书（a sick note）/ 音符（high notes）；<strong>不含“假期”</strong>。"),
    ("与 rubbish 同义的词是", ["A. waste", "B. device", "C. request", "D. desire"], 0,
     "<strong>waste</strong> 作名词时可表“垃圾”，与 rubbish 同义。"),
    ("老师对英语错题的要求是", ["A. 只需订正答案", "B. 撰写简要解析，语境理解类错题录制语音讲解题逻辑", "C. 抄写三遍", "D. 背下整篇文章"], 1,
     "所有错题需<strong>撰写解析</strong>；<strong>语境理解类错题</strong>需<strong>录制语音讲解题逻辑</strong>。"),
    ("老师推荐的循环学习模式是", ["A. 刷题 → 刷题 → 刷题", "B. 基础复习 → 做题演练 → 错题反思", "C. 只背单词", "D. 只看讲解不做题"], 1,
     "<strong>基础复习 → 做题演练 → 错题反思</strong>的循环；“听懂”与“会做”是两回事。"),
]

FLASH = [
    ("智能设备阅读的全文结构与内容？",
     "<strong>总分总</strong>：首段以科技发展背景引出 Smart devices → 中间三段介绍<strong>智能安全设备、智能温度控制器、智能音箱</strong> → 尾段总结作者看法与对智能家居的期待。"),
    ("两个可套用的高分表达？",
     "① <strong>With the rapid development of science and technology</strong>…（背景引入）；② <strong>a growing number of</strong>（替换 more and more）。"),
    ("本课核心词汇 12 个？",
     "observe 观察 / constantly 经常地 / intelligent 聪明的 / device 设备 / convenient 方便的 / innovation 创新 / desire 渴望 / contribute to 有助于 / request 请求 / rapid 迅速的 / remarkable 显著的 / AI 人工智能。"),
    ("非限制性定语从句与被动语态的要点？",
     "非限制性定语从句用<strong>逗号隔开</strong>、作补充说明；被动语态 = <strong>be + 过去分词</strong>。先抓主干再处理修饰成分。"),
    ("阅读干扰项“张冠李戴”怎么识别？",
     "干扰项把<strong>A 事物的特点安到 B 事物身上</strong>；对策：回原文<strong>逐项核对主语与特征</strong>，注意范围词（all/some/never）。"),
    ("不定代词的范围分类？",
     "<strong>两者</strong>：both / either / neither；<strong>三者及以上</strong>：all / none / any / every。解题先判断指代范围。"),
    ("复合不定代词的使用禁忌？",
     "复合不定代词（someone/something…）<strong>不能与 of 连用</strong>；普通不定代词才可以：none of them / neither of them。"),
    ("哪些词能修饰比较级？哪些不能？",
     "能：<strong>much / a lot / far / even / a little / a bit</strong>；不能：<strong>very 和 more</strong>。"),
    ("“越……就越……”的固定句式？",
     "<strong>the + 比较级, the + 比较级</strong>：The more you read, the more you know."),
    ("as...as 同级比较：用形容词还是副词？",
     "取决于<strong>所修饰的动词</strong>：修饰 be/系动词用形容词（as tall as）；修饰实义动词用副词（as carefully as）。"),
    ("note 与 waste 的多义？",
     "<strong>note</strong>：笔记 / 纸币 / 证明书 / 音符；<strong>waste</strong>：v. 浪费（waste time）、n. 垃圾（=rubbish）。"),
    ("老师布置的作业与学习方法要求？",
     "优先完成学校<strong>高质量月考卷</strong>（负担重则做薄弱模块）；错题<strong>写解析</strong>、语境类错题<strong>录语音</strong>；学习循环：<strong>基础复习 → 做题演练 → 错题反思</strong>，必背点用默写检验。"),
]

ERRORS = [
    ("❌ 用 very / more 修饰比较级",
     "It is very better. / He is more taller than me.",
     "very 和 more <strong>不能修饰比较级</strong>；用 <strong>much / a lot / far / even / a little / a bit</strong>。"),
    ("❌ 复合不定代词误接 of",
     "someone of them / anything of these。",
     "<strong>复合不定代词不能与 of 连用</strong>；要表达“他们中没有”用 <strong>none of them / neither of them</strong>。"),
    ("❌ 不定代词范围判断错误",
     "指代两者时用 none：Of the two boys, none is taller. ",
     "两者用 <strong>neither</strong>；三者及以上才用 <strong>none</strong>。做题先圈定范围（two / three / many）。"),
    ("❌ as...as 中间词性用错",
     "She sings as good as her sister.（修饰实义动词却用形容词）",
     "修饰<strong>实义动词</strong>用副词 → sings as <strong>well</strong> as；修饰 be/系动词才用形容词（as tall as）。"),
    ("❌ 细节题被“张冠李戴”误导",
     "把智能音箱的功能选成了智能温度控制器的特点。",
     "回原文<strong>逐项核对主语</strong>：选项说的是哪个设备、原文说的是哪个设备，一一对应才选。"),
    ("❌ 作文开篇只会用 more and more",
     "There are more and more smart devices…（重复、低分表达）",
     "升级为 <strong>a growing number of smart devices</strong>；背景句用 <strong>With the rapid development of science and technology</strong>。"),
    ("❌ 只“听懂”不练题",
     "上课听懂就以为掌握了，不写解析、不做错题反思。",
     "“听懂”≠“会做”：遵循<strong>基础复习 → 做题演练 → 错题反思</strong>循环，必背知识点用<strong>默写</strong>检验。"),
]

h = open(BASE_F, encoding='utf-8').read()
nq, nf, ne, nk = len(QUIZ), len(FLASH), len(ERRORS), len(KNOW)

h = h.replace('<title>🌍 Words &amp; Comparatives · 互动学习</title>', '<title>🤖 Smart Devices 阅读与语法 · 互动学习</title>', 1)
h = h.replace('<h1><i class="fas fa-book"></i> Words &amp; Comparatives · 互动学习</h1>',
              '<h1><i class="fas fa-robot"></i> Smart Devices 阅读与语法 · 互动学习</h1>', 1)
h = re.sub(r'<p>2026秋双语八年级 C班 · 第2讲 · \d+ 题 · \d+ 卡牌 \| 双语英语</p>',
           f'<p>2026秋双语八年级 C班 · 课堂补充课 · {nq} 题 · {nf} 卡牌 | 智能设备阅读</p>', h, count=1)
h = re.sub(r'<span><i class="fas fa-check-circle"[^>]*></i> \d+道测验题</span>',
           f'<span><i class="fas fa-check-circle" style="color:var(--success)"></i> {nq}道测验题</span>', h, count=1)
h = re.sub(r'<span><i class="fas fa-layer-group"></i> \d+张知识卡</span>',
           f'<span><i class="fas fa-layer-group"></i> {nf}张知识卡</span>', h, count=1)
h = re.sub(r'<span><i class="fas fa-exclamation-triangle" style="color:var(--danger)"></i> \d+大易错点</span>',
           f'<span><i class="fas fa-exclamation-triangle" style="color:var(--danger)"></i> {ne}大易错点</span>', h, count=1)
h = re.sub(r'<div class="section-header"><i class="fas fa-sitemap"[^>]*></i> 第二讲 · [^<]*</div>',
           '<div class="section-header"><i class="fas fa-sitemap" style="color:#667eea"></i> 课堂补充 · Smart Devices 阅读与语法</div>', h, count=1)

g0 = h.find('<div class="knowledge-grid">'); g1 = h.find('<div class="teacher-talk">', g0)
cards = ''
for cls, title, lis in KNOW:
    items = ''.join(f'<li>{x}</li>' for x in lis)
    cards += f'      <div class="knowledge-card {cls}"><h3>{title}</h3><ul>{items}</ul></div>\n'
h = h[:g0] + '<div class="knowledge-grid">\n' + cards + '    </div>\n    ' + h[g1:]

t0 = h.find('<div class="teacher-talk">'); t1 = h.find('<div id="tab-quiz"', t0)
tt = '''<div class="teacher-talk">
      <h4><i class="fas fa-microphone-alt"></i> 🎙️ 课堂要点 · 智能设备阅读与语法巩固</h4>
      <p><strong>本课核心</strong>：①阅读：<strong>Smart Devices（智能设备）</strong>总分总结构——首段背景引入、中间三段分类（智能安全设备/智能温度控制器/智能音箱）、尾段总结展望；②句型词汇：<strong>With the rapid development of science and technology</strong>、<strong>a growing number of</strong>、observe / constantly / intelligent 等；③语法：<strong>非限制性定语从句、被动语态</strong>、不定代词范围分类、比较级修饰词与 as...as 同级比较。</p>
      <p><strong>解题技巧</strong>：阅读用 30 秒扫读判断结构（总分总），细节题用<strong>逐项核对主语</strong>的排除法防“张冠李戴”；不定代词先判断<strong>指代范围</strong>（两者 or 三者以上），复合不定代词<strong>不能接 of</strong>；比较级修饰词记“much/a lot/far/even/a little/a bit”，<strong>very 与 more 不可</strong>；as...as 中间用形容词还是副词取决于<strong>所修饰的动词</strong>。</p>
      <p><strong>作业要求</strong>：优先完成学校高质量月考卷（负担过重则针对薄弱模块）；<strong>所有错题撰写解析</strong>，语境理解类错题<strong>录制语音讲解题逻辑</strong>；完成智能设备阅读的剩余配套习题；教材第 20 页单词短语过关（note / waste 等多义词）。</p>
      <p><strong>🎓 老师课堂金句</strong> — “听懂是前提，然后要自己亲自实践演练，同时反思自己的问题。”｜“文科学习就像扩大池塘，虽然每次做题可能只会用到一条水，但你至少要有水可舀。”｜“把学习养成吃饭喝水一样的习惯，就不会觉得抵触和痛苦。”</p>
    </div>
    '''
h = h[:t0] + tt + h[t1:]

q0 = h.find('const questions = ['); q1 = h.find('const flashcards = [', q0)
qdata = [{'q': q, 'opts': o, 'ans': a, 'exp': e} for q, o, a, e in QUIZ]
h = h[:q0] + 'const questions = ' + json.dumps(qdata, ensure_ascii=False, indent=1) + ';\n\n\n' + h[q1:]

f0 = h.find('const flashcards = ['); f1 = h.find('errors = [', f0)
fdata = [{'front': x, 'back': y} for x, y in FLASH]
h = h[:f0] + 'const flashcards = ' + json.dumps(fdata, ensure_ascii=False, indent=1) + ';\n\n\n' + h[f1:]

e0 = h.find('errors = ['); e1 = h.find('function toast', e0)
edata = [{'title': t, 'wrong': w, 'right': r} for t, w, r in ERRORS]
h = h[:e0] + 'errors = ' + json.dumps(edata, ensure_ascii=False, indent=1) + ';\n\n\n\n' + h[e1:]

h = h.replace('english_lesson2_state_check', 'english_lesson3_state_check')
h = h.replace("QUIZ_PROG_KEY='quiz_progress_english_lesson2'", "QUIZ_PROG_KEY='quiz_progress_english_lesson3'")
h = h.replace("WRONG_HISTORY_KEY='quiz_english_lesson2_wrong'", "WRONG_HISTORY_KEY='quiz_english_lesson3_wrong'")
h = h.replace('第2讲 Words &amp; Comparatives话题', '课堂补充 Smart Devices话题')
h = h.replace('第2讲 Words &amp; Comparatives | 双语英语', 'Smart Devices 阅读与语法 | 双语英语')
h = h.replace('英语 · 第2讲', '英语 · 课堂补充')
h = re.sub(r'<div class="quiz-stats" id="quizStats">0 / \d+</div>', f'<div class="quiz-stats" id="quizStats">0 / {nq}</div>', h, count=1)
h = re.sub(r'共\d+张知识卡', f'共{nf}张知识卡', h, count=1)
open(OUT_F, 'w', encoding='utf-8').write(h)

js = r"""const fs=require('fs');const html=fs.readFileSync('english_lesson3_interactive.html','utf8');const re=/<script[^>]*>([\s\S]*?)<\/script>/g;let m,ok=true;while((m=re.exec(html))){try{new Function(m[1])}catch(e){ok=false;console.log('ERR',e.message)}}console.log(ok?'JS OK':'JS ERR')"""
r = subprocess.run(['node','-e',js], capture_output=True, text=True, cwd=REPO)
hh = open(OUT_F, encoding='utf-8').read()
print(r.stdout.strip())
print(f'题{nq} 卡{nf} 错{ne} 知识{nk}')
print('div:', len(re.findall(r'<div\b', hh)), '/', hh.count('</div>'))
print('残留 第2讲:', hh.count('第2讲'), '| lesson2:', hh.count('lesson2'))
