#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""学习中心全量错题连续制改造：错题必须【连续】做对3次才移出。
改动：
 A. 富模板38页 saveWrongHistoryItem：答错时 redo 清零（原只 count++ 不清零）
 B. 对象类76页 selA wrong 重做答错：r 清零 + 新提示（原保留 r）
 C. 对象类78页 selA else 分支（s==='ok' 已做/已合格再答错）→ 转回 wrong r0 + 重新入错题库
 D. 特殊页2页 selectAnswer 同 B/C
"""
import glob, re, sys

def patch_file(fn, ops, tag):
    """ops: list of (old,new,expect_count)"""
    h = open(fn, encoding='utf-8').read()
    changed = []
    for old, new, expect in ops:
        n = h.count(old)
        if expect is not None and n != expect:
            print(f'  SKIP[{tag}] {fn}: expect {expect} got {n} :: {old[:60]}')
            return False
        if n > 0:
            h = h.replace(old, new)
            changed.append(old[:50])
    if changed:
        open(fn, 'w', encoding='utf-8').write(h)
    return True

# ---- A. 富模板 38 页 ----
A_OLD = "if(found){found.count++;found.lastWrong=Date.now();if(found.redo===undefined)found.redo=0;}"
A_NEW = "if(found){found.count++;found.lastWrong=Date.now();found.redo=0;}"
rich = [f for f in glob.glob('*.html') if 'markRedoOk' in open(f, encoding='utf-8').read()]
print(f'A 富模板类 {len(rich)} 页')
okA = 0
for fn in rich:
    if patch_file(fn, [(A_OLD, A_NEW, 1)], 'A'):
        okA += 1
print(f'A 完成 {okA}/{len(rich)}')

# ---- B. 对象类 76 页 selA wrong 答错清零 ----
B_OLD = "else{saveQuizProg(idx,{s:'wrong',r:pr.r||0});toast('❌ 仍记入待重做','warning');}"
B_NEW = "else{saveQuizProg(idx,{s:'wrong',r:0});toast('❌ 答错！连续重做清零，需重新连对3次','warning');}"
obj = [f for f in glob.glob('*.html') if 'REDO_NEEDED' in open(f, encoding='utf-8').read()]
okB = 0
for fn in obj:
    h = open(fn, encoding='utf-8').read()
    if h.count(B_OLD) == 1:
        h = h.replace(B_OLD, B_NEW)
        open(fn, 'w', encoding='utf-8').write(h)
        okB += 1
    elif 'selectAnswer' in h:
        pass  # 特殊页 D 处理
    else:
        print(f'B 未匹配 {fn}')
print(f'B 完成 {okB}/76(带toast)')

# ---- C/D. else 分支（s ok 再答错 → 转 wrong r0 + 入错题库） ----
C_OLD = "else{saveQuizProg(idx,{s:'ok',r:pr.r||0});}"
# 富模板对象？C 只用于 REDO_NEEDED 页（selA/selectAnswer 都含）。guard autoImportWB 防特殊页无函数
C_NEW = "else if(correct){saveQuizProg(idx,{s:'ok',r:pr.r||0});}else{saveQuizProg(idx,{s:'wrong',r:0});if(typeof autoImportWB==='function'&&autoImportWB(idx,oi))toast('📥 已重新加入错题库','success');}"
okC = 0
for fn in obj:
    h = open(fn, encoding='utf-8').read()
    n = h.count(C_OLD)
    if n == 1:
        h = h.replace(C_OLD, C_NEW)
        open(fn, 'w', encoding='utf-8').write(h)
        okC += 1
    else:
        print(f'C 异常 {fn}: {n}')
print(f'C/D 完成 {okC}/78')

# ---- D. 特殊页 selectAnswer wrong 分支（无 toast 变体） ----
D_OLD = "else{saveQuizProg(idx,{s:'wrong',r:pr.r||0});}"
D_NEW = "else{saveQuizProg(idx,{s:'wrong',r:0});}"
for fn in ['math_surd_interactive.html', 'physics_sound_interactive.html']:
    h = open(fn, encoding='utf-8').read()
    if D_OLD in h:
        h = h.replace(D_OLD, D_NEW)
        open(fn, 'w', encoding='utf-8').write(h)
        print(f'D 特殊页 {fn} 已改 wrong 清零')
    else:
        print(f'D 特殊页 {fn} 已无 D_OLD（可能被 C 覆盖为新的 else if）')
