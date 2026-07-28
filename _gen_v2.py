#!/usr/bin/env python3
"""Generate 7th grade subject interactive HTML pages - FIXED version."""
import re

def escape_js(s):
    """Escape a string for embedding in JS single-quoted strings."""
    return s.replace('\\', '\\\\').replace("'", "\\'").replace('\n', '\\n')

SUBJECTS_DATA = {}

# Read and parse template
with open('/home/administrator/xuci-jiancha/physics_lesson3_interactive.html', 'r', encoding='utf-8') as f:
    TEMPLATE = f.read()

# Find template JS data boundaries
def find_data_boundaries(template, var_name):
    """Find the start and end positions of a JS variable definition."""
    start_marker = f'const {var_name}=['
    q_start = template.find(start_marker)
    if q_start < 0:
        raise ValueError(f'Could not find {start_marker} in template')
    # Find the end - look for ]; that's followed by \n\nconst or \nconst
    search_from = q_start + len(start_marker)
    remaining = template[search_from:]
    # Search for ]; followed by whitespace then const or \n or similar
    m = re.search(r'\];\s*\n', remaining)
    if m:
        end = search_from + m.end()
        return q_start, end
    # Fallback - find ]; at depth 0
    depth = 1
    end = -1
    for i, ch in enumerate(remaining):
        if ch == '[':
            depth += 1
        elif ch == ']':
            depth -= 1
            if depth == 0:
                # Check if next char is ;
                if i + 1 < len(remaining) and remaining[i+1] == ';':
                    end = search_from + i + 2
                else:
                    end = search_from + i + 1
                break
    if end < 0:
        raise ValueError(f'Could not find end of {var_name}')
    return q_start, end

TEMPLATE_BOUNDARIES = {}
for var in ['questions', 'flashcards', 'errors']:
    try:
        TEMPLATE_BOUNDARIES[var] = find_data_boundaries(TEMPLATE, var)
    except ValueError as e:
        print(f"Warning: {e}")

# Also find unique strings for replacement
TEMPLATE_MARKERS = {
    'navbar_back': '物理 · 测量与声学',
    'hero_title': '📐 物理 · 测量与声学 · 互动学习',
    'hero_desc': '初二暑假博学班 · 天元教育 | ⭐⭐⭐',
    'section_title': '第三讲 · 测量（声学计算+刻度尺+秒表）',
    'teacher_p1': '声学计算和测量工具的使用是八上物理的两大基础。声学计算一定要掌握画图列式子的方法；秒表读数和刻度尺的使用是新的重点内容，其中单位换算的关系需要熟练掌握。',
    'teacher_p2': '⚠️ 声学计算有三种题型：直接套公式、回声问题、和火车鸣笛问题。测量部分要注意估读和单位换算的幂次关系。做之前一定要复习！',
    'meta_quiz': '30道测验题',
    'meta_cards': '20张知识卡',
    'meta_errors': '6大易错点',
    'footer': '数学 · 物理 · 测量与声学互动学习 | 天元教育 · 初二暑假博学班',
    'wrong_key': "const WRONG_HISTORY_KEY='quiz_lesson3_wrong'",
    'import_item': "const item={subject:'物理',chapter:'测量（三）',content:q.q,correct_answer:q.opts[q.ans],my_answer:q.opts[myAns],error_reason:'概念不清',source:'练习',difficulty:3,tags:'测量,物理'}",
    'import_chapter': "subject:'物理',chapter:'测量（三）'",
    'import_tags': "tags:'测量,物理'",
    'ls_get': "localStorage.getItem('physics_measure_check')",
    'ls_set': "localStorage.setItem('physics_measure_check'",
    'ls_remove': "localStorage.removeItem('physics_measure_check'",
}

print(f"Template ready: {len(TEMPLATE)} chars")
print(f"Template boundaries: {TEMPLATE_BOUNDARIES}")

