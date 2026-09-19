#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""从 review_data.json 生成复习模块：
   1) review/<slug>.html  —— 每题一个独立页面
   2) review_interactive.html —— 索引页（分学科 + 搜索 → 点击进单题页）
"""
import json, os, html, re

REPO = '/home/administrator/xuci-jiancha'
DATA_FILE = os.path.join(REPO, 'review_data.json')
OUT_DIR = os.path.join(REPO, 'review')
os.makedirs(OUT_DIR, exist_ok=True)

SUBJ_SLUG = {'数学':'math','语文':'chinese','英语':'english','物理':'physics',
             '化学':'chem','生物':'bio','历史':'hist','地理':'geo','道法':'pol'}

with open(DATA_FILE, encoding='utf-8') as f:
    DATA = json.load(f)

def esc(s): return html.escape(str(s), quote=True)

def slug_of(q, idx):
    sub = SUBJ_SLUG.get(q['subj'], 'x')
    num = re.sub(r'[^0-9]', '', q.get('num', '')) or str(idx + 1)
    return f"{sub}_{num}"

# ---------- 单题页 ----------
PAGE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>__TITLE__ · 复习模块</title>
<style>
  *{box-sizing:border-box}
  body{margin:0;font-family:-apple-system,BlinkMacSystemFont,"PingFang SC","Microsoft YaHei",sans-serif;
       background:#f4f6fb;color:#1f2937;line-height:1.75}
  .wrap{max-width:860px;margin:0 auto;padding:1rem 1rem 3rem}
  .back{display:inline-block;color:#2f6fed;text-decoration:none;font-size:.88rem;margin-bottom:.7rem}
  .back:hover{text-decoration:underline}
  .hero{background:linear-gradient(135deg,#2f6fed,#5f3dc4);color:#fff;border-radius:16px;padding:1.2rem 1.2rem;margin-bottom:1rem}
  .hero .crumb{font-size:.8rem;opacity:.9;margin-bottom:.3rem}
  .hero h1{margin:0;font-size:1.2rem;line-height:1.45}
  .hero .meta{margin-top:.5rem;font-size:.78rem;opacity:.85}
  .card{background:#fff;border-radius:14px;padding:1rem 1.1rem;margin-bottom:1rem;box-shadow:0 2px 10px rgba(31,41,55,.06)}
  h2{font-size:1rem;margin:0 0 .6rem;color:#3b4cca}
  .stem{background:#fafbff;border-left:3px solid #2f6fed;border-radius:8px;padding:.65rem .85rem;
        font-size:.94rem;white-space:pre-wrap;margin-bottom:.7rem}
  .q-img{width:100%;max-width:440px;border-radius:10px;border:1px solid #eef1f8;cursor:zoom-in;display:block}
  .dim{border-radius:10px;padding:.6rem .85rem;margin-bottom:.55rem;font-size:.93rem}
  .dim .k{font-weight:700;font-size:.87rem;display:block;margin-bottom:.2rem}
  .dim p{margin:0;white-space:pre-wrap}
  .dim.A{background:#eef7ff;border:1px solid #d3e8ff}.dim.A .k{color:#1a6bb8}
  .dim.B{background:#eefaf3;border:1px solid #c7eeda}.dim.B .k{color:#0b6b3a}
  .dim.C{background:#fff8e8;border:1px solid #ffe6b3}.dim.C .k{color:#a5720a}
  .dim.D{background:#fff2f2;border:1px solid #ffd6d6}.dim.D .k{color:#b02a2a}
  .dim.E{background:#f6f0ff;border:1px solid #e3d5ff}.dim.E .k{color:#6b3fc4}
  .nav{display:flex;justify-content:space-between;gap:.6rem;margin-top:1.2rem;flex-wrap:wrap}
  .nav a{background:#fff;border:1px solid #e3e8f2;border-radius:10px;padding:.5rem .9rem;text-decoration:none;
         color:#374151;font-size:.87rem;max-width:47%}
  .nav a:hover{border-color:#2f6fed;color:#2f6fed}
  .nav a.dis{opacity:.35;pointer-events:none}
  #lightbox{display:none;position:fixed;inset:0;background:rgba(15,20,35,.9);z-index:99;
            align-items:center;justify-content:center;padding:1rem}
  #lightbox.on{display:flex}
  #lightbox img{max-width:100%;max-height:92vh;border-radius:10px}
  footer{text-align:center;color:#9aa3b2;font-size:.78rem;margin-top:1.5rem}
  @media print{.back,.nav,footer{display:none}.card{box-shadow:none;border:1px solid #ddd}}
</style>
</head>
<body>
<div class="wrap">
  <a class="back" href="../review_interactive.html">← 返回题目列表</a>
  <div class="hero">
    <div class="crumb">__CRUMB__</div>
    <h1>__TOPIC__</h1>
    <div class="meta">来源：__DATE__ ｜ 赵若琳学习中心 · 复习模块</div>
  </div>

  <div class="card">
    <h2>题目</h2>
    <div class="stem">__STEM__</div>
    __IMG__
  </div>

  <div class="card">
    <h2>五维分析</h2>
    __DIMS__
  </div>

  <div class="nav">__NAV__</div>
  <footer>赵若琳学习中心 · 复习模块</footer>
</div>
<div id="lightbox" onclick="this.classList.remove('on')"><img id="lb" src="" alt="题目图片"></div>
<script>
document.querySelectorAll('.q-img').forEach(function(im){
  im.onclick = function(){ document.getElementById('lb').src = im.src;
                           document.getElementById('lightbox').classList.add('on'); };
});
</script>
</body>
</html>
"""

