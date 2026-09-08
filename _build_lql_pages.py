#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
_build_lql_pages.py — 批量克隆若琳学习中心"学校学习区+错题库工具"页面 → 刘秋灵学习中心(lql_前缀)
规则:
  * 文件名加 lql_ 前缀
  * '若琳' → '刘秋灵'
  * href="index.html" / 'index.html' → 'liuqiuling_index.html'
  * IMPORT_KEY 值 'wrong_bank_import' → 'lql_wrong_bank_import'
  * localStorage key 内嵌旧文件名段 → 加 lql_ 前缀(长段先换, 短段负向后视防重复)
  * wrong_bank 的 LS_KEY 'wrong_bank_data' → 'lql_wrong_bank_data'
  * three_brush 的 LS_KEY 'three_brush_list' → 'lql_three_brush_list'
  * preview 页 LS 前缀 preview_xxx_ → lql_preview_xxx_
运行: python3 _build_lql_pages.py
"""
import re, os, shutil, sys

SRC = '/home/administrator/xuci-jiancha'
DST = SRC  # 同目录平铺, lql_ 前缀

PAGES = [
    # 7年级课堂笔记(6)
    '数学_7grade_interactive.html','语文_7grade_interactive.html','英语_7grade_interactive.html',
    '物理_7grade_interactive.html','生物_7grade_interactive.html','地理_7grade_interactive.html',
    # 8年级上分章(46)
    'math8_ch1_interactive.html','math8_ch2_interactive.html','math8_ch3_interactive.html',
    'math8_ch4_interactive.html','math8_ch5_interactive.html','math8_ch6_interactive.html',
    'math8_ch7_interactive.html',
    'chinese8_u1_interactive.html','chinese8_u2_interactive.html','chinese8_u3_interactive.html',
    'chinese8_u4_interactive.html','chinese8_u5_interactive.html','chinese8_u6_interactive.html',
    'english8_u1_interactive.html','english8_u2_interactive.html','english8_u3_interactive.html',
    'english8_u4_interactive.html','english8_u5_interactive.html','english8_u6_interactive.html',
    'english8_u7_interactive.html','english8_u8_interactive.html','english8_u9_interactive.html',
    'english8_u10_interactive.html',
    'physics8_ch1_interactive.html','physics8_ch2_interactive.html','physics8_ch3_interactive.html',
    'physics8_ch4_interactive.html','physics8_ch5_interactive.html','physics8_ch6_interactive.html',
    'physics8_interactive.html',
    'bio8_ch1_interactive.html','bio8_ch2_interactive.html','bio8_ch3_interactive.html',
    'bio8_ch6_interactive.html',
    'geo8_ch1_interactive.html','geo8_ch2_interactive.html','geo8_ch3_interactive.html',
    'geo8_ch4_interactive.html',
    'hist8_u1_interactive.html','hist8_u2_interactive.html','hist8_u3_interactive.html',
    'hist8_u4_interactive.html',
    'dao8_u1_interactive.html','dao8_u2_interactive.html','dao8_u3_interactive.html',
    'dao8_u4_interactive.html',
    # 综合(1)
    '虚实词逐义检查卷.html',
    # 预习闯关游戏(4)
    'preview_challenge_math8.html','preview_challenge_physics8.html',
    'preview_challenge_chinese8.html','preview_challenge_english8.html',
    # 占位动态页(1)
    'school_interactive.html',
    # 工具(3)
    'wrong_bank.html','three_brush.html','wubufa_card.html',
]

def transform(src_name):
    stem = src_name[:-5]                    # 去 .html
    short = stem[:-12] if stem.endswith('_interactive') else stem  # 去 _interactive
    path = os.path.join(SRC, src_name)
    with open(path, encoding='utf-8') as f:
        s = f.read()
    log = []
    def rep(old, new, tag, cnt_max=None):
        nonlocal s
        n = s.count(old)
        if n:
            s = s.replace(old, new)
            log.append(f'  {tag}: {n}')
    def rep_re(sub, old_pat, new_pat, tag):
        nonlocal s
        s, n = re.subn(old_pat, new_pat, s)
        if n:
            log.append(f'  {tag}: {n}')

    # 1) 品牌
    rep('若琳', '刘秋灵', '若琳→刘秋灵')
    # 2) 回链
    rep('index.html', 'liuqiuling_index.html', '回链→liuqiuling_index.html')
    # 3) 错题导入 key (互动页 IMPORT_KEY + wrong_bank 引用)
    rep("'wrong_bank_import'", "'lql_wrong_bank_import'", "IMPORT_KEY→lql")
    rep('wrong_bank_import', 'lql_wrong_bank_import', 'wrong_bank_import全文')
    # 4) wrong_bank / three_brush 数据 key
    rep("'wrong_bank_data'", "'lql_wrong_bank_data'", "LS_KEY data→lql")
    rep("'three_brush_list'", "'lql_three_brush_list'", "three_brush key→lql")
    # 5) preview 页 LS 前缀
    for p in ['coins','stars','unlocked','cleared','wrong','boss']:
        rep(f"'preview_{p}_'", f"'lql_preview_{p}_'", f"preview_{p}前缀→lql")
    # 6) key 内嵌文件名段 (长段先, 短段负向后视)
    if stem != short:
        n = s.count(stem)
        if n:
            s = s.replace(stem, 'lql_' + stem)
            log.append(f'  stem→lql: {n}')
    if short and short != stem:
        # 负向后视防 lql_ 前缀重复
        s2, n2 = re.subn(r'(?<!lql_)' + re.escape(short), 'lql_' + short, s)
        if n2:
            # 长段替换后再换短段; 但短段替换可能伤到 stem 新串里的 short?
            # stem 已变 lql_stem => 其中 short 前有 lql_ 会被负向后视挡住 ✓
            s = s2
            log.append(f'  short→lql: {n2}')
    # 7) 保留文件内若有指向其它本地页(非index)且被克隆 → 转 lql_ 名
    for other in PAGES:
        if other == src_name:
            continue
        o_stem = other[:-5]
        if other in s or (o_stem in s):
            # 页面内容引用同批其他页面(罕见)
            s = s.replace(other, 'lql_' + other)
            s = s.replace(o_stem, 'lql_' + o_stem)
            log.append(f'  内链{other}→lql_{other}')
    return s, log

def main():
    os.makedirs(DST, exist_ok=True)
    errors = []
    for name in PAGES:
        src_path = os.path.join(SRC, name)
        if not os.path.exists(src_path):
            errors.append(f'MISSING: {name}')
            continue
        new_name = 'lql_' + name
        try:
            content, log = transform(name)
        except Exception as e:
            errors.append(f'ERR transform {name}: {e}')
            continue
        with open(os.path.join(DST, new_name), 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'✅ {name} -> {new_name}')
        for l in log:
            print(l)
    if errors:
        print('\n⚠️ ERRORS:')
        for e in errors:
            print(' ', e)
        sys.exit(1)
    print(f'\n完成: {len(PAGES)} 个文件')

if __name__ == '__main__':
    main()
