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

# ── 网页图标（方案③ 内嵌 base64；网页 / NAS / 公网 / APK 通用，无需额外文件）──
FAVICON_TAGS = '<link rel="icon" type="image/png" sizes="128x128" href="data:image/png;base64,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">\n<link rel="apple-touch-icon" sizes="180x180" href="data:image/png;base64,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">'

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, 'wrong_bank.html')
DST = os.path.join(ROOT, 'ai_wrongbook.html')
# 独立版（脱离「赵若琳学习中心」）：部署到 /ai-wrongbook/ 顶层路径
# 用 <base href="/xuci-jiancha/"> 让 assets/、uploads/ 图片仍指向原目录（不必复制资源）
STANDALONE_DIR = os.path.join(ROOT, 'ai-wrongbook')
STANDALONE = os.path.join(STANDALONE_DIR, 'index.html')

CSS = """/* ===== AI错题本 · 顶部导航（老板 2026-10-02：取消「错题本/三层训练/复习要点」三标签） ===== */
#mainNav{border-top:1px solid rgba(255,255,255,.18);padding-top:.35rem}
.domain-tip{font-size:.76rem;color:var(--text-light);margin:-.4rem 0 .8rem}
</style>"""

NAV_OLD = """<nav class="navbar"><div class="container">
  <a class="navbar-brand" href="#" onclick="navigate('dashboard');return false"><i class="fas fa-database"></i> 错题库</a>
  <div class="navbar-nav" id="mainNav">
    <a class="active" data-page="dashboard"><i class="fas fa-home"></i><span>首页</span></a>
    <a data-page="add"><i class="fas fa-plus-circle"></i><span>录入</span></a>
    <a data-page="list"><i class="fas fa-list"></i><span>错题本</span></a>
    <a data-page="review"><i class="fas fa-redo"></i><span>复习</span></a>
    <a data-page="training"><i class="fas fa-layer-group"></i><span>三层练</span></a>
    <a data-page="print-page"><i class="fas fa-print"></i><span>打印</span></a>
    <a data-page="analysis"><i class="fas fa-chart-pie"></i><span>分析</span></a>
  </div>
  <a class="nav-back" id="navBack" onclick="goBack()" title="返回上一页"><i class="fas fa-arrow-left"></i><span>返回</span></a>
</div></nav>"""

NAV_NEW = """<nav class="navbar"><div class="container" style="flex-direction:column;align-items:stretch;gap:.45rem">
  <div style="display:flex;align-items:center;gap:.5rem;flex-wrap:wrap">
    <a class="navbar-brand" href="index.html"><i class="fas fa-robot"></i> AI错题本</a>
  </div>
  <div class="navbar-nav" id="mainNav">
    <a class="active" data-page="dashboard"><i class="fas fa-home"></i><span>首页</span></a>
    <a data-page="add"><i class="fas fa-plus-circle"></i><span>录入</span></a>
    <a data-page="list"><i class="fas fa-list"></i><span>错题本</span></a>
    <a data-page="review"><i class="fas fa-redo"></i><span>复习</span></a>
    <a data-page="print-page"><i class="fas fa-print"></i><span>打印</span></a>
    <a data-page="analysis"><i class="fas fa-chart-pie"></i><span>分析</span></a>
  </div>
  <div style="display:flex;justify-content:flex-end">
    <a class="nav-back" id="navBack" onclick="goBack()" title="返回上一页"><i class="fas fa-arrow-left"></i><span>返回</span></a>
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
function _aiApplyTopTab(page){
  // 【老板 2026-10-02】顶部「错题本/三层训练/复习要点」三标签已取消
  // 子导航 #mainNav 改为常显（原来进 三层训练/复习要点 页会把它隐藏，现在没标签可回来了，必须常显）
  const mn = document.getElementById('mainNav');
  if (mn && mn.style.display !== 'flex') mn.style.display = 'flex';
  document.body.setAttribute('data-domain', (page === 'training' || page === 'points') ? page : 'notebook');
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


def _count_builtin(txt):
    """数内置快照里有几道题（兼容 JS 的 key:'x' 与 JSON 的 "key":"x" 两种写法）。"""
    a = txt.index('const BUILTIN_QUESTIONS=')
    b = txt.index('function applyBuiltinQuestions', a)
    return len(re.findall(r'[{\s]"?key"?\s*:', txt[a:b]))


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
/* 账号信息：放进顶部紫色导航栏（右上角），跟着 sticky 导航栏一起吸顶 */
.ab-chip{position:static;margin-left:auto;background:rgba(255,255,255,.16);border:1px solid rgba(255,255,255,.34);
  color:#fff;font-size:.72rem;padding:.24rem .58rem;border-radius:999px;display:flex;gap:.45rem;align-items:center;
  white-space:nowrap;line-height:1.5}
.ab-chip a{color:#fff;cursor:pointer;text-decoration:underline}
.ab-chip #abUserName{font-weight:600}
.ab-off{background:#ecc94b;color:#1a202c;border-radius:999px;padding:.05rem .45rem;font-size:.7rem}
.ab-trial{background:#fefcbf;color:#744210;border-radius:999px;padding:.05rem .45rem;font-size:.7rem;font-weight:700}
#abPayQrBox img{width:230px;max-width:82%;border:1px solid #e2e8f0;border-radius:10px;background:#fff;padding:6px}
#abPayQrBox .ab-qrhint{font-size:.8rem;color:#718096;line-height:1.6}
#abPayNote.ok{color:#2f855a}#abPayNote.err{color:#c53030}
.ab-lb{display:block;text-align:left;font-size:.8rem;color:#4a5568;font-weight:600;margin:.6rem 0 .25rem}
.ab-card select{width:100%;padding:.55rem .7rem;border:1px solid #cbd5e0;border-radius:8px;font-size:.95rem;
  font-family:inherit;background:#fff;color:#1a202c}
.ab-rad{display:flex;gap:1.4rem;justify-content:flex-start;padding:.3rem 0 .2rem;font-size:.95rem;color:#2d3748}
.ab-rad label{display:flex;align-items:center;gap:.35rem;cursor:pointer}
.ab-btn2{width:100%;background:#edf2f7;color:#2d3748;border:none;padding:.6rem;border-radius:10px;
  font-size:.9rem;font-weight:600;cursor:pointer;font-family:inherit;margin-top:.5rem}
.ab-bk{display:flex;gap:.5rem}
.ab-bk .ab-btn2{margin-top:.2rem;font-size:.85rem;padding:.55rem .4rem}
.ab-trial.lock{background:#fed7d7;color:#c53030;cursor:pointer}
/* 账号胶囊放在子导航行最右（顶部三标签取消后走 .ab-navrow 兜底通道） */
.ab-navrow .ab-chip{margin-left:auto}
@media (max-width:520px){
  .ab-chip{font-size:.6rem !important;padding:.1rem .34rem !important;gap:.2rem !important;margin-left:auto !important}
  .ab-chip .ab-trial,.ab-chip .ab-off{font-size:.58rem;padding:.01rem .26rem;border-radius:999px}
}
</style>"""

