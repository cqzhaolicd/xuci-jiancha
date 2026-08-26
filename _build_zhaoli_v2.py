# -*- coding: utf-8 -*-
"""基于《Python Crash Course 3rd》蒸馏笔记, 重写/增强赵立 AI 学习页(防幻觉)"""
import io, sys, json, subprocess, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# ================= 复用 build_page 生成器(从 _build_zhaoli_pages.py 提取) =================
def build_page(fname, title, subtitle, kp_key, knowledge, questions, flashcards, errors, color='#667eea'):
    kp_items = '\n'.join(f'      <div class="k-item"><h4>{t}</h4><p>{c}</p></div>' for t, c in knowledge)
    q_arr = json.dumps([{"q": q, "opts": o, "ans": a, "exp": e} for q, o, a, e in questions], ensure_ascii=False)
    fc_arr = json.dumps([{"q": q, "a": a} for q, a in flashcards], ensure_ascii=False)
    err_arr = json.dumps([{"title": t, "wrong": w, "right": r} for t, w, r in errors], ensure_ascii=False)
    n_q = len(questions); n_fc = len(flashcards); n_err = len(errors)

    html = f'''<!DOCTYPE html><html lang="zh-CN"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{title} · 赵立AI学习</title>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;500;600;700;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
<style>
:root{{--primary:{color};--bg:#f0f2f5;--card-bg:#fff;--text:#1a202c;--text-light:#718096;--border:#e2e8f0;--radius:16px;--radius-sm:10px}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:"Noto Sans SC",sans-serif;background:var(--bg);color:var(--text);line-height:1.7}}
.navbar{{background:linear-gradient(135deg,var(--primary),var(--primary)dd);padding:.6rem 0;position:sticky;top:0;z-index:1000}}
.navbar .container{{max-width:1000px;margin:0 auto;padding:0 1rem;display:flex;align-items:center;justify-content:space-between}}
.navbar-brand{{color:#fff;text-decoration:none;font-size:1rem;font-weight:700;display:flex;align-items:center;gap:.35rem}}
.navbar-nav{{display:flex;gap:.1rem}}
.navbar-nav a{{color:rgba(255,255,255,.85);text-decoration:none;padding:.25rem .55rem;border-radius:6px;font-size:.75rem;cursor:pointer;transition:all .15s}}
.navbar-nav a:hover,.navbar-nav a.active{{background:rgba(255,255,255,.2);color:#fff}}
.container{{max-width:960px;margin:0 auto;padding:.5rem 1rem}}
.hero{{background:var(--card-bg);border-radius:var(--radius);padding:1.2rem 1.5rem;margin-bottom:.8rem;text-align:center}}
.hero h1{{font-size:1.25rem;font-weight:800;color:var(--text)}}
.hero h1 i{{color:var(--primary);margin-right:.35rem}}
.hero .meta{{margin-top:.3rem;font-size:.78rem;color:var(--text-light)}}
.tab-nav{{display:flex;gap:.3rem;margin-bottom:.8rem;flex-wrap:wrap}}
.tab-btn{{padding:.4rem .75rem;border:2px solid var(--border);border-radius:var(--radius-sm);background:var(--card-bg);cursor:pointer;font-size:.78rem;font-weight:500;color:var(--text-light)}}
.tab-btn:hover,.tab-btn.active{{border-color:var(--primary);color:var(--primary)}}
.tab-content{{display:none}}.tab-content.active{{display:block}}
.card{{background:var(--card-bg);border-radius:var(--radius);padding:1rem 1.2rem;margin-bottom:.6rem}}
.card-title{{font-size:.88rem;font-weight:700;margin-bottom:.6rem;color:var(--text)}}
.knowledge-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:.5rem}}
.k-item{{background:var(--bg);border-radius:var(--radius-sm);padding:.7rem;border-left:3px solid var(--primary)}}
.k-item h4{{font-size:.8rem;font-weight:600;color:var(--text);margin-bottom:.2rem}}
.k-item p{{font-size:.74rem;color:var(--text-light);line-height:1.5}}
.quiz-progress{{display:flex;align-items:center;gap:.5rem;margin-bottom:.5rem;flex-wrap:wrap}}
.quiz-progress .progress-bar{{flex:1;height:5px;background:var(--border);border-radius:3px;overflow:hidden;min-width:80px}}
.quiz-progress .progress-fill{{height:100%;background:var(--primary);border-radius:3px;transition:width .3s}}
.quiz-progress span{{font-size:.74rem;color:var(--text-light)}}
.q-header{{font-size:.95rem;font-weight:600;margin-bottom:.7rem;color:var(--text)}}
.option{{display:block;width:100%;padding:.55rem .75rem;margin-bottom:.3rem;border:2px solid var(--border);border-radius:var(--radius-sm);background:var(--card-bg);cursor:pointer;text-align:left;font-size:.8rem;color:var(--text);transition:all .12s}}
.option:hover:not(.disabled){{border-color:var(--primary)}}
.option.correct{{border-color:#48bb78;background:rgba(72,187,120,.08);color:#48bb78}}
.option.wrong{{border-color:#f56565;background:rgba(245,101,101,.08);color:#f56565}}
.option.disabled{{cursor:default;opacity:.7}}
.exp-box{{margin-top:.5rem;padding:.6rem;background:#fffbeb;border-radius:var(--radius-sm);border-left:4px solid #ecc94b;font-size:.78rem;color:var(--text);line-height:1.5}}
.result-card{{text-align:center;padding:1.5rem}}
.result-card .score{{font-size:2.2rem;font-weight:900;color:var(--primary)}}
.result-card .sub{{font-size:.82rem;color:var(--text-light);margin-top:.25rem}}
.flashcard{{background:var(--card-bg);border-radius:var(--radius);padding:1.5rem;text-align:center;min-height:140px;cursor:pointer;border:2px solid var(--border);transition:all .2s;display:flex;flex-direction:column;justify-content:center;align-items:center}}
.flashcard:hover{{border-color:var(--primary)}}
.flashcard .front{{font-size:.9rem;font-weight:600;color:var(--text)}}
.flashcard .back{{font-size:.8rem;color:var(--text-light);margin-top:.4rem}}
.flashcard-nav{{display:flex;justify-content:center;align-items:center;gap:.5rem;margin-top:.5rem}}
.flashcard-counter{{font-size:.78rem;color:var(--text-light)}}
.check-item{{padding:.55rem .75rem;background:var(--card-bg);border-radius:var(--radius-sm);margin-bottom:.3rem;border-left:4px solid #f56565;font-size:.78rem;color:var(--text)}}
.check-item strong{{color:#f56565}}
.footer{{text-align:center;padding:.8rem;font-size:.74rem;color:var(--text-light)}}
.btn{{padding:.3rem .65rem;border-radius:var(--radius-sm);border:none;cursor:pointer;font-size:.76rem;margin:.15rem;color:#fff}}
.btn-primary{{background:var(--primary);color:#fff}}
.btn-outline{{background:transparent;border:2px solid var(--border);color:#718096}}
.btn-sm{{padding:.18rem .4rem;font-size:.7rem}}
@media(max-width:768px){{.navbar-nav a span{{display:none}}.knowledge-grid{{grid-template-columns:1fr}}}}
.quiz-mode-bar{{display:flex;gap:.4rem;flex-wrap:wrap;align-items:center;margin-bottom:.8rem;padding:.5rem .6rem;background:var(--bg);border:1px solid var(--border);border-radius:var(--radius-sm)}}
.qm-btn{{border:1.5px solid var(--border);background:transparent;color:var(--text);padding:.3rem .75rem;border-radius:20px;font-size:.78rem;cursor:pointer;transition:all .2s;line-height:1.4}}
.qm-btn.qm-active{{background:var(--primary);color:#fff;border-color:var(--primary);font-weight:600}}
#quizModeInfo{{margin-left:auto;font-size:.74rem;color:var(--text-light);white-space:nowrap}}
.done-badge{{display:inline-block;font-size:.64rem;font-weight:700;padding:.12rem .45rem;border-radius:10px;margin-left:.35rem;vertical-align:middle;line-height:1.4}}
.done-badge.ok{{background:#48bb7818;color:#2f855a;border:1px solid #48bb7855}}
.done-badge.no{{background:#e74c3c18;color:#c0392b;border:1px solid #e74c3c55}}
@media(max-width:768px){{#quizModeInfo{{display:none}}}}
.flashcard{{position:relative}}
.flashcard .fc-mark{{position:absolute;top:.25rem;right:.25rem;cursor:pointer;font-size:.55rem;color:#999;transition:all .2s;z-index:5;background:rgba(255,255,255,.85);border-radius:8px;padding:1px 4px;display:inline-flex;align-items:center;gap:2px}}
.flashcard .fc-mark.done{{color:#27ae60}}
.flashcard.kp-learned{{border-color:rgba(46,204,113,.6);background:rgba(46,204,113,.06)}}
.check-item{{position:relative}}
.check-item .ec-mark{{cursor:pointer;font-size:.58rem;color:#999;margin-left:.3rem;transition:all .2s;display:inline-flex;align-items:center}}
.check-item .ec-mark.done{{color:#27ae60}}
.check-item.kp-learned{{background:rgba(46,204,113,.12);border-left-color:#27ae60}}
</style><style>.toast{{position:fixed;top:1.2rem;left:50%;transform:translateX(-50%);z-index:9999;padding:.6rem 1.2rem;border-radius:10px;font-size:.85rem;font-weight:600;color:#fff;box-shadow:0 4px 16px rgba(0,0,0,.18);opacity:1;transition:opacity .3s;pointer-events:none;max-width:86vw;text-align:center}}
.toast-success{{background:#48bb78}}
.toast-warning{{background:#ed8936}}
.toast-info{{background:#667eea}}</style></head><body>
<nav class="navbar"><div class="container">
  <a class="navbar-brand" href="zhaoli_index.html"><i class="fas fa-arrow-left"></i> AI学习中心</a>
  <div class="navbar-nav">
    <a class="active" onclick="switchTab('knowledge')"><i class="fas fa-sitemap"></i><span>知识点</span></a>
    <a onclick="switchTab('quiz')"><i class="fas fa-pen"></i><span>测验</span></a>
    <a onclick="switchTab('flashcard')"><i class="fas fa-layer-group"></i><span>卡片</span></a>
    <a onclick="switchTab('errors')"><i class="fas fa-exclamation-triangle"></i><span>易错点</span></a>
  </div>
</div></nav>
<div class="container">
  <div class="hero">
    <h1><i class="fas fa-book-open"></i> {title}</h1>
    <div class="meta">{subtitle} · {n_q} 题 · {n_fc} 卡牌</div>
  </div>
  <div class="tab-nav">
    <button class="tab-btn active" onclick="switchTab('knowledge')"><i class="fas fa-sitemap"></i> 知识图谱</button>
    <button class="tab-btn" onclick="switchTab('quiz')"><i class="fas fa-pen"></i> 闯关测验</button>
    <button class="tab-btn" onclick="switchTab('flashcard')"><i class="fas fa-layer-group"></i> 知识卡牌</button>
    <button class="tab-btn" onclick="switchTab('errors')"><i class="fas fa-exclamation-triangle"></i> 易错自检</button>
  </div>
  <div id="tab-knowledge" class="tab-content active"><div class="knowledge-grid">
{kp_items}
  </div></div><div id="tab-quiz" class="tab-content"><div class="quiz-mode-bar" id="quizModeBar">
    <button class="qm-btn qm-active" data-m="all" onclick="setQuizMode('all')">📋 全部</button>
    <button class="qm-btn" data-m="todo" onclick="setQuizMode('todo')">🆕 未做</button>
    <button class="qm-btn" data-m="wrong" onclick="setQuizMode('wrong')">❌ 错题</button>
    <span id="quizModeInfo"></span>
  </div>
<div id="quizArea"></div></div>
  <div id="tab-flashcard" class="tab-content">
    <p style="font-size:.76rem;color:var(--text-light);margin-bottom:.4rem">点击卡片翻转查看答案</p>
    <div id="flashcardArea"></div>
  </div>
  <div id="tab-errors" class="tab-content">
    <div class="card"><div class="card-title"><i class="fas fa-exclamation-triangle" style="color:#f56565"></i> 高频易错点自检</div>
    <div id="errorChecklist"></div></div>
  </div>
</div>
<div class="footer">为赵立定制的 AI 学习工具 | {subtitle} | 持续更新中</div>
<script>
function speakDone(){{
  try{{
    if(!window.__voiceMuted && window.speechSynthesis){{
      window.speechSynthesis.cancel();
      var u=new SpeechSynthesisUtterance('你完成了一项，太棒了');
      u.lang='zh-CN'; u.rate=0.95; u.pitch=1.05;
      window.speechSynthesis.speak(u);
    }}
  }}catch(e){{}}
}}
const KP_KEY = '{kp_key}';
function getKP() {{ try {{ return JSON.parse(localStorage.getItem(KP_KEY) || '[]'); }} catch(e) {{ return []; }} }}
function toggleKP(name, el) {{
  let arr = getKP();
  const i = arr.indexOf(name);
  if (i >= 0) {{ arr.splice(i, 1); }} else {{ arr.push(name); speakDone(); }}
  localStorage.setItem(KP_KEY, JSON.stringify(arr));
  const item = el.closest('.k-item, .flashcard, .check-item');
  if (item) item.classList.toggle('kp-learned', arr.includes(name));
  const mark = el.querySelector('.kp-mark') || el;
  if (mark) {{
    mark.innerHTML = arr.includes(name) ? '<i class="fas fa-check-circle"></i> 已学习' : '<i class="far fa-circle"></i> 已学习';
  }}
  try {{
    const ac = new (window.AudioContext || window.webkitAudioContext)();
    const o = ac.createOscillator(), g = ac.createGain();
    o.connect(g); g.connect(ac.destination);
    o.frequency.value = arr.includes(name) ? 880 : 440; o.type = 'sine';
    g.gain.setValueAtTime(0.08, ac.currentTime);
    g.gain.exponentialRampToValueAtTime(0.001, ac.currentTime + 0.12);
    o.start(ac.currentTime); o.stop(ac.currentTime + 0.12);
  }} catch(e) {{}}
}}
function kpMark(name) {{
  const learned = getKP().includes(name);
  return '<span class="kp-mark ' + (learned ? 'done' : '') + '" title="标记已学习">' + (learned ? '<i class="fas fa-check-circle"></i> 已学习' : '<i class="far fa-circle"></i> 已学习') + '</span>';
}}
function kpInit() {{
  document.querySelectorAll('.k-item').forEach(item => {{
    const titleEl = item.querySelector('h4');
    if (!titleEl) return;
    const name = titleEl.textContent.trim();
    const learned = getKP().includes(name);
    item.classList.toggle('kp-learned', learned);
    const mark = document.createElement('span');
    mark.className = 'kp-mark' + (learned ? ' done' : '');
    mark.innerHTML = learned ? '<i class="fas fa-check-circle"></i> 已学习' : '<i class="far fa-circle"></i> 已学习';
    mark.setAttribute('data-kp', encodeURIComponent(name));
    mark.title = '标记已学习';
    titleEl.parentNode.insertBefore(mark, titleEl.nextSibling);
  }});
}}
document.addEventListener('DOMContentLoaded', kpInit);
function fcMark(q) {{
  const learned = getKP().includes('fc:' + q);
  return '<span class="kp-mark fc-mark ' + (learned ? 'done' : '') + '" data-kp="fc:' + encodeURIComponent(q) + '" title="标记已学习">' + (learned ? '<i class="fas fa-check-circle"></i> 已学习' : '<i class="far fa-circle"></i> 已学习') + '</span>';
}}
function ecMark(t) {{
  const learned = getKP().includes('err:' + t);
  return '<span class="kp-mark ec-mark ' + (learned ? 'done' : '') + '" data-kp="err:' + encodeURIComponent(t) + '" title="标记已学习">' + (learned ? '<i class="fas fa-check-circle"></i> 已学习' : '<i class="far fa-circle"></i> 已学习') + '</span>';
}}
document.addEventListener('click', function(e) {{
  const mark = e.target.closest('.kp-mark');
  if (!mark) return;
  const name = decodeURIComponent(mark.getAttribute('data-kp'));
  e.preventDefault(); e.stopPropagation();
  toggleKP(name, mark);
}});
function toast(msg,type){{type=type||'info';var el=document.createElement('div');el.className='toast toast-'+type;el.textContent=msg;document.body.appendChild(el);setTimeout(function(){{el.style.opacity='0';setTimeout(function(){{el.remove();}},350);}},2600);}}
const questions={q_arr}
const flashcards={fc_arr}
const errors={err_arr}
let curQ=0;let score=0;let answered=0;let fIdx=0;let shuffled=questions.map(function(_,i){{return i;}}).sort(function(){{return Math.random()-0.5;}});
var QUIZ_MODE='all';
var QUIZ_PROG_KEY='quiz_progress_{kp_key}';
function getQuizProg(){{try{{return JSON.parse(localStorage.getItem(QUIZ_PROG_KEY)||'{{}}')}}catch(e){{return {{}}}}}}
function saveQuizProg(idx,res){{var p=getQuizProg();p[idx]=res;localStorage.setItem(QUIZ_PROG_KEY,JSON.stringify(p));updateModeInfo();}}
function updateModeInfo(){{var p=getQuizProg();var keys=Object.keys(p);var wrong=0;keys.forEach(function(k){{if(p[k]==='wrong')wrong++;}});var el=document.getElementById('quizModeInfo');if(el)el.textContent='已做 '+keys.length+'/'+questions.length+' · 错题 '+wrong;}}
function setQuizMode(m){{QUIZ_MODE=m;document.querySelectorAll('.qm-btn').forEach(function(b){{b.classList.toggle('qm-active',b.getAttribute('data-m')===m)}});initQ();if(shuffled.length)renderQ();}}
function quizFilterIds(){{var ids=questions.map(function(_,i){{return i;}});if(QUIZ_MODE==='all')return ids;var p=getQuizProg();if(QUIZ_MODE==='todo')return ids.filter(function(i){{return !(i in p)}});return ids.filter(function(i){{return p[i]==='wrong'}})}}
function showQuizEmpty(){{var el=document.getElementById('quizArea');if(!el)return;var msg=QUIZ_MODE==='wrong'?'🎉 没有错题，全部掌握！':'🎉 所有题都已做过！切换「全部」可重新练习。';el.innerHTML='<div class="result-card" style="text-align:center;padding:2rem"><div style="font-size:2rem;margin-bottom:.5rem">'+(QUIZ_MODE==='wrong'?'🎉':'✅')+'</div><p style="color:var(--text-light)">'+msg+'</p><div style="margin-top:1rem"><button class="btn btn-primary" onclick="setQuizMode(&#39;all&#39;)">📋 切换全部</button></div></div>';}}
function initQ(){{curQ=0;score=0;answered=0;var ids=quizFilterIds();if(!ids.length){{showQuizEmpty();shuffled=[];return;}}shuffled=ids.sort(function(){{return Math.random()-0.5;}});updateModeInfo();}}
function renderQ(){{if(curQ>=questions.length){{showResult();return;}}
var q=questions[shuffled[curQ]];var prog=document.getElementById('quizArea');
prog.innerHTML='<div class="quiz-progress"><span>第'+(curQ+1)+'/'+questions.length+'题</span><div class="progress-bar"><div class="progress-fill" style="width:'+(curQ/questions.length*100)+'%"></div></div><span>'+score+'/'+answered+'</span></div><div class="q-header">'+(function(){{var _dp=getQuizProg()[shuffled[curQ]];return _dp?'<span class="done-badge '+(_dp==='ok'?'ok':'no')+'">'+(_dp==='ok'?'✅已做':'❌已做')+'</span>':'';}})()+q.q+'</div>'+
q.opts.map(function(o,i){{return '<button class="option" onclick="selA('+i+')">'+o+'</button>';}}).join('');}}
function selA(oi){{var idx=shuffled[curQ];if(questions[idx]._answered)return;questions[idx]._answered=1;answered++;saveQuizProg(idx,oi===questions[idx].ans?'ok':'wrong');
var btns=document.querySelectorAll('.option');btns.forEach(function(b,i){{b.onclick=null;b.classList.add('disabled');
if(i===questions[idx].ans)b.classList.add('correct');if(i===oi&&oi!==questions[idx].ans)b.classList.add('wrong');}});
if(oi===questions[idx].ans){{score++;speakDone();}}else{{toast('❌ 记入错题','warning');}}var qh=document.querySelector('.q-header');
qh.insertAdjacentHTML('afterend','<div class="exp-box">'+questions[idx].exp+'</div>');
var nav=document.createElement('div');nav.style.cssText='margin-top:.9rem;text-align:center';nav.innerHTML='<button class="btn btn-primary" onclick="nextQ()">'+(curQ<questions.length-1?'下一题':'查看结果')+'</button>';document.getElementById('quizArea').appendChild(nav);}}
function nextQ(){{if(curQ<questions.length-1){{curQ++;renderQ();}}else showResult();}}
function showResult(){{document.getElementById('quizArea').innerHTML='<div class="result-card"><div class="score">'+score+'/'+questions.length+'</div><div class="sub">答对'+score+'题 / 共'+questions.length+'题</div><div style="margin-top:.8rem"><button class="btn btn-primary" onclick="initQ();renderQ();">重新测验</button></div></div>';}}
function renderFC(dir){{if(dir==='next'&&fIdx<flashcards.length-1)fIdx++;else if(dir==='prev'&&fIdx>0)fIdx--;
var fc=flashcards[fIdx];var a=document.getElementById('flashcardArea');
a.innerHTML='<div class="flashcard" id="fc-card"><div class="front">'+fc.q+' '+fcMark(fc.q)+'</div><div class="back" style="display:block">'+fc.a+'</div></div><div class="flashcard-nav"><button class="btn btn-outline btn-sm" onclick="goPrev()"'+(fIdx===0?' disabled':'')+'><i class="fas fa-arrow-left"></i> 上一张</button><span class="flashcard-counter">'+(fIdx+1)+'/'+flashcards.length+'</span><button class="btn btn-primary btn-sm" onclick="goNext()"'+(fIdx===flashcards.length-1?' disabled':'')+'>下一张 <i class="fas fa-arrow-right"></i></button></div>';
document.getElementById('fc-card').onclick=function(){{this.classList.toggle('flipped');}};}}
function goPrev(){{fIdx--;renderFC(null);}}
function goNext(){{fIdx++;renderFC(null);}}
function renderEC(){{var a=document.getElementById('errorChecklist');
a.innerHTML=errors.map(function(e){{return '<div class="check-item"><strong>'+e.title+'</strong>'+ecMark(e.title)+'<br>'+e.wrong+'<br><span style="color:#48bb78">→ '+e.right+'</span></div>';}}).join('');}}
function switchTab(n){{document.querySelectorAll('.tab-content').forEach(function(e){{e.classList.remove('active');}});
document.querySelectorAll('.tab-btn').forEach(function(e){{e.classList.remove('active');}});
document.getElementById('tab-'+n).classList.add('active');
document.querySelectorAll('.tab-btn').forEach(function(e){{var im={{knowledge:'fa-sitemap',quiz:'fa-pen',flashcard:'fa-layer-group',errors:'fa-exclamation-triangle'}};if(e.innerHTML.includes(im[n]))e.classList.add('active');}});}}
renderFC();initQ();renderQ();renderEC();
</script>
</body></html>'''
    open(fname, 'w', encoding='utf-8').write(html)
    return len(html)

