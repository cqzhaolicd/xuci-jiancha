#!/usr/bin/env python3
"""Generate 7th grade subject interactive HTML pages - v3 fixed."""
import os, json

def esc(s):
    """Escape for JS single-quoted string."""
    return s.replace('\\', '\\\\').replace("'", "\\'").replace('\n', '\\n')

def js_arr_q(qs):
    parts = []
    for q in qs:
        opts = ','.join(f"'{esc(o)}'" for o in q['opts'])
        parts.append(f"{{q:'{esc(q['q'])}',opts:[{opts}],ans:{q['ans']},exp:'{esc(q['exp'])}'}}")
    return '[\n' + ',\n'.join(parts) + '\n]'

def js_arr_f(fcs):
    parts = []
    for fc in fcs:
        parts.append(f"{{front:'{esc(fc['front'])}',back:'{esc(fc['back'])}'}}")
    return '[\n' + ',\n'.join(parts) + '\n]'

def js_arr_e(errs):
    parts = []
    for e in errs:
        parts.append(f"{{title:'{esc(e['title'])}',wrong:'{esc(e['wrong'])}',right:'{esc(e['right'])}'}}")
    return '[\n' + ',\n'.join(parts) + '\n]'

def build_knowledge(cards):
    parts = []
    for cls, icon, color, title, items in cards:
        items_html = '\n'.join(f'            <li>{item}</li>' for item in items)
        parts.append(
            f'      <div class="knowledge-card {cls}"><h3><i class="fas {icon}" style="color:{color}"></i> {title}</h3><ul>\n{items_html}\n          </ul></div>'
        )
    return '\n'.join(parts)

# Read template
with open('/home/administrator/xuci-jiancha/physics_lesson3_interactive.html', 'r', encoding='utf-8') as f:
    TPL = f.read()

# Find JS array boundaries (depth starts at 1 since we consumed the opening [)
def find_end(tpl, marker):
    start = tpl.find(marker)
    if start < 0:
        return -1, -1
    rest = tpl[start + len(marker):]
    depth = 1
    end_pos = -1
    for i, ch in enumerate(rest):
        if ch == '[':
            depth += 1
        elif ch == ']':
            depth -= 1
            if depth == 0:
                end_pos = start + len(marker) + i + 1
                break
    if end_pos > 0 and end_pos < len(tpl) and tpl[end_pos] == ';':
        end_pos += 1
    return start, end_pos

Q_START, Q_END = find_end(TPL, 'const questions=[')
FC_START, FC_END = find_end(TPL, 'const flashcards=[')
ER_START, ER_END = find_end(TPL, 'const errors=[')

