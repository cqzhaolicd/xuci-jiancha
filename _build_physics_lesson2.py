#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""_build_physics_lesson2.py — 物理第2讲 运动学拔高（二）：相对速度与过街安全（B卷压轴）
素材: 初二秋季备课笔记2（扫描件，已辨识）+ 老师群通知
基座: physics26q_lesson1_interactive.html
输出: physics26q_lesson2_interactive.html
"""
import re, json, subprocess

REPO = '/home/administrator/xuci-jiancha'
BASE_F = f'{REPO}/physics26q_lesson1_interactive.html'
OUT_F = f'{REPO}/physics26q_lesson2_interactive.html'

KNOW = [
    ("c1", "🧭 相对速度解题两法", [
        "口诀：<strong class=\"hl\">以谁为参照物就把谁看作静止</strong>",
        "法① <strong class=\"hl\">换参考系（换参）</strong>：先求相对速度 V相对，再 t = S相对 / V相对",
        "法② <strong class=\"hl\">距离关系</strong>：用位移等式列方程（与换参结果一致）",
    ]),
    ("c2", "🤝 相遇（相向运动）", [
        "换参：<strong class=\"hl\">V相对 = v₁ + v₂</strong>",
        "时间：t = S / (v₁ + v₂)",
        "距离关系：S₁ + S₂ = S → v₁t + v₂t = S",
    ]),
    ("c3", "🏃 追及（同向运动）", [
        "换参：<strong class=\"hl\">V相对 = v₁ − v₂</strong>（v₁ > v₂）",
        "时间：t = S / (v₁ − v₂)",
        "距离关系：S₁ = S₂ + S → v₁t = v₂t + S",
    ]),
    ("c4", "🚗 超车（同向，注意车身长度）", [
        "相对距离：<strong class=\"hl\">S相对 = l_A + l_B</strong>（两车长之和）",
        "相对速度：V相对 = v_A − v_B",
        "时间：t = (l_A + l_B) / (v_A − v_B)",
    ]),
    ("c5", "🚙 错车（相向，注意车身长度）", [
        "相对距离：<strong class=\"hl\">S相对 = l_A + l_B</strong>",
        "相对速度：<strong class=\"hl\">V相对 = v_A + v_B</strong>（相向相加）",
        "时间：t = (l_A + l_B) / (v_A + v_B)",
    ]),
    ("c6", "⛵ 流水行船", [
        "以地面为参照：顺水 <strong class=\"hl\">V船′ = V船 + V水</strong>；逆水 <strong class=\"hl\">V船′ = V船 − V水</strong>",
        "以水为参照：<strong class=\"hl\">V相对 = V船</strong>（与水速无关）",
    ]),
    ("c7", "🛑 刹车问题：过程分析（B卷压轴）", [
        "<strong class=\"hl\">反应阶段</strong>：发现危险后汽车仍以<strong class=\"hl\">原速匀速</strong>行驶 → S反应 = v·t反应",
        "<strong class=\"hl\">制动阶段</strong>：踩刹车后<strong class=\"hl\">匀减速到停止</strong> → S制动（题给）",
        "总停车距离：<strong class=\"hl\">S总 = S反应 + S制动</strong>",
        "v-t 图：水平段（反应）+ 斜向下直线（制动）",
    ]),
    ("c8", "🚸 安全过街：行人两个临界", [
        "① <strong class=\"hl\">快速临界</strong>（车刚到，人已过）：S人 = <strong class=\"hl\">D/2 + d/2</strong>，S车 = S",
        "② <strong class=\"hl\">慢速临界</strong>（人刚到，车已过）：S人 = <strong class=\"hl\">D/2 − d/2</strong>，S车 = <strong class=\"hl\">S + l</strong>",
        "两临界都满足 t人 = t车（同时刻到达）",
        "D 路宽 / d 人宽 / l 车长 / S 车到横道距离",
    ]),
    ("c9", "🚲 安全过街：自行车版", [
        "① 快速临界：S自 = <strong class=\"hl\">D/2 + d/2 + C</strong>（多一个车身长 C）",
        "② 慢速临界：S自 = D/2 − d/2",
        "⚠️ 自行车起步/通过更慢，临界速度更小，更要注意“慢速临界”那一侧",
    ]),
    ("c10", "📏 安全范围与相撞范围（看清问什么！）", [
        "<strong class=\"hl\">安全范围</strong>：比快速临界<strong class=\"hl\">更快</strong>，或比慢速临界<strong class=\"hl\">更慢</strong>",
        "<strong class=\"hl\">相撞范围</strong>：<strong class=\"hl\">慢速临界 < v < 快速临界</strong>",
        "口诀：<strong class=\"hl\">要么人很慢，要么人很快</strong>",
    ]),
    ("c11", "🎯 本讲方法论（老师强调）", [
        "关键是<strong class=\"hl\">整个过程的分析</strong> + <strong class=\"hl\">临界状态的确定</strong>",
        "物理综合计算的通用逻辑：<strong class=\"hl\">过程分析 + 临界状态分析</strong>",
        "临界 = 恰好通过 / 恰好相遇 → 用 t 相等或位移关系列等式",
    ]),
    ("c12", "⚠️ 本讲易错提醒", [
        "超车/错车忘记加<strong class=\"hl\">车身长度</strong>（S相对 = l_A + l_B）",
        "相向用加法、同向用减法（相对速度方向搞反）",
        "刹车题漏掉<strong class=\"hl\">反应距离</strong>（只算制动距离）",
        "过街题把<strong class=\"hl\">快速临界与慢速临界</strong>弄反，或范围写成开闭不当",
    ]),
]

QUIZ = [
    # 相对速度：概念与方法 8
    ("甲、乙两物体相向运动，速度分别为 v₁、v₂，若以甲为参照物，乙的相对速度大小为",
     ["A. v₁ + v₂", "B. v₁ − v₂", "C. v₂ − v₁", "D. v₁ × v₂"], 0,
     "相向运动 → 相对速度 = <strong>v₁ + v₂</strong>（以一方为参照物，另一方速度相加）。"),
    ("两物体同向运动，v₁ > v₂，后者追前者，相对速度为",
     ["A. v₁ + v₂", "B. v₁ − v₂", "C. v₂ − v₁", "D. 0"], 1,
     "同向运动 → 相对速度 = <strong>v₁ − v₂</strong>。"),
    ("甲、乙相向而行，相距 S，速度 v₁、v₂，相遇时间为",
     ["A. S/(v₁−v₂)", "B. S/(v₁+v₂)", "C. S·(v₁+v₂)", "D. (v₁+v₂)/S"], 1,
     "相遇：t = S / V相对 = <strong>S/(v₁+v₂)</strong>。"),
    ("A 车在前、B 车在后同向行驶（v_B > v_A），B 车要完全超过 A 车，需要通过的相对距离是",
     ["A. l_A", "B. l_B", "C. l_A + l_B", "D. l_A − l_B"], 2,
     "超车：从 B 车头到 A 车尾开始，到 B 车尾离开 A 车头结束 → 相对距离 = <strong>l_A + l_B</strong>。"),
    ("甲、乙两车相向错车，长度 l_A、l_B，速度 v_A、v_B，错车时间为",
     ["A. (l_A+l_B)/(v_A+v_B)", "B. (l_A+l_B)/(v_A−v_B)", "C. (l_A−l_B)/(v_A+v_B)", "D. (l_A+l_B)×(v_A+v_B)"], 0,
     "错车：S相对 = l_A+l_B，V相对 = v_A+v_B → t = <strong>(l_A+l_B)/(v_A+v_B)</strong>。"),
    ("船在流水中顺水航行的对地速度为",
     ["A. V船 − V水", "B. V船 + V水", "C. V船", "D. V水 − V船"], 1,
     "顺水：<strong>V船′ = V船 + V水</strong>（船速与水速同向相加）。"),
    ("以水为参照物时，船的运动速度等于",
     ["A. V船 + V水", "B. V船 − V水", "C. 船自身的速度 V船", "D. 0"], 2,
     "以水为参照物 → <strong>V相对 = V船</strong>（与水速无关）。"),
    ("甲、乙两车同时出发相向而行，甲的速度 10 m/s，乙的速度 15 m/s，出发时相距 500 m，则它们经过多少秒相遇",
     ["A. 20 s", "B. 25 s", "C. 33.3 s", "D. 50 s"], 0,
     "V相对 = 10+15 = 25 m/s → t = 500 ÷ 25 = <strong>20 s</strong>。"),
    # 数值计算 6
    ("甲车以 20 m/s 追赶前方 100 m 处、以 15 m/s 同向行驶的乙车，追上所需时间为",
     ["A. 5 s", "B. 20 s", "C. 25 s", "D. 100 s"], 1,
     "V相对 = 20−15 = 5 m/s → t = 100 ÷ 5 = <strong>20 s</strong>。"),
    ("B 车（长 5 m）以 20 m/s 同向追赶 A 车（长 6 m，15 m/s），B 车完全超过 A 车需要的时间是",
     ["A. 1.1 s", "B. 2.2 s", "C. 2.75 s", "D. 5.5 s"], 1,
     "S相对 = 5+6 = 11 m，V相对 = 20−15 = 5 m/s → t = 11 ÷ 5 = <strong>2.2 s</strong>。"),
    ("A 车（长 6 m）与 B 车（长 8 m）相向错车，速度分别为 15 m/s、10 m/s，错车时间为",
     ["A. 0.56 s", "B. 1.4 s", "C. 2.8 s", "D. 0.28 s"], 0,
     "S相对 = 6+8 = 14 m，V相对 = 15+10 = 25 m/s → t = 14 ÷ 25 = <strong>0.56 s</strong>。"),
    ("小船顺水航行速度 8 m/s，水流速度 2 m/s，则小船逆水航行速度为",
     ["A. 10 m/s", "B. 8 m/s", "C. 6 m/s", "D. 4 m/s"], 3,
     "顺水 V船+V水 = 8 → V船 = 6 m/s → 逆水 = V船−V水 = <strong>4 m/s</strong>。"),
    ("两物体相距 60 m 相向运动，速度均为 0.2 m/s，经过多长时间相遇",
     ["A. 150 s", "B. 300 s", "C. 75 s", "D. 600 s"], 0,
     "V相对 = 0.4 m/s → t = 60 ÷ 0.4 = <strong>150 s</strong>。"),
    ("甲、乙两人从相距 300 m 的两地同时相向出发，甲 1.2 m/s、乙 1.8 m/s，3 分钟后两人相距多少米",
     ["A. 相距 0（已相遇）", "B. 相距 240 m", "C. 相距 180 m", "D. 相距 60 m"], 0,
     "V相对 = 3 m/s，180 s 内相对移动 540 m > 300 m → 早已相遇（3 分钟内相遇），故 <strong>相距 0</strong>。"),
    # 刹车问题 8
    ("在刹车问题中，“反应阶段”汽车的运动情况是",
     ["A. 匀减速运动", "B. 以原来的速度做匀速运动", "C. 静止", "D. 加速运动"], 1,
     "反应阶段：驾驶员尚未踩下刹车 → 汽车以<strong>原速匀速</strong>行驶，对应 S反应。"),
    ("汽车总停车距离等于",
     ["A. 制动距离", "B. 反应距离", "C. 反应距离 + 制动距离", "D. 反应距离 − 制动距离"], 2,
     "<strong>S总 = S反应 + S制动</strong>（从发现危险到完全停下走过的总路程）。"),
    ("汽车以 15 m/s 行驶，驾驶员反应时间为 0.8 s，则反应距离为",
     ["A. 10 m", "B. 12 m", "C. 15 m", "D. 18 m"], 1,
     "S反应 = v·t = 15 × 0.8 = <strong>12 m</strong>。"),
    ("上题中若汽车的制动距离为 22.5 m，则总停车距离为",
     ["A. 30 m", "B. 32.5 m", "C. 34.5 m", "D. 37.5 m"], 2,
     "S总 = 12 + 22.5 = <strong>34.5 m</strong>。"),
    ("汽车以 20 m/s 行驶，反应时间为 0.5 s，则反应距离是",
     ["A. 5 m", "B. 10 m", "C. 20 m", "D. 40 m"], 1,
     "S反应 = 20 × 0.5 = <strong>10 m</strong>。"),
    ("酒后驾车时反应时间变长，其他条件不变，则",
     ["A. 反应距离和总停车距离都变大", "B. 反应距离变大、制动距离不变", "C. 制动距离变大、反应距离不变", "D. 两者都不变"], 0,
     "反应时间变长 → S反应 = v·t<sub>反应</sub> 变大；制动距离由路面/车况决定基本不变，但<strong>总停车距离变大</strong>（更危险）。"),
    ("刹车过程中汽车的 v-t 图像形状是",
     ["A. 一条水平直线", "B. 一条斜向上的直线", "C. 先水平、后斜向下的折线", "D. 一条抛物线"], 2,
     "反应阶段速度不变（<strong>水平段</strong>），制动阶段匀减速到 0（<strong>斜向下直线</strong>）。"),
    ("雨天路面湿滑时，汽车的制动距离会",
     ["A. 变短", "B. 变长", "C. 不变", "D. 先变短后变长"], 1,
     "摩擦力减小 → 减速更慢 → <strong>制动距离变长</strong>，总停车距离变大。"),
    # 安全过街 8
    ("安全过街问题中，“快速临界”（车刚到、人已过）时人的位移是",
     ["A. D/2 + d/2", "B. D/2 − d/2", "C. D + d", "D. D/2"], 0,
     "人已完全通过马路（还要留出人自己的半个宽度）→ S人 = <strong>D/2 + d/2</strong>，同时车走 S。"),
    ("“慢速临界”（人刚到、车已过）时，汽车的位移是",
     ["A. S", "B. S + l", "C. S − l", "D. S + D"], 1,
     "车必须<strong>完全通过</strong>人行横道 → S车 = <strong>S + l</strong>（多走一个车身长）。"),
    ("安全过街时，行人安全通过的速度范围是",
     ["A. 比快速临界更慢，或比慢速临界更快", "B. 比快速临界更快，或比慢速临界更慢", "C. 一定介于两个临界之间", "D. 与两个临界无关"], 1,
     "安全范围 = <strong>比快速临界更快，或比慢速临界更慢</strong>（口诀：要么人很慢，要么人很快）。"),
    ("行人会在马路上与车相撞的速度范围是",
     ["A. v > 快速临界", "B. v < 慢速临界", "C. 慢速临界 < v < 快速临界", "D. v 可取任意值"], 2,
     "相撞范围：<strong>慢速临界 < v < 快速临界</strong>（速度介于两者之间时人会被车撞）。"),
    ("自行车过街的“快速临界”位移比行人的多一个",
     ["A. 车身长 C", "B. 车宽", "C. 马路宽 D", "D. 反应距离"], 0,
     "自行车需整体通过 → S自 = D/2 + d/2 + <strong>C（自行车长度）</strong>。"),
    ("马路宽 D = 6 m、行人宽 d = 0.4 m，汽车距人行横道 S = 15 m、车长 l = 5 m，车速 15 m/s。若行人快步通过（快速临界），其最小速度为",
     ["A. 2.1 m/s", "B. 3.2 m/s", "C. 4.0 m/s", "D. 1.6 m/s"], 1,
     "快速临界：S人 = D/2+d/2 = 3+0.2 = 3.2 m；t车 = S/v车 = 15/15 = 1 s → v人 = 3.2 ÷ 1 = <strong>3.2 m/s</strong>（比这更快才安全）。"),
    ("同上条件，若人通过很慢（慢速临界，人刚到车已过），其最大速度为",
     ["A. 2.1 m/s", "B. 3.2 m/s", "C. 4.0 m/s", "D. 0.75 m/s"], 0,
     "慢速临界：S人 = D/2−d/2 = 3−0.2 = 2.8 m；t车 = (S+l)/v车 = 20/15 = 4/3 s → v人 = 2.8 ÷ (4/3) = <strong>2.1 m/s</strong>（比这更慢才安全）。"),
    ("由上两题可知，该行人在 2.1 m/s ~ 3.2 m/s 之间通过马路时会",
     ["A. 安全通过", "B. 与汽车相撞", "C. 视情况而定", "D. 汽车会停下"], 1,
     "此区间正是<strong>相撞范围</strong>（慢速临界 2.1 < v < 快速临界 3.2）——不快不慢最危险。"),
    ("解刹车/过街这类压轴题的关键是",
     ["A. 直接套公式", "B. 过程分析 + 临界状态的确定", "C. 画出图形即可", "D. 记住答案"], 1,
     "老师强调：关键是<strong>整个过程的分析</strong>与<strong>临界状态的确定</strong>——物理综合计算的通用逻辑。"),
    ("关于“临界状态”，下列说法正确的是",
     ["A. 临界就是任意取一个时刻", "B. 临界指“恰好通过 / 恰好相遇”的状态，此时通常用 t 相等或位移关系列等式", "C. 临界状态不需要计算", "D. 临界状态一定发生在最后"], 1,
     "临界 = “恰好”状态（恰好通过、恰好相遇），据此<strong>列等式（t人 = t车 或位移关系）</strong>求解。"),
    ("做这类压轴题时，读题后第一步应当",
     ["A. 立刻代公式计算", "B. 先分析物体的运动过程（分阶段）并找出可能的临界状态", "C. 先算总时间", "D. 先猜答案"], 1,
     "先<strong>过程分析（分阶段）→ 确定临界状态 → 列式求解</strong>，这是 B 卷压轴题的标准解法流程。"),
    ("老师布置的作业与复习建议是",
     ["A. 只做选择题", "B. 作业是压轴题，计算较费时间，务必先复习例题再做", "C. 不用复习直接做", "D. 只背公式"], 1,
     "老师通知：作业布置的是<strong>压轴题</strong>（计算较费时间），<strong>务必先复习例题再做作业</strong>；这是月考/半期压轴常考题型。"),
]

FLASH = [
    ("相对速度两法是什么？口诀？",
     "① <strong>换参考系</strong>：求 V相对 后 t = S相对/V相对；② <strong>距离关系</strong>：位移等式。口诀：<strong>以谁为参照物就把谁看作静止</strong>。"),
    ("相遇与追及的时间公式？",
     "相遇（相向）：V相对 = v₁+v₂，t = S/(v₁+v₂)；追及（同向）：V相对 = v₁−v₂，t = S/(v₁−v₂)。"),
    ("超车与错车的相对距离和相对速度？",
     "两者 S相对 = <strong>l_A + l_B</strong>；超车（同向）V相对 = v_A−v_B；错车（相向）V相对 = v_A+v_B。"),
    ("流水行船的速度关系？",
     "顺水 V船+V水；逆水 V船−V水；以水为参照物时 V相对 = V船（与水速无关）。"),
    ("刹车问题分哪两个阶段？",
     "<strong>反应阶段</strong>（原速匀速，S反应 = v·t反应）+ <strong>制动阶段</strong>（匀减速到停，S制动）；S总 = S反应 + S制动。"),
    ("影响停车距离的因素？",
     "车速越大、反应时间越长（酒驾/疲劳）→ S反应 越大；路面越滑 → 制动距离越大；两者叠加使总停车距离变大。"),
    ("安全过街的两个临界（行人）？",
     "快速临界（车刚到、人已过）：S人 = <strong>D/2+d/2</strong>，S车 = S；慢速临界（人刚到、车已过）：S人 = <strong>D/2−d/2</strong>，S车 = <strong>S+l</strong>。"),
    ("自行车版与行人版的区别？",
     "自行车快速临界多一个车身长：S自 = D/2+d/2+<strong>C</strong>；慢速临界与行人相同（D/2−d/2）。"),
    ("安全范围与相撞范围？",
     "安全：比快速临界<strong>更快</strong>或比慢速临界<strong>更慢</strong>；相撞：<strong>慢速临界 < v < 快速临界</strong>。"),
    ("过街题要看清什么？",
     "看清题目问的是**安全范围**还是**相撞范围**，以及求的是哪一侧临界（速度快慢两侧答案不同）。"),
    ("本讲核心方法论？",
     "<strong>过程分析 + 临界状态分析</strong>——先分阶段分析运动过程，再抓住“恰好”的临界状态列等式。"),
    ("解答压轴题的标准流程？",
     "读题 → <strong>过程分析（分阶段）</strong> → <strong>确定临界状态</strong> → 用 t 相等/位移关系列式 → 求解并检验范围。"),
]

ERRORS = [
    ("❌ 超车/错车忘记加车身长度",
     "t = S/(v_A−v_B)，只算初始距离，忽略两车长度。",
     "超车与错车的相对距离都是 <strong>l_A + l_B</strong>：t = (l_A+l_B)/(v_A±v_B)。"),
    ("❌ 同向/相向的相对速度用错",
     "追及用 v₁+v₂，相遇用 v₁−v₂。",
     "同向相减（v₁−v₂）、相向相加（v₁+v₂）——记住“相向靠近得快，同向靠近得慢”。"),
    ("❌ 刹车题漏掉反应距离",
     "直接用制动距离当作停车距离。",
     "总停车距离 = <strong>S反应 + S制动</strong>；S反应 = v × t反应，别漏这一步。"),
    ("❌ 过街题两个临界弄反",
     "把快速临界的位移写成 D/2−d/2。",
     "<strong>快速临界</strong>（人已完全通过，要加上人的半个宽度）：D/2+<strong>d/2</strong>；<strong>慢速临界</strong>（人刚到路边）：D/2−d/2。慢速临界时车要多走一个车身长 S+l。"),
    ("❌ 范围写错或漏写一侧",
     "答“v > 快速临界”就说安全（漏掉“比慢速临界更慢也安全”）。",
     "安全范围有<strong>两侧</strong>：v > 快速临界 <strong>或</strong> v < 慢速临界；中间区间是<strong>相撞范围</strong>。"),
    ("❌ 不分析过程直接套公式",
     "读完题就直接代 v=s/t，忽视分阶段（反应+制动）或临界。",
     "先<strong>过程分析</strong>（分段、画 v-t 图），再<strong>找临界状态</strong>（恰好通过/相遇），最后列式。"),
    ("❌ 流水行船参照物混乱",
     "顺水仍用 V船−V水，或以为水流会影响“以水为参照物”的船速。",
     "顺水加、逆水减；以水为参照物时船速就是 <strong>V船</strong>（与水速无关）。"),
]

h = open(BASE_F, encoding='utf-8').read()
nq, nf, ne, nk = len(QUIZ), len(FLASH), len(ERRORS), len(KNOW)

h = re.sub(r'<title>[^<]*</title>', '<title>🚦 相对速度与过街安全 · 互动学习</title>', h, count=1)
h = re.sub(r'<h1[^>]*>.*?</h1>', '<h1><i class="fas fa-traffic-light"></i> 相对速度与过街安全 · 互动学习</h1>', h, count=1, flags=re.DOTALL)
h = re.sub(r'<p>2026秋物理博学班 第1讲 · \d+ 题 · \d+ 卡牌 \| 博学班物理</p>',
           f'<p>2026秋初二物理 第2讲（B卷压轴） · {nq} 题 · {nf} 卡牌 | 运动学拔高二</p>', h, count=1)
h = re.sub(r'<span><i class="fas fa-check-circle"[^>]*></i> \d+道测验题</span>',
           f'<span><i class="fas fa-check-circle" style="color:var(--success)"></i> {nq}道测验题</span>', h, count=1)
h = re.sub(r'<span><i class="fas fa-layer-group"></i> \d+张知识卡</span>',
           f'<span><i class="fas fa-layer-group"></i> {nf}张知识卡</span>', h, count=1)
h = re.sub(r'<span><i class="fas fa-exclamation-triangle" style="color:var(--danger)"></i> \d+大易错点</span>',
           f'<span><i class="fas fa-exclamation-triangle" style="color:var(--danger)"></i> {ne}大易错点</span>', h, count=1)

g0 = h.find('<div class="knowledge-grid">'); g1 = h.find('<div class="teacher-talk">', g0)
assert g0 > 0 and g1 > g0
cards = ''
for cls, title, lis in KNOW:
    items = ''.join(f'<li>{x}</li>' for x in lis)
    cards += f'      <div class="knowledge-card {cls}"><h3>{title}</h3><ul>{items}</ul></div>\n'
h = h[:g0] + '<div class="knowledge-grid">\n' + cards + '    </div>\n    </div>\n    ' + h[g1:]

t0 = h.find('<div class="teacher-talk">'); t1 = h.find('<div id="tab-quiz"', t0)
tt = '''<div class="teacher-talk">
      <h4><i class="fas fa-microphone-alt"></i> 🎙️ 课堂要点 · 第二讲（运动学拔高二 · B卷压轴）</h4>
      <p><strong>本讲核心</strong>：① <strong>相对速度五题型</strong>——相遇（v₁+v₂）、追及（v₁−v₂）、超车与错车（相对距离 = l_A+l_B）、流水行船（顺加逆减）；两法：换参考系 / 距离关系。② <strong>刹车问题</strong>——反应阶段（原速匀速）+ 制动阶段（匀减速），S总 = S反应 + S制动，看 v-t 图。③ <strong>安全过街</strong>（B7 压轴）——快速临界（人已过：D/2+d/2，车走 S）与慢速临界（人刚到：D/2−d/2，车走 S+l），自行车快速临界再加车身长 C。</p>
      <p><strong>范围判断（最关键）</strong>：<strong>安全 = 比快速临界更快，或比慢速临界更慢</strong>；<strong>相撞 = 慢速临界 &lt; v &lt; 快速临界</strong>。口诀：<strong>要么人很慢，要么人很快</strong>。</p>
      <p><strong>🎓 老师强调的方法论</strong>：关键是<strong>整个过程的分析</strong>与<strong>临界状态的确定</strong>——初中物理后面所有综合计算都是同一逻辑：<strong>过程分析 + 临界状态分析</strong>。这是<strong>月考和半期压轴常考题型</strong>。</p>
      <p><strong>📝 作业</strong>：布置的是讲义压轴例题（计算较费时间）——<strong>务必先复习例题再做作业</strong>；老师会在大家完成后发详解。</p>
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

h = h.replace('physics26q_lesson1_state_check', 'physics26q_lesson2_state_check')
h = h.replace("QUIZ_PROG_KEY='quiz_progress_physics26q_lesson1'", "QUIZ_PROG_KEY='quiz_progress_physics26q_lesson2'")
h = h.replace("WRONG_HISTORY_KEY='quiz_physics26q_lesson1_wrong'", "WRONG_HISTORY_KEY='quiz_physics26q_lesson2_wrong'")
h = h.replace('第1讲 运动学计算（一）', '第2讲 相对速度与过街安全')
h = h.replace('运动学计算（一） | 博学班物理', '相对速度与过街安全 | 博学班物理')
h = h.replace('物理 · 第1讲', '物理 · 第2讲')
h = re.sub(r"subject:'[^']*'", "subject:'物理(2026秋)'", h, count=2)
h = re.sub(r"chapter:'[^']*'", "chapter:'第2讲 相对速度与过街安全（B卷压轴）'", h, count=2)
h = re.sub(r"tags:'[^']*'", "tags:'物理,2026秋,第2讲,相对速度,刹车,过街安全,临界分析'", h, count=2)
h = re.sub(r'<div class="quiz-stats" id="quizStats">0 / \d+</div>', f'<div class="quiz-stats" id="quizStats">0 / {nq}</div>', h, count=1)
h = re.sub(r'共\d+张知识卡', f'共{nf}张知识卡', h, count=1)
open(OUT_F, 'w', encoding='utf-8').write(h)

js = r"""const fs=require('fs');const html=fs.readFileSync('physics26q_lesson2_interactive.html','utf8');const re=/<script[^>]*>([\s\S]*?)<\/script>/g;let m,ok=true;while((m=re.exec(html))){try{new Function(m[1])}catch(e){ok=false;console.log('ERR',e.message)}}console.log(ok?'JS OK':'JS ERR')"""
r = subprocess.run(['node','-e',js], capture_output=True, text=True, cwd=REPO)
hh = open(OUT_F, encoding='utf-8').read()
print(r.stdout.strip())
print(f'题{nq} 卡{nf} 错{ne} 知识{nk}')
print('div:', len(re.findall(r'<div\b', hh)), '/', hh.count('</div>'))
print('残留 运动学计算（一）:', hh.count('运动学计算（一）'), '| lesson1:', hh.count('lesson1'), '| 第1讲:', hh.count('第1讲'))
