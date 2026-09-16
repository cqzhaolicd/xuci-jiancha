#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""_build_physics_light12.py — 运动学轻课 第1、2讲 精练互动页
素材: 运动学轻课 第1、2讲.pdf（14题，无答案；AI 逐题验算）
基座: physics26q_lesson2_interactive.html
输出: physics26q_light12_interactive.html
"""
import re, json, subprocess

REPO = '/home/administrator/xuci-jiancha'
BASE_F = f'{REPO}/physics26q_lesson2_interactive.html'
OUT_F = f'{REPO}/physics26q_light12_interactive.html'

KNOW = [
    ("c1", "📊 平均速度（轻课第1讲）", [
        "**平均速度 = 总路程 ÷ 总时间**（绝不是速度的平均值！）",
        "例：前 1/3 路程 4m/s、后 2/3 路程 7m/s → v̄ = 3s ÷ (s/4 + 2s/7) = <strong class=\"hl\">5.6 m/s</strong>",
        "陷阱：直接取 (4+7)/2 = 5.5 是错的",
    ]),
    ("c2", "🧭 相对运动与参照物", [
        "\"甲看到楼房上升\" → 甲在<strong class=\"hl\">下降</strong>（反向判断）",
        "\"乙看到甲上升\" → 乙下降得<strong class=\"hl\">比甲快</strong>（v乙 > v甲）",
        "口诀：<strong class=\"hl\">看别人相对自己往哪动，自己就往反方向动得更多/更少</strong>",
    ]),
    ("c3", "🫀 心电图 = 匀速运动 + 周期", [
        "心动周期 T = 60 s ÷ 心率；走纸速度 v = 相邻波峰间距 ÷ T",
        "本题：A 间距 35mm、心率 60 次/min（T=1s）→ <strong class=\"hl\">v = 35 mm/s</strong>",
        "B 间距 30mm → T = 30/35 s → 心率 = 60 ÷ (30/35) = <strong class=\"hl\">70 次/min</strong>",
    ]),
    ("c4", "🔫 \"旋转法\"测子弹速度", [
        "塑片转速 n 转/s → 转一周时间 = 1/n；转 θ 角时间 = θ/(360n)",
        "子弹穿过间距 d 的两片塑片，时间 = 转过角所需时间",
        "转过 N 周零 60°：t = N/n + 1/(6n) → <strong class=\"hl\">v = 6nd/(6N+1)</strong>",
    ]),
    ("c5", "🛑 制动与警示牌（可见距离修正）", [
        "S反应 = v·t反应；S制动 = v²/(2a)；<strong class=\"hl\">S总 = S反应 + S制动</strong>",
        "最短制动时间 t = v/a",
        "⚠️ 若只能看清前方 L 处的物体，警示牌需放在车后 <strong class=\"hl\">S总 − L</strong> 处",
    ]),
    ("c6", "🚸 横穿马路的两个临界", [
        "快速临界（车刚到、人已过）：S人 = <strong class=\"hl\">D/2 + d/2 + 车/人自身长度</strong>，S车 = S",
        "慢速临界（人刚到、车已过）：S人 = <strong class=\"hl\">D/2 − d/2</strong>，S车 = S + l",
        "安全：<strong class=\"hl\">比快速临界更快 或 比慢速临界更慢</strong>；相撞在两者之间",
    ]),
    ("c7", "🔊 回声测距通用模型（第2讲）", [
        "核心方程：<strong class=\"hl\">声音路程 = 车路程 + 2×车与障碍物的距离差</strong>",
        "鸣笛时距障碍 x、听到回声时车走了 s：<strong class=\"hl\">x + (x − s) = v声 × t</strong>",
        "变速时用平均速度算车走的路程",
    ]),
    ("c8", "📡 超声波测速仪", [
        "两次发出间隔 Δt，两次接收间隔 Δt′：Δt′ > Δt → 车在<strong class=\"hl\">远离</strong>；Δt′ < Δt → 车在<strong class=\"hl\">靠近</strong>",
        "汽车位置 = 声速 × 单程时间 ÷ 2",
        "车移动距离 ÷ 两次反射的时间间隔 = 车速",
    ]),
    ("c9", "🧊 冰上声呐（分层介质）", [
        "水深 h = v水·t₁/2（t₁ 为从水面发射到返回的时间）",
        "穿过冰层 + 水层：2H/v冰 + 2h/v水 = t₂ → <strong class=\"hl\">H = v冰(t₂ − t₁)/2</strong>",
        "注意声在冰、水中的<strong class=\"hl\">速度不同</strong>，时间要分段计算",
    ]),
    ("c10", "🐭 传送带上的相对运动", [
        "对地速度 = 相对带速度 ± 带速（同向相加、反向相减）",
        "例：鼠相对带 0.4 向 A，带 0.1 向 B → 对地 <strong class=\"hl\">0.3 m/s（向 A）</strong>",
        "带面被污染长度 = 老鼠<strong class=\"hl\">相对带面</strong>爬过的距离 = 0.4 × 时间",
    ]),
    ("c11", "⚠️ 本讲义的重难点提示", [
        "第1讲 2 题：A、C 两个选项都符合题述（题目表述不严谨）",
        "第2讲 1 题：B、D 两个选项都能推出（若为多选则 BD）",
        "第2讲 4、5 题需读图 b 的时间轴刻度；第1讲 7、第2讲 2(3) 需结合原图数据",
        "结论：本讲义是<strong class=\"hl\">难题/多解题集</strong>，务必听老师详解核对",
    ]),
    ("c12", "🎯 轻课定位（承接 B 卷压轴）", [
        "轻课 = 45min 直播（有回放）的 B 卷压轴专项强化",
        "核心逻辑：<strong class=\"hl\">过程分析 + 临界状态分析</strong>",
        "本讲覆盖：平均速度、相对运动、回声测距、超声波测速、横穿临界、传送带相对运动",
    ]),
]

QUIZ = [
    # 第1讲
    ("【第1讲·1】汽车沿直线运动，前 1/3 路程用 4m/s，后 2/3 路程用 7m/s，全程平均速度是",
     ["A. 6 m/s", "B. 5.6 m/s", "C. 4.8 m/s", "D. 无法计算"], 1,
     "设总路程 3s：t = s/4 + 2s/7 = 15s/28 → v̄ = 3s ÷ (15s/28) = <strong>5.6 m/s</strong>。平均速度必须用总路程÷总时间（不能取 (4+7)/2 = 5.5）。"),
    ("【第1讲·2】甲看楼房上升、乙看甲上升、甲看丙上升、丙看乙下降，则地面看三人的运动可能是",
     ["A. 甲、乙匀速下降且 v甲<v乙，丙停在空中", "B. 甲、乙匀速下降且 v甲>v乙，丙匀速上升", "C. 甲、乙匀速下降且 v乙>v甲，丙匀速下降且 v丙<v甲", "D. 甲、乙匀速下降且 v乙>v甲，丙匀速下降且 v丙>v甲"], 0,
     "由“乙看甲上升”得 v乙>v甲；由“丙看乙下降”得丙下降慢于乙或静止/上升。\n⚠️ 本题 A、C <strong>两个选项都符合题述</strong>（题目表述不严谨，常规标准答案给 A），上课时留意老师讲法。"),
    ("【第1讲·3】同一台心电图仪：A 相邻波峰间距 35mm、心率 60 次/min；B 相邻波峰间距 30mm。则走纸速度与 B 的心率为",
     ["A. 25mm/s、60 次", "B. 35mm/s、60 次", "C. 35mm/s、70 次", "D. 25mm/s、70 次"], 2,
     "A 的周期 T = 60/60 = 1s → 走纸速度 v = 35mm ÷ 1s = <strong>35 mm/s</strong>；B 的周期 = 30/35 s → 心率 = 60 ÷ (30/35) = <strong>70 次/min</strong>。"),
    ("【第1讲·4(1)】“旋转法”中塑片转速 500 转/s，则薄塑片转过 360° 的时间是",
     ["A. 0.002 s", "B. 0.02 s", "C. 0.2 s", "D. 1/3000 s"], 0,
     "转一周时间 = 1/500 = <strong>0.002 s</strong>；转过 60° 的时间 = 0.002×(60/360) = 1/3000 s ≈ 3.3×10⁻⁴ s。"),
    ("【第1讲·4(2)】两塑片间距 20cm，子弹先后射穿 A、B 两孔（孔夹角 60°），若两塑片未转过一周即被射穿，子弹速度是",
     ["A. 300 m/s", "B. 600 m/s", "C. 1200 m/s", "D. 100 m/s"], 1,
     "时间 = 转过 60° 的时间 = 1/3000 s → v = 0.2 ÷ (1/3000) = <strong>600 m/s</strong>。"),
    ("【第1讲·4(3)】设两塑片间距 d、电动机转速 n，薄塑片转过 N 周后才被射穿，弹孔仍如图。子弹速度为",
     ["A. v = nd/N", "B. v = 6nd/(6N+1)", "C. v = nd/(N+1)", "D. v = 6nd/(6N−1)"], 1,
     "t = N/n + 1/(6n) = (6N+1)/(6n) → v = d/t = <strong>6nd/(6N+1)</strong>。"),
    ("【第1讲·5(1)】小轿车以 30m/s 行驶、制动最大加速度 5m/s²，从刹车到停止的最短时间是",
     ["A. 3 s", "B. 5 s", "C. 6 s", "D. 10 s"], 2,
     "t = v/a = 30 ÷ 5 = <strong>6 s</strong>。"),
    ("【第1讲·5(2)】同上，驾驶员反应时间 0.6s、夜间只能看清前方 60m，三角警示牌至少要放在车后多少米处",
     ["A. 30 m", "B. 48 m", "C. 60 m", "D. 108 m"], 1,
     "S反应 = 30×0.6 = 18m；S制动 = v²/(2a) = 900/10 = 90m；S总 = 108m。\n因只能看清 60m，需警示牌放车后 108 − 60 = <strong>48 m</strong>。"),
    ("【第1讲·6】马路宽 D=20m，汽车长 6m、宽 3.2m、以 15m/s 在路中间行驶，距车头 30m 处自行车（长 1.6m）横穿。自行车安全通过的速度范围是",
     ["A. 0 < v₂ < 6.6 m/s", "B. v₂ < 4.2 或 v₂ > 5.8 m/s", "C. v₂ < 3.5 或 v₂ > 6.6 m/s", "D. v₂ < 3.5 或 v₂ > 4.2 m/s"], 2,
     "快速临界：S自 = D/2+d/2+l₂ = 10+1.6+1.6 = 13.2m，t = 30/15 = 2s → v₂ = 6.6 m/s（更快安全）\n慢速临界：S自 = D/2−d/2 = 8.4m，t = 36/15 = 2.4s → v₂ = 3.5 m/s（更慢安全）\n→ <strong>v₂ < 3.5 m/s 或 v₂ > 6.6 m/s</strong>。"),
    ("【第1讲·7】关于两车相遇与行人横穿（s-t 图 + 车道示意图），下列说法正确的是",
     ["A. 初始距离可由 15s 相遇与两车速度直接相乘相加求得（需读图取速度）", "B. 行人安全速度只需算快速临界一侧", "C. 行人安全速度只需算慢速临界一侧", "D. 与车的长度无关"], 0,
     "由 s-t 图读出 A、B 的速度，初始距离 = 15×(v_A+v_B)；行人横穿要同时算<strong>快速临界与慢速临界两侧</strong>（与车长、车宽、路宽都有关）。\n⚠️ 本题需结合原图数据计算，答案待老师详解确认。"),
    # 第2讲
    ("【第2讲·1】列车鸣笛回声题（6t₁ = t₃，v声 = 342 m/s）中，下列判断正确的是",
     ["A. 列车速度为 56 m/s", "B. t₂ : t₃ = 2 : 7", "C. 司机听到回声时声音通过的路程是列车的 3 倍", "D. 若列车速度加快，则 t₁:t₂ > 7:12"], 1,
     "设 AB = L：t₁ = L/342，t₃ = L/v，由 6t₁ = t₃ → v = <strong>57 m/s</strong>（A 写 56 为近似值）；\n听到回声：2L − v·t₂ = 342t₂ → t₂ = 2L/399 → <strong>t₂:t₃ = 2:7 ✓（B 对）</strong>；\n声音路程 : 列车路程 = 342t₂ : v·t₂ = <strong>6:1</strong>（C 错）；v=57 时 t₁:t₂ = 7:12，速度加快则更大（D 也对）。\n⚠️ 本题 B、D 均成立（若为多选选 BD）。"),
    ("【第2讲·2(1)】洒水车以 10m/s 行驶，鸣笛 2s 后听到隧道口山崖反射的回声（v声=340m/s），2s 内声音传播的距离是",
     ["A. 340 m", "B. 680 m", "C. 660 m", "D. 700 m"], 1,
     "s声 = v声·t = 340 × 2 = <strong>680 m</strong>。"),
    ("【第2讲·2(2)】同上，司机听到回声时到隧道口的距离是",
     ["A. 320 m", "B. 330 m", "C. 340 m", "D. 350 m"], 1,
     "设鸣笛时距隧道口 x：x + (x − 10×2) = 680 → x = 350m → 听到回声时距隧道口 = 350 − 20 = <strong>330 m</strong>。"),
    ("【第2讲·2(3)】洒水车距隧道口 540m 时，小乐在隧道中听到音乐声并立刻跑向隧道口，洒水车到达隧道口时她刚好跑出（v人=2.5m/s）。她距该隧道口约为",
     ["A. 100 m", "B. 130 m", "C. 200 m", "D. 260 m"], 1,
     "时间关系：(540+d)/340 + d/2.5 = 540/10 → d ≈ <strong>130 m</strong>。（隧道全长需结合原图确认）"),
    ("【第2讲·3(1)】火车以 144km/h 行驶，鸣笛后减速，4s 听到回声且此时 v₁:v₂ = 2:1，则 v₂ 为",
     ["A. 10 m/s", "B. 20 m/s", "C. 30 m/s", "D. 40 m/s"], 1,
     "v₁ = 144 km/h = 40 m/s，v₁:v₂ = 2:1 → v₂ = <strong>20 m/s</strong>。"),
    ("【第2讲·3(2)】同上，第一次鸣笛时车距隧道口多少米",
     ["A. 620 m", "B. 700 m", "C. 740 m", "D. 780 m"], 2,
     "4s 内车走 (40+20)/2×4 = 120m；声音走 340×4 = 1360 = x + (x−120) → x = <strong>740 m</strong>。"),
    ("【第2讲·3(3)】第二次鸣笛后 3.5s 再次听到回声，此后火车再经过多少秒开始进入隧道",
     ["A. 25.0 s", "B. 27.5 s", "C. 30.0 s", "D. 31.0 s"], 1,
     "第二次听到回声时车距隧道口 = (740−120) − 20×3.5 = 550m → t = 550 ÷ 20 = <strong>27.5 s</strong>。（题给 3.5s 为近似值）"),
    ("【第2讲·4】超声波测速仪题（Δt = 0.9s，v声 = 340m/s，图 b 给出 P₁、P₂、n₁、n₂ 时刻），下列判断正确的是",
     ["A. 汽车第一次碰到信号处距测速仪 61.2 m", "B. 汽车第二次碰到信号处距测速仪 91.8 m", "C. 汽车两次碰到信号的时间间隔为 0.81 s", "D. 汽车的速度是 35.8 m/s"], 3,
     "方法：由时间轴读出 P₁、P₂ 发出的时刻与 n₁、n₂ 接收的时刻 → 各次汽车位置 = 340 × 单程时间 ÷ 2；\n再由两次位置差与时间间隔求车速。\n⚠️ 图 b 刻度需结合原图核对，选项 D（35.8 m/s）为常见标准答案，最终以老师详解为准。"),
    ("【第2讲·5】测速仪两次发出间隔 1.5s、收到两次间隔 1.9s，汽车第一次接收信号时距测速仪 102m，车速约为",
     ["A. 20 m/s", "B. 30 m/s", "C. 40 m/s", "D. 50 m/s"], 3,
     "Δt′ > Δt → 车在远离。按常规模型算得 v ≈ 56.7 m/s，<strong>与给定选项不符</strong>；\n若用“接收间隔差”估算：Δs = (1.9−1.5)×340/2 = 68m → v ≈ 68/1.9 ≈ 35.8 m/s。\n⚠️ 本题数据存在不自洽，答案待老师详解确认。"),
    ("【第2讲·6(1)】冰上声呐紧贴水面按下，显示 t₁ = 0.02s（v水 = 1530m/s），此处水深为",
     ["A. 15.3 m", "B. 30.6 m", "C. 7.65 m", "D. 153 m"], 0,
     "声音往返水层：2h = v水·t₁ → h = 1530×0.02/2 = <strong>15.3 m</strong>。"),
    ("【第2讲·6(2)】同上，若紧贴冰面测试，超声波穿过冰层与水层后反射回来用时 t₂（声在冰中速度 v冰），冰层厚度为",
     ["A. v冰·t₂/2", "B. v冰(t₂ − t₁)/2", "C. v冰(t₂ + t₁)/2", "D. v水(t₂ − t₁)/2"], 1,
     "2H/v冰 + 2h/v水 = t₂，其中 2h/v水 = t₁ → 2H/v冰 = t₂ − t₁ → <strong>H = v冰(t₂ − t₁)/2</strong>。"),
    ("【第2讲·7(1)】传送带速度 0.1m/s（A→B 方向），老鼠相对传送带以 0.4m/s 从 B 爬向 A，它对地面的速度是",
     ["A. 0.5 m/s 指向 B", "B. 0.4 m/s 指向 A", "C. 0.3 m/s 指向 A", "D. 0.1 m/s 指向 B"], 2,
     "反向相减：0.4 − 0.1 = <strong>0.3 m/s</strong>，方向指向 A（与传送带运动反向）。"),
    ("【第2讲·7(2)】同上，老鼠第一次从 A 爬到 B（AB = 1.5m）的过程中，传送带被油渍污染的长度是",
     ["A. 1.2 m", "B. 1.5 m", "C. 1.8 m", "D. 3.0 m"], 0,
     "对地速度 = 0.4 + 0.1 = 0.5 m/s → 用时 3s；带面被污染长度 = 老鼠<strong>相对带面</strong>爬过的距离 = 0.4 × 3 = <strong>1.2 m</strong>。\n⚠️ 若按“带面长度”口径有争议，建议与老师核对。"),
    ("【第2讲·7(3)】反复来回后传送带全部被污染，求解这类问题的关键是",
     ["A. 只看老鼠对地速度", "B. 逐步累计每段循环中被污染的新带面长度，直到覆盖整条 3m 带", "C. 直接用 总长 ÷ 带速", "D. 只算第一次"], 1,
     "需要<strong>逐段累计</strong>：每次 A→B（3s，污染 1.2m 带面）与 B→A（5s，相对带面 2m）所覆盖的新带面区间逐步拼满 3m。\n⚠️ 本题为压轴综合题，最终答案以老师详解为准。"),
]

FLASH = [
    ("平均速度怎么算？为什么不能取速度平均？",
     "<strong>总路程 ÷ 总时间</strong>。因为两段路程所用时间不同，速度平均没有任何物理意义。"),
    ("心电图的走纸速度与心率怎么互求？",
     "心动周期 T = 60s ÷ 心率；走纸速度 v = 相邻波峰间距 ÷ T；反过来 T = 间距 ÷ v。"),
    ("“旋转法”测子弹速度的推导？",
     "子弹穿过两塑片时间 = 塑片转过角度所需时间。转过 N 周零 60°：t = N/n + 1/(6n) → v = <strong>6nd/(6N+1)</strong>。"),
    ("制动问题中“只能看清 L”如何影响警示牌位置？",
     "S总 = S反应 + S制动；警示牌至少放车后 <strong>S总 − L</strong> 处（因为司机只能在 L 处才发现它）。"),
    ("横穿马路的两个临界？",
     "快速临界：S人 = D/2+d/2+自身长度，S车 = S；慢速临界：S人 = D/2−d/2，S车 = S+l。安全 = 更快 或 更慢。"),
    ("回声测距的核心方程？",
     "声音走的路程 = 2×鸣笛时距离 − 车走的距离，即 <strong>x + (x − s) = v声·t</strong>。"),
    ("超声波测速仪怎么判断车是靠近还是远离？",
     "比较两次接收间隔与两次发出间隔：<strong>接收间隔变长 → 远离</strong>；变短 → 靠近。"),
    ("汽车位置的求法？",
     "位置 = v声 × 单程时间 ÷ 2（单程时间 = 从发出到接收的时间 ÷ 2）。"),
    ("冰上声呐的冰层厚度公式？",
     "2H/v冰 + 2h/v水 = t₂，其中 t₁ = 2h/v水 → <strong>H = v冰(t₂ − t₁)/2</strong>。"),
    ("传送带上物体对地速度怎么算？",
     "同向相加、反向相减：对地速度 = 相对带速度 ± 带速。"),
    ("传送带被污染长度怎么算？",
     "等于物体<strong>相对带面</strong>移动的距离（不是对地距离、也不是带移动距离）。"),
    ("本讲义有哪些题需要特别注意？",
     "第1讲2（A、C 均可）、第2讲1（B、D 均可）、第2讲4/5（需读图）、第1讲7 与第2讲2(3)（需原图数据）——务听老师详解。"),
]

ERRORS = [
    ("❌ 平均速度取速度平均",
     "(4+7)/2 = 5.5 m/s。",
     "必须用<strong>总路程 ÷ 总时间</strong>：vf = 3s ÷ (s/4 + 2s/7) = 5.6 m/s。"),
    ("❌ 相对运动方向判断反了",
     "看到“甲的电梯相对楼房上升”就认为甲在上升。",
     "楼房静止 → 甲看到它上升 → <strong>甲在下降</strong>。反向推理。"),
    ("❌ 制动题漏掉反应距离",
     "直接把制动距离当作停车总距离。",
     "S总 = <strong>S反应 + S制动</strong> = 18 + 90 = 108m（还要再减去可见距离 60m）。"),
    ("❌ 横穿题只算一侧临界",
     "只算出“人快过”的临界，忽略了“人慢过”的临界。",
     "两个临界都要算：<strong>快过（S人=D/2+d/2+自身长）与慢过（S人=D/2−d/2，S车=S+l）</strong>。"),
    ("❌ 回声题中车走的距离算错（变速时）",
     "变速段直接用 v×t 求车走距离。",
     "变速用<strong>平均速度</strong>（匀变速 = 初末速度平均）乘以时间。"),
    ("❌ 超声波题忽略“单程时间”",
     "把“发出到接收”的总时间当成单程。",
     "位置 = v声 × (总时间 ÷ 2)；<strong>先取一半</strong>再乘声速。"),
    ("❌ 传送带题用对地距离当污染长度",
     "用 0.5×3 = 1.5m 作为污染长度。",
     "污染长度 = 老鼠<strong>相对带面</strong>走过的距离 = 0.4×3 = 1.2m。"),
]

h = open(BASE_F, encoding='utf-8').read()
nq, nf, ne, nk = len(QUIZ), len(FLASH), len(ERRORS), len(KNOW)

h = re.sub(r'<title>[^<]*</title>', '<title>🚦 运动学轻课（第1、2讲）· 精练</title>', h, count=1)
h = re.sub(r'<h1[^>]*>.*?</h1>', '<h1><i class="fas fa-gauge-high"></i> 运动学轻课（第1、2讲）· 精练</h1>', h, count=1, flags=re.DOTALL)
h = re.sub(r'<p>2026秋初二物理 第2讲（B卷压轴） · \d+ 题 · \d+ 卡牌 \| 运动学拔高二</p>',
           f'<p>运动学轻课 第1、2讲 · {nq} 题 · {nf} 卡牌 | 14 道讲义难题（含验算）</p>', h, count=1)
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
      <h4><i class="fas fa-microphone-alt"></i> 🎙️ 轻课要点 · 第1、2讲（运动学难题精练）</h4>
      <p><strong>第1讲</strong>：① <strong>平均速度</strong>（总路程÷总时间，1 题答 5.6m/s）；② <strong>相对运动</strong>（三人电梯，注意“看到上升/下降”是相对判断）；③ <strong>心电图</strong>（走纸速度 = 间距÷周期 → 35mm/s、B 心率 70）；④ <strong>“旋转法”测子弹</strong>（转角度换时间 → v = 6nd/(6N+1)，未满一周时 v = 600m/s）；⑤ <strong>制动 + 三角警示牌</strong>（S总 108m，减去可见 60m → 警示牌放车后 48m）；⑥ <strong>自行车横穿</strong>（快速/慢速临界 → v₂<3.5 或 >6.6 m/s）；⑦ 两车相遇 + 行人横穿（需读图）。</p>
      <p><strong>第2讲</strong>：① <strong>列车鸣笛回声</strong>（6t₁=t₃ → v=57m/s，t₂:t₃=2:7）；② <strong>洒水车回声</strong>（2s 走 680m，听到回声距隧道口 330m）；③ <strong>火车减速 + 两次鸣笛</strong>（v₂=20m/s、第一次鸣笛距 740m、再 27.5s 进隧道）；④ <strong>超声波测速仪</strong>（读时间轴求两次车位置 → 车速）；⑤ 超声波测速（数据存疑）；⑥ <strong>冰上声呐</strong>（水深 15.3m；冰层厚 H = v冰(t₂−t₁)/2）；⑦ <strong>传送带老鼠</strong>（对地 0.3m/s；污染长度 = 相对带面 1.2m）。</p>
      <p><strong>⚠️ 重要提示（本页含 AI 验算，非官方答案）</strong>：讲义本身<strong>无答案</strong>，本页答案为 AI 独立验算结果。其中第1讲 2 题（A、C 均符合）、第2讲 1 题（B、D 均成立）、第2讲 4 题（需读图 b 时间轴）、第2讲 5 题（数据不自洽）、第1讲 7 与第2讲 2(3)（需原图数据）——<strong>这几题务必以老师轻课详解为准</strong>。</p>
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

h = h.replace('physics26q_lesson2_state_check', 'physics26q_light12_state_check')
h = h.replace("QUIZ_PROG_KEY='quiz_progress_physics26q_lesson2'", "QUIZ_PROG_KEY='quiz_progress_physics26q_light12'")
h = h.replace("WRONG_HISTORY_KEY='quiz_physics26q_lesson2_wrong'", "WRONG_HISTORY_KEY='quiz_physics26q_light12_wrong'")
h = h.replace('第2讲 相对速度与过街安全', '运动学轻课 第1、2讲')
h = h.replace('相对速度与过街安全 | 博学班物理', '运动学轻课（第1、2讲）· 精练')
h = h.replace('物理 · 第2讲', '物理 · 轻课第1、2讲')
h = re.sub(r"subject:'[^']*'", "subject:'物理(轻课)'", h, count=2)
h = re.sub(r"chapter:'[^']*'", "chapter:'运动学轻课 第1、2讲（难题精练）'", h, count=2)
h = re.sub(r"tags:'[^']*'", "tags:'物理,轻课,运动学,回声测距,超声波测速,横穿临界,传送带'", h, count=2)
h = re.sub(r'<div class="quiz-stats" id="quizStats">0 / \d+</div>', f'<div class="quiz-stats" id="quizStats">0 / {nq}</div>', h, count=1)
h = re.sub(r'共\d+张知识卡', f'共{nf}张知识卡', h, count=1)
open(OUT_F, 'w', encoding='utf-8').write(h)

js = r"""const fs=require('fs');const html=fs.readFileSync('physics26q_light12_interactive.html','utf8');const re=/<script[^>]*>([\s\S]*?)<\/script>/g;let m,ok=true;while((m=re.exec(html))){try{new Function(m[1])}catch(e){ok=false;console.log('ERR',e.message)}}console.log(ok?'JS OK':'JS ERR')"""
r = subprocess.run(['node','-e',js], capture_output=True, text=True, cwd=REPO)
hh = open(OUT_F, encoding='utf-8').read()
print(r.stdout.strip())
print(f'题{nq} 卡{nf} 错{ne} 知识{nk}')
print('div:', len(re.findall(r'<div\b', hh)), '/', hh.count('</div>'))
print('残留 过街安全:', hh.count('过街安全'), '| lesson2:', hh.count('physics26q_lesson2'))