# ================= Python 基础页(重写, 基于教材 Ch1-7) =================
py_knowledge = [
    ('Python 与运行方式', '解释型语言，语法简洁。Python 3.9+ 为佳；终端 `>>>` 提示符可运行代码片段（Windows 用 python，macOS/Linux 用 python3）。写 .py 文件用 `python hello.py` 运行。'),
    ('变量：标签模型', '变量是贴在值上的标签（不是盒子），值可随时更改，Python 始终跟踪当前值。命名：字母/下划线开头、不能含空格、避免关键字、小写+下划线。拼写不一致 → NameError（Python 不做拼写检查）。'),
    ('字符串与常用方法', '引号内都是字符串（单/双引号均可）。方法：title()/upper()/lower()、strip()/lstrip()/rstrip()（去空白，需重新赋值才永久）、removeprefix()/removesuffix()（删前后缀，如 URL 去 https://）。含撇号用双引号包住，否则 SyntaxError。'),
    ('f-string 格式化', '在开引号前加 f，用花括号 {} 插入变量或表达式：f"Hello, {name}!"。忘记 f 前缀 → 花括号原样输出。'),
    ('整数与浮点', '算术：+ - * /(真除，总返回浮点) **(幂)，遵循运算顺序。0.2+0.1=0.30000000000000004 是浮点精度问题（所有语言共有，不是 bug）。数字可加下划线分组：14_000_000_000。常量用全大写约定：MAX_CONNECTIONS=5000。'),
    ('列表 List', '方括号 [] 有序可变集合。索引从 0 开始，-1 取最后一个。增 append()/insert()、删 del/pop()/remove()、组织 sort()/sorted()/reverse()、len()。访问不存在索引 → IndexError。'),
    ('列表操作进阶', 'for 循环遍历（缩进是语法！）。range(1,5) 含头不含尾。min()/max()/sum()。列表解析：[x**2 for x in range(1,11)]。切片 players[0:3] 含头不含尾，复制用 [:]（直接 = 只是同一列表两个名字）。'),
    ('元组 Tuple', '不可变列表，圆括号定义：dimensions=(200,50)。元素不可改（TypeError），但可整体重新赋值。单元素元组要尾随逗号 my_t=(3,)。存\"不应改变的值\"时用元组。'),
    ('if 条件语句', '条件测试：== 比较、= 赋值，别混淆！比较区分大小写（可用 lower() 忽略）。and/or 组合、in/not in 成员检查。if-elif-else 只执行第一个通过的分支；多个独立 if 检查所有条件。'),
    ('字典 Dict', '花括号键值对：{...}。取值 d["key"]（不存在→KeyError）或 d.get("key",默认值)（安全，默认 None）。增改 d["k"]=v，删除 del。遍历 items()/keys()/values()，sorted() 排序、set() 去重。嵌套：字典列表/字典中列表/字典中字典。'),
    ('input() 与 while', 'input() 永远返回字符串，数值要 int() 转换（否则 TypeError）。while 条件循环，用退出值/flag/break/continue 控制。修改列表内容时用 while 而不是 for（如删除全部指定值）。'),
    ('函数 Function', 'def 定义。形参=定义占位，实参=调用传入。位置实参/关键字实参(名=值)/默认值(必须放后面)。return 返回值。*args 收任意数量实参（元组），**kwargs 收任意关键字实参（字典）。可变默认参数陷阱：用 None 占位。'),
    ('模块与导入', '模块=存函数的 .py 文件。5 种导入：import pizza；from pizza import make_pizza；起别名 from pizza import make_pizza as mp / import pizza as p；from pizza import *（不推荐，可能覆盖同名函数）。'),
    ('文件读写 (第3版 pathlib)', '第3版用 pathlib.Path：path=Path("a.txt")，读 contents=path.read_text()（可加 encoding="utf-8"），写 path.write_text(contents)（覆盖！）。splitlines() 逐行。读出的都是字符串，数字要转换。'),
    ('异常处理', 'try-except-else 捕获运行时错误（ZeroDivisionError、FileNotFoundError）。try 只放可能出错的行，else 放依赖成功的结果。except 里写 pass 静默失败。别用裸 except: 会吞掉所有错误包括自己的 bug。'),
    ('JSON 持久化', 'json.dumps() 数据→JSON 字符串，json.loads() 读回。配文件对象用 dump/load。让程序重启后数据仍在。'),
    ('PEP 8 风格', '官方风格指南：4 空格缩进（别混 Tab）、每行 ≤79 字符、类用 CamelCase、变量小写下划线、import 放文件开头。\"代码被阅读的次数远多于书写的次数\"。'),
]

