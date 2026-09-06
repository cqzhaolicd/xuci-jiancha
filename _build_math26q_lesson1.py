#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build math26q_lesson1_interactive.html from english_lesson1 base (fixed template).
Replaces all content: title/nav/hero/knowledge-grid/teacher-talk/3 arrays/keys/footer."""
FN = 'math26q_lesson1_interactive.html'
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
rep('<title>🌍 Holidays & Summer Vacation · 互动学习</title>',
    '<title>🧮 二次根式综合复习 · 互动学习</title>', 'title')
rep('英语 · 第1讲', '数学 · 第1讲', 'navbar-brand', count=2)
rep('<i class="fas fa-globe-asia"></i> Holidays &amp; Summer Vacation · 互动学习',
    '<i class="fas fa-square-root-alt"></i> 二次根式综合复习 · 互动学习', 'hero-h1')
rep('2026秋双语八年级 B班 · 第1讲 · 32 题 · 15 卡牌 | 双语英语',
    '26秋博学班 数学第1讲 · 28 题 · 14 卡牌 | 博学班', 'hero-sub')
rep('<span><i class="fas fa-check-circle" style="color:var(--success)"></i> 32道测验题</span>',
    '<span><i class="fas fa-check-circle" style="color:var(--success)"></i> 28道测验题</span>', 'meta-quiz')
rep('<i class="fas fa-layer-group"></i> 15张知识卡</span>',
    '<i class="fas fa-layer-group"></i> 14张知识卡</span>', 'meta-flash')
rep('<i class="fas fa-exclamation-triangle" style="color:var(--danger)"></i> 8大易错点</span>',
    '<i class="fas fa-exclamation-triangle" style="color:var(--danger)"></i> 8大易错点</span>', 'meta-err')
rep('第一讲 · Holidays &amp; Summer Vacation', '第一讲 · 二次根式综合复习', 'section-header')
rep('点击卡片翻转查看答案 · 共15张知识卡', '点击卡片翻转查看答案 · 共14张知识卡', 'flash-hint')
rep('英语 · 第1讲 Holidays &amp; Summer Vacation | 双语英语 · 2026秋',
    '数学 · 第1讲 二次根式综合复习 | 博学班 · 2026秋', 'footer')
rep('<div class="quiz-stats" id="quizStats">0 / 32</div>',
    '<div class="quiz-stats" id="quizStats">0 / 28</div>', 'quizstats')

# ---------- 知识图谱 ----------
KG = '''<div class="knowledge-grid">
      <div class="knowledge-card c1"><h3><i class="fas fa-cube" style="color:#34495e"></i> 定义与有意义条件</h3><ul>
        <li>√a 叫二次根式，要求 <strong class="hl">a≥0</strong></li>
        <li>被开方数≥0；分母≠0；偶次根式被开方数≥0</li>
        <li>³√8 是三次根式，不属于二次根式</li>
      </ul></div>
      <div class="knowledge-card c2"><h3><i class="fas fa-balance-scale" style="color:#8e44ad"></i> 双重非负性</h3><ul>
        <li>a≥0 且 <strong class="hl">√a ≥ 0</strong></li>
        <li>√(x-2)+√(4-2x)：两项都要有意义 → <strong class="hl">x=2</strong></li>
        <li>被开方数互为相反数 → 都=0（如 x²-4 与 4-x²）</li>
      </ul></div>
      <div class="knowledge-card c3"><h3><i class="fas fa-divide" style="color:#3498db"></i> √(a²)=|a|</h3><ul>
        <li>化简先写<strong class="hl">绝对值</strong>，再按范围去绝对值</li>
        <li>1<x<4：√((x+1)²)-√((x-5)²)=|x+1|-|x-5|=2x-4</li>
        <li>含数轴/隐藏条件题：先定正负</li>
      </ul></div>
      <div class="knowledge-card c4"><h3><i class="fas fa-puzzle-piece" style="color:#27ae60"></i> 双重二次根式配方</h3><ul>
        <li>√(3±2√2)=<strong class="hl">√2±1</strong>；√(5-2√6)=√3-√2</li>
        <li>套路：找 a²+b²±2ab → (√a±√b)²</li>
        <li>√(4±√15) 型先 ×2 或凑 (√10±√6)²/4</li>
      </ul></div>
      <div class="knowledge-card c5"><h3><i class="fas fa-random" style="color:#2980b9"></i> 有理化与裂项</h3><ul>
        <li>分母有理化：1/(√a+√b)=(√a-√b)/(a-b)</li>
        <li>分子有理化：√a-√b=(a-b)/(√a+√b)，用于比大小/最值</li>
        <li>裂项：1/(√n+√(n+1))=<strong class="hl">√(n+1)-√n</strong></li>
      </ul></div>
      <div class="knowledge-card c6"><h3><i class="fas fa-exchange-alt" style="color:#f39c12"></i> 知二求二</h3><ul>
        <li>a²+b²=(a+b)²-2ab</li>
        <li>(a-b)²=(a+b)²-4ab</li>
        <li>√(a/b)+√(b/a) 型：先平方消根号，再定号</li>
      </ul></div>
      <div class="knowledge-card c7"><h3><i class="fas fa-arrow-down" style="color:#16a085"></i> 降次技巧</h3><ul>
        <li>由 a²=2a+1 可迭代：a³=<strong class="hl">5a+2</strong>、a⁴=…</li>
        <li>高次多项式代入：全部换成 a 的一次式</li>
        <li>a=√2+1 型先平方建恒等式再降次</li>
      </ul></div>
      <div class="knowledge-card c8"><h3><i class="fas fa-star" style="color:#e74c3c"></i> 共轭根式互倒</h3><ul>
        <li>x=(√(n+1)-√n)/(√(n+1)+√n)，y 为其倒数</li>
        <li>xy=<strong class="hl">1</strong>，x+y=<strong class="hl">4n+2</strong>（分子分母平方差=1）</li>
        <li>常用于给定 x²+y² 型等式反求 n/m</li>
      </ul></div>
    </div>
    '''
seg_replace('<div class="knowledge-grid">', '<div class="teacher-talk">', KG, 'knowledge-grid')

# ---------- 课堂要点 ----------
TT = '''<div class="teacher-talk">
      <h4><i class="fas fa-microphone-alt"></i> 🎙️ 课堂要点 · 第1讲（二次根式综合复习）</h4>
      <p><strong>本讲核心</strong>：2026秋博学班数学第1讲，把暑期二次根式知识做<strong>综合复习</strong>，按三模块推进：①<strong>定义复习</strong>（有意义的条件、双重非负性求参）②<strong>化简与计算</strong>（结合数轴去绝对值、双重二次根式配方、有理化与裂项求和）③<strong>知二求二与降次</strong>（a+b/ab 与 a²+b² 互化、共轭根式互倒、高次代入降次）。</p>
      <p><strong>方法要点</strong>：见到 √(a²) 先写 |a| 再结合范围去绝对值；被开方数互为相反数 → 两式都为 0 是求参突破口；双重根式找 (√a±√b)²；含 √2027 的连加裂项用 1/(√n+√(n+1))=√(n+1)-√n；知二求二熟记 a²+b²=(a+b)²-2ab；共轭根式 x、y 满足 xy=1、x+y=4n+2。</p>
      <p><strong>易错提醒</strong>：①先判被开方数≥0 再运算；②√(a²)=a 漏绝对值；③分母 x-2≠0 漏掉；④非同类根式盲目加减；⑤裂项/降次符号出错；⑥双重根式配方拆错（√(21+14√2)=√14+√7 而非 √7+√2）。</p>
      <p><strong>🎓 老师课堂总结</strong> — 综合复习课核心是把"定义→化简→求值"三条线串起来：任何题先看被开方数范围（双重非负性），化简统一走绝对值；见到根式连加想裂项、见到分式想有理化；知二求二与降次是代数求值两大神器，遇到高次多项式不要硬代，先降次再代入。</p>
    </div>
    '''
seg_replace('<div class="teacher-talk">', '<div id="tab-quiz"', TT, 'teacher-talk')

# ---------- 题库 28 题 ----------
Q = '''const questions = [
  {"q":"下列各式中，属于二次根式的是","opts":["A. √(π-4)","B. √m","C. √(a²+1)","D. ³√8"],"ans":2,"exp":"二次根式形如 √a（a≥0）。√(a²+1) 被开方数<strong>恒≥0</strong> 必是二次根式；√(π-4) 被开方数<0；√m 需额外说明 m≥0；³√8 是三次根式。"},
  {"q":"若 y=√(x-2)+√(4-2x)-√5，则 x+y 的值为","opts":["A. 2-√5","B. 2+√5","C. √5-2","D. -2-√5"],"ans":0,"exp":"双重非负：x-2≥0 且 4-2x≥0 → <strong>x=2</strong>；y=0+0-√5=-√5；x+y=<strong>2-√5</strong>。"},
  {"q":"若 |2025-a|+√(a-2026)=a，则 2025²-a 的值为","opts":["A. -2026","B. 2026","C. -2025","D. 2025"],"ans":0,"exp":"a≥2026 → |2025-a|=a-2025；a-2025+√(a-2026)=a → √(a-2026)=2025 → a-2026=2025² → 2025²-a=<strong>-2026</strong>。"},
  {"q":"若 y=(√(x²-4)+√(4-x²)+1)/(x-2)，则 √(18xy) 的平方根是","opts":["A. ±√3","B. ±3","C. √3","D. ±√5"],"ans":0,"exp":"x²=4 且分母 x-2≠0 → <strong>x=-2</strong>；y=(0+0+1)/(-4)=-1/4；xy=1/2；√(18xy)=√9=3，其<strong>平方根=±√3</strong>。"},
  {"q":"已知 1≤a≤2，化简 √(a²-2a+1)+|a-2| 的结果是","opts":["A. 1","B. 2a-3","C. 3-2a","D. -1"],"ans":0,"exp":"原式=√((a-1)²)+|a-2|=|a-1|+|a-2|=(a-1)+(2-a)=<strong>1</strong>。"},
  {"q":"使代数式 (√(2x+4)-√(10-3x))/(x+1) 有意义的 x 取值范围是","opts":["A. -2≤x≤10/3 且 x≠-1","B. -2<x<10/3","C. -2≤x≤10/3","D. x≥-2 且 x≠-1"],"ans":0,"exp":"2x+4≥0 → x≥-2；10-3x≥0 → x≤10/3；<strong>x+1≠0</strong> → x≠-1；三条件取交集。"},
  {"q":"若 b=√(a-12)+√(12-a)+8，则 a-b 的算术平方根是","opts":["A. 2","B. 4","C. 8","D. ±2"],"ans":0,"exp":"a-12≥0 且 12-a≥0 → <strong>a=12</strong>，b=8；a-b=4；<strong>算术平方根=2</strong>（非负）。"},
  {"q":"已知实数 a 满足 |75-a|+√(a-100)=a，则 a-75² 的平方根是","opts":["A. ±10","B. 10","C. ±75","D. ±100"],"ans":0,"exp":"a≥100>75 → a-75+√(a-100)=a → √(a-100)=75 → a=5725；a-75²=100；<strong>平方根=±10</strong>。"},
  {"q":"当 1<x<4 时，化简 √(1+2x+x²)-√(x²-10x+25) 的结果是","opts":["A. 2x-4","B. 6","C. 2x+6","D. -2x+4"],"ans":0,"exp":"原式=|x+1|-|x-5|=(x+1)-(5-x)=<strong>2x-4</strong>（x-5<0，去绝对值要变号）。"},
  {"q":"计算 √(3-2√2)+√(5-2√6)+√(7-2√12) 的值是","opts":["A. 1","B. 2","C. √3","D. 0"],"ans":0,"exp":"配方：(√2-1)+(√3-√2)+(2-√3)=<strong>1</strong>（逐项抵消）。"},
  {"q":"计算 √(8-4√3)+√(17+12√2)-√(11+6√2) 的值是","opts":["A. √6","B. √2","C. 2√3","D. √6-√2"],"ans":0,"exp":"8-4√3=(√6-√2)²，17+12√2=(3+2√2)²，11+6√2=(3+√2)²；原式=(√6-√2)+(3+2√2)-(3+√2)=<strong>√6</strong>。"},
  {"q":"计算 √(6+√35)-√(6-√35)+√(4+√7)-√(4-√7) 的值是","opts":["A. √10+√2","B. √10-√2","C. 2√7","D. 2√5+2"],"ans":0,"exp":"√(6±√35)=(√7±√5)/√2，前两项差=√10；√(4±√7)=(√7±1)/√2，后两项差=√2；合计 <strong>√10+√2</strong>。"},
  {"q":"下列双重二次根式的配方，正确的是","opts":["A. √(4+2√3)=√3+1","B. √(5-2√6)=√5-√2","C. √(21+14√2)=3+√2","D. √(4-√15)=(√6-√2)/2"],"ans":0,"exp":"(√3+1)²=4+2√3 ✓；B 应为 √3-√2；C 应为 √14+√7（(√14)²+(√7)²=21）；D 应为 (√10-√6)/2。"},
  {"q":"计算 (1/(1+√2)+1/(√2+√3)+…+1/(√2026+√2027))×(1+√2027) 的值是","opts":["A. 2026","B. 2027","C. 2025","D. 2026√2027"],"ans":0,"exp":"每项分母有理化裂项：(√2-1+√3-√2+…+√2027-√2026)(1+√2027)=(√2027-1)(√2027+1)=<strong>2026</strong>。"},
  {"q":"计算 1/(2+√2)+1/(3√2+2√3)+…+1/(100√99+99√100) 的值是","opts":["A. 9/10","B. 1","C. 99/100","D. 4/5"],"ans":0,"exp":"通项 1/((k+1)√k+k√(k+1)) 有理化 = 1/√k-1/√(k+1)；求和 = 1-1/√100=<strong>9/10</strong>。"},
  {"q":"比较 √13-√15 与 √11-√13 的大小，正确的是","opts":["A. √13-√15 ＞ √11-√13","B. √13-√15 ＜ √11-√13","C. 两者相等","D. 无法确定"],"ans":0,"exp":"分子有理化：√13-√15=-2/(√13+√15)，√11-√13=-2/(√11+√13)；√13+√15＞√11+√13 → 负数前者绝对值小 → <strong>前者大</strong>。"},
  {"q":"y=√(1+x)-√x（x≥0）的最大值是","opts":["A. 1","B. 0","C. 2","D. √2"],"ans":0,"exp":"分子有理化 y=1/(√(1+x)+√x)；x=0 时分母最小为 1 → y 最大 =<strong>1</strong>。"},
  {"q":"已知 a+b=-5，ab=3，则 -√(a/b)-√(b/a) 的值是","opts":["A. -5√3/3","B. 5√3/3","C. -25/3","D. ±5√3/3"],"ans":0,"exp":"设 A²=a/b+b/a+2=((a+b)²-2ab)/ab+2=(25-6)/3+2=25/3；a、b 同负 → A<0 → A=<strong>-5√3/3</strong>。"},
  {"q":"已知 √(43-x)-√(11-x)=4，则 √(43-x)+√(11-x) 的值是","opts":["A. 8","B. 4","C. 32","D. 16"],"ans":0,"exp":"(a-b)(a+b)=(43-x)-(11-x)=32 → a+b=32/4=<strong>8</strong>（平方差公式）。"},
  {"q":"计算 (√7+√6)/(√7-√6)+(√7-√6)/(√7+√6) 的值是","opts":["A. 26","B. 14","C. 13","D. 28"],"ans":0,"exp":"通分：(√7+√6)²+(√7-√6)²=13+2√42+13-2√42=<strong>26</strong>，分母 7-6=1。"},
  {"q":"x=(√(n+1)-√n)/(√(n+1)+√n)，y=(√(n+1)+√n)/(√(n+1)-√n)，n 为正整数，且 19x²+123xy+19y²=1985，则 n 的值是","opts":["A. 2","B. 3","C. 1","D. 4"],"ans":0,"exp":"xy=1，x+y=<strong>4n+2</strong>；19[(x+y)²-2]+123=1985 → 19(x+y)²+85=1985 → (x+y)²=100 → 4n+2=10 → n=<strong>2</strong>。"},
  {"q":"已知 √(21+x²)-√(17-x²)=4，则 √(21+x²)+√(17-x²) 的值是","opts":["A. 2√15","B. 2√17","C. √60","D. 4√15"],"ans":0,"exp":"令 a-b=4，a²+b²=38；(a+b)²=2(a²+b²)-(a-b)²=76-16=60 → a+b=<strong>2√15</strong>。"},
  {"q":"若 a=1/(√2-1)，则 3a³-12a²+9a-12 的值是","opts":["A. -18","B. 18","C. 0","D. -12"],"ans":0,"exp":"a=√2+1 → (a-1)²=2 → a²=2a+1 → a³=5a+2；原式=3(5a+2)-12(2a+1)+9a-12=<strong>-18</strong>（降次后 a 项抵消）。"},
  {"q":"若 (√17-4)a=1，则 a⁴-10a³+18a²-22a+165 的值是","opts":["A. 168","B. 172","C. 0","D. 165"],"ans":0,"exp":"a=√17+4 → a²=8a+1；迭代：a³=65a+8，a⁴=528a+65；原式=(528-650+144-22)a+常数=0·a+<strong>168</strong>。"},
  {"q":"已知 a+b=-4，ab=4，则 b√(b/a)+a√(a/b) 的值是","opts":["A. -4","B. 4","C. 0","D. ±4"],"ans":0,"exp":"a+b=-4 且 ab=4 → a=b=-2；原式=(-2)·√1+(-2)·√1=<strong>-4</strong>。"},
  {"q":"已知 √(15+x²)-√(19-x²)=2，则 √(15+x²)+√(19-x²) 的值是","opts":["A. 8","B. 2√17","C. 2√15","D. 6"],"ans":0,"exp":"令 a-b=2，a²+b²=34；(a+b)²=2(a²+b²)-(a-b)²=68-4=64 → a+b=<strong>8</strong>。⚠️ 2√17≈8.25 与条件自洽不符。"},
  {"q":"新定义：若 n²＜T＜(n+1)²（T 为正整数），称 √T 的“青一区间”为 (n,n+1)，-√T 的为 (-n-1,-n)。则 √17 与 -√23 的“青一区间”分别是","opts":["A. (4,5) 与 (-5,-4)","B. (4,5) 与 (-4,-3)","C. (3,4) 与 (-5,-4)","D. (5,6) 与 (-4,-3)"],"ans":0,"exp":"4²＜17＜5² → √17∈(4,5)；4²＜23＜5² → √23∈(4,5) → -√23∈(-5,-4)。"},
  {"q":"已知 x+y=2√3，xy=-2，则 x²+y² 的值是","opts":["A. 16","B. 14","C. 10","D. 12"],"ans":0,"exp":"x²+y²=(x+y)²-2xy=12-(-4)=<strong>16</strong>（知二求二基础公式）。"}
];'''
arr_replace('const questions = [', Q, 'questions')

# ---------- 卡牌 14 张 ----------
F = '''const flashcards = [
  {"front":"二次根式的定义？","back":"形如 <strong>√a（a≥0）</strong> 的式子；³√a 是三次根式不算；√(a²+1) 恒有意义。"},
  {"front":"二次根式有意义的条件？","back":"①被开方数≥0；②若在分母 → 分母≠0；③偶次根式被开方数≥0，奇次根式任意实数。"},
  {"front":"双重非负性是什么？","back":"a≥0 且 <strong>√a≥0</strong>；两被开方数互为相反数（√(x²-4) 与 √(4-x²)）→ 只能同时为 0，常用来求参。"},
  {"front":"√(a²)=？","back":"<strong>|a|</strong>，先写绝对值再按范围展开。1<x<4 时 √((x+1)²)-√((x-5)²)=2x-4。"},
  {"front":"双重根式怎么配方？","back":"找 (√a±√b)²：√(3+2√2)=√2+1；√(5-2√6)=√3-√2；√(21+14√2)=√14+√7；√(4-√15)=(√10-√6)/2。"},
  {"front":"分母有理化公式？","back":"1/(√a+√b)=(√a-√b)/(a-b)；1/(√a-√b)=(√a+√b)/(a-b)；1/√a=√a/a。"},
  {"front":"分子有理化有什么用？","back":"√a-√b=(a-b)/(√a+√b)。用于比较根式大小（√13-√15 vs √11-√13）与求最值（y=√(1+x)-√x 最大 1）。"},
  {"front":"根式裂项公式？","back":"1/(√n+√(n+1))=<strong>√(n+1)-√n</strong>；连加从 1 到 2027 会首尾相消。"},
  {"front":"知二求二有哪些公式？","back":"a²+b²=(a+b)²-2ab；(a-b)²=(a+b)²-4ab；a³+b³=(a+b)³-3ab(a+b)。"},
  {"front":"√(a/b)+√(b/a) 型怎么求？","back":"先平方：A²=a/b+b/a+2=(a²+b²)/(ab)+2，再根据 a、b 符号<strong>定号</strong>。"},
  {"front":"共轭根式 x、y 有什么性质？","back":"x=(√(n+1)-√n)/(√(n+1)+√n)，y=1/x：xy=<strong>1</strong>，x+y=<strong>4n+2</strong>。"},
  {"front":"高次多项式怎么降次代入？","back":"由 a²=2a+1 迭代：a³=2a²+a=5a+2，a⁴=… 全部换成 a 的一次式，a 项系数常会抵消。"},
  {"front":"平方差求根式和差？","back":"(√A-√B)(√A+√B)=A-B。差已知时，和=(A-B)/差；如 √(43-x)-√(11-x)=4 → 和=32/4=8。"},
  {"front":"算术平方根 vs 平方根？","back":"√4=<strong>2</strong>（算术）；x²=4 → x=<strong>±2</strong>（平方根）；√(a²)=|a| 也体现非负。"}
];'''
arr_replace('const flashcards = [', F, 'flashcards')

# ---------- 易错 8 条 ----------
E = '''errors = [
  {"title":"❌ 忽略被开方数≥0","wrong":"见到 √(x-2) 直接开方运算，不先要求 x≥2。","right":"<strong>先定范围再运算</strong>：被开方数≥0、分母≠0 是第一步；双重根式更要先判定义域。"},
  {"title":"❌ √(a²)=a 漏绝对值","wrong":"把 √((x-5)²) 直接写成 x-5，导致 1<x<4 时符号错误。","right":"√(a²)=<strong>|a|</strong>：先写绝对值，再按变量范围去绝对值（x-5<0 时 =5-x）。"},
  {"title":"❌ 双重非负求参漏分母","wrong":"由 x²-4=0 直接得 x=±2，没有排除分母 x-2。","right":"双重非负给 x²=4 后还要看<strong>分母 x-2≠0</strong> → x 只能取 -2。"},
  {"title":"❌ 非同类二次根式盲目加减","wrong":"√2+√3=√5；2√2+3√3=5√5 的合并错误。","right":"只有<strong>同类二次根式</strong>（被开方数相同）才能合并：√2+√3 不能化简；2√2+3√2=5√2。"},
  {"title":"❌ 裂项符号写反","wrong":"把 1/(√n+√(n+1)) 写成 √n-√(n+1)（负数）。","right":"1/(√n+√(n+1))=<strong>√(n+1)-√n</strong>（恒为正），分子有理化时勿丢正负。"},
  {"title":"❌ 去绝对值不讨论范围","wrong":"|2025-a|+√(a-2026)=a 不先判 a≥2026，直接把 |2025-a| 当 2025-a。","right":"√(a-2026) 定义域 a≥2026 → |2025-a|=a-2025，等式才能化简求解。"},
  {"title":"❌ 双重根式配方拆错","wrong":"把 √(21+14√2) 配成 (√7+√2)²（21 拆错）。","right":"凑 (√14+√7)²：14+7=21、2·√14·√7=2√98=14√2 ✓。"},
  {"title":"❌ 平方求值后忘定号","wrong":"-√(a/b)-√(b/a) 平方得 25/3 后直接取 ±5√3/3。","right":"先由 a、b 同负判断<strong>原式为负</strong>，再取负号：-5√3/3。"}
];'''
arr_replace('errors = [', E, 'errors')

# ---------- localStorage keys ----------
rep("const WRONG_HISTORY_KEY='quiz_english_lesson1_wrong';",
    "const WRONG_HISTORY_KEY='quiz_math26q_lesson1_wrong';", 'wrong-key')
rep("var QUIZ_PROG_KEY='quiz_progress_english_lesson1';",
    "var QUIZ_PROG_KEY='quiz_progress_math26q_lesson1';", 'prog-key')
if h.count('english_lesson1_state_check') == 5:
    h = h.replace('english_lesson1_state_check', 'math26q_lesson1_state_check')
    report.append('OK[state-key x5]')
else:
    report.append(f'FAIL[state-key]: {h.count("english_lesson1_state_check")}')

# ---------- import 文案 ----------
rep("subject:'英语(双语B班)',chapter:'第1讲 Holidays & 暑假话题',content:q.q,correct_answer:q.opts[q.ans],my_answer:q.opts[myAns]||'未作答',error_reason:'概念不清',source:'练习',difficulty:3,tags:'英语,双语B班,第1讲,holiday,nothing but,against,so...that,不定代词,词形变化'",
    "subject:'数学(博学班)',chapter:'第1讲 二次根式综合复习',content:q.q,correct_answer:q.opts[q.ans],my_answer:q.opts[myAns]||'未作答',error_reason:'概念不清',source:'练习',difficulty:3,tags:'数学,博学班,2026秋,第1讲,二次根式,双重非负性,双重根式,裂项,知二求二,降次'",
    'autoImport-tags')
rep("subject:'英语',chapter:'第1讲 Holidays & 暑假话题',content:w.q.q,correct_answer:w.q.opts[w.q.ans],my_answer:w.q.opts[w.uc]||'未作答',error_reason:'概念不清',source:'练习',difficulty:3,tags:'英语,双语B班,第1讲,holiday,nothing but,against,so that,不定代词,词形变化'",
    "subject:'数学',chapter:'第1讲 二次根式综合复习',content:w.q.q,correct_answer:w.q.opts[w.q.ans],my_answer:w.q.opts[w.uc]||'未作答',error_reason:'概念不清',source:'练习',difficulty:3,tags:'数学,博学班,2026秋,第1讲,二次根式'",
    'importWB-tags')

# ---------- 残留检查 ----------
for pat in ['Holidays','双语','english_lesson1','quiz_progress_english','quiz_english','nothing but','不定代词','32 题','15 张']:
    c = h.count(pat)
    if c:
        report.append(f'WARN leftover[{pat}] = {c}')

open(FN, 'w', encoding='utf-8').write(h)
print('new len', len(h))
print('\n'.join(report))
