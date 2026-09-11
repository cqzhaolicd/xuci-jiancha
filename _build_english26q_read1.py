#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Clone english_lesson1_interactive.html (clean base) -> english26q_read1_interactive.html
2026秋 八年级第一周 · 21世纪报带读课：AI 陪伴机器人新规
替换：title/navbar/hero/hero-sub/meta/section-header/knowledge-grid/teacher-talk/
      3 数据数组/localStorage keys/importWB 文案/footer/统计数字
"""
import sys

BASE = 'english_lesson1_interactive.html'
FN = 'english26q_read1_interactive.html'
h = open(BASE, encoding='utf-8').read()
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


def seg_replace(start_marker, end_marker, new_seg, tag):
    """Replace [start_marker, end_marker) keeping end_marker."""
    global h
    i = h.find(start_marker)
    if i < 0:
        report.append(f'FAIL[{tag}]: start not found')
        return False
    j = h.find(end_marker, i + len(start_marker))
    if j < 0:
        report.append(f'FAIL[{tag}]: end not found')
        return False
    h = h[:i] + new_seg + h[j:]
    report.append(f'OK[{tag}]')
    return True


def arr_replace(decl, new_content, tag):
    """Replace from decl (incl.) to that array's own first closing ]; (incl.)."""
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


# ============ 1. title / navbar / footer ============
rep('<title>🌍 Holidays & Summer Vacation · 互动学习</title>',
    '<title>🤖 AI 陪伴机器人新规 · 英语阅读互动学习</title>', 'title')
rep('</i> 英语 · 第1讲</a>', '</i> 英语阅读 · 第1周</a>', 'navbar-brand')
rep('<i class="fas fa-heart" style="color:var(--danger)"></i> 英语 · 第1讲 Holidays &amp; Summer Vacation | 双语英语 · 2026秋</div>',
    '<i class="fas fa-heart" style="color:var(--danger)"></i> 英语阅读 · 第1周 AI 陪伴机器人新规 | 21世纪报带读课 · 2026秋</div>', 'footer')

# ============ 2. hero ============
rep('<i class="fas fa-globe-asia"></i> Holidays &amp; Summer Vacation · 互动学习',
    '<i class="fas fa-newspaper"></i> AI 陪伴机器人新规 · 英语阅读互动学习', 'hero-h1')
rep('<p>2026秋双语八年级 B班 · 第1讲 · 32 题 · 15 卡牌 | 双语英语</p>',
    '<p>2026秋 八年级第一周 · 21世纪报带读课 · 28 题 · 12 卡牌 | 英语阅读</p>', 'hero-sub')
rep('<i class="fas fa-check-circle" style="color:var(--success)"></i> 32道测验题',
    '<i class="fas fa-check-circle" style="color:var(--success)"></i> 28道测验题', 'meta-quiz')
rep('<i class="fas fa-layer-group"></i> 15张知识卡</span>',
    '<i class="fas fa-layer-group"></i> 12张知识卡</span>', 'meta-flash')
rep('<i class="fas fa-exclamation-triangle" style="color:var(--danger)"></i> 8大易错点</span>',
    '<i class="fas fa-exclamation-triangle" style="color:var(--danger)"></i> 6大易错点</span>', 'meta-err')

# ============ 3. section header ============
rep('第一讲 · Holidays &amp; Summer Vacation</div>',
    '八年级第一周 · 21世纪报带读课：AI 陪伴机器人新规</div>', 'section-header')