py_questions = [
    ("Python 中 `5 // 2` 的结果是", ["A. 2", "B. 2.5", "C. 3", "D. 2.0"], 0, "// 是整除（地板除），5//2=2，结果永远是整数。"),
    ("Python 中 `5 % 2` 的结果是", ["A. 1", "B. 2", "C. 2.5", "D. 0"], 0, "% 是取余运算符，5 除以 2 余 1。常用于判断奇偶：x%2==0 为偶数。"),
    ("`2 ** 3` 的值是", ["A. 6", "B. 8", "C. 9", "D. 5"], 1, "** 是幂运算，2 的 3 次方 = 8。"),
    ("下列哪个是合法的变量名？", ["A. 2name", "B. my-name", "C. name_1", "D. for"], 2, "变量名不能以数字开头、不能含连字符（-）、不能是关键字（for）。name_1 合法。"),
    ("`type(3.14)` 返回", ["A. int", "B. float", "C. str", "D. bool"], 1, "3.14 带小数点，是 float（浮点型）。"),
    ("`\"Ada Lovelace\".title()` 的结果是", ["A. Ada Lovelace", "B. ada lovelace", "C. ADA LOVELACE", "D. Ada lovelace"], 0, "title() 把每个单词首字母大写 → Ada Lovelace。"),
    ("`[1,2,3][1]` 的值是", ["A. 1", "B. 3", "C. 0", "D. 2"], 3, "列表索引从 0 开始，[1] 取第 2 个元素 = 2。"),
    ("`[1,2,3,4,5][-1]` 的值是", ["A. 1", "B. 5", "C. 4", "D. 报错"], 1, "-1 永远返回最后一个元素 = 5。"),
    ("`{\"name\":\"赵立\"}[\"name\"]` 的值是", ["A. 赵立", "B. name", "C. 报错", "D. None"], 0, "字典用键取值，d[\"name\"] = \"赵立\"。"),
    ("`{\"a\":1}.get(\"b\", 99)` 的值是", ["A. 1", "B. 报错", "C. 99", "D. None"], 2, "get() 第二个参数是键不存在时的默认值；省略则返回 None。"),
    ("`for i in range(3):` 会循环几次？", ["A. 2 次", "B. 3 次", "C. 4 次", "D. 1 次"], 1, "range(3) 生成 0,1,2 共 3 次。range(1,5) 含头不含尾 → 1,2,3,4。"),
    ("`[x**2 for x in range(1,4)]` 的结果是", ["A. [1,4,9]", "B. [1,2,3]", "C. [1,4,9,16]", "D. [2,4,6]"], 0, "列表解析：x 取 1,2,3，x**2 → [1,4,9]。"),
    ("函数定义的关键字是", ["A. function", "B. func", "C. def", "D. define"], 2, "Python 用 def 定义函数。"),
    ("`def f(a, b=10):` 中 b=10 是", ["A. 默认值参数", "B. 位置实参", "C. 关键字实参", "D. 返回值"], 0, "b=10 是默认值参数，调用不传 b 时自动用 10；默认值参数必须放最后。"),
    ("`\"ab\" * 3` 的结果是", ["A. ababab", "B. ab3", "C. 报错", "D. aabb"], 0, "字符串乘整数表示重复拼接：ab 重复 3 次 = ababab。"),
    ("下列哪个判断语句写法正确？", ["A. if x = 5:", "B. if x == 5:", "C. if (x = 5)", "D. if x equals 5"], 1, "== 是比较，= 是赋值。if 后必须冒号。"),
    ("`input()` 返回的值总是", ["A. 字符串", "B. 整数", "C. 浮点数", "D. 布尔值"], 0, "input() 永远返回字符串！要数值必须 int()/float() 转换，否则比较会 TypeError。"),
    ("第3版教材读取文件的推荐方式是", ["A. pathlib.Path + read_text()", "B. open() + read()", "C. 文件对象 + for", "D. with open() as f"], 0, "第3版改用 pathlib：path=Path('a.txt'); contents=path.read_text()。open/with 是第2版写法。"),
    ("`try:` 块中应该放", ["A. 只可能出错的那一行", "B. 整个程序", "C. 所有 print", "D. 什么都行"], 0, "try 只放可能引发异常的行，else 放依赖 try 成功的代码。"),
    ("`from pizza import *` 为什么不推荐？", ["A. 可能覆盖同名函数", "B. 太慢", "C. 会报错", "D. 不能导入"], 0, "导入全部函数可能覆盖当前文件中的同名函数，应优先用 import pizza 或精确导入。"),
]

