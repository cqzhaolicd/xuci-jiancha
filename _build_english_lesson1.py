#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Clone english_lesson1_interactive.html from physics_lesson15 base.
Replaces: title/nav/hero/section-header/knowledge-grid/teacher-talk/3 data arrays/
keys/text remnants + fixes tab-quiz missing <div + adds autoImportWB/IMPORT_KEY."""
import re, sys

FN = 'english_lesson1_interactive.html'
h = open(FN, encoding='utf-8').read()
orig_len = len(h)
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

def seg_replace(start_marker, end_marker, new_seg, tag, include_start=True, include_end=False):
    """Replace from start_marker (inclusive) to end_marker location."""
    global h
    i = h.find(start_marker)
    if i < 0:
        report.append(f'FAIL[{tag}]: start marker not found')
        return False
    j = h.find(end_marker, i + len(start_marker) if include_start else i)
    if j < 0:
        report.append(f'FAIL[{tag}]: end marker not found')
        return False
    si = i if include_start else i + len(start_marker)
    ej = j if include_end else j
    h = h[:si] + new_seg + h[ej:]
    report.append(f'OK[{tag}]')
    return True

def arr_replace(decl, new_content, tag):
    """Replace whole array from decl (incl.) to its own closing ]; (incl.)."""
    global h
    i = h.find(decl)
    if i < 0:
        report.append(f'FAIL[{tag}]: decl not found')
        return False
    j = h.find('];', i + len(decl))
    if j < 0:
        report.append(f'FAIL[{tag}]: ]; not found')
        return False
    h = h[:i] + new_content + h[j + 2:]
    report.append(f'OK[{tag}]')
    return True

# ============ 1. title ============
rep('<title>📊 密度图象与计算 · 互动学习</title>',
    '<title>🌍 Holidays & Summer Vacation · 互动学习</title>', 'title')

# ============ 2. navbar brand ============
rep('物理 · 密度', '英语 · 第1讲', 'navbar-brand')

# ============ 3. hero h1 ============
rep('<i class="fas fa-chart-line"></i> 密度图象与计算 · 互动学习',
    '<i class="fas fa-globe-asia"></i> Holidays &amp; Summer Vacation · 互动学习', 'hero-h1')

# ============ 4. hero subtitle ============
rep('初二博学班 · 2 模块 · 9 题 · 12 卡牌 | 天元教育',
    '2026秋双语八年级 B班 · 第1讲 · 32 题 · 15 卡牌 | 双语英语', 'hero-sub')

# ============ 5. hero meta ============
rep('<span><i class="fas fa-check-circle" style="color:var(--success)"></i> 9道测验题</span>',
    '<span><i class="fas fa-check-circle" style="color:var(--success)"></i> 32道测验题</span>', 'meta-quiz')
rep('<i class="fas fa-layer-group"></i> 12张知识卡</span>',
    '<i class="fas fa-layer-group"></i> 15张知识卡</span>', 'meta-flash')
rep('<i class="fas fa-exclamation-triangle" style="color:var(--danger)"></i> 6大易错点</span>',
    '<i class="fas fa-exclamation-triangle" style="color:var(--danger)"></i> 8大易错点</span>', 'meta-err')

# ============ 6. section header ============
rep('第十五讲 · 密度图象与计算', '第一讲 · Holidays &amp; Summer Vacation', 'section-header')

# ============ 7. knowledge grid ============
KG = '''<div class="knowledge-grid">
      <div class="knowledge-card c1"><h3><i class="fas fa-book-open" style="color:#34495e"></i> 📖 话题精读 What is a holiday?</h3><ul>
        <li>holiday = 纪念<strong class="hl">特别人物/历史事件</strong>的特殊时刻</li>
        <li>假日上班的人：<strong class="hl">hard-working and great</strong></li>
        <li>庆祝方式：相聚 spending time + <strong class="hl">parade 游行</strong></li>
      </ul></div>
      <div class="knowledge-card c2"><h3><i class="fas fa-puzzle-piece" style="color:#8e44ad"></i> 🧩 nothing but 结构</h3><ul>
        <li>nothing but + <strong class="hl">名词</strong>：只是……</li>
        <li>前谓语含 do → but + <strong class="hl">动词原形</strong>（could do nothing but stay）</li>
        <li>前谓语不含 do → but + <strong class="hl">to do</strong>（had no choice but to wait）</li>
      </ul></div>
      <div class="knowledge-card c3"><h3><i class="fas fa-code-branch" style="color:#3498db"></i> 🔀 against 一词多义</h3><ul>
        <li>① 与……<strong class="hl">竞争</strong>：fight/play against</li>
        <li>② <strong class="hl">反对</strong>（反义词 for）</li>
        <li>③ <strong class="hl">靠着、倚着</strong>（表位置）</li>
        <li>④ <strong class="hl">碰、撞</strong>：hit against the guardrail</li>
      </ul></div>
      <div class="knowledge-card c4"><h3><i class="fas fa-balance-scale" style="color:#27ae60"></i> ⚖️ so/such…that</h3><ul>
        <li>so + <strong class="hl">形/副</strong> + that（结果状语从句）</li>
        <li>such + <strong class="hl">名词短语</strong> + that（such a boring movie）</li>
        <li>转化：so hot that = <strong class="hl">too hot to</strong> = <strong class="hl">not cool enough to</strong></li>
      </ul></div>
      <div class="knowledge-card c5"><h3><i class="fas fa-boxes" style="color:#2980b9"></i> 📦 复合不定代词</h3><ul>
        <li>some 系列：<strong class="hl">肯定句</strong>；any 系列：否定/疑问句</li>
        <li>形容词<strong class="hl">后置</strong>：something beautiful / something unusual</li>
        <li>someone → anyone（疑问句）；don't know anything = know nothing</li>
      </ul></div>
      <div class="knowledge-card c6"><h3><i class="fas fa-sun" style="color:#f39c12"></i> 🌊 完形背景：暑假的意义</h3><ul>
        <li>过去：农场干活 vs 现在：<strong class="hl">课外班/运动/爱好</strong></li>
        <li>观点一：玩太多 → 学业进步 slow</li>
        <li>观点二：activities 帮助成长（Some say ↔ But others say）</li>
      </ul></div>
      <div class="knowledge-card c7"><h3><i class="fas fa-umbrella-beach" style="color:#16a085"></i> 🏖️ 短文填空：词形变化</h3><ul>
        <li>stranger→<strong class="hl">strange</strong>、breathe→<strong class="hl">breath</strong>（take a deep breath）</li>
        <li>comfortably→<strong class="hl">comfortable</strong>、boring→<strong class="hl">bored</strong></li>
        <li>remind→reminded、make→<strong class="hl">made</strong>、no→<strong class="hl">None</strong>（句首大写）</li>
      </ul></div>
      <div class="knowledge-card c8"><h3><i class="fas fa-exchange-alt" style="color:#e74c3c"></i> 💬 句型句式转换</h3><ul>
        <li>say nothing = walk out <strong class="hl">without saying anything</strong></li>
        <li>don't know anything = know nothing</li>
        <li>否定/疑问句：something → <strong class="hl">anything</strong></li>
      </ul></div>
    </div>
    '''
seg_replace('<div class="knowledge-grid">', '<div class="teacher-talk">', KG, 'knowledge-grid')

# ============ 8. teacher-talk ============
TT = '''<div class="teacher-talk">
      <h4><i class="fas fa-microphone-alt"></i> 🎙️ 课堂要点 · 第一讲（Holidays &amp; Summer Vacation）</h4>
      <p><strong>本讲核心</strong>：2026秋双语八年级 B班第1讲，话题 <strong>Holidays（节假日/暑假）</strong>。①精读：holiday 的定义与庆祝方式；②词汇 10 个：event / be derived from / religion / include / theme / of course / parade / kick off / attract / nearly；③语法四大考点：<strong>nothing but 结构、against 一词多义、so/such...that、复合不定代词</strong>。</p>
      <p><strong>练习册重点</strong>：完形（暑假的意义——两种观点对比）+ 短文填空（海边度假，10 空有 7 空考<strong>词形变化</strong>）。做题技巧：完形抓转折对比词（lucky ↔ not so lucky、Some say ↔ But others say）；短文填空先把词库按词性归类，再结合时态/固定搭配变形。</p>
      <p><strong>易错提醒</strong>：① nothing but 后动词形式（含 do → 原形）；② -ed/-ing 形容词 bored / boring；③ anything → something 陈述句转换；④ None 句首大写；⑤ ⚠️ 教材答案两处笔误——人称代词 I 误写成小写 l；"did nothing but lay down" 规范应为 lie down，以老师课堂讲解为准。</p>
      <p><strong>🎓 老师课堂总结</strong> — 新学期起步课：假期话题阅读帮大家热身，10 个词汇短语要当堂消化；nothing but 与 so...that 是中考高频考点，句型转换要能熟练互变；不定代词注意 some/any 家族在肯定、否定、疑问句中的切换。订正练习册时词形变化错一个订正一个，把"词库原词 → 文中正确形式"成对记住。</p>
    </div>
    </div>
    '''
seg_replace('<div class="teacher-talk">', 'id="tab-quiz"', TT, 'teacher-talk', include_start=True, include_end=True)

# ============ 9. fix tab-quiz missing <div ============
rep('</div>id="tab-quiz" class="tab-content">', '</div><div id="tab-quiz" class="tab-content">', 'tab-quiz-div')

# ============ 10. quiz stats initial ============
rep('<div class="quiz-stats" id="quizStats">0 / 32</div>',
    '<div class="quiz-stats" id="quizStats">0 / 32</div>', 'quizstats-init')

# ============ 11. flashcard hint ============
rep('点击卡片翻转查看答案 · 共12张知识卡', '点击卡片翻转查看答案 · 共15张知识卡', 'flash-hint')

# ============ 12. questions array ============
Q = '''const questions = [
  {"q":"Around the world, summer vacation means much free time... Also, there's something ___1___ to students — no school.","opts":["A. boring","B. difficult","C. important"],"ans":2,"exp":"破折号强调“不用上学”(no school) 对学生是<strong>重要的(important)</strong>；boring/difficult 与语境相反。"},
  {"q":"Hundreds of years ago, students ___2___ the summer on the farm. They helped to grow vegetables and feed animals.","opts":["A. cost","B. spent","C. took"],"ans":1,"exp":"“度过(时间)”用 <strong>spend→spent</strong>；cost 主语为物表花钱；take 用于 It takes sb. time to do sth."},
  {"q":"But today, students can do something ___3___ in summer vacation: after-school classes, sports or hobbies.","opts":["A. boring","B. different","C. useless"],"ans":1,"exp":"与过去“在农场干农活”对比，现在上课外班/运动/爱好——做的事情<strong>不同了(different)</strong>。"},
  {"q":"If you're ___4___, in the weeks away from school, you can go on a trip or go camping.","opts":["A. lucky","B. scared","C. tired"],"ans":0,"exp":"与后文 “But if you're not so lucky” 呼应，此空填<strong>幸运的(lucky)</strong>。"},
  {"q":"It's time to ___5___ new things. You can learn to play the guitar or play basketball.","opts":["A. make","B. look","C. try"],"ans":2,"exp":"<strong>try new things</strong>（尝试新事物）是常见搭配；make/look 语意不通。"},
  {"q":"But if you're not so lucky, summer vacation may mean summer ___6___ — a long, hot summer inside the classroom.","opts":["A. clubs","B. schools","C. camps"],"ans":1,"exp":"后文“在教室里度过漫长炎热的夏天”→ <strong>summer schools</strong>（暑假学校/补课）。"},
  {"q":"Some say that summer vacation means ___7___ academic progress(学业进步). They think having too much fun will make students forget their studies.","opts":["A. slow","B. real","C. much"],"ans":0,"exp":"后文是负面观点（玩多→忘记学习、难继续）→ 学业进步<strong>缓慢(slow)</strong>；下一句 But others say 形成转折。"},
  {"q":"They think spending too much time having fun will make students ___8___ their studies. And it's hard for them to go on studying.","opts":["A. think of","B. help with","C. forget about"],"ans":2,"exp":"玩太多自然导致<strong>忘记(forget about)</strong>学习，符合因果逻辑。"},
  {"q":"But others say that the ___9___ in summer vacation can help students to grow up.","opts":["A. gifts","B. activities","C. persons"],"ans":1,"exp":"暑假里做的事可统称为<strong>活动(activities)</strong>，帮助成长；gifts/persons 太片面。"},
  {"q":"Learn something! Help someone! Make this summer a good one for you to ___10___.","opts":["A. see","B. learn","C. remember"],"ans":2,"exp":"结尾祝愿“让这个夏天值得<strong>记住(remember)</strong>”；see/learn 语意不通。"},
  {"q":"短文填空①：Last summer my family went to a small coastal town. Everything there felt ___ to us at first because we had never been there.","opts":["A. strange","B. stranger","C. strangely","D. strangers"],"ans":0,"exp":"felt 是系动词，后接<strong>形容词 strange</strong>（陌生的）；词库 stranger 需还原成形容词。"},
  {"q":"短文填空②：The sea air smelled fresh, and I took a deep ___ to enjoy it.","opts":["A. breathe","B. breath","C. breathing","D. breathes"],"ans":1,"exp":"固定搭配 <strong>take a deep breath</strong>（深呼吸）；动词 breathe 变名词 breath。"},
  {"q":"短文填空③：Our hotel room was small but very ___.","opts":["A. comfortably","B. comfort","C. comfortable","D. comforted"],"ans":2,"exp":"修饰名词 room 用形容词 <strong>comfortable</strong>；comfortably 是副词需变形。"},
  {"q":"短文填空④：My little brother kept asking, “Are you ___ to go to the beach now?” He was so excited.","opts":["A. ready","B. sick","C. bored","D. all"],"ans":0,"exp":"固定搭配 <strong>be ready to do sth.</strong>（准备好做某事），词库原词 ready 直接填。"},
  {"q":"短文填空⑤：After two days of swimming and playing volleyball on the beach, I started to feel ___ with these activities.","opts":["A. boring","B. bored","C. bore","D. bores"],"ans":1,"exp":"-ed 形容词修饰人的感受：<strong>bored</strong>（感到无聊）；boring 修饰事物，此处搭配 feel 用人感受。"},
  {"q":"短文填空⑥：Luckily, I could take a rest and enjoy the beautiful scenery. It ___ me of a painting that I had seen in an art book.","opts":["A. remind","B. reminds","C. reminded","D. reminding"],"ans":2,"exp":"全文过去时 → <strong>reminded</strong>；搭配 remind sb. of sth.（使某人想起）。"},
  {"q":"短文填空⑦：One afternoon, we saw ___ unusual in the water — it was a dolphin!","opts":["A. anything","B. nothing","C. something","D. everything"],"ans":2,"exp":"肯定陈述句表“某件…事”用 <strong>something</strong>（由 anything 转换）；形容词 unusual 后置：something unusual。"},
  {"q":"短文填空⑧：We were all amazed. ___ of us had ever seen a dolphin so close before.","opts":["A. No","B. Not","C. None","D. All"],"ans":2,"exp":"<strong>None of us</strong>（我们中没有人）；⚠️ 句首首字母必须大写 None。no 是形容词不能直接作主语。"},
  {"q":"短文填空⑨：Suddenly, two local boys started to ___ about who saw the dolphin first.","opts":["A. fight","B. fought","C. fighting","D. fights"],"ans":0,"exp":"started to do → 填<strong>原形 fight</strong>；fight about = 为……争吵。"},
  {"q":"短文填空⑩：Their argument (争论) ___ us all laugh. What a wonderful vacation!","opts":["A. make","B. makes","C. made","D. making"],"ans":2,"exp":"全文过去时 → <strong>made</strong>；make sb. do sth.（让某人做某事），宾语补足语用原形 laugh。"},
  {"q":"游客们除了等下一班火车，什么也做不了。正确英译是","opts":["A. The tourists could do nothing but wait for the next train.","B. The tourists could do nothing but waiting for the next train.","C. The tourists could do nothing but waited for the next train.","D. The tourists could do nothing but to wait for the next train."],"ans":0,"exp":"谓语含 do（did nothing）→ <strong>nothing but + 动词原形 wait</strong>；等价写法：had no choice but to wait。"},
  {"q":"我们昨天什么也没有做，只是静静地躺在草地上。规范英译是","opts":["A. We did nothing but lie down on the grass quietly yesterday.","B. We did nothing but lay down on the grass quietly yesterday.","C. We did nothing but lying down on the grass quietly yesterday.","D. We did nothing but lay down quietly on the grass yesterday."],"ans":0,"exp":"nothing but 前有 did → 后接<strong>动词原形 lie</strong> down。⚠️ 教材答案 B 写法 lay down 疑为笔误（lay 是及物“放置”或 lie 的过去式），规范作答写 lie down。"},
  {"q":"Going against the traffic rules is dangerous. 句中 against 的含义是","opts":["A. 违反","B. 靠着","C. 反对","D. 碰；撞"],"ans":0,"exp":"against the traffic rules = <strong>违反</strong>交通规则（against 意为“违背/违反”）。"},
  {"q":"The car skidded and hit against the guardrail(护栏). 句中 against 的含义是","opts":["A. 竞争","B. 反对","C. 靠着","D. 碰；撞"],"ans":3,"exp":"hit against the guardrail = 撞上护栏，against 表<strong>碰、撞</strong>。"},
  {"q":"Many people are against the new tax law(税法). 句中 against 的含义是","opts":["A. 反对","B. 靠着","C. 违反","D. 竞争"],"ans":0,"exp":"be against = <strong>反对</strong>；against 的反义词是 for。"},
  {"q":"这部电影太乏味了，以至于我看到一半就睡着了。用 so...that 翻译正确的是","opts":["A. The movie was so boring that I fell asleep halfway through.","B. The movie was such boring that I fell asleep halfway through.","C. The movie was so boring movie that I fell asleep halfway through.","D. The movie was so boring for me to fall asleep halfway through."],"ans":0,"exp":"so + 形容词 + that 从句：<strong>so boring that I fell asleep</strong>；可转化为 too boring for me to watch halfway。"},
  {"q":"同一句用 such...that 表达，正确的是","opts":["A. It was so a boring movie that I fell asleep halfway through.","B. It was such a boring movie that I fell asleep halfway through.","C. It was a such boring movie that I fell asleep halfway through.","D. It was such boring a movie that I fell asleep halfway through."],"ans":1,"exp":"such + a(n) + 形容词 + 名词 + that：<strong>such a boring movie that…</strong>。"},
  {"q":"—My family went to Taizhou to eat morning tea during the May Day holiday. —So did I. There are ___ many tourists that all the waiters ___ stopped to eat or rest the whole day.","opts":["A. so; mostly","B. such; nearly","C. so; hardly","D. such; highly"],"ans":2,"exp":"so many tourists（so+many+可数复数）+ hardly（几乎不）表否定：服务员们几乎整天没停下吃喝。"},
  {"q":"She is new here, so we don't know anything about her.（同义句）She is new here, so we ___ about her.","opts":["A. know nothing","B. don't know nothing","C. know anything","D. not know something"],"ans":0,"exp":"don't know anything = <strong>know nothing</strong>（单重否定同义改写）。"},
  {"q":"There is something wrong with the bike.（改否定句）","opts":["A. There isn't anything wrong with the bike.","B. There is nothing not wrong with the bike.","C. There isn't something wrong with the bike.","D. There doesn't be anything wrong with the bike."],"ans":0,"exp":"否定句把 something 改为 <strong>anything</strong>：There isn't anything wrong with the bike."},
  {"q":"His mother said nothing and walked out.（同义句）His mother walked out ___ ___.","opts":["A. without saying anything","B. with saying nothing","C. without to say anything","D. without say anything"],"ans":0,"exp":"say nothing = walk out <strong>without saying anything</strong>（介词后接动名词）。"},
  {"q":"She'd like something beautiful for her mother.（改一般疑问句）","opts":["A. Would she like anything beautiful for her mother?","B. Would she like something beautiful for her mother?","C. Does she like anything beautiful for her mother?","D. Would she likes anything beautiful for her mother?"],"ans":0,"exp":"一般疑问句 some → <strong>any</strong>：Would she like anything beautiful...?（would like 句型保留 would）"}
];'''

arr_replace('const questions = [', Q, 'questions-array')

# ============ 13. flashcards array ============
F = '''const flashcards = [
  {"front":"What is a holiday?（话题核心）","back":"It's a special time to <strong>remember special people or events in history</strong>. 假日是纪念特别人物/历史事件的特殊时刻。"},
  {"front":"对假日上班的人，作者怎么看？人们如何庆祝？","back":"They are <strong>hard-working and great</strong>. 庆祝方式：By spending time together and <strong>parading</strong>（相聚+游行）。"},
  {"front":"event 的词性与词义","back":"event <strong>n. 事件</strong>（尤指重要/历史事件）。"},
  {"front":"be derived from 什么意思？","back":"<strong>起源于</strong>（derive v. 来自、源于）。"},
  {"front":"religion / include / theme 词义","back":"religion n. <strong>宗教</strong>；include v. <strong>包含</strong>；theme n. <strong>主题</strong>。"},
  {"front":"parade / kick off / attract / nearly 词义","back":"parade n./v. <strong>游行</strong>；kick off <strong>开始</strong>；attract v. <strong>吸引</strong>；nearly adv. <strong>几乎，差不多</strong>。"},
  {"front":"of course 的用法","back":"of course = <strong>当然</strong>，表示同意/肯定。"},
  {"front":"nothing but 的三种搭配","back":"① nothing but + <strong>名词</strong>：只是……；② 前谓语含 do → but + <strong>动词原形</strong>（could do nothing but stay）；③ 前谓语不含 do → but + <strong>to do</strong>（had no choice but to wait）。"},
  {"front":"against 的一词多义（4 义）","back":"① 与……<strong>竞争</strong>（fight/play against）；② <strong>反对</strong>（反义词 for）；③ <strong>靠着、倚着</strong>；④ <strong>碰、撞</strong>（hit against）。"},
  {"front":"so...that 与 such...that 的区别","back":"so + <strong>形容词/副词</strong> + that；such + <strong>名词短语</strong> + that（such a boring movie）。转化：so hot that I can't touch = too hot for me to touch = not cool enough for me to touch。"},
  {"front":"复合不定代词 some/any 家族怎么用？","back":"肯定句用 <strong>something / someone</strong>；否定/疑问句用 <strong>anything / anyone</strong>；形容词<strong>后置</strong>：something beautiful。"},
  {"front":"breathe 与 breath 的区别","back":"breathe <strong>v. 呼吸</strong>；breath <strong>n. 呼吸</strong>。固定搭配：take a deep breath（深呼吸）。"},
  {"front":"-ed / -ing 形容词：bored vs boring","back":"bored 修饰<strong>人</strong>（感到无聊）：I felt bored；boring 修饰<strong>事物</strong>：The movie is boring。"},
  {"front":"None of us 的用法与易错点","back":"None of us = 我们中没有人；<strong>句首首字母大写</strong>；no 是形容词不能直接作主语。"},
  {"front":"spend / cost / take 辨析","back":"spend：人作主语（度过时间/花钱，spend...on/in doing）；cost：物作主语（花费多少钱）；take：It takes sb. time to do sth."}
];'''

arr_replace('const flashcards = [', F, 'flashcards-array')

# ============ 14. errors array ============
E = '''errors = [
  {"title":"❌ nothing but 后动词用错形式","wrong":"写成 did nothing but waiting / waited / to wait。","right":"谓语含 do（did nothing）→ nothing but + <strong>动词原形 wait</strong>；不含 do 才用 to do：had no choice but to wait。"},
  {"title":"❌ “躺下”写成 lay down","wrong":"教材答案写作 We did nothing but lay down...（lay 是及物“放置”或 lie 的过去式）。","right":"规范应写 <strong>We did nothing but lie down...</strong>（nothing but 后接动词原形 lie）。教材此处疑为笔误，以老师课堂讲解为准。"},
  {"title":"❌ -ed / -ing 形容词混用","wrong":"I felt boring. 用 boring 形容人的感受。","right":"-ed 形容<strong>人</strong>的感受：I felt <strong>bored</strong>；-ing 形容<strong>事物</strong>：The movie is boring。"},
  {"title":"❌ 肯定陈述句该用 something 却用 anything","wrong":"We saw anything unusual in the water.","right":"肯定陈述句表“某件…”用 <strong>something</strong>：We saw something unusual. anything 用于否定/疑问句。"},
  {"title":"❌ None 首字母小写","wrong":"none of us had ever seen... 句首不大写。","right":"句首单词必须大写：<strong>None</strong> of us had ever seen a dolphin. 同时区分 no（形容词）/ none（代词）。"},
  {"title":"❌ so / such 后接成分混淆","wrong":"The movie was such boring that... / It was so a boring movie that...","right":"so + <strong>形容词/副词</strong>（so boring / so many tourists）；such + <strong>名词短语</strong>（such a boring movie）。"},
  {"title":"❌ 人称代词 I 写成小写 l","wrong":"教材答案手打笔误：Because l need time...（小写 l）。","right":"英语人称代词 <strong>I 永远大写</strong>；小写 l 是数字1/字母L，写作时注意。"},
  {"title":"❌ spend / cost / take 三词混用","wrong":"He cost the summer on the farm. / The book took 30 yuan.","right":"人 + spend + 时间/钱（on sth./in doing）；物 + cost + 钱；It takes sb. time to do sth."}
];'''

arr_replace('errors = [', E, 'errors-array')

# ============ 15. IMPORT_KEY + autoImportWB injection before WRONG_HISTORY_KEY ============
AI = """const IMPORT_KEY='wrong_bank_import';
function autoImportWB(idx,myAns){const q=questions[idx];const item={subject:'英语(双语B班)',chapter:'第1讲 Holidays & 暑假话题',content:q.q,correct_answer:q.opts[q.ans],my_answer:q.opts[myAns]||'未作答',error_reason:'概念不清',source:'练习',difficulty:3,tags:'英语,双语B班,第1讲,holiday,nothing but,against,so...that,不定代词,词形变化'};const ex=JSON.parse(localStorage.getItem(IMPORT_KEY)||'[]');if(ex.some(x=>x.content===item.content))return false;ex.push(item);localStorage.setItem(IMPORT_KEY,JSON.stringify(ex));return true;}
"""
rep("const WRONG_HISTORY_KEY='quiz_physics_lesson14_wrong';",
    AI + "const WRONG_HISTORY_KEY='quiz_english_lesson1_wrong';", 'wrong-key+autoImport')

# ============ 16. quiz progress key ============
rep("var QUIZ_PROG_KEY='quiz_progress_physics_lesson15';",
    "var QUIZ_PROG_KEY='quiz_progress_english_lesson1';", 'quiz-prog-key')

# ============ 17. state_check key (5 occurrences) ============
if h.count("phy_lesson7_state_check") == 5:
    h = h.replace("phy_lesson7_state_check", "english_lesson1_state_check")
    report.append('OK[state-check-key x5]')
else:
    report.append(f'FAIL[state-check-key]: got {h.count("phy_lesson7_state_check")}')

# ============ 18. importWB subject/chapter/tags ============
rep("subject:'物理',chapter:'密度',content:w.q.q,correct_answer:w.q.opts[w.q.ans],my_answer:w.q.opts[w.uc]||'未作答',error_reason:'概念不清',source:'练习',difficulty:3,tags:'密度,ρ=m/V,单位换算,气体计算,比例计算,m-V图像,物理'",
    "subject:'英语',chapter:'第1讲 Holidays & 暑假话题',content:w.q.q,correct_answer:w.q.opts[w.q.ans],my_answer:w.q.opts[w.uc]||'未作答',error_reason:'概念不清',source:'练习',difficulty:3,tags:'英语,双语B班,第1讲,holiday,nothing but,against,so that,不定代词,词形变化'",
    'importWB-tags')

# ============ 19. leftover checks ============
for pat in ['物理', '密度', '天元教育', '初二博学班', 'lesson14', 'lesson15', 'lesson7', '第十五讲']:
    c = h.count(pat)
    if c:
        report.append(f'WARN leftover[{pat}] = {c}')

open(FN, 'w', encoding='utf-8').write(h)
print(f'original {orig_len} -> new {len(h)} bytes')
print('\\n'.join(report))