# ============ 4. knowledge grid ============
KG = '''<div class="knowledge-grid">
      <div class="knowledge-card c1"><h3><i class="fas fa-book-open" style="color:#34495e"></i> 📖 文章脉络 Protecting users</h3><ul>
        <li>① 提问引入：你会不会把 AI 当<strong class="hl">真朋友</strong>并过度依赖？</li>
        <li>② 摆现象：AI 陪伴机器人已是日常，有人因此<strong class="hl">疏远真人朋友</strong></li>
        <li>③④⑤ 新规三条：<strong class="hl">限时提醒 + 必须安全友善 + 青少年模式</strong></li>
      </ul></div>
      <div class="knowledge-card c2"><h3><i class="fas fa-clock" style="color:#e67e22"></i> ⏰ 新规一：限时与提醒</h3><ul>
        <li>AI 不得鼓励用户长时间使用</li>
        <li>连续使用 <strong class="hl">2 小时</strong>必须弹窗提醒 <strong class="hl">take a break</strong></li>
        <li>要讲清区别：<strong class="hl">This is a machine, not a real person.</strong></li>
      </ul></div>
      <div class="knowledge-card c3"><h3><i class="fas fa-shield-alt" style="color:#27ae60"></i> 🛡️ 新规二：三条禁止</h3><ul>
        <li>不许 <strong class="hl">tell lies</strong>（撒谎，含善意谎言）</li>
        <li>不许 <strong class="hl">share private information</strong></li>
        <li>不许做 <strong class="hl">harm national security</strong>（危害国家安全）的事</li>
      </ul></div>
      <div class="knowledge-card c4"><h3><i class="fas fa-child" style="color:#8e44ad"></i> 👦 新规三：青少年模式</h3><ul>
        <li>未满 18 岁打开 AI App → <strong class="hl">teen mode 自动开启</strong></li>
        <li>家长可查看 <strong class="hl">how long you chat</strong>（聊天时长）</li>
        <li>AI 不得为讨好用户而给出<strong class="hl">不安全建议</strong></li>
      </ul></div>
      <div class="knowledge-card c5"><h3><i class="fas fa-font" style="color:#2980b9"></i> 📚 6 个必背词组</h3><ul>
        <li><strong class="hl">depend on</strong> 依赖 ｜ <strong class="hl">introduce</strong> 颁布/引入</li>
        <li><strong class="hl">pull away from</strong> 疏远 ｜ <strong class="hl">tell lies</strong> 撒谎</li>
        <li><strong class="hl">either...or...</strong> 要么…要么 ｜ <strong class="hl">remind sb. to do sth.</strong> 提醒某人做</li>
      </ul></div>
      <div class="knowledge-card c6"><h3><i class="fas fa-balance-scale" style="color:#16a085"></i> ⚖️ either...or... 用法</h3><ul>
        <li>结构：<strong class="hl">either + A + or + B</strong>（二选一）</li>
        <li>连接<strong class="hl">同类成分</strong>：名词/动词/句子</li>
        <li>例：These bots, <strong class="hl">either in the form of a toy or an app</strong>…（作插入语）</li>
      </ul></div>
      <div class="knowledge-card c7"><h3><i class="fas fa-bullhorn" style="color:#e74c3c"></i> 🔔 remind 的两种搭配</h3><ul>
        <li><strong class="hl">remind sb. to do sth.</strong> 提醒某人做某事（要有 to）</li>
        <li><strong class="hl">remind sb. of sth.</strong> 使某人想起某事</li>
        <li>例：pop-up messages <strong class="hl">reminding people to take a break</strong></li>
      </ul></div>
      <div class="knowledge-card c8"><h3><i class="fas fa-pen-fancy" style="color:#f39c12"></i> ✍️ 写作任务 Survey Report</h3><ul>
        <li>调查 <strong class="hl">≥10 位同学</strong>：AI 是工具还是朋友？</li>
        <li>写 <strong class="hl">150–200 词</strong>：给数据 + 表态 + <strong class="hl">必须给理由</strong></li>
        <li>句式：According to the survey, … / while 对比 / First… Second…</li>
      </ul></div>
    </div>
    '''
seg_replace('<div class="knowledge-grid">', '<div class="teacher-talk">', KG, 'knowledge-grid')