AUTH_OVERLAY = """<!-- AUTH_GATE_V1 · AI错题本-测试版 登录门禁 -->
<div id="abGate" class="ab-gate">
  <div class="ab-card">
    <div class="ab-logo">🤖 AI错题本 <span style="color:#90cdf4;font-size:.86em">{APP_VER}</span></div>
    <div class="ab-sub">请先登录后再使用</div>
    <div class="ab-tabs">
      <button id="abTabLogin" class="ab-tab active" onclick="ABG.tab('login')">登录</button>
      <button id="abTabReg" class="ab-tab" onclick="ABG.tab('reg')">注册</button>
    </div>
    <div id="abPaneLogin">
      <input id="abLoginUser" placeholder="手机号" inputmode="numeric" maxlength="11" autocomplete="username">
      <input id="abLoginPass" type="password" placeholder="密码" autocomplete="current-password">
      <button class="ab-btn" id="abLoginBtn" onclick="ABG.login()">登 录</button>
    </div>
    <div id="abPaneReg" style="display:none">
      <input id="abRegUser" placeholder="11 位手机号（如 13800001111）" inputmode="numeric" maxlength="11" autocomplete="tel">
      <input id="abRegPass" type="password" placeholder="密码（至少 6 位）">
      <input id="abRegPass2" type="password" placeholder="确认密码">
      <button class="ab-btn" id="abRegBtn" onclick="ABG.register()">注册并登录</button>
    </div>
    <div id="abMsg" class="ab-msg"></div>
  </div>
</div>
<div id="abUserChip" class="ab-chip" style="display:none">
  <span id="abUserName" onclick="ABG.profileModal(true)" style="cursor:pointer" title="点这里填/改账号资料"></span><span id="abTrialTag" class="ab-trial" style="display:none"></span><span id="abOffTag" class="ab-off" style="display:none">离线</span>
  <a onclick="ABG.logout()">退出</a>
</div>
<div id="abProf" class="ab-gate ab-hide">
  <div class="ab-card" style="max-width:400px">
    <div class="ab-logo">📇 账号资料</div>
    <div class="ab-sub">填一次就行，方便分班与联系；之后点右下角「👤」随时改</div>
    <label class="ab-lb">城市</label>
    <input id="abPfCity" placeholder="如：成都" maxlength="30">
    <label class="ab-lb">学校名称</label>
    <input id="abPfSchool" placeholder="如：树德实验中学" maxlength="60">
    <label class="ab-lb">年级</label>
    <select id="abPfGrade">
      <option value="">请选择</option><option>六年级</option><option>七年级</option><option>八年级</option>
      <option>九年级</option><option>高一</option><option>高二</option><option>高三</option><option>其他</option>
    </select>
    <label class="ab-lb">姓名</label>
    <input id="abPfName" placeholder="孩子姓名或常用称呼" maxlength="20">
    <label class="ab-lb">性别</label>
    <div class="ab-rad">
      <label><input type="radio" name="abPfGender" value="男"> 男</label>
      <label><input type="radio" name="abPfGender" value="女"> 女</label>
    </div>
    <label class="ab-lb">会员状态</label>
    <div class="ab-bk" style="align-items:center">
      <span id="abVipState" style="flex:1;text-align:left;font-size:.85rem;color:#4a5568;line-height:1.5">—</span>
      <button class="ab-btn2" id="abVipBtn" onclick="ABG.openPay()" style="display:none;white-space:nowrap">👑 开通 VIP</button>
    </div>
    <label class="ab-lb">数据备份（换手机 / 重装前建议先导出）</label>
    <div class="ab-bk">
      <button class="ab-btn2" onclick="ABG.exportData()">⬇ 导出备份</button>
      <button class="ab-btn2" onclick="ABG.importData()">⬆ 导入恢复</button>
    </div>
    <div id="abBkMsg" class="ab-msg" style="min-height:1.15rem;font-size:.78rem;color:#4a5568;text-align:left"></div>
    <div id="abPfMsg" class="ab-msg" style="min-height:1.2em"></div>
    <button class="ab-btn" onclick="ABG.saveProfile()">保存</button>
    <button class="ab-btn2" onclick="ABG.closeProfile()">以后再说</button>
  </div>
</div>
<div id="abPay" class="ab-gate ab-hide">
  <div class="ab-card" style="max-width:400px;text-align:center">
    <div class="ab-logo" id="abPayTitle">⏰ 免费试用已结束</div>
    <div class="ab-sub" id="abPaySub"></div>
    <div id="abPayWhy" class="ab-msg err" style="display:none;background:#fff5f5;border:1px solid #fed7d7;border-radius:8px;padding:.45rem .6rem;margin-top:.5rem"></div>
    <div id="abPayStep1">
      <div style="font-size:.88rem;color:#4a5568;line-height:1.75;margin:.5rem 0 .7rem;text-align:left">
        有邀请码？填在下面，下一步按 <b style="color:#c53030">299 元</b> 开通；<br>
        没有邀请码，点下面「直接开通」，按标准价 <b>399 元</b> 开通。
      </div>
      <input id="abPayInvite" placeholder="邀请码（没有可留空）" style="text-transform:uppercase">
      <button class="ab-btn" onclick="ABG.claimInvite()">使用邀请码，按 299 元开通</button>
      <button class="ab-btn2" onclick="ABG.payStep('qr')">没有邀请码，直接开通（399 元）</button>
      <a onclick="ABG.payStep('card')" style="display:block;margin-top:10px;font-size:.85rem;color:#3182ce;cursor:pointer;font-weight:600">🎟️ 我有卡密（一次性码），直接开通</a>
    </div>
    <div id="abPayStep2" style="display:none">
      <div id="abPayAmt" style="font-size:1.7rem;font-weight:800;color:#e53e3e;margin:8px 0">￥--</div>
      <div id="abPayQrBox" style="margin:10px 0;min-height:60px"></div>
      <input id="abPayUserNote" placeholder="选填：付款时留的备注 / 微信昵称（便于核对）" style="margin-bottom:6px">
      <button class="ab-btn" onclick="ABG.submitPaid()">✅ 我已付款，提交核对</button>
      <button class="ab-btn2" onclick="ABG.refreshPay()">🔄 已开通？刷新状态</button>
      <div style="display:flex;gap:12px;justify-content:center;margin-top:10px;flex-wrap:wrap">
        <a onclick="ABG.payStep('invite')" style="font-size:.85rem;color:#3182ce;cursor:pointer;font-weight:600">返回上一步（我有邀请码）</a>
        <a onclick="ABG.payStep('card')" style="font-size:.85rem;color:#3182ce;cursor:pointer;font-weight:600">🎟️ 我有卡密</a>
      </div>
    </div>
    <div id="abPayStep3" style="display:none">
      <div style="font-size:.88rem;color:#4a5568;line-height:1.75;margin:.5rem 0 .7rem;text-align:left">
        把卡密填在下面，点「兑换并开通」<b style="color:#c53030">立即开通</b>，不用等管理员核对。
      </div>
      <input id="abPayCard" placeholder="卡密（如 AB-XXXX-XXXX）" style="text-transform:uppercase;letter-spacing:1px">
      <button class="ab-btn" onclick="ABG.redeemCard()">兑换并开通</button>
      <a onclick="ABG.payStep('invite')" style="display:block;margin-top:10px;font-size:.85rem;color:#3182ce;cursor:pointer;font-weight:600">返回上一步</a>
    </div>
    <div id="abPayNote" class="ab-msg" style="min-height:1.2em"></div>
    <a onclick="ABG.closePay()" style="display:block;margin-top:12px;font-size:.85rem;color:#3182ce;cursor:pointer;font-weight:600">先看看，稍后开通</a>
    <a onclick="ABG.logout()" style="display:block;margin-top:6px;font-size:.8rem;color:#a0aec0;cursor:pointer">退出登录</a>
  </div>
</div>"""

