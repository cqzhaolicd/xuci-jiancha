# -*- coding: utf-8 -*-
"""生成 zhaoli_index.html — 赵立 AI 学习中心(复制若琳学习中心框架, 内容换成 Python+AI)"""
import io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

h = open('index.html', encoding='utf-8').read()

# ============ 1. 标题/副标题/footer ============
h = h.replace('若琳 · 学习中心', '赵立 · AI 学习中心')
h = h.replace('互动学习 &amp; 错题库', 'Python 编程 · AI 应用 · 持续进化')
h = h.replace('为若琳定制的学习工具 &nbsp;|&nbsp; 持续更新中', '为赵立定制的 AI 学习工具 &nbsp;|&nbsp; 持续更新中')

# ============ 2. 替换 tools 数组(错题库工具 → AI 工具箱) ============
old_tools = '''const tools = [
  { name: '录入错题', icon: 'fa-plus-circle', desc: '添加新错题', cls: 't-add', url: 'wrong_bank.html#add' },
  { name: '错题本', icon: 'fa-list', desc: '浏览筛选错题', cls: 't-list', url: 'wrong_bank.html#list' },
  { name: '复习模式', icon: 'fa-redo', desc: '循环复习巩固', cls: 't-review', url: 'wrong_bank.html#review' },
  { name: '三层训练', icon: 'fa-layer-group', desc: '数学三层训练', cls: 't-training', url: 'wrong_bank.html#training' },
  { name: '打印试卷', icon: 'fa-print', desc: '组卷打印', cls: 't-print', url: 'wrong_bank.html#print-page' },
  { name: '数据分析', icon: 'fa-chart-pie', desc: '错题统计分析', cls: 't-analysis', url: 'wrong_bank.html#analysis' },
  { name: '五步法模板', icon: 'fa-clipboard-check', desc: '数学解题流程卡(打印)', cls: 't-flow', url: 'wubufa_card.html' },
  { name: '三刷清单', icon: 'fa-calendar-check', desc: '错题三刷时间表', cls: 't-brush', url: 'three_brush.html' },
];'''

new_tools = '''const tools = [
  { name: 'Python 基础', icon: 'fa-code', desc: '变量/数据类型/控制流', cls: 't-add', url: 'python_basics_interactive.html' },
  { name: 'AI 应用', icon: 'fa-robot', desc: '机器学习/大模型/提示词', cls: 't-training', url: 'ai_basics_interactive.html' },
  { name: '学习路线', icon: 'fa-route', desc: '从零到 AI 应用路线图', cls: 't-flow', url: 'zhaoli_index.html#ai-route' },
];'''
assert old_tools in h
h = h.replace(old_tools, new_tools)

# ============ 3. 删除学校学习数据段(仅到 schoolSubjectsData, 保留 trainingTerms) ============
old_school_start = h.index("const schoolGrades")
old_school_end = h.index("// 🔵 课外培训 — 互动学习（按学期分目录）")
h = h[:old_school_start] + h[old_school_end:]

# ============ 4. 替换 trainingTerms 为 AI 课程目录 (先找原数据段) ============
old_terms_start = h.index("// 🔵 课外培训 — 互动学习（按学期分目录）")
old_terms_end = h.index("const numColors")
old_terms = h[old_terms_start:old_terms_end]

new_terms = '''// 🔵 AI 学习 — 课程目录（按模块分层）
const trainingTerms = [
  {
    id: 'ai-python', name: 'Python 编程', icon: 'fa-code', cls: 'subject-physics',
    subjects: [
      {
        id: 'python-basics', name: 'Python 基础', icon: 'fa-code', cls: 'subject-physics',
        lectures: [
          { num: '01', title: 'Python 基础语法', url: 'python_basics_interactive.html', date: '2026-08-25', tags: ['Python'], new: true },
        ]
      },
    ]
  },
  {
    id: 'ai-apps', name: 'AI 应用', icon: 'fa-robot', cls: 'subject-math',
    subjects: [
      {
        id: 'ai-basics', name: 'AI 应用入门', icon: 'fa-robot', cls: 'subject-math',
        lectures: [
          { num: '01', title: 'AI 与机器学习概览', url: 'ai_basics_interactive.html', date: '2026-08-25', tags: ['AI'], new: true },
        ]
      },
    ]
  },
];
'''
h = h.replace(old_terms, new_terms)

# ============ 5. render() 主体: 移除错题库工具/预习闯关/学校学习, 只留 AI 学习 ============
old_render_body_start = h.index("  // === 错题库工具 ===")
old_render_body_end = h.index("  document.getElementById('app').innerHTML = html;")
new_render_body = '''  // === AI 学习目录 ===
  html += renderSection('AI 学习', 'fa-robot', '#667eea', 'badge-training',
    trainingTerms.map((term, ti) => {
      const cnt = term.subjects.reduce((a, s) => a + s.lectures.length, 0);
      return renderTrainingTerm(term, ti, cnt);
    }).join(''));

'''
h = h.replace(h[old_render_body_start:old_render_body_end], new_render_body)

# ============ 6. 删除 renderGrade 函数(学校专用, 不再使用) ============
rg_start = h.index("function renderGrade(grade, gi, cnt) {")
rg_end = h.index("function renderTrainingTerm(term, ti, cnt) {")
h = h[:rg_start] + h[rg_end:]

# ============ 7. 删除 renderSubject 函数(不再使用) ============
rs_start = h.index("function renderSubject(subj, si, cnt) {")
rs_end = h.index("function toggleSubject(header) {")
h = h[:rs_start] + h[rs_end:]

# ============ 8. 顶部 header 加"返回若琳学习中心"入口? 不需要, 独立入口 ============
# 检查残留引用
h = h.replace("schoolSubjectsData", "trainingTerms")  # 保险

open('zhaoli_index.html', 'w', encoding='utf-8').write(h)
print("zhaoli_index.html 生成, 大小:", len(h))

# 验证 JS 语法
import subprocess
r = subprocess.run(["node", "-e", f"""
const fs=require('fs');const html=fs.readFileSync('zhaoli_index.html','utf8');
const re=/<script[^>]*>([\\s\\S]*?)<\\/script>/g;let m,ok=true;
while((m=re.exec(html))){{try{{new Function(m[1])}}catch(e){{ok=false;console.log('ERR:',e.message)}}}}
console.log(ok?'JS OK':'JS FAIL');
"""], capture_output=True, text=True)
print(r.stdout.strip() or r.stderr[:300])
