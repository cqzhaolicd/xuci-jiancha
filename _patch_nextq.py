#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""富模板(38页)补齐 nextQ/prevQ/showResult —— 修复"点下一题无反应"(ReferenceError)。
插入锚点: function renderQ(){ (每页1次)。已有定义的页跳过。"""
import glob

NEW_FNS = """function prevQ(){if(curQ>0){curQ--;renderQ();}}
function nextQ(){const total=retryMode?shuffled.length:questions.length;if(curQ<total-1){curQ++;renderQ();}else showResult();}
function showResult(){const p=getQuizProg();let ok=0,done=0;Object.keys(p||{}).forEach(function(k){if(p[k].s==='ok'&&(p[k].r||0)>=3)ok++;});for(let i=0;i<quizAns.length;i++){if(quizAns[i]>=0)done++;}let h='<div class="question-card result-card fade-in-up" style="text-align:center;padding:2rem"><div style="font-size:2.6rem">🎉</div><h2>本组答题完成</h2><p style="color:var(--text-light)">本次已完成 '+done+' 题 · 连续做对3次已合格 '+ok+' 题</p><div style="margin-top:1rem;display:flex;gap:.6rem;justify-content:center;flex-wrap:wrap"><button class="btn btn-outline" onclick="setQuizMode(&#39;all&#39;)">📋 继续练习全部</button><button class="btn btn-primary" onclick="initRetryMode()">🔁 错题重练</button></div></div>';document.getElementById('quizArea').innerHTML=h;}
"""

files = [f for f in glob.glob('*.html') if 'markRedoOk' in open(f, encoding='utf-8').read()]
ok = 0
for fn in files:
    h = open(fn, encoding='utf-8').read()
    if 'function nextQ' in h:
        print(f'SKIP(已有): {fn}')
        continue
    anchor = 'function renderQ(){'
    n = h.count(anchor)
    if n != 1:
        print(f'异常锚点 {fn}: {n}')
        continue
    h = h.replace(anchor, NEW_FNS + anchor, 1)
    open(fn, 'w', encoding='utf-8').write(h)
    ok += 1
print(f'补齐 {ok}/{len(files)} 页')