AUTH_JS = """<script>
/* ===== AI错题本-测试版 · 登录门禁（独立于页面逻辑，前缀 ABG / ab*） ===== */
var ABG=(function(){
  var TOKEN_KEY='wb_auth_token_test', USER_KEY='wb_auth_user_test';
  // 【账号隔离】把当前登录账号交给页面云同步层 → 服务器按账号分文件存，互不相通
  window.__wbSyncUser=function(){
    try{var u=JSON.parse(localStorage.getItem(USER_KEY)||'null');return (u&&u.username)||''}catch(e){return ''}
  };
  // 记录「本机数据属于哪个账号」：换账号登录时提示，避免把上一个账号的数据推到新账号云端
  var NL=String.fromCharCode(10);
  OWNER_KEY='wb_test_owner_user';
  // 内网私有云（iStoreOS）认证服务；如需外网访问，把 https 隧道地址填到 REMOTE_APIS
  var LAN_APIS=['http://192.168.3.3:8090'];
  var REMOTE_APIS=[];
  var api=null, offline=false;

  function $(id){return document.getElementById(id)}
  function msg(t,ok){var e=$('abMsg');e.textContent=t;e.className='ab-msg '+(ok?'ok':'err')}
  // 连不上服务器时的提示：不给用户看「内网/公网」这些内部概念（老板 2026-10-01）
  function netErr(){return '网络连不上服务器，请检查手机网络后重试'}
  function expireOf(t){try{var p=JSON.parse(atob(t.split('.')[0].replace(/-/g,'+').replace(/_/g,'/')));return (p.exp||0)*1000}catch(e){return 0}}

  function candidates(){
    var https=location.protocol==='https:';
    // https 页面会被浏览器拦截 http 请求（混合内容），故 https 下只走 https 隧道
    return https ? REMOTE_APIS.slice() : LAN_APIS.concat(REMOTE_APIS);
  }
  // 每个候选地址的超时：内网(http)试得快一点，公网(https)给足时间
  function timeoutFor(base){return base.indexOf('https:')===0?12000:3000}
  // 依次尝试所有候选地址：在外网时内网地址连不上，必须自动切到公网隧道
  // （老板 2026-10-01：外网登录不了 —— 原来只试第一个地址，内网连不上就直接失败）
  function request(path,body,token){
    var list=candidates();
    if(!list.length)return Promise.reject(new Error('no-endpoint'));
    if(api&&list.indexOf(api)>=0)list=[api].concat(list.filter(function(x){return x!==api}));
    var i=0;
    function tryNext(){
      if(i>=list.length)return Promise.reject(new Error('all-endpoints-failed'));
      var base=list[i++];
      // 静默依次尝试，不给用户看「正在切换线路」这类过程提示
      var h={};if(body)h['Content-Type']='application/json';if(token)h['Authorization']='Bearer '+token;
      var opts={method:body?'POST':'GET',headers:h,body:body?JSON.stringify(body):undefined};
      var ctl=null,to=null;
      try{
        if(window.AbortController){ctl=new AbortController();opts.signal=ctl.signal;to=setTimeout(function(){try{ctl.abort()}catch(e){}},timeoutFor(base))}
      }catch(e){}
      return fetch(base+path,opts).then(function(r){
        if(to)clearTimeout(to);
        api=base;
        return r.text().then(function(t){
          var j={};try{j=JSON.parse(t)}catch(e){}
          return {status:r.status,json:j,base:base};
        });
      },function(err){
        if(to)clearTimeout(to);
        return tryNext();
      });
    }
    return tryNext();
  }
  function show(){var g=$('abGate');if(g)g.classList.remove('ab-hide');document.documentElement.style.overflow='hidden'}
  function hide(){var g=$('abGate');if(g)g.classList.add('ab-hide');document.documentElement.style.overflow=''}
  function showPay(){var g=$('abPay');if(g)g.classList.remove('ab-hide');document.documentElement.style.overflow='hidden'}
  function hidePay(){var g=$('abPay');if(g)g.classList.add('ab-hide');document.documentElement.style.overflow=''}
  // ── 试用 / 到期收款（老板 2026-10-01：免费试用 7 天；到期弹付费页，两步走：填码→299，不填→399）──
  var ACCESS=null;
  function setLock(v){try{if(window.__AB_SETLOCK)window.__AB_SETLOCK(v)}catch(e){}}
  function applyAccess(a){
    if(!a)return;
    ACCESS=a;setLock(!!a.locked);
    var why=document.getElementById('abPayWhy');if(why){why.style.display='none'}
    var tag=$('abTrialTag');
    if(tag){
      if(a.paid){tag.textContent='V';tag.title='VIP · 已开通';tag.className='ab-trial';tag.onclick=null;tag.style.display=''}
      else if(a.expired){tag.title='';tag.textContent='试用已结束 · 点此开通';tag.className='ab-trial lock';tag.onclick=function(){paywall()};tag.style.display=''}
      else{tag.title='点此开通 VIP（永久）';tag.textContent='试用剩 '+a.days_left+' 天';tag.className='ab-trial';tag.onclick=function(){paywall()};tag.style.display=''}
    }
    var vs=$('abVipState'),vb=$('abVipBtn');
    if(vs){
      if(a.paid){vs.innerHTML='✅ <b>VIP · 已开通</b>（永久有效）';if(vb)vb.style.display='none'}
      else if(a.expired){vs.innerHTML='⚠️ 试用已结束（已锁定新增）';if(vb)vb.style.display=''}
      else{vs.innerHTML='🎁 免费试用中，还剩 <b>'+a.days_left+'</b> 天';if(vb)vb.style.display=''}
    }
    if(a.locked)paywall();else hidePay();
    // 资料为空 → 登录后提示填一次（每台设备只提示一次，可「以后再说」）
    try{
      if(!a.locked && profileEmpty(a.profile) && !localStorage.getItem('ab_prof_asked')){
        localStorage.setItem('ab_prof_asked','1');
        setTimeout(function(){profileModal(true)},900);
      }
    }catch(e){}
  }
  function payStep(step){
    var s1=$('abPayStep1'),s2=$('abPayStep2'),s3=$('abPayStep3');
    if(!s1||!s2)return;
    if(s3)s3.style.display='none';
    if(step==='invite'){
      s1.style.display='';s2.style.display='none';
      $('abPayTitle').textContent='⏰ 免费试用已结束';
      $('abPaySub').textContent='有邀请码可享 299 元优惠价；没有也能按 399 元直接开通';
      return;
    }
    if(step==='card'){
      s1.style.display='none';s2.style.display='none';
      if(s3)s3.style.display='';
      $('abPayTitle').textContent='🎟️ 卡密开通';
      $('abPaySub').textContent='填入卡密，立即开通（无需等待管理员核对）';
      var el=$('abPayCard');if(el)setTimeout(function(){try{el.focus()}catch(e){}},80);
      var n0=$('abPayNote');if(n0){n0.textContent='';n0.className='ab-msg'}
      return;
    }
    s1.style.display='none';s2.style.display='';
    payQr();
  }
  function claimInvite(){
    var el=$('abPayInvite'),iv=(el&&el.value||'').trim(),note=$('abPayNote');
    if(!iv){note.textContent='请填写邀请码；没有邀请码请点下面的「直接开通（399 元）」';note.className='ab-msg err';return}
    note.textContent='正在核对邀请码…';note.className='ab-msg';
    request('/api/invite-claim',{invite:iv},localStorage.getItem(TOKEN_KEY)).then(function(r){
      var j=r.json||{};
      if(j.ok){
        if(ACCESS){ACCESS.invite_code=j.invite_code;ACCESS.price=j.price}
        payStep('qr');
        note.textContent='✅ 邀请码已生效，按 '+j.price+' 元开通'+(j.unit?('（'+j.unit+'）'):'');
        note.className='ab-msg ok';
      }else{note.textContent=j.error||'邀请码无效';note.className='ab-msg err'}
    }).catch(function(){note.textContent=netErr();note.className='ab-msg err'});
  }
  // ── 我已付款，提交核对（进后台待处理列表）（老板 2026-10-02）──
  function submitPaid(){
    var note=$('abPayNote'),el=$('abPayUserNote');
    var body={note:(el&&el.value||'').trim()};
    note.textContent='正在提交…';note.className='ab-msg';
    request('/api/pay-claim',body,localStorage.getItem(TOKEN_KEY)).then(function(r){
      var j=r.json||{};
      if(j.ok){
        if(j.already){note.textContent='该账号已是 VIP';note.className='ab-msg ok';refreshPay();return}
        note.innerHTML='✅ 已提交核对（应付 ￥'+j.amount+'）<br>管理员核对到账后即开通；开通后点「🔄 已开通？刷新状态」即可，不用重新登录。';
        note.className='ab-msg ok';
      }else{note.textContent=j.error||'提交失败';note.className='ab-msg err'}
    }).catch(function(){note.textContent=netErr();note.className='ab-msg err'});
  }
  // ── 卡密兑换：填码即开通（老板 2026-10-02）──
  function redeemCard(){
    var el=$('abPayCard'),code=(el&&el.value||'').trim(),note=$('abPayNote');
    if(!code){note.textContent='请填写卡密';note.className='ab-msg err';return}
    note.textContent='正在兑换…';note.className='ab-msg';
    request('/api/redeem-card',{code:code},localStorage.getItem(TOKEN_KEY)).then(function(r){
      var j=r.json||{};
      if(j.ok){
        note.textContent='✅ '+(j.message||'卡密兑换成功，VIP 已开通');
        note.className='ab-msg ok';
        if(j.access){ACCESS=j.access;setLock(false);applyAccess(j.access)}
        setTimeout(function(){
          try{alert('✅ 卡密兑换成功，VIP 已开通，欢迎继续使用！')}catch(e){}
          hidePay();
          try{location.reload()}catch(e){}
        },400);
      }else{note.textContent=j.error||'卡密无效';note.className='ab-msg err'}
    }).catch(function(){note.textContent=netErr();note.className='ab-msg err'});
  }
  // ── 常驻入口：资料弹窗里的「👑 开通 VIP」──
  function openPay(){
    try{profileModal(false)}catch(e){}
    try{paywall()}catch(e){}
  }
  function closePay(){hidePay()}
  // ── 账号资料（城市/学校/年级/姓名/性别 → 后台可见）──
  function profileEmpty(p){return !p||!(p.city||p.school||p.real_name)}
  function profileModal(show){
    var el=$('abProf');if(!el)return;
    if(!show){el.classList.add('ab-hide');return}
    var p=(ACCESS&&ACCESS.profile)||{};
    $('abPfCity').value=p.city||'';$('abPfSchool').value=p.school||'';$('abPfGrade').value=p.grade||'';
    $('abPfName').value=p.real_name||'';
    var g=document.querySelector('input[name="abPfGender"][value="'+(p.gender||'')+'"]');if(g)g.checked=true;
    $('abPfMsg').textContent='';$('abPfMsg').className='ab-msg';
    el.classList.remove('ab-hide');
  }
  function closeProfile(){profileModal(false)}
  function saveProfile(){
    var g=document.querySelector('input[name="abPfGender"]:checked'),note=$('abPfMsg');
    var body={city:$('abPfCity').value.trim(),school:$('abPfSchool').value.trim(),grade:$('abPfGrade').value,
              real_name:$('abPfName').value.trim(),gender:g?g.value:''};
    if(!body.city&&!body.school&&!body.real_name){note.textContent='至少填一项（城市/学校/姓名）再保存';note.className='ab-msg err';return}
    note.textContent='保存中…';note.className='ab-msg';
    request('/api/profile',body,localStorage.getItem(TOKEN_KEY)).then(function(r){
      var j=r.json||{};
      if(j.ok){if(ACCESS)ACCESS.profile=j.profile;note.textContent='✅ 已保存，谢谢！';note.className='ab-msg ok';
        setTimeout(function(){profileModal(false)},700);}
      else{note.textContent=j.error||'保存失败';note.className='ab-msg err'}
    }).catch(function(){note.textContent=netErr();note.className='ab-msg err'});
  }
  function paywall(){
    if(!ACCESS)return;
    showPay();
    if(!ACCESS.invite_code){payStep('invite');return}
    payStep('qr');
  }
  function payQr(){
    var box=$('abPayQrBox'),note=$('abPayNote');
    $('abPayAmt').textContent='￥'+(ACCESS?ACCESS.price:'--');
    $('abPaySub').textContent=ACCESS&&ACCESS.invite_code?('已用邀请码 '+ACCESS.invite_code+'，按优惠价 '+ACCESS.price+' 元开通'):('按标准价 '+(ACCESS?ACCESS.price:399)+' 元开通');
    note.textContent='正在读取收款码…';note.className='ab-msg';
    request('/api/payinfo',null,localStorage.getItem(TOKEN_KEY)).then(function(r){
      var j=r.json||{};
      if(j.amount)$('abPayAmt').textContent='￥'+j.amount;
      if(j.reason)$('abPaySub').textContent=j.reason;
      if(j.qr_ready&&j.qr_data){box.innerHTML='<img src="'+j.qr_data+'" alt="收款码">'}
      else{box.innerHTML='<div class="ab-qrhint">收款码还没上传：请管理员在后台「试用期与收款码」里上传图片<br>（当前应付 ￥'+((j.amount)||(ACCESS&&ACCESS.price))+'）</div>'}
      note.textContent=j.note||'付款后点「✅ 我已付款，提交核对」，我们核对到账后即开通；也可用卡密直接开通。';
      note.className='ab-msg ok';
    }).catch(function(){
      box.innerHTML='<div class="ab-qrhint">连不上服务器，收款码读不出来。<br>请检查网络后稍后重试。</div>';
      note.textContent=netErr();note.className='ab-msg err';
    });
  }
  function refreshPay(){
    var note=$('abPayNote');note.textContent='正在核对…';note.className='ab-msg';
    request('/api/me',null,localStorage.getItem(TOKEN_KEY)).then(function(r){
      var a=(r.json||{}).access;
      if(r.status===401){clear();hidePay();chip(null);show();msg('登录已失效，请重新登录');return}
      if(!a)return;
      if(!a.locked){
        ACCESS=a;setLock(false);hidePay();chip(JSON.parse(localStorage.getItem(USER_KEY)||'{}')||{username:'已登录'});
        note.textContent='';alert('✅ 已开通，欢迎继续使用！');
        try{location.reload()}catch(e){}
        return;
      }
      applyAccess(a);
      note.textContent='还没查到开通记录。已付款请点「✅ 我已付款，提交核对」，管理员核对到账后即开通；也可用卡密直接开通。';
      note.className='ab-msg err';
    }).catch(function(){note.textContent=netErr();note.className='ab-msg err'});
  }
  function placeBack(host){   // 【老板 2026-10-02】返回按钮固定在这一排最右
    var nb=$('navBack');if(nb&&host&&nb.parentNode!==host)host.appendChild(nb);
  }
  function placeChip(){
    var c=$('abUserChip');if(!c)return;
    // 【老板 2026-10-01】账号要跟「错题本/三层训练/复习要点」这排标签同一行、靠最右。
    var tabs=$('topTabs');
    if(tabs&&tabs.parentNode){
      var host=tabs.parentNode;
      host.style.flexWrap='wrap';                 // 极窄屏才换行；换行后依然靠右
      if(c.parentNode!==host) host.appendChild(c);
      placeBack(host);
      return;
    }
    var mn=$('mainNav'); if(!mn||!mn.parentNode) return;
    // 兜底（找不到标签行时）：原来的做法——第二行包一层 flex 行，右边放账号胶囊
    var row=document.querySelector('.ab-navrow');   // 【2026-10-02】全局找，避免重复调用套娃出新行
    if(!row){
      row=document.createElement('div'); row.className='ab-navrow';
      row.style.cssText='display:flex;align-items:center;gap:.5rem;flex-wrap:wrap;'
                       +'border-top:1px solid rgba(255,255,255,.18);padding-top:.35rem';
      mn.parentNode.insertBefore(row,mn);
      row.appendChild(mn);
      mn.style.borderTop='none'; mn.style.paddingTop='0';
    }
    if(c.parentNode!==row) row.appendChild(c);
    placeBack(row);
  }
  function chip(u){
    var c=$('abUserChip');if(!c)return;
    if(!u){c.style.display='none';var t0=$('abTrialTag');if(t0)t0.style.display='none';return}
    $('abUserName').textContent='👤 '+(u.display||u.username);
    placeChip();
    $('abOffTag').style.display=offline?'':'none';
    c.style.display='flex';
  }
  function save(token,user){
    try{localStorage.setItem(TOKEN_KEY,token);localStorage.setItem(USER_KEY,JSON.stringify(user))}catch(e){}
  }
  function clear(){try{localStorage.removeItem(TOKEN_KEY);localStorage.removeItem(USER_KEY)}catch(e){}}

  function login(){
    var u=$('abLoginUser').value.replace(/[\\s()（）-]/g,''),p=$('abLoginPass').value;
    if(!u)return msg('请填写手机号');
    $('abLoginBtn').disabled=true;msg('登录中…',true);
    request('/api/login',{username:u,password:p}).then(function(r){
      $('abLoginBtn').disabled=false;
      if(r.json&&r.json.ok){save(r.json.token,r.json.user);afterAuth(r.json.user,r.json.access);msg('登录成功',true)}
      else msg((r.json&&r.json.error)||'登录失败');
    }).catch(function(){ $('abLoginBtn').disabled=false; msg(netErr()) });
  }
  function register(){
    var u=$('abRegUser').value.replace(/[\\s()（）-]/g,''),p=$('abRegPass').value,p2=$('abRegPass2').value;
    if(!/^1[3-9]\\d{9}$/.test(u))return msg('请填写 11 位手机号（如 13800001111）');
    if(p.length<6)return msg('密码至少 6 位');
    if(p!==p2)return msg('两次输入的密码不一致');
    $('abRegBtn').disabled=true;msg('注册中…',true);
    request('/api/register',{username:u,password:p}).then(function(r){
      $('abRegBtn').disabled=false;
      if(r.json&&r.json.ok){save(r.json.token,r.json.user);afterAuth(r.json.user,r.json.access);msg('注册成功，免费试用开始',true)}
      else msg((r.json&&r.json.error)||'注册失败');
    }).catch(function(){ $('abRegBtn').disabled=false; msg(netErr()) });
  }
  function afterAuth(user,a){
    offline=false;chip(user);hide();if(a)applyAccess(a);
    window.setTimeout(function(){verify(user,0)},1500);
    afterAuthSync(user);
  }
  // 【账号隔离】登录后：① 首次登录记住「本机数据归属账号」；② 换账号则先问（防止把上一个
  //   账号的数据推到新账号云端）；③ 同账号则静默再同步一次，确保拿到本账号的云端数据。
  function afterAuthSync(user){
    var uname=(user&&user.username)||'';
    if(!uname)return;
    var owner='';
    try{owner=localStorage.getItem(OWNER_KEY)||''}catch(e){}
    if(!owner){
      try{localStorage.setItem(OWNER_KEY,uname)}catch(e){}
    }else if(owner!==uname){
      var go=confirm('⚠️ 本机数据属于账号 '+owner+NL+'当前登录：'+uname+NL+NL+'【确定】清空本机数据，改用当前账号的云端数据'+NL+'（建议先用「数据备份 → 导出备份」留底）'+NL+NL+'【取消】暂不切换：本机保持现状，也不会把这份数据传到当前账号云端');
      if(go){
        try{
          localStorage.removeItem('wrong_bank_data_test');            // 测试版主数据键（仅本页）
          localStorage.removeItem('wrong_bank_builtin_applied_test');  // 让内置快照按新账号重新判定
          localStorage.setItem(OWNER_KEY,uname);
        }catch(e){}
        location.reload();
        return;
      }
      return;   // 不切换 → 不做自动同步，两边数据都不被覆盖
    }
    window.setTimeout(function(){          // 同账号：静默再拉一次（登录前可能被 403 挡回）
      try{ if(typeof window.cloudInit==='function') window.cloudInit(false,true); }catch(e){}
    },900);
  }
  // ── 数据备份：导出 / 导入恢复（具体实现在页面里，这里只做入口与提示）──
  function bkMsg(t,cls){var e=$('abBkMsg');if(e){e.textContent=t||'';e.className='ab-msg '+(cls||'');e.style.textAlign='left'}}
  function exportData(){
    if(typeof window.exportBackup!=='function'){bkMsg('当前页面版本不支持导出，请更新到最新版','err');return}
    try{
      var r=window.exportBackup();
      if(r.where==='native') bkMsg('✅ 已保存到手机：'+r.path+'（共 '+r.counts.questions+' 道错题）'+NL+'可在「文件管理 → 下载 → AI错题本备份」里找到，可发微信或存网盘','ok');
      else if(r.where==='browser') bkMsg('✅ 已下载 '+r.name+'（共 '+r.counts.questions+' 道错题），请到浏览器下载目录查看','ok');
      else bkMsg('❌ 导出失败：'+(r.msg||'未知原因'),'err');
    }catch(e){bkMsg('❌ 导出失败：'+(e.message||e),'err')}
  }
  function importData(){
    if(typeof window.pickBackupFile!=='function'){bkMsg('当前页面版本不支持导入，请更新到最新版','err');return}
    bkMsg('请选择之前导出的 .json 备份文件（导入只增不减，不会覆盖现有错题）');
    try{window.pickBackupFile()}catch(e){bkMsg('❌ 打开文件选择器失败：'+(e.message||e),'err')}
  }
  // 后台核实凭证；偶发一次失败先重试，别在刚登录成功时就闪「离线」
  function verify(user,retry){
    request('/api/me',null,localStorage.getItem(TOKEN_KEY)).then(function(r){
      if(r.status===401){clear();chip(null);show();msg('登录已失效，请重新登录')}
      else if(r.status===403){clear();chip(null);show();msg((r.json&&r.json.error)||'账号已停用，请联系管理员')}
      else{offline=false;chip(user);applyAccess((r.json||{}).access)}
    }).catch(function(){
      if(retry<1){window.setTimeout(function(){verify(user,retry+1)},3000);return}
      offline=true;chip(user);
    });
  }
  function logout(){
    if(!confirm('确定退出登录？'))return;
    clear();chip(null);hidePay();api=null;
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
    window.addEventListener('resize',placeChip);
    setTimeout(placeChip,300);
    var tok=null,user=null;
    try{tok=localStorage.getItem(TOKEN_KEY);user=JSON.parse(localStorage.getItem(USER_KEY)||'null')}catch(e){}
    if(tok&&expireOf(tok)>Date.now()){
      // 有未过期凭证 ⇒ 先进去（离线可用），再后台向服务器核实
      afterAuth(user||{username:'已登录'});
    }else{
      show();
      if(location.protocol==='https:'&&!REMOTE_APIS.length)
        msg('网络暂时连不上，请稍后重试');
    }
    $('abLoginPass').addEventListener('keydown',function(e){if(e.key==='Enter')login()});
    $('abRegPass2').addEventListener('keydown',function(e){if(e.key==='Enter')register()});
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init);else init();
  return {login:login,register:register,openPay:openPay,submitPaid:submitPaid,redeemCard:redeemCard,logout:logout,tab:tab,init:init,refreshPay:refreshPay,applyAccess:applyAccess,paywall:paywall,payStep:payStep,claimInvite:claimInvite,closePay:closePay,profileModal:profileModal,saveProfile:saveProfile,closeProfile:closeProfile,placeChip:placeChip,exportData:exportData,importData:importData};
})();
</script>"""