# Remaining markers
def generate(cfg):
    out = TPL
    
    # Simple text replacements
    out = out.replace('物理 · 测量与声学', cfg['navbar_title'])
    out = out.replace('📐 物理 · 测量与声学 · 互动学习', cfg['hero_title'])
    out = out.replace('初二暑假博学班 · 天元教育 | ⭐⭐⭐', cfg['hero_desc'])
    out = out.replace('第三讲 · 测量（声学计算+刻度尺+秒表）', cfg['section_title'])
    out = out.replace(
        '声学计算和测量工具的使用是八上物理的两大基础。声学计算一定要掌握画图列式子的方法；秒表读数和刻度尺的使用是新的重点内容，其中单位换算的关系需要熟练掌握。',
        cfg['teacher_talk_p1'])
    out = out.replace(
        '⚠️ 声学计算有三种题型：直接套公式、回声问题、和火车鸣笛问题。测量部分要注意估读和单位换算的幂次关系。做之前一定要复习！',
        cfg['teacher_talk_p2'])
    out = out.replace('30道测验题', cfg['meta_quiz'])
    out = out.replace('20张知识卡', cfg['meta_cards'])
    out = out.replace('6大易错点', cfg['meta_errors'])
    out = out.replace('数学 · 物理 · 测量与声学互动学习 | 天元教育 · 初二暑假博学班', cfg['footer_text'])
    out = out.replace("const WRONG_HISTORY_KEY='quiz_lesson3_wrong'", f"const WRONG_HISTORY_KEY='{cfg['wrong_history_key']}'")
    out = out.replace(
        "const item={subject:'物理',chapter:'测量（三）',content:q.q,correct_answer:q.opts[q.ans],my_answer:q.opts[myAns],error_reason:'概念不清',source:'练习',difficulty:3,tags:'测量,物理'}",
        f"const item={{subject:'{cfg['import_subject']}',chapter:'{cfg['import_chapter']}',content:q.q,correct_answer:q.opts[q.ans],my_answer:q.opts[myAns],error_reason:'概念不清',source:'练习',difficulty:3,tags:'{cfg['import_tags']}'}}")
    out = out.replace("subject:'物理',chapter:'测量（三）'", f"subject:'{cfg['import_subject']}',chapter:'{cfg['import_chapter']}'")
    out = out.replace("tags:'测量,物理'", f"tags:'{cfg['import_tags']}'")
    out = out.replace("localStorage.getItem('physics_measure_check')", f"localStorage.getItem('{cfg['local_storage_key']}')")
    out = out.replace("localStorage.setItem('physics_measure_check'", f"localStorage.setItem('{cfg['local_storage_key']}'")
    out = out.replace("localStorage.removeItem('physics_measure_check'", f"localStorage.removeItem('{cfg['local_storage_key']}'")
    
    # Replace JS arrays
    out = out[:Q_START] + f'const questions={js_arr_q(cfg["questions"])};' + out[Q_END:]
    out = out[:FC_START] + f'const flashcards={js_arr_f(cfg["flashcards"])};' + out[FC_END:]
    out = out[:ER_START] + f'const errors={js_arr_e(cfg["errors"])};' + out[ER_END:]
    
    # Replace knowledge grid
    khtml = build_knowledge(cfg['knowledge_cards'])
    kg_start = out.find('<div class="knowledge-grid">')
    if kg_start >= 0:
        # Find the end of this grid div
        rest = out[kg_start + len('<div class="knowledge-grid">'):]
        depth = 1
        end_pos = -1
        for i, ch in enumerate(rest):
            if rest[i:i+5] == '<div ' and 'class=' in rest[i:i+30]:
                depth += 1
            elif rest[i:i+6] == '</div>':
                depth -= 1
                if depth == 0:
                    end_pos = kg_start + len('<div class="knowledge-grid">') + i + 6
                    break
        if end_pos:
            out = out[:kg_start] + f'<div class="knowledge-grid">\n{khtml}\n      </div>' + out[end_pos:]
    
    # Remove "重点复习提示" card
    rev_start = out.find('本讲重点复习提示')
    if rev_start >= 0:
        card_start = out.rfind('<div class="card"', 0, rev_start)
        if card_start >= 0:
            rest = out[card_start + len('<div class="card"'):]
            depth = 1
            end_pos = -1
            for i, ch in enumerate(rest):
                if rest[i:i+5] == '<div ':
                    depth += 1
                elif rest[i:i+6] == '</div>':
                    depth -= 1
                    if depth == 0:
                        end_pos = card_start + len('<div class="card"') + i + 6
                        break
            if end_pos:
                out = out[:card_start] + out[end_pos:]
    
    return out


# ========== DATA ==========
# Load data from the first config file
exec(compile(open('/home/administrator/xuci-jiancha/_gen_pages.py', 'r').read(), '_gen_pages.py', 'exec'))

# Read subjects dict from the loaded namespace
import sys
# The subjects dict is in the global scope
subjects = None
for k, v in list(globals().items()):
    if k == 'subjects':
        subjects = v
        break

# If subjects wasn't found via globals trick, reload properly
if subjects is None:
    # Just copy the namespace
    ns = {}
    exec(open('/home/administrator/xuci-jiancha/_gen_pages.py', 'r').read(), ns)
    subjects = ns.get('subjects', {})
    if not subjects:
        print("ERROR: Could not load subjects data!")
        sys.exit(1)

print(f"Loaded {len(subjects)} subjects from config")

base = '/home/administrator/xuci-jiancha'
for name, cfg in subjects.items():
    print(f"Generating {name}.html...")
    html = generate(cfg)
    path = f'{base}/{name}.html'
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"  => {path} ({len(html)} bytes)")

print("Done! All 6 pages regenerated.")
