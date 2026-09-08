#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
_build_lql_index.py — 生成刘秋灵学习中心入口 liuqiuling_index.html
源: index.html(若琳中心), 复制并改造:
  1. 品牌: 若琳→刘秋灵; 副标题注明 重庆文德中学·九年级
  2. tools: wrong_bank→lql_wrong_bank; 删除 ai_workshop 行
  3. 预习闯关 4 卡 → lql_preview_challenge_*
  4. 删除 trainingTerms 常量段(课外培训)
  5. 学校数据重写: 9年级(7科·人教版章节框架) / 8年级上(46页 lql_) / 7年级(6科课堂笔记 lql_)
  6. render(): 删除课外培训渲染段
  7. LEARNED_KEY → lql_learned_pages
"""
import re, os

SRC = '/home/administrator/xuci-jiancha/index.html'
OUT = '/home/administrator/xuci-jiancha/liuqiuling_index.html'

s = open(SRC, encoding='utf-8').read()
log = []
def rep(old, new, tag, required=True):
    global s
    n = s.count(old)
    if n == 0 and required:
        raise SystemExit(f'❌ 未找到: {tag}\n{old[:120]}')
    s = s.replace(old, new)
    if n: log.append(f'  {tag}: {n}')

# ---------- 1. 品牌 ----------
rep('📚 若琳 · 学习中心', '📚 刘秋灵 · 学习中心', 'title品牌')
rep('若琳 · 学习中心', '刘秋灵 · 学习中心', 'h1品牌')
rep('<p>互动学习 &amp; 错题库</p>', '<p>重庆文德中学 · 九年级 &nbsp;|&nbsp; 互动学习 &amp; 错题库</p>', '副标题')
rep('为若琳定制的学习工具', '为刘秋灵定制的学习工具', 'footer')

# ---------- 2. tools ----------
for u in ['wrong_bank.html#add','wrong_bank.html#list','wrong_bank.html#review','wrong_bank.html#training','wrong_bank.html#print-page','wrong_bank.html#analysis']:
    rep(u, u.replace('wrong_bank.html','lql_wrong_bank.html'), f'tools {u}')
# 删除 ai_workshop 工具行
s2 = re.sub(r'\n\s*\{ name: \'AI学习工坊\'.*?\},?\n', '\n', s)
if s2 != s:
    log.append('  删除 ai_workshop 行')
s = s2

# ---------- 3. 预习闯关 4 卡 URL ----------
for sub in ['math8','physics8','chinese8','english8']:
    rep(f'preview_challenge_{sub}.html', f'lql_preview_challenge_{sub}.html', f'闯关{sub}')

# ---------- 4. 删除 trainingTerms 常量段 ----------
i0 = s.find('// 🔵 课外培训')
i1 = s.find('const numColors', i0)
if i0 < 0 or i1 < 0:
    raise SystemExit('❌ 找不到课外培训段边界')
s = s[:i0] + s[i1:]
log.append('  删除 trainingTerms 常量段')

# ---------- 5. 学校数据重写 ----------
b0 = s.find('function buildSchoolData() {')
b1 = s.find('const schoolSubjectsData = buildSchoolData();', b0)
if b0 < 0 or b1 < 0:
    raise SystemExit('❌ 找不到 buildSchoolData')
b1 = s.find('\n', b1) + 1

NEW_DATA = '''
function buildSchoolData() {
  // 刘秋灵学习中心 · 学校学习区
  // 9年级 = 当前年级(人教版/统编框架, 章节内容按课本上传后填充, 教材版本以学校课本为准)
  // 8年级上 / 7年级 = 备用复习(由若琳学习中心同步)
  const data = [];
  const pushGrade = (id, name, icon, cls, subjects) => data.push({ id, name, icon, cls, subjects });
  const G9 = (subject) => ({
    id: '9-' + subject,
    name: subject,
    icon: schoolIconsMap[subject] || 'fa-book',
    cls: schoolColorsMap[subject] || 'subject-math',
    lectures: (GRADE9[subject] || []).map((c, i) => ({
      num: String(i + 1).padStart(2, '0'),
      title: c,
      url: 'lql_school_interactive.html?level=' + encodeURIComponent('9年级') + '&subject=' + encodeURIComponent(subject) + '&chapter=' + encodeURIComponent(c),
      date: '',
      tags: [subject],
      new: false
    }))
  });
  const GRADE9 = {
    '语文': ['九年级上 · 第1单元', '九年级上 · 第2单元', '九年级上 · 第3单元', '九年级上 · 第4单元', '九年级上 · 第5单元', '九年级上 · 第6单元', '九年级下 · 第1单元', '九年级下 · 第2单元', '九年级下 · 第3单元', '九年级下 · 第4单元', '九年级下 · 第5单元', '九年级下 · 第6单元'],
    '数学': ['第21章 一元二次方程(九上)', '第22章 二次函数(九上)', '第23章 旋转(九上)', '第24章 圆(九上)', '第25章 概率初步(九上)', '第26章 反比例函数(九下)', '第27章 相似(九下)', '第28章 锐角三角函数(九下)', '第29章 投影与视图(九下)'],
    '英语': ['Unit 1', 'Unit 2', 'Unit 3', 'Unit 4', 'Unit 5', 'Unit 6', 'Unit 7', 'Unit 8', 'Unit 9', 'Unit 10', 'Unit 11', 'Unit 12', 'Unit 13', 'Unit 14'],
    '物理': ['第13章 内能', '第14章 内能的利用', '第15章 电流和电路', '第16章 电压 电阻', '第17章 欧姆定律', '第18章 电功率', '第19章 生活用电', '第20章 电与磁', '第21章 信息的传递', '第22章 能源与可持续发展'],
    '化学': ['绪言 化学使世界变得更加绚丽多彩', '第1单元 走进化学世界', '第2单元 我们周围的空气', '第3单元 物质构成的奥秘', '第4单元 自然界的水', '第5单元 化学方程式', '第6单元 碳和碳的氧化物', '第7单元 燃料及其利用', '第8单元 金属和金属材料', '第9单元 溶液', '第10单元 酸和碱', '第11单元 盐 化肥', '第12单元 化学与生活'],
    '历史': ['九年级上 · 第1单元', '九年级上 · 第2单元', '九年级上 · 第3单元', '九年级上 · 第4单元', '九年级上 · 第5单元', '九年级上 · 第6单元', '九年级上 · 第7单元', '九年级下 · 第1单元', '九年级下 · 第2单元', '九年级下 · 第3单元', '九年级下 · 第4单元', '九年级下 · 第5单元', '九年级下 · 第6单元'],
    '道法': ['九年级上 · 第1单元 富强与创新', '九年级上 · 第2单元 民主与法治', '九年级上 · 第3单元 文明与家园', '九年级上 · 第4单元 和谐与梦想', '九年级下 · 第1单元 我们共同的世界', '九年级下 · 第2单元 世界舞台上的中国', '九年级下 · 第3单元 走向未来的少年']
  };
  const grade9Subjects = ['语文', '数学', '英语', '物理', '化学', '历史', '道法'];
  pushGrade('grade1', '9年级', 'fa-graduation-cap', 'subject-math', grade9Subjects.map(G9));

  // 8年级上(备用复习): 语/数/英/物/生/史/地/道 全部分章页
  pushGrade('grade2', '8年级上 · 备用复习', 'fa-book', 'subject-chinese', [
    { id: 'g8-数学', name: '数学', icon: 'fa-calculator', cls: 'subject-math', lectures: [
      { num: '01', title: '第1章 勾股定理', url: 'lql_math8_ch1_interactive.html', date: '2026-07-31', tags: ['数学'], new: true },
      { num: '02', title: '第2章 实数', url: 'lql_math8_ch2_interactive.html', date: '2026-07-31', tags: ['数学'], new: true },
      { num: '03', title: '第3章 位置与坐标', url: 'lql_math8_ch3_interactive.html', date: '2026-07-31', tags: ['数学'], new: true },
      { num: '04', title: '第4章 一次函数', url: 'lql_math8_ch4_interactive.html', date: '2026-07-31', tags: ['数学'], new: true },
      { num: '05', title: '第5章 二元一次方程组', url: 'lql_math8_ch5_interactive.html', date: '2026-07-31', tags: ['数学'], new: true },
      { num: '06', title: '第6章 数据的分析', url: 'lql_math8_ch6_interactive.html', date: '2026-07-31', tags: ['数学'], new: true },
      { num: '07', title: '第7章 平行线的证明', url: 'lql_math8_ch7_interactive.html', date: '2026-07-31', tags: ['数学'], new: true }
    ]},
    { id: 'g8-语文', name: '语文', icon: 'fa-book', cls: 'subject-chinese', lectures: [
      { num: '01', title: '第一单元 新闻阅读', url: 'lql_chinese8_u1_interactive.html', date: '2026-08-24', tags: ['语文'], new: true },
      { num: '02', title: '第二单元 回忆性散文与传记', url: 'lql_chinese8_u2_interactive.html', date: '2026-08-24', tags: ['语文'], new: true },
      { num: '03', title: '第三单元 古诗文山水', url: 'lql_chinese8_u3_interactive.html', date: '2026-08-24', tags: ['语文'], new: true },
      { num: '04', title: '第四单元 散文', url: 'lql_chinese8_u4_interactive.html', date: '2026-08-24', tags: ['语文'], new: true },
      { num: '05', title: '第五单元 说明文', url: 'lql_chinese8_u5_interactive.html', date: '2026-08-24', tags: ['语文'], new: true },
      { num: '06', title: '第六单元 文言文', url: 'lql_chinese8_u6_interactive.html', date: '2026-08-24', tags: ['语文'], new: true },
      { num: '07', title: '文言虚实词逐义检查(138词)', url: 'lql_虚实词逐义检查卷.html', date: '2026-07-27', tags: ['语文'], new: false }
    ]},
    { id: 'g8-英语', name: '英语', icon: 'fa-language', cls: 'subject-math', lectures: [
      { num: '01', title: 'Unit 1 Where did you go on vacation?', url: 'lql_english8_u1_interactive.html', date: '2026-08-24', tags: ['英语'], new: true },
      { num: '02', title: 'Unit 2 How often do you exercise?', url: 'lql_english8_u2_interactive.html', date: '2026-08-24', tags: ['英语'], new: true },
      { num: '03', title: 'Unit 3 I\\'m more outgoing than my sister.', url: 'lql_english8_u3_interactive.html', date: '2026-08-24', tags: ['英语'], new: true },
      { num: '04', title: 'Unit 4 What\\'s the best movie theater?', url: 'lql_english8_u4_interactive.html', date: '2026-08-24', tags: ['英语'], new: true },
      { num: '05', title: 'Unit 5 Do you want to watch a game show?', url: 'lql_english8_u5_interactive.html', date: '2026-08-24', tags: ['英语'], new: true },
      { num: '06', title: 'Unit 6 I\\'m going to study computer science.', url: 'lql_english8_u6_interactive.html', date: '2026-08-24', tags: ['英语'], new: true },
      { num: '07', title: 'Unit 7 Will people have robots?', url: 'lql_english8_u7_interactive.html', date: '2026-08-24', tags: ['英语'], new: true },
      { num: '08', title: 'Unit 8 How do you make a banana milk shake?', url: 'lql_english8_u8_interactive.html', date: '2026-08-24', tags: ['英语'], new: true },
      { num: '09', title: 'Unit 9 Can you come to my party?', url: 'lql_english8_u9_interactive.html', date: '2026-08-24', tags: ['英语'], new: true },
      { num: '10', title: 'Unit 10 If you go to the party...', url: 'lql_english8_u10_interactive.html', date: '2026-08-24', tags: ['英语'], new: true }
    ]},
    { id: 'g8-物理', name: '物理', icon: 'fa-flask', cls: 'subject-physics', lectures: [
      { num: '01', title: '第1章 机械运动', url: 'lql_physics8_ch1_interactive.html', date: '2026-08-08', tags: ['物理'], new: true },
      { num: '02', title: '第2章 声现象', url: 'lql_physics8_ch2_interactive.html', date: '2026-08-08', tags: ['物理'], new: true },
      { num: '03', title: '第3章 物态变化', url: 'lql_physics8_ch3_interactive.html', date: '2026-08-08', tags: ['物理'], new: true },
      { num: '04', title: '第4章 光现象', url: 'lql_physics8_ch4_interactive.html', date: '2026-08-08', tags: ['物理'], new: true },
      { num: '05', title: '第5章 透镜及其应用', url: 'lql_physics8_ch5_interactive.html', date: '2026-08-08', tags: ['物理'], new: true },
      { num: '06', title: '第6章 质量与密度', url: 'lql_physics8_ch6_interactive.html', date: '2026-08-08', tags: ['物理'], new: true },
      { num: '07', title: '八上物理 · 早背晚默(全册综合)', url: 'lql_physics8_interactive.html', date: '2026-07-28', tags: ['物理'], new: false }
    ]},
    { id: 'g8-生物', name: '生物', icon: 'fa-leaf', cls: 'subject-chinese', lectures: [
      { num: '01', title: '第五单元 第1章 动物的主要类群', url: 'lql_bio8_ch1_interactive.html', date: '2026-08-24', tags: ['生物'], new: true },
      { num: '02', title: '第五单元 第2章 动物的运动和行为', url: 'lql_bio8_ch2_interactive.html', date: '2026-08-24', tags: ['生物'], new: true },
      { num: '03', title: '第五单元 第3章 动物在生物圈中的作用', url: 'lql_bio8_ch3_interactive.html', date: '2026-08-24', tags: ['生物'], new: true },
      { num: '04', title: '第六单元 生物的多样性及其保护', url: 'lql_bio8_ch6_interactive.html', date: '2026-08-24', tags: ['生物'], new: true }
    ]},
    { id: 'g8-历史', name: '历史', icon: 'fa-history', cls: 'subject-math', lectures: [
      { num: '01', title: '第一、二单元 侵略与探索', url: 'lql_hist8_u1_interactive.html', date: '2026-08-24', tags: ['历史'], new: true },
      { num: '02', title: '第三、四单元 革命与启蒙', url: 'lql_hist8_u2_interactive.html', date: '2026-08-24', tags: ['历史'], new: true },
      { num: '03', title: '第五、六单元 合作与抗战', url: 'lql_hist8_u3_interactive.html', date: '2026-08-24', tags: ['历史'], new: true },
      { num: '04', title: '第七、八单元 解放与建设', url: 'lql_hist8_u4_interactive.html', date: '2026-08-24', tags: ['历史'], new: true }
    ]},
    { id: 'g8-地理', name: '地理', icon: 'fa-globe', cls: 'subject-physics', lectures: [
      { num: '01', title: '第一章 从世界看中国', url: 'lql_geo8_ch1_interactive.html', date: '2026-08-24', tags: ['地理'], new: true },
      { num: '02', title: '第二章 中国的自然环境', url: 'lql_geo8_ch2_interactive.html', date: '2026-08-24', tags: ['地理'], new: true },
      { num: '03', title: '第三章 中国的自然资源', url: 'lql_geo8_ch3_interactive.html', date: '2026-08-24', tags: ['地理'], new: true },
      { num: '04', title: '第四章 中国的经济发展', url: 'lql_geo8_ch4_interactive.html', date: '2026-08-24', tags: ['地理'], new: true }
    ]},
    { id: 'g8-道法', name: '道法', icon: 'fa-gavel', cls: 'subject-math', lectures: [
      { num: '01', title: '第一单元 走进社会生活', url: 'lql_dao8_u1_interactive.html', date: '2026-08-24', tags: ['道法'], new: true },
      { num: '02', title: '第二单元 遵守社会规则', url: 'lql_dao8_u2_interactive.html', date: '2026-08-24', tags: ['道法'], new: true },
      { num: '03', title: '第三单元 勇担社会责任', url: 'lql_dao8_u3_interactive.html', date: '2026-08-24', tags: ['道法'], new: true },
      { num: '04', title: '第四单元 维护国家利益', url: 'lql_dao8_u4_interactive.html', date: '2026-08-24', tags: ['道法'], new: true }
    ]}
  ]);

  // 7年级(备用复习): 课堂笔记 6 科
  const G7 = (name, fname) => ({
    id: 'g7-' + name, name: name,
    icon: schoolIconsMap[name] || 'fa-book', cls: schoolColorsMap[name] || 'subject-math',
    lectures: [{ num: '01', title: '课堂笔记', url: fname, date: '2026-07-28', tags: [name], new: true }]
  });
  pushGrade('grade3', '7年级 · 备用复习', 'fa-child', 'subject-physics', [
    G7('数学', 'lql_数学_7grade_interactive.html'),
    G7('语文', 'lql_语文_7grade_interactive.html'),
    G7('英语', 'lql_英语_7grade_interactive.html'),
    G7('物理', 'lql_物理_7grade_interactive.html'),
    G7('生物', 'lql_生物_7grade_interactive.html'),
    G7('地理', 'lql_地理_7grade_interactive.html')
  ]);

  return data;
}
const schoolSubjectsData = buildSchoolData();
'''
s = s[:b0] + NEW_DATA + s[b1:]
log.append('  学校数据重写(9/8/7年级)')

# ---------- 6. render() 删除课外培训渲染段 ----------
seg = "  // === 课外培训 ===\n  html += renderSection('课外培训 · 互动学习', 'fa-graduation-cap', '#e67e22', 'badge-training',\n    trainingTerms.map((term, ti) => {\n      const cnt = term.subjects.reduce((a, s) => a + s.lectures.length, 0);\n      return renderTrainingTerm(term, ti, cnt);\n    }).join(''));\n"
if seg not in s:
    raise SystemExit('❌ render课外段未匹配')
s = s.replace(seg, '')
log.append('  render 删除课外培训段')

# 学校学习 section 标题带年级提示
rep("html += renderSection('学校学习', 'fa-school', '#2ecc71', 'badge-study',", "html += renderSection('学校学习', 'fa-school', '#2ecc71', 'badge-study',", '学校学习标题保留')
s = s.replace("renderSection('学校学习', 'fa-school', '#2ecc71', 'badge-study',", "renderSection('学校学习 · 人教版教材(以课本为准)', 'fa-school', '#2ecc71', 'badge-study',", 1)

# ---------- 7. LEARNED_KEY ----------
rep("const LEARNED_KEY = 'learned_pages';", "const LEARNED_KEY = 'lql_learned_pages';", 'LEARNED_KEY独立')

open(OUT, 'w', encoding='utf-8').write(s)
print('✅ 生成', OUT)
for l in log: print(l)
