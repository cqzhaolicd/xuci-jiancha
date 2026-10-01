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
import json

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


AUTH_CSS = """<style>
/* ===== AI错题本-测试版 · 登录门禁 ===== */
.ab-gate{position:fixed;inset:0;z-index:99999;background:linear-gradient(135deg,#667eea,#764ba2);
  display:flex;align-items:center;justify-content:center;padding:18px}
.ab-gate.ab-hide{display:none}
.ab-card{background:#fff;border-radius:18px;padding:22px 20px;width:100%;max-width:360px;
  box-shadow:0 18px 50px rgba(0,0,0,.25)}
.ab-logo{font-size:1.12rem;font-weight:700;color:#1a202c;text-align:center}
.ab-sub{font-size:.82rem;color:#718096;text-align:center;margin:.25rem 0 1rem}
.ab-tabs{display:flex;gap:.4rem;margin-bottom:.9rem}
.ab-tab{flex:1;background:#f0f2f5;color:#4a5568;border:none;padding:.5rem;border-radius:10px;
  font-weight:600;font-size:.9rem;cursor:pointer;font-family:inherit}
.ab-tab.active{background:#667eea;color:#fff}
.ab-card input{width:100%;padding:.62rem .8rem;border:1.5px solid #e2e8f0;border-radius:10px;
  font-size:.92rem;margin-bottom:.55rem;font-family:inherit;outline:none}
.ab-card input:focus{border-color:#667eea}
.ab-btn{width:100%;background:#667eea;color:#fff;border:none;padding:.68rem;border-radius:10px;
  font-size:.95rem;font-weight:700;cursor:pointer;font-family:inherit;margin-top:.2rem}
.ab-btn:disabled{opacity:.6;cursor:not-allowed}
.ab-msg{font-size:.82rem;min-height:1.15rem;margin-top:.6rem;text-align:center}
.ab-msg.err{color:#e53e3e}.ab-msg.ok{color:#38a169}
.ab-foot{font-size:.72rem;color:#a0aec0;text-align:center;margin-top:.8rem;line-height:1.5}
.ab-chip{position:fixed;right:10px;bottom:10px;z-index:9998;background:rgba(26,32,44,.82);color:#fff;
  font-size:.75rem;padding:.3rem .6rem;border-radius:999px;display:flex;gap:.5rem;align-items:center}
.ab-chip a{color:#90cdf4;cursor:pointer;text-decoration:underline}
.ab-off{background:#ecc94b;color:#1a202c;border-radius:999px;padding:.05rem .45rem;font-size:.7rem}
</style>"""

AUTH_OVERLAY = """<!-- AUTH_GATE_V1 · AI错题本-测试版 登录门禁 -->
<div id="abGate" class="ab-gate">
  <div class="ab-card">
    <div class="ab-logo">🤖 AI错题本-测试版</div>
    <div class="ab-sub">请先登录后再使用</div>
    <div class="ab-tabs">
      <button id="abTabLogin" class="ab-tab active" onclick="ABG.tab('login')">登录</button>
      <button id="abTabReg" class="ab-tab" onclick="ABG.tab('reg')">注册</button>
    </div>
    <div id="abPaneLogin">
      <input id="abLoginUser" placeholder="用户名 / 手机号" autocomplete="username">
      <input id="abLoginPass" type="password" placeholder="密码" autocomplete="current-password">
      <button class="ab-btn" id="abLoginBtn" onclick="ABG.login()">登 录</button>
    </div>
    <div id="abPaneReg" style="display:none">
      <input id="abRegUser" placeholder="用户名（3-32位字母数字）或手机号">
      <input id="abRegPass" type="password" placeholder="密码（至少 6 位）">
      <input id="abRegPass2" type="password" placeholder="确认密码">
      <input id="abRegInvite" placeholder="邀请码（无则留空）">
      <button class="ab-btn" id="abRegBtn" onclick="ABG.register()">注册并登录</button>
    </div>
    <div id="abMsg" class="ab-msg"></div>
    <div class="ab-foot">账号服务：家里的私有云 iStoreOS · 数据独立存储</div>
  </div>
</div>
<div id="abUserChip" class="ab-chip" style="display:none">
  <span id="abUserName"></span><span id="abOffTag" class="ab-off" style="display:none">离线</span>
  <a onclick="ABG.logout()">退出</a>
</div>"""