# Now create the generation function using the template with proper boundaries
def generate_page(name, cfg):
    """Generate a full HTML page for one subject."""
    result = TEMPLATE
    
    # Replace template markers
    result = result.replace('物理 · 测量与声学', cfg['navbar_title'])
    result = result.replace('📐 物理 · 测量与声学 · 互动学习', cfg['hero_title'])
    result = result.replace('初二暑假博学班 · 天元教育 | ⭐⭐⭐', cfg['hero_desc'])
    result = result.replace('第三讲 · 测量（声学计算+刻度尺+秒表）', cfg['section_title'])
    result = result.replace(
        '声学计算和测量工具的使用是八上物理的两大基础。声学计算一定要掌握画图列式子的方法；秒表读数和刻度尺的使用是新的重点内容，其中单位换算的关系需要熟练掌握。',
        cfg['teacher_p1'])
    result = result.replace(
        '⚠️ 声学计算有三种题型：直接套公式、回声问题、和火车鸣笛问题。测量部分要注意估读和单位换算的幂次关系。做之前一定要复习！',
        cfg['teacher_p2'])
    result = result.replace('30道测验题', cfg['meta_quiz'])
    result = result.replace('20张知识卡', cfg['meta_cards'])
    result = result.replace('6大易错点', cfg['meta_errors'])
    result = result.replace('数学 · 物理 · 测量与声学互动学习 | 天元教育 · 初二暑假博学班', cfg['footer'])
    result = result.replace("const WRONG_HISTORY_KEY='quiz_lesson3_wrong'", f"const WRONG_HISTORY_KEY='{cfg['wrong_history_key']}'")
    result = result.replace(
        "const item={subject:'物理',chapter:'测量（三）',content:q.q,correct_answer:q.opts[q.ans],my_answer:q.opts[myAns],error_reason:'概念不清',source:'练习',difficulty:3,tags:'测量,物理'}",
        f"const item={{subject:'{cfg['import_subject']}',chapter:'{cfg['import_chapter']}',content:q.q,correct_answer:q.opts[q.ans],my_answer:q.opts[myAns],error_reason:'概念不清',source:'练习',difficulty:3,tags:'{cfg['import_tags']}'}}")
    result = result.replace("subject:'物理',chapter:'测量（三）'", f"subject:'{cfg['import_subject']}',chapter:'{cfg['import_chapter']}'")
    result = result.replace("tags:'测量,物理'", f"tags:'{cfg['import_tags']}'")
    result = result.replace("localStorage.getItem('physics_measure_check')", f"localStorage.getItem('{cfg['local_storage_key']}')")
    result = result.replace("localStorage.setItem('physics_measure_check'", f"localStorage.setItem('{cfg['local_storage_key']}'")
    result = result.replace("localStorage.removeItem('physics_measure_check'", f"localStorage.removeItem('{cfg['local_storage_key']}'")
    
    # Build knowledge grid HTML
    khtml = ''
    for cls, icon, color, title, items in cfg['knowledge_cards']:
        items_html = '\n'.join(f'            <li>{item}</li>' for item in items)
        khtml += f'''      <div class="knowledge-card {cls}"><h3><i class="fas {icon}" style="color:{color}"></i> {title}</h3><ul>
{items_html}
          </ul></div>
'''
    
    # Replace knowledge grid content
    kg_start = result.find('<div class="knowledge-grid">')
    if kg_start >= 0:
        # Find the end of the grid div
        grid_start = kg_start
        # Find </div> that closes the grid
        depth = 0
        found = False
        for i in range(grid_start, len(result)):
            if result[i:i+5] == '<div ' or result[i:i+5] == '<div ':
                if result[i:i+6] != '<div c' and result[i:i+6] != '<div c':
                    pass
                # Check for opening div
                if '<div ' in result[i:i+20]:
                    depth += 1
            elif result[i:i+6] == '</div>':
                depth -= 1
                if depth == 0:
                    # This is the closing </div> of knowledge-grid
                    kg_end = i + 6
                    found = True
                    break
        
        if found:
            result = result[:kg_start] + f'<div class="knowledge-grid">\n{khtml}      </div>' + result[kg_end:]
    
    # Replace "重点复习提示" card - remove it
    review_start = result.find('本讲重点复习提示')
    if review_start >= 0:
        # Find enclosing card
        card_start = result.rfind('<div class="card"', 0, review_start)
        if card_start >= 0:
            inner = result[card_start:]
            depth = 0
            end_pos = -1
            for i, ch in enumerate(inner):
                if inner[i:i+5] == '<div ':
                    depth += 1
                elif inner[i:i+6] == '</div>':
                    depth -= 1
                    if depth == 0:
                        end_pos = card_start + i + 6
                        break
            if end_pos:
                result = result[:card_start] + result[end_pos:]
    
    # Build and replace JS data arrays
    def build_questions_js(qs):
        parts = []
        for q in qs:
            opts = ','.join(f"'{escape_js(o)}'" for o in q['opts'])
            parts.append(f"{{q:'{escape_js(q['q'])}',opts:[{opts}],ans:{q['ans']},exp:'{escape_js(q['exp'])}'}}")
        return '[\n' + ',\n'.join(parts) + '\n]'
    
    def build_flashcards_js(fcs):
        parts = []
        for fc in fcs:
            parts.append(f"{{front:'{escape_js(fc['front'])}',back:'{escape_js(fc['back'])}'}}")
        return '[\n' + ',\n'.join(parts) + '\n]'
    
    def build_errors_js(errs):
        parts = []
        for e in errs:
            parts.append(f"{{title:'{escape_js(e['title'])}',wrong:'{escape_js(e['wrong'])}',right:'{escape_js(e['right'])}'}}")
        return '[\n' + ',\n'.join(parts) + '\n]'
    
    qjs = build_questions_js(cfg['questions'])
    fjs = build_flashcards_js(cfg['flashcards'])
    ejs = build_errors_js(cfg['errors'])
    
    # Replace JS arrays using boundaries
    for var_name, (start, end) in TEMPLATE_BOUNDARIES.items():
        if var_name == 'questions':
            repl = f'const questions={qjs};'
        elif var_name == 'flashcards':
            repl = f'const flashcards={fjs};'
        elif var_name == 'errors':
            repl = f'const errors={ejs};'
        else:
            continue
        result = result[:start] + repl + result[end:]
    
    return result


