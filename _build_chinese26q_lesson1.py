#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build chinese26q_lesson1_interactive.html from math26q_lesson1 base (fixed template).
语文第一课：新闻类文本阅读（课外培训2026秋季·语文第1讲）"""
FN = 'chinese26q_lesson1_interactive.html'
h = open(FN, encoding='utf-8').read()
report = []

def rep(old, new, tag, count=1):
    global h
    n = h.count(old)
    if n != count:
        report.append(f'FAIL[{tag}]: expected {count} got {n}')
        return False
    h = h.replace(old, new)
    report.append(f'OK[{tag}]')
    return True

def arr_replace(decl, new_content, tag):
    global h
    i = h.find(decl)
    if i < 0:
        report.append(f'FAIL[{tag}]: decl not found'); return False
    j = h.find('];', i + len(decl))
    if j < 0:
        report.append(f'FAIL[{tag}]: ]; not found'); return False
    h = h[:i] + new_content + h[j + 2:]
    report.append(f'OK[{tag}]')
    return True

def seg_replace(start_marker, end_marker, new_seg, tag):
    global h
    i = h.find(start_marker)
    if i < 0:
        report.append(f'FAIL[{tag}]: start not found'); return False
    j = h.find(end_marker, i)
    if j < 0:
        report.append(f'FAIL[{tag}]: end not found'); return False
    h = h[:i] + new_seg + h[j:]
    report.append(f'OK[{tag}]')
    return True

# ---------- 文本 ----------
rep('<title>🧮 二次根式综合复习 · 互动学习</title>',
    '<title>📰 新闻类文本阅读 · 互动学习</title>', 'title')
rep('数学 · 第1讲', '语文 · 第1讲', 'navbar-brand', count=2)
rep('<i class="fas fa-square-root-alt"></i> 二次根式综合复习 · 互动学习',
    '<i class="fas fa-newspaper"></i> 新闻类文本阅读 · 互动学习', 'hero-h1')
rep('26秋博学班 数学第1讲 · 28 题 · 14 卡牌 | 博学班',
    '2026秋语文课外班 第1课 · 14 题 · 10 卡牌 | 新闻阅读', 'hero-sub')
rep('<span><i class="fas fa-check-circle" style="color:var(--success)"></i> 28道测验题</span>',
    '<span><i class="fas fa-check-circle" style="color:var(--success)"></i> 14道测验题</span>', 'meta-quiz')
rep('<i class="fas fa-layer-group"></i> 14张知识卡</span>',
    '<i class="fas fa-layer-group"></i> 10张知识卡</span>', 'meta-flash')
rep('<i class="fas fa-exclamation-triangle" style="color:var(--danger)"></i> 8大易错点</span>',
    '<i class="fas fa-exclamation-triangle" style="color:var(--danger)"></i> 6大易错点</span>', 'meta-err')
rep('第一讲 · 二次根式综合复习', '第一课 · 新闻类文本阅读', 'section-header')
rep('点击卡片翻转查看答案 · 共14张知识卡', '点击卡片翻转查看答案 · 共10张知识卡', 'flash-hint')
rep('数学 · 第1讲 二次根式综合复习 | 博学班 · 2026秋',
    '语文 · 第1课 新闻类文本阅读 | 2026秋 · 新闻阅读', 'footer')
rep('<div class="quiz-stats" id="quizStats">0 / 28</div>',
    '<div class="quiz-stats" id="quizStats">0 / 14</div>', 'quizstats')

# ---------- 知识图谱 ----------
KG = '''<div class="knowledge-grid">
      <div class="knowledge-card c1"><h3><i class="fas fa-newspaper" style="color:#34495e"></i> 新闻是什么</h3><ul>
        <li>新闻三特点：<strong class="hl">真实性、时效性、准确性</strong></li>
        <li>消息是新闻中最常用的体裁，用事实说话</li>
        <li>成都考情：新闻<strong class="hl">连续5年霸榜中考</strong>（约8-10分）</li>
      </ul></div>
      <div class="knowledge-card c2"><h3><i class="fas fa-layer-group" style="color:#8e44ad"></i> 消息结构五部分</h3><ul>
        <li><strong class="hl">标题 → 导语 → 主体 → 背景 → 结语</strong></li>
        <li>标题：新闻的眼睛（拟题/赏析常考）</li>
        <li>导语：<strong class="hl">第一段或第一句</strong>，概括最重要的事实</li>
      </ul></div>
      <div class="knowledge-card c3"><h3><i class="fas fa-question" style="color:#3498db"></i> 新闻六要素</h3><ul>
        <li>5W1H：<strong class="hl">who、what、when、where、why、how</strong></li>
        <li>一句话新闻：到导语里找 who+what+how</li>
        <li>与时间地点取舍：无新闻价值可省（不超过字数）</li>
      </ul></div>
      <div class="knowledge-card c4"><h3><i class="fas fa-pen-fancy" style="color:#27ae60"></i> 标题赏析角度</h3><ul>
        <li><strong class="hl">手法</strong>：比喻/拟人/对偶/双关等修辞</li>
        <li><strong class="hl">内容</strong>：点明对象、概括事件、呼应线路作用</li>
        <li><strong class="hl">效果</strong>：生动形象、吸引读者阅读兴趣</li>
        <li>例：2024成都中考“地下长龙贯通西东”</li>
      </ul></div>
      <div class="knowledge-card c5"><h3><i class="fas fa-microphone-alt" style="color:#2980b9"></i> 采访提纲设计</h3><ul>
        <li>先分析：采访<strong class="hl">对象身份</strong> + 活动<strong class="hl">主题</strong> + 采访<strong class="hl">目的</strong></li>
        <li>从对象职业/经历切入提问，紧扣主题与材料</li>
        <li>格式：<strong class="hl">称呼问候 + 采访内容</strong>；问题具体不空泛</li>
      </ul></div>
      <div class="knowledge-card c6"><h3><i class="fas fa-columns" style="color:#f39c12"></i> 非连续性文本</h3><ul>
        <li>新闻常与<strong class="hl">说明文、议论文</strong>联合出题</li>
        <li>题型分布：A卷小阅读、A卷小作文、B卷语言运用</li>
        <li>跨材料分析：先分则概括，再综合比较异同</li>
      </ul></div>
      <div class="knowledge-card c7"><h3><i class="fas fa-map-pin" style="color:#16a085"></i> 本土素材特点</h3><ul>
        <li>成都爱考<strong class="hl">本土大事</strong>：大运会、地铁新线、世园会、科幻大会</li>
        <li>素材新鲜、贴近生活，考查信息提取与表达</li>
        <li>读题先划<strong class="hl">主题词/对象词</strong>（红色标注即提示）</li>
      </ul></div>
      <div class="knowledge-card c8"><h3><i class="fas fa-link" style="color:#e74c3c"></i> 对联补写（挽联）</h3><ul>
        <li>规则：字数相等、<strong class="hl">词性相对</strong>、结构相同、内容相关</li>
        <li>平仄：上联末字<strong class="hl">仄声(3/4声)</strong>，下联末字<strong class="hl">平声(1/2声)</strong></li>
        <li>先断句分短语，再回<strong class="hl">材料中找素材</strong>（优先提取而非创造）</li>
      </ul></div>
    </div>
    '''
seg_replace('<div class="knowledge-grid">', '<div class="teacher-talk">', KG, 'knowledge-grid')

# ---------- 课堂要点 ----------
TT = '''<div class="teacher-talk">
      <h4><i class="fas fa-microphone-alt"></i> 🎙️ 课堂要点 · 第一课（新闻类文本阅读）</h4>
      <p><strong>本讲核心</strong>：2026秋语文课外班第1课，直击八上第一单元新文体——<strong>新闻</strong>。新闻近几年常与说明文、议论文联合以<strong>非连续性文本</strong>方式出题，成都连续 5 年霸榜中考（8-10 分），且专挑本土大事当素材（大运会、地铁新线、世园会、科幻大会……）。</p>
      <p><strong>作业三题方法</strong>：①<strong>一句话新闻</strong>——去导语（第一段第一句）找 who+what+how，时间地点无新闻价值可舍，控制在字数内；②<strong>采访问题设计</strong>——先看采访对象身份（物理老师→物理+教育两领域切入），再看主题（缅怀科学巨匠、传承科学精神）与目的，格式先称呼问候再提问；③<strong>补写挽联</strong>——先断句辨短语类型（研物理/获诺奖/名扬四海均为动宾），对下联注意数量词对数量词（四海→八方/九州），末字平收（一声/二声），素材优先回材料中提炼（归故土/育人才/德润八方）。</p>
      <p><strong>易错提醒</strong>：①概括题只答细节不抓导语核心；②标题妙处只说“生动形象”不答角度；③采访问题脱离对象身份或主题；④忘记称呼与礼貌用语；⑤对联不对仗、末字不平收；⑥答题凭空想象、不用材料。</p>
      <p><strong>🎓 老师课堂总结</strong> — 新闻题本质考两件事：<strong>会不会读</strong>（快速提取导语核心事实）和<strong>会不会写</strong>（概括/拟题/采访/对联都是规范表达）。所有题先划题干中的主题词与对象词，答案从材料中来，格式分一分都不能丢。</p>
    </div>
    '''
seg_replace('<div class="teacher-talk">', '<div id="tab-quiz"', TT, 'teacher-talk')

# ---------- 题库 14 题 ----------
Q = '''const questions = [
  {"q":"新闻材料：杨振宁先生被公认在凝聚态物理、粒子物理、场论等领域拥有13项诺贝尔级别成就；他资助数百名中国学者深造，协助清华建高等研究中心；在清华110周年校庆寄语学子选对方向。杨振宁的学生翟芸称他最喜欢的格言是“宁拙毋巧，宁朴毋华”。（来源：央视新闻、新华社）请用一句话概括这则新闻的主要内容（不超过15字）：","opts":["A. 杨振宁因病去世，享年103岁","B. 杨振宁拥有13项诺贝尔级别成就","C. 杨振宁资助数百名中国学者深造","D. 杨振宁寄语学子要选对发展方向"],"ans":0,"exp":"一句话新闻=到<strong>导语</strong>中找 who+what+how：who 杨振宁，what/how 因病去世享年103岁。成就、资助、寄语都只是主体部分细节，不能作概括。"},
  {"q":"概括一句话新闻时，下列做法正确的一项是","opts":["A. 到导语（第一段第一句）中提取 who、what、how 组织答案","B. 把材料中所有数字和细节都写进去","C. 时间地点不管有无价值都一定要保留","D. 用自己的想象补充材料没有的内容"],"ans":0,"exp":"一句话新闻方法：读导语→提取 who/what/how→限字数成句。细节冗余、无新闻价值的时间地点可舍弃；<strong>不能凭空添加</strong>材料外信息。"},
  {"q":"班级要举办“缅怀科学巨匠，传承科学精神”主题班会，主持人要现场采访本班物理老师，让大家更深入了解杨振宁先生。下列两个采访问题设计最恰当的是","opts":["A. ①杨振宁因宇称不守恒获诺奖，老师能用通俗语言讲讲这个原理吗？②杨先生晚年归国培养人才的家国情怀，对青少年有什么启示？","B. ①老师您教物理多少年了？②老师您觉得我们班谁物理最好？","C. ①杨振宁先生有几个孩子？②他的退休工资高不高？","D. ①老师您平时几点下班？②您觉得物理作业布置多少合适？"],"ans":0,"exp":"采访问题三看：<strong>对象身份</strong>（物理老师→物理+教育）、<strong>主题</strong>（缅怀巨匠、传承科学精神）、<strong>目的</strong>（了解杨振宁）。A 既结合人物与物理，又扣住家国情怀与青少年启示。"},
  {"q":"设计采访问题时，下列说法不正确的是","opts":["A. 要先考虑采访对象的身份、职业和受教育情况","B. 问题要结合活动主题和采访目的来设计","C. 可以直接问与主题无关的私人生活细节","D. 作答格式应先有称呼问候，再写采访内容"],"ans":2,"exp":"问题须<strong>紧扣主题与目的</strong>，私人细节、与主题无关的内容都不合适；对象身份决定切入角度，格式注意称呼与礼貌。"},
  {"q":"石怀责同学要写一副挽联缅怀杨振宁先生，上联是“研物理获诺奖，名扬四海”。下列补写的下联最恰当的是","opts":["A. 归故土育人才，德润八方","B. 留异乡攻难题，名扬四海","C. 研物理获诺奖，声震九州","D. 回祖国享晚年，福泽万民"],"ans":0,"exp":"①词性相对：归故土/育人才 对 研物理/获诺奖（动宾），德润八方 对 名扬四海（主谓）；②<strong>四海→八方</strong>（数量词对数量词）；③下联末字“方”为<strong>平声</strong>（上联“海”仄声，上仄下平）；④内容由材料提炼（归国、育人）。“名扬四海”与上联重复、D 内容偏离材料。"},
  {"q":"对联的基本要求不包括","opts":["A. 字数相等","B. 词性相对、结构相同","C. 上联末字一般为仄声，下联末字一般为平声","D. 上下联内容必须完全相同"],"ans":3,"exp":"对联规则：字数相等、词性相对、结构相同、平仄相协（上仄下平）、内容相关。内容“完全相同”会变成合掌，是对联大忌。"},
  {"q":"消息（新闻）的结构一般包括五部分，正确的顺序是","opts":["A. 标题—导语—主体—背景—结语","B. 导语—标题—主体—结语—背景","C. 标题—主体—导语—背景—结语","D. 导语—主体—标题—背景—结语"],"ans":0,"exp":"消息五部分：<strong>标题→导语→主体→背景→结语</strong>。标题最醒目，导语在开头概括最重要事实，主体展开，背景交代来龙去脉，结语收束。"},
  {"q":"新闻最重要的特点是","opts":["A. 真实性","B. 生动性","C. 娱乐性","D. 夸张性"],"ans":0,"exp":"新闻用事实说话，<strong>真实性</strong>是新闻的生命；同时讲究时效性与准确性。生动夸张是文学手法，不是新闻要求。"},
  {"q":"消息中的“导语”一般指","opts":["A. 消息开头第一段或第一句话，概括最重要的事实","B. 消息的标题","C. 消息的结尾","D. 穿插在主体中的背景材料"],"ans":0,"exp":"导语位于<strong>开头第一段/第一句</strong>，用最简练的语言交代最主要的事实，是概括题、拟标题题的突破口。"},
  {"q":"2024成都中考题：给地铁报道拟标题“地下长龙贯通西东”，分析其妙处，下列角度分析最完整的是","opts":["A. 运用比喻手法，生动形象；交代了线路贯穿东西的作用；新颖别致吸引读者","B. 只是把地铁比作长龙，没有任何作用","C. 说明地铁很长，地下交通很方便","D. 用了对偶修辞，读起来朗朗上口"],"ans":0,"exp":"标题赏析三步：①<strong>手法</strong>——比喻（地铁如地下长龙）；②<strong>内容/作用</strong>——点出线路东西贯穿的作用；③<strong>效果</strong>——生动形象、吸引读者。只说“生动形象”是常见失分点。"},
  {"q":"拟写新闻标题或概括内容时，第一步应该做什么？","opts":["A. 通读材料，找到导语并提取核心事实","B. 直接抄写材料第一句","C. 先数字数再动笔","D. 凭印象编一个吸引人的句子"],"ans":0,"exp":"先<strong>读导语提取 who/what/where/when</strong> 等核心要素，再据此压缩成句；不能照抄也不能凭空编造。"},
  {"q":"成都中考新闻素材常选用（　　）","opts":["A. 成都本土大事：大运会、地铁新线、世园会、科幻大会等","B. 只考国外新闻","C. 只考古代历史事件","D. 只考娱乐明星八卦"],"ans":0,"exp":"成都考情：<strong>专挑本土大事</strong>当素材（大运会、地铁新线、世园会、科幻大会……），贴近生活、时代感强。"},
  {"q":"杨振宁先生的格言“宁拙毋巧，宁朴毋华”中，前四字讲的是（　　），后四字说的是（　　）","opts":["A. 科学精神；人格特征","B. 学习方法；考试成绩","C. 物质追求；外表打扮","D. 家庭生活；个人爱好"],"ans":0,"exp":"据其学生翟芸介绍：“宁拙毋巧”讲<strong>科学精神</strong>（治学踏实不投机），“宁朴毋华”是<strong>人格特征</strong>（为人质朴不浮华）。"},
  {"q":"新闻与说明文、议论文组合成非连续性文本时，分析策略正确的是","opts":["A. 先分则概括各材料要点，再综合比较异同","B. 只看其中一则材料","C. 跳过图表只看文字","D. 把每则材料都全文背下来"],"ans":0,"exp":"非连续性文本（含新闻+图表/说明/议论）策略：<strong>分则读→标要点→综合比较</strong>，提取信息要全面、答题有依据。"}
];'''
arr_replace('const questions = [', Q, 'questions')

# ---------- 卡牌 10 张 ----------
F = '''const flashcards = [
  {"front":"新闻三特点是什么？","back":"<strong>真实性、时效性、准确性</strong>。真实性是新闻的生命，用事实说话。"},
  {"front":"消息结构五部分？","back":"<strong>标题—导语—主体—背景—结语</strong>。标题最醒目，导语概括最重要事实。"},
  {"front":"导语在哪里？有什么用？","back":"消息<strong>开头第一段或第一句</strong>；作用：概括最主要事实，是概括题突破口。"},
  {"front":"新闻六要素（5W1H）？","back":"who（人物）、what（事件）、when（时间）、where（地点）、why（原因）、how（经过/结果）。"},
  {"front":"一句话新闻怎么概括？","back":"到<strong>导语</strong>中找 who+what+how；无新闻价值的时间地点可舍；不超过规定字数；句末加句号。"},
  {"front":"标题妙处赏析三步？","back":"①<strong>手法</strong>（比喻/拟人/对偶…）②<strong>内容作用</strong>（点对象、概事件、呼应线路作用）③<strong>效果</strong>（生动形象、吸引读者）。"},
  {"front":"采访问题设计要点？","back":"看<strong>对象身份职业</strong>→定角度；扣<strong>活动主题</strong>与<strong>目的</strong>；格式：<strong>称呼问候+采访内容</strong>；问题具体、有深度。"},
  {"front":"对联五规则？","back":"字数相等；<strong>词性相对</strong>；结构相同；平仄相协（上联末字仄声 3/4 声，下联末字平声 1/2 声）；内容相关。"},
  {"front":"对联素材从哪来？","back":"<strong>优先从材料中提炼</strong>（人物事迹概括成动宾短语），而非凭空创造；数量词要对数量词（四海→八方/九州）。"},
  {"front":"成都新闻考题特点？","back":"连续 5 年霸榜中考（8-10 分），素材选<strong>本土大事</strong>（大运会、地铁、世园会、科幻大会）；常以非连续性文本形式与说明文、议论文联合出题。"}
];'''
arr_replace('const flashcards = [', F, 'flashcards')

# ---------- 易错 6 条 ----------
E = '''errors = [
  {"title":"❌ 概括题只答细节不抓导语","wrong":"把“杨振宁有13项成就、资助数百名学者”等主体细节当作概括。","right":"一句话新闻去<strong>导语</strong>找 who+what+how：如“杨振宁因病去世，享年103岁”；细节留给主体。"},
  {"title":"❌ 标题妙处只说“生动形象”","wrong":"赏析“地下长龙贯通西东”只答“运用比喻，生动形象”。","right":"三步完整答：<strong>手法（比喻）+内容作用（贯通西东）+效果（吸引读者）</strong>。"},
  {"title":"❌ 采访问题脱离对象身份或主题","wrong":"采访物理老师却问私人生活、八卦或与主题无关的问题。","right":"先看对象身份职业（物理老师→物理+教育），再扣<strong>主题与目的</strong>提问，格式先称呼问候。"},
  {"title":"❌ 对联不对仗、末字不平收","wrong":"下联写成“名扬四海”与上联重复，或末字用三声/四声。","right":"词性相对、数量词对数量词（四海→八方），<strong>下联末字平声（1/2声）</strong>：方、州、才都可以。"},
  {"title":"❌ 答题凭空想象、不用材料","wrong":"对联补写自己编造人物事迹、采访问题脱离材料信息。","right":"<strong>素材优先回材料提炼</strong>（归故土/育人才/助学者），从人物真实事迹中概括。"},
  {"title":"❌ 忽略格式分","wrong":"采访题直接写问题内容，没有称呼问候；概括题忘了句号。","right":"表达题都有隐性格式分：<strong>称呼+问候+内容</strong>；一句话新闻结尾加句号。"}
];'''
arr_replace('errors = [', E, 'errors')

# ---------- localStorage keys ----------
rep("const WRONG_HISTORY_KEY='quiz_math26q_lesson1_wrong';",
    "const WRONG_HISTORY_KEY='quiz_chinese26q_lesson1_wrong';", 'wrong-key')
rep("var QUIZ_PROG_KEY='quiz_progress_math26q_lesson1';",
    "var QUIZ_PROG_KEY='quiz_progress_chinese26q_lesson1';", 'prog-key')
if h.count('math26q_lesson1_state_check') == 5:
    h = h.replace('math26q_lesson1_state_check', 'chinese26q_lesson1_state_check')
    report.append('OK[state-key x5]')
else:
    report.append(f'FAIL[state-key]: {h.count("math26q_lesson1_state_check")}')

# ---------- import 文案 ----------
rep("subject:'数学(博学班)',chapter:'第1讲 二次根式综合复习',content:q.q,correct_answer:q.opts[q.ans],my_answer:q.opts[myAns]||'未作答',error_reason:'概念不清',source:'练习',difficulty:3,tags:'数学,博学班,2026秋,第1讲,二次根式,双重非负性,双重根式,裂项,知二求二,降次'",
    "subject:'语文(课外班)',chapter:'第1课 新闻类文本阅读',content:q.q,correct_answer:q.opts[q.ans],my_answer:q.opts[myAns]||'未作答',error_reason:'概念不清',source:'练习',difficulty:3,tags:'语文,2026秋,第1课,新闻阅读,一句话新闻,采访提纲,对联'",
    'autoImport-tags')
rep("subject:'数学',chapter:'第1讲 二次根式综合复习',content:w.q.q,correct_answer:w.q.opts[w.q.ans],my_answer:w.q.opts[w.uc]||'未作答',error_reason:'概念不清',source:'练习',difficulty:3,tags:'数学,博学班,2026秋,第1讲,二次根式'",
    "subject:'语文',chapter:'第1课 新闻类文本阅读',content:w.q.q,correct_answer:w.q.opts[w.q.ans],my_answer:w.q.opts[w.uc]||'未作答',error_reason:'概念不清',source:'练习',difficulty:3,tags:'语文,2026秋,第1课,新闻阅读'",
    'importWB-tags')

# ---------- 残留检查 ----------
for pat in ['二次根式','数学','博学班','quiz_math26q','双重非负']:
    c = h.count(pat)
    if c:
        report.append(f'WARN leftover[{pat}] = {c}')

open(FN, 'w', encoding='utf-8').write(h)
print('new len', len(h))
print('\\n'.join(report))