# ============ 5. teacher-talk ============
TT = '''<div class="teacher-talk">
      <h4><i class="fas fa-microphone-alt"></i> 🎙️ 带读要点 · 八年级第一周（21世纪报：AI 陪伴机器人新规）</h4>
      <p><strong>本篇讲什么</strong>：China makes new rules for AI companion bots（中国为 AI 陪伴机器人出台新规）。文章结构是典型说明文：<strong>抛问题（青少年依赖 AI）→ 政府出新规 → 三条具体规定 → 举例说明</strong>。读懂结构，主旨题就先拿一半分。</p>
      <p><strong>三条新规要能背</strong>：① 不得鼓励长时间使用，<strong>连续 2 小时必须弹窗提醒休息</strong>（take a break），并明确"这是机器不是真人"；② 不得撒谎、泄露隐私、危害国家安全；以前 AI 会用你的情绪推广告，<strong>现在被规则叫停</strong>；③ 未满 18 岁 <strong>青少年模式自动开启</strong>，家长可查看聊天时长。</p>
      <p><strong>词汇与语法</strong>：6 个必背词组 depend on / introduce / pull away from / either...or... / tell lies / remind sb. to do sth.；语法点：<strong>现在分词作后置定语</strong>（pop-up messages reminding people to take a break = that remind people…）、<strong>either...or 插入语</strong>。</p>
      <p><strong>易错提醒</strong>：① 主旨题别选"细节选项"（C 只是第 2 段的现象）；② 细节题考<strong>同义替换</strong>——原文 take a break ↔ 选项 take a rest；③ 判断题注意 <strong>Now, the rules stop this</strong> 的转折（过去可以，现在禁止）；④ remind 后面<strong>别丢 to</strong>。</p>
      <p><strong>🎓 本周任务</strong> — 读 3 遍文章（重点第 3、5 段），6 个词组各造 1 个自己的句子；把 `remind sb. to do sth.` 和 `either...or...` 用进自己的句子里；完成 150–200 词 survey report，检查三件事：有数据、有理由、remind 后没丢 to。</p>
    </div>
    </div>
    '''
seg_replace('<div class="teacher-talk">', '<div id="tab-quiz" class="tab-content">', TT, 'teacher-talk')