# =============== DEFINE ALL SUBJECTS ===============

# MATH
SUBJECTS_DATA['math_7grade_interactive'] = {
    "navbar_title": "数学 · 7年级课堂笔记",
    "hero_title": "📐 数学 · 7年级课堂笔记 · 互动学习",
    "hero_desc": "若琳课堂笔记 · 知识点归类 | ⭐⭐⭐",
    "meta_quiz": "15道测验题",
    "meta_cards": "10张知识卡",
    "meta_errors": "7大易错点",
    "section_title": "第七年级 · 数学（一次函数+三角形+全等模型+代数+概率）",
    "teacher_p1": "数学期末复习涵盖了七大知识模块：一次函数应用题分段讨论、角平分线与中垂线模型、三角形面积比例、动点最值问题、全等三角形核心模型、代数式计算与基础易错、概率题答题规范。",
    "teacher_p2": "⚠️ 注意分段讨论时不要遗漏区间，几何书写三个条件缺一不可，动点问题先判断轨迹！",
    "footer": "数学 · 7年级课堂笔记互动学习 | 若琳课堂笔记",
    "wrong_history_key": "quiz_math7_wrong",
    "import_subject": "数学",
    "import_chapter": "7年级",
    "import_tags": "数学,7年级",
    "local_storage_key": "math7_errors_check",
    "knowledge_cards": [],
    "questions": [],
    "flashcards": [],
    "errors": [],
}

# (Data loading from the _gen_pages.py module)
# Let me load the data from the previous file
exec(compile(open('/home/administrator/xuci-jiancha/_gen_pages.py').read(), '/home/administrator/xuci-jiancha/_gen_pages.py', 'exec'))
