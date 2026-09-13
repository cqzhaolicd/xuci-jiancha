#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""_build_chinese_lesson2.py — 语文第2课 山水游记专题（源自 20260912 课堂录音笔记）
基座: chinese26q_lesson1_interactive.html
输出: chinese26q_lesson2_interactive.html
"""
import re, json, subprocess

REPO = '/home/administrator/xuci-jiancha'
BASE_F = f'{REPO}/chinese26q_lesson1_interactive.html'
OUT_F = f'{REPO}/chinese26q_lesson2_interactive.html'

KNOW = [
    ("c1", "🏔️ 山水游记发展脉络·魏晋南北朝（萌芽）", [
        "代表：<strong class=\"hl\">王羲之、谢灵运、陶渊明</strong>",
        "内容以<strong class=\"hl\">纯描摹山水</strong>为主",
        "核心情感：对自然山水的<strong class=\"hl\">欣赏与陶醉</strong>",
    ]),
    ("c2", "🌊 唐代（情景交融）", [
        "文人开始把<strong class=\"hl\">主观情感融入景物</strong>描写，实现情景交融",
        "代表：柳宗元被贬永州后创作的<strong class=\"hl\">《永州八记》</strong>",
        "其中<strong class=\"hl\">《小石潭记》要求全文背诵</strong>",
    ]),
    ("c3", "📖 宋代（寓理于景）", [
        "受<strong class=\"hl\">宋明理学</strong>思辨风气影响，收敛泛滥抒情，转向<strong class=\"hl\">寓理于景</strong>",
        "代表：苏轼<strong class=\"hl\">《赤壁赋》</strong>、王安石<strong class=\"hl\">《游褒禅山记》</strong>",
        "侧重探讨天地万物运行规律与为人处世的道理",
    ]),
    ("c4", "🏛️ 明清（鼎盛成熟期）", [
        "山水游记发展至<strong class=\"hl\">鼎盛成熟期</strong>，创作群体多元",
        "文人：<strong class=\"hl\">公安三袁、张岱</strong>；官员：<strong class=\"hl\">施润章</strong>（关注民生政务）",
        "内容涵盖山水描摹、个人志趣、民生思考，<strong class=\"hl\">解读难度最高</strong>",
    ]),
    ("c5", "📍 成都本地出题背景", [
        "陆游曾在成都<strong class=\"hl\">崇州</strong>长期居住（成都东站坐高铁 15 分钟可达其故居）",
        "素材：《入蜀记》（陆游）、<strong class=\"hl\">《吴船录》（范成大）</strong>",
        "杨慎整理蜀地相关文言文 <strong class=\"hl\">1600 多篇</strong>；《华阳国志》篇目",
        "⚠️ <strong class=\"hl\">半期考试后</strong>山水游记阅读题难度明显提升",
    ]),
    ("c6", "📜 《浣花溪记》文本背景", [
        "作者：明代文学家<strong class=\"hl\">袁中道</strong>（属明清山水游记）",
        "篇幅较长：八上后半段就会遇到同篇幅难度题目，八下日常训练基本都是这个长度",
    ]),
    ("c7", "🔤 文言知识点：并提·互文·宾语前置", [
        "<strong class=\"hl\">并提</strong>、<strong class=\"hl\">互文</strong>：古诗文专属修辞手法",
        "<strong class=\"hl\">“水木清华”</strong>是<strong class=\"hl\">宾语前置</strong>句式",
        "正确翻译：<strong class=\"hl\">流水清澈、树木茂盛</strong>",
    ]),
    ("c8", "👥 人文背景：杜甫与严武", [
        "严武曾为杜甫在<strong class=\"hl\">浣花溪畔</strong>安排居所，保障其吃穿用度",
        "严武去世后杜甫失去依托，离开浣花溪前往<strong class=\"hl\">重庆夔门</strong>",
        "在夔门创作千古第一律诗<strong class=\"hl\">《登高》</strong>",
    ]),
    ("c9", "🖼️ 写作手法：移步换景", [
        "全文用<strong class=\"hl\">移步换景</strong>串联：万里桥 → 杜甫草堂 → 百花潭等景点逐一串联",
        "整体氛围<strong class=\"hl\">清幽悠远</strong>",
        "寄寓作者对杜甫从容不迫、热爱生活品质的<strong class=\"hl\">敬佩与赞美</strong>",
    ]),
    ("c10", "🎯 情感推断三路径（解题核心）", [
        "① 锁定文章<strong class=\"hl\">结尾关键总结句</strong>，提取直接流露的情感",
        "② 通过<strong class=\"hl\">景物特点反推</strong>情感（如“冷月”常对应战乱后的悲痛）",
        "③ 结合<strong class=\"hl\">作者生平与写作背景</strong>（如苏轼被贬黄州 → 苦闷与怀才不遇）",
    ]),
    ("c11", "🧭 分难度文本解题法", [
        "<strong class=\"hl\">魏晋南北朝（简单）</strong>：游踪 → 景物 → 时间季节变化 → 结合氛围推导情感",
        "<strong class=\"hl\">唐及以后（复杂）</strong>：额外圈出文中<strong class=\"hl\">人物</strong>，分析作者对人物的情感倾向",
        "最后结合<strong class=\"hl\">朝代特征</strong>判断作品使用的核心手法",
    ]),
    ("c12", "📌 课堂安排与作业", [
        "调课：<strong class=\"hl\">9月19日停课</strong>；9月26日补19日课时；<strong class=\"hl\">10月6日</strong>补国庆调休占用课时",
        "作业：第一/三套习题有重复，<strong class=\"hl\">本周优先完成 A 卷</strong>，下周推进 B 卷",
        "待办：完成《刘大令四序》山水游记阅读习题，做好批注并订正；《浣花溪记》重点实词整理到积累本",
    ]),
]

QUIZ = [
    ("中国古代山水游记的萌芽阶段是哪个时期？", ["A. 唐代", "B. 魏晋南北朝", "C. 宋代", "D. 明清"], 1,
     "魏晋南北朝是山水游记的<strong>萌芽阶段</strong>，代表王羲之、谢灵运、陶渊明。"),
    ("魏晋南北朝山水游记的核心情感是", ["A. 忧国忧民", "B. 对自然山水的欣赏与陶醉", "C. 被贬的苦闷", "D. 对功名的追求"], 1,
     "此阶段作品以纯描摹山水为主，核心情感是<strong>对自然山水的欣赏与陶醉</strong>。"),
    ("《永州八记》的作者是", ["A. 柳宗元", "B. 苏轼", "C. 王安石", "D. 袁中道"], 0,
     "唐代<strong>柳宗元</strong>被贬永州后创作《永州八记》，实现情景交融。"),
    ("下列要求全文背诵的篇目是", ["A. 《赤壁赋》", "B. 《游褒禅山记》", "C. 《小石潭记》", "D. 《浣花溪记》"], 2,
     "《永州八记》中的<strong>《小石潭记》</strong>要求全文背诵。"),
    ("唐代山水游记的突出特征是", ["A. 纯描摹山水", "B. 情景交融", "C. 寓理于景", "D. 民生思考"], 1,
     "唐代文人把主观情感融入景物，实现<strong>情景交融</strong>；纯描摹是魏晋、寓理于景是宋代。"),
    ("宋代山水游记转向“寓理于景”，主要受什么影响？", ["A. 佛教兴盛", "B. 宋明理学的思辨风气", "C. 科举改革", "D. 市民文化"], 1,
     "受<strong>宋明理学</strong>思辨风气影响，文人收敛抒情、转向寓理于景。"),
    ("《游褒禅山记》的作者是", ["A. 苏轼", "B. 王安石", "C. 柳宗元", "D. 张岱"], 1,
     "宋代代表作品：苏轼《赤壁赋》、<strong>王安石《游褒禅山记》</strong>。"),
    ("山水游记发展至鼎盛成熟期是在", ["A. 唐代", "B. 宋代", "C. 明清", "D. 魏晋"], 2,
     "<strong>明清</strong>是山水游记的鼎盛成熟期，创作群体多元、解读难度最高。"),
    ("下列人物属于明清时期山水游记作者的是", ["A. 谢灵运", "B. 公安三袁、张岱", "C. 柳宗元", "D. 王安石"], 1,
     "明清文人代表：<strong>公安三袁、张岱</strong>；另有施润章这类关注民生政务的官员。"),
    ("施润章在山水游记创作中的特点是", ["A. 纯描摹山水", "B. 关注民生政务", "C. 专写赤壁", "D. 只写佛教题材"], 1,
     "施润章是<strong>关注民生政务</strong>的官员型作者。"),
    ("关于成都本地出题素材，下列说法正确的是", ["A. 陆游曾在成都崇州长期居住", "B. 杨慎整理蜀地文言文 160 篇", "C. 《入蜀记》作者是范成大", "D. 《华阳国志》与山水游记无关"], 0,
     "<strong>陆游曾在成都崇州长期居住</strong>（东站高铁 15 分钟可达故居）；杨慎整理 <strong>1600 多篇</strong>；《入蜀记》作者是陆游。"),
    ("《吴船录》的作者是", ["A. 陆游", "B. 杨慎", "C. 范成大", "D. 袁中道"], 2,
     "<strong>范成大</strong>创作《吴船录》；陆游创作《入蜀记》。"),
    ("杨慎整理的蜀地相关文言文约有", ["A. 160 篇", "B. 600 篇", "C. 1600 多篇", "D. 6000 篇"], 2,
     "杨慎整理了<strong>1600 多篇</strong>蜀地相关文言文，是重要出题素材。"),
    ("《浣花溪记》的作者是", ["A. 袁中道", "B. 袁宏道", "C. 张岱", "D. 苏轼"], 0,
     "《浣花溪记》作者是明代文学家<strong>袁中道</strong>，属明清山水游记。"),
    ("“水木清华”属于哪种文言句式？", ["A. 判断句", "B. 宾语前置", "C. 被动句", "D. 省略句"], 1,
     "“水木清华”是<strong>宾语前置</strong>句式，正确翻译为“<strong>流水清澈、树木茂盛</strong>”。"),
    ("关于“并提”和“互文”，下列说法正确的是", ["A. 是古诗文专属修辞手法", "B. 是两种文言句式", "C. 只用于散文", "D. 属于通假字现象"], 0,
     "<strong>并提、互文</strong>是古诗文<strong>专属修辞手法</strong>（不是句式、不是通假）。"),
    ("谁曾为杜甫在浣花溪畔安排居所？", ["A. 李白", "B. 严武", "C. 高适", "D. 王安石"], 1,
     "<strong>严武</strong>曾为杜甫在浣花溪畔安排居所，保障其日常吃穿用度。"),
    ("严武去世后，杜甫离开浣花溪前往哪里？", ["A. 成都崇州", "B. 重庆夔门", "C. 湖北黄州", "D. 湖南长沙"], 1,
     "杜甫失去依托后前往<strong>重庆夔门</strong>，在此创作了千古第一律诗《登高》。"),
    ("被称为“千古第一律诗”的作品是", ["A. 《赤壁赋》", "B. 《登高》", "C. 《小石潭记》", "D. 《华阳国志》"], 1,
     "杜甫在夔门创作的<strong>《登高》</strong>被誉为千古第一律诗。"),
    ("《浣花溪记》全文采用的串联方式是", ["A. 移步换景", "B. 托物言志", "C. 欲扬先抑", "D. 卒章显志"], 0,
     "全文用<strong>移步换景</strong>把万里桥、杜甫草堂、百花潭等景点逐一串联。"),
    ("《浣花溪记》整体氛围与寄寓的情感是", ["A. 悲凉萧瑟，怀才不遇", "B. 清幽悠远，敬佩赞美杜甫", "C. 热烈奔放，歌颂自然", "D. 忧国忧民，愤世嫉俗"], 1,
     "整体氛围<strong>清幽悠远</strong>，寄寓作者对杜甫从容不迫、热爱生活品质的<strong>敬佩与赞美</strong>。"),
    ("情感推断的第一条路径是", ["A. 锁定结尾关键总结句", "B. 只看标题", "C. 猜测作者年龄", "D. 统计字数"], 0,
     "情感推断三路径：① <strong>结尾关键总结句</strong> ② 景物特点反推 ③ 作者生平与写作背景。"),
    ("读到“冷月”这类景物，通常可推断的情感是", ["A. 欢快喜悦", "B. 战乱后的悲痛", "C. 悠闲自得", "D. 豪情万丈"], 1,
     "通过<strong>景物特点反推情感</strong>：写“冷月”通常对应<strong>战乱后的悲痛</strong>情绪。"),
    ("苏轼被贬黄州时期作品的核心情感多包含", ["A. 建功立业的豪情", "B. 被贬的苦闷与怀才不遇的悲愤", "C. 归隐山林的闲适", "D. 对科举的批判"], 1,
     "结合作者生平背景：苏轼被贬黄州时期作品核心情感多为<strong>被贬的苦闷与怀才不遇的悲愤</strong>。"),
    ("阅读魏晋南北朝（较简单）的山水游记，正确的顺序是", ["A. 先判断手法再找情感", "B. 游踪→景物→时间季节变化→结合氛围推导情感", "C. 只看结尾一句", "D. 先分析人物关系"], 1,
     "简单文本：先梳理<strong>作者游踪与所写景物</strong>，再看景物的时间、季节变化，最后结合氛围推导情感。"),
    ("阅读唐及以后的复杂山水游记，除上述步骤外还要额外做什么？", ["A. 统计修辞数量", "B. 圈出文中人物，分析作者对人物的情感倾向", "C. 抄写全文", "D. 只看注释"], 1,
     "复杂文本需额外<strong>圈出人物并分析情感倾向</strong>，最后结合<strong>朝代特征</strong>判断核心手法。"),
    ("关于语文课后续安排，正确的是", ["A. 9月19日正常上课", "B. 9月19日停课，9月26日补课时", "C. 10月6日不上课", "D. 本周优先完成 B 卷"], 1,
     "<strong>9月19日停课，9月26日补19日课时，10月6日补国庆调休占用课时</strong>；作业本周优先完成 A 卷。"),
    ("老师布置的山水游记阅读习题是", ["A. 《浣花溪记》", "B. 《刘大令四序》", "C. 《小石潭记》", "D. 《赤壁赋》"], 1,
     "待办：完成<strong>《刘大令四序》</strong>山水游记阅读习题，做好文本批注并订正错误。"),
    ("半期考试之后，山水游记类阅读题的难度变化是", ["A. 明显降低", "B. 明显提升", "C. 保持不变", "D. 只考背诵"], 1,
     "半期考试后山水游记阅读题<strong>难度会明显提升</strong>，需提前适应更高强度的文本解读。"),
]

FLASH = [
    ("山水游记四个发展阶段及特征？",
     "① <strong>魏晋南北朝（萌芽）</strong>：纯描摹山水，欣赏陶醉；② <strong>唐代</strong>：情景交融（柳宗元《永州八记》）；③ <strong>宋代</strong>：寓理于景（苏轼《赤壁赋》、王安石《游褒禅山记》）；④ <strong>明清</strong>：鼎盛成熟（公安三袁、张岱、施润章）。"),
    ("魏晋南北朝的三个代表人物？",
     "<strong>王羲之、谢灵运、陶渊明</strong>；内容以纯描摹山水为主，情感是对自然山水的欣赏与陶醉。"),
    ("《永州八记》与《小石潭记》的关系？",
     "《小石潭记》是柳宗元<strong>《永州八记》</strong>中的一篇，<strong>要求全文背诵</strong>。"),
    ("宋代山水游记为什么“寓理于景”？",
     "受<strong>宋明理学</strong>思辨风气影响，文人收敛泛滥抒情，转向寓理于景，探讨天地万物运行规律与为人处世的道理。"),
    ("成都本地有哪些山水游记出题素材？",
     "陆游（居崇州，《入蜀记》）、<strong>范成大《吴船录》</strong>、杨慎整理的 1600 多篇蜀地文言文、《华阳国志》篇目。"),
    ("《浣花溪记》作者、朝代与难度定位？",
     "明代文学家<strong>袁中道</strong>的作品，属明清山水游记；篇幅较长，<strong>八上后半段</strong>就会在考试中遇到同篇幅难度。"),
    ("“水木清华”的句式与正确翻译？",
     "属于<strong>宾语前置</strong>句式；正确翻译为“<strong>流水清澈、树木茂盛</strong>”。"),
    ("并提、互文是什么？",
     "古诗文<strong>专属修辞手法</strong>（不是句式）；《浣花溪记》中重点讲解的两类文言知识点。"),
    ("杜甫与浣花溪、严武的关系？",
     "<strong>严武</strong>为杜甫在<strong>浣花溪畔</strong>安排居所；严武去世后杜甫失去依托，离开浣花溪前往<strong>重庆夔门</strong>，创作千古第一律诗<strong>《登高》</strong>。"),
    ("《浣花溪记》的写作手法与情感？",
     "<strong>移步换景</strong>（万里桥→杜甫草堂→百花潭）；氛围清幽悠远，寄寓对杜甫从容不迫、热爱生活品质的<strong>敬佩与赞美</strong>。"),
    ("情感推断的三条路径？",
     "① 锁定<strong>结尾关键总结句</strong>；② 通过<strong>景物特点反推</strong>（冷月→战乱悲痛）；③ 结合<strong>作者生平与写作背景</strong>（苏轼贬黄州→苦闷与怀才不遇）。"),
    ("不同难度山水游记的解题步骤？",
     "<strong>简单（魏晋）</strong>：游踪→景物→时间季节→氛围→情感；<strong>复杂（唐及以后）</strong>：再加圈人物、分析情感倾向，结合朝代特征判断手法。"),
]

ERRORS = [
    ("❌ 把阶段特征张冠李戴",
     "认为唐代“寓理于景”、宋代“纯描摹山水”。",
     "记忆链条：<strong>魏晋纯描摹 → 唐代情景交融 → 宋代寓理于景 → 明清鼎盛多元</strong>。"),
    ("❌ 作品与作者对应错误",
     "把《永州八记》记成苏轼、《游褒禅山记》记成柳宗元。",
     "柳宗元→<strong>《永州八记》/《小石潭记》</strong>；苏轼→《赤壁赋》；王安石→<strong>《游褒禅山记》</strong>；袁中道→《浣花溪记》。"),
    ("❌ “水木清华”翻译成“水清木华”",
     "只做字面直译，未按宾语前置还原语序。",
     "“水木清华”是<strong>宾语前置</strong>，正确翻译为“<strong>流水清澈、树木茂盛</strong>”。"),
    ("❌ 把并提、互文当作句式",
     "认为“并提”“互文”与宾语前置一样是文言句式。",
     "并提、互文是<strong>修辞手法</strong>；宾语前置才是<strong>句式</strong>，两类要分开记。"),
    ("❌ 情感推断只凭感觉",
     "读完就凭印象写“表达了作者的喜爱之情”。",
     "用<strong>三路径</strong>落地：结尾关键句 + 景物特点反推 + 作者生平背景，答题才有依据。"),
    ("❌ 忽略作者背景导致情感误判",
     "读苏轼被贬黄州时期作品，答“豪迈乐观、壮志满怀”。",
     "结合作者经历：被贬黄州时期核心情感多含<strong>被贬的苦闷与怀才不遇的悲愤</strong>。"),
    ("❌ 复杂文本漏掉“人物”这一环",
     "读唐及以后山水游记时只梳理景物，不圈人物。",
     "复杂文本要额外<strong>圈出人物</strong>、分析作者对人物的情感倾向，再结合<strong>朝代特征</strong>判断手法。"),
]

h = open(BASE_F, encoding='utf-8').read()
nq, nf, ne, nk = len(QUIZ), len(FLASH), len(ERRORS), len(KNOW)

# 1) 文案
h = h.replace('<title>📰 新闻类文本阅读 · 互动学习</title>', '<title>🏔️ 山水游记专题 · 互动学习</title>', 1)
h = h.replace('<h1><i class="fas fa-newspaper"></i> 新闻类文本阅读 · 互动学习</h1>',
              '<h1><i class="fas fa-mountain"></i> 山水游记专题 · 互动学习</h1>', 1)
h = re.sub(r'<p>2026秋语文课外班 第1课 · \d+ 题 · \d+ 卡牌 \| 新闻阅读</p>',
           f'<p>2026秋语文课外班 第2课 · {nq} 题 · {nf} 卡牌 | 山水游记专题</p>', h, count=1)
h = re.sub(r'<span><i class="fas fa-check-circle"[^>]*></i> \d+道测验题</span>',
           f'<span><i class="fas fa-check-circle" style="color:var(--success)"></i> {nq}道测验题</span>', h, count=1)
h = re.sub(r'<span><i class="fas fa-layer-group"></i> \d+张知识卡</span>',
           f'<span><i class="fas fa-layer-group"></i> {nf}张知识卡</span>', h, count=1)
h = re.sub(r'<span><i class="fas fa-exclamation-triangle" style="color:var(--danger)"></i> \d+大易错点</span>',
           f'<span><i class="fas fa-exclamation-triangle" style="color:var(--danger)"></i> {ne}大易错点</span>', h, count=1)

# 2) 知识图谱
g0 = h.find('<div class="knowledge-grid">'); g1 = h.find('<div class="teacher-talk">', g0)
assert g0 > 0 and g1 > g0
cards = ''
for cls, title, lis in KNOW:
    items = ''.join(f'<li>{x}</li>' for x in lis)
    cards += f'      <div class="knowledge-card {cls}"><h3>{title}</h3><ul>{items}</ul></div>\n'
h = h[:g0] + '<div class="knowledge-grid">\n' + cards + '    </div>\n    </div>\n    ' + h[g1:]

# 3) teacher-talk
t0 = h.find('<div class="teacher-talk">'); t1 = h.find('<div id="tab-quiz"', t0)
tt = '''<div class="teacher-talk">
      <h4><i class="fas fa-microphone-alt"></i> 🎙️ 课堂要点 · 第2课（山水游记专题）</h4>
      <p><strong>本讲核心</strong>：2026秋语文课外班第2课，专题为<strong>中国古代山水游记</strong>。①发展脉络四阶段：<strong>魏晋南北朝（萌芽·纯描摹）→ 唐代（情景交融·柳宗元《永州八记》）→ 宋代（寓理于景·苏轼/王安石）→ 明清（鼎盛成熟·公安三袁、张岱）</strong>；②文本精讲：袁中道<strong>《浣花溪记》</strong>（并提、互文、宾语前置“水木清华”、移步换景）；③解题方法：<strong>情感推断三路径</strong> + 分难度文本阅读步骤。</p>
      <p><strong>本地出题背景</strong>：陆游居崇州（《入蜀记》）、范成大（《吴船录》）、杨慎整理 1600 多篇蜀地文言文、《华阳国志》——素材充足；<strong>半期考试后阅读难度会明显提升</strong>，八下日常训练基本都是《浣花溪记》这样的篇幅。</p>
      <p><strong>作业与安排</strong>：9月19日停课，9月26日补课时，10月6日补国庆调休占用课时；习题集作业本周优先完成 <strong>A 卷</strong>、下周推进 B 卷；完成《刘大令四序》阅读习题并订正；把《浣花溪记》重点实词整理到积累本。</p>
      <p><strong>🎓 老师课堂金句</strong> — “中国古人出去玩儿不能纯玩儿……必须写点儿东西。”｜“听懂是前提，然后要自己亲自实践演练，同时反思自己的问题。”｜“文科学习就像扩大池塘，虽然每次做题可能只会用到一条水，但你至少要有水可舀。”</p>
    </div>
    '''
h = h[:t0] + tt + h[t1:]

# 4) 数组
q0 = h.find('const questions = ['); q1 = h.find('const flashcards = [', q0)
qdata = [{'q': q, 'opts': o, 'ans': a, 'exp': e} for q, o, a, e in QUIZ]
h = h[:q0] + 'const questions = ' + json.dumps(qdata, ensure_ascii=False, indent=1) + ';\n\n\n' + h[q1:]

f0 = h.find('const flashcards = ['); f1 = h.find('errors = [', f0)
fdata = [{'front': x, 'back': y} for x, y in FLASH]
h = h[:f0] + 'const flashcards = ' + json.dumps(fdata, ensure_ascii=False, indent=1) + ';\n\n\n' + h[f1:]

e0 = h.find('errors = ['); e1 = h.find('function toast', e0)
edata = [{'title': t, 'wrong': w, 'right': r} for t, w, r in ERRORS]
h = h[:e0] + 'errors = ' + json.dumps(edata, ensure_ascii=False, indent=1) + ';\n\n\n\n' + h[e1:]

# 5) key 隔离 + 残留文案
h = h.replace('chinese26q_lesson1_state_check', 'chinese26q_lesson2_state_check')
h = h.replace("QUIZ_PROG_KEY='quiz_progress_chinese26q_lesson1'", "QUIZ_PROG_KEY='quiz_progress_chinese26q_lesson2'")
h = h.replace("WRONG_HISTORY_KEY='quiz_chinese26q_lesson1_wrong'", "WRONG_HISTORY_KEY='quiz_chinese26q_lesson2_wrong'")
h = h.replace('第1课 新闻类文本阅读', '第2课 山水游记专题')
h = h.replace('新闻类文本阅读 | 2026秋 · 新闻阅读', '山水游记专题 | 2026秋 · 山水游记')
h = h.replace('英语 · 第1讲', '语文 · 第2课')
h = re.sub(r"subject:'新闻[^']*'", "subject:'语文(2026秋)'", h)
h = re.sub(r"chapter:'第1课[^']*'", "chapter:'第2课 山水游记专题'", h)
h = re.sub(r"tags:'[^']*新闻[^']*'", "tags:'语文,2026秋,第2课,山水游记,浣花溪记,情感推断'", h)
h = re.sub(r'<div class="quiz-stats" id="quizStats">0 / \d+</div>', f'<div class="quiz-stats" id="quizStats">0 / {nq}</div>', h, count=1)
h = re.sub(r'共\d+张知识卡', f'共{nf}张知识卡', h, count=1)
open(OUT_F, 'w', encoding='utf-8').write(h)

js = r"""const fs=require('fs');const html=fs.readFileSync('chinese26q_lesson2_interactive.html','utf8');const re=/<script[^>]*>([\s\S]*?)<\/script>/g;let m,ok=true;while((m=re.exec(html))){try{new Function(m[1])}catch(e){ok=false;console.log('ERR',e.message)}}console.log(ok?'JS OK':'JS ERR')"""
r = subprocess.run(['node','-e',js], capture_output=True, text=True, cwd=REPO)
hh = open(OUT_F, encoding='utf-8').read()
print(r.stdout.strip())
print(f'题{nq} 卡{nf} 错{ne} 知识{nk}')
print('div:', len(re.findall(r'<div\b', hh)), '/', hh.count('</div>'))
print('残留 新闻:', hh.count('新闻类文本阅读'), '| lesson1:', hh.count('lesson1'))