# ============ 6. questions ============
Q = '''const questions = [
  {"q":"理清文章结构后判断：本文最好的主旨是","opts":["A. AI companion bots are very smart and friendly.","B. China introduced new rules for AI companion bots.","C. Many young people make friends with AI bots instead of real friends.","D. Teenagers are not allowed to use AI companion bots in China."],"ans":1,"exp":"全文都在讲政府出台新规及具体条款，选 <strong>B</strong>。C 只是第 2 段的一个现象细节，D 与原文矛盾（未满18岁是开启青少年模式，不是禁止使用）。"},
  {"q":"What problem do some young people have while using AI companion bots?（用原文回答）","opts":["A. They spend a lot of time with AI bots and pull away from their real-life friends.","B. They spend too much money on AI toys and apps.","C. They become angry and impatient with their parents.","D. They fail their exams because of chatting with AI."],"ans":0,"exp":"定位第 2 段：Some young people spend a lot of time with them and <strong>pull away from real-life friends</strong>。其余三项原文均未提及。"},
  {"q":"According to the new rules, what must the AI bot do when people have used it for two hours?","opts":["A. Stop working at once.","B. Play a short video.","C. Tell people to take a rest.","D. Turn on its teen mode."],"ans":2,"exp":"原文：show pop-up messages <strong>reminding people to take a break after two hours</strong>。选项用 <strong>take a rest</strong> 同义替换 take a break；D 是另一条规定（未满18岁）张冠李戴。"},
  {"q":"What will happen if under-18 users open AI apps, according to the new rules?","opts":["A. Teen mode will turn on by itself.","B. They have to ask their parents for a password.","C. The app will close in two hours.","D. They can only use the app at weekends."],"ans":0,"exp":"定位第 5 段：If you're under 18 and open an AI app, <strong>teen mode will turn on by itself</strong>（by itself = 自动）。"},
  {"q":"判断正误：AI bots are allowed to tell white lies.","opts":["A. True (T)","B. False (F)","C. Not mentioned in the article","D. The article only talks about adult users"],"ans":1,"exp":"<strong>F</strong>。原文 They can't tell lies——规则没有「善意谎言」的例外，white lies 也是 lies。"},
  {"q":"判断正误：AI bots cannot share users' private information.","opts":["A. True (T)","B. False (F)","C. Only for users under 18","D. Only when parents ask"],"ans":0,"exp":"<strong>T</strong>。原文明确：They can't tell lies, <strong>share private information</strong> or do anything that could harm national security."},
  {"q":"判断正误：It's okay for AI to send people ads based on their feelings.","opts":["A. True (T)","B. False (F)——the new rules stop this now","C. True, but only for toys","D. The article doesn't say"],"ans":1,"exp":"<strong>F</strong>。原文：In the past, AI might use information about your feelings to show you ads… <strong>Now, the rules stop this.</strong> 抓住 Now 这个词，是「过去可以、现在禁止」的转折。"},
  {"q":"If people start to see AI as a real friend, what should the system make clear?","opts":["A. That users should pay more money.","B. That the AI has its own feelings.","C. That this is a machine, not a real person.","D. That the AI will report to their parents."],"ans":2,"exp":"定位第 3 段末：the system should also make the difference clear: <strong>This is a machine, not a real person</strong>（专家刘晓春语）。"},
  {"q":"What can parents do under the new rules?","opts":["A. Check how long their children chat with AI.","B. Read all the messages their children send.","C. Turn off the AI app on their children's phones.","D. Choose which AI bots their children may use."],"ans":0,"exp":"原文：Your parents can <strong>check how long you chat</strong>（查看聊天时长），并未授权读消息、关应用或挑选模型。"},
  {"q":"The writing task at the end asks you to ______.","opts":["A. design an AI companion bot of your own","B. ask more than 10 classmates and write a 150–200 word report","C. write a letter to the government about the new rules","D. interview AI experts in your city"],"ans":1,"exp":"题目原文：ask <strong>more than 10 classmates</strong> about their experiences… write a short report (<strong>about 150–200 words</strong>)。数字是硬考点，别写错。"},
  {"q":"词汇：depend on 的意思是","opts":["A. 依赖；依靠","B. 讨厌；厌倦","C. 假装；假扮","D. 依靠……生活（只用于人）"],"ans":0,"exp":"depend on = <strong>依赖；依靠</strong>。原句：…see it as a real friend and <strong>depend on</strong> it too much? A 项表述完整，D 项加限定错误（物也可作主语，如 It depends on the weather）。"},
  {"q":"词汇：The government has introduced new rules for AI companion bots. 句中 introduce 的含义是","opts":["A. 介绍（某个人）","B. 颁布；引入","C. 翻译","D. 取消"],"ans":1,"exp":"introduce sth 在此表<strong>颁布、推出</strong>（新规）；也可表「介绍、引进」。原句：The government has <strong>introduced</strong> new rules for AI companion bots."},
  {"q":"词汇：pull away from real-life friends 的意思是","opts":["A. 把朋友拉过来","B. 疏远；远离真人朋友","C. 和朋友一起参加活动","D. 把朋友介绍给别人"],"ans":1,"exp":"pull away from = <strong>疏远；远离</strong>。例句：If you spend all day on your phone, you may pull away from your family. 注意介词 <strong>from</strong> 不能丢。"},
  {"q":"词汇：either in the form of a toy or an app 中 either...or... 的含义是","opts":["A. 要么……要么……（二选一）","B. 既……又……（两者都）","C. 不仅……而且……","D. 既不……也不……"],"ans":0,"exp":"either + A + or + B = <strong>要么 A 要么 B</strong>（二选一）。B 项 both...and、C 项 not only...but also、D 项 neither...nor 均不符。"},
  {"q":"词汇：tell lies 与下列哪个表达意思最接近？","opts":["A. tell the truth","B. tell stories to children","C. say something that is not true","D. tell a joke"],"ans":2,"exp":"tell lies = <strong>撒谎</strong>，即 say something that is not true；其反义表达是 <strong>tell the truth</strong>（说实话）。"},
  {"q":"结构：下列句子中 remind 用法正确的是","opts":["A. My watch reminds me take a break every hour.","B. My watch reminds me to take a break every hour.","C. My watch reminds me taking a break every hour.","D. My watch reminds to take a break every hour."],"ans":1,"exp":"<strong>remind sb. to do sth.</strong>：先出人（me），再出 <strong>to do</strong>（to take）。A 丢 to、C 用动名词、D 丢宾语，都错。"},
  {"q":"选词填空：Don't ______ AI too much. It is not always right.","opts":["A. depend on","B. pull away from","C. tell lies","D. introduce"],"ans":0,"exp":"“不要太<strong>依赖</strong> AI，它并不总是对的” → depend on。"},
  {"q":"选词填空：The government ______ new rules for AI companion bots last year.","opts":["A. introduce","B. introduced","C. introducing","D. introduces"],"ans":1,"exp":"时间状语 <strong>last year</strong> 用过去式 <strong>introduced</strong>。"},
  {"q":"选词填空：If you stay online all day long, you may ______ your family and friends.","opts":["A. depend on","B. pull away from","C. remind","D. introduce"],"ans":1,"exp":"整天上网 → 会<strong>疏远</strong>家人朋友 → pull away from。"},
  {"q":"选词填空：It's wrong for teenagers ______. Honesty is the best policy.","opts":["A. tell lies","B. to tell lies","C. telling lies","D. told lies"],"ans":1,"exp":"It is + adj. + for sb. + <strong>to do sth.</strong> 句型 → to tell lies。后半句 Honesty is the best policy（诚实为上）提示填「撒谎」。"},
  {"q":"选词填空：This pop-up message ______ users ______ take a break after two hours.","opts":["A. reminds; to","B. reminds; for","C. remind; to","D. reminding; to"],"ans":0,"exp":"主语 This pop-up message 是单数 → <strong>reminds</strong>；搭配 <strong>remind sb. to do sth.</strong> → reminds users <strong>to</strong> take a break。"},
  {"q":"同义替换：原文 take a break 与下列哪个表达最接近？","opts":["A. take a rest","B. take a walk","C. take a photo","D. take a seat"],"ans":0,"exp":"<strong>take a break = take a rest</strong>（休息一下）。这正是第 3 题选项的考法——细节题常靠同义替换设置正确答案。"},
  {"q":"Now, the rules stop this. 句中 this 指代的是","opts":["A. AI bots telling lies to users","B. AI using information about your feelings to show you ads","C. young people pulling away from real friends","D. parents checking how long children chat"],"ans":1,"exp":"this 指代前一句：In the past, AI might <strong>use information about your feelings to show you ads</strong> for toys or candy——新规把这种行为叫停了。"},
  {"q":"把 pop-up messages reminding people to take a break 改写为定语从句，正确的是","opts":["A. pop-up messages that remind people to take a break","B. pop-up messages that reminding people to take a break","C. pop-up messages remind people to take a break","D. pop-up messages which reminds people to take a break"],"ans":0,"exp":"现在分词短语作后置定语 = 定语从句 <strong>that/which remind people…</strong>（先行词 messages 是复数，从句谓语用 <strong>remind</strong>，不加 s）。"},
  {"q":"短语 harm national security 的意思是","opts":["A. 危害国家安全","B. 泄露个人隐私","C. 提供不安全建议","D. 传播不实信息"],"ans":0,"exp":"harm = 危害；national security = 国家安全。文中三条禁止之一：不许做 anything that could <strong>harm national security</strong>。"},
  {"q":"翻译：You can either call me or send me a message.","opts":["A. 你可以给我打电话或者发信息。","B. 你既可以给我打电话，也可以发信息（两者都可）。","C. 你既不能打电话也不能发信息。","D. 你必须先打电话再发信息。"],"ans":0,"exp":"either...or 表<strong>二选一</strong>（或此或彼）；若表「两者都」应用 <strong>both...and</strong>——这是最常见的混淆点。"},
  {"q":"根据新规，AI 陪伴机器人被禁止做下列哪些事？","opts":["A. 撒谎、泄露隐私、危害国家安全","B. 使用中文与用户对话","C. 向用户提问","D. 提醒用户休息"],"ans":0,"exp":"原文：They can't <strong>tell lies, share private information or do anything that could harm national security</strong>。D 项提醒休息恰恰是新规<strong>要求</strong>做的事。"},
  {"q":"文章第 1 段（If you talked to an AI bot a lot…）在全文中的作用是","opts":["A. 提出话题、引出新规（抛问题引入）","B. 总结全文并给出建议","C. 举一个具体的新闻事例","D. 介绍 AI 陪伴机器人的价格"],"ans":0,"exp":"开头用提问（你会不会过度依赖 AI？）+ 政府已出台新规，属于典型的<strong>抛问题引入</strong>写法，看到开头提问就要预判下文讲「解决方案/规定」。"}
];'''
arr_replace('const questions = [', Q, 'questions-array')