py_flashcards = [
    ("变量是标签", "变量贴在值上，不是盒子。拼写不一致→NameError，Python 不做拼写检查只要求一致。"),
    ("字符串方法", "title/upper/lower、strip/lstrip/rstrip（要重新赋值才永久）、removeprefix/removesuffix。含撇号用双引号。"),
    ("f-string", "f\"Hello, {name}!\"。忘记 f 前缀→花括号原样输出。"),
    ("浮点精度", "0.2+0.1=0.30000000000000004。所有语言共有，不是 bug。4/2=2.0（真除总返回浮点）。"),
    ("列表操作", "索引从0，-1 取尾。append/pop/del/remove、sort/sorted/reverse、len。索引越界→IndexError。"),
    ("切片与复制", "players[0:3] 含头不含尾；[:] 复制得到独立列表；直接 = 是同一列表两个名字。"),
    ("字典 get()", "d[\"k\"] 不存在→KeyError；d.get(\"k\",默认) 安全；省略默认返回 None。"),
    ("*args/**kwargs", "*args 收任意数量实参成元组，**kwargs 收关键字实参成字典；必须放参数最后。"),
    ("pathlib 读写", "path=Path('a.txt'); read_text() 读、write_text() 写（覆盖！）。第3版标准方式。"),
    ("try-except-else", "try 只放可能出错行，except 捕获错误，else 放依赖成功的结果。pass 静默失败。"),
]

