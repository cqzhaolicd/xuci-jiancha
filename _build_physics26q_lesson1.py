#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build physics26q_lesson1_interactive.html from chinese26q base (fixed template).
物理秋季第1讲：运动学计算（一） — 课外培训2026秋季·物理"""
FN = 'physics26q_lesson1_interactive.html'
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

# ---------- 文本（navbar/footer 分别唯一替换，避免互相污染） ----------
rep('<title>📰 新闻类文本阅读 · 互动学习</title>',
    '<title>🏃 运动学计算（一） · 互动学习</title>', 'title')
rep('<i class="fas fa-arrow-left" style="font-size:.85rem;opacity:.8"></i> 语文 · 第1讲</a>',
    '<i class="fas fa-arrow-left" style="font-size:.85rem;opacity:.8"></i> 物理 · 第1讲</a>', 'navbar-brand')
rep('<i class="fas fa-newspaper"></i> 新闻类文本阅读 · 互动学习',
    '<i class="fas fa-tachometer-alt"></i> 运动学计算（一） · 互动学习', 'hero-h1')
rep('2026秋语文课外班 第1课 · 14 题 · 10 卡牌 | 新闻阅读',
    '2026秋物理博学班 第1讲 · 16 题 · 12 卡牌 | 博学班物理', 'hero-sub')
rep('<span><i class="fas fa-check-circle" style="color:var(--success)"></i> 14道测验题</span>',
    '<span><i class="fas fa-check-circle" style="color:var(--success)"></i> 16道测验题</span>', 'meta-quiz')
rep('<i class="fas fa-layer-group"></i> 10张知识卡</span>',
    '<i class="fas fa-layer-group"></i> 12张知识卡</span>', 'meta-flash')
rep('<i class="fas fa-exclamation-triangle" style="color:var(--danger)"></i> 6大易错点</span>',
    '<i class="fas fa-exclamation-triangle" style="color:var(--danger)"></i> 7大易错点</span>', 'meta-err')
rep('第一课 · 新闻类文本阅读', '第一讲 · 运动学计算（一）', 'section-header')
rep('点击卡片翻转查看答案 · 共10张知识卡', '点击卡片翻转查看答案 · 共12张知识卡', 'flash-hint')
rep('语文 · 第1课 新闻类文本阅读 | 2026秋 · 新闻阅读',
    '物理 · 第1讲 运动学计算（一） | 博学班 · 2026秋', 'footer')
rep('<div class="quiz-stats" id="quizStats">0 / 14</div>',
    '<div class="quiz-stats" id="quizStats">0 / 16</div>', 'quizstats')

# ---------- 知识图谱 ----------
KG = '''<div class="knowledge-grid">
      <div class="knowledge-card c1"><h3><i class="fas fa-arrows-alt-h" style="color:#34495e"></i> 参照物与相对运动</h3><ul>
        <li>判断运动先选<strong class="hl">参照物</strong>；研究对象相对参照物位置改变则运动</li>
        <li>不能选<strong class="hl">研究对象自己</strong>当参照物（永远“静止”）</li>
        <li>甲看树东移 → 甲向西；乙相对甲向东 → 甲快于乙</li>
      </ul></div>
      <div class="knowledge-card c2"><h3><i class="fas fa-car" style="color:#8e44ad"></i> 相对速度</h3><ul>
        <li>同向：相对速度 = <strong class="hl">原速度之差</strong>（方向取快者）</li>
        <li>反向：相对速度 = <strong class="hl">原速度之和</strong></li>
        <li>例：甲3m/s东、乙5m/s东 → 乙相对甲 2m/s 向东</li>
      </ul></div>
      <div class="knowledge-card c3"><h3><i class="fas fa-divide" style="color:#3498db"></i> 平均速度·一半一半</h3><ul>
        <li>v̄ = <strong class="hl">总路程/总时间</strong>（不是速度的平均值）</li>
        <li>半时间方案：v̄=(v₁+v₂)/2</li>
        <li>半路程方案：v̄=2v₁v₂/(v₁+v₂)</li>
        <li>结论：v₁≠v₂ 时<strong class="hl">半时间平均速度更大、用时更短</strong></li>
      </ul></div>
      <div class="knowledge-card c4"><h3><i class="fas fa-chart-area" style="color:#27ae60"></i> 运动图像</h3><ul>
        <li>s-t 图：斜率 = <strong class="hl">速度</strong>（越陡越快）</li>
        <li>v-t 图：图线与 t 轴围成<strong class="hl">面积 = 路程</strong></li>
        <li>匀速直线：s-t 斜直线；v-t 水平线</li>
      </ul></div>
      <div class="knowledge-card c5"><h3><i class="fas fa-wave-square" style="color:#2980b9"></i> 心电图问题</h3><ul>
        <li>纸带速度 v纸 已知 → 相邻心跳距离 S₀</li>
        <li>一次心跳时间 t = <strong class="hl">S₀/v纸</strong></li>
        <li>心率 = 60/t（次/分钟）；BPM 60-100 正常</li>
      </ul></div>
      <div class="knowledge-card c6"><h3><i class="fas fa-bug" style="color:#f39c12"></i> 蜻蜓点水</h3><ul>
        <li>波纹半径 = v波 × 时间；蜻蜓位移 = v蜻 × 时间</li>
        <li>内切：v蜻=v波；外切：v蜻<v波；后波超前：v蜻>v波</li>
        <li>v蜻/v波 = S蜻/S波 = <strong class="hl">a₂/(R₁-R₂)</strong></li>
      </ul></div>
      <div class="knowledge-card c7"><h3><i class="fas fa-bolt" style="color:#16a085"></i> 追及问题</h3><ul>
        <li>先出发者多走 Δs = v × Δt</li>
        <li>追上时间 = <strong class="hl">Δs/(v追 - v被追)</strong></li>
        <li>追上时离起点 = v追 × t追上</li>
      </ul></div>
      <div class="knowledge-card c8"><h3><i class="fas fa-sync-alt" style="color:#e74c3c"></i> 往返相遇模型</h3><ul>
        <li>两端相向往返：第 n 次相遇合走 <strong class="hl">(2n-1)S</strong></li>
        <li>静水湖两船：再遇共走 3S → S+600=3×800</li>
        <li>速度比 = 各次相遇所走路程比（恒定）</li>
      </ul></div>
    </div>
    '''
seg_replace('<div class="knowledge-grid">', '<div class="teacher-talk">', KG, 'knowledge-grid')

# ---------- 课堂要点 ----------
TT = '''<div class="teacher-talk">
      <h4><i class="fas fa-microphone-alt"></i> 🎙️ 课堂要点 · 第1讲（运动学计算（一））</h4>
      <p><strong>本讲核心</strong>：2026秋物理博学班第1讲，机械运动章的<strong>计算与模型升级</strong>。四大块：①<strong>相对速度</strong>（同向差、反向和）；②<strong>一半一半</strong>平均速度（半时间用 (v₁+v₂)/2，半路程用 2v₁v₂/(v₁+v₂)，v₁≠v₂ 时半时间更快）；③<strong>图像</strong>（v-t 图面积=路程、s-t 图斜率=速度）；④<strong>创新题</strong>（心电图、蜻蜓点水、往返相遇、追及）。</p>
      <p><strong>方法要点</strong>：平均速度永远用<strong>总路程÷总时间</strong>；追及先算先出发者多走的 Δs=vΔt 再除速度差；心电图把“两波距离÷纸速”得一次心跳时间，60÷t=心率；往返相遇记住<strong>第 n 次相遇合走 (2n-1)S</strong>，静水湖两船再遇=3S；速度比看各次相遇两人路程比（恒定）。</p>
      <p><strong>易错提醒</strong>：①平均速度不是速度的平均；②相对速度同向/反向方向搞反；③v-t 图面积当成速度、s-t 图斜率看错；④追及忘了先出发的时间差；⑤往返相遇只算单程；⑥“以研究对象自己为参照物”得出永远静止的假象。</p>
      <p><strong>🎓 老师课堂总结</strong> — 运动学计算的核心就一句：<strong>画图</strong>（行程图/图像），把文字变成线段。相向画合走、同向画差距，追及找 Δs，往返数相遇次数；速度题先统一单位，再代 v=s/t，平均速度用总路程总时间。</p>
    </div>
    </div>
    '''
seg_replace('<div class="teacher-talk">', '<div id="tab-quiz"', TT, 'teacher-talk')

# ---------- 题库 16 题 ----------
Q = '''const questions = [
  {"q":"甲、乙两人分别坐在并列的两列火车中，甲看见乙在向东行驶，路旁的树也向东运动。若以地面为参照物，则","opts":["A. 甲在向东行驶，乙在向东行驶","B. 甲、乙都向西行驶，但乙比甲快","C. 甲、乙都向西行驶，但甲比乙快","D. 甲、乙都向东行驶，但甲比乙快"],"ans":2,"exp":"甲看树向东 → 甲相对地向<strong>西</strong>；乙相对甲向东 → v甲＞v乙。故甲、乙都西行且<strong>甲比乙快</strong>（C）。"},
  {"q":"甲以3m/s向东运动，乙以5m/s向东运动，则乙相对于甲的速度是","opts":["A. 2m/s，向东","B. 2m/s，向西","C. 8m/s，向东","D. 8m/s，向西"],"ans":0,"exp":"同向：相对速度 = 速度之差 = 5-3=<strong>2m/s</strong>，方向取快的乙的方向（<strong>向东</strong>）。"},
  {"q":"甲以3m/s向东运动，丙以3m/s向西运动，则丙相对于甲的速度是","opts":["A. 6m/s，向西","B. 6m/s，向东","C. 0","D. 3m/s，向西"],"ans":0,"exp":"反向：相对速度 = 速度之和 = 3+3=<strong>6m/s</strong>，方向沿丙的运动方向（<strong>向西</strong>）。"},
  {"q":"某物体前一半时间以 v₁ 运动、后一半时间以 v₂ 运动（v₁≠v₂），全程平均速度是","opts":["A. (v₁+v₂)/2","B. 2v₁v₂/(v₁+v₂)","C. v₁v₂/(v₁+v₂)","D. (v₁-v₂)/2"],"ans":0,"exp":"半时间方案：v̄=(v₁t+v₂t)/(2t)=<strong>(v₁+v₂)/2</strong>。"},
  {"q":"某物体前一半路程以 v₁ 运动、后一半路程以 v₂ 运动（v₁≠v₂），全程平均速度是","opts":["A. 2v₁v₂/(v₁+v₂)","B. (v₁+v₂)/2","C. (v₁+v₂)/(v₁v₂)","D. v₁+v₂"],"ans":0,"exp":"半路程方案：v̄=2s/(s/v₁+s/v₂)=<strong>2v₁v₂/(v₁+v₂)</strong>。"},
  {"q":"同一段路程，方案一：前一半时间 v₁、后一半时间 v₂；方案二：前一半路程 v₁、后一半路程 v₂（v₁≠v₂）。两次平均速度与用时比较，正确的是","opts":["A. 方案一平均速度大，用时短","B. 方案二平均速度大，用时长","C. 两者平均速度相等","D. 方案一平均速度小，用时长"],"ans":0,"exp":"(v₁+v₂)/2 − 2v₁v₂/(v₁+v₂) = (v₁−v₂)²/[2(v₁+v₂)] ＞ 0 → 方案一（半时间）平均速度<strong>更大、用时更短</strong>。"},
  {"q":"v-t 图像中，图线与时间轴围成的面积表示","opts":["A. 路程（位移）","B. 速度","C. 时间","D. 加速度"],"ans":0,"exp":"v-t 图：<strong>面积 = 路程</strong>（如匀速 v·t、匀变速三角形 ½vt）。"},
  {"q":"心电图图纸以25mm/s匀速移动，测得两次心跳的波峰距离为20mm，则此人心脏每分钟跳动次数约为","opts":["A. 75次","B. 60次","C. 100次","D. 50次"],"ans":0,"exp":"一次心跳时间 t=20mm÷25mm/s=<strong>0.8s</strong>；心率 = 60÷0.8 = <strong>75 次/min</strong>（属正常范围）。"},
  {"q":"某人心率为60次/min，则他相邻两次心跳的时间间隔是","opts":["A. 1s","B. 0.8s","C. 60s","D. 0.5s"],"ans":0,"exp":"一次心跳时间 = 60s ÷ 60 次 = <strong>1s</strong>。心电图题先由纸速与波距求时间，再 60÷t 得心率。"},
  {"q":"两个相同小球以相同速度分别滚入相同高度的凸形槽与凹形槽（初末速度相同），通过凸形槽时间 t₁、凹形槽时间 t₂，则","opts":["A. t₁＞t₂","B. t₁=t₂","C. t₁＜t₂","D. 无法确定"],"ans":0,"exp":"凸形槽先上坡减速，中途速度始终≤初速 → 平均速度小；凹形槽先下坡加速，平均速度大 → 同样长度<strong>t₁＞t₂</strong>。"},
  {"q":"100m短跑中，小明比小华早1.5s到达终点，小明到终点时小华离终点还有10m。若每次训练平均速度不变，下列预测正确的是","opts":["A. 小明推迟1.5s出发，二人将同时到达终点","B. 小华提前1.5s出发，小华将先到达终点","C. 小明起点后移10m，小华将先到达终点","D. 小华起点前移10m，小华将先到达终点"],"ans":0,"exp":"小明用时 t=13.5s（小华 15s）。A：小明推迟1.5s → 13.5+1.5=15s 与小华同时到 ✓；B 应为同时到；C 小明后移10m需跑110m，110÷(100/13.5)=14.85s＜15s 小明先到；D 小华前移10m跑90m用13.5s与小明同时到。"},
  {"q":"甲车3min内行驶1.08km，乙车0.4h内行驶7.2km（两车同向匀速），甲车的速度是","opts":["A. 6m/s","B. 5m/s","C. 18m/s","D. 3.6m/s"],"ans":0,"exp":"v甲 = 1080m ÷ 180s = <strong>6m/s</strong>；v乙 = 7200m ÷ 1440s = 5m/s。"},
  {"q":"甲车（6m/s）与乙车（5m/s）同向行驶，乙车经过途中某路标比甲车早5min，则甲车追上乙车所需时间是","opts":["A. 1500s","B. 150s","C. 300s","D. 900s"],"ans":0,"exp":"甲到路标时乙已前行 Δs=5m/s×300s=<strong>1500m</strong>；追上时间 = 1500÷(6−5)=<strong>1500s</strong>（追上点离路标 9000m）。"},
  {"q":"静水湖两岸有两只船同时相向垂直驶向对岸，第一次在离北岸800m处相遇；靠岸返航后又在离南岸600m处相遇（不计靠岸时间），湖面南北宽度是","opts":["A. 1800m","B. 1000m","C. 1200m","D. 1600m"],"ans":0,"exp":"第二次相遇两船共走 3S；北岸出发的船共走 800×3=2400m = S+600 → S=<strong>1800m</strong>。"},
  {"q":"甲、乙分别从 a、b 两点同时出发直线折返跑，第一次相遇距 a 点25m，折返后第二次相遇距 a 点45m（速度大小不变），a、b 两点相距","opts":["A. 60m","B. 70m","C. 50m","D. 80m"],"ans":0,"exp":"速度比 = 25:(S−25) = (2S−45):(S+45) → S=<strong>60m</strong>（第二次相遇甲共走 2S−45、乙走 S+45）。"},
  {"q":"上题中甲、乙的速度之比是","opts":["A. 5:7","B. 7:5","C. 5:9","D. 1:1"],"ans":0,"exp":"第一次相遇同时同地出发：路程比=速度比=25:(60−25)=25:35=<strong>5:7</strong>；第二次相遇用时为第一次的 3 倍。"}
];'''
arr_replace('const questions = [', Q, 'questions')

# ---------- 卡牌 12 张 ----------
F = '''const flashcards = [
  {"front":"怎么判断物体运动还是静止？","back":"先选<strong>参照物</strong>，看研究对象相对参照物的位置是否改变；参照物不同，运动情况可能不同。"},
  {"front":"相对速度怎么算？","back":"同向 = 速度<strong>之差</strong>（方向取快者）；反向 = 速度<strong>之和</strong>。例：甲3东乙5东 → 乙相对甲 2m/s 向东。"},
  {"front":"平均速度公式？","back":"v̄ = <strong>总路程 ÷ 总时间</strong>。绝不是 (v₁+v₂)/2 的简单平均（只有半时间方案才恰为 (v₁+v₂)/2）。"},
  {"front":"“一半一半”两方案？","back":"半时间：v̄=(v₁+v₂)/2；半路程：v̄=2v₁v₂/(v₁+v₂)。v₁≠v₂ 时<strong>半时间更快</strong>。"},
  {"front":"v-t 图与 s-t 图怎么看？","back":"s-t 图：<strong>斜率=速度</strong>（越陡越快）；v-t 图：<strong>面积=路程</strong>。匀速直线：s-t 斜线、v-t 水平线。"},
  {"front":"追及问题三步？","back":"①算先出发者领先距离 Δs=v×Δt；②追上时间 = Δs÷(v追−v被追)；③追上时离起点 = v追×t。"},
  {"front":"心电图题怎么算心率？","back":"①找纸带速度 v纸；②量相邻两波峰距离 S₀；③一次心跳 t=S₀/v纸；④心率=60÷t（次/min）；BPM 60-100 正常。"},
  {"front":"蜻蜓点水判断方向与速度比？","back":"后一次波纹：内切 v蜻=v波；外切 v蜻<v波；后波超出前波 v蜻>v波。v蜻/v波 = 蜻蜓位移/波纹半径差。"},
  {"front":"两端往返相遇的规律？","back":"第 n 次相遇两船/人共走 <strong>(2n−1)S</strong>：第一次合走 S，第二次合走 3S，第三次 5S…"},
  {"front":"静水湖两船经典题？","back":"北岸船第一次走 800m；第二次再遇共走 3S，北岸船共走 2400m=S+600 → S=1800m。"},
  {"front":"凸形槽与凹形槽时间比较？","back":"凸形先减速后加速（中途慢）→ 平均速度小、<strong>t₁ 大</strong>；凹形先加速后减速 → t₂ 小。初末速度相同时结论仍成立。"},
  {"front":"参照物选择禁忌？","back":"不能选<strong>研究对象自己</strong>做参照物（会永远“静止”）；判断谁动先想清楚以什么为参照。"}
];'''
arr_replace('const flashcards = [', F, 'flashcards')

# ---------- 易错 7 条 ----------
E = '''errors = [
  {"title":"❌ 平均速度当成速度平均值","wrong":"全程 v₁=2m/s、v₂=4m/s 直接写平均速度 3m/s。","right":"必须用<strong>总路程÷总时间</strong>；若各占一半路程，v̄=2v₁v₂/(v₁+v₂)，不是 3m/s。"},
  {"title":"❌ 相对速度方向搞反","wrong":"甲3东乙5东，写“乙相对甲向西2m/s”。","right":"同向相减后方向取<strong>快者方向</strong>：乙快 → 向东；反向则相加。"},
  {"title":"❌ v-t 图面积与 s-t 图斜率混淆","wrong":"看到 v-t 图线就说“速度=斜率”，或把 s-t 图两点高度差当路程。","right":"s-t 图看<strong>斜率</strong>（速度），v-t 图看<strong>面积</strong>（路程），两条轴先看清楚。"},
  {"title":"❌ 追及漏算先出发时间","wrong":"乙早 5min 过路标，直接 1500÷(6−5) 却忘了乙已领先 5m/s×300s=1500m。","right":"追上时间=Δs÷速度差，Δs 必须包含<strong>先出发者提前走的距离</strong>。"},
  {"title":"❌ 往返相遇只算单程","wrong":"静水湖两船再遇时只让两船各走一个河宽。","right":"第二次相遇两船<strong>共走 3S</strong>：北岸船走 3×800 = S+600 → S=1800m。"},
  {"title":"❌ 心电图把距离当时间","wrong":"看到两次心跳 20mm 直接说一次心跳 20s。","right":"20mm 是<strong>距离</strong>，需除以纸带速度 25mm/s 得时间 0.8s，再 60÷0.8=75 次。"},
  {"title":"❌ 以研究对象自身为参照物","wrong":"问“甲车上的人看甲车”说甲车在运动。","right":"参照物不能选研究对象自己；判断乙相对甲，就以甲为参照、看乙。"}
];'''
arr_replace('errors = [', E, 'errors')

# ---------- localStorage keys ----------
rep("const WRONG_HISTORY_KEY='quiz_chinese26q_lesson1_wrong';",
    "const WRONG_HISTORY_KEY='quiz_physics26q_lesson1_wrong';", 'wrong-key')
rep("var QUIZ_PROG_KEY='quiz_progress_chinese26q_lesson1';",
    "var QUIZ_PROG_KEY='quiz_progress_physics26q_lesson1';", 'prog-key')
if h.count('chinese26q_lesson1_state_check') == 5:
    h = h.replace('chinese26q_lesson1_state_check', 'physics26q_lesson1_state_check')
    report.append('OK[state-key x5]')
else:
    report.append(f'FAIL[state-key]: {h.count("chinese26q_lesson1_state_check")}')

# ---------- import 文案 ----------
rep("subject:'语文(课外班)',chapter:'第1课 新闻类文本阅读',content:q.q,correct_answer:q.opts[q.ans],my_answer:q.opts[myAns]||'未作答',error_reason:'概念不清',source:'练习',difficulty:3,tags:'语文,2026秋,第1课,新闻阅读,一句话新闻,采访提纲,对联'",
    "subject:'物理(博学班)',chapter:'第1讲 运动学计算（一）',content:q.q,correct_answer:q.opts[q.ans],my_answer:q.opts[myAns]||'未作答',error_reason:'概念不清',source:'练习',difficulty:3,tags:'物理,博学班,2026秋,第1讲,相对速度,平均速度,图像,追及,心电图,往返相遇'",
    'autoImport-tags')
rep("subject:'语文',chapter:'第1课 新闻类文本阅读',content:w.q.q,correct_answer:w.q.opts[w.q.ans],my_answer:w.q.opts[w.uc]||'未作答',error_reason:'概念不清',source:'练习',difficulty:3,tags:'语文,2026秋,第1课,新闻阅读'",
    "subject:'物理',chapter:'第1讲 运动学计算（一）',content:w.q.q,correct_answer:w.q.opts[w.q.ans],my_answer:w.q.opts[w.uc]||'未作答',error_reason:'概念不清',source:'练习',difficulty:3,tags:'物理,博学班,2026秋,第1讲'",
    'importWB-tags')

# ---------- 残留检查 ----------
for pat in ['新闻','语文','chinese26q','新 闻']:
    c = h.count(pat)
    if c:
        report.append(f'WARN leftover[{pat}] = {c}')

open(FN, 'w', encoding='utf-8').write(h)
print('new len', len(h))
print('\\n'.join(report))