# ============ 7. flashcards ============
F = '''const flashcards = [
  {"front":"这篇《Protecting users》的主旨是什么？","back":"中国为 AI 陪伴机器人（AI companion bots）<strong>出台新规</strong>，保护用户、尤其是未成年人。"},
  {"front":"六个必背词组","back":"depend on <strong>依赖</strong>；introduce sth <strong>颁布/引入</strong>；pull away from <strong>疏远</strong>；either...or... <strong>要么…要么</strong>；tell lies <strong>撒谎</strong>；remind sb. to do sth. <strong>提醒某人做某事</strong>。"},
  {"front":"depend on 怎么用？","back":"<strong>依赖；依靠</strong>。例：Many teenagers <strong>depend on</strong> AI to do their homework.（depend on sb./sth.；也可 depend on sb. to do sth.）"},
  {"front":"introduce sth 的两个意思","back":"① <strong>颁布、推出</strong>（新规）：The government has introduced new rules…；② <strong>介绍、引进</strong>：introduce a friend / a new subject。"},
  {"front":"pull away from 的用法与易错点","back":"<strong>疏远、远离</strong>。例：If you spend all day on your phone, you may pull away from your family. ⚠️ 介词 <strong>from</strong> 不能丢。"},
  {"front":"either...or... 的含义与例句","back":"<strong>要么 A 要么 B</strong>（二选一）。例：These bots, either in the form of a toy or an app, have become…；You can either call me or send me a message. ⚠️ 表「两者都」要用 both...and。"},
  {"front":"tell lies 与 honesty","back":"tell lies = <strong>撒谎</strong>（反义 tell the truth）。例：It's wrong for teenagers to tell lies. Honesty is the best policy.（诚实为上）"},
  {"front":"remind 的两种搭配","back":"① <strong>remind sb. to do sth.</strong> 提醒某人做某事（reminds users <strong>to</strong> take a break）② <strong>remind sb. of sth.</strong> 使某人想起（It reminded me of a painting.）"},
  {"front":"新规的三条核心内容","back":"① <strong>限时</strong>：连续 2 小时弹窗提醒休息，并说明「这是机器不是真人」；② <strong>安全友善</strong>：不许撒谎、泄露隐私、危害国家安全，不许用情绪信息推广告；③ <strong>青少年模式</strong>：未满 18 岁自动开启，家长可查看聊天时长。"},
  {"front":"take a break 的同义表达（考点）","back":"<strong>take a rest</strong>。细节题常把原文词组换成同义词作正确选项——见原文 reminding people to take a break after two hours。"},
  {"front":"现在分词作后置定语怎么改定语从句？","back":"pop-up messages <strong>reminding</strong> people to take a break = pop-up messages <strong>that/which remind</strong> people to take a break（先行词复数 → 从句谓语 remind 不加 s）。"},
  {"front":"Survey report（150–200 词）写作框架","back":"① 开头：I asked <strong>12</strong> classmates about their experiences with AI companion bots. ② 数据：According to the survey, <strong>8 out of 12</strong> see AI bots as helpful tools, while <strong>3</strong> see them as real friends. ③ 立场+理由：I agree with the new rules. First… Second… 最后扣回 AI is a good tool, but it is still a machine. ⚠️ 必须给理由。"}
];'''
arr_replace('const flashcards = [', F, 'flashcards-array')