py_errors = [
    ("缩进错误", "代码块不缩进或缩进不一致。", "Python 用缩进（4空格）表示代码块，缩进错误→IndentationError。统一 4 空格，别混 Tab。"),
    ("== 与 = 混淆", "if 条件里用 = 赋值。", "== 是比较是否相等；= 是赋值。判断时用 if x == 5:。"),
    ("索引从 1 开始", "以为 lst[1] 是第一个元素。", "索引从 0 开始：lst[0] 第一个、lst[-1] 最后一个。range(1,5) 也是含头不含尾。"),
    ("input() 忘转换", "把 input() 的结果直接当数字比较。", "input() 永远返回字符串，int()/float() 转换后才能做数值运算，否则 TypeError。"),
    ("复制列表用 =", "friend_foods = my_foods 想复制列表。", "直接 = 只是两个名字指向同一列表，互相影响。要用切片 my_foods[:] 得到独立副本。"),
    ("可变默认参数", "def add(item, lst=[]) 用列表做默认值。", "默认值只创建一次会被多次调用共享累积。应改用 None 占位：def add(item, lst=None)。"),
    ("单引号内撇号", "message = 'One of Python's...' 报错。", "单引号字符串里写撇号→SyntaxError。用双引号包住含撇号的字符串。"),
    ("f-string 忘 f", "f\"{name}\" 少了 f 前缀。", "忘记 f 前缀花括号会原样输出，不会替换成变量值。"),
]

