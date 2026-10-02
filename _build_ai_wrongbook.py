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
      else{tag.title='';tag.textContent='试用剩 '+a.days_left+' 天';tag.className='ab-trial';tag.onclick=null;tag.style.display=''}
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
  return {login:login,register:register,submitPaid:submitPaid,redeemCard:redeemCard,logout:logout,tab:tab,init:init,refreshPay:refreshPay,applyAccess:applyAccess,paywall:paywall,payStep:payStep,claimInvite:claimInvite,closePay:closePay,profileModal:profileModal,saveProfile:saveProfile,closeProfile:closeProfile,placeChip:placeChip,exportData:exportData,importData:importData};
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
                 '<title>AI错题本 {APP_VER}</title>\n<base href="/xuci-jiancha/">', '独立版: 标题 + base')
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
