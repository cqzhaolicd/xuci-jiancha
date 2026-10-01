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
.ab-trial.lock{background:#fed7d7;color:#c53030;cursor:pointer}
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
    </div>
    <div id="abPayStep2" style="display:none">
      <div id="abPayAmt" style="font-size:1.7rem;font-weight:800;color:#e53e3e;margin:8px 0">￥--</div>
      <div id="abPayQrBox" style="margin:10px 0;min-height:60px"></div>
      <button class="ab-btn" onclick="ABG.refreshPay()">我已付款，刷新状态</button>
      <button class="ab-btn2" onclick="ABG.payStep('invite')">返回上一步（我有邀请码）</button>
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
      if(a.paid){tag.textContent='VIP·已开通';tag.className='ab-trial';tag.onclick=null;tag.style.display=''}
      else if(a.expired){tag.textContent='试用已结束 · 点此开通';tag.className='ab-trial lock';tag.onclick=function(){paywall()};tag.style.display=''}
      else{tag.textContent='试用剩 '+a.days_left+' 天';tag.className='ab-trial';tag.onclick=null;tag.style.display=''}
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
    var s1=$('abPayStep1'),s2=$('abPayStep2');
    if(!s1||!s2)return;
    if(step==='invite'){
      s1.style.display='';s2.style.display='none';
      $('abPayTitle').textContent='⏰ 免费试用已结束';
      $('abPaySub').textContent='有邀请码可享 299 元优惠价；没有也能按 399 元直接开通';
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
      note.textContent=j.note||'付款后请联系管理员开通';
      note.className='ab-msg ok';
    }).catch(function(){
      box.innerHTML='<div class="ab-qrhint">连不上服务器，收款码读不出来。<br>请确认设备连着家里 WiFi，或稍后重试。</div>';
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
      note.textContent='还没查到开通记录。付款后请联系管理员在后台点「升级为VIP」，再点本按钮刷新。';
      note.className='ab-msg err';
    }).catch(function(){note.textContent=netErr();note.className='ab-msg err'});
  }
  function placeChip(){
    var c=$('abUserChip');if(!c)return;
    var mn=$('mainNav'); if(!mn||!mn.parentNode) return;
    // 第二行包一层 flex 行：左边是 #mainNav（首页/录入/复习/打印/分析），右边是账号胶囊
    var row=mn.parentNode.querySelector('.ab-navrow');
    if(!row){
      row=document.createElement('div'); row.className='ab-navrow';
      row.style.cssText='display:flex;align-items:center;gap:.5rem;flex-wrap:wrap;'
                       +'border-top:1px solid rgba(255,255,255,.18);padding-top:.35rem';
      mn.parentNode.insertBefore(row,mn);
      row.appendChild(mn);
      mn.style.borderTop='none'; mn.style.paddingTop='0';
    }
    if(c.parentNode!==row) row.appendChild(c);
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
        msg('当前是 https 网页访问，浏览器会拦截内网请求；请用 App 或家里的内网地址登录');
    }
    $('abLoginPass').addEventListener('keydown',function(e){if(e.key==='Enter')login()});
    $('abRegPass2').addEventListener('keydown',function(e){if(e.key==='Enter')register()});
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init);else init();
  return {login:login,register:register,logout:logout,tab:tab,init:init,refreshPay:refreshPay,applyAccess:applyAccess,paywall:paywall,payStep:payStep,claimInvite:claimInvite,closePay:closePay,profileModal:profileModal,saveProfile:saveProfile,closeProfile:closeProfile,placeChip:placeChip};
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
