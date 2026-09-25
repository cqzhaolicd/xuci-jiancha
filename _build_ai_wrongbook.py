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
# 独立版（脱离「赵若琳学习中心」）：部署到 /ai-wrongbook/ 顶层路径
# 用 <base href="/xuci-jiancha/"> 让 assets/、uploads/ 图片仍指向原目录（不必复制资源）
STANDALONE_DIR = os.path.join(ROOT, 'ai-wrongbook')
STANDALONE = os.path.join(STANDALONE_DIR, 'index.html')

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
      <button class="top-tab" data-top="points" onclick="switchTop('points')"><i class="fas fa-clipboard-check"></i> 复习要点</button>
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
  <i class="fas fa-heart" style="color:var(--danger)"></i> AI错题本 · 收录「错题本」「三层训练」「复习要点」三项功能
  &nbsp;|&nbsp; 数据与「错题库」共用同一份（本机存储 + 云端同步）
  &nbsp;|&nbsp; <a href="index.html" style="color:var(--primary)">返回学习中心</a>
</div>"""

JS_BLOCK = """// ===================== AI错题本 · 双功能区（错题本 / 三层训练） =====================
// 本页 = 把错题库里的「错题本」与「三层训练」两项功能单独成页。
// 数据层/渲染函数与原页完全同源；localStorage 键与云端后端也一致 ⇒ 两页数据互通：
// 在原错题库录入或复习的题，这里立刻可见；反之亦然。
let _aiLastNbPage = 'dashboard';
function _aiTopTabOf(page){ return page === 'training' ? 'training' : (page === 'points' ? 'points' : 'notebook'); }
function _aiApplyTopTab(page){
  const t = _aiTopTabOf(page);
  document.querySelectorAll('#topTabs .top-tab').forEach(b => b.classList.toggle('active', b.dataset.top === t));
  const mn = document.getElementById('mainNav');
  if (mn) mn.style.display = (t === 'notebook') ? 'flex' : 'none';   // 三层训练/复习要点页隐藏错题本子导航
  document.body.setAttribute('data-domain', t);
}
function switchTop(tab){
  if (tab === 'training') { navigate('training', {}); return; }
  if (tab === 'points')   { navigate('points'); return; }
  navigate(_aiLastNbPage || 'dashboard');
}
const _aiNavigateBase = navigate;
navigate = function(page, data){
  _aiNavigateBase(page, data);
  if (page !== 'training' && page !== 'points') _aiLastNbPage = (page === 'detail') ? 'list' : page;  // detail 需带参，不记忆
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

    # ---------- 同步生成「独立版」（/ai-wrongbook/）：去掉一切指向学习中心的东西 ----------
    # 命名：独立版 = 「AI错题本-测试版」（老板指定）
    s = h
    s = sub_once(s, '<title>AI错题本 · 赵若琳学习中心</title>',
                 '<title>AI错题本-测试版</title>\n<base href="/xuci-jiancha/">', '独立版: 标题 + base')
    s = sub_once(s, '<a class="navbar-brand" href="index.html"><i class="fas fa-robot"></i> AI错题本</a>',
                 '<span class="navbar-brand"><i class="fas fa-robot"></i> AI错题本-测试版</span>', '独立版: 品牌链接去外链')
    s = sub_once(s, 'AI错题本 · 收录「错题本」「三层训练」「复习要点」三项功能',
                 'AI错题本-测试版 · 收录「错题本」「三层训练」「复习要点」三项功能', '独立版: 页脚命名')
    s = re.sub(r'\n\s*&nbsp;\|&nbsp; <a href="index\.html"[^>]*>返回学习中心</a>', '', s, count=1)
    # API 用绝对同源路径，避免受 base/目录层级影响
    s = sub_once(s, "if (host === '192.168.3.88') return 'api_wrongbank.php';",
                 "if (host === '192.168.3.88') return '/xuci-jiancha/api_wrongbank_test.php';", '独立版: API(威联通·测试库)')
    s = sub_once(s, "if (/\\.trycloudflare\\.com$/.test(host)) return 'api_wrongbank.php';",
                 "if (/\\.trycloudflare\\.com$/.test(host)) return '/xuci-jiancha/api_wrongbank_test.php';", '独立版: API(隧道·测试库)')
    # ---------- 数据隔离：独立存储键 + 独立后端数据文件 ----------
    for a, b, lab in [
        ("const LS_KEY = 'wrong_bank_data';", "const LS_KEY = 'wrong_bank_data_test';", '隔离: 主数据键'),
        ("const IMPORT_KEY = 'wrong_bank_import';", "const IMPORT_KEY = 'wrong_bank_import_test';", '隔离: 导入键'),
        ("const BUILTIN_FLAG='wrong_bank_builtin_applied';", "const BUILTIN_FLAG='wrong_bank_builtin_applied_test';", '隔离: 内置收录标记'),
        ("const SYNC_REMOTE = 'http://192.168.3.88/xuci-jiancha/api_wrongbank.php';",
         "const SYNC_REMOTE = 'http://192.168.3.88/xuci-jiancha/api_wrongbank_test.php';", '隔离: 后端(内网其它来源)'),
        ("localStorage.getItem('wb_last_grade')", "localStorage.getItem('wb_last_grade_test')", '隔离: 上次年级(读)'),
        ("localStorage.setItem('wb_last_grade'", "localStorage.setItem('wb_last_grade_test'", '隔离: 上次年级(写)'),
        ("localStorage.setItem('wrong_bank_review_filter'", "localStorage.setItem('wrong_bank_review_filter_test'", '隔离: 筛选记忆(存)'),
        ("localStorage.getItem('wrong_bank_review_filter')", "localStorage.getItem('wrong_bank_review_filter_test')", '隔离: 筛选记忆(读)'),
        ("const REVIEW_SHOW_ANA5=false;", "const REVIEW_SHOW_ANA5=true;   // 测试版先开：复习页显示五维分析", '测试版: 复习页显示五维分析'),
    ]:
        s = sub_once(s, a, b, lab)
    os.makedirs(STANDALONE_DIR, exist_ok=True)
    open(STANDALONE, 'w', encoding='utf-8').write(s)
    ok = True
    chips = [
        ('独立版: 名称=AI错题本-测试版', s.count('AI错题本-测试版') >= 3),
        ('独立版: 无「返回学习中心」链接', '返回学习中心' not in s),
        ('独立版: 无 index.html 外链', 'href="index.html"' not in s),
        ('独立版: base 已设', s.count('<base href="/xuci-jiancha/">') == 1),
        ('独立版: 带 复习要点/筛选', 'function renderPoints' in s and 'function rvfPanel' in s),
    ]
    for name, cond in chips:
        print(('  ✓ ' if cond else '  ✗ ') + name)
        ok = ok and cond

    # 自检：关键锚点仍在、无残留旧品牌
    checks = [
        ('渲染函数齐全', all(f'function {f}' in h for f in
                            ('renderDashboard', 'renderAdd', 'renderList', 'renderDetail',
                             'renderReview', 'renderTraining', 'renderQTraining', 'renderPrint', 'renderAnalysis'))),
        ('数据键未改', "const LS_KEY = 'wrong_bank_data';" in h),
        ('云同步未改', 'api_wrongbank.php' in h),
        ('双功能区到位', h.count("data-top=\"notebook\"") == 1 and h.count("data-top=\"training\"") == 1),
        ('复习要点到位', h.count("data-top=\"points\"") == 1 and 'function renderPoints' in h),
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