GUARD_JS = """<script>
/* READONLY_GUARD_V1 · 到期未开通：能登录、能查看，不能新增错题（只加在测试版页面，学习中心不受影响） */
(function(){
  var LOCK=false;
  window.__AB_SETLOCK=function(v){LOCK=!!v};
  window.__AB_ISLOCK=function(){return LOCK};
  function hit(msg){
    if(!LOCK)return false;
    try{
      ABG.paywall();
      var why=document.getElementById('abPayWhy');
      if(why){why.textContent=msg||'免费试用已结束：可以查看已有错题，开通后才能新增。';why.style.display=''}
    }catch(e){ try{alert(msg)}catch(e2){} }
    return true;
  }
  var done=false;
  function boot(){
    if(done)return;done=true;
    var _n=window.navigate;
    if(typeof _n==='function'){
      window.navigate=function(p){
        if(p==='add'&&LOCK){hit('免费试用已结束：可以查看已有错题，开通后才能新增。');return}
        return _n.apply(this,arguments);
      };
    }
    var _s=window.submitAdd;
    if(typeof _s==='function'){
      window.submitAdd=function(){
        if(LOCK){hit('免费试用已结束：开通后才能新增错题。');return}
        return _s.apply(this,arguments);
      };
    }
    var _a=window.aiGenerate;
    if(typeof _a==='function'){
      window.aiGenerate=function(which){
        if(LOCK&&which!=='ed'){hit('免费试用已结束：开通后才能用 AI 新增错题。');return}
        return _a.apply(this,arguments);
      };
    }
  }
  boot();
  document.addEventListener('DOMContentLoaded',boot);
  window.addEventListener('load',boot);
  setTimeout(boot,800);
})();
</script>"""


