#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""由 wrong_bank.html 派生独立页 ai_wrongbook.html（AI错题本）。

为什么用生成脚本而不是手工复制：
  ai_wrongbook.html 与 wrong_bank.html 共用同一套数据层 / 渲染函数 / 云同步，
  上游修 bug 或加字段时，只需重跑本脚本，两边不会漂移。

用法: python3 _build_ai_wrongbook.py
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, 'wrong_bank.html')
DST = os.path.join(ROOT, 'ai_wrongbook.html')

CSS = """/* ===== AI错题本 · 顶部双功能区（错题本 / 三层训练） ===== */
.top-tabs{display:flex;gap:.35rem;flex-wrap:wrap}
.top-tab{background:rgba(255,255,255,.16);color:#fff;border:1.5px solid rgba(255,255,255,.35);
  padding:.35rem .95rem;border-radius:999px;font-size:.85rem;font-weight:600;cursor:pointer;
  display:inline-flex;align-items:center;gap:.35rem;transition:all .2s;font-family:inherit}
.top-tab:hover{background:rgba(255,255,255,.3)}
.top-tab.active{background:#fff;color:var(--primary);border-color:#fff;box-shadow:0 2px 10px rgba(0,0,0,.18)}
#mainNav{border-top:1px solid rgba(255,255,255,.18);padding-top:.35rem}
.domain-tip{font-size:.76rem;color:var(--text-light);margin:-.4rem 0 .8rem}
@media(max-width:768px){.top-tab{font-size:.78rem;padding:.3rem .7rem}}
</style>"""

NAV_OLD = """<nav class="navbar"><div class="container">
  <a class="navbar-brand" href="#"><i class="fas fa-database"></i> 错题库</a>
  <div class="navbar-nav" id="mainNav">
    <a class="active" data-page="dashboard"><i class="fas fa-home"></i><span>首页</span></a>
    <a data-page="add"><i class="fas fa-plus-circle"></i><span>录入</span></a>
    <a data-page="list"><i class="fas fa-list"></i><span>错题本</span></a>
    <a data-page="review"><i class="fas fa-redo"></i><span>复习</span></a>
    <a data-page="training"><i class="fas fa-layer-group"></i><span>三层练</span></a>
    <a data-page="print-page"><i class="fas fa-print"></i><span>打印</span></a>
    <a data-page="analysis"><i class="fas fa-chart-pie"></i><span>分析</span></a>
  </div>
</div></nav>"""

NAV_NEW = """<nav class="navbar"><div class="container" style="flex-direction:column;align-items:stretch;gap:.45rem">
  <div style="display:flex;align-items:center;justify-content:space-between;gap:.5rem;flex-wrap:wrap">
    <a class="navbar-brand" href="index.html"><i class="fas fa-robot"></i> AI错题本</a>
    <div class="top-tabs" id="topTabs">
      <button class="top-tab active" data-top="notebook" onclick="switchTop('notebook')"><i class="fas fa-book"></i> 错题本</button>
      <button class="top-tab" data-top="training" onclick="switchTop('training')"><i class="fas fa-layer-group"></i> 三层训练</button>
    </div>
  </div>
  <div class="navbar-nav" id="mainNav">
    <a class="active" data-page="dashboard"><i class="fas fa-home"></i><span>首页</span></a>
    <a data-page="add"><i class="fas fa-plus-circle"></i><span>录入</span></a>
    <a data-page="list"><i class="fas fa-list"></i><span>错题本</span></a>
    <a data-page="review"><i class="fas fa-redo"></i><span>复习</span></a>
    <a data-page="print-page"><i class="fas fa-print"></i><span>打印</span></a>
    <a data-page="analysis"><i class="fas fa-chart-pie"></i><span>分析</span></a>
  </div>
</div></nav>"""

FOOTER_OLD = """<div class="footer"><i class="fas fa-heart" style="color:var(--danger)"></i> 错题库 · 浏览器本地存储 &nbsp;|&nbsp; 数据自动保存在本机</div>"""