DIM_LABEL = {'known':('A','已知条件'), 'ask':('B','求解什么'), 'method':('C','做题思路'),
             'pitfall':('D','易错点'), 'points':('E','知识点')}

slugs = [slug_of(q, i) for i, q in enumerate(DATA)]
titles = [f"{q['subj']}{q['num']}" for q in DATA]

for i, q in enumerate(DATA):
    dims = ''
    for key, (k, label) in DIM_LABEL.items():
        if q.get(key):
            dims += f'<div class="dim {k}"><span class="k">{k}　{label}</span><p>{esc(q[key])}</p></div>\n    '
    img = ''
    if q.get('img'):
        img = f'<img class="q-img" src="../{esc(q["img"])}" alt="{esc(q["subj"])}{esc(q["num"])}题目图片">'
    nav = ''
    if i > 0:
        nav += f'<a href="{slugs[i-1]}.html">← 上一题：{esc(titles[i-1])}</a>'
    else:
        nav += '<a class="dis">← 已是第一题</a>'
    if i < len(DATA) - 1:
        nav += f'<a href="{slugs[i+1]}.html">下一题：{esc(titles[i+1])} →</a>'
    else:
        nav += '<a class="dis">已是最后一题 →</a>'

    page = (PAGE.replace('__TITLE__', esc(q['subj']) + esc(q['num']))
                .replace('__CRUMB__', esc(q['subj']) + ' · ' + esc(q['num']))
                .replace('__TOPIC__', esc(q.get('topic', '')))
                .replace('__DATE__', esc(q.get('date', '')))
                .replace('__STEM__', esc(q['stem']))
                .replace('__IMG__', img)
                .replace('__DIMS__', dims)
                .replace('__NAV__', nav))
    with open(os.path.join(OUT_DIR, slugs[i] + '.html'), 'w', encoding='utf-8') as f:
        f.write(page)
print('单题页生成:', len(DATA), '个 ->', OUT_DIR)

# ---------- 索引页 ----------
subjects = []
for q in DATA:
    if q['subj'] not in subjects:
        subjects.append(q['subj'])

cards = []
for i, q in enumerate(DATA):
    excerpt = re.sub(r'\s+', ' ', q['stem'])[:88]
    cards.append({
        'subj': q['subj'], 'num': q['num'], 'topic': q.get('topic', ''),
        'date': q.get('date', ''), 'url': f"review/{slugs[i]}.html",
        'excerpt': excerpt, 'key': (q['subj'] + q['num'] + q.get('topic', '') + q['stem']).lower()
    })

