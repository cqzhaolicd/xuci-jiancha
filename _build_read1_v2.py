#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""21世纪报阅读页模板改造 v2（老师要求）：
   tab1 知识图谱 → 文章全文
   tab2 闯关测验 → 带答案全文（文章+答案+解析+做题方法；底部保留选做自测）
   tab3 知识卡牌 → 词汇积累（14 条）
   tab4 易错自检 → 段落总结 + 思维导图（重点：培养阅读思维）
基座：english26q_read1_interactive.html v1（已上线，git 有备份）
"""
import re

FN = 'english26q_read1_interactive.html'
h = open(FN, encoding='utf-8').read()
orig_len = len(h)
report = []

# 已改造过则退出，避免重复替换
if '段落总结与思维导图' in h:
    print('⚠️ 该页已是 v2，如需重建请先 git checkout -- %s' % FN)
    raise SystemExit(1)


def rep(old, new, tag, count=1):
    global h
    n = h.count(old)
    if n != count:
        report.append(f'FAIL[{tag}]: expected {count} got {n}')
        return False
    h = h.replace(old, new)
    report.append(f'OK[{tag}]')
    return True


def seg(start, end, new_seg, tag):
    global h
    i = h.find(start)
    if i < 0:
        report.append(f'FAIL[{tag}]: start not found')
        return False
    j = h.find(end, i + len(start))
    if j < 0:
        report.append(f'FAIL[{tag}]: end not found')
        return False
    h = h[:i] + new_seg + h[j:]
    report.append(f'OK[{tag}]')
    return True


# ============================================================
# ① 标题 / navbar / hero / 统计
# ============================================================
rep('<title>🤖 AI 陪伴机器人新规 · 英语阅读互动学习</title>',
    '<title>📖 AI 陪伴机器人新规 · 英语阅读（全文 + 段落总结 + 思维导图）</title>', 'title')
rep('</i> 英语阅读 · 第1周</a>', '</i> 英语阅读 · 第1周（21世纪报）</a>', 'navbar-brand')
rep('<i class="fas fa-newspaper"></i> AI 陪伴机器人新规 · 英语阅读互动学习',
    '<i class="fas fa-book-open-reader"></i> AI 陪伴机器人新规 · 全文精读与阅读思维', 'hero-h1')
rep('<p>2026秋 八年级第一周 · 21世纪报带读课 · 28 题 · 12 卡牌 | 英语阅读</p>',
    '<p>2026秋 八年级第一周 · 21世纪报带读课 · 全文 + 答案 + 词汇 + 段落总结/思维导图</p>', 'hero-sub')
rep('<i class="fas fa-check-circle" style="color:var(--success)"></i> 28道测验题',
    '<i class="fas fa-file-alt" style="color:var(--success)"></i> 文章全文（5 段）', 'meta-1')
rep('<i class="fas fa-layer-group"></i> 12张知识卡</span>',
    '<i class="fas fa-layer-group"></i> 14 条词汇积累</span>', 'meta-2')
rep('<i class="fas fa-exclamation-triangle" style="color:var(--danger)"></i> 6大易错点</span>',
    '<i class="fas fa-project-diagram" style="color:var(--danger)"></i> 段落总结 + 思维导图</span>', 'meta-3')
rep('<span><i class="fas fa-microphone"></i> 点击卡片翻转</span>',
    '<span><i class="fas fa-pen"></i> 底部选做自测 28 题</span>', 'meta-4')

# navbar 导航文案
rep('><span>知识点</span>', '><span>全文</span>', 'nav-1')
rep('><span>测验</span>', '><span>答案</span>', 'nav-2')
rep('><span>重练</span>', '><span>自测</span>', 'nav-3')
rep('><span>卡片</span>', '><span>词汇</span>', 'nav-4')
rep('><span>易错点</span>', '><span>总结</span>', 'nav-5')

# tab 按钮文案
rep('<i class="fas fa-sitemap"></i> 知识图谱', '<i class="fas fa-file-alt"></i> 文章全文', 'tabbtn-1')
rep('<i class="fas fa-pen"></i> 闯关测验', '<i class="fas fa-clipboard-check"></i> 带答案全文', 'tabbtn-2')
rep('<i class="fas fa-layer-group"></i> 知识卡牌', '<i class="fas fa-spell-check"></i> 词汇积累', 'tabbtn-3')
rep('<i class="fas fa-exclamation-triangle"></i> 易错自检', '<i class="fas fa-project-diagram"></i> 段落总结·思维导图', 'tabbtn-4')

# ============================================================
# ② tab1：文章全文
# ============================================================
ART = '''<div class="section-header"><i class="fas fa-file-alt" style="color:#667eea"></i> 文章全文 · Protecting users（21世纪报 八年级 · 约 300 词）</div>
    <div style="background:var(--card,#fff);border-radius:12px;padding:1.2rem 1.5rem;box-shadow:0 2px 12px rgba(0,0,0,.06);line-height:2;font-size:.95rem">
      <h3 style="margin:0 0 .3rem;font-size:1.15rem">China makes new rules for AI companion bots</h3>
      <p style="margin:0 0 1rem;color:var(--text-light);font-size:.85rem">AI 陪伴机器人有了「紧箍咒」 · 配图来源 TUCHONG · 建议朗读 3 遍，第 3、5 段精读</p>

      <div style="border-left:4px solid #667eea;padding-left:.9rem;margin-bottom:1.1rem">
        <strong style="color:#667eea;font-size:.85rem">Para 1 · 提出问题（抛问题引入）</strong>
        <p style="margin:.35rem 0 0">If you talked to an AI bot a lot, would you start to see it as a real friend and <strong>depend on</strong> it too much? The government has <strong>introduced</strong> new rules for AI companion bots (陪伴型机器人).</p>
      </div>

      <div style="border-left:4px solid #3498db;padding-left:.9rem;margin-bottom:1.1rem">
        <strong style="color:#3498db;font-size:.85rem">Para 2 · 摆出现象（问题是什么）</strong>
        <p style="margin:.35rem 0 0">These bots, <strong>either</strong> in the form of a toy <strong>or</strong> an app, have become a part of many people's daily lives. They are always friendly and patient. Some young people spend a lot of time with them and <strong>pull away from</strong> real-life friends, Wang Zhechen from Fudan University told <em>China Daily</em>.</p>
      </div>

      <div style="border-left:4px solid #e67e22;padding-left:.9rem;margin-bottom:1.1rem">
        <strong style="color:#e67e22;font-size:.85rem">Para 3 · 新规一（限时与提醒）</strong>
        <p style="margin:.35rem 0 0">To fix this, the new rules say AI bots can't encourage people to use them for too long. They must show pop-up messages <strong>reminding people to take a break</strong> after two hours. If people start to see AI as a real friend, the system should also make the difference clear: "This is a machine, not a real person," expert Liu Xiaochun explained to <em>China Daily</em>.</p>
      </div>

      <div style="border-left:4px solid #27ae60;padding-left:.9rem;margin-bottom:1.1rem">
        <strong style="color:#27ae60;font-size:.85rem">Para 4 · 新规二（安全与友善）</strong>
        <p style="margin:.35rem 0 0">The rules also require (要求) AI bots to be safe and kind. They can't <strong>tell lies</strong>, share <strong>private information</strong> or do anything that could harm <strong>national security</strong> (国家安全). For example, imagine you have a bad day and tell AI, "I'm sad." In the past, AI might use information about your feelings to show you ads (广告) for toys or candy. <strong>Now, the rules stop this.</strong></p>
      </div>

      <div style="border-left:4px solid #8e44ad;padding-left:.9rem">
        <strong style="color:#8e44ad;font-size:.85rem">Para 5 · 新规三（青少年模式）</strong>
        <p style="margin:.35rem 0 0">If you're under 18 and open an AI app, <strong>teen mode</strong> (青少年模式) will turn on by itself. Your parents can <strong>check how long you chat</strong>. At the same time, AI won't give you unsafe advice just to make you happy.</p>
      </div>

      <div style="margin-top:1.3rem;padding-top:1rem;border-top:1px dashed #e2e8f0">
        <strong style="color:#e74c3c;font-size:.88rem">✍️ 文末任务 · Tools or friends?</strong>
        <p style="margin:.35rem 0 0">Design a survey and ask <strong>more than 10 classmates</strong> about their experiences with AI companion bots. After the survey, write a short report (<strong>about 150–200 words</strong>) answering these two questions:</p>
        <p style="margin:.35rem 0 0">1. Do most of your classmates see AI bots as helpful tools or as real friends?<br>2. Based on what you have found, do you agree with the new rules mentioned in the article? Explain why.</p>
      </div>
    </div>
    </div>
    '''
seg('<div id="tab-knowledge" class="tab-content active">', '<div id="tab-quiz" class="tab-content">',
    '<div id="tab-knowledge" class="tab-content active">\n    ' + ART, 'tab1-article')

# ============================================================
# ③ tab2：带答案全文
# ============================================================
ANS = '''<div class="section-header"><i class="fas fa-clipboard-check" style="color:#27ae60"></i> 带答案全文 · 文章 + 题目 + 答案 + 解析</div>
    <div style="background:var(--card,#fff);border-radius:12px;padding:1.2rem 1.5rem;box-shadow:0 2px 12px rgba(0,0,0,.06);line-height:1.95;font-size:.95rem">

      <h3 style="margin:0 0 .5rem;font-size:1.05rem;color:#667eea">一、文章原文（含答案版标注）</h3>
      <p style="margin:.3rem 0">If you talked to an AI bot a lot, would you start to see it as a real friend and <strong>depend on</strong> it too much? The government has <strong>introduced</strong> new rules for AI companion bots (陪伴型机器人).</p>
      <p style="margin:.3rem 0">These bots, <strong>either</strong> in the form of a toy <strong>or</strong> an app, have become a part of many people's daily lives. They are always friendly and patient. Some young people spend a lot of time with them and <strong>pull away from</strong> real-life friends, Wang Zhechen from Fudan University told <em>China Daily</em>.</p>
      <p style="margin:.3rem 0">To fix this, the new rules say AI bots can't encourage people to use them for too long. They must show pop-up messages <strong>reminding people to take a break</strong> after two hours. If people start to see AI as a real friend, the system should also make the difference clear: "This is a machine, not a real person," expert Liu Xiaochun explained to <em>China Daily</em>.</p>
      <p style="margin:.3rem 0">The rules also require (要求) AI bots to be safe and kind. They can't <strong>tell lies</strong>, share <strong>private information</strong> or do anything that could harm <strong>national security</strong> (国家安全). For example, imagine you have a bad day and tell AI, "I'm sad." In the past, AI might use information about your feelings to show you ads (广告) for toys or candy. <strong>Now, the rules stop this.</strong></p>
      <p style="margin:.3rem 0">If you're under 18 and open an AI app, <strong>teen mode</strong> (青少年模式) will turn on by itself. Your parents can <strong>check how long you chat</strong>. At the same time, AI won't give you unsafe advice just to make you happy.</p>

      <h3 style="margin:1.4rem 0 .5rem;font-size:1.05rem;color:#27ae60">二、题目与答案</h3>
      <div style="background:#f7fbf8;border-radius:10px;padding:.9rem 1.1rem;margin-bottom:.8rem">
        <p style="margin:0 0 .4rem"><strong>Read and choose</strong></p>
        <p style="margin:.25rem 0"><strong>1.</strong> 主旨 → <strong style="color:#27ae60">B. China introduced new rules for AI companion bots.</strong><br><span style="color:var(--text-light);font-size:.88rem">解析：C 只是第 2 段的细节现象，范围太窄；D 与原文矛盾（未满 18 岁是开启青少年模式，不是禁止使用）。</span></p>
        <p style="margin:.25rem 0"><strong>2.</strong> What problem do some young people have? → <strong style="color:#27ae60">When they spend a lot of time with AI bots, they pull away from their real-life friends.</strong></p>
        <p style="margin:.25rem 0"><strong>3.</strong> 两小时后 AI 必须做什么 → <strong style="color:#27ae60">C. Tell people to take a rest.</strong><br><span style="color:var(--text-light);font-size:.88rem">解析：原文 take a break ↔ 选项 take a rest（<strong>同义替换</strong>）；D 属另一条规定，张冠李戴。</span></p>
        <p style="margin:.25rem 0"><strong>4.</strong> 未满 18 岁打开 AI App → <strong style="color:#27ae60">Teen mode will turn on by itself.</strong></p>
      </div>
      <div style="background:#fff8f7;border-radius:10px;padding:.9rem 1.1rem;margin-bottom:.8rem">
        <p style="margin:0 0 .4rem"><strong>True or False</strong></p>
        <p style="margin:.25rem 0"><strong>5.</strong> AI bots are allowed to tell white lies. → <strong style="color:#e74c3c">F</strong>　<span style="font-size:.88rem;color:var(--text-light)">can't tell lies，没有「善意谎言」的例外</span></p>
        <p style="margin:.25rem 0"><strong>6.</strong> AI bots cannot share users' private information. → <strong style="color:#27ae60">T</strong></p>
        <p style="margin:.25rem 0"><strong>7.</strong> It's okay for AI to send people ads based on their feelings. → <strong style="color:#e74c3c">F</strong>　<span style="font-size:.88rem;color:var(--text-light)">Now, the rules stop this（过去可以 → 现在禁止）</span></p>
      </div>
      <div style="background:#f7f9ff;border-radius:10px;padding:.9rem 1.1rem">
        <p style="margin:0 0 .4rem"><strong>Words in use（选词填空答案）</strong></p>
        <p style="margin:.25rem 0">1. Don't <strong style="color:#27ae60">depend on</strong> AI too much. It is not always right.</p>
        <p style="margin:.25rem 0">2. The government <strong style="color:#27ae60">introduced</strong> new rules for AI companion bots last year.</p>
        <p style="margin:.25rem 0">3. If you stay online all day long, you may <strong style="color:#27ae60">pull away from</strong> your family and friends.</p>
        <p style="margin:.25rem 0">4. It's wrong for teenagers <strong style="color:#27ae60">to tell lies</strong>. Honesty is the best policy.</p>
        <p style="margin:.25rem 0">5. This pop-up message <strong style="color:#27ae60">reminds</strong> users <strong style="color:#27ae60">to</strong> take a break after two hours.</p>
      </div>

      <h3 style="margin:1.4rem 0 .5rem;font-size:1.05rem;color:#e67e22">三、做题方法（点到为止 · 详见「段落总结·思维导图」）</h3>
      <div style="background:#fffaf3;border-left:4px solid #f39c12;border-radius:10px;padding:.9rem 1.1rem;font-size:.9rem">
        <p style="margin:.2rem 0">① <strong>主旨题</strong>：先看首段提问 + 各段首句，选「能管住全文」的项，别选某段细节。</p>
        <p style="margin:.2rem 0">② <strong>细节题</strong>：题干关键词（two hours / under 18）回原文定位，答案多在<strong>同义替换</strong>里（take a break = take a rest）。</p>
        <p style="margin:.2rem 0">③ <strong>判断题</strong>：盯 <strong>Now / But / In the past</strong> 等转折词；出现 all / must / never 等绝对化表述先打问号。</p>
        <p style="margin:.2rem 0">④ <strong>词义题</strong>：把词组放回原句推意思（pull away from → 由「花大量时间陪 AI」推「疏远」）。</p>
      </div>

      <h3 style="margin:1.6rem 0 .4rem;font-size:1.05rem;color:#8e44ad">四、选做自测（28 题互动闯关 · 答错自动进错题库）</h3>
      <p style="margin:0 0 .8rem;color:var(--text-light);font-size:.86rem">老师建议：题只用来检验方法，重点放在上一栏的段落总结与思维导图。</p>
    </div>
    '''
seg('<div id="tab-quiz" class="tab-content">', '<div class="quiz-mode-bar" id="quizModeBar">',
    '<div id="tab-quiz" class="tab-content">\n    ' + ANS, 'tab2-answers')

# ============================================================
# ④ tab3：词汇积累（卡片数量文案）
# ============================================================
rep('点击卡片翻转查看答案 · 共12张知识卡', '点击卡片翻转 · 共 14 条词汇积累（正面词组 → 背面释义+原句+例句）', 'flash-hint')

# ============================================================
# ⑤ tab4：段落总结 + 思维导图
# ============================================================
MAP = '''<div class="section-header"><i class="fas fa-project-diagram" style="color:#e74c3c"></i> 段落总结与思维导图（老师重点 · 培养阅读思维）</div>
    <p style="color:var(--text-light);margin-bottom:.9rem;font-size:.88rem">读文章先搭骨架：<strong>现象 → 新规（三条）→ 举例 → 任务</strong>。看懂结构，主旨题和细节题都能秒定位。</p>

    <div style="background:var(--card,#fff);border-radius:12px;padding:1rem;box-shadow:0 2px 12px rgba(0,0,0,.06);overflow-x:auto">
      <svg viewBox="0 0 875 575" style="width:100%;min-width:660px;height:auto;font-family:inherit">
        <defs>
          <marker id="arw" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto">
            <path d="M0,0 L8,4 L0,8 z" fill="#b7c3d6"/>
          </marker>
        </defs>
        <!-- 连接线 -->
        <path d="M225,290 C255,290 265,62 295,62" stroke="#b7c3d6" stroke-width="1.6" fill="none" marker-end="url(#arw)"/>
        <path d="M225,290 L295,280" stroke="#b7c3d6" stroke-width="1.6" fill="none" marker-end="url(#arw)"/>
        <path d="M225,290 C255,290 265,502 295,502" stroke="#b7c3d6" stroke-width="1.6" fill="none" marker-end="url(#arw)"/>
        <path d="M495,62 C525,62 535,38 565,38" stroke="#b7c3d6" stroke-width="1.4" fill="none" marker-end="url(#arw)"/>
        <path d="M495,62 C525,62 535,100 565,100" stroke="#b7c3d6" stroke-width="1.4" fill="none" marker-end="url(#arw)"/>
        <path d="M495,280 C525,280 535,196 565,196" stroke="#b7c3d6" stroke-width="1.4" fill="none" marker-end="url(#arw)"/>
        <path d="M495,280 L565,258" stroke="#b7c3d6" stroke-width="1.4" fill="none" marker-end="url(#arw)"/>
        <path d="M495,280 C525,280 535,320 565,320" stroke="#b7c3d6" stroke-width="1.4" fill="none" marker-end="url(#arw)"/>
        <path d="M495,502 C525,502 535,466 565,466" stroke="#b7c3d6" stroke-width="1.4" fill="none" marker-end="url(#arw)"/>
        <path d="M495,502 C525,502 535,528 565,528" stroke="#b7c3d6" stroke-width="1.4" fill="none" marker-end="url(#arw)"/>
        <!-- 中心 -->
        <rect x="20" y="245" width="205" height="90" rx="14" fill="#667eea"/>
        <text x="122" y="282" text-anchor="middle" fill="#fff" font-size="14" font-weight="700">AI 陪伴机器人新规</text>
        <text x="122" y="306" text-anchor="middle" fill="#e8ecff" font-size="12">Protecting users</text>
        <!-- 一级 -->
        <rect x="295" y="30" width="200" height="64" rx="10" fill="#e8f1fd" stroke="#3498db" stroke-width="1.4"/>
        <text x="395" y="56" text-anchor="middle" fill="#1f6fb2" font-size="13" font-weight="700">① 现象：过度依赖</text>
        <text x="395" y="76" text-anchor="middle" fill="#31658c" font-size="11.5">pull away from friends</text>
        <rect x="295" y="248" width="200" height="64" rx="10" fill="#fdeee0" stroke="#e67e22" stroke-width="1.4"/>
        <text x="395" y="274" text-anchor="middle" fill="#a8590a" font-size="13" font-weight="700">② 新规三条（核心）</text>
        <text x="395" y="294" text-anchor="middle" fill="#8a5a1e" font-size="11.5">the new rules</text>
        <rect x="295" y="470" width="200" height="64" rx="10" fill="#f0e9fb" stroke="#8e44ad" stroke-width="1.4"/>
        <text x="395" y="496" text-anchor="middle" fill="#6c3d99" font-size="13" font-weight="700">③ 输出任务</text>
        <text x="395" y="516" text-anchor="middle" fill="#6c3d99" font-size="11.5">survey report</text>
        <!-- 二级 -->
        <rect x="565" y="12" width="290" height="52" rx="8" fill="#f7fbff" stroke="#c9dcf0"/>
        <text x="578" y="43" fill="#2c3e50" font-size="12.5">复旦王哲晨：陪伴太久 → 疏远真人朋友</text>
        <rect x="565" y="74" width="290" height="52" rx="8" fill="#f7fbff" stroke="#c9dcf0"/>
        <text x="578" y="105" fill="#2c3e50" font-size="12.5">形态：either a toy or an app</text>
        <rect x="565" y="170" width="290" height="52" rx="8" fill="#fffaf3" stroke="#f0d3ae"/>
        <text x="578" y="201" fill="#2c3e50" font-size="12.5">① 限时：2 小时弹窗提醒休息</text>
        <rect x="565" y="232" width="290" height="52" rx="8" fill="#fffaf3" stroke="#f0d3ae"/>
        <text x="578" y="263" fill="#2c3e50" font-size="12.5">② 禁止：撒谎 / 泄隐私 / 危害国安</text>
        <rect x="565" y="294" width="290" height="52" rx="8" fill="#fffaf3" stroke="#f0d3ae"/>
        <text x="578" y="325" fill="#2c3e50" font-size="12.5">③ 青少年模式：未满 18 自动开启</text>
        <rect x="565" y="440" width="290" height="52" rx="8" fill="#faf7fe" stroke="#ddc9f0"/>
        <text x="578" y="471" fill="#2c3e50" font-size="12.5">调查 ≥10 位同学：工具 or 朋友？</text>
        <rect x="565" y="502" width="290" height="52" rx="8" fill="#faf7fe" stroke="#ddc9f0"/>
        <text x="578" y="533" fill="#2c3e50" font-size="12.5">150–200 词，必须给理由</text>
        <!-- 阅读思维标注 -->
        <text x="20" y="40" fill="#8b95a5" font-size="12" font-weight="700">阅读思维：先抓结构，再定细节</text>
        <text x="20" y="60" fill="#a6adba" font-size="11">现象 → 对策 → 举例 → 任务</text>
      </svg>
    </div>

    <div class="section-header" style="margin-top:1.4rem"><i class="fas fa-list-ol" style="color:#667eea"></i> 段落总结（5 段 · 一段一句读透）</div>
    <div class="knowledge-grid">
      <div class="knowledge-card c1"><h3><i class="fas fa-question-circle" style="color:#667eea"></i> Para 1 · 提出问题</h3><ul>
        <li><strong class="hl">主旨句</strong>：If you talked to an AI bot a lot, would you start to see it as a real friend…?</li>
        <li>写法：<strong class="hl">抛问题 + 给答案（政府出新规）</strong></li>
        <li>段落作用：引出话题，预告全文讲「新规」</li>
      </ul></div>
      <div class="knowledge-card c2"><h3><i class="fas fa-user-friends" style="color:#3498db"></i> Para 2 · 摆现象</h3><ul>
        <li><strong class="hl">主旨句</strong>：Some young people spend a lot of time with them and pull away from real-life friends.</li>
        <li>支撑：AI 玩具/App 已进日常，friendly and patient</li>
        <li>作用：说明「为什么要管」——给出了<strong class="hl">问题</strong></li>
      </ul></div>
      <div class="knowledge-card c3"><h3><i class="fas fa-clock" style="color:#e67e22"></i> Para 3 · 新规一</h3><ul>
        <li><strong class="hl">主旨句</strong>：AI bots can't encourage people to use them for too long.</li>
        <li>具体：2 小时弹窗提醒 take a break；讲清 machine ≠ person</li>
        <li>作用：讲「怎么限制使用时长」</li>
      </ul></div>
      <div class="knowledge-card c4"><h3><i class="fas fa-shield-alt" style="color:#27ae60"></i> Para 4 · 新规二</h3><ul>
        <li><strong class="hl">主旨句</strong>：The rules also require AI bots to be safe and kind.</li>
        <li>三禁止：tell lies / share private information / harm national security</li>
        <li>举例：过去用情绪推广告，<strong class="hl">Now, the rules stop this</strong></li>
      </ul></div>
      <div class="knowledge-card c5"><h3><i class="fas fa-child" style="color:#8e44ad"></i> Para 5 · 新规三</h3><ul>
        <li><strong class="hl">主旨句</strong>：If you're under 18 and open an AI app, teen mode will turn on by itself.</li>
        <li>细节：家长可查看聊天时长；AI 不得为讨好而给不安全建议</li>
        <li>作用：把保护落到<strong class="hl">未成年人</strong>身上</li>
      </ul></div>
      <div class="knowledge-card c6"><h3><i class="fas fa-lightbulb" style="color:#f39c12"></i> 一句话串全文</h3><ul>
        <li>现象（青少年依赖 AI）→ <strong class="hl">新规三条</strong>（限时 / 安全友善 / 青少年模式）→ 任务（做调查写报告）</li>
        <li>背下这条线，主旨题必对</li>
      </ul></div>
    </div>

    <div class="section-header" style="margin-top:1.4rem"><i class="fas fa-brain" style="color:#e74c3c"></i> 阅读思维 · 四类题怎么想</div>
    <div class="knowledge-grid">
      <div class="knowledge-card c1"><h3><i class="fas fa-bullseye" style="color:#e74c3c"></i> 🎯 主旨题</h3><ul>
        <li>读<strong class="hl">首段提问</strong>预判：下文一定给「对策/规定」</li>
        <li>再看各段<strong class="hl">首句</strong>串主线，选能管住全文的项</li>
        <li>排除法：只覆盖某段细节的选项 = 错</li>
      </ul></div>
      <div class="knowledge-card c2"><h3><i class="fas fa-search" style="color:#3498db"></i> 🔍 细节题</h3><ul>
        <li>题干关键词（two hours / under 18）→ 回原文<strong class="hl">定位</strong></li>
        <li>答案常在<strong class="hl">同义替换</strong>：take a break = take a rest</li>
        <li>警惕「<strong class="hl">另一条规定</strong>」被拿来当选项（张冠李戴）</li>
      </ul></div>
      <div class="knowledge-card c3"><h3><i class="fas fa-balance-scale" style="color:#e67e22"></i> ⚖️ 判断（T/F）题</h3><ul>
        <li>盯转折词：<strong class="hl">Now / But / In the past</strong>（过去可以≠现在可以）</li>
        <li>绝对化表述（all / must / never / white lies 例外）先打问号</li>
        <li>用原文<strong class="hl">原句</strong>核对，不凭印象</li>
      </ul></div>
      <div class="knowledge-card c4"><h3><i class="fas fa-book" style="color:#27ae60"></i> 📚 词义/词组题</h3><ul>
        <li>把词组<strong class="hl">放回原句</strong>，靠上下文推意思</li>
        <li>pull away from：前文「花大量时间陪 AI」→ 推「疏远」</li>
        <li>先判词性，再看搭配介词（depend <strong class="hl">on</strong> / remind sb. <strong class="hl">of</strong>）</li>
      </ul></div>
    </div>

    <div class="teacher-talk" style="margin-top:1.2rem">
      <h4><i class="fas fa-microphone-alt"></i> 🎙️ 老师要求 · 阅读板块怎么用这个页面</h4>
      <p><strong>先看骨架，再做题</strong>：打开先读「文章全文」3 遍（第 3、5 段精读），再用「段落总结与思维导图」把 5 段串成一条线，最后才用底部自测检验方法。</p>
      <p><strong>重中之重</strong>：段落总结 + 思维导图。题只带过方法（主旨三步、细节定位、同义替换、转折警戒），真正要练的是「<strong>读一段就说出这段在干什么</strong>」的阅读思维。</p>
      <p><strong>本周动作</strong>：① 用自己的话复述 Para 1–5 各一句；② 照着思维导图默画一遍结构；③ 完成 Tools or friends? 调查 + 150–200 词报告。</p>
    </div>
    <div id="errorChecklist" style="display:none"></div>
    <span id="ecProgress" style="display:none"></span>
    '''
seg('<div id="tab-errors" class="tab-content">', '<div class="footer"',
    '<div id="tab-errors" class="tab-content">\n    ' + MAP + '</div>\n\n', 'tab4-summary-map')

# ============================================================
# ⑥ 词汇积累数组（14 条）
# ============================================================
F = '''const flashcards = [
  {"front":"depend on","back":"<strong>依赖；依靠</strong>（v.）<br>原句：…see it as a real friend and <strong>depend on</strong> it too much?<br>例句：Many teenagers depend on AI to do their homework.<br>搭配：depend on sb./sth.；depend on sb. to do sth."},
  {"front":"introduce sth","back":"<strong>颁布；引入；介绍</strong>（v.）<br>原句：The government has <strong>introduced</strong> new rules for AI companion bots.<br>例句：The school introduced new rules for mobile phones last term.<br>⚠️ 过去式 introduced，常与 last year / term 连用。"},
  {"front":"pull away from","back":"<strong>疏远；远离</strong>（v.+prep.）<br>原句：Some young people spend a lot of time with them and <strong>pull away from</strong> real-life friends.<br>例句：If you spend all day on your phone, you may pull away from your family.<br>⚠️ 介词 <strong>from</strong> 不能丢。"},
  {"front":"either...or...","back":"<strong>要么…要么…</strong>（二选一）<br>原句：These bots, <strong>either</strong> in the form of a toy <strong>or</strong> an app, have become a part of many people's daily lives.<br>例句：You can either call me or send me a message.<br>⚠️ 表「两者都」用 <strong>both...and</strong>，别混。"},
  {"front":"tell lies","back":"<strong>撒谎</strong>（v.+n.）<br>原句：They can't <strong>tell lies</strong>, share private information or do anything that could harm national security.<br>例句：It's wrong for teenagers to tell lies.<br>反义：tell the truth（说实话）"},
  {"front":"remind sb. to do sth.","back":"<strong>提醒某人做某事</strong><br>原句：They must show pop-up messages <strong>reminding people to take a break</strong> after two hours.<br>例句：My watch reminds me <strong>to</strong> take a break every hour.<br>⚠️ 还有 <strong>remind sb. of sth.</strong>（使某人想起）"},
  {"front":"companion(名词) / bot","back":"companion <strong>n. 同伴、陪伴者</strong>；bot <strong>n. 机器人程序</strong><br>AI companion bots = <strong>AI 陪伴机器人</strong>（标题核心词，全文出现多次）"},
  {"front":"pop-up message","back":"<strong>弹窗消息</strong>（n.）<br>原句：They must show <strong>pop-up messages</strong> reminding people to take a break after two hours.<br>例句：I got a pop-up message about the new app update."},
  {"front":"private information","back":"<strong>隐私信息</strong>（n.）<br>原句：They can't tell lies, share <strong>private information</strong> or…<br>对比：personal information 个人信息；private 强调「私密的、不公开的」"},
  {"front":"national security","back":"<strong>国家安全</strong>（n.）<br>原句：…or do anything that could harm <strong>national security</strong>.<br>搭配：harm / threaten national security"},
  {"front":"teen mode","back":"<strong>青少年模式</strong>（n.）<br>原句：If you're under 18 and open an AI app, <strong>teen mode</strong> will turn on by itself.<br>⚠️ by itself = 自动地（不是「自己一个人」）"},
  {"front":"encourage sb. to do sth.","back":"<strong>鼓励某人做某事</strong>（v.）<br>原句：the new rules say AI bots can't <strong>encourage people to use them for too long</strong>.<br>例句：My teacher encourages us to read English aloud."},
  {"front":"require sb./sth. to do sth.","back":"<strong>要求…做…</strong>（v.）<br>原句：The rules also <strong>require</strong> AI bots to be safe and kind.<br>例句：The school requires students to wear school uniforms."},
  {"front":"词形/搭配易错：lie 的兄弟们","back":"tell lies（撒谎，动词 lie → lied → lied, lying）<br>lie（躺 → lay → lain, lying）<br>lay（放置 → laid → laid）<br>⚠️ 「躺下」写 lie down；教材里 lay down 属笔误，考试按 lie down。"}
];'''
i = h.find('const flashcards = [')
j = h.find('];', i)
assert i > 0 and j > 0, 'flashcards array not found'
h = h[:i] + F + h[j + 2:]
report.append('OK[flashcards-14]')

# ============================================================
# ⑦ 残留检查 & 写出
# ============================================================
for pat in ['知识图谱', '知识卡牌', '易错自检', '闯关测验', '12张知识卡', '6大易错点']:
    c = h.count(pat)
    if c:
        report.append(f'抽查[{pat}] 残留 {c} 处')

open(FN, 'w', encoding='utf-8').write(h)
print(f'{orig_len} -> {len(h)} bytes')
print('\n'.join(report))
