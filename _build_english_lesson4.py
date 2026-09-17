#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""_build_english_lesson4.py — 英语第四课时 Section B (1a~1d) 词汇与句式 互动页
素材: 老师讲义照片（空白默写清单，AI 按教材补全答案）
基座: english_lesson3_interactive.html
输出: english_lesson4_interactive.html
"""
import re, json, subprocess

REPO = '/home/administrator/xuci-jiancha'
BASE_F = f'{REPO}/english_lesson3_interactive.html'
OUT_F = f'{REPO}/english_lesson4_interactive.html'

KNOW = [
    ("c1", "📘 本课概览（Section B 1a~1d）", [
        "内容：<strong class=\"hl\">第四课时 Section B (1a~1d)</strong> 的重点单词、词形变化、重点语块与句式",
        "主题场景：<strong class=\"hl\">参观博物馆/旅行经历</strong>——玻璃“眼泪”艺术作品、战争与和平、宫殿与地铁",
        "学法：先按讲义<strong class=\"hl\">空白默写</strong>，再对照英文答案订正，隔天复默一遍",
    ]),
    ("c2", "🔤 重点单词（12 个）", [
        "<strong class=\"hl\">square</strong> 广场；正方形／正方形的；平方的",
        "<strong class=\"hl\">during</strong> 在……期间（介词，后接名词）",
        "<strong class=\"hl\">victory</strong> 胜利；成功｜<strong class=\"hl\">against</strong> 反对；与……相反；紧靠",
        "<strong class=\"hl\">artwork</strong> 艺术作品；插图｜<strong class=\"hl\">tear</strong> 眼泪；泪水",
    ]),
    ("c3", "🔤 重点单词（续）", [
        "<strong class=\"hl\">remind</strong> 提醒；使想起（remind sb. of sth. / remind sb. to do sth.）",
        "<strong class=\"hl\">noon</strong> 正午；中午｜<strong class=\"hl\">subway</strong> 地下铁道系统",
        "<strong class=\"hl\">station</strong> 车站；所；局｜<strong class=\"hl\">palace</strong> 王宫；宫殿",
        "<strong class=\"hl\">accordion</strong> 手风琴",
    ]),
    ("c4", "🧩 词形变化（一）", [
        "<strong class=\"hl\">Russian</strong> 俄罗斯的；俄罗斯人；俄语 → <strong class=\"hl\">Russia</strong> 俄罗斯",
        "<strong class=\"hl\">fight</strong> 战斗；搏斗；斗争／打仗；打架 → 过去式 <strong class=\"hl\">fought</strong>",
        "<strong class=\"hl\">peace</strong> 和平；太平 → <strong class=\"hl\">peaceful</strong> 和平的；安静的；平静的",
    ]),
    ("c5", "🧩 词形变化（二）", [
        "<strong class=\"hl\">easily</strong> 容易地（副词） → <strong class=\"hl\">easy</strong> 容易的（形容词）",
        "<strong class=\"hl\">forget</strong> 忘记 → 过去式 <strong class=\"hl\">forgot</strong> → <strong class=\"hl\">forgetful</strong> 健忘的",
        "<strong class=\"hl\">sick</strong> 恶心的；生病的（feel sick 感到不舒服）",
    ]),
    ("c6", "🧱 重点语块（旅行类）", [
        "<strong class=\"hl\">travel experience</strong> 假期/旅行经历",
        "<strong class=\"hl\">be excited about doing sth.</strong> 做……感到兴奋",
        "<strong class=\"hl\">travel around / look around</strong> 四处逛逛；到处旅行",
        "<strong class=\"hl\">tour guide</strong> 导游｜<strong class=\"hl\">subway station</strong> 地铁站",
    ]),
    ("c7", "🧱 重点语块（动作类）", [
        "<strong class=\"hl\">fight against / fight with</strong> 与……作战；与……作斗争",
        "<strong class=\"hl\">walk through the hall</strong> 走过大厅｜<strong class=\"hl\">take out</strong> 拿出；取出",
        "<strong class=\"hl\">want to do sth. / would like to do sth.</strong> 想要做某事",
        "<strong class=\"hl\">get together</strong> 聚会；相聚",
    ]),
    ("c8", "🧱 重点语块（感受类）", [
        "<strong class=\"hl\">feel sick</strong> 感到恶心；感到不舒服",
        "<strong class=\"hl\">have/get a good sleep</strong> 睡个好觉",
        "<strong class=\"hl\">fresh and cool</strong> 清新凉爽",
        "<strong class=\"hl\">thousands of</strong> 数以千计的；成千上万的",
    ]),
    ("c9", "📝 重点句式（1）", [
        "在一个展厅里，我看到了一幅作品，上面有成千上万滴玻璃“眼泪”正在落下。",
        "→ In one of the halls, I saw a work of art with thousands of glass \"tears\" <strong class=\"hl\">falling down</strong>.",
        "要点：<strong class=\"hl\">with + 宾语 + doing</strong> 结构（伴随动作）",
    ]),
    ("c10", "📝 重点句式（2）(3)", [
        "它提醒我们，战争是可怕的，和平来之不易。→ It <strong class=\"hl\">reminds us that</strong> war is terrible and peace doesn't come easily.",
        "我觉得我好像走在一座宫殿里。→ I <strong class=\"hl\">felt like</strong> I was walking in a palace.",
        "要点：remind sb. that… 宾语从句；feel like + 句子/doing",
    ]),
    ("c11", "⚠️ 易混辨析", [
        "<strong class=\"hl\">during</strong>（介词+名词）vs for（时间段）vs while（+句子）",
        "<strong class=\"hl\">thousands of</strong>（概数，带 s）vs two thousand（确数，不带 s）",
        "<strong class=\"hl\">against</strong>（介词）vs fight against（动词短语）",
        "<strong class=\"hl\">forget / forgot / forgetful</strong>：动词—过去式—形容词三态；注意 forgetful = 健忘的（形容人）",
    ]),
    ("c12", "🎯 学法建议（若琳）", [
        "① 先按讲义空白<strong class=\"hl\">默写</strong>；② 对照英文答案<strong class=\"hl\">红笔订正</strong>；③ 隔天<strong class=\"hl\">复默</strong>（重点：sickness / against / accordion / forgetful / thousands of）",
        "三个句式可作“旅行/参观”话题作文的<strong class=\"hl\">模板句</strong>",
        "默写错词可直接记入<strong class=\"hl\">错题库</strong>（英语科目），按三层练巩固",
    ]),
]

QUIZ = [
    # 重点单词 12
    ("“广场；正方形（n.）/正方形的（adj.）”对应的单词是",
     ["A. square", "B. station", "C. palace", "D. victory"], 0,
     "<strong>square</strong> 广场；正方形／正方形的；平方的（注意一词多词性）。"),
    ("“在……期间（prep.）”对应的单词是",
     ["A. during", "B. while", "C. between", "D. among"], 0,
     "<strong>during</strong> + 名词（during the holiday）；while 后面要接句子。"),
    ("“胜利；成功（n.）”对应的单词是",
     ["A. victory", "B. defeat", "C. success", "D. prize"], 0,
     "<strong>victory</strong> 胜利；成功（win a victory）。"),
    ("“反对；与……相反；紧靠（prep.）”对应的单词是",
     ["A. against", "B. across", "C. among", "D. above"], 0,
     "<strong>against</strong>：反对（be against）、靠着（lean against）、与……作斗争（fight against）。"),
    ("“艺术作品；插图（n.）”对应的单词是",
     ["A. artwork", "B. article", "C. artist", "D. artless"], 0,
     "<strong>artwork</strong> 艺术作品；插图（也可说 a work of art）。"),
    ("“眼泪；泪水（n.）”对应的单词是",
     ["A. tear", "B. tear（撕）", "C. tears of joy", "D. wear"], 0,
     "<strong>tear</strong> 眼泪（可数名词，常用复数 tears）；注意 tear 作动词读 /teə/ 意为“撕”。"),
    ("“提醒；使想起（v.）”对应的单词是",
     ["A. remind", "B. remember", "C. mind", "D. recall"], 0,
     "<strong>remind</strong> sb. of sth. / remind sb. to do sth. / remind sb. that…"),
    ("“正午；中午（n.）”对应的单词是",
     ["A. noon", "B. night", "C. afternoon", "D. midnight"], 0,
     "<strong>noon</strong> 正午（at noon）；midnight 午夜。"),
    ("“地下铁道系统（n.）”对应的单词是",
     ["A. subway", "B. highway", "C. railway", "D. tunnel"], 0,
     "<strong>subway</strong>（美式）地下铁道；英式用 underground / metro。"),
    ("“车站；所；局（n.）”对应的单词是",
     ["A. station", "B. stop", "C. hall", "D. square"], 0,
     "<strong>station</strong> 车站；所；局（subway station 地铁站、police station 派出所）。"),
    ("“王宫；宫殿（n.）”对应的单词是",
     ["A. palace", "B. castle", "C. hall", "D. tower"], 0,
     "<strong>palace</strong> 王宫；宫殿（the Summer Palace 颐和园）。"),
    ("“手风琴（n.）”对应的单词是",
     ["A. accordion", "B. guitar", "C. violin", "D. piano"], 0,
     "<strong>accordion</strong> 手风琴（play the accordion）。"),
    # 词形变化 6
    ("“俄罗斯的；俄罗斯人；俄语”与“俄罗斯”分别是",
     ["A. Russian / Russia", "B. Russia / Russian", "C. Russian / Russian", "D. Russion / Russia"], 0,
     "国名 <strong>Russia</strong>（俄罗斯）→ 形容词/人/语言 <strong>Russian</strong>。"),
    ("“战斗；搏斗（n.）/打仗；打架（v.）”的过去式是",
     ["A. fought", "B. fighted", "C. fighting", "D. fights"], 0,
     "fight → <strong>fought</strong>（不规则动词，注意 -ought 拼写）。"),
    ("“和平（n.）”与“和平的；安静的（adj.）”分别是",
     ["A. peace / peaceful", "B. peaceful / peace", "C. peace / peaceable", "D. peace / peacefully"], 0,
     "<strong>peace</strong>（名词）→ <strong>peaceful</strong>（形容词）；peacefully 是副词。"),
    ("“容易地（adv.）”与“容易的（adj.）”分别是",
     ["A. easily / easy", "B. easy / easily", "C. easily / ease", "D. easy / ease"], 0,
     "形容词 <strong>easy</strong>（以 y 结尾）→ 副词变 y 为 i 加 ly：<strong>easily</strong>。"),
    ("“忘记（v.）”的过去式与“健忘的（adj.）”分别是",
     ["A. forgot / forgetful", "B. forgetted / forgetful", "C. forgot / forgetting", "D. forget / forgetful"], 0,
     "forget → <strong>forgot</strong>（过去式）；<strong>forgetful</strong> = 健忘的（形容人）。"),
    ("“恶心的；生病的（adj.）”对应的单词是",
     ["A. sick", "B. ill", "C. sickness", "D. disease"], 0,
     "<strong>sick</strong>（形容词，feel sick 感到不舒服）；ill 多作表语；sickness 是名词。"),
    # 语块 6
    ("“做……感到兴奋”的正确表达是",
     ["A. be excited about doing sth.", "B. be exciting about doing sth.", "C. be excited to do", "D. excite doing sth."], 0,
     "<strong>be excited about doing sth.</strong>（人做主语用 -ed 形式）。"),
    ("“与……作战；与……作斗争”的正确表达是",
     ["A. fight against / fight with", "B. fight for / fight to", "C. fight on / fight in", "D. fight off / fight up"], 0,
     "<strong>fight against</strong>（与……作斗争）；fight with 也可表示“与……一起战斗/与……打架”。"),
    ("“数以千计的；成千上万的”的正确表达是",
     ["A. thousands of", "B. thousand of", "C. two thousands", "D. thousands"], 0,
     "概数用 <strong>thousands of</strong>（有 s 有 of）；确数 two thousand 不加 s。"),
    ("“走过大厅”的正确表达是",
     ["A. walk through the hall", "B. walk across the hall", "C. walk over the hall", "D. walk on the hall"], 0,
     "<strong>walk through the hall</strong>（从内部穿过用 through）。"),
    ("“拿出；取出”与“聚会；相聚”分别是",
     ["A. take out / get together", "B. take off / get up", "C. take in / get on", "D. take away / get back"], 0,
     "<strong>take out</strong> 拿出；取出｜<strong>get together</strong> 聚会；相聚。"),
    ("“睡个好觉”与“清新凉爽”分别是",
     ["A. have/get a good sleep / fresh and cool", "B. sleep good / cool and fresh", "C. go to sleep / fresh cool", "D. have a nice dream / cool fresh"], 0,
     "<strong>have/get a good sleep</strong> 睡个好觉；<strong>fresh and cool</strong> 清新凉爽。"),
    # 句式 3
    ("翻译：“在一个展厅里，我看到了一幅作品，上面有成千上万滴玻璃‘眼泪’正在落下。”",
     ["A. In one of the halls, I saw a work of art with thousands of glass \"tears\" falling down.", "B. In one of the halls, I see a work of art has thousands of glass \"tears\" fall down.", "C. In one of the halls, I saw a work of art with thousands of glass \"tears\" fell down.", "D. In one of the halls, I saw a work of art thousands of glass \"tears\" falling down."], 0,
     "用 <strong>with + 宾语 + doing</strong> 表示伴随动作：with thousands of glass \"tears\" falling down（falling 是现在分词，不能换成 fell）。"),
    ("翻译：“它提醒我们，战争是可怕的，和平来之不易。”",
     ["A. It reminds us that war is terrible and peace doesn't come easily.", "B. It reminds us war is terrible and peace doesn't come easy.", "C. It reminds us of war is terrible and peace doesn't come easily.", "D. It reminds that war is terrible and peace doesn't come easily."], 0,
     "<strong>remind sb. that + 从句</strong>；“来之不易”用 doesn't come easily（副词 easily 修饰动词）。"),
    ("翻译：“我觉得我好像走在一座宫殿里。”",
     ["A. I felt like I was walking in a palace.", "B. I felt like walking in a palace.", "C. I felt that like I was walking in a palace.", "D. I feel like I am walking in a palace."], 0,
     "<strong>feel like + 句子</strong>（过去时 felt），表示“觉得好像……”。"),
]

FLASH = [
    ("广场；正方形／正方形的", "<strong>square</strong>（n./adj.）"),
    ("在……期间（介词）", "<strong>during</strong> + 名词（during the holiday）"),
    ("胜利；成功", "<strong>victory</strong>"),
    ("反对；与……相反；紧靠", "<strong>against</strong>"),
    ("艺术作品；插图", "<strong>artwork</strong>（a work of art）"),
    ("眼泪；泪水", "<strong>tear</strong>（tears）"),
    ("提醒；使想起", "<strong>remind</strong> sb. of sth. / to do sth. / that…"),
    ("正午；中午", "<strong>noon</strong>（at noon）"),
    ("地下铁道系统／车站", "<strong>subway</strong> ／ <strong>station</strong>"),
    ("王宫；宫殿／手风琴", "<strong>palace</strong> ／ <strong>accordion</strong>"),
    ("俄罗斯（国名）／俄罗斯的；俄语", "<strong>Russia</strong> ／ <strong>Russian</strong>"),
    ("与……作斗争／数以千计的", "<strong>fight against</strong> ／ <strong>thousands of</strong>"),
]

ERRORS = [
    ("❌ during / while / for 混用",
     "during he was away ／ during three years（错）",
     "<strong>during + 名词</strong>；<strong>while + 句子</strong>；<strong>for + 时间段</strong>。"),
    ("❌ thousands of 写成 thousand of / two thousands",
     "thousand of glass tears（错）",
     "概数：<strong>thousands of</strong>（s + of 都要有）；确数：two <strong>thousand</strong>（不写 s）。"),
    ("❌ 忘记的过去式写错",
     "forgetted（错）",
     "forget → <strong>forgot</strong>（不规则变化）；健忘的 = <strong>forgetful</strong>。"),
    ("❌ easy 变副词直接加 ly",
     "easyly（错）",
     "以“辅音字母 + y”结尾：变 y 为 i 再加 ly → <strong>easily</strong>。"),
    ("❌ be excited about 后接动词原形",
     "be excited about go there（错）",
     "介词 about 后接<strong>动名词</strong>：be excited about <strong>going</strong> there。"),
    ("❌ with 复合结构中的动词形式用错",
     "with thousands of tears <em>fell</em> down（错）",
     "<strong>with + 宾语 + doing</strong>（主动进行）：with tears <strong>falling</strong> down。"),
    ("❌ feel like 后接动词/句子混用",
     "I felt like walk in a palace（错）",
     "feel like + <strong>句子</strong>（I felt like I was walking…）或 + <strong>doing</strong>（feel like walking）。"),
]

h = open(BASE_F, encoding='utf-8').read()
nq, nf, ne, nk = len(QUIZ), len(FLASH), len(ERRORS), len(KNOW)

h = re.sub(r'<title>[^<]*</title>', '<title>📘 Section B 词汇与句式 · 第四课时</title>', h, count=1)
h = re.sub(r'<h1[^>]*>.*?</h1>', '<h1><i class="fas fa-spell-check"></i> Section B 词汇与句式 · 第四课时</h1>', h, count=1, flags=re.DOTALL)
h = re.sub(r'<p>[^<]*\| 英语[^<]*</p>', f'<p>第四课时 Section B (1a~1d) · {nq} 题 · {nf} 卡牌 | 词汇默写自测</p>', h, count=1)
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
      <h4><i class="fas fa-microphone-alt"></i> 📘 本课要点 · 第四课时 Section B (1a~1d)</h4>
      <p><strong>重点单词（12）</strong>：square 广场/正方形｜during 在……期间｜victory 胜利｜against 反对/紧靠｜artwork 艺术作品｜tear 眼泪｜remind 提醒｜noon 正午｜subway 地铁｜station 车站｜palace 宫殿｜accordion 手风琴。</p>
      <p><strong>词形变化</strong>：Russia → Russian；fight → <strong>fought</strong>；peace → <strong>peaceful</strong>；easy → <strong>easily</strong>；forget → <strong>forgot</strong> → <strong>forgetful</strong>；sick 恶心的/生病的。</p>
      <p><strong>重点语块</strong>：travel experience｜be excited about doing sth.｜fight against｜walk through the hall｜tour guide｜thousands of｜want to do sth.｜feel sick｜have a good sleep｜fresh and cool｜travel around｜subway station｜take out｜get together。</p>
      <p><strong>重点句式</strong>：① In one of the halls, I saw a work of art with thousands of glass "tears" falling down.（with + 宾语 + doing）② It reminds us that war is terrible and peace doesn't come easily.（remind sb. that…）③ I felt like I was walking in a palace.（feel like + 句子）</p>
      <p><strong>📝 复习建议</strong>：先照讲义空白默写 → 对照本页答案红笔订正 → 隔天复默；错词直接记入错题库（英语科目）。⚠️ 本页英文为 AI 按教材语境补全，若与课本用词有差异以课本为准。</p>
    </div>
    '''
h = h[:t0] + tt + h[t1:]

q0 = h.find('const questions = ['); q1 = h.find('const flashcards = [', q0)

def rotate(opts, ans, target):
    """把正确项挪到 target 位置，打散答案分布"""
    correct = opts[ans]
    rest = [o for i, o in enumerate(opts) if i != ans]
    return rest[:target] + [correct] + rest[target:], target

qdata = []
for i, (q, o, a, e) in enumerate(QUIZ):
    no, na = rotate(o, a, i % 4)
    qdata.append({'q': q, 'opts': no, 'ans': na, 'exp': e})
h = h[:q0] + 'const questions = ' + json.dumps(qdata, ensure_ascii=False, indent=1) + ';\n\n\n' + h[q1:]

f0 = h.find('const flashcards = ['); f1 = h.find('errors = [', f0)
fdata = [{'front': x, 'back': y} for x, y in FLASH]
h = h[:f0] + 'const flashcards = ' + json.dumps(fdata, ensure_ascii=False, indent=1) + ';\n\n\n' + h[f1:]

e0 = h.find('errors = ['); e1 = h.find('function toast', e0)
edata = [{'title': t, 'wrong': w, 'right': r} for t, w, r in ERRORS]
h = h[:e0] + 'errors = ' + json.dumps(edata, ensure_ascii=False, indent=1) + ';\n\n\n\n' + h[e1:]

h = re.sub(r"QUIZ_PROG_KEY='[^']*'", "QUIZ_PROG_KEY='quiz_progress_english_lesson4'", h, count=1)
h = re.sub(r"WRONG_HISTORY_KEY='[^']*'", "WRONG_HISTORY_KEY='quiz_english_lesson4_wrong'", h, count=1)
h = re.sub(r"state_check'", "state_check'", h, count=1)
h = h.replace('english_lesson3_state_check', 'english_lesson4_state_check')
h = re.sub(r'第3讲[^<|]{0,20}', '第四课时 Section B', h, count=1)
h = h.replace('Smart Devices 阅读与语法 · 课堂补充', '第四课时 Section B 词汇与句式')
h = h.replace('英语 · 第3讲', '英语 · 第四课时')
h = re.sub(r"subject:'[^']*'", "subject:'英语(课内)'", h, count=2)
h = re.sub(r"chapter:'[^']*'", "chapter:'第四课时 Section B (1a~1d) 词汇与句式'", h, count=2)
h = re.sub(r"tags:'[^']*'", "tags:'英语,词汇,SectionB,词形变化,语块,句式,默写自测'", h, count=2)
h = re.sub(r'<div class="quiz-stats" id="quizStats">0 / \d+</div>', f'<div class="quiz-stats" id="quizStats">0 / {nq}</div>', h, count=1)
h = re.sub(r'共\d+张知识卡', f'共{nf}张知识卡', h, count=1)
open(OUT_F, 'w', encoding='utf-8').write(h)

js = r"""const fs=require('fs');const html=fs.readFileSync('english_lesson4_interactive.html','utf8');const re=/<script[^>]*>([\s\S]*?)<\/script>/g;let m,ok=true;while((m=re.exec(html))){try{new Function(m[1])}catch(e){ok=false;console.log('ERR',e.message)}}console.log(ok?'JS OK':'JS ERR')"""
r = subprocess.run(['node','-e',js], capture_output=True, text=True, cwd=REPO)
hh = open(OUT_F, encoding='utf-8').read()
print(r.stdout.strip())
print(f'题{nq} 卡{nf} 错{ne} 知识{nk}')
print('div:', len(re.findall(r'<div\b', hh)), '/', hh.count('</div>'))
print('残留 Smart Devices:', hh.count('Smart Devices'), '| lesson3:', hh.count('english_lesson3'))