def app_version():
    """App 版本号的单一来源：Android 工程里的 versionName（发新版改那一处即可）"""
    try:
        t = open('/home/administrator/android-build/make_aiwrongbook_project.py', encoding='utf-8').read()
        m = re.search(r'android:versionName="([0-9.]+)"', t)
        if m: return 'v' + m.group(1)
    except Exception:
        pass
    return 'v1.0'
APP_VER = app_version()


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
                 '<title>AI错题本 {APP_VER}</title>\n<base href="/xuci-jiancha/">\n' + FAVICON_TAGS, '独立版: 标题 + base + 图标')
    s = sub_once(s, '<a class="navbar-brand" href="index.html"><i class="fas fa-robot"></i> AI错题本</a>',
                 '<span class="navbar-brand"><i class="fas fa-robot"></i> AI错题本 {APP_VER}</span>', '独立版: 品牌链接去外链')
    s = sub_once(s, 'AI错题本 · 收录「错题本」「三层训练」「复习要点」三项功能',
                 'AI错题本 {APP_VER} · 收录「错题本」「三层训练」「复习要点」三项功能', '独立版: 页脚命名')
    # 独立版数据已隔离 ⇒ 文案不能说"与错题库共用同一份"（老板会误解为错题会同步过来）
    # 老板 2026-10-01：独立版页脚不要「数据独立存储，与学校错题库互不影响」这句 → 整行删掉（连分隔符）
    s = sub_once(s, '\n  &nbsp;|&nbsp; 数据与「错题库」共用同一份（本机存储 + 云端同步）', '',
                 '独立版: 删掉数据说明文案')
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

    # ---------- 测试版：新账号/新设备从「空白 + 例题示范」开始（老板 2026-10-01）----------
    # ⚠️ 只替换【测试版 / App】的内置快照；学习中心正式页 ai_wrongbook.html（若琳在用）一律不动。
    # ⚠️ 这里刻意不写若琳的真实题目、不带任何 uploads 图片；每道题都填好五维分析与三层训练，
    #    当「怎么用这个 App」的样板。用户可长按/编辑自行删除。
    DEMO_QUESTIONS = [
        {"key": "demo_math_eq_1", "subject": "数学", "chapter": "一元一次方程（解方程）",
         "content": "解方程：3(x − 2) + 1 = 2x − 5，则 x = ______。\n\n（示例题：可自行编辑或删除）",
         "correct_answer": "x = 0\n\n【解析】去括号：3x − 6 + 1 = 2x − 5\n左边合并：3x − 5 = 2x − 5\n移项：3x − 2x = −5 + 5\n所以 x = 0。\n（检验：左边 3(0−2)+1 = −5，右边 0−5 = −5，两边相等 ✓）",
         "my_answer": "x = 10（去括号时把 −6 写成了 +6）",
         "error_reason": "计算失误", "tags": "示例,数学,一元一次方程,去括号", "source": "练习", "difficulty": 1,
         "flow": {"known": "方程 3(x − 2) + 1 = 2x − 5", "target": "求 x 的值",
                  "plan": "去括号 → 合并同类项 → 移项 → 系数化为 1",
                  "check": "把 x = 0 代回原方程两边验算，左边 = 右边 ✓"},
         "ana5": {"known": "一个含 x 的一元一次方程；括号外有系数 3",
                  "ask": "求 x 的值",
                  "method": "先去括号（注意括号内每一项都要乘 3、符号要跟着变），再把含 x 的项移到一边、常数移到另一边，最后系数化为 1",
                  "pitfall": "去括号时 +1 没变号、−6 写成 +6；移项忘记变号",
                  "points": "一元一次方程的解法步骤：去括号 → 移项 → 合并同类项 → 系数化为 1；等式两边同加同减仍然相等"}},
        {"key": "demo_math_square_1", "subject": "数学", "chapter": "整式乘法（完全平方公式）",
         "content": "计算：(2a − 3b)² = ______。\n\n（示例题：可自行编辑或删除）",
         "correct_answer": "4a² − 12ab + 9b²\n\n【解析】完全平方公式 (x − y)² = x² − 2xy + y²\n取 x = 2a、y = 3b：\n(2a)² − 2·(2a)·(3b) + (3b)² = 4a² − 12ab + 9b²。\n（口诀：首平方、尾平方，首尾两倍中间放，中间符号看两个数的符号）",
         "my_answer": "4a² − 9b²（漏掉了中间项 −12ab）",
         "error_reason": "公式记错", "tags": "示例,数学,完全平方公式,整式乘法", "source": "练习", "difficulty": 2,
         "flow": {"known": "(2a − 3b)²，两个数相减后平方", "target": "展开成多项式",
                  "plan": "套完全平方公式 (x − y)² = x² − 2xy + y²，分别代入 x = 2a、y = 3b",
                  "check": "取 a = b = 1 验算：(2 − 3)² = 1，而 4 − 12 + 9 = 1 ✓"},
         "ana5": {"known": "(2a − 3b)²，即 (2a − 3b)(2a − 3b)",
                  "ask": "把这个式子展开",
                  "method": "用完全平方公式 (x − y)² = x² − 2xy + y² 直接展开，比逐项相乘快且不易错",
                  "pitfall": "最常见的是漏掉中间项 2xy，把 (a−b)² 错写成 a² − b²；另外别忘 (2a)² = 4a²",
                  "points": "完全平方公式；平方差公式 (x+y)(x−y) = x² − y² 的区别——前者三项、后者两项"}},
        {"key": "demo_phys_speed_1", "subject": "物理", "chapter": "机械运动（速度计算）",
         "content": "小明骑自行车 3 min 行驶了 900 m，他的平均速度是 ______ m/s，合 ______ km/h。\n\n（示例题：可自行编辑或删除）",
         "correct_answer": "5 m/s；18 km/h\n\n【解析】先统一单位：3 min = 3 × 60 s = 180 s。\nv = s / t = 900 m ÷ 180 s = 5 m/s。\n单位换算：1 m/s = 3.6 km/h ⇒ 5 × 3.6 = 18 km/h。",
         "my_answer": "300 m/s（时间直接用了 3，没有换算成秒）",
         "error_reason": "审题不清", "tags": "示例,物理,机械运动,速度计算,单位换算", "source": "练习", "difficulty": 2,
         "flow": {"known": "路程 s = 900 m，时间 t = 3 min", "target": "求平均速度（m/s，并换算成 km/h）",
                  "plan": "先把时间换算成秒 → 用 v = s/t 求 m/s → 再乘 3.6 换成 km/h",
                  "check": "5 m/s × 180 s = 900 m ✓ 与题目路程一致"},
         "ana5": {"known": "路程 900 m；时间 3 min（单位不是秒）",
                  "ask": "平均速度，且要两种单位",
                  "method": "速度公式 v = s / t；代入前必须统一单位，时间换成秒",
                  "pitfall": "直接用分钟代入算出 300 m/s；换算时乘除弄反（应乘 3.6 把 m/s 换成 km/h）",
                  "points": "速度的定义式 v = s/t；1 m/s = 3.6 km/h；平均速度不是各段速度的平均值"}},
        {"key": "demo_eng_verb_1", "subject": "英语", "chapter": "一般现在时（主谓一致）",
         "content": "用括号中所给词的适当形式填空：\nMy sister often ______ (go) to the library on Sundays.\n\n（示例题：可自行编辑或删除）",
         "correct_answer": "goes\n\n【解析】主语 My sister 是第三人称单数，句子为一般现在时，动词要用第三人称单数形式：go → goes。\n（标志词 often / usually / every day / on Sundays 都提示一般现在时；主语为 he/she/it 或单个的人时，动词加 -s/-es。）",
         "my_answer": "go（主语是三单，动词忘了加 -es）",
         "error_reason": "概念不清", "tags": "示例,英语,一般现在时,主谓一致,三单", "source": "练习", "difficulty": 1,
         "flow": {"known": "主语 My sister；时间状语 often / on Sundays；动词 go", "target": "把 go 变成正确形式",
                  "plan": "先判断时态（often/on Sundays → 一般现在时）→ 再看主语人称（My sister → 三单）→ 动词加 -es",
                  "check": "句子读一遍：My sister often goes to the library. 主谓一致 ✓"},
         "ana5": {"known": "主语 My sister（第三人称单数）；频度副词 often；时间状语 on Sundays",
                  "ask": "用 go 的适当形式填空",
                  "method": "先定时态（一般现在时），再定形式（主语三单 → 动词加 -s/-es）",
                  "pitfall": "只看动词不看主语，直接写 go；以 o/s/x/ch/sh 结尾要加 -es（go → goes）",
                  "points": "一般现在时的用法与标志词；第三人称单数动词变化规则"}},
        {"key": "demo_chin_idiom_1", "subject": "语文", "chapter": "字音字形（成语辨析）",
         "content": "下列词语中，没有错别字的一项是（　　）\nA. 骸人听闻　B. 人声鼎沸　C. 锋芒必露　D. 翻来复去\n\n（示例题：可自行编辑或删除）",
         "correct_answer": "B（人声鼎沸）\n\n【解析】逐项改正：\nA. 「骸人听闻」应为「骇人听闻」（骇：惊吓、震惊）；\nC. 「锋芒必露」应为「锋芒毕露」（毕：完全）；\nD. 「翻来复去」应为「翻来覆去」（覆：翻过来）。\n只有 B「人声鼎沸」书写正确——鼎沸：像锅里的水沸腾一样，形容人声嘈杂。",
         "my_answer": "C（形近字分不清，「必」与「毕」混用）",
         "error_reason": "概念不清", "tags": "示例,语文,字形,成语,形近字", "source": "练习", "difficulty": 2,
         "flow": {"known": "四个成语，其中三项含错别字", "target": "找出没有错别字的一项",
                  "plan": "逐项回忆成语本义，用字义反推正确写法，排除错项",
                  "check": "把改正后的四个成语写一遍，确认字形无误"},
         "ana5": {"known": "四个成语选项，只有一项完全正确",
                  "ask": "选出书写没有错误的一项",
                  "method": "逐字理解成语含义：字义对了，字形就错不了（骇=震惊、毕=完全、覆=翻转）",
                  "pitfall": "只凭印象读通就下判断；形近字（骸/骇、必/毕、复/覆）容易混",
                  "points": "常见成语的正确写法；形近字辨析；成语的意思与感情色彩"}},
    ]
    _demo_js = json.dumps(DEMO_QUESTIONS, ensure_ascii=False, indent=0)
    _a = s.index('const BUILTIN_QUESTIONS=[')
    _b = s.index('\n];', _a) + len('\n];')
    s = s[: _a] + 'const BUILTIN_QUESTIONS=' + _demo_js + ';' + s[_b:]
    print(f'  · 测试版: 内置快照已替换为 {len(DEMO_QUESTIONS)} 道通用例题（新账号从空白+例题开始；正式页不受影响）')

    # ---------- 测试版：错题保持原样，只是「以后新增的不进来」（老板 2026-09-27）----------
    # 「新增不进测试版」由「键隔离 + 后端隔离」天然保证：生产页面录入只写生产库，测试版后端是独立文件，拉不到新题。
    # BUILTIN_QUESTIONS 是**静态快照**（不随生产库变化）⇒ 保留，不要清空（老板：「测试版内的错题就不动了」）。
    n_builtin = _count_builtin(s)
    print(f'  · 测试版: 内置快照（通用例题）{n_builtin} 条（新账号从空白+例题开始；正式页不受影响）')

    # ---------- 登录门禁（老板 2026-10-01）：测试版必须先注册/登录才能使用 ----------
    # 账号服务跑在家里的私有云 iStoreOS(192.168.3.3:8090)，只作用于本测试版页面
    s = sub_once(s, '<base href="/xuci-jiancha/">',
                 '<base href="/xuci-jiancha/">' + AUTH_CSS, '登录门禁: 样式')
    tun = tunnel_url()
    auth_js = AUTH_JS if not tun else AUTH_JS.replace(
        'var REMOTE_APIS=[];', 'var REMOTE_APIS=[' + json.dumps(tun) + '];')
    print(f'  · 外网登录通道: {tun or "（无隧道，仅内网 + App 可用）"}')
    s = sub_once(s, '</body>', AUTH_OVERLAY + auth_js + GUARD_JS + '\n</body>', '登录门禁: 登录页 + 脚本 + 只读守卫')

    os.makedirs(STANDALONE_DIR, exist_ok=True)
    # 版本号占位符统一替换（来源 = Android versionName）
    s = s.replace('{APP_VER}', APP_VER)
    print('  版本号：' + APP_VER)

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
        ('顶部三标签已取消（老板 2026-10-02）',
         h.count('data-top=') == 0 and 'id="topTabs"' not in h and 'class="top-tab' not in h),
        ('复习要点页保留（renderPoints 富页面）', 'function renderPoints' in h and 'function rvfPanel' in h),
        ('顶层三数组未动', h.count('const BUILTIN_QUESTIONS=[') == 1),
    ]
    ok = True
    for name, cond in checks:
        print(('  ✓ ' if cond else '  ✗ ') + name)
        ok = ok and cond
    n_q = len(re.findall(r'\{q:', h)) + h.count('content:')
    print(f'  参考：BUILTIN 题数 = {_count_builtin(h)}')
    return 0 if ok else 2


if __name__ == '__main__':
    sys.exit(main())

