# -*- coding: utf-8 -*-
"""课外培训加学期子目录(2026暑期/2026秋季), 数学物理移入暑期"""
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

P = 'index.html'
h = open(P, encoding='utf-8').read()

# ============ 1. 替换 trainingSubjects 数据为 trainingTerms ============
old_data = '''// 🔵 课外培训 — 互动学习（已有讲次）
const trainingSubjects = [
  {
    id: 'tyjy-math', name: '数学', icon: 'fa-calculator', cls: 'subject-math',
    lectures: [
      { num: '01', title: '二次根式（一）', url: 'math_surd_interactive.html', date: '2026-07-25', tags: ['数学'], new: false },
      { num: '02', title: '二次根式（二）', url: 'math_surd2_interactive.html', date: '2026-07-26', tags: ['数学'], new: false },
      { num: '03', title: '二次根式（三）', url: 'math_lesson3_interactive.html', date: '2026-07-27', tags: ['数学'], new: false },
      { num: '04', title: '二次根式（四）', url: 'math_surd4_interactive.html', date: '2026-07-28', tags: ['数学'], new: true },
      { num: '05', title: '勾股定理', url: 'math_lesson5_interactive.html', date: '2026-07-29', tags: ['数学'], new: false },
      { num: '06', title: '勾股定理应用', url: 'math_lesson6_interactive.html', date: '2026-07-31', tags: ['数学'], new: false },
      { num: '07', title: '勾股定理解三角形', url: 'math_lesson7_interactive.html', date: '2026-08-01', tags: ['数学'], new: true },
      { num: '08', title: '勾股定理构造与翻折', url: 'math_lesson8_interactive.html', date: '2026-08-02', tags: ['数学'], new: true },
      { num: '09', title: '二元一次方程组', url: 'math_lesson9_interactive.html', date: '2026-08-03', tags: ['数学'], new: true },
      { num: '10', title: '含参问题', url: 'math_lesson10_interactive.html', date: '2026-08-04', tags: ['数学'], new: false },
      { num: '11', title: '平面直角坐标系', url: 'math_lesson11_interactive.html', date: '2026-08-06', tags: ['数学'], new: false },
      { num: '12', title: '正比例函数与一次函数', url: 'math_lesson12_interactive.html', date: '2026-08-07', tags: ['数学'], new: false },
      { num: '13', title: '函数解析式与交点坐标', url: 'math_lesson13_interactive.html', date: '2026-08-08', tags: ['数学'], new: false },
      { num: '14', title: '一次函数数形结合与图象变换', url: 'math_lesson14_interactive.html', date: '2026-08-09', tags: ['数学'], new: true },
    ]
  },
  {
    id: 'tyjy-physics', name: '物理', icon: 'fa-flask', cls: 'subject-physics',
    lectures: [
      { num: '01', title: '声现象（一）', url: 'physics_sound_interactive.html', date: '2026-07-25', tags: ['物理'], new: false },
      { num: '02', title: '声现象（二）', url: 'physics_sound2_interactive.html', date: '2026-07-26', tags: ['物理'], new: false },
      { num: '03', title: '测量（三）', url: 'physics_lesson3_interactive.html', date: '2026-07-27', tags: ['物理'], new: true },
      { num: '04', title: '机械运动', url: 'physics_mechanical_interactive.html', date: '2026-07-28', tags: ['物理'], new: true },
      { num: '05', title: '运动学图像与计算', url: 'physics_lesson5_interactive.html', date: '2026-07-29', tags: ['物理'], new: false },
      { num: '06', title: '温度与物态', url: 'physics_lesson6_interactive.html', date: '2026-07-31', tags: ['物理'], new: false },
      { num: '07', title: '物态变化', url: 'physics_lesson7_interactive.html', date: '2026-08-01', tags: ['物理'], new: true },
      { num: '08', title: '光的传播与反射', url: 'physics_lesson8_interactive.html', date: '2026-08-03', tags: ['物理'], new: true },
      { num: '09', title: '平面镜成像', url: 'physics_lesson9_interactive.html', date: '2026-08-04', tags: ['物理'], new: false },
      { num: '10', title: '光的折射', url: 'physics_lesson10_interactive.html', date: '2026-08-06', tags: ['物理'], new: false },
      { num: '11', title: '透镜专题', url: 'physics_lens_interactive.html', date: '2026-08-06', tags: ['物理'], new: false },
      { num: '12', title: '透镜应用', url: 'physics_lesson12_interactive.html', date: '2026-08-08', tags: ['物理'], new: true },
      { num: '13', title: '质量和体积', url: 'physics_lesson13_interactive.html', date: '2026-08-08', tags: ['物理'], new: false },
      { num: '14', title: '密度', url: 'physics_lesson14_interactive.html', date: '2026-08-09', tags: ['物理'], new: false },
      { num: '15', title: '密度图象与计算', url: 'physics_lesson15_interactive.html', date: '2026-08-10', tags: ['物理'], new: true },
    ]
  },
];'''