# ================= Python 进阶页(教材 Ch8-11: 类/模块/文件/测试) =================
adv_knowledge = [
    ('类与实例', 'class 定义模板，__init__() 创建实例时自动运行初始化属性，self 指向实例本身（第一个参数自动传入）。my_dog = Dog("Willie", 6) 创建实例，点号访问属性和调用方法。'),
    ('修改属性 3 种方式', '① 直接赋值：my_car.odometer=23；② 通过方法改（可加校验，如拒绝回拨里程）；③ 通过方法递增：increment_odometer(miles)。'),
    ('继承 Inheritance', '子类 class ElectricCar(Car):，__init__ 里 super().__init__(...) 继承父类属性。可添加专属属性、重写父类方法。父类必须定义在子类之前。'),
    ('组合 Composition', '实例作为另一个类的属性，把复杂类拆成小类。例：Battery 类作为 ElectricCar 的属性 self.battery = Battery()。继承 vs 组合：\"是一个\"用继承，\"有一个\"用组合。'),
    ('模块导入', '模块=存类/函数的 .py 文件。from car import Car、from car import Car, ElectricCar、import car 用 car.Car。标准库：import random 用 random.choice/randint。'),
    ('pathlib 文件操作', 'path=Path("pi.txt")；read_text() 读整文件、splitlines() 逐行；write_text() 写（覆盖）。读出的都是字符串，数值要转换。路径用正斜杠 /，Windows 自动转换。'),
    ('异常 try-except-else', '捕获 ZeroDivisionError/FileNotFoundError 防崩溃。try 只放可能出错行，else 放依赖成功结果。pass 静默失败。别用裸 except 吞掉所有错误。'),
    ('JSON 持久化', 'json.dumps() 对象→JSON 字符串存文件，json.loads() 读回。dump/load 配文件对象，dumps/loads 配字符串。让程序重启后数据仍在。'),
    ('pytest 测试', '测试文件 test_ 开头，函数 test_ 开头，用 assert 断言。pytest 自动发现运行。例：def test_f(): assert add(2,3)==5。失败改代码不改测试。fixture 提供共享数据。'),
    ('Django MVT', 'Model(数据)→View(逻辑)→Template(展示) 三层分离，URL 负责路由。URL 找视图，视图取模型，模板画页面。Django 的 View ≈ MVC 的 Controller。'),
]

