#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""_build_english_lesson2.py — 生成英语第2讲互动页（C班）
材料: 2026秋双语八年级C班第2讲（默写单&知识清单 + 练习册 + 教材答案 + 练习册答案）
基座: english_lesson1_interactive.html（C班版, 已验证）
输出: english_lesson2_interactive.html
"""
import re, json, subprocess

REPO = '/home/administrator/xuci-jiancha'
BASE_F = f'{REPO}/english_lesson1_interactive.html'
OUT_F = f'{REPO}/english_lesson2_interactive.html'

KNOW = [
    ("c1", "📘 lift 的三种用法", [
        "搭便车 / 开车顺便送某人：<strong class=\"hl\">give sb. a lift</strong>",
        "电梯：<strong class=\"hl\">take the lift</strong> 乘电梯",
        "举起；抬起：<strong class=\"hl\">lift up</strong>（用体力或机械力举起）",
        "拓展：lifter 升降机；举重运动员（weight lifter）",
    ]),
    ("c2", "📝 note 的多重词义", [
        "记笔记：<strong class=\"hl\">take/make notes</strong>",
        "便利贴：<strong class=\"hl\">sticky note / post-it note</strong>",
        "v. 注意；指出（后接名词/代词/<strong class=\"hl\">that 从句</strong>）",
        "货币义：<strong class=\"hl\">纸币</strong> a £5 note ｜ 文件义：a sick note 证明书 ｜ 音乐义：high/low notes 音符",
    ]),
    ("c3", "🗑️ rubbish 与垃圾表达", [
        "同义词：<strong class=\"hl\">waste / trash / garbage / litter</strong>",
        "垃圾袋/桶：a rubbish bag/bin；生活垃圾：household rubbish",
        "倒垃圾：<strong class=\"hl\">take out the rubbish</strong>",
        "垃圾分类：<strong class=\"hl\">rubbish sorting</strong>",
    ]),
    ("c4", "🙏 Can/Could you please…?（请求）", [
        "Can/Could you please water the plants? 请你……好吗？",
        "肯定：<strong class=\"hl\">No problem. / With pleasure. / Sure·Of course·Certainly.</strong>",
        "否定：Sorry, I can't. I have to… / Sorry, I'm going to… / <strong class=\"hl\">I'm afraid not.</strong>",
    ]),
    ("c5", "🔑 Can/Could I…?（请求许可）", [
        "意为“我能……吗？”，请求对方允许自己做某事",
        "肯定：<strong class=\"hl\">Yes, you can. / Of course you can. / Yes, please.</strong>",
        "否定：Sorry, you can't. / <strong class=\"hl\">Sorry, I'm afraid you can't.</strong>",
    ]),
    ("c6", "⚖️ 比较级规则变化（5 条）", [
        "一般 +er：short → <strong class=\"hl\">shorter</strong>",
        "不发音 e 结尾 +r：cute → <strong class=\"hl\">cuter</strong>",
        "辅音+y 结尾变 y 为 i +er：pretty → <strong class=\"hl\">prettier</strong>",
        "重读闭音节双写末尾辅音 +er：big → <strong class=\"hl\">bigger</strong>；hot → hotter",
        "多音节/部分双音节前加 more：important → <strong class=\"hl\">more important</strong>",
    ]),
    ("c7", "📊 比较级不规则变化", [
        "good/well → <strong class=\"hl\">better</strong>",
        "ill/bad/badly → <strong class=\"hl\">worse</strong>",
        "many/much → <strong class=\"hl\">more</strong>；little → <strong class=\"hl\">less</strong>",
        "old → older/<strong class=\"hl\">elder</strong>；far → farther/<strong class=\"hl\">further</strong>",
    ]),
    ("c8", "🔤 三种比较结构", [
        "高级比较（比……更）：比较级 + <strong class=\"hl\">than</strong>（I am taller than him.）",
        "次级比较（不如……）：<strong class=\"hl\">less + 原级 + than</strong>（I am less tall than him.）",
        "同级比较（和……一样）：<strong class=\"hl\">as + 原级 + as</strong>（I am as tall as him.）",
    ]),
    ("c9", "💪 修饰比较级的程度副词", [
        "三多：<strong class=\"hl\">much / a lot / far</strong>",
        "两少：<strong class=\"hl\">a little / a bit</strong>；一甚至：<strong class=\"hl\">even</strong>",
        "⚠️ <strong class=\"hl\">very 和 more 不能修饰比较级</strong>",
    ]),
    ("c10", "🎯 比较级特殊表达", [
        "the + 比较级, the + 比较级（越……就越……）：The more careful you are, <strong class=\"hl\">the fewer</strong> mistakes you will make.",
        "比较级 + and + 比较级（越来越……）：The weather is <strong class=\"hl\">hotter and hotter</strong>.",
        "多音节：<strong class=\"hl\">more and more + 原级</strong>（more and more beautiful）",
    ]),
    ("c11", "📚 考点词汇（上）：invite / sort / plan / add", [
        "invite sb. <strong class=\"hl\">to do</strong> sth 邀请某人做某事；<strong class=\"hl\">invitation</strong> n. 邀请；请柬",
        "imagine→<strong class=\"hl\">imagination</strong>；prepare→preparation；organize→organization",
        "sort：a sort of 一种 / <strong class=\"hl\">all sorts of</strong> 许多种 / sort of 有点儿 / sort out 弄清",
        "plan to do sth 打算做；add...<strong class=\"hl\">to</strong>... 把……加到；<strong class=\"hl\">add up to</strong> 总计为",
    ]),
    ("c12", "📚 考点词汇（下）：until / familiar / describe / matter / cover / decorate", [
        "until：<strong class=\"hl\">not...until</strong> 直到……才",
        "familiar：sb. be familiar <strong class=\"hl\">with</strong> sth ｜ sth. be familiar <strong class=\"hl\">to</strong> sb",
        "describe...<strong class=\"hl\">as</strong> 把……描述成为；<strong class=\"hl\">description</strong> n. 描述；beyond description 难以描绘",
        "matter：What's the matter? / <strong class=\"hl\">It doesn't matter.</strong> / no matter 不论",
        "cover...<strong class=\"hl\">with</strong> 覆盖 → be covered with；<strong class=\"hl\">discover</strong> v. 发现",
        "decorate...<strong class=\"hl\">with</strong> 用……装饰；<strong class=\"hl\">decoration</strong> n. 装饰品",
    ]),
]

QUIZ = [
    ("give sb. a lift 的意思是", ["A. 给某人一部电梯", "B. 开车顺便送某人", "C. 把某人举起来", "D. 借给某人钱"], 1,
     "give sb. a lift = <strong>开车顺便送某人</strong>（顺路捎带）；lift 此处指“搭便车”。"),
    ("“乘电梯”的正确表达是", ["A. take the lift", "B. give a lift", "C. lift up", "D. take a note"], 0,
     "take the lift = <strong>乘电梯</strong>；lift up = 举起。"),
    ("“记笔记”的正确表达是", ["A. take/make notes", "B. take a note", "C. do notes", "D. notes taking"], 0,
     "固定表达 <strong>take/make notes</strong>（记笔记），notes 用复数。"),
    ("“倒垃圾”的正确表达是", ["A. take up the rubbish", "B. take out the rubbish", "C. take off the rubbish", "D. take in the rubbish"], 1,
     "<strong>take out the rubbish</strong> = 倒垃圾；take up 占据/开始，take off 起飞/脱下。"),
    ("与 rubbish（垃圾）意思最接近的一组是", ["A. paper, plastic, glass", "B. waste, trash, garbage", "C. lift, note, sort", "D. plan, add, cover"], 1,
     "rubbish 的同义词：<strong>waste、trash、garbage、litter</strong>。"),
    ("“垃圾分类”的正确表达是", ["A. rubbish sorting", "B. rubbish lifting", "C. rubbish noting", "D. rubbish covering"], 0,
     "<strong>rubbish sorting</strong> = 垃圾分类（sort 分类）。"),
    ("a £5 note 中 note 的意思是", ["A. 笔记", "B. 纸币", "C. 便条", "D. 音符"], 1,
     "note 表 <strong>纸币</strong>：a £5 note 一张 5 英镑纸币。"),
    ("a sick note 中 note 的意思是", ["A. 正式文件；证明书", "B. 音符", "C. 纸币", "D. 注释"], 0,
     "a sick note = <strong>病假证明/正式文件</strong>；high/low notes 才是音符。"),
    ("—Could you please water the plants? —___（表示乐意帮忙）",
     ["A. With pleasure.", "B. I'm afraid not.", "C. Sorry, I can't.", "D. Yes, you can."], 0,
     "对请求的肯定答语：<strong>With pleasure.</strong>（乐意帮忙）；I'm afraid not 是否定。"),
    ("—Could I use your pen? —___（表示拒绝）",
     ["A. Yes, you can.", "B. Sorry, I'm afraid you can't.", "C. With pleasure.", "D. No problem."], 1,
     "请求许可的否定答语：<strong>Sorry, I'm afraid you can't.</strong>；D、A 为肯定。"),
    ("—Could you help me with my homework? —___（委婉拒绝）",
     ["A. Sure. Of course.", "B. Sorry, I can't. I have to do my own homework.", "C. Yes, please.", "D. No problem."], 1,
     "拒绝请求用 <strong>Sorry, I can't. I have to…</strong>；Yes, please 是许可类答语，不用于回答求助。"),
    ("Can/Could I…? 这一句型的用途是", ["A. 请求对方允许自己做某事", "B. 询问对方的能力", "C. 提出建议", "D. 表达感谢"], 0,
     "<strong>Can/Could I…?</strong> = 我能……吗？用于<strong>请求许可</strong>（允许自己做某事）。"),
    ("pretty 的比较级是", ["A. more pretty", "B. prettier", "C. prettiest", "D. prettyer"], 1,
     "辅音字母+y 结尾 → 变 y 为 i 再加 er：pretty → <strong>prettier</strong>。"),
    ("big 的比较级是", ["A. biger", "B. bigger", "C. more big", "D. biggest"], 1,
     "重读闭音节 → 双写末尾辅音字母 + er：big → <strong>bigger</strong>。"),
    ("important 的比较级是", ["A. importanter", "B. more important", "C. most important", "D. importantest"], 1,
     "多音节词前加 more：important → <strong>more important</strong>。"),
    ("ill / bad / badly 的比较级是", ["A. badder", "B. more bad", "C. worse", "D. worst"], 2,
     "不规则变化：ill/bad/badly → <strong>worse</strong>。"),
    ("little 的比较级是", ["A. littler", "B. less", "C. least", "D. more little"], 1,
     "little → <strong>less</strong>（不规则变化）；least 是最高级。"),
    ("far 的比较级是", ["A. farer", "B. more far", "C. farther/further", "D. farthest"], 2,
     "far → <strong>farther / further</strong>（两个形式均可）。"),
    ("“我比他高”的正确表达是", ["A. I am taller than him.", "B. I am more tall than him.", "C. I am tall than him.", "D. I am as tall than him."], 0,
     "高级比较：比较级 + <strong>than</strong> → I am taller than him."),
    ("“我不如他努力”的正确表达是", ["A. I am not hard-working than him.", "B. I am less hard-working than him.", "C. I am less hard-working as him.", "D. I am more hard-working than him."], 1,
     "次级比较：<strong>less + 原级 + than</strong> → less hard-working than him。"),
    ("“我和他一样高”的正确表达是", ["A. I am so tall as him.", "B. I am as taller as him.", "C. I am as tall as him.", "D. I am as tall than him."], 2,
     "同级比较：<strong>as + 原级 + as</strong> → as tall as him。"),
    ("下列不能修饰比较级的是", ["A. much", "B. a lot", "C. very", "D. even"], 2,
     "修饰比较级：三多 much/a lot/far；两少 a little/a bit；一甚至 even。<strong>very 和 more 不能修饰比较级</strong>。"),
    ("“你越仔细，你犯错越少”的正确表达是",
     ["A. More careful you are, fewer mistakes you will make.", "B. The more careful you are, the fewer mistakes you will make.", "C. The more careful you are, the less mistakes you will make.", "D. The careful you are, the few mistakes you make."], 1,
     "<strong>the + 比较级, the + 比较级</strong>（越……就越……）→ The more careful you are, the fewer mistakes you will make."),
    ("“天气越来越热”的正确表达是",
     ["A. The weather is hotter and hotter.", "B. The weather is more hot and more hot.", "C. The weather is more and more hot.", "D. The weather is hotter and hot."], 0,
     "<strong>比较级 + and + 比较级</strong>（越来越……）→ hotter and hotter。"),
    ("多音节词“越来越漂亮”的正确表达是",
     ["A. beautifuler and beautifuler", "B. more and more beautiful", "C. more beautiful and more beautiful", "D. most and most beautiful"], 1,
     "多音节/部分双音节用 <strong>more and more + 原级</strong> → more and more beautiful。"),
    ("invite sb. ___ sth 邀请某人做某事", ["A. to do", "B. do", "C. doing", "D. done"], 0,
     "<strong>invite sb. to do sth</strong>（邀请某人做某事）；invite sb. to... 邀请某人到……"),
    ("“邀请；请柬”的英文名词是", ["A. invite", "B. inviting", "C. invitation", "D. invited"], 2,
     "<strong>invitation</strong> n. 邀请；请柬（invite 是动词）。"),
    ("imagine 的名词形式是", ["A. imagination", "B. imaginition", "C. imagine", "D. imaginating"], 0,
     "变 e 为 a 加 tion：imagine → <strong>imagination</strong>（同 prepare→preparation；organize→organization）。"),
    ("“许多种……”的正确表达是", ["A. a sort of", "B. all sorts of", "C. sort of", "D. sort with"], 1,
     "<strong>all sorts of</strong> = 许多种；a sort of 一种；sort of 有点儿。"),
    ("add up to 的意思是", ["A. 把……加起来", "B. 总计为", "C. 增加", "D. 除了……以外（还）"], 1,
     "<strong>add up to</strong> = 总计为；add up 才是“把……加起来”。"),
    ("“直到……才”的正确表达是", ["A. until", "B. not...until", "C. till not", "D. not...till"], 1,
     "<strong>not...until</strong> = 直到……才（谓语用否定形式）；until 单独用表“直到……为止”。"),
    ("“某人熟悉某物”的正确表达是", ["A. sb. be familiar to sth", "B. sb. be familiar with sth", "C. sth. be familiar with sb", "D. familiar sb. with sth"], 1,
     "sb. be <strong>familiar with</strong> sth（人熟悉物）；sth. be familiar <strong>to</strong> sb（物为人所熟悉）。"),
    ("describe...as... 的意思是", ["A. 向某人描述", "B. 把……描述成为", "C. 发现", "D. 难以描绘"], 1,
     "<strong>describe...as...</strong> = 把……描述成为……；beyond description 才是“难以描绘”。"),
    ("“It doesn't matter.” 的意思是", ["A. 没关系。", "B. 怎么了？", "C. 这很重要。", "D. 不论……"], 0,
     "<strong>It doesn't matter.</strong> = 没关系/不要紧；What's the matter? 才是“怎么了”。"),
    ("The desk ___ flowers.（用花覆盖桌面）", ["A. is covered with", "B. covers with", "C. cover with", "D. is covering"], 0,
     "<strong>be covered with</strong> = 被……覆盖（cover...with 的被动形式）。"),
    ("“用花装饰教室”的正确表达是", ["A. decorate the classroom with flowers", "B. decorate flowers with classroom", "C. cover the classroom with flowers", "D. decorate the classroom to flowers"], 0,
     "<strong>decorate...with...</strong> = 用……装饰……；decorate 侧重装饰美化（cover 侧重覆盖）。"),
    ("no matter how busy you are 中 no matter 的意思是", ["A. 没关系", "B. 不论", "C. 要紧", "D. 问题"], 1,
     "<strong>no matter + 疑问词</strong> = 不论……（no matter how/what/where…）。"),
    ("（练习册）作者在感恩节前给儿子发短信的目的是",
     ["A. 表达她的爱", "B. 让他回家", "C. 询问感恩节的计划", "D. 提醒他做作业"], 2,
     "第一段作者明确问 <strong>“Let me know your plans”</strong>，是询问感恩节的计划（答案 C）。"),
    ("（练习册）作者认为 one-word replies（一词回复）怎么样？",
     ["A. 冷漠且不礼貌", "B. 冷漠但清晰", "C. 礼貌且清晰", "D. 完全没有问题"], 0,
     "原文提到一词回复 may be too <strong>impolite</strong>、may seem <strong>cold</strong>，未提 clear（答案 A：①②）。"),
    ("（练习册）画线句 “I will ask for full sentences” 表明",
     ["A. 作者会更常用一词回复", "B. 作者希望儿子改变沟通方式", "C. 作者不愿再和儿子说话", "D. 作者希望儿子提高成绩"], 1,
     "“我会要求完整句子”表明希望儿子<strong>改变沟通方式</strong>（答案 B）。"),
    ("（练习册）全文主要讲的是",
     ["A. 年轻人为何喜欢一词回复", "B. 别人用一词回复时如何应对", "C. 一位母亲对儿子简短回复的感受", "D. 如何用短信表达礼貌"], 2,
     "全文围绕一位母亲对儿子简短回复的感受与看法（答案 C）。"),
    ("（练习册·短文填空）___ a surprise farewell party for Mrs. Chen required careful organization.",
     ["A. Plan", "B. Planning", "C. Planned", "D. Plans"], 1,
     "plan 变动名词作主语且句首大写 → <strong>Planning</strong>（谓语 required 要求单数主语）。"),
    ("（练习册·短文填空）First, we needed to ___ out who would bring decorations and snacks.",
     ["A. sort", "B. cover", "C. add", "D. describe"], 0,
     "固定搭配 <strong>sort out</strong> = 弄清、分配。"),
    ("（练习册·短文填空）“We can't relax ___ everything is ready!” Mrs. Lee reminded us.",
     ["A. until", "B. not until", "C. since", "D. while"], 0,
     "can't relax <strong>until</strong> everything is ready（直到一切就绪才能放松）；此处不写 not。"),
    ("（练习册·短文填空）Luckily, it didn't ___ since Tom had prepared extra songs.",
     ["A. matter", "B. care", "C. mind", "D. work"], 0,
     "固定搭配 <strong>it didn't matter</strong> = 没关系/不要紧。"),
    ("（练习册·短文填空）Later, she ___ a hidden album of our class memories.",
     ["A. discover", "B. discovered", "C. discovers", "D. discovering"], 1,
     "全文为过去时 → <strong>discovered</strong>（发现了一个隐藏相册）。"),
]

FLASH = [
    ("give sb. a lift / take the lift / lift up 分别什么意思？",
     "<strong>give sb. a lift</strong> 开车顺便送某人；<strong>take the lift</strong> 乘电梯；<strong>lift up</strong> 举起。"),
    ("note 的四个拓展词义？",
     "① 注释；批注 notes of an article ② <strong>纸币</strong> a £5 note ③ 正式文件 a sick note ④ 音符 high/low notes。"),
    ("rubbish 的同义词有哪些？",
     "<strong>waste、trash、garbage、litter</strong>；短语：take out the rubbish 倒垃圾 / rubbish sorting 垃圾分类。"),
    ("Can/Could you please…? 的肯定、否定答语？",
     "肯定：No problem. / <strong>With pleasure.</strong> / Sure·Of course·Certainly.；否定：Sorry, I can't. I have to… / I'm afraid not."),
    ("Can/Could I…? 是问什么？答语？",
     "请求<strong>许可</strong>（允许自己做某事）。肯定：Yes, you can. / Of course you can. / Yes, please.；否定：Sorry, you can't. / Sorry, I'm afraid you can't."),
    ("比较级规则变化 5 条",
     "① 一般 +er（shorter）② 不发音 e +r（cuter）③ 辅音+y 变 i +er（prettier）④ 重读闭音节双写辅音 +er（bigger/hotter）⑤ 多音节前加 more（more important）。"),
    ("比较级不规则变化 6 组",
     "good/well → better；ill/bad/badly → worse；many/much → more；little → less；old → older/elder；far → farther/further。"),
    ("三种比较结构（比…更 / 不如 / 一样）",
     "比较级 + <strong>than</strong>（taller than him）；<strong>less + 原级 + than</strong>（less tall than him）；<strong>as + 原级 + as</strong>（as tall as him）。"),
    ("哪些词可以修饰比较级？",
     "三多 <strong>much / a lot / far</strong>；两少 <strong>a little / a bit</strong>；一甚至 <strong>even</strong>。⚠️ very 和 more 不能修饰比较级。"),
    ("“越……就越……”和“越来越……”怎么表达？",
     "<strong>the + 比较级, the + 比较级</strong>（The more careful you are, the fewer mistakes you will make.）；<strong>比较级 + and + 比较级</strong>（hotter and hotter）；多音节用 more and more + 原级。"),
    ("invite / imagine / prepare / organize 的名词形式？",
     "invite → <strong>invitation</strong>；imagine → <strong>imagination</strong>；prepare → <strong>preparation</strong>；organize → <strong>organization</strong>。"),
    ("familiar / describe / matter / cover / decorate 的关键搭配？",
     "sb. be familiar <strong>with</strong> sth；describe...<strong>as</strong> 把……描述成为；It doesn't matter. 没关系；be covered <strong>with</strong> 被……覆盖；decorate...<strong>with</strong> 用……装饰。"),
]

ERRORS = [
    ("❌ 用 very / more 修饰比较级",
     "He is very taller than me. / This book is more better.",
     "very 和 more <strong>不修饰比较级</strong>；用 much / a lot / far / even / a little / a bit → He is much taller than me."),
    ("❌ 比较级规则变化错用",
     "pretty → more pretty；big → biger；important → importanter。",
     "pretty → <strong>prettier</strong>（辅音+y 变 i 加 er）；big → <strong>bigger</strong>（双写末尾辅音）；important → <strong>more important</strong>（多音节前加 more）。"),
    ("❌ 不规则比较级写错",
     "bad → badder；little → littler；far → farer。",
     "bad/badly → <strong>worse</strong>；little → <strong>less</strong>；far → <strong>farther/further</strong>。"),
    ("❌ familiar 的介词颠倒",
     "sb. be familiar to sth / sth. be familiar with sb。",
     "人熟悉物：sb. be familiar <strong>with</strong> sth；物为人所知：sth. be familiar <strong>to</strong> sb。"),
    ("❌ not...until 漏掉 not 或位置错",
     "We can relax until everything is ready.（意思反了）",
     "“直到……才”用 <strong>not...until</strong>：We <strong>can't</strong> relax until everything is ready."),
    ("❌ cover 与 decorate 混用",
     "decorate the board with photos（想表达“贴满照片”）；cover the desk with flowers（想表达“装饰桌子”）。",
     "cover...with 侧重<strong>覆盖、铺满</strong>（photos 贴满布告板用 cover）；decorate...with 侧重<strong>装饰美化</strong>（用花装饰桌子用 decorate）。"),
    ("❌ 短文填空词形错误",
     "plan → plan（句首不大写/不用动名词）；discover → discover（全文过去时却用原形）。",
     "作主语用动名词且句首大写：<strong>Planning</strong>... required...；时态为过去时用 <strong>discovered</strong>。"),
]

# ─────────── 组装 ───────────
h = open(BASE_F, encoding='utf-8').read()
nq, nf, ne, nk = len(QUIZ), len(FLASH), len(ERRORS), len(KNOW)

# 1) 标题/hero/meta/section-header
h = h.replace('<title>🌍 Nauru &amp; Holidays · 互动学习</title>', '<title>🌍 Words &amp; Comparatives · 互动学习</title>', 1)
h = h.replace('<h1><i class="fas fa-globe-asia"></i> Nauru &amp; Holidays · 互动学习</h1>',
              '<h1><i class="fas fa-book"></i> Words &amp; Comparatives · 互动学习</h1>', 1)
h = re.sub(r'<p>2026秋双语八年级 C班 · 第1讲 · \d+ 题 · \d+ 卡牌 \| 双语英语</p>',
           f'<p>2026秋双语八年级 C班 · 第2讲 · {nq} 题 · {nf} 卡牌 | 双语英语</p>', h, count=1)
h = re.sub(r'<span><i class="fas fa-check-circle"[^>]*></i> \d+道测验题</span>',
           f'<span><i class="fas fa-check-circle" style="color:var(--success)"></i> {nq}道测验题</span>', h, count=1)
h = re.sub(r'<span><i class="fas fa-layer-group"></i> \d+张知识卡</span>',
           f'<span><i class="fas fa-layer-group"></i> {nf}张知识卡</span>', h, count=1)
h = re.sub(r'<span><i class="fas fa-exclamation-triangle" style="color:var(--danger)"></i> \d+大易错点</span>',
           f'<span><i class="fas fa-exclamation-triangle" style="color:var(--danger)"></i> {ne}大易错点</span>', h, count=1)
h = re.sub(r'<div class="section-header"><i class="fas fa-sitemap"[^>]*></i> 第一讲 · [^<]*</div>',
           '<div class="section-header"><i class="fas fa-sitemap" style="color:#667eea"></i> 第二讲 · Words &amp; Comparatives（C班）</div>', h, count=1)

# 2) 知识图谱
g0 = h.find('<div class="knowledge-grid">'); g1 = h.find('<div class="teacher-talk">', g0)
cards = ''
for cls, title, lis in KNOW:
    items = ''.join(f'<li>{x}</li>' for x in lis)
    cards += f'      <div class="knowledge-card {cls}"><h3>{title}</h3><ul>{items}</ul></div>\n'
h = h[:g0] + '<div class="knowledge-grid">\n' + cards + '    </div>\n    ' + h[g1:]

# 3) teacher-talk（注意保留 tab-knowledge 的闭合 </div>）
t0 = h.find('<div class="teacher-talk">'); t1 = h.find('<div id="tab-quiz"', t0)
tt = '''<div class="teacher-talk">
      <h4><i class="fas fa-microphone-alt"></i> 🎙️ 课堂要点 · 第二讲（C班 · Words &amp; Comparatives）</h4>
      <p><strong>本讲核心</strong>：2026秋双语八年级 C班第2讲。①核心词汇：<strong>lift（give sb. a lift / take the lift / lift up）、note（记笔记/纸币/证明书/音符）、rubbish</strong>；②句型：<strong>Can/Could you please…?</strong>（请求）与 <strong>Can/Could I…?</strong>（许可）及答语；③语法：<strong>形容词和副词的比较级</strong>（规则/不规则变化、三种比较结构、修饰词、特殊表达）。</p>
      <p><strong>练习册重点</strong>：阅读理解（感恩节儿子"Sure"式简短回复的议论文，答案 CBABC）+ 短文填空 10 空（farewell party：Planning / sort / cover / decorate / familiar / until / add / matter / describe / discovered）。做题技巧：短文填空先按词性归类词库（plan→Planning 动名词作主语；discover→discovered 跟全文时态）。</p>
      <p><strong>易错提醒</strong>：① <strong>very/more 不能修饰比较级</strong>（用 much/a lot/far/even/a little）；② 不规则比较级：bad→worse、little→less、far→farther/further；③ familiar 的介词方向（人 with 物、物 to 人）；④ <strong>not...until</strong> 别漏 not；⑤ cover（覆盖）与 decorate（装饰）辨析；⑥ 短文填空注意首字母大写与时态。</p>
      <p><strong>🎓 老师课堂总结</strong> — 本讲是"词汇+语法"双主线：三个核心词（lift/note/rubbish）要连短语一起记；比较级是本讲重头戏，"三多两少一甚至"的修饰词口诀 + "the more...the more"结构是中考高频考点。练习册的送别派对短文把 10 个考点词汇串成完整情景，订正时把"词库原词 → 文中正确形式"成对背诵。</p>
    </div>
    '''
h = h[:t0] + tt + h[t1:]

# 4) questions / flashcards / errors
q0 = h.find('const questions = ['); q1 = h.find('const flashcards = [', q0)
qdata = [{'q': q, 'opts': o, 'ans': a, 'exp': e} for q, o, a, e in QUIZ]
h = h[:q0] + 'const questions = ' + json.dumps(qdata, ensure_ascii=False, indent=1) + ';\n\n\n' + h[q1:]

f0 = h.find('const flashcards = ['); f1 = h.find('errors = [', f0)
fdata = [{'front': x, 'back': y} for x, y in FLASH]
h = h[:f0] + 'const flashcards = ' + json.dumps(fdata, ensure_ascii=False, indent=1) + ';\n\n\n' + h[f1:]

e0 = h.find('errors = ['); e1 = h.find('function toast', e0)
edata = [{'title': t, 'wrong': w, 'right': r} for t, w, r in ERRORS]
h = h[:e0] + 'errors = ' + json.dumps(edata, ensure_ascii=False, indent=1) + ';\n\n\n\n' + h[e1:]

# 5) localStorage key 隔离 + 文案
h = h.replace('english_lesson1_state_check', 'english_lesson2_state_check')
h = h.replace("QUIZ_PROG_KEY='quiz_progress_english_lesson1'", "QUIZ_PROG_KEY='quiz_progress_english_lesson2'")
h = h.replace("WRONG_HISTORY_KEY='quiz_english_lesson1_wrong'", "WRONG_HISTORY_KEY='quiz_english_lesson2_wrong'")
h = h.replace('第1讲 Nauru &amp; Holidays话题', '第2讲 Words &amp; Comparatives')
h = h.replace('第1讲 Nauru &amp; Holidays | 双语英语', '第2讲 Words &amp; Comparatives | 双语英语')
h = h.replace('共12张知识卡', f'共{nf}张知识卡')
h = re.sub(r'<div class="quiz-stats" id="quizStats">0 / \d+</div>', f'<div class="quiz-stats" id="quizStats">0 / {nq}</div>', h, count=1)

open(OUT_F, 'w', encoding='utf-8').write(h)

# 复验
js = r"""const fs=require('fs');const html=fs.readFileSync('english_lesson2_interactive.html','utf8');const re=/<script[^>]*>([\s\S]*?)<\/script>/g;let m,ok=true;while((m=re.exec(html))){try{new Function(m[1])}catch(e){ok=false;console.log('ERR',e.message)}}console.log(ok?'JS OK':'JS ERR')"""
r = subprocess.run(['node','-e',js], capture_output=True, text=True, cwd=REPO)
hh = open(OUT_F, encoding='utf-8').read()
print(r.stdout.strip())
print(f'题{nq} 卡{nf} 错{ne} 知识{nk}')
print('div:', len(re.findall(r'<div\b', hh)), '/', hh.count('</div>'))
print('残留 lesson1 文案:', hh.count('lesson1'), '| 第1讲:', hh.count('第1讲'))