FOOTER_NEW = """<div class="footer">
  <i class="fas fa-heart" style="color:var(--danger)"></i> AI错题本 · 收录「错题本」与「三层训练」两项功能
  &nbsp;|&nbsp; 数据与「错题库」共用同一份（本机存储 + 云端同步）
  &nbsp;|&nbsp; <a href="index.html" style="color:var(--primary)">返回学习中心</a>
</div>"""

JS_BLOCK = """// ===================== AI错题本 · 双功能区（错题本 / 三层训练） =====================
// 本页 = 把错题库里的「错题本」与「三层训练」两项功能单独成页。
// 数据层/渲染函数与原页完全同源；localStorage 键与云端后端也一致 ⇒ 两页数据互通：
// 在原错题库录入或复习的题，这里立刻可见；反之亦然。
let _aiLastNbPage = 'dashboard';
function _aiTopTabOf(page){ return page === 'training' ? 'training' : 'notebook'; }
function _aiApplyTopTab(page){
  const t = _aiTopTabOf(page);
  document.querySelectorAll('#topTabs .top-tab').forEach(b => b.classList.toggle('active', b.dataset.top === t));
  const mn = document.getElementById('mainNav');
  if (mn) mn.style.display = (t === 'training') ? 'none' : 'flex';   // 三层训练页隐藏错题本子导航
  document.body.setAttribute('data-domain', t);
}
function switchTop(tab){
  navigate(tab === 'training' ? 'training' : (_aiLastNbPage || 'dashboard'));
}
const _aiNavigateBase = navigate;
navigate = function(page, data){
  _aiNavigateBase(page, data);
  if (page !== 'training') _aiLastNbPage = (page === 'detail') ? 'list' : page;  // detail 需带参，不记忆
  _aiApplyTopTab(page);
};

// ===================== INIT ====================="""


def sub_once(text, old, new, label):
    if old not in text:
        print(f'  ✗ 锚点未找到: {label}', file=sys.stderr)
        sys.exit(1)
    if text.count(old) != 1:
        print(f'  ✗ 锚点不唯一({text.count(old)}): {label}', file=sys.stderr)
        sys.exit(1)
    print(f'  ✓ {label}')
    return text.replace(old, new, 1)


def main():
    h = open(SRC, encoding='utf-8').read()
    print(f'源: {SRC}  {len(h)} 字符')
    h = sub_once(h, '<title>错题库 · 学习工具</title>', '<title>AI错题本 · 赵若琳学习中心</title>', 'title')
    h = sub_once(h, '</style>', CSS, 'CSS 注入')
    h = sub_once(h, NAV_OLD, NAV_NEW, '导航（双功能区）')
    h = sub_once(h, FOOTER_OLD, FOOTER_NEW, 'footer')
    h = sub_once(h, '// ===================== INIT =====================', JS_BLOCK, 'JS 切换逻辑')
    open(DST, 'w', encoding='utf-8').write(h)
    print(f'输出: {DST}  {len(h)} 字符')

    # 自检：关键锚点仍在、无残留旧品牌
    checks = [
        ('渲染函数齐全', all(f'function {f}' in h for f in
                            ('renderDashboard', 'renderAdd', 'renderList', 'renderDetail',
                             'renderReview', 'renderTraining', 'renderQTraining', 'renderPrint', 'renderAnalysis'))),
        ('数据键未改', "const LS_KEY = 'wrong_bank_data';" in h),
        ('云同步未改', 'api_wrongbank.php' in h),
        ('双功能区到位', h.count("data-top=\"notebook\"") == 1 and h.count("data-top=\"training\"") == 1),
        ('顶层三数组未动', h.count('const BUILTIN_QUESTIONS=[') == 1),
    ]
    ok = True
    for name, cond in checks:
        print(('  ✓ ' if cond else '  ✗ ') + name)
        ok = ok and cond
    n_q = len(re.findall(r'\{q:', h)) + h.count('content:')
    print(f'  参考：BUILTIN 题数 = {h[h.index("const BUILTIN_QUESTIONS=["):h.index("];", h.index("const BUILTIN_QUESTIONS=["))].count("key:")}')
    return 0 if ok else 2


if __name__ == '__main__':
    sys.exit(main())
