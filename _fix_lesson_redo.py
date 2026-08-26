# -*- coding: utf-8 -*-
"""博学班34页: 错题重做+3次合格改造(基于 initRetryMode/WRONG_HISTORY_KEY 机制)"""
import io, sys, re, glob
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

lesson_group = ['physics_lesson12_interactive.html', 'math_lesson5_interactive.html', 'physics_lesson6_interactive.html', 'math_lesson3_interactive.html', 'physics_sound2_interactive.html', 'physics_mechanical_interactive.html', 'math_lesson11_interactive.html', 'math_lesson10_interactive.html', 'physics_lesson10_interactive.html', 'physics8_ch4_interactive.html', 'physics_lesson15_interactive.html', 'math_lesson9_interactive.html', 'physics_lesson8_interactive.html', 'math_surd4_interactive.html', 'math_lesson7_interactive.html', 'physics8_ch2_interactive.html', 'physics8_ch1_interactive.html', 'math_lesson14_interactive.html', 'math_surd2_interactive.html', 'physics_lesson13_interactive.html', 'math_lesson6_interactive.html', 'physics_lens_interactive.html', 'physics_lesson3_interactive.html', 'physics8_ch5_interactive.html', 'math_lesson13_interactive.html', 'physics_lesson5_interactive.html', 'physics8_interactive.html', 'physics_lesson14_interactive.html', 'physics8_ch3_interactive.html', 'math_lesson8_interactive.html', 'physics8_ch6_interactive.html', 'math_lesson12_interactive.html', 'physics_lesson7_interactive.html', 'physics_lesson9_interactive.html']

# ============ 公共替换段 ============

# 1. saveWrongHistoryItem 增加 redo 字段(初始 redo=0)
NEW_SAVE_WRONG = """function saveWrongHistoryItem(idx){
  let h=loadWrongHistory();
  const found=h.find(x=>x.idx===idx);
  if(found){found.count++;found.lastWrong=Date.now();if(found.redo===undefined)found.redo=0;}
  else h.push({idx,count:1,lastWrong:Date.now(),redo:0});
  localStorage.setItem(WRONG_HISTORY_KEY,JSON.stringify(h));
}
function markRedoOk(idx){
  let h=loadWrongHistory();
  const found=h.find(x=>x.idx===idx);
  if(!found)return;
  found.redo=(found.redo||0)+1;
  if(found.redo>=3){h=h.filter(x=>x.idx!==idx);toast('🎉 重做'+found.redo+'次，已合格！','success');}
  else{toast('✅ 答对！重做'+found.redo+'/3','success');}
  localStorage.setItem(WRONG_HISTORY_KEY,JSON.stringify(h));
}
"""

# 2. selA 通用版(答对时 markRedoOk; 保留 autoImportWB; 无 speakDone)
NEW_SELA_NO_SOUND = """function selA(oi){const idx=shuffled[curQ];if(quizAns[idx]>=0)return;quizAns[idx]=oi;saveQuizProg(idx,oi===questions[idx].ans?'ok':'wrong');
  if(oi===questions[idx].ans){const wh=loadWrongHistory();if(wh.some(x=>x.idx===idx))markRedoOk(idx);}
  if(oi!==questions[idx].ans){saveWrongHistoryItem(idx);if(autoImportWB(idx,oi))toast('📥 已自动加入错题库','success');else toast('📥 错题已在错题库中','info');}
renderQ();}"""

# 3. selA 带音效版(physics8 系列)
NEW_SELA_SOUND = """function selA(oi){const idx=shuffled[curQ];if(quizAns[idx]>=0)return;quizAns[idx]=oi;saveQuizProg(idx,oi===questions[idx].ans?'ok':'wrong');if(oi===questions[idx].ans){speakDone();}
  if(oi===questions[idx].ans){const wh=loadWrongHistory();if(wh.some(x=>x.idx===idx))markRedoOk(idx);}
  if(oi!==questions[idx].ans){saveWrongHistoryItem(idx);if(autoImportWB(idx,oi))toast('📥 已自动加入错题库','success');else toast('📥 错题已在错题库中','info');}
renderQ();}"""