INDEX = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>复习模块 · 赵若琳学习中心</title>
<style>
  *{box-sizing:border-box}
  body{margin:0;font-family:-apple-system,BlinkMacSystemFont,"PingFang SC","Microsoft YaHei",sans-serif;
       background:#f4f6fb;color:#1f2937;line-height:1.7}
  .wrap{max-width:900px;margin:0 auto;padding:1rem 1rem 3rem}
  .hero{background:linear-gradient(135deg,#2f6fed,#5f3dc4);color:#fff;border-radius:16px;padding:1.3rem 1.2rem;margin-bottom:1rem}
  .hero h1{margin:0 0 .35rem;font-size:1.3rem}
  .hero p{margin:0;font-size:.86rem;opacity:.92}
  .toolbar{display:flex;gap:.5rem;flex-wrap:wrap;align-items:center;margin-bottom:.8rem}
  .tab{background:#fff;border:1px solid #e3e8f2;border-radius:999px;padding:.4rem .95rem;font-size:.88rem;
       cursor:pointer;color:#374151;user-select:none}
  .tab.on{background:#2f6fed;border-color:#2f6fed;color:#fff;font-weight:600}
  .tab .cnt{opacity:.7;font-size:.78rem;margin-left:.25rem}
  input.search{flex:1;min-width:150px;border:1px solid #e3e8f2;border-radius:10px;padding:.45rem .8rem;font-size:.9rem;outline:none}
  input.search:focus{border-color:#2f6fed}
  .stat{color:#6b7280;font-size:.85rem;margin:.2rem 0 .9rem}
  .grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(255px,1fr));gap:.8rem}
  .q-card{background:#fff;border-radius:14px;padding:.9rem 1rem;text-decoration:none;color:inherit;
          box-shadow:0 2px 10px rgba(31,41,55,.06);display:flex;flex-direction:column;transition:.15s;border:1px solid transparent}
  .q-card:hover{transform:translateY(-2px);border-color:#c9d6f5;box-shadow:0 6px 16px rgba(47,111,237,.13)}
  .q-card .top{display:flex;align-items:center;gap:.45rem;margin-bottom:.4rem;flex-wrap:wrap}
  .q-card .subj{background:#e8efff;color:#2f6fed;font-weight:700;font-size:.76rem;border-radius:7px;padding:.12rem .45rem}
  .q-card .num{font-weight:700;font-size:.92rem}
  .q-card .date{margin-left:auto;color:#9aa3b2;font-size:.74rem}
  .q-card .topic{color:#5f3dc4;font-size:.82rem;margin-bottom:.35rem}
  .q-card .ex{color:#6b7280;font-size:.83rem;flex:1}
  .q-card .go{color:#2f6fed;font-size:.82rem;font-weight:600;margin-top:.5rem}
  .empty{text-align:center;color:#9aa3b2;padding:2rem;font-size:.92rem}
  .tip{background:#f0f4ff;border:1px dashed #b9c6e8;border-radius:10px;padding:.7rem .9rem;font-size:.85rem;color:#41507a;margin-bottom:1rem}
  footer{text-align:center;color:#9aa3b2;font-size:.78rem;margin-top:1.6rem}
</style>
</head>
<body>
<div class="wrap">
  <div class="hero">
    <h1>📖 复习模块 · 作业题精析</h1>
    <p>点开任一题进入<b>独立页面</b>：A 已知条件 · B 求解什么 · C 做题思路 · D 易错点 · E 知识点</p>
  </div>
  <div class="tip">💡 先自己读题做一遍 → 再对照 C 思路 → 重点记 D 易错点。新作业会陆续按同样格式补入。</div>
  <div class="toolbar">
    <div id="tabs" style="display:flex;gap:.5rem;flex-wrap:wrap"></div>
    <input class="search" id="q" placeholder="🔍 搜索关键词（题号/考点/公式）">
  </div>
  <div class="stat" id="stat"></div>
  <div class="grid" id="list"></div>
  <footer>赵若琳学习中心 · 复习模块</footer>
</div>
<script>
const CARDS = __CARDS__;
const SUBJECTS = __SUBJECTS__;
let curSubj = '全部', curKw = '';
function renderTabs(){
  const items = [['全部', CARDS.length]].concat(SUBJECTS.map(s => [s, CARDS.filter(c => c.subj === s).length]));
  const tabs = document.getElementById('tabs');
  tabs.innerHTML = items.map(function(it){
    return '<div class="tab' + (it[0] === curSubj ? ' on' : '') + '" data-s="' + it[0] + '">' + it[0] +
           '<span class="cnt">' + it[1] + '</span></div>';
  }).join('');
  tabs.querySelectorAll('.tab').forEach(function(t){
    t.onclick = function(){ curSubj = t.dataset.s; renderTabs(); renderList(); };
  });
}
function renderList(){
  let list = CARDS.filter(function(c){ return curSubj === '全部' || c.subj === curSubj; });
  if(curKw) list = list.filter(function(c){ return c.key.indexOf(curKw) >= 0; });
  document.getElementById('stat').textContent = '共 ' + list.length + ' 道题' + (curKw ? '（关键词：' + curKw + '）' : '');
  const box = document.getElementById('list');
  if(!list.length){ box.innerHTML = '<div class="empty">没有匹配的题目</div>'; return; }
  box.innerHTML = list.map(function(c){
    return '<a class="q-card" href="' + c.url + '">' +
      '<div class="top"><span class="subj">' + c.subj + '</span><span class="num">' + c.num + '</span>' +
      '<span class="date">' + c.date + '</span></div>' +
      '<div class="topic">' + c.topic + '</div>' +
      '<div class="ex">' + c.excerpt + '…</div>' +
      '<div class="go">查看详解 →</div></a>';
  }).join('');
}
document.getElementById('q').addEventListener('input', function(e){ curKw = e.target.value.trim().toLowerCase(); renderList(); });
renderTabs(); renderList();
</script>
</body>
</html>
"""

idx = (INDEX.replace('__CARDS__', json.dumps(cards, ensure_ascii=False, indent=1))
            .replace('__SUBJECTS__', json.dumps(subjects, ensure_ascii=False)))
with open(os.path.join(REPO, 'review_interactive.html'), 'w', encoding='utf-8') as f:
    f.write(idx)
print('索引页生成: review_interactive.html')
print('题目 slug:', ', '.join(slugs))