AUTH_JS = """<script>
/* ===== AI错题本-测试版 · 登录门禁（独立于页面逻辑，前缀 ABG / ab*） ===== */
var ABG=(function(){
  var TOKEN_KEY='wb_auth_token_test', USER_KEY='wb_auth_user_test';
  // 内网私有云（iStoreOS）认证服务；如需外网访问，把 https 隧道地址填到 REMOTE_APIS
  var LAN_APIS=['http://192.168.3.3:8090'];
  var REMOTE_APIS=[];
  var api=null, offline=false;

  function $(id){return document.getElementById(id)}
  function msg(t,ok){var e=$('abMsg');e.textContent=t;e.className='ab-msg '+(ok?'ok':'err')}
  // 连不上服务器时给「对症」的提示：https 网页被浏览器拦住，跟手机没连 WiFi 是两回事
  function netErr(){return location.protocol==='https:'
    ? '公网网页版（https）无法直连家里的账号服务：请用 App，或在家里打开内网网址登录'
    : '连不上家里的服务器：请确认设备连着家里 WiFi（或稍后再试）'}
  function expireOf(t){try{var p=JSON.parse(atob(t.split('.')[0].replace(/-/g,'+').replace(/_/g,'/')));return (p.exp||0)*1000}catch(e){return 0}}

  function candidates(){
    var https=location.protocol==='https:';
    // https 页面会被浏览器拦截 http 请求（混合内容），故 https 下只走 https 隧道
    return https ? REMOTE_APIS.slice() : LAN_APIS.concat(REMOTE_APIS);
  }
  function request(path,body,token){
    var list=candidates();
    if(!list.length)return Promise.reject(new Error('no-endpoint'));
    var base=(api&&list.indexOf(api)>=0)?api:list[0];
    var h={};if(body)h['Content-Type']='application/json';if(token)h['Authorization']='Bearer '+token;
    return fetch(base+path,{method:body?'POST':'GET',headers:h,body:body?JSON.stringify(body):undefined})
      .then(function(r){
        if(r.status===401||r.status===403){api=base}
        else if(r.ok){api=base}
        return r.json().then(function(j){return {status:r.status,json:j}});
      });
  }
  function show(){var g=$('abGate');if(g)g.classList.remove('ab-hide');document.documentElement.style.overflow='hidden'}
  function hide(){var g=$('abGate');if(g)g.classList.add('ab-hide');document.documentElement.style.overflow=''}
  function chip(u){
    var c=$('abUserChip');if(!c)return;
    if(!u){c.style.display='none';return}
    $('abUserName').textContent='👤 '+(u.display||u.username);
    $('abOffTag').style.display=offline?'':'none';
    c.style.display='flex';
  }
  function save(token,user){
    try{localStorage.setItem(TOKEN_KEY,token);localStorage.setItem(USER_KEY,JSON.stringify(user))}catch(e){}
  }
  function clear(){try{localStorage.removeItem(TOKEN_KEY);localStorage.removeItem(USER_KEY)}catch(e){}}

  function login(){
    var u=$('abLoginUser').value.trim(),p=$('abLoginPass').value;
    if(!u||!p)return msg('请填写账号和密码');
    $('abLoginBtn').disabled=true;msg('登录中…',true);
    request('/api/login',{username:u,password:p}).then(function(r){
      $('abLoginBtn').disabled=false;
      if(r.json&&r.json.ok){save(r.json.token,r.json.user);afterAuth(r.json.user);msg('登录成功',true)}
      else msg((r.json&&r.json.error)||'登录失败');
    }).catch(function(){ $('abLoginBtn').disabled=false; msg(netErr()) });
  }
  function register(){
    var u=$('abRegUser').value.trim(),p=$('abRegPass').value,p2=$('abRegPass2').value,iv=$('abRegInvite').value.trim();
    if(!u)return msg('请填写用户名或手机号');
    if(p.length<6)return msg('密码至少 6 位');
    if(p!==p2)return msg('两次输入的密码不一致');
    $('abRegBtn').disabled=true;msg('注册中…',true);
    request('/api/register',{username:u,password:p,invite:iv}).then(function(r){
      $('abRegBtn').disabled=false;
      if(r.json&&r.json.ok){save(r.json.token,r.json.user);afterAuth(r.json.user);msg('注册成功',true)}
      else msg((r.json&&r.json.error)||'注册失败');
    }).catch(function(){ $('abRegBtn').disabled=false; msg(netErr()) });
  }
  function afterAuth(user){
    offline=false;chip(user);hide();
    window.setTimeout(function(){
      request('/api/me',null,localStorage.getItem(TOKEN_KEY)).then(function(r){
        if(r.status===401){clear();chip(null);show();msg('登录已失效，请重新登录')}
        else{offline=false;chip(user)}
      }).catch(function(){offline=true;chip(user)});
    },1500);
  }
  function logout(){
    if(!confirm('确定退出登录？'))return;
    clear();chip(null);api=null;
    var g=$('abGate');if(g)g.classList.remove('ab-hide');
    $('abLoginUser').value='';$('abLoginPass').value='';show();
  }
  function tab(which){
    var isLogin=which==='login';
    $('abTabLogin').className='ab-tab'+(isLogin?' active':'');
    $('abTabReg').className='ab-tab'+(isLogin?'':' active');
    $('abPaneLogin').style.display=isLogin?'':'none';
    $('abPaneReg').style.display=isLogin?'none':'';
    msg('',true);
  }
  function init(){
    var tok=null,user=null;
    try{tok=localStorage.getItem(TOKEN_KEY);user=JSON.parse(localStorage.getItem(USER_KEY)||'null')}catch(e){}
    if(tok&&expireOf(tok)>Date.now()){
      // 有未过期凭证 ⇒ 先进去（离线可用），再后台向服务器核实
      afterAuth(user||{username:'已登录'});
    }else{
      show();
      if(location.protocol==='https:'&&!REMOTE_APIS.length)
        msg('当前是 https 网页访问，浏览器会拦截内网请求；请用 App 或家里的内网地址登录');
    }
    $('abLoginPass').addEventListener('keydown',function(e){if(e.key==='Enter')login()});
    $('abRegPass2').addEventListener('keydown',function(e){if(e.key==='Enter')register()});
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init);else init();
  return {login:login,register:register,logout:logout,tab:tab,init:init};
})();
</script>"""