# 4. initRetryMode 只取未合格错题(redo<3), 增加 badge 显示重做进度
NEW_INIT_RETRY = """function initRetryMode(){
  const h=loadWrongHistory().filter(x=>(x.redo||0)<3);
  if(!h.length){alert('没有待重做的错题了，全部合格！');return;}
  wrongIds=h.map(x=>x.idx);
  curQ=0;retryMode=true;
  quizAns=new Array(questions.length).fill(-1);
  shuffled=shuffle([...wrongIds]);
  switchTab('quiz');
  renderQ();
}"""

# 5. renderQ badge: 错题历史中显示重做进度
# 替换 _db 生成行: 原: const _db=_dp?`<span class="done-badge ${_dp==='ok'?'ok':'no'}">${_dp==='ok'?'✅已做':'❌已做'}</span>`:'';
# 新: 检查错题历史的 redo
NEW_DB_GEN = """const _db=(function(){if(_dp){const wh=loadWrongHistory();const rec=wh.find(x=>x.idx===idx);if(rec){const rr=(rec.redo||0);return `<span class="done-badge ${rr>=3?'ok':'no'}">${rr>=3?'✅已合格':'❌重做'+rr+'/3'}</span>`;}return `<span class="done-badge ${_dp==='ok'?'ok':'no'}">${_dp==='ok'?'✅已做':'❌已做'}</span>`;}return '';})();"""

done = []
fail = []
for b in lesson_group:
    f = f'/home/administrator/xuci-jiancha/{b}'
    h = open(f, encoding='utf-8').read()
    try:
        # 检查是否已改
        if 'markRedoOk' in h:
            done.append(b + '(已改)')
            continue
        # 1. 替换 saveWrongHistoryItem 函数(含其后新加 markRedoOk)
        # 找 saveWrongHistoryItem 函数体
        i = h.find('function saveWrongHistoryItem(')
        if i < 0: raise Exception('无 saveWrongHistoryItem')
        j = h.find('\n}', i) + 2  # 函数结束的 }
        old_save = h[i:j]
        h = h[:i] + NEW_SAVE_WRONG.strip() + h[j:]
        
        # 2. 替换 selA(判断是否有 speakDone 行)
        i = h.find('function selA(')
        if i < 0: raise Exception('无 selA')
        j = h.find('\n}', i) + 2
        old_sela = h[i:j]
        if 'speakDone()' in old_sela:
            h = h[:i] + NEW_SELA_SOUND.strip() + h[j:]
        else:
            h = h[:i] + NEW_SELA_NO_SOUND.strip() + h[j:]
        
        # 3. 替换 initRetryMode
        i = h.find('function initRetryMode(')
        if i < 0: raise Exception('无 initRetryMode')
        j = h.find('\n}\n', i) + 3
        h = h[:i] + NEW_INIT_RETRY.strip() + h[j:]
        
        # 4. 替换 renderQ 中的 _db 生成(两行式)
        old_db = "const _db=_dp?`<span class=\\\"done-badge ${_dp==='ok'?'ok':'no'}\\\">${_dp==='ok'?'✅已做':'❌已做'}</span>`:'';"
        # 实际文件里可能没有反斜杠转义, 试两种
        candidates = [
            "const _db=_dp?`<span class=\"done-badge ${_dp==='ok'?'ok':'no'}\">${_dp==='ok'?'✅已做':'❌已做'}</span>`:'';",
            "const _db=_dp?`<span class=\\\"done-badge ${_dp==='ok'?'ok':'no'}\\\">${_dp==='ok'?'✅已做':'❌已做'}</span>`:'';",
        ]
        replaced_db = False
        for cand in candidates:
            if cand in h:
                h = h.replace(cand, NEW_DB_GEN, 1)
                replaced_db = True
                break
        if not replaced_db:
            # 尝试正则
            m = re.search(r"const _db=_dp\?`<span class=\\\\?\"done-badge \$\{_dp==='ok'\?'ok':'no'\}\\\\?\">\$\{_dp==='ok'\?'✅已做':'❌已做'\}</span>`:'';", h)
            if m:
                h = h[:m.start()] + NEW_DB_GEN + h[m.end():]
                replaced_db = True
        if not replaced_db:
            raise Exception('未找到 _db 生成行')
        
        open(f, 'w', encoding='utf-8').write(h)
        done.append(b)
    except Exception as ex:
        fail.append((b, str(ex)[:100]))

print(f"成功: {len(done)}/{len(lesson_group)}")
if fail:
    print("失败:")
    for b, e in fail:
        print(f"  {b}: {e}")
