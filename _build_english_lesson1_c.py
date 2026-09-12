#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""_build_english_lesson1_c.py — 英语第1讲 B班 → C班 替换
材料: 2026秋双语八年级C班第1讲闯关单 + 官方答案
输出: english_lesson1_interactive.html (覆盖, 保持入口引用不变)
"""
import re, json

REPO = '/home/administrator/xuci-jiancha'
F = f'{REPO}/english_lesson1_interactive.html'

# ─────────── 数据 ───────────
KNOW = [
    ("c1", "📖 话题精读 Nauru 瑙鲁", [
        "大洋洲<strong class=\"hl\">最小</strong>的国家；<strong class=\"hl\">赤道</strong>以南约 42 km",
        "<strong class=\"hl\">没有首都</strong>，但亚伦(Yaren)有政府建筑",
        "岩石<strong class=\"hl\">表层</strong>下有天然磷酸盐矿",
        "<strong class=\"hl\">1968 年</strong>才成为独立国家",
    ]),
    ("c2", "🔤 本讲核心词汇 5 个", [
        "<strong class=\"hl\">strange</strong> adj. 奇怪的；陌生的",
        "<strong class=\"hl\">breath</strong> n. 呼吸的空气；一口气（take a deep breath）",
        "<strong class=\"hl\">comfortable</strong> adj. 舒适的",
        "<strong class=\"hl\">prepared</strong> adj. 准备好的（be prepared for）",
        "<strong class=\"hl\">tired</strong> adj. 厌倦的；疲惫的（be tired of）",
    ]),
    ("c3", "🧩 划线词·阅读词汇", [
        "Oceania <strong class=\"hl\">大洋洲</strong> / equator <strong class=\"hl\">赤道</strong>",
        "capital <strong class=\"hl\">首都</strong> / government <strong class=\"hl\">政府</strong>",
        "surface <strong class=\"hl\">表面</strong> / independent <strong class=\"hl\">独立的</strong>",
    ]),
    ("c4", "💪 fight against 抵制；对抗", [
        "fight against + 名词：与……作斗争/对抗",
        "本讲：I <strong class=\"hl\">fought against</strong> the urge to waste time.",
        "我抵制住了浪费时间的冲动",
    ]),
    ("c5", "⚖️ nothing but 只有；只不过", [
        "nothing but + <strong class=\"hl\">名词/动名词</strong>",
        "Nothing but exploring new places <strong class=\"hl\">was</strong> meaningful.",
        "作主语时谓语用<strong class=\"hl\">单数</strong>",
    ]),
    ("c6", "😮 be surprised at 对……感到惊讶", [
        "be surprised at + 名词/从句",
        "no one <strong class=\"hl\">was surprised at</strong> how much I enjoyed it",
        "没人对我有多享受感到惊讶",
    ]),
    ("c7", "🔢 a little / with energy", [
        "a little + <strong class=\"hl\">形容词</strong>：有点……（my legs got a little sore）",
        "a little + <strong class=\"hl\">不可数名词</strong>：一点儿水",
        "fill sb <strong class=\"hl\">with</strong> sth：使某人充满……（fill me with energy）",
    ]),
    ("c8", "📦 不定代词：两者 vs 三者以上", [
        "<strong class=\"hl\">两者</strong>：both 都 / either 任一 / neither 都不",
        "<strong class=\"hl\">三者及以上</strong>：all 都 / any 任一 / none 都不",
        "neither of / none of + 复数名词，谓语用<strong class=\"hl\">单数</strong>",
    ]),
    ("c9", "🔗 neither...nor 就近原则", [
        "Neither Tom <strong class=\"hl\">nor his parents have</strong> been to Paris.",
        "谓语与<strong class=\"hl\">最近的主语</strong>一致（his parents → have）",
        "both...and 连接主语则用复数谓语",
    ]),
    ("c10", "⚠️ 本讲易错清单", [
        "neither（两者）/ none（三者以上）数量别混",
        "both...but <strong class=\"hl\">neither</strong> of them is...（but 后不能用 none）",
        "prepared ≠ ready（本讲考 prepared）；tired 表厌倦",
        "none of them <strong class=\"hl\">is</strong>（正式语体用单数）",
    ]),
]

QUIZ = [
    # 词汇 5
    ("“奇怪的；陌生的” adj. 是", ["A. strange", "B. stranger", "C. strangely", "D. strangers"], 0,
     "feel/look + <strong>形容词 strange</strong>（陌生的）；stranger 是名词“陌生人”。"),
    ("“呼吸的空气；一口气” n. 是", ["A. breathe", "B. breath", "C. breathing", "D. breaths"], 1,
     "固定搭配 <strong>take a deep breath</strong>（深呼吸）；breathe 是动词“呼吸”。"),
    ("“舒适的” adj. 是", ["A. comfort", "B. comfortably", "C. comfortable", "D. comforting"], 2,
     "修饰名词用形容词 <strong>comfortable</strong>；comfortably 是副词。"),
    ("“准备好的” adj. 是（be ___ for）", ["A. prepare", "B. prepared", "C. preparing", "D. preparation"], 1,
     "固定搭配 <strong>be prepared for</strong>（为……做好准备）；本讲词汇表答案为 prepared。"),
    ("“厌倦的；疲惫的” adj. 是（be ___ of）", ["A. tired", "B. tiring", "C. tiredly", "D. retire"], 0,
     "固定搭配 <strong>be tired of</strong>（厌倦……）；本讲词汇表答案为 tired。"),
    # 划线词中文 6
    ("Nauru is not only the smallest country in <u>Oceania</u>. 划线词意为", ["A. 大西洋", "B. 大洋洲", "C. 印度洋", "D. 欧洲"], 1,
     "Oceania = <strong>大洋洲</strong>（太平洋中部及周边岛屿）。"),
    ("Nauru sits about 42 km south of the <u>equator</u>. 划线词意为", ["A. 北极", "B. 海岸", "C. 赤道", "D. 沙漠"], 2,
     "equator = <strong>赤道</strong>（0° 纬线）；south of the equator 赤道以南。"),
    ("In fact, the country does not have a <u>capital</u>. 划线词意为", ["A. 国会", "B. 大厦", "C. 广场", "D. 首都"], 3,
     "capital = <strong>首都</strong>；也可指“资本、大写字母”，此处为首都。"),
    ("There are some <u>government</u> buildings in Yaren. 划线词意为", ["A. 政府", "B. 军队", "C. 公司", "D. 医院"], 0,
     "government = <strong>政府</strong>；government buildings 政府建筑。"),
    ("The phosphate is found right under the rock <u>surface</u>. 划线词意为", ["A. 内部", "B. 底部", "C. 表面", "D. 周围"], 2,
     "surface = <strong>表面</strong>；under the rock surface 岩石表层之下。"),
    ("Only in 1968 did the country become <u>independent</u>. 划线词意为", ["A. 独立的", "B. 富有的", "C. 贫穷的", "D. 美丽的"], 0,
     "independent = <strong>独立的</strong>；become independent 获得独立。"),
    # 选词填空 5
    ("选词填空：During holidays, I ___ the urge to waste time.（抵制住……的冲动）",
     ["A. nothing but", "B. fought against", "C. was surprised at", "D. with energy"], 1,
     "<strong>fight against</strong> = 抵制、对抗；fought 是其过去式。"),
    ("选词填空：___ exploring new places was meaningful.（只有探索新地方才有意义）",
     ["A. Nothing but", "B. Fought against", "C. Was surprised at", "D. A little"], 0,
     "<strong>nothing but</strong> = 只有；此处作主语，谓语用单数 was。"),
    ("选词填空：no one ___ how much I enjoyed it.（没人对我有多享受感到惊讶）",
     ["A. nothing but", "B. fought against", "C. was surprised at", "D. a little"], 2,
     "<strong>be surprised at</strong> = 对……感到惊讶，主语 no one → was。"),
    ("选词填空：Though my legs got ___ sore, the fresh air made every step worthwhile.（有点酸痛）",
     ["A. nothing but", "B. with energy", "C. was surprised at", "D. a little"], 3,
     "<strong>a little</strong> 修饰形容词 sore（有点酸痛）；a little 也可修饰不可数名词。"),
    ("选词填空：Holidays, short as they are, fill me ___.（让我充满活力）",
     ["A. nothing but", "B. fought against", "C. with energy", "D. a little"], 2,
     "固定搭配 <strong>fill sb with sth</strong>（使某人充满……）→ fill me with energy。"),
    # 语法 不定代词 5
    ("Of the two new films, ___ interests me much. I'd rather stay at home and read.",
     ["A. both", "B. neither", "C. none", "D. all"], 1,
     "两部电影（<strong>两者</strong>）都不感兴趣 → <strong>neither</strong>（两者都不），谓语单数 interests。"),
    ("___ Tom nor his parents have been to Paris, but they all dream of visiting it one day.",
     ["A. Both", "B. Either", "C. Neither", "D. None"], 2,
     "<strong>Neither...nor</strong> 固定搭配；谓语<strong>就近一致</strong>：nor his parents → have。"),
    ("—Which of the three dresses do you like? —___. They are either too long or too expensive.",
     ["A. Both", "B. Either", "C. Neither", "D. None"], 3,
     "三件裙子（<strong>三者以上</strong>）都不喜欢 → <strong>None</strong>（三者及以上都不）。"),
    ("The twins ___ love painting, but ___ of them is good at drawing animals.",
     ["A. both; neither", "B. neither; both", "C. both; none", "D. all; neither"], 0,
     "双胞胎<strong>两个都</strong>爱画画 → both；但<strong>两人都不</strong>擅长画动物 → neither of them + 单数 is。"),
    ("There are many books on the shelf, but ___ of them is about history. I need to go to another bookstore.",
     ["A. both", "B. neither", "C. all", "D. none"], 3,
     "书架上很多书（<strong>三者以上</strong>），没有一本是关于历史的 → <strong>none</strong> of them。"),
    ("—Which of the two sweaters do you prefer? —___. I'll take the third one on the left.",
     ["A. Neither", "B. None", "C. Both", "D. All"], 0,
     "两件毛衣（<strong>两者</strong>）都不喜欢，要第三件 → <strong>None</strong> 用于三者以上，此处用 Neither。"),
]

FLASH = [
    ("Nauru（瑙鲁）的基本情况？", "大洋洲<strong>最小</strong>的国家；位于<strong>赤道</strong>以南约 42 km；<strong>没有首都</strong>（亚伦有政府建筑）；岩石<strong>表层</strong>下有磷酸盐矿；<strong>1968 年</strong>独立。"),
    ("本讲 5 个核心词汇", "<strong>strange</strong> 奇怪的/陌生的；<strong>breath</strong> 呼吸；<strong>comfortable</strong> 舒适的；<strong>prepared</strong> 准备好的；<strong>tired</strong> 厌倦的。"),
    ("6 个阅读划线词的中文", "Oceania 大洋洲 / equator 赤道 / capital 首都 / government 政府 / surface 表面 / independent 独立的。"),
    ("fought against 怎么用？", "fight against = <strong>抵制、对抗</strong>。I fought against the urge to waste time.（我抵制住浪费时间的冲动）。"),
    ("nothing but 的用法与谓语？", "nothing but = <strong>只有；只不过</strong>，后接名词/动名词。作主语时谓语用<strong>单数</strong>：Nothing but exploring new places <strong>was</strong> meaningful."),
    ("be surprised at 什么意思？", "<strong>对……感到惊讶</strong>。no one was surprised at how much I enjoyed it."),
    ("a little 与 a few 的区别？", "a little + <strong>不可数</strong>名词/形容词（a little sore）；a few + <strong>可数</strong>名词复数。"),
    ("fill sb with sth 释义", "<strong>使某人充满……</strong>：Holidays fill me with energy.（假期让我充满活力）。"),
    ("不定代词：两者怎么表达？", "both 两个都 / either 两者中任一 / neither 两者都不。谓语搭配：neither of them <strong>is</strong>。"),
    ("不定代词：三者及以上怎么表达？", "all 全都 / any 任一 / none 都不。none of them <strong>is</strong>（正式语体用单数）。"),
    ("neither...nor 的谓语规则？", "<strong>就近原则</strong>：谓语跟最近的主语一致。Neither Tom nor his parents <strong>have</strong> been to Paris."),
    ("both...but neither 结构怎么理解？", "The twins <strong>both</strong> love painting, but <strong>neither</strong> of them is good at drawing animals.（两个都爱画画，但两人都不擅长画动物）。"),
]

ERRORS = [
    ("❌ neither 与 none 数量混用",
     "Of the two films, none interests me. / Of the three dresses, neither fits me.",
     "<strong>两者</strong>用 neither；<strong>三者及以上</strong>用 none。看清题干中的数量词（two / three）。"),
    ("❌ neither...nor 谓语错用复数",
     "Neither Tom nor his parents <u>has</u> been to Paris.（误按 Tom 定谓语）",
     "<strong>就近原则</strong>：谓语与最近的主语 his parents 一致 → <strong>have</strong>。"),
    ("❌ but 后误用 none 搭配 both",
     "The twins both love painting, but <u>none</u> of them is good at drawing animals.",
     "前句是<strong>两者</strong>（the twins），后半句应用 <strong>neither</strong> of them is...。"),
    ("❌ 准备好的误写 ready",
     "词汇表“准备好的”写成 <u>ready</u>。",
     "本讲词汇表答案为 <strong>prepared</strong>（be prepared for）；ready 虽同义但不符本讲考纲。"),
    ("❌ 厌倦的误写 bored",
     "词汇表“厌倦的”写成 <u>bored</u>。",
     "本讲答案用 <strong>tired</strong>（be tired of 厌倦）；bored 是 -ed 形容词（感到无聊）。"),
    ("❌ a little 与 with energy 位置混用",
     "Holidays fill me <u>a little</u>. / My legs got <u>with energy</u> sore.",
     "fill sb <strong>with energy</strong>（充满活力）；a little 修饰形容词：got <strong>a little</strong> sore。"),
    ("❌ nothing but 作主语时谓语误用复数",
     "Nothing but exploring new places <u>were</u> meaningful.",
     "nothing but + 动名词作主语视作单数 → <strong>was</strong> meaningful。"),
]

# ─────────── 组装 ───────────
h = open(F, encoding='utf-8').read()
nq, nf, ne, nk = len(QUIZ), len(FLASH), len(ERRORS), len(KNOW)

# 1) hero / meta / 文案
h = h.replace('<h1><i class="fas fa-globe-asia"></i> Holidays &amp; Summer Vacation · 互动学习</h1>',
              '<h1><i class="fas fa-globe-asia"></i> Nauru &amp; Holidays · 互动学习</h1>', 1)
h = re.sub(r'<p>2026秋双语八年级 B班 · 第1讲 · \d+ 题 · \d+ 卡牌 \| 双语英语</p>',
           f'<p>2026秋双语八年级 C班 · 第1讲 · {nq} 题 · {nf} 卡牌 | 双语英语</p>', h, count=1)
h = re.sub(r'<span><i class="fas fa-check-circle"[^>]*></i> \d+道测验题</span>',
           f'<span><i class="fas fa-check-circle" style="color:var(--success)"></i> {nq}道测验题</span>', h, count=1)
h = re.sub(r'<span><i class="fas fa-layer-group"></i> \d+张知识卡</span>',
           f'<span><i class="fas fa-layer-group"></i> {nf}张知识卡</span>', h, count=1)
h = re.sub(r'<span><i class="fas fa-exclamation-triangle" style="color:var(--danger)"></i> \d+大易错点</span>',
           f'<span><i class="fas fa-exclamation-triangle" style="color:var(--danger)"></i> {ne}大易错点</span>', h, count=1)
h = h.replace('<div class="section-header"><i class="fas fa-sitemap" style="color:#667eea"></i> 第一讲 · Holidays &amp; Summer Vacation</div>',
              '<div class="section-header"><i class="fas fa-sitemap" style="color:#667eea"></i> 第一讲 · Nauru &amp; Holidays（C班）</div>', 1)

# 2) 知识图谱整段
g0 = h.find('<div class="knowledge-grid">'); g1 = h.find('<div class="teacher-talk">', g0)
cards = ''
for cls, title, lis in KNOW:
    items = ''.join(f'<li>{x}</li>' for x in lis)
    cards += f'      <div class="knowledge-card {cls}"><h3>{title}</h3><ul>{items}</ul></div>\n'
h = h[:g0] + '<div class="knowledge-grid">\n' + cards + '    </div>\n    ' + h[g1:]

# 3) teacher-talk 整段
t0 = h.find('<div class="teacher-talk">'); t1 = h.find('<div id="tab-quiz"', t0)
tt = f'''<div class="teacher-talk">
      <h4><i class="fas fa-microphone-alt"></i> 🎙️ 课堂要点 · 第一讲（C班 · Nauru &amp; Holidays）</h4>
      <p><strong>本讲核心</strong>：2026秋双语八年级 C班第1讲。①阅读：<strong>Nauru 瑙鲁</strong>（大洋洲最小国、赤道以南、无首都、磷酸盐、1968独立）6 个划线词；②词汇 5 个：<strong>strange / breath / comfortable / prepared / tired</strong>；③短语 5 个：<strong>fight against、nothing but、be surprised at、a little、fill sb with energy</strong>；④语法：<strong>不定代词</strong>（两者 both/either/neither；三者以上 all/any/none）。</p>
      <p><strong>练习册重点</strong>：假期短文选词填空（I fought against the urge... / Nothing but exploring... / no one was surprised at... / got a little sore / fill me with energy）+ 不定代词单选（neither 与 none 的数量判断）。做题技巧：先判断"两者还是三者以上"，再定 both/either/neither 还是 all/any/none。</p>
      <p><strong>易错提醒</strong>：① 两者用 <strong>neither</strong>、三者以上用 <strong>none</strong>；② neither...nor 谓语<strong>就近一致</strong>（nor his parents → have）；③ The twins <strong>both</strong> love..., but <strong>neither</strong> of them is...；④ 词汇表答案：准备好的=<strong>prepared</strong>、厌倦的=<strong>tired</strong>；⑤ fill sb <strong>with</strong> energy（不是 fill sb a little）。</p>
      <p><strong>🎓 老师课堂总结</strong> — 本讲是阅读+语法双线：阅读抓 Nauru 的关键数字与事实（最小国/42km/无首都/1968），语法抓不定代词的"数量分界"。neither...nor 与 none of 的谓语形式是中考高频考点，务必背熟"就近原则"和"none of + 复数 + 单数谓语"。<strong>本页已按 C 班材料全新替换（原 B 班内容已下线）。</strong></p>
    </div>
    '''
h = h[:t0] + tt + h[t1:]

# 4) questions 数组
q0 = h.find('const questions = ['); q1 = h.find('const flashcards = [', q0)
qdata = [{'q': q, 'opts': o, 'ans': a, 'exp': e} for q, o, a, e in QUIZ]
h = h[:q0] + 'const questions = ' + json.dumps(qdata, ensure_ascii=False, indent=1) + ';\n\n\n' + h[q1:]

# 5) flashcards 数组
f0 = h.find('const flashcards = ['); f1 = h.find('errors = [', f0)
fdata = [{'front': x, 'back': y} for x, y in FLASH]
h = h[:f0] + 'const flashcards = ' + json.dumps(fdata, ensure_ascii=False, indent=1) + ';\n\n\n' + h[f1:]

# 6) errors 数组
e0 = h.find('errors = ['); e1 = h.find('function toast', e0)
edata = [{'title': t, 'wrong': w, 'right': r} for t, w, r in ERRORS]
h = h[:e0] + 'errors = ' + json.dumps(edata, ensure_ascii=False, indent=1) + ';\n\n\n\n' + h[e1:]

# 7) 文案 B班 → C班
h = h.replace('双语B班', '双语C班').replace('B班第1讲', 'C班第1讲')
h = h.replace('第1讲 Holidays &amp; 暑假话题', '第1讲 Nauru &amp; Holidays话题')
h = h.replace('第1讲 Holidays &amp; Summer Vacation | 双语英语', '第1讲 Nauru &amp; Holidays | 双语英语')
h = h.replace('共15张知识卡', f'共{nf}张知识卡')
h = h.replace('<div class="quiz-stats" id="quizStats">0 / 32</div>', f'<div class="quiz-stats" id="quizStats">0 / {nq}</div>')

open(F, 'w', encoding='utf-8').write(h)

# 复验
import subprocess
js = r"""const fs=require('fs');const html=fs.readFileSync('english_lesson1_interactive.html','utf8');const re=/<script[^>]*>([\s\S]*?)<\/script>/g;let m,ok=true;while((m=re.exec(html))){try{new Function(m[1])}catch(e){ok=false;console.log('ERR',e.message)}}console.log(ok?'JS OK':'JS ERR')"""
r = subprocess.run(['node','-e',js], capture_output=True, text=True, cwd=REPO)
hh = open(F, encoding='utf-8').read()
print(r.stdout.strip())
print(f'题{nq} 卡{nf} 错{ne} 知识{nk}')
print('div:', len(re.findall(r'<div\b', hh)), '/', hh.count('</div>'))
print('残留 B班:', hh.count('B班'), '| sumer Vacation:', hh.count('Summer Vacation'))