new_data = '''// 🔵 课外培训 — 互动学习（按学期分目录）
const trainingTerms = [
  {
    id: 'tyjy-2026summer', name: '2026年暑期', icon: 'fa-sun', cls: 'subject-math',
    subjects: [
      {
        id: 'tyjy-math', name: '数学', icon: 'fa-calculator', cls: 'subject-math',
        lectures: [
          { num: '01', title: '二次根式（一）', url: 'math_surd_interactive.html', date: '2026-07-25', tags: ['数学'], new: false },
          { num: '02', title: '二次根式（二）', url: 'math_surd2_interactive.html', date: '2026-07-26', tags: ['数学'], new: false },
          { num: '03', title: '二次根式（三）', url: 'math_lesson3_interactive.html', date: '2026-07-27', tags: ['数学'], new: false },
          { num: '04', title: '二次根式（四）', url: 'math_surd4_interactive.html', date: '2026-07-28', tags: ['数学'], new: true },
          { num: '05', title: '勾股定理', url: 'math_lesson5_interactive.html', date: '2026-07-29', tags: ['数学'], new: false },
          { num: '06', title: '勾股定理应用', url: 'math_lesson6_interactive.html', date: '2026-07-31', tags: ['数学'], new: false },
          { num: '07', title: '勾股定理解三角形', url: 'math_lesson7_interactive.html', date: '2026-08-01', tags: ['数学'], new: true },
          { num: '08', title: '勾股定理构造与翻折', url: 'math_lesson8_interactive.html', date: '2026-08-02', tags: ['数学'], new: true },
          { num: '09', title: '二元一次方程组', url: 'math_lesson9_interactive.html', date: '2026-08-03', tags: ['数学'], new: true },
          { num: '10', title: '含参问题', url: 'math_lesson10_interactive.html', date: '2026-08-04', tags: ['数学'], new: false },
          { num: '11', title: '平面直角坐标系', url: 'math_lesson11_interactive.html', date: '2026-08-06', tags: ['数学'], new: false },
          { num: '12', title: '正比例函数与一次函数', url: 'math_lesson12_interactive.html', date: '2026-08-07', tags: ['数学'], new: false },
          { num: '13', title: '函数解析式与交点坐标', url: 'math_lesson13_interactive.html', date: '2026-08-08', tags: ['数学'], new: false },
          { num: '14', title: '一次函数数形结合与图象变换', url: 'math_lesson14_interactive.html', date: '2026-08-09', tags: ['数学'], new: true },
        ]
      },
      {
        id: 'tyjy-physics', name: '物理', icon: 'fa-flask', cls: 'subject-physics',
        lectures: [
          { num: '01', title: '声现象（一）', url: 'physics_sound_interactive.html', date: '2026-07-25', tags: ['物理'], new: false },
          { num: '02', title: '声现象（二）', url: 'physics_sound2_interactive.html', date: '2026-07-26', tags: ['物理'], new: false },
          { num: '03', title: '测量（三）', url: 'physics_lesson3_interactive.html', date: '2026-07-27', tags: ['物理'], new: true },
          { num: '04', title: '机械运动', url: 'physics_mechanical_interactive.html', date: '2026-07-28', tags: ['物理'], new: true },
          { num: '05', title: '运动学图像与计算', url: 'physics_lesson5_interactive.html', date: '2026-07-29', tags: ['物理'], new: false },
          { num: '06', title: '温度与物态', url: 'physics_lesson6_interactive.html', date: '2026-07-31', tags: ['物理'], new: false },
          { num: '07', title: '物态变化', url: 'physics_lesson7_interactive.html', date: '2026-08-01', tags: ['物理'], new: true },
          { num: '08', title: '光的传播与反射', url: 'physics_lesson8_interactive.html', date: '2026-08-03', tags: ['物理'], new: true },
          { num: '09', title: '平面镜成像', url: 'physics_lesson9_interactive.html', date: '2026-08-04', tags: ['物理'], new: false },
          { num: '10', title: '光的折射', url: 'physics_lesson10_interactive.html', date: '2026-08-06', tags: ['物理'], new: false },
          { num: '11', title: '透镜专题', url: 'physics_lens_interactive.html', date: '2026-08-06', tags: ['物理'], new: false },
          { num: '12', title: '透镜应用', url: 'physics_lesson12_interactive.html', date: '2026-08-08', tags: ['物理'], new: true },
          { num: '13', title: '质量和体积', url: 'physics_lesson13_interactive.html', date: '2026-08-08', tags: ['物理'], new: false },
          { num: '14', title: '密度', url: 'physics_lesson14_interactive.html', date: '2026-08-09', tags: ['物理'], new: false },
          { num: '15', title: '密度图象与计算', url: 'physics_lesson15_interactive.html', date: '2026-08-10', tags: ['物理'], new: true },
        ]
      },
    ]
  },
  {
    id: 'tyjy-2026fall', name: '2026年秋季', icon: 'fa-leaf', cls: 'subject-physics',
    subjects: []
  },
];'''