def sub_once(text, old, new, label):
    if old not in text:
        print(f'  ✗ 锚点未找到: {label}', file=sys.stderr)
        sys.exit(1)
    if text.count(old) != 1:
        print(f'  ✗ 锚点不唯一({text.count(old)}): {label}', file=sys.stderr)
        sys.exit(1)
    print(f'  ✓ {label}')
    return text.replace(old, new, 1)


def tunnel_url():
    """账号服务的外网 https 隧道地址（cloudflared quick tunnel）。
    优先读状态文件，其次读隧道日志；取不到就返回 ''（门禁自动只走内网 + App）。"""
    try:
        st = json.load(open(os.path.expanduser('~/.hermes/state/tunnel_urls.json'), encoding='utf-8'))
        u = (st.get('aiwrongbook') or '').strip()
        if u.startswith('https://'):
            return u.rstrip('/')
    except Exception:
        pass
    try:
        txt = open('/tmp/cf_aiwrongbook.log', encoding='utf-8', errors='ignore').read()
        m = re.findall(r'https://[a-z0-9-]+\.trycloudflare\.com', txt)
        return m[-1].rstrip('/') if m else ''
    except Exception:
        return ''


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
    # 独立版数据已隔离 ⇒ 文案不能说"与错题库共用同一份"（老板会误解为错题会同步过来）
    s = sub_once(s, '数据与「错题库」共用同一份（本机存储 + 云端同步）',
                 '数据独立存储（测试用，与错题库互不影响）', '独立版: 数据说明文案')
    s = sub_once(s, '// 数据层/渲染函数与原页完全同源；localStorage 键与云端后端也一致 ⇒ 两页数据互通：\n// 在原错题库录入或复习的题，这里立刻可见；反之亦然。',
                 '// ⚠️ 测试版：数据层与错题库「隔离」—— 独立 localStorage 键 + 独立后端\n'
                 '// （api_wrongbank_test.php / wrong_bank_data_test.json）。错题只进「错题库」与「AI错题本」，\n'
                 '// 不进本测试版；这里录入的内容也不会回流到错题库。', '独立版: 数据互通注释纠正')
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
        ("const REVIEW_SHOW_ANA5=true;", "const REVIEW_SHOW_ANA5=true;", '复习页显示五维分析（正式版+测试版均已开）'),
        ("const AI_LS='wb_ai_cfg';", "const AI_LS='wb_ai_cfg_test';", '隔离: AI 设置(Key/模型)'),
    ]:
        s = sub_once(s, a, b, lab)

    # ---------- 测试版：错题保持原样，只是「以后新增的不进来」（老板 2026-09-27）----------
    # 「新增不进测试版」由「键隔离 + 后端隔离」天然保证：生产页面录入只写生产库，测试版后端是独立文件，拉不到新题。
    # BUILTIN_QUESTIONS 是**静态快照**（不随生产库变化）⇒ 保留，不要清空（老板：「测试版内的错题就不动了」）。
    n_builtin = s[s.index('const BUILTIN_QUESTIONS='):s.index('function applyBuiltinQuestions')].count('key:')
    print(f'  · 测试版: 保留内置错题快照 {n_builtin} 条（以后新增的错题不会进入测试版）')

    # ---------- 登录门禁（老板 2026-10-01）：测试版必须先注册/登录才能使用 ----------
    # 账号服务跑在家里的私有云 iStoreOS(192.168.3.3:8090)，只作用于本测试版页面
    s = sub_once(s, '<base href="/xuci-jiancha/">',
                 '<base href="/xuci-jiancha/">' + AUTH_CSS, '登录门禁: 样式')
    tun = tunnel_url()
    auth_js = AUTH_JS if not tun else AUTH_JS.replace(
        'var REMOTE_APIS=[];', 'var REMOTE_APIS=[' + json.dumps(tun) + '];')
    print(f'  · 外网登录通道: {tun or "（无隧道，仅内网 + App 可用）"}')
    s = sub_once(s, '</body>', AUTH_OVERLAY + auth_js + '\n</body>', '登录门禁: 登录页 + 脚本')

    os.makedirs(STANDALONE_DIR, exist_ok=True)
    open(STANDALONE, 'w', encoding='utf-8').write(s)
    ok = True
    chips = [
        ('独立版: 名称=AI错题本-测试版', s.count('AI错题本-测试版') >= 3),
        ('独立版: 登录门禁已注入（需注册/登录后才能用）',
         'AUTH_GATE_V1' in s and 'var ABG=' in s and 'wb_auth_token_test' in s
         and s.count('id="abGate"') == 1),
        ('独立版: 无「返回学习中心」链接', '返回学习中心' not in s),
        ('独立版: 外网登录通道已写入', bool(tun) and (tun in s)),
        ('独立版: 无 index.html 外链', 'href="index.html"' not in s),
        ('独立版: base 已设', s.count('<base href="/xuci-jiancha/">') == 1),
        ('独立版: 带 复习要点/筛选', 'function renderPoints' in s and 'function rvfPanel' in s),
        ('独立版: 保留内置错题快照（新增不进测试版）',
         'const BUILTIN_QUESTIONS=[' in s and 'wrong_bank_data_test' in s
         and 'api_wrongbank_test.php' in s and 'wb_test_purge_builtin_v1' not in s),
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