# ============ 8. errors ============
E = '''errors = [
  {"title":"❌ 主旨题选了细节选项","wrong":"第 1 题选 C：Many young people make friends with AI bots instead of real friends.","right":"主旨题要选能<strong>统摄全文</strong>的项 → B（China introduced new rules for AI companion bots.）。C 只是第 2 段举的一个现象，范围太窄。"},
  {"title":"❌ remind 后面丢了 to","wrong":"My watch reminds me take a break every hour.","right":"<strong>remind sb. to do sth.</strong>：先人后 to do → My watch reminds me <strong>to</strong> take a break."},
  {"title":"❌ 以为「善意谎言」可以例外","wrong":"第 5 题选 T：AI bots are allowed to tell white lies.","right":"规则原文 They can't <strong>tell lies</strong>，没有 white lies 的例外 → 判 <strong>F</strong>。"},
  {"title":"❌ 忽略 Now 的转折，把「过去可以」当「现在可以」","wrong":"第 7 题选 T：AI 可以用你的情绪推广告。","right":"原文 In the past, AI might… <strong>Now, the rules stop this.</strong> 看到 <strong>Now / But / However</strong> 要立刻警觉语义转折 → 判 <strong>F</strong>。"},
  {"title":"❌ pull away from 漏掉介词 from","wrong":"写成 pull away real-life friends / pull away of friends。","right":"<strong>pull away from sb./sth.</strong>；同类搭配还有 depend <strong>on</strong>、remind sb. <strong>of</strong> sth.——介词是固定搭配的一部分，必须背准。"},
  {"title":"❌ 写报告只表态不给理由","wrong":"I agree with the new rules. They are very good. （约 15 词，且无数据无理由）","right":"任务要求 <strong>150–200 词</strong>且必须解释 why：先给调查<strong>数据</strong>（N out of 10…），再分点给<strong>理由</strong>（First… Second…），最后收尾表态。"}
];'''
arr_replace('errors = [', E, 'errors-array')