adv_questions = [
    ("类中 `__init__` 方法的作用是", ["A. 创建实例时自动初始化属性", "B. 删除实例", "C. 打印信息", "D. 导入模块"], 0, "__init__ 是特殊方法（两侧各两个下划线），创建实例时自动调用，self.name=name 绑定实例属性。"),
    ("`self` 在类方法中的作用是", ["A. 指向实例本身", "B. 指向类", "C. 指向模块", "D. 无作用"], 0, "self 必须是方法第一个参数，自动传入，指向当前实例。"),
    ("子类继承父类，`__init__` 中调用父类初始化的方法是", ["A. super().__init__()", "B. parent.init()", "C. self.parent()", "D. base().__init__()"], 0, "super().__init__(...) 调用父类初始化方法，继承父类全部属性。"),
    ("`def add(item, lst=[])` 有什么问题？", ["A. 默认列表被多次调用共享累积", "B. 语法错误", "C. 不能传参", "D. 没问题"], 0, "可变默认参数陷阱：默认值只创建一次，多次调用共享累积。应改用 None 占位。"),
    ("测试文件与测试函数的命名规范是", ["A. test_ 开头", "B. 任意命名", "C. 大写开头", "D. 数字开头"], 0, "pytest 自动发现 test_ 开头的文件和函数。断言用 assert。"),
    ("`json.dumps()` 的作用是", ["A. Python对象→JSON字符串", "B. JSON→对象", "C. 打印JSON", "D. 删除JSON"], 0, "dumps = 导出（对象→字符串）；loads = 加载（字符串→对象）。dump/load 配文件对象。"),
    ("pathlib 中读取整个文件的方法是", ["A. path.read_text()", "B. open(path)", "C. path.read()", "D. path.load()"], 0, "第3版标准：path=Path('a.txt'); contents=path.read_text()。"),
    ("`write_text()` 对已存在文件的行为是", ["A. 先清空再覆盖", "B. 追加", "C. 报错", "D. 跳过"], 0, "write_text() 文件已存在时先清空原内容再写（覆盖！）。"),
    ("Django 中 MVT 的 V 指的是", ["A. View 视图(逻辑)", "B. Value 值", "C. Variable 变量", "D. Vector 向量"], 0, "MVT：Model(数据)→View(逻辑)→Template(展示)。URL 路由。"),
    ("异常处理中 `except: pass` 表示", ["A. 静默失败，程序继续", "B. 崩溃", "C. 报错", "D. 重试"], 0, "pass 表示什么都不做，程序继续运行。但裸 except 会吞掉所有错误包括自己的 bug。"),
]

adv_flashcards = [
    ("类和实例", "class Dog: 定义；__init__ 初始化；self 指向实例；my_dog=Dog('Willie',6) 创建；点号访问。"),
    ("继承", "class ElectricCar(Car): super().__init__(...)。可加属性、重写方法。"),
    ("组合", "实例作为属性：self.battery = Battery()。\"有一个\"用组合，\"是一个\"用继承。"),
    ("pathlib", "Path('a.txt').read_text() 读、write_text() 写(覆盖)。splitlines() 逐行。"),
    ("JSON", "dumps 导出(对象→字符串)、loads 加载(字符串→对象)；dump/load 配文件。"),
    ("pytest", "test_ 命名 + assert 断言。失败改代码不改测试。fixture 共享数据。"),
    ("Django MVT", "Model 数据 / View 逻辑 / Template 展示；URL 路由。"),
]

adv_errors = [
    ("忘写 __init__", "类没有 __init__，实例无法初始化属性。", "需要初始化属性就定义 __init__，创建实例时自动调用。"),
    ("self 漏掉", "类方法定义时忘了 self 参数。", "self 必须是类方法第一个参数，虽然调用时不传。"),
    ("可变默认参数", "def f(lst=[]) 共享累积。", "改用 None 占位：def f(lst=None): if lst is None: lst=[]。"),
    ("write_text 覆盖", "以为 write_text 是追加。", "write_text() 会先清空再写。追加要先把原内容读出拼好再写。"),
    ("裸 except", "except: 吞掉所有错误。", "指定异常类型 except FileNotFoundError: 或 except Exception as e: 打印错误。"),
]

# ================= 数据可视化与 API 页(教材 Ch15-17) =================
viz_knowledge = [
    ('matplotlib 基础', 'import matplotlib.pyplot as plt；fig, ax = plt.subplots()；ax.plot(x, y) 折线、ax.scatter(x, y) 散点；plt.show() 显示。fig=整个图，ax=子图。'),
    ('图表定制', 'ax.set_title/set_xlabel/set_ylabel；ax.tick_params(labelsize=14)；plt.style.use("seaborn") 内置样式；ax.axis([xmin,xmax,ymin,ymax]) 设范围。'),
    ('plot() 易错点', '只传一个序列时假设 x 从 0 开始。数据起点是 x=1 时要显式传 input_values：ax.plot(input_values, squares)。'),
    ('散点与 colormap', 'scatter(x, y, s=10) 画点，s 是大小。colormap 强调数据模式：ax.scatter(x, y, c=y_values, cmap=plt.cm.Blues)。注意 c 不是 color！'),
    ('随机漫步 RandomWalk', '纯随机决策的路径。用 random.choice() 做决策：方向×距离=步长，x_step==0 且 y_step==0 时 continue 跳过。ax.set_aspect("equal") 保持形状真实。'),
    ('Plotly Express', '交互式浏览器图表。pip install plotly pandas。px.bar(x=..., y=...) 两行出图，fig.show() 渲染 HTML。px.scatter_geo() 世界地图。'),
    ('CSV 数据处理', 'csv.reader 解析 CSV；datetime.strptime() 解析日期；try-except-else 处理缺失数据。先看表头结构再处理。'),
    ('API 调用', 'requests.get(url) 发起请求；检查 status_code==200；r.json() 解析响应为 Python 字典。GitHub API: api.github.com/search/repositories?q=language:python+sort:stars。'),
    ('API 嵌套取值', 'repo_dict["owner"]["login"] 多级取值，任意一级键名错→KeyError。用 try-except 跳过异常帖子。'),
    ('API 限流', 'GitHub 搜索 API 未认证约 10 次/分钟。访问 api.github.com/rate_limit 查看。很多 API 需要注册获取 API key。'),
    ('Django 入门', 'python -m venv 创建虚拟环境隔离包；django-admin startproject 建项目；models.py 定义模型；makemigrations/migrate 迁移建表；startapp 建应用。'),
    ('Django 模板', '定义 URL → 编写视图 → 编写模板 三步法。模板继承 base.html 复用布局。ModelForm 处理表单，@login_required 限制登录用户。'),
]

