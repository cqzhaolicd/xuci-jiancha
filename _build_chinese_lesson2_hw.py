#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""_build_chinese_lesson2_hw.py — 语文第2课作业解析《游大林寺序》互动页
素材: 第二课作业解析视频（转写 + 抽帧互证）+ 若琳实词积累笔记
基座: chinese26q_lesson2_interactive.html
输出: chinese26q_lesson2_hw_interactive.html
"""
import re, json, subprocess

REPO = '/home/administrator/xuci-jiancha'
BASE_F = f'{REPO}/chinese26q_lesson2_interactive.html'
OUT_F = f'{REPO}/chinese26q_lesson2_hw_interactive.html'

KNOW = [
    ("c1", "📜 《游大林寺序》背景", [
        "作者：<strong class=\"hl\">白居易（字乐天）</strong>，唐·元和十二年四月九日作于<strong class=\"hl\">庐山</strong>",
        "文体：<strong class=\"hl\">序</strong>（游记类序文，记游览与感慨）",
        "大林寺：庐山名寺，山高地深、气候偏冷——<strong class=\"hl\">桃花比山下开得迟</strong>",
        "名句（白居易《大林寺桃花》）：<strong class=\"hl\">“人间四月芳菲尽，山寺桃花始盛开。长恨春归无觅处，不知转入此中来。”</strong>",
    ]),
    ("c2", "🧭 文本脉络（三段）", [
        "第一段：<strong class=\"hl\">交代游踪</strong>——与十七人自遗爱草堂出发，历东、西二林，抵化城，憩峰顶，登香炉峰，宿大林寺（大林穷远、人迹罕到）",
        "第二段：<strong class=\"hl\">写景抒情</strong>——山高地深、时节绝晚；梨桃始华、涧草犹短；初到恍然若别造一世界→<strong class=\"hl\">惊喜</strong>",
        "第三段：<strong class=\"hl\">感慨议论</strong>——“迨今垂二十年，寂寥无继者。嗟乎，名利之诱人也如此！”→<strong class=\"hl\">惋惜感叹</strong>",
    ]),
    ("c3", "🔤 重点实词（一）", [
        "<strong class=\"hl\">凡</strong>十有七人：总共（不是“凡人”）",
        "<strong class=\"hl\">穷</strong>远：穷 = <strong class=\"hl\">极、非常</strong>（副词，修饰形容词“远”）→ 极其偏远",
        "<strong class=\"hl\">环</strong>寺：环绕；寺中<strong class=\"hl\">惟</strong>板屋木器：只有",
        "<strong class=\"hl\">其</strong>僧皆海东人：那些（僧人）",
    ]),
    ("c4", "🔤 重点实词（二）", [
        "时节<strong class=\"hl\">绝</strong>晚：绝 = 极、非常；<strong class=\"hl\">晚</strong> = <strong class=\"hl\">迟、慢</strong>（季节变换得迟）",
        "梨桃始<strong class=\"hl\">华</strong>：华 = <strong class=\"hl\">开花（盛开）</strong>（通“花”）",
        "涧草<strong class=\"hl\">犹</strong>短：仍然；<strong class=\"hl\">造</strong>：到、往（“别造一世界”= 另进入一个世界）",
        "<strong class=\"hl\">迨</strong>今<strong class=\"hl\">垂</strong>二十年：迨 = 等到；垂 = 将近",
    ]),
    ("c5", "⚠️ 古今异义与固定搭配", [
        "<strong class=\"hl\">人物风候</strong>：人与气候（“人物”古今异义，非“人物形象”）",
        "<strong class=\"hl\">口号</strong>：<strong class=\"hl\">信口吟成</strong>（随口吟诵，不是“喊口号”）",
        "<strong class=\"hl\">既而</strong>：不久（时间副词，固定搭配）",
        "<strong class=\"hl\">聚落</strong>：村庄；<strong class=\"hl\">山门</strong>：佛寺的大门；<strong class=\"hl\">曾</strong>无半日程：还（竟）",
    ]),
    ("c6", "✍️ 翻译题答题规范", [
        "① <strong class=\"hl\">重点实词要“组词”落实</strong>（如 环=环绕、苍=苍绿/深青、瘦=细瘦）",
        "② 句意<strong class=\"hl\">通顺完整</strong>，不能逐字硬抄",
        "③ 采分点：关键词翻译各 0.5 分 + 句子通顺 1 分",
        "④ <strong class=\"hl\">翻译后回读检查</strong>：是否补充了主语、语序是否顺畅",
    ]),
    ("c7", "🎯 情感分析题的答题结构（第4题）", [
        "第一步：<strong class=\"hl\">先总述情感变化</strong>（由喜悦转为感叹惋惜）",
        "第二步：<strong class=\"hl\">结合具体句子分点分析</strong>（“结合具体句子”= 必须引用原句或翻译原句）",
        "喜悦（2分）：引用“初到，恍然若别造一世界者”或“长恨春归无觅处，不知转入此中来”",
        "惋惜（2分）：引用“迨今垂二十年，寂寥无继者。嗟乎，名利之诱人也如此！”",
    ]),
    ("c8", "🔍 由上下文推断词义", [
        "遇到不确定的词 → <strong class=\"hl\">往后文/前后文找线索</strong>",
        "例：“时节绝晚”的“晚”——由下文“梨桃始华、涧草犹短”（花期晚）推知 = <strong class=\"hl\">迟、慢</strong>",
        "例：“大林穷远”的“穷”——“穷”修饰形容词“远” → 只能是<strong class=\"hl\">副词（极、非常）</strong>，不能译成“贫穷”",
        "方法：<strong class=\"hl\">看搭配、看结构、看语境</strong>",
    ]),
    ("c9", "📝 作业四题概览（本讲）", [
        "第1题 <strong class=\"hl\">解释加点词</strong>（4分）：华／造／既而／迨",
        "第2题 <strong class=\"hl\">翻译句子</strong>（4分）：①环寺多清流苍石，短松瘦竹 ②山高地深，时节绝晚",
        "第3题 <strong class=\"hl\">概括轨迹 + 游人少的原因</strong>（4分）",
        "第4题 <strong class=\"hl\">结合句子分析情感变化</strong>（4分）",
    ]),
    ("c10", "📚 实词积累法（若琳笔记本）", [
        "按<strong class=\"hl\">篇目+字头</strong>整理：《司马穰苴执法》《李密传》《白居易传》",
        "例：《司马穰苴执法》——既（已经）、素（向来）、乃（才）、谢（道歉）、期（约定）",
        "例：《李密传》——徒（只）、阴（暗地里）、俟（等待）、衔（怀恨）、拜（授予）、旋（旋即）",
        "例：《白居易传》——先（祖先）、多（称赞）、持（忍受）、与（到）、币（聘礼）",
        "同时归纳<strong class=\"hl\">人物形象</strong>：敏慧过人／爱民如子／直言敢谏／忧国忧民",
    ]),
    ("c11", "📌 本周任务（老师群公告）", [
        "① <strong class=\"hl\">整理文章中的实词</strong>并提交到本群验收（继续用暑假笔记本）",
        "② 完成<strong class=\"hl\">《知行合一》第二讲</strong>练习题",
        "③ 完成<strong class=\"hl\">第一套真题卷 A 卷</strong>题目",
    ]),
    ("c12", "🗺️ 文言文写景游记学习路径", [
        "本讲《文言文写景游记》= 八年级<strong class=\"hl\">“入门奠基课”</strong>",
        "八年级寒假：<strong class=\"hl\">《〈永州八记〉选读》</strong>（深化）",
        "九年级秋季：<strong class=\"hl\">《写景类文言文升级讲解》</strong>（升级）",
        "路径：<strong class=\"hl\">入门 → 深化 → 升级</strong>；本讲要背熟、学扎实",
    ]),
]

QUIZ = [
    # 第1题 实词解释
    ("第1题：“梨桃始华”中“华”的意思是",
     ["A. 开花（盛开）", "B. 华丽", "C. 中华", "D. 花白"], 0,
     "华 = <strong>开花、盛开</strong>（通“花”）。下文“山寺桃花始盛开”可互证。"),
    ("第1题：“恍然若别造一世界者”中“造”的意思是",
     ["A. 制造", "B. 到、往（进入）", "C. 造成", "D. 建造"], 1,
     "“造”在此为 <strong>到、往</strong>（也可理解为“进入”），“别造一世界”= 好像另进入一个世界。"),
    ("第1题：“既而周览屋壁”中“既而”的意思是",
     ["A. 既然", "B. 已经", "C. 不久", "D. 而且"], 2,
     "“既而”是固定搭配，意为 <strong>不久（接着）</strong>。"),
    ("第1题：“迨今垂二十年”中“迨”的意思是",
     ["A. 将近", "B. 等到、到", "C. 趁着", "D. 超过"], 1,
     "迨 = <strong>等到、到</strong>；“垂”才是“将近”。"),
    ("“大林穷远”中“穷”的意思是",
     ["A. 贫穷", "B. 极、非常", "C. 穷尽", "D. 困窘"], 1,
     "“穷”修饰形容词“远” → 只能是<strong>副词：极、非常</strong>；大林穷远 = 极其偏远。"),
    ("“时节绝晚”中“晚”的意思是",
     ["A. 傍晚", "B. 迟、慢", "C. 晚辈", "D. 夜晚"], 1,
     "由下文“梨桃始华、涧草犹短”推知：季节变换得<strong>迟（慢）</strong>；“绝”= 极、非常。"),
    ("“因口号”中“因”与“口号”分别是什么意思",
     ["A. 因为／喊口号", "B. 于是／信口吟成", "C. 于是／口号声", "D. 依靠／标题"], 1,
     "因 = <strong>于是</strong>；口号 = <strong>信口吟成（随口吟诵）</strong>——古今异义+固定搭配。"),
    ("“迨今垂二十年”中“垂”的意思是",
     ["A. 垂下", "B. 将近", "C. 流传", "D. 临近"], 1,
     "垂 = <strong>将近</strong>（将近二十年）。"),
    ("“曾无半日程”中“曾”的意思是",
     ["A. 曾经", "B. 竟然", "C. 还", "D. 增加"], 2,
     "曾 = <strong>还</strong>（“曾无半日程”= 还不到半天的路程）。"),
    ("“自遗爱草堂，历东、西二林”中“历”的意思是",
     ["A. 历史", "B. 经过", "C. 严厉", "D. 依次"], 1,
     "历 = <strong>经过</strong>（经过东林寺、西林寺）。"),
    # 第2题 翻译
    ("第2题翻译：“环寺多清流苍石，短松瘦竹。”最恰当的是",
     ["A. 围绕寺院，很多清水流着苍石，松树短、竹子瘦。", "B. 环绕寺院的大多是清澈的溪流、苍绿的岩石，矮小的松树、细瘦的竹子。", "C. 寺院周围水流清澈，石头苍老，松竹都很短小。", "D. 环寺多清澈的水和苍色的石头，还有矮松和瘦竹。"], 1,
     "关键词要“组词”落实：<strong>环=环绕、苍=苍绿（深青）、瘦=细瘦</strong>，且句子要通顺；“环”“瘦”各 0.5 分，通顺 1 分。"),
    ("第2题翻译：“山高地深，时节绝晚。”最恰当的是",
     ["A. 山很高，地很深，季节非常晚。", "B. 山峰高峻，谷地深幽，季节变换得非常迟（慢）。", "C. 山高地远，时间已经很晚了。", "D. 山高地深，节气断绝得晚。"], 1,
     "绝 = 极、非常；<strong>晚 = 迟、慢</strong>（季节变换得迟）——由后文花期晚推知。"),
    ("翻译文言句子的采分点主要是",
     ["A. 只求字面逐字对应", "B. 重点实词翻译 + 句子通顺", "C. 字数够多", "D. 抄写原句"], 1,
     "本题评分：关键词（环、瘦）翻译各 0.5 分，<strong>句子通顺 1 分</strong>——实词落实 + 通顺缺一不可。"),
    ("“初到，恍然若别造一世界者”的意思是",
     ["A. 刚到这里，恍惚间好像另进入了一个世界。", "B. 初到这里，恍恍惚惚不知道在哪。", "C. 刚来时，仿佛造了一个世界的房子。", "D. 初次到来，像告别了原来的世界。"], 0,
     "造 = 到、往；<strong>恍然若别造一世界者</strong> = 恍惚觉得像进入了另一个世界（写惊喜之情）。"),
    # 第3题 轨迹与原因
    ("第3题：白居易一行游大林寺的轨迹（按顺序）是",
     ["A. 遗爱草堂→化城→东、西二林→峰顶→香炉峰→大林寺", "B. 遗爱草堂→东、西二林→化城→憩峰顶→登香炉峰→宿大林寺", "C. 大林寺→香炉峰→峰顶→化城→遗爱草堂", "D. 东、西二林→遗爱草堂→香炉峰→大林寺"], 1,
     "原文顺序：自<strong>遗爱草堂</strong>，<strong>历东、西二林</strong>，<strong>抵化城</strong>，<strong>憩峰顶</strong>，<strong>登香炉峰</strong>，<strong>宿大林寺</strong>——抄原文即可得 2 分。"),
    ("第3题：大林寺风景优美却游人甚少的原因，用原文回答是",
     ["A. ①大林穷远 ②名利之诱人也如此", "B. ①山高地深 ②时节绝晚", "C. ①人迹罕到 ②其僧皆海东人", "D. ①寺中惟板屋木器 ②寂寥无继者"], 0,
     "原文依据：第一段“<strong>大林穷远</strong>”（偏远）+ 结尾“<strong>名利之诱人也如此</strong>”（世人追逐名利、无人前来题诗留名）——1 点 1 分。"),
    ("第3题答题的启示是",
     ["A. 凭印象概括即可", "B. 答案多可从原文中定位、引用原文作答", "C. 只需写原因不写轨迹", "D. 轨迹要自己发挥"], 1,
     "这类题属“送分题”：<strong>先在文中定位（游踪句 + 议论句），再引用原文</strong>作答即可。"),
    # 第4题 情感变化
    ("第4题：作者游大林寺的情感变化是",
     ["A. 由喜悦（惊喜）转为感叹惋惜", "B. 由悲伤转为喜悦", "C. 始终平静", "D. 由惊喜转为愤怒"], 0,
     "第二段写“初到，恍然若别造一世界者”→ <strong>喜悦/惊喜</strong>；结尾“寂寥无继者。嗟乎，名利之诱人也如此!”→ <strong>感叹惋惜</strong>。"),
    ("第4题中“结合文中具体句子”的含义是",
     ["A. 只写情感不必举例", "B. 答题时必须引用原句或翻译原句作依据", "C. 抄写整段原文", "D. 自己编造句子"], 1,
     "“结合具体句子”= <strong>引用原句（或翻译该句）</strong>再分析，这是得分关键，不能只写情感结论。"),
    ("第4题答案中体现“喜悦”的句子是",
     ["A. 大林穷远，人迹罕到", "B. 初到，恍然若别造一世界者", "C. 寺中惟板屋木器", "D. 自萧、魏、李游"], 1,
     "“<strong>初到，恍然若别造一世界者</strong>”（及诗句“长恨春归无觅处，不知转入此中来”）体现初夏见春景的惊喜。"),
    ("第4题答案中体现“感叹惋惜”的句子是",
     ["A. 环寺多清流苍石", "B. 山高地深，时节绝晚", "C. 迨今垂二十年，寂寥无继者。嗟乎，名利之诱人也如此！", "D. 时元和十二年四月九日"], 2,
     "结尾议论句：<strong>“迨今垂二十年，寂寥无继者。嗟乎，名利之诱人也如此！”</strong>——世人沉迷名利，少有人来赏美景。"),
    ("情感分析题的正确答题顺序是",
     ["A. 先分点举例，最后总结", "B. 先总述情感变化，再结合具体句子分点分析", "C. 只写总述", "D. 只引用句子不分析"], 1,
     "标准结构：<strong>先给出总体结论（由喜悦转为惋惜），再引用原句分点分析</strong>——两步都不能丢。"),
    ("遇到不理解的文言实词时，最有效的方法是",
     ["A. 凭现代汉语猜", "B. 看搭配、看结构、结合上下文推断", "C. 直接跳过", "D. 只查字典不看语境"], 1,
     "本课示范：由后文“梨桃始华”推知“晚”= 迟；“穷”修饰“远”故为副词（极、非常）——<strong>语境推断</strong>。"),
    ("“人物风候，与平地聚落不同”中“人物”的意思是",
     ["A. 人物形象", "B. 人与气候（古今异义）", "C. 有名的人物", "D. 人物的风貌"], 1,
     "“<strong>人物风候</strong>”指人与气候风土（古今异义，不能理解为“人物形象”）。"),
    ("关于《游大林寺序》的作者与写作时间，正确的是",
     ["A. 李白·开元年间", "B. 白居易（乐天）·元和十二年", "C. 柳宗元·永州时期", "D. 苏轼·元丰年间"], 1,
     "文末交代：“时<strong>元和十二年</strong>四月九日，<strong>乐天</strong>序”——作者白居易（字乐天）。"),
]

FLASH = [
    ("“华”“造”“既而”“迨”分别什么意思？",
     "华 = <strong>开花（盛开）</strong>；造 = <strong>到、往（进入）</strong>；既而 = <strong>不久</strong>；迨 = <strong>等到、到</strong>。"),
    ("“大林穷远”的“穷”怎么讲？为什么？",
     "穷 = <strong>极、非常</strong>（副词）。因为“穷”修饰形容词“远”，不能译成“贫穷”。"),
    ("“时节绝晚”的“绝”“晚”？",
     "绝 = 极、非常；<strong>晚 = 迟、慢</strong>（季节变换得迟）——由后文“梨桃始华、涧草犹短”推知。"),
    ("“因口号”中“因”与“口号”？",
     "因 = <strong>于是</strong>；口号 = <strong>信口吟成</strong>（随口吟诵）——固定搭配 + 古今异义。"),
    ("“迨今垂二十年”“曾无半日程”中的“垂”“曾”？",
     "垂 = <strong>将近</strong>；曾 = <strong>还</strong>（曾无半日程 = 还不到半天路程）。"),
    ("翻译文言句子的两个采分点？",
     "① <strong>重点实词组词落实</strong>（环=环绕、苍=苍绿、瘦=细瘦）；② <strong>句子通顺</strong>（环、瘦各0.5分，通顺1分）。"),
    ("白居易一行游大林寺的轨迹？",
     "自<strong>遗爱草堂</strong> → 历<strong>东、西二林</strong> → 抵<strong>化城</strong> → 憩<strong>峰顶</strong> → 登<strong>香炉峰</strong> → 宿<strong>大林寺</strong>。"),
    ("大林寺美景却游人少的原因（原文）？",
     "① <strong>大林穷远</strong>（偏远难至）；② <strong>名利之诱人也如此</strong>（世人追逐名利，无人题诗留名）。"),
    ("作者的情感变化？依据？",
     "由<strong>喜悦（惊喜）</strong>转为<strong>感叹惋惜</strong>：依据“初到，恍然若别造一世界者”（喜悦）+“迨今垂二十年，寂寥无继者…名利之诱人也如此！”（惋惜）。"),
    ("“结合具体句子”类题的得分关键？",
     "必须<strong>引用原句或翻译原句</strong>再作分析；结构上<strong>先总述情感变化，再分点结合原句</strong>。"),
    ("本讲实词积累怎么做？",
     "按<strong>篇目 + 字头</strong>整理（《司马穰苴执法》《李密传》《白居易传》），一字多义与人物形象词分开记，用暑假笔记本持续积累。"),
    ("本讲作业三项任务？",
     "① 整理实词并提交群验收；② 完成《知行合一》第二讲练习；③ 完成第一套真题卷 A 卷。"),
]

ERRORS = [
    ("❌ 实词只看字面（如“穷”译成贫穷）",
     "“大林穷远”译成“大林寺很贫穷遥远”。",
     "看<strong>搭配与词性</strong>：“穷”修饰形容词“远”→ 副词 <strong>极、非常</strong>。"),
    ("❌ “晚”直译成“傍晚/晚上”",
     "“时节绝晚”译成“季节非常晚（时间晚了）”。",
     "结合后文语境（花期晚、草犹短）→ <strong>晚 = 迟、慢</strong>，指季节变换得迟。"),
    ("❌ 翻译忽略“组词落实”",
     "“环寺多清流苍石”译成“寺院周围有水有石头”，漏掉关键词。",
     "关键词必须逐一组词翻译：<strong>环=环绕、苍=苍绿、瘦=细瘦</strong>；再加通顺成句。"),
    ("❌ 情感分析题只写结论不引原句",
     "只答“由喜悦转为惋惜”，没有引用任何句子。",
     "题干要求“<strong>结合文中具体句子</strong>”→ 必须引用（或翻译）原句作依据，否则扣分。"),
    ("❌ 情感变化漏掉其一（只答“惋惜”）",
     "只写结尾的惋惜，忽略第二段的惊喜。",
     "情感是<strong>变化</strong>：由<strong>喜悦（惊喜）</strong>转为<strong>感叹惋惜</strong>，前后都要写并各配原句。"),
    ("❌ 概括题自己发挥，不回原文定位",
     "轨迹题凭记忆乱序背诵，原因题自己编。",
     "先<strong>回原文定位</strong>（游踪句、议论句），<strong>引用原文</strong>作答——轨迹与原因都能在文中找到原句。"),
    ("❌ 古今异义按现代汉语理解",
     "“人物风候”理解成“人物形象”；“口号”理解成“喊口号”。",
     "标注古今异义与固定搭配：<strong>人物风候 = 人与气候</strong>；<strong>口号 = 信口吟成</strong>；<strong>既而 = 不久</strong>。"),
]

h = open(BASE_F, encoding='utf-8').read()
nq, nf, ne, nk = len(QUIZ), len(FLASH), len(ERRORS), len(KNOW)

h = re.sub(r'<title>[^<]*</title>', '<title>📜 游大林寺序 · 作业解析</title>', h, count=1)
h = re.sub(r'<h1[^>]*>.*?</h1>', '<h1><i class="fas fa-book-open"></i> 《游大林寺序》作业解析 · 互动学习</h1>', h, count=1, flags=re.DOTALL)
h = re.sub(r'<p>[^<]*\| 语文</p>', f'<p>2026秋语文第2课作业解析 · {nq} 题 · {nf} 卡牌 | 文言文写景游记</p>', h, count=1)
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
      <h4><i class="fas fa-microphone-alt"></i> 🎙️ 作业解析要点 · 第2课（《游大林寺序》）</h4>
      <p><strong>文本梳理</strong>：白居易《游大林寺序》（元和十二年，庐山）。第一段<strong>交代游踪</strong>（遗爱草堂→东、西二林→化城→憩峰顶→登香炉峰→宿大林寺；大林穷远）；第二段<strong>写景抒情</strong>（山高地深、时节绝晚、梨桃始华→初到恍然若别造一世界→<strong>惊喜</strong>）；第三段<strong>感慨议论</strong>（迨今垂二十年寂寥无继者，名利之诱人也如此→<strong>惋惜</strong>）。</p>
      <p><strong>实词要点</strong>：华=开花｜造=到、往（进入）｜既而=不久｜迨=等到｜垂=将近｜曾=还｜穷=极、非常（副词）｜绝=极、非常｜晚=迟、慢｜因=于是｜口号=信口吟成｜人物风候=人与气候（古今异义）。</p>
      <p><strong>答题方法</strong>：① 翻译题——<strong>重点实词组词落实 + 句子通顺</strong>；② 情感分析题——<strong>先总述变化，再“结合文中具体句子”分点分析</strong>（必须引用原句，这一步不能丢）；③ 概括题——<strong>回原文定位、引用原句</strong>（送分题）。</p>
      <p><strong>📝 本周任务（老师群公告）</strong>：① 整理本讲实词并提交本群验收（继续用暑假笔记本）；② 完成《知行合一》第二讲练习题；③ 完成第一套真题卷 A 卷。本讲为八年级<strong>入门奠基课</strong>，后续“<strong>入门→深化（《永州八记》选读）→升级（写景类文言文升级讲解）</strong>”，务必及时背诵复习、扎实掌握。</p>
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

h = h.replace('chinese26q_lesson2_state_check', 'chinese26q_lesson2hw_state_check')
h = h.replace("QUIZ_PROG_KEY='quiz_progress_chinese26q_lesson2'", "QUIZ_PROG_KEY='quiz_progress_chinese26q_lesson2_hw'")
h = h.replace("WRONG_HISTORY_KEY='quiz_chinese26q_lesson2_wrong'", "WRONG_HISTORY_KEY='quiz_chinese26q_lesson2_hw_wrong'")
h = re.sub(r'第2课[^<|]*', '第2课作业解析《游大林寺序》', h, count=1)
h = h.replace('第二课 · 山水游记专题', '第2课作业解析 · 游大林寺序')
h = h.replace('chinese26q_lesson2_title', 'chinese26q_lesson2hw_title')
h = re.sub(r"subject:'[^']*'", "subject:'语文(2026秋)'", h, count=2)
h = re.sub(r"chapter:'[^']*'", "chapter:'第2课作业解析《游大林寺序》'", h, count=2)
h = re.sub(r"tags:'[^']*'", "tags:'语文,2026秋,第2课,游大林寺序,文言实词,翻译,情感分析'", h, count=2)
h = re.sub(r'<div class="quiz-stats" id="quizStats">0 / \d+</div>', f'<div class="quiz-stats" id="quizStats">0 / {nq}</div>', h, count=1)
h = re.sub(r'共\d+张知识卡', f'共{nf}张知识卡', h, count=1)
open(OUT_F, 'w', encoding='utf-8').write(h)

js = r"""const fs=require('fs');const html=fs.readFileSync('chinese26q_lesson2_hw_interactive.html','utf8');const re=/<script[^>]*>([\s\S]*?)<\/script>/g;let m,ok=true;while((m=re.exec(html))){try{new Function(m[1])}catch(e){ok=false;console.log('ERR',e.message)}}console.log(ok?'JS OK':'JS ERR')"""
r = subprocess.run(['node','-e',js], capture_output=True, text=True, cwd=REPO)
hh = open(OUT_F, encoding='utf-8').read()
print(r.stdout.strip())
print(f'题{nq} 卡{nf} 错{ne} 知识{nk}')
print('div:', len(re.findall(r'<div\b', hh)), '/', hh.count('</div>'))
print('残留 山水游记:', hh.count('山水游记'), '| lesson2_state:', hh.count("chinese26q_lesson2_state_check"))