# ============ 9. quiz stats / flash hint ============
rep('<div class="quiz-stats" id="quizStats">0 / 32</div>',
    '<div class="quiz-stats" id="quizStats">0 / 28</div>', 'quizstats-init')
rep('点击卡片翻转查看答案 · 共15张知识卡',
    '点击卡片翻转查看答案 · 共12张知识卡', 'flash-hint')

# ============ 10. localStorage keys ============
rep("const WRONG_HISTORY_KEY='quiz_english_lesson1_wrong';",
    "const WRONG_HISTORY_KEY='quiz_english26q_read1_wrong';", 'wrong-key')
rep("var QUIZ_PROG_KEY='quiz_progress_english_lesson1';",
    "var QUIZ_PROG_KEY='quiz_progress_english26q_read1';", 'quiz-prog-key')

# ============ 11. autoImportWB / importWB 文案 ============
rep("const item={subject:'英语(双语B班)',chapter:'第1讲 Holidays & 暑假话题',content:q.q,correct_answer:q.opts[q.ans],my_answer:q.opts[myAns]||'未作答',error_reason:'概念不清',source:'练习',difficulty:3,tags:'英语,双语B班,第1讲,holiday,nothing but,against,so...that,不定代词,词形变化'}",
    "const item={subject:'英语阅读(21世纪报)',chapter:'八年级第一周 AI陪伴机器人新规',content:q.q,correct_answer:q.opts[q.ans],my_answer:q.opts[myAns]||'未作答',error_reason:'概念不清',source:'练习',difficulty:3,tags:'英语,21世纪报,八年级,AI陪伴机器人,depend on,pull away from,remind,either...or,阅读理解'}",
    'autoImportWB-item')
rep("subject:'英语',chapter:'第1讲 Holidays & 暑假话题',content:w.q.q,correct_answer:w.q.opts[w.q.ans],my_answer:w.q.opts[w.uc]||'未作答',error_reason:'概念不清',source:'练习',difficulty:3,tags:'英语,双语B班,第1讲,holiday,nothing but,against,so that,不定代词,词形变化'",
    "subject:'英语阅读(21世纪报)',chapter:'八年级第一周 AI陪伴机器人新规',content:w.q.q,correct_answer:w.q.opts[w.q.ans],my_answer:w.q.opts[w.uc]||'未作答',error_reason:'概念不清',source:'练习',difficulty:3,tags:'英语,21世纪报,八年级,AI陪伴机器人,depend on,pull away from,remind,either...or,阅读理解'",
    'importWB-tags')

# ============ 12. leftover checks ============
for pat in ['Holidays', '双语', 'nothing but', 'lay down', 'lesson1_', '第1讲', '暑假话题']:
    c = h.count(pat)
    if c:
        report.append(f'WARN leftover[{pat}] = {c}')

open(FN, 'w', encoding='utf-8').write(h)
print(f'base {orig_len} -> new {len(h)} bytes  ({FN})')
print('\n'.join(report))