assert old_data in h, 'trainingSubjects 数据未找到'
h = h.replace(old_data, new_data)
print('1. trainingTerms 数据替换 OK')

# ============ 2. render() 课外培训调用: trainingSubjects→trainingTerms, renderSubject→renderTrainingTerm ============
old_render = '''  // === 课外培训 ===
  html += renderSection('课外培训 · 互动学习', 'fa-graduation-cap', '#e67e22', 'badge-training',
    trainingSubjects.map((subj, si) => {
      const cnt = subj.lectures.length;
      return renderSubject(subj, si, cnt);
    }).join(''));'''

new_render = '''  // === 课外培训 ===
  html += renderSection('课外培训 · 互动学习', 'fa-graduation-cap', '#e67e22', 'badge-training',
    trainingTerms.map((term, ti) => {
      const cnt = term.subjects.reduce((a, s) => a + s.lectures.length, 0);
      return renderTrainingTerm(term, ti, cnt);
    }).join(''));'''

assert old_render in h, 'render 调用未找到'
h = h.replace(old_render, new_render)
print('2. render() 调用替换 OK')

# ============ 3. 新增 renderTrainingTerm 函数(在 renderSubject 之前插入) ============
new_func = '''function renderTrainingTerm(term, ti, cnt) {
  return `
    <div class="subject-section fade-in-up" style="animation-delay:${0.1 + ti * 0.06}s">
      <div class="subject-header ${term.cls}" onclick="toggleSubject(this)">
        <div class="icon"><i class="fas ${term.icon}"></i></div>
        <h3>${term.name}</h3>
        <span class="count">${cnt} 讲</span>
        <span class="toggle-icon"><i class="fas fa-chevron-down"></i></span>
      </div>
      <div class="grade-grid">
        ${term.subjects.length > 0 ? term.subjects.map((subj, si) => `
          <div class="subject-section" style="margin-bottom:0">
            <div class="subject-header ${subj.cls}" onclick="toggleSubject(this)" style="cursor:pointer">
              <div class="icon" style="font-size:1rem;color:var(--primary)"><i class="fas ${subj.icon}"></i></div>
              <h3 style="font-size:0.88rem;font-weight:600;flex:1;margin:0;color:var(--text)">${subj.name}</h3>
              <span style="font-size:0.7rem;color:var(--text-light)">${subj.lectures.length}项</span>
              <span class="toggle-icon"><i class="fas fa-chevron-down"></i></span>
            </div>
            <div class="lecture-grid">
              ${subj.lectures.map((lec, li) => `
              <a href="${lec.url}" class="lecture-card ${isLearned(lec.url) ? 'learned' : ''}">
                ${lec.new ? '<span class="badge-new">NEW</span>' : ''}
                <span class="learn-badge" style="display:${isLearned(lec.url) ? 'inline-flex' : 'none'}"><i class="fas fa-check"></i> 已学习</span>
                <div class="lnum" style="background:${numColors[li % numColors.length]}">${lec.num}</div>
                <div class="info">
                  <h4>${lec.title}</h4>
                  <div class="meta"><span>${lec.date}</span>${lec.tags.map(t => `<span class="tag">${t}</span>`).join('')}</div>
                </div>
                <div class="arrow"><i class="fas fa-chevron-right"></i></div>
                ${learnedBtn(lec.url)}
              </a>`).join('')}
            </div>
          </div>`).join('') : `<div style="grid-column:1/-1;padding:1rem;text-align:center;color:var(--text-light);font-size:0.85rem">暂无内容 · 后续增加</div>`}
      </div>
    </div>`;
}

'''
anchor = 'function renderSubject(subj, si, cnt) {'
assert anchor in h, 'renderSubject 未找到'
h = h.replace(anchor, new_func + anchor)
print('3. renderTrainingTerm 函数插入 OK')

open(P, 'w', encoding='utf-8').write(h)
print('DONE')