viz_questions = [
    ("matplotlib 中创建图形和子图的标准写法是", ["A. fig, ax = plt.subplots()", "B. plt.figure()", "C. ax = plt.plot()", "D. fig = plt.ax()"], 0, "subplots() 返回 fig(整个图) 和 ax(子图)，是自定义图表最常用的方式。"),
    ("plot() 只传一个列表时，x 轴假设从几开始？", ["A. 0", "B. 1", "C. 2", "D. -1"], 0, "只传一个序列时假设第一个数据点 x=0；起点是 x=1 时要显式传 input_values。"),
    ("scatter() 中用于颜色映射的参数是", ["A. c", "B. color", "C. cmap 单独", "D. s"], 0, "c 关联值序列与 colormap；color 是单一颜色。cmap 指定具体色图。"),
    ("Plotly Express 出交互图需要先安装", ["A. plotly 和 pandas", "B. 只 plotly", "C. matplotlib", "D. Django"], 0, "Plotly Express 依赖 pandas，需一并安装：pip install plotly pandas。"),
    ("随机漫步中 `x_step==0 and y_step==0` 时应该", ["A. continue 跳过", "B. break 退出", "C. pass 继续", "D. 报错"], 0, "两个方向都原地踏步就 continue 跳过，避免重复点。"),
    ("requests 调用 API 后先检查什么？", ["A. status_code==200", "B. 返回长度", "C. 响应时间", "D. 什么也不检查"], 0, "必须先检查 status_code==200 再 r.json()，否则 4xx/5xx 时结构不是预期。"),
    ("`r.json()` 把 API 响应转成", ["A. Python 字典/列表", "B. 字符串", "C. JSON 文件", "D. 图片"], 0, "r.json() 把 JSON 响应解析为 Python 数据结构（GitHub 返回字典，HN 返回列表）。"),
    ("GitHub 搜索 API 未认证的限流约为", ["A. 10次/分钟", "B. 100次/分钟", "C. 无限", "D. 1次/天"], 0, "GitHub 搜索 API 未认证约 10 次/分钟；获取令牌后限额大幅提高。"),
    ("Django 中创建虚拟环境的命令是", ["A. python -m venv ll_env", "B. pip install django", "C. django-admin startproject", "D. python manage.py runserver"], 0, "venv 创建隔离环境，激活后安装包不影响系统。ll_env 是两小写 L。"),
    ("`repo_dict['owner']['login']` 中 owner 是", ["A. 嵌套字典", "B. 列表", "C. 字符串", "D. 数字"], 0, "owner 键的值是另一个字典，需二级取值。任意一级键名错→KeyError。"),
]

viz_flashcards = [
    ("matplotlib 套路", "subplots() → plot/scatter → set_title/labels → plt.show()。样式：plt.style.use('seaborn')。"),
    ("plot 单序列坑", "只传一个序列从 x=0 开始；起点 x=1 显式传 input_values。"),
    ("随机漫步", "choice() 决策；x_step=0 且 y_step=0 时 continue；set_aspect('equal')。"),
    ("Plotly", "pip install plotly pandas；px.bar/scatter_geo；fig.show() 交互。"),
    ("CSV", "csv.reader + datetime.strptime + try-except-else；先看表头。"),
    ("API 三步", "requests.get(url) → 检查 status_code==200 → r.json() 解析。"),
    ("Django 三步", "定义 URL → 编写视图 → 编写模板。MVT：Model/View/Template。"),
]

viz_errors = [
    ("不检查 status_code", "请求失败还继续 r.json()。", "必须先断言 status_code==200，4xx/5xx 时响应结构不是预期。"),
    ("colormap 用 color", "scatter 里用 color 做颜色映射。", "c 关联值序列与 colormap，color 是单一颜色。cmap 指定色图。"),
    ("嵌套 KeyError", "repo_dict['owner']['login'] 某级键名错。", "多级取值用 try-except 跳过特殊数据，或先 print(keys()) 确认结构。"),
    ("忘了 API 限流", "循环请求太多触发限流。", "GitHub 搜索约 10次/分钟。先查 rate_limit，注意 incomplete_results 标志。"),
    ("Matplotlib 中文方框", "标题含中文显示为方框。", "默认字体不含中文字形，需配置中文字体或用英文标签。"),
]

# ================= 生成三个页面 =================
n1 = build_page('python_basics_interactive.html', 'Python 基础语法', 'Python 编程 · 第1讲', 'zhaoli_python', py_knowledge, py_questions, py_flashcards, py_errors, color='#667eea')
n2 = build_page('python_advanced_interactive.html', 'Python 进阶：类/文件/测试', 'Python 编程 · 第2讲', 'zhaoli_python_adv', adv_knowledge, adv_questions, adv_flashcards, adv_errors, color='#3498db')
n3 = build_page('ai_dataviz_interactive.html', '数据可视化与 API', 'AI 应用 · 第2讲', 'zhaoli_ai_viz', viz_knowledge, viz_questions, viz_flashcards, viz_errors, color='#e67e22')

print(f"python_basics_interactive.html: {n1} 字节")
print(f"python_advanced_interactive.html: {n2} 字节")
print(f"ai_dataviz_interactive.html: {n3} 字节")

# JS 验证
for f in ['python_basics_interactive.html', 'python_advanced_interactive.html', 'ai_dataviz_interactive.html']:
    r = subprocess.run(["node", "-e", f"""
const fs=require('fs');const html=fs.readFileSync('{f}','utf8');
const re=/<script[^>]*>([\\s\\S]*?)<\\/script>/g;let m,ok=true;
while((m=re.exec(html))){{try{{new Function(m[1])}}catch(e){{ok=false;console.log('ERR:',e.message)}}}}
console.log('{f}:',ok?'JS OK':'JS FAIL');
"""], capture_output=True, text=True)
    print(r.stdout.strip() or r.stderr[:300])
