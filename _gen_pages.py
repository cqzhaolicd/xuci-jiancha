#!/usr/bin/env python3
"""Generate 7th grade subject interactive HTML pages."""
import json, re

def read_template():
    with open('/home/administrator/xuci-jiancha/physics_lesson3_interactive.html', 'r', encoding='utf-8') as f:
        return f.read()

def write_file(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"  ✓ {path}")

def build_knowledge_html(cards):
    """Build knowledge grid HTML from card data."""
    parts = []
    for cls, icon, color, title, items in cards:
        items_html = ''.join(f'<li>{item}</li>' for item in items)
        parts.append(
            f'<div class="knowledge-card {cls}"><h3><i class="fas {icon}" style="color:{color}"></i> {title}</h3><ul>\n'
            f'{items_html}\n'
            f'</ul></div>'
        )
    return '\n'.join(parts)

def build_questions_js(questions):
    """Build questions JS array."""
    parts = []
    for q in questions:
        opts = ','.join(f"'{o}'" for o in q['opts'])
        parts.append(
            f"{{q:'{q['q']}',opts:[{opts}],ans:{q['ans']},exp:'{q['exp']}'}}"
        )
    return '[\n' + ',\n'.join(parts) + '\n]'

def build_flashcards_js(flashcards):
    """Build flashcards JS array."""
    parts = []
    for fc in flashcards:
        parts.append(
            f"{{front:'{fc['front']}',back:'{fc['back']}'}}"
        )
    return '[\n' + ',\n'.join(parts) + '\n]'

def build_errors_js(errors):
    """Build errors JS array."""
    parts = []
    for e in errors:
        # Escape single quotes within the strings
        title = e['title'].replace("'", "\\'")
        wrong = e['wrong'].replace("'", "\\'")
        right = e['right'].replace("'", "\\'")
        parts.append(
            f"{{title:'{title}',wrong:'{wrong}',right:'{right}'}}"
        )
    return '[\n' + ',\n'.join(parts) + '\n]'

def escape_js(s):
    """Escape a string for embedding in JS single-quoted strings."""
    return s.replace('\\', '\\\\').replace("'", "\\'").replace('\n', '\\n')


# ===== Subject configurations =====
subjects = {}

# ---- Math ----
subjects['math_7grade_interactive'] = {
    "navbar_back": "index.html",
    "navbar_title": "数学 · 7年级课堂笔记",
    "hero_title": "数学 · 7年级课堂笔记 · 互动学习",
    "hero_desc": "若琳课堂笔记 · 知识点归类 | ⭐⭐⭐",
    "meta_quiz": "15道测验题",
    "meta_cards": "10张知识卡",
    "meta_errors": "7大易错点",
    "section_title": "第七年级 · 数学（一次函数+三角形+全等模型+代数+概率）",
    "teacher_talk_title": "教师寄语",
    "teacher_talk_p1": "数学期末复习涵盖了七大知识模块：一次函数应用题分段讨论、角平分线与中垂线模型、三角形面积比例、动点最值问题、全等三角形核心模型、代数式计算与基础易错、概率题答题规范。",
    "teacher_talk_p2": "⚠️ 注意分段讨论时不要遗漏区间，几何书写三个条件缺一不可，动点问题先判断轨迹！",
    "footer_text": "数学 · 7年级课堂笔记互动学习 | 若琳课堂笔记",
    "wrong_history_key": "quiz_math7_wrong",
    "import_subject": "数学",
    "import_chapter": "7年级",
    "import_tags": "数学,7年级",
    "local_storage_key": "math7_errors_check",

    "knowledge_cards": [
        ("c1", "fa-chart-line", "#667eea", "一次函数应用题", [
            "分段设函数关系式 → 分类讨论 → 列绝对值方程求解",
            "电车充电：满电60千瓦，分0~300km和>300km两段",
            "快慢车相遇：纵坐标含义转换，联立方程求解",
            "双车行程：甲去程60km/h、返程90km/h，分段计算路程差",
            "工厂零件题：故障→速度提升2倍，绝对值方程求相差时间",
            "卸货分段：甲100吨/小时，乙前2小时150后段50吨/小时",
        ]),
        ("c2", "fa-ruler-triangle", "#e67e22", "角平分线与中垂线", [
            "角平分线：将角分成两个相等角的射线，点到角两边距离相等",
            "内心：三条内角平分线交点；旁心：两个外角+一个内角平分线交点",
            "双角平分线模型：两内交角=90°+½∠A，一内一外交角=½∠A",
            "中垂线：垂直且平分线段，中垂线上的点到线段两端距离相等",
            "辅助线：对称法、双垂法、截长补短法、平行线法",
        ]),
        ("c3", "fa-shapes", "#2ecc71", "三角形面积与比例模型", [
            "比例法求面积：设未知数，利用线段比例和中线性质推导",
            "折叠问题：图形还原→平角180°计算折叠角",
            "割补法：不规则三角形补成矩形，减去三个直角三角形面积",
            "同高三角形：面积比等于底边比",
            "中线分面积：中线将三角形面积平分为1/2",
        ]),
        ("c4", "fa-arrows", "#3498db", "动点最值问题", [
            "逆等线构造全等：将BF+CE转化为BF+FG",
            "手拉手模型求最小值：两共顶点等边三角形→全等→垂线段最短",
            "将军饮马模型：两点之间线段最短；点到直线垂线段最短",
            "最值转化规则：和的最小值→异侧连线；差的最大值→同侧延长",
        ]),
        ("c1", "fa-puzzle-piece", "#9b59b6", "全等三角形核心模型", [
            "一线三等角：三个角相等，通过角度和差推等角→AAS证明全等",
            "手拉手模型：两个等边/等腰直角共顶点→SAS全等",
            "K型全等：等腰直角过直角顶点做垂线段构造全等",
            "动点全等：对应关系不唯一时需分两种情况讨论",
            "尺规作图原理：作已知角（SSS）、中垂线、角平分线（SSS）",
        ]),
        ("c2", "fa-square-root-variable", "#1abc9c", "代数计算与易错", [
            "完全平方公式：(A±B)² = A²±2AB+B²",
            "平方差公式：在面积转化题中常用",
            "科学计数法：1纳米=10⁻⁹米，95纳米=9.5×10⁻⁸米",
            "多项式参数题：不含x²项→合并同类项令系数为0",
            "不等式：\u2018不大于2\u2019即≤2，满足条件的整数只有-2",
        ]),
        ("c3", "fa-dice", "#f39c12", "概率题答题规范", [
            "解答题不能直接写约分结果，先写原始分子分母",
            "注意\u2018放回\u2019和\u2018不放回\u2019的区别",
            "判断公平性必须分别算出双方获胜概率再对比",
        ]),
    ],

    "questions": [
        {'q': '分段函数应用题的解题第一步是', 'opts': ['A. 直接列方程', 'B. 分段设函数关系式', 'C. 画图像', 'D. 代入数值'], 'ans': 1, 'exp': '分段函数应用题应先分段设函数关系式，再分类讨论求解。'},
        {'q': '电车充电问题中，满电60千瓦，家用充电0.5元/千瓦，下列哪个是正确思路？', 'opts': ['A. 直接计算总费用', 'B. 分0~300km和>300km两段推导剩余电量关系式', 'C. 只用公共充电费用', 'D. 不分段计算'], 'ans': 1, 'exp': '需要分0~300km和>300km两段推导剩余电量关系式，考虑损耗率1.2。'},
        {'q': '快慢车相遇问题中，纵坐标的含义是', 'opts': ['A. 距离各自出发地', 'B. 距离甲地', 'C. 总路程', 'D. 时间'], 'ans': 0, 'exp': '纵坐标是距离各自出发地的距离，转换后联立方程求解相遇时间。'},
        {'q': '角平分线上的点到角两边的距离', 'opts': ['A. 相等', 'B. 不相等', 'C. 和为定值', 'D. 积为定值'], 'ans': 0, 'exp': '角平分线上的点到角两边距离相等，判定同理。'},
        {'q': '三角形内心的定义是', 'opts': ['A. 三条中线的交点', 'B. 三条角平分线的交点', 'C. 三条高的交点', 'D. 三边中垂线的交点'], 'ans': 1, 'exp': '内心是三条内角平分线的交点（内切圆圆心）。'},
        {'q': '同高三角形的面积比等于', 'opts': ['A. 底边比', 'B. 高之比', 'C. 周长比', 'D. 角度比'], 'ans': 0, 'exp': '同高三角形的面积比等于底边比。'},
        {'q': '折叠问题中，折叠角的计算依据是', 'opts': ['A. 勾股定理', 'B. 平角180°', 'C. 面积公式', 'D. 三角形内角和'], 'ans': 1, 'exp': '折叠问题先将图形还原，利用平角180°计算折叠角。'},
        {'q': '将军饮马模型的核心原理是', 'opts': ['A. 三角形内角和', 'B. 两点之间线段最短', 'C. 面积不变', 'D. 角度相等'], 'ans': 1, 'exp': '将军饮马模型利用两点之间线段最短，点到直线垂线段最短求解最值。'},
        {'q': '一线三等角模型中，三个角的关系是', 'opts': ['A. 必须都是直角', 'B. 三个角相等即可', 'C. 两个角互补', 'D. 角和为180°'], 'ans': 1, 'exp': '一线三等角不要求一定是三个直角，只要三个角相等，通过角度和差推等角→AAS证明全等。'},
        {'q': 'SSA为什么不能证明全等？', 'opts': ['A. 因为两边一角对应相等', 'B. 因为满足条件的三角形可能有两个', 'C. 因为角不是夹角', 'D. 因为边不够'], 'ans': 1, 'exp': 'SSA不存在的原因是边长满足条件的三角形可以有两个，不确定顶点需分类讨论。'},
        {'q': 'K型全等中，过等腰直角三角形的直角顶点作一条直线，应如何构造全等？', 'opts': ['A. 直接连接', 'B. 做两个垂线段构造全等', 'C. 做角平分线', 'D. 做中线'], 'ans': 1, 'exp': 'K型全等：等腰直角三角形过直角顶点的直线，做两个垂线段构造全等。'},
        {'q': '完全平方公式是', 'opts': ['A. (A±B)² = A²±B²', 'B. (A±B)² = A²±2AB+B²', 'C. (A±B)² = A²±AB+B²', 'D. (A±B)² = A²+B²'], 'ans': 1, 'exp': '完全平方公式：(A±B)² = A²±2AB+B²'},
        {'q': '1纳米等于多少米？', 'opts': ['A. 10⁻⁶米', 'B. 10⁻⁸米', 'C. 10⁻⁹米', 'D. 10⁻¹²米'], 'ans': 2, 'exp': '1纳米=10⁻⁹米。'},
        {'q': '多项式中"不含x²项"的意思是', 'opts': ['A. 没有x²这个字母', 'B. 合并后x²的系数为0', 'C. x²的系数为1', 'D. x²的系数为-1'], 'ans': 1, 'exp': '"不含x²项"→合并同类项后令x²的系数为0。'},
        {'q': '概率题中判断游戏是否公平，方法是', 'opts': ['A. 只算一个人获胜概率', 'B. 分别算出双方获胜概率再对比', 'C. 看谁更容易赢', 'D. 猜硬币决定'], 'ans': 1, 'exp': '判断公平性必须分别算出双方获胜概率再对比。注意"放回"和"不放回"的区别。'},
    ],

    "flashcards": [
        {'front': '分段函数解题步骤', 'back': '① 分段设函数关系式<br>② 分类讨论<br>③ 列绝对值方程求解<br>④ 验证解在区间内'},
        {'front': '双角平分线模型', 'back': '<span class="f-formula">两内交角 = 90° + ½∠A</span><br><span class="f-formula">一内一外交角 = ½∠A</span>'},
        {'front': '同高三角形面积比', 'back': '<span class="f-formula">S₁:S₂ = a₁:a₂</span><br>面积比等于底边比'},
        {'front': '将军饮马模型', 'back': '和的最小值→转化到直线异侧连线<br>差的绝对值最大值→同侧延长连线'},
        {'front': '一线三等角全等', 'back': '三个角相等→角度和差推等角<br>→ AAS证明全等'},
        {'front': '手拉手模型', 'back': '两共顶点等边三角形<br>→ SAS全等<br>→ BD和CE夹角=顶角'},
        {'front': '完全平方公式', 'back': '<span class="f-formula">(A±B)² = A²±2AB+B²</span>'},
        {'front': '科学计数法换算', 'back': '1nm = 10⁻⁹m<br>1μm = 10⁻⁶m<br>单位换算三步法：抄数值→换单位→科学计数法'},
        {'front': '概率答题规范', 'back': '① 先写原始分子分母（不约分）<br>② 区别"放回"和"不放回"<br>③ 分别算双方概率再比'},
        {'front': '三角形面积割补法', 'back': '不规则三角形→补成矩形<br>→减去三个直角三角形面积'},
    ],

    "errors": [
        {'title': '分段讨论遗漏区间 ❌', 'wrong': '分段函数只考虑部分区间，忘记覆盖所有情况。', 'right': '分段函数必须分<span class="hl">所有可能区间</span>，每一段都列方程，解的取值范围要验证是否在该区间内。'},
        {'title': '纵坐标含义理解错误 ❌', 'wrong': '把"距离各自出发地"当成"距离甲地"来算。', 'right': '仔细读题确认纵坐标的<span class="hl">实际含义</span>，有时需要转换坐标含义再联立方程。'},
        {'title': '几何书写缺条件 ❌', 'wrong': '证明全等时只写两个条件就下结论。', 'right': '几何证明要写全<span class="hl">三个条件</span>（如SSS/SAS/ASA/AAS），缺一不可。'},
        {'title': '动点轨迹判断错误 ❌', 'wrong': '动点走直线当走曲线算，或者想当然认为轨迹是圆的。', 'right': '先判断动点的<span class="hl">运动轨迹</span>（直线/射线/线段），再根据轨迹选择最值方法。'},
        {'title': 'SSA做全等 ❌', 'wrong': '看到两边和一角就认为全等成立。', 'right': '<span class="hl">SSA不存在</span>！边长满足条件的三角形可能有2个，不确定顶点需分类讨论。'},
        {'title': '绝对值方程忘验证 ❌', 'wrong': '解出绝对值方程直接写答案，不知道是否在定义区间内。', 'right': '绝对值方程的解必须<span class="hl">验证是否在区间内</span>，不在的解需要舍去。'},
        {'title': '概率题直接写约分结果 ❌', 'wrong': '概率直接写1/2、2/3等约分后结果。', 'right': '解答题先写原始分子分母（如6/12），再约分。注意"放回"和"不放回"的区别。'},
    ],
}

# ---- English ----
subjects['english_7grade_interactive'] = {
    "navbar_back": "index.html",
    "navbar_title": "英语 · 7年级课堂笔记",
    "hero_title": "英语 · 7年级课堂笔记 · 互动学习",
    "hero_desc": "若琳课堂笔记 · 知识点归类 | ⭐⭐⭐",
    "meta_quiz": "12道测验题",
    "meta_cards": "8张知识卡",
    "meta_errors": "5大易错点",
    "section_title": "第七年级 · 英语（阅读技巧+语法词汇+作文+主题阅读）",
    "teacher_talk_title": "教师寄语",
    "teacher_talk_p1": "英语期末复习涵盖了四大模块：阅读解题技巧（主旨题、细节题、猜词题、推断题、态度题）、语法与词汇要点（非谓语动词、时态、固定搭配）、英语写作技巧（发言稿、看图写话、日记）、主题阅读内容。",
    "teacher_talk_p2": "⚠️ 阅读注意题文同序原则；语法时态先找时间标志词；作文不要干列要点，要有逻辑连接！",
    "footer_text": "英语 · 7年级课堂笔记互动学习 | 若琳课堂笔记",
    "wrong_history_key": "quiz_english7_wrong",
    "import_subject": "英语",
    "import_chapter": "7年级",
    "import_tags": "英语,7年级",
    "local_storage_key": "english7_errors_check",

    "knowledge_cards": [
        ("c1", "fa-book-open", "#667eea", "阅读解题技巧", [
            "主旨题：抓重复信息 + 看首句结尾 + 按文体判断",
            "细节题：优先抓大写人名地名、数字符号、具体信息",
            "题文同序原则：第二题找不到先做第三题",
            "关注逻辑词：because/so that因果、however/but转折",
            "猜词题：代词往前找，熟词生义结合语境",
            "推断题：不选和原文一样的，基于原文引申",
            "态度题：明确谁对谁的态度，看形容词情感色彩",
        ]),
        ("c2", "fa-spell-check", "#e67e22", "语法与词汇要点", [
            "非谓语动词：介词to后接doing，不定式to后接do",
            "常考10组：look forward to doing / give up doing / mind doing 等",
            "时态判断：四年前/去年→过去式；每天→一般现在时",
            "stop to do（停下去做）vs stop doing（停下正在做的）",
            "used to do（过去常常）/ be used to doing（习惯于）",
            "see sb do（全过程）/ see sb doing（正在做）",
            "-ed形容人的感受，-ing形容事物性质",
        ]),
        ("c3", "fa-pen-fancy", "#2ecc71", "英语写作技巧", [
            "核心思路：先抓人物→再抓背景→逻辑融合，不要干列要点",
            "安全主题发言稿：学校+饮食+交通+网络安全四个方向",
            "看图写话：Once upon a time句式，按顺序梳理情节",
            "日记写作：整体一般过去时，习惯/真理用一般现在时",
            "作文结构：开头主题→中间事件支撑→结尾收获意义",
            "运动会广播稿：增加观众细节，升华运动精神/团队合作",
        ]),
        ("c4", "fa-newspaper", "#3498db", "英语阅读主题", [
            "中国医疗优势：等候时间短、医护友好、花费低",
            "反校园霸凌新规（2026.1.1）：霸凌四类，学校需预防调查",
            "全球变暖：节约用水=减少能源消耗，现在进行时回答",
            "中国南北天气差异：冬季差异大，and前后语法功能一致",
            "自动扶梯规则：站右走左存在问题→所有人站立效率更高",
        ]),
    ],

    "questions": [
        {'q': '主旨题的常见提问方式不包括', 'opts': ['A. main idea', 'B. best title', 'C. purpose of the author', 'D. What color is it'], 'ans': 3, 'exp': '主旨题识别：main idea / best title / purpose of the author。D是细节题。'},
        {'q': '细节题定位时应优先抓什么信息？', 'opts': ['A. 形容词', 'B. 虚词', 'C. 大写人名地名、数字符号', 'D. 连词'], 'ans': 2, 'exp': '细节题优先抓大写人名地名、数字符号、具体信息。题干无法定位用选项定位。'},
        {'q': 'look forward to 后面应该接什么？', 'opts': ['A. 动词原形', 'B. doing形式', 'C. 过去分词', 'D. 不定式'], 'ans': 1, 'exp': '介词to后接doing。注意：look forward to中的to是介词，不是不定式符号！'},
        {'q': '"He used to live here" 的意思是', 'opts': ['A. 他过去住在这里', 'B. 他被用于住在这里', 'C. 他习惯住在这里', 'D. 他正住在这里'], 'ans': 0, 'exp': 'used to do = 过去常常（现在不这样了）。'},
        {'q': 'stop to do sth 和 stop doing sth 的区别是', 'opts': ['A. 意思相同', 'B. 前者是停下去做另一件事，后者是停下正在做的事', 'C. 前者是继续做，后者是停止做', 'D. 没有区别'], 'ans': 1, 'exp': 'stop to do sth（停下去做另一件事）vs stop doing sth（停下正在做的事）。'},
        {'q': '-ed结尾形容词和-ing结尾形容词的区别是', 'opts': ['A. 意思相同', 'B. -ed形容人的感受，-ing形容事物性质', 'C. -ed形容事物，-ing形容人', 'D. 都可以随意使用'], 'ans': 1, 'exp': '-ed形容人的感受（如I am bored），-ing形容事物性质（如The movie is boring）。'},
        {'q': '英语写作的核心思路是', 'opts': ['A. 直接列要点', 'B. 先抓人物→再抓背景→逻辑融合', 'C. 先写结尾', 'D. 只写开头'], 'ans': 1, 'exp': '写作核心思路：先抓人物→再抓背景→将人物和背景通过逻辑融合，不要干列要点。'},
        {'q': 'but 和 although', 'opts': ['A. 可以同时使用', 'B. 不能同时使用', 'C. 意思相反', 'D. 都是连词可以互换'], 'ans': 1, 'exp': 'but和although不能同时使用，这是英语中的常见错误。'},
        {'q': '日记写作的时态要求是', 'opts': ['A. 全用现在时', 'B. 整体一般过去时，习惯性动作/真理用一般现在时', 'C. 全用过去完成时', 'D. 全用现在完成时'], 'ans': 1, 'exp': '日记写作：整体一般过去时，但习惯性动作/客观真理/谚语名言用一般现在时。'},
        {'q': '反校园霸凌新规规定霸凌不包括以下哪类？', 'opts': ['A. 肢体欺凌', 'B. 辱骂欺凌', 'C. 孤立欺凌', 'D. 成绩歧视'], 'ans': 3, 'exp': '霸凌四类：肢体/辱骂/孤立/侮辱性绰号。成绩歧视不属于规定中的霸凌类型。'},
        {'q': '题文同序原则是指', 'opts': ['A. 题目顺序和文章顺序无关', 'B. 第二题找不到先做第三题，第一三题中间是第二题答案区间', 'C. 先做第一题', 'D. 所有答案都在最后一段'], 'ans': 1, 'exp': '题文同序：第二题找不到先做第三题，第一三题中间是第二题答案区间。'},
        {'q': '推断题的答题原则是', 'opts': ['A. 选和原文一模一样的', 'B. 基于原文引申，不选和原文一模一样的', 'C. 可以自由想象', 'D. 选最长选项'], 'ans': 1, 'exp': '推断题不选和原文一模一样的，基于原文引申。最忌无中生有。'},
    ],

    "flashcards": [
        {'front': '主旨题解题方法', 'back': '① 抓重复信息（原文+题干+选项）<br>② 看每段首句和全文开头结尾<br>③ 按文体判断（记叙/说明/议论）'},
        {'front': '细节题定位法', 'back': '优先抓大写人名地名、数字符号<br>题文同序原则<br>题干无法定位用选项定位'},
        {'front': '非谓语动词10组', 'back': 'look forward to doing<br>give up doing<br>mind doing<br>pay attention to doing<br>insist on doing'},
        {'front': '时态判断三规则', 'back': '四年前/去年/昨天→过去式<br>每天/每周→一般现在时<br>无特殊语境→一般现在时'},
        {'front': 'used to 辨析', 'back': 'used to do = 过去常常<br>be used to do = 被用于<br>be used to doing = 习惯于'},
        {'front': 'stop搭配', 'back': 'stop to do = 停下去做另一件事<br>stop doing = 停下正在做的事'},
        {'front': '作文万能结构', 'back': '开头主题句→中间事件支撑<br>→结尾收获意义<br>按时间顺序加顺序词'},
        {'front': '推断题原则', 'back': '不选和原文一模一样的<br>基于原文引申<br>最忌无中生有'},
    ],

    "errors": [
        {'title': '细节题和主旨题方法混淆 ❌', 'wrong': '细节题也用重复信息定位（和主旨题一样）。', 'right': '<span class="hl">细节题</span>优先抓大写地名数字等具体信息；<span class="hl">主旨题</span>才用重复信息。注意区分！'},
        {'title': 'look forward to 误当不定式 ❌', 'wrong': '在to后直接加动词原形。', 'right': 'look forward to中的to是<span class="hl">介词</span>，后接doing形式。类似还有pay attention to、insist on等。'},
        {'title': '推断题加入主观猜测 ❌', 'wrong': '推断题凭自己的想象编造文中没有的信息。', 'right': '推断题一定要基于原文<span class="hl">合理引申</span>，不能凭空想象或加入文中没有的信息。'},
        {'title': '时态不加判断直接用过去式 ❌', 'wrong': '所有语境都用过去式，忽略了习惯性动作或客观真理。', 'right': '先找<span class="hl">时间标志词</span>。没有明显过去时间标志且是常规行为→一般现在时。'},
        {'title': '作文内容干条列举无连接 ❌', 'wrong': '作文里直接1234列要点，没有逻辑连接词。', 'right': '要点之间用<span class="hl">逻辑连接词</span>（first/then/after that/finally）连接。先抓人和背景再融合。'},
    ],
}

# ---- Chinese ----
subjects['chinese_7grade_interactive'] = {
    "navbar_back": "index.html",
    "navbar_title": "语文 · 7年级课堂笔记",
    "hero_title": "语文 · 7年级课堂笔记 · 互动学习",
    "hero_desc": "若琳课堂笔记 · 知识点归类 | ⭐⭐⭐",
    "meta_quiz": "12道测验题",
    "meta_cards": "8张知识卡",
    "meta_errors": "5大易错点",
    "section_title": "第七年级 · 语文（字音字形+文言文古诗+现代文阅读+语言运用）",
    "teacher_talk_title": "教师寄语",
    "teacher_talk_p1": "语文期末复习涵盖了四大模块：基础知识（字音字形与病句辨析）、文言文与古诗赏析、现代文阅读答题方法（比喻修辞/插叙/环境描写/段落作用）、语言运用题型（概括/补句/仿写）。",
    "teacher_talk_p2": "⚠️ 古诗情感不能只答笼统（如仅写\u201c思乡\u201d不写如何思乡）；现代文阅读要分点作答标注序号！",
    "footer_text": "语文 · 7年级课堂笔记互动学习 | 若琳课堂笔记",
    "wrong_history_key": "quiz_chinese7_wrong",
    "import_subject": "语文",
    "import_chapter": "7年级",
    "import_tags": "语文,7年级",
    "local_storage_key": "chinese7_errors_check",

    "knowledge_cards": [
        ("c1", "fa-font", "#667eea", "字音字形与病句", [
            "易错字词：恍惚、心急如焚、憋屈、心扉、执拗、由衷",
            "字形辨析：登录的\u201c录\u201d、竹竿的\u201c竿\u201d、黯淡、滂沱",
            "\u201c汇合\u201d（水流）vs \u201c会合\u201d（人群）",
            "病句类型：句式杂糅、偷换主语、语义重复、否定不当",
            "逻辑顺序：先培育→再建设→最后推广",
            "词语搭配：提高水平/质量/效率；发扬精神/传统/优点",
        ]),
        ("c2", "fa-scroll", "#e67e22", "文言文与古诗", [
            "《陋室铭》《爱莲说》：\u201c名\u201d=出名，\u201c馨\u201d=香气美好",
            "《城南》：对比手法，朴素无华的事物生命力更顽强",
            "化虚为实：\u201c只恐双溪舴艋舟，载不动许多愁\u201d",
            "《桂源铺》：溪水冲破万山阻拦→困难无法阻挡前进",
            "《水口行舟》：困境是暂时的，美好本质不会被磨灭",
            "文言虚词\u201c之\u201d：可表\u201c靠近\u201d；\u201c为\u201d作\u201c做/作为\u201d",
            "\u201c涕\u201d古义：眼泪（三点水）",
        ]),
        ("c3", "fa-book", "#2ecc71", "现代文阅读方法", [
            "比喻修辞答题：本体+喻体→写出特点→表达情感",
            "插叙作用：概括内容→分析对人物/主旨作用→结构作用",
            "环境描写：修辞+多感官→写出环境特征",
            "段落作用：内容（总结全文、点明主题）→结构（承上启下）",
            "概括题三法：摘句法、要素法、问题法",
            "修辞赏析三步：点明修辞→内容分析→效果情感",
        ]),
        ("c4", "fa-comments", "#3498db", "语言运用题型", [
            "中考/期末3道小题：①概括 ②补句/排序 ③仿写",
            "补句方法：瞻前顾后，先定内容再定形式",
            "表格错误修改：从内容和形式两个维度判断",
            "仿写要求：对偶句式，保持字数大体一致",
        ]),
    ],

    "questions": [
        {'q': '\u201c汇合\u201d和\u201c会合\u201d的区别是', 'opts': ['A. 意思相同', 'B. \u201c汇合\u201d用于水流，\u201c会合\u201d用于人群', 'C. \u201c汇合\u201d用于人群', 'D. \u201c会合\u201d用于水流'], 'ans': 1, 'exp': '\u201c汇合\u201d（水流）vs \u201c会合\u201d（人群），注意区分。'},
        {'q': '下列哪个不是病句类型？', 'opts': ['A. 句式杂糅', 'B. 偷换主语', 'C. 词语重复', 'D. 并列短语'], 'ans': 3, 'exp': '病句类型包括：句式杂糅、偷换主语（中途易辙）、语义重复、否定不当、歧义、搭配不当。\u201c并列短语\u201d本身不是病句类型。'},
        {'q': '比喻修辞答题的完整步骤是', 'opts': ['A. 只写比喻二字', 'B. 本体+喻体→写出特点→表达情感', 'C. 只分析内容', 'D. 只写情感'], 'ans': 1, 'exp': '比喻修辞答题：本体+喻体→写出特点→表达情感（4分以内不答结构作用）。'},
        {'q': '插叙的作用题应该从哪些角度回答？', 'opts': ['A. 只写内容', 'B. 只写结构', 'C. 概括内容→分析对人物/主旨作用→对文章结构作用', 'D. 只写情感'], 'ans': 2, 'exp': '插叙作用题：概括插叙内容→分析对人物/主旨的作用→对文章结构和情感铺垫的作用。'},
        {'q': '《爱莲说》的文体是', 'opts': ['A. 骈文', 'B. 议论文', 'C. 记叙文', 'D. 说明文'], 'ans': 1, 'exp': '《爱莲说》是议论文，《陋室铭》是不标准骈文。'},
        {'q': '\u201c只恐双溪舴艋舟，载不动许多愁\u201d使用了什么诗歌技巧？', 'opts': ['A. 比喻', 'B. 化虚为实', 'C. 拟人', 'D. 夸张'], 'ans': 1, 'exp': '将无形的\u201c愁\u201d转化为有重量的实物——化虚为实（诗歌技巧）。'},
        {'q': '环境描写的作用题应首先分析', 'opts': ['A. 只写环境特点', 'B. 修辞手法+多感官描写→写出环境特征', 'C. 只写人物情感', 'D. 只写结构作用'], 'ans': 1, 'exp': '环境描写作用：修辞手法（比喻拟人）+多感官描写→写出环境特征。'},
        {'q': '概括题三种方法是', 'opts': ['A. 摘抄法', 'B. 摘句法、要素法、问题法', 'C. 总结法', 'D. 分析法'], 'ans': 1, 'exp': '概括题三种方法：摘句法（摘关键句）、要素法（时间地点人物事件）、问题法（围绕题干提炼）。'},
        {'q': '\u201c沮丧\u201d的正确写法是', 'opts': ['A. 沮sang', 'B. 沮丧', 'C. 沮伤', 'D. 疽丧'], 'ans': 1, 'exp': '沮丧的\u201c丧\u201d是\u201c丧失\u201d的\u201c丧\u201d，不要写成\u201c伤\u201d。'},
        {'q': '补句题的方法是', 'opts': ['A. 随意填写', 'B. 瞻前顾后，先定内容再定形式', 'C. 只考虑句式', 'D. 只考虑内容'], 'ans': 1, 'exp': '补句方法：瞻前顾后，先定内容再定形式。既要看前文也要看后文。'},
        {'q': '仿写的要求是', 'opts': ['A. 完全照抄', 'B. 对偶句式，保持字数大体一致', 'C. 字数必须完全一样', 'D. 只保持句式'], 'ans': 1, 'exp': '仿写要求：对偶句式，保持字数大体一致。'},
        {'q': '古诗《水口行舟》的主旨是', 'opts': ['A. 写景', 'B. 困境是暂时的，美好本质不会被磨灭', 'C. 思乡', 'D. 怀古'], 'ans': 1, 'exp': '《水口行舟》：夜晚风浪紧张→清晨风景依旧→困境是暂时的，美好本质不会被磨灭。'},
    ],

    "flashcards": [
        {'front': '比喻修辞答题公式', 'back': '本体+喻体→写出特点→表达情感<br>4分以内不答结构作用'},
        {'front': '插叙作用三层次', 'back': '① 概括插叙内容<br>② 分析对人物/主旨作用<br>③ 分析对文章结构作用'},
        {'front': '概括题三法', 'back': '摘句法（摘关键句）<br>要素法（时间、地点、人物、事件）<br>问题法（围绕题干提炼）'},
        {'front': '修辞赏析三步', 'back': '① 点明修辞<br>② 内容分析<br>③ 效果情感'},
        {'front': '化虚为实', 'back': '将抽象的情感/思绪转化为<br>有重量、可触摸的实物<br>如\u201c载不动许多愁\u201d'},
        {'front': '病句六大类型', 'back': '句式杂糅 / 偷换主语<br>语义重复 / 否定不当<br>歧义 / 搭配不当'},
        {'front': '古诗赏析要点', 'back': '不答笼统情感<br>要结合具体诗句分析<br>手法+内容+情感'},
        {'front': '词语搭配库', 'back': '提高水平/质量/效率<br>发扬精神/传统/优点<br>发挥作用/优势/潜能<br>开展活动/工作/竞赛'},
    ],

    "errors": [
        {'title': '古诗情感答得笼统 ❌', 'wrong': '只写\u201c思乡\u201d\u201c忧国\u201d等笼统情感，不结合具体诗句。', 'right': '古诗情感不能只答笼统，必须<span class="hl">结合内容</span>分析如何体现该情感（如通过什么意象、什么手法）。'},
        {'title': '病句判断只看一面 ❌', 'wrong': '只从内容或只从形式判断是否病句。', 'right': '病句判断需从<span class="hl">多个角度</span>分析：搭配、成分、逻辑、语序等。尤其注意\u201c否定不当\u201d和\u201c语义重复\u201d。'},
        {'title': '阅读不标注序号 ❌', 'wrong': '答题没有分点，一大段文字堆在一起。', 'right': '现代文阅读要<span class="hl">分点作答</span>，标注① ② ③序号。先总后分，条理清晰。'},
        {'title': '字形写错 ❌', 'wrong': '\u201c汇合\u201d和\u201c会合\u201d混用；\u201c黯淡\u201d写成\u201c暗淡\u201d。', 'right': '注意字词辨析：<span class="hl">\u201c汇合\u201d</span>用于水流，<span class="hl">\u201c会合\u201d</span>用于人群。多记多背易错字词。'},
        {'title': '补句忽略形式 ❌', 'wrong': '只考虑内容是否连贯，忽略了句式结构的一致性。', 'right': '补句要<span class="hl">瞻前顾后</span>：先定内容（是否连贯），再定形式（句式结构是否与前后一致）。'},
    ],
}

# ---- Geography ----
subjects['geography_7grade_interactive'] = {
    "navbar_back": "index.html",
    "navbar_title": "地理 · 7年级课堂笔记",
    "hero_title": "地理 · 7年级课堂笔记 · 互动学习",
    "hero_desc": "若琳课堂笔记 · 知识点归类 | ⭐⭐⭐",
    "meta_quiz": "10道测验题",
    "meta_cards": "8张知识卡",
    "meta_errors": "4大易错点",
    "section_title": "第七年级 · 地理（巴西地理+美国地理）",
    "teacher_talk_title": "教师寄语",
    "teacher_talk_p1": "地理复习涵盖了两大国家地理：巴西（位置、地形气候、农业工业、亚马孙河、雨林生态）和美国（黑土、农业专业化分区、三大工业区、人口移民）。",
    "teacher_talk_p2": "⚠️ 南美洲东西临海方向不要混淆；亚马孙河航运价值与自然条件要区分理解！",
    "footer_text": "地理 · 7年级课堂笔记互动学习 | 若琳课堂笔记",
    "wrong_history_key": "quiz_geography7_wrong",
    "import_subject": "地理",
    "import_chapter": "7年级",
    "import_tags": "地理,7年级",
    "local_storage_key": "geography7_errors_check",

    "knowledge_cards": [
        ("c1", "fa-globe-americas", "#667eea", "巴西地理", [
            "位置：主要在南半球，赤道穿过北部；东临大西洋",
            "领土：南美洲面积最大、人口最多；人口分布在东部沿海",
            "地形气候：北部亚马孙平原（热带雨林），南部巴西高原（热带草原），南高北低",
            "农业：大豆/咖啡/橙子/牛肉出口世界前列",
            "工业：钢铁/汽车/造船/石油化工/航空制造",
            "能源特色：甘蔗生产乙醇添加汽油缓解能源短缺",
            "亚马孙河：流量大、支流多、无结冰期",
            "雨林：全球最大热带雨林，土壤贫瘠（养分在植物体内）",
            "迁都：巴西利亚（新首都），原首都里约热内卢，最大城市圣保罗",
            "人口特征：2/5混血种人，以白种人和混血种人为主",
        ]),
        ("c2", "fa-flag-usa", "#e67e22", "美国地理", [
            "黑土：中央大平原，世界三大黑土分布区之一",
            "农业专业化分区：小麦区/玉米带/乳畜带等",
            "两个小麦区被玉米带隔开（纬度差异→春小麦vs冬小麦）",
            "三大工业区：东北部老工业基地、南部休斯敦（航空航天）、西部硅谷",
            "人口特征：自然增长率低（1.5‰），总增长率4.5‰（主要来自移民）",
            "移民来源：墨西哥（24%）→印度→中国（520万华人华侨）",
            "地形：南北纵列，西部山地→中部平原→东部山地",
            "水文：密西西比河（世界第四长河）；五大湖（最大淡水湖群）",
        ]),
    ],

    "questions": [
        {'q': '巴西的地形特点是什么？', 'opts': ['A. 北低南高', 'B. 南高北低', 'C. 东西高中部低', 'D. 中部高四周低'], 'ans': 1, 'exp': '巴西地形南高北低：南部巴西高原（海拔较高），北部亚马孙平原（地势低平）。'},
        {'q': '巴西的能源特色是什么？', 'opts': ['A. 大量进口石油', 'B. 甘蔗生产乙醇添加汽油', 'C. 全部靠水电', 'D. 使用核能'], 'ans': 1, 'exp': '巴西用甘蔗生产乙醇添加汽油来缓解能源短缺，这是其能源特色。'},
        {'q': '亚马孙河航运价值低的原因是', 'opts': ['A. 水流太急', 'B. 结冰期长', 'C. 流域人口少需求低', 'D. 河道太窄'], 'ans': 2, 'exp': '亚马孙河自然航运条件优越（流量大、支流多、无结冰期），但实际价值低——流域内人口少、经济需求低。'},
        {'q': '亚马孙热带雨林土壤贫瘠的原因是', 'opts': ['A. 温度太高', 'B. 降水太少', 'C. 养分在植物体内', 'D. 岩石风化不充分'], 'ans': 2, 'exp': '亚马孙雨林土壤贫瘠，因为养分主要储存在植物体内（植物快速吸收），而非土壤中。'},
        {'q': '巴西迁都后的新首都是', 'opts': ['A. 里约热内卢', 'B. 圣保罗', 'C. 巴西利亚', 'D. 萨尔瓦多'], 'ans': 2, 'exp': '巴西迁都到巴西利亚（新首都），原首都里约热内卢，最大城市圣保罗。'},
        {'q': '美国中央大平原的黑土属于世界第几大黑土分布区？', 'opts': ['A. 第一大', 'B. 第二大', 'C. 第三大', 'D. 第四大'], 'ans': 2, 'exp': '美国中央大平原是世界三大黑土分布区之一。'},
        {'q': '美国两个小麦区被什么作物带隔开？', 'opts': ['A. 乳畜带', 'B. 玉米带', 'C. 棉花带', 'D. 水果带'], 'ans': 1, 'exp': '两个小麦区被玉米带隔开。纬度差异导致北部种春小麦、南部种冬小麦。'},
        {'q': '美国最大的高新技术产业中心位于', 'opts': ['A. 底特律', 'B. 休斯敦', 'C. 硅谷', 'D. 纽约'], 'ans': 2, 'exp': '西部硅谷是全球最大高新技术产业中心。东北部底特律是汽车城，南部休斯敦是航空航天中心。'},
        {'q': '美国人口总增长率（4.5‰）比自然增长率（1.5‰）高，主要原因是', 'opts': ['A. 出生率高', 'B. 死亡率低', 'C. 移民', 'D. 寿命延长'], 'ans': 2, 'exp': '美国人口自然增长率低（1.5‰），总增长率4.5‰——差额主要来自移民。'},
        {'q': '美国五大湖中全部属于美国的是', 'opts': ['A. 苏必利尔湖', 'B. 密歇根湖', 'C. 休伦湖', 'D. 伊利湖'], 'ans': 1, 'exp': '密歇根湖全部属于美国，其余为美加共有。'},
    ],

    "flashcards": [
        {'front': '巴西地形气候', 'back': '北部：亚马孙平原（热带雨林气候）<br>南部：巴西高原（热带草原气候）<br>南高北低'},
        {'front': '亚马孙河特点', 'back': '<strong>自然</strong>条件优越：流量大、支流多、无结冰期<br>航运<strong>价值</strong>低：人口少、需求低'},
        {'front': '雨林土壤特点', 'back': '土壤贫瘠——<br>养分在<span class="hl">植物体内</span>而非土壤中'},
        {'front': '巴西迁都', 'back': '最大城市：圣保罗<br>原首都：里约热内卢<br>新首都：<span class="hl">巴西利亚</span>'},
        {'front': '美国三大工业区', 'back': '东北部：老工业基地（底特律汽车城）<br>南部休斯敦：航空航天<br>西部硅谷：高新技术产业中心'},
        {'front': '美国小麦区分布', 'back': '两个小麦区被<span class="hl">玉米带</span>隔开<br>北部→春小麦<br>南部→冬小麦'},
        {'front': '美国移民来源', 'back': '墨西哥（24%）家庭团聚/农业劳工<br>印度→技术移民<br>中国→520万华人华侨'},
        {'front': '密西西比河与五大湖', 'back': '密西西比河：世界第四长河<br>自北向南注入墨西哥湾<br>五大湖：最大淡水湖群<br>密歇根湖全属美国'},
    ],

    "errors": [
        {'title': '南美洲东西临海方向混淆 ❌', 'wrong': '巴西东临太平洋/西临大西洋方向搞反。', 'right': '巴西<span class="hl">东临大西洋</span>（东边是大西洋）。南美洲西临太平洋、东临大西洋。'},
        {'title': '亚马孙河航运价值与自然条件区分 ❌', 'wrong': '认为亚马孙河自然条件不好所以航运价值低。', 'right': '亚马孙河<span class="hl">自然条件优越</span>（流量大、支流多、无结冰期），但<span class="hl">航运价值低</span>是因为流域人口少、经济需求低。两者不矛盾！'},
        {'title': '小麦区南北差异原因混淆 ❌', 'wrong': '以为南北小麦区品种不同是因为土壤不同。', 'right': '南北小麦区品种差异是因为<span class="hl">纬度差异</span>导致的气候不同（北部→春小麦，南部→冬小麦）。'},
        {'title': '五大湖归属混淆 ❌', 'wrong': '以为五大湖全部是美加共有。', 'right': '<span class="hl">密歇根湖</span>全部属于美国，其余为美加共有。'},
    ],
}

# ---- Physics ----
subjects['physics_7grade_interactive'] = {
    "navbar_back": "index.html",
    "navbar_title": "物理 · 7年级课堂笔记",
    "hero_title": "物理 · 7年级课堂笔记 · 互动学习",
    "hero_desc": "若琳课堂笔记 · 知识点归类 | ⭐⭐⭐",
    "meta_quiz": "10道测验题",
    "meta_cards": "6张知识卡",
    "meta_errors": "4大易错点",
    "section_title": "第七年级 · 物理（长度测量+机械运动+参照物）",
    "teacher_talk_title": "教师寄语",
    "teacher_talk_p1": "物理新课程涵盖了两大模块：长度测量（刻度尺使用、误差分析、特殊测量）和机械运动（参照物选择、相对运动分析、风向判断）。",
    "teacher_talk_p2": "⚠️ 读数末尾的0不能省略！分度值必须带数字和单位。风向一定要画图标注箭头！",
    "footer_text": "物理 · 7年级课堂笔记互动学习 | 若琳课堂笔记",
    "wrong_history_key": "quiz_physics7_wrong",
    "import_subject": "物理",
    "import_chapter": "7年级",
    "import_tags": "物理,7年级",
    "local_storage_key": "physics7_errors_check",

    "knowledge_cards": [
        ("c1", "fa-ruler", "#667eea", "长度测量与误差", [
            "刻度尺使用：先看分度值；读数估读到分度值下一位",
            "读数 = 准确值 + 估读值（末尾的0不能省略！如7.40cm）",
            "分度值反推：最后一位是估读位→前一位是分度值对应位置→加单位",
            "误差定义：操作正确前提下，测量值与真实值之差（顺序不能颠倒）",
            "误差分类：偶然误差（多次测量求平均）；系统误差（换工具/优化方法）",
            "求平均规则：先剔除异常数据→结果四舍五入保留原小数位数",
            "特殊测量：比例法、化曲为直法、滚动法、累积法",
        ]),
        ("c2", "fa-car", "#e67e22", "机械运动与参照物", [
            "机械运动定义：一个物体相对于另一个物体空间位置改变",
            "非机械运动：分子扩散、植物生长、物态变化不属于",
            "参照物：研究物体运动时选作标准的物体（默认假定静止）",
            "运动绝对性：宇宙中所有物体都在运动；静止是相对的",
            "相对静止应用：接力赛交接棒、空中加油、地球同步卫星",
            "风向判断：东风=从东边吹来的风；必须画图标注箭头",
        ]),
    ],

    "questions": [
        {'q': '刻度尺读数时，需要估读到', 'opts': ['A. 分度值', 'B. 分度值下一位', 'C. 分度值上一位', 'D. 毫米'], 'ans': 1, 'exp': '估读到分度值的下一位，如分度值1mm，读数到0.1mm（0.01cm）。'},
        {'q': '读数7.40cm中，估读值是', 'opts': ['A. 7cm', 'B. 0.4cm', 'C. 0.00cm', 'D. 没有估读'], 'ans': 2, 'exp': '7.40cm中，分度值是0.1cm（1mm），估读值是0.00cm。末尾的0不能省略！'},
        {'q': '误差和错误的区别正确的是', 'opts': ['A. 误差可以避免', 'B. 错误不可避免', 'C. 误差不可避免', 'D. 两者都不可避免'], 'ans': 2, 'exp': '误差不可避免（只能减小），错误可以避免（规范操作即可）。'},
        {'q': '减小偶然误差的方法是', 'opts': ['A. 换更精准的仪器', 'B. 多次测量取平均值', 'C. 不估读', 'D. 不作图'], 'ans': 1, 'exp': '偶然误差通过多次测量取平均值来减小。系统误差通过换更精准工具或优化方法来减小。'},
        {'q': '累积法测一张纸的厚度，应先测量', 'opts': ['A. 一张纸的厚度', 'B. 多张纸的厚度再除以张数', 'C. 书的页数', 'D. 书的宽度'], 'ans': 1, 'exp': '累积法测多张纸（如50张）的总厚度，再除以张数得到每张纸厚度。注意页数÷2=张数。'},
        {'q': '下列哪个不属于机械运动？', 'opts': ['A. 汽车行驶', 'B. 分子扩散', 'C. 飞机飞行', 'D. 地球自转'], 'ans': 1, 'exp': '分子扩散、植物生长、物态变化不属于机械运动。'},
        {'q': '东风是指风从哪个方向吹来？', 'opts': ['A. 从东边吹来', 'B. 吹向东边', 'C. 从南边吹来', 'D. 从西边吹来'], 'ans': 0, 'exp': '东风=从东边吹来的风。必须画图标注箭头来辅助判断。'},
        {'q': '接力赛交接棒时，交接棒运动员之间是', 'opts': ['A. 相对运动', 'B. 相对静止', 'C. 绝对静止', 'D. 没有关系'], 'ans': 1, 'exp': '接力赛交接棒时，交接棒运动员保持相对静止（同速同向运动）才能顺利交接。'},
        {'q': '刻度尺被拉伸后测量结果会', 'opts': ['A. 偏大', 'B. 偏小', 'C. 不变', 'D. 不一定'], 'ans': 1, 'exp': '刻度尺拉伸后，实际1cm变长了但刻度没变，所以读数会比实际值偏小。'},
        {'q': '物体的运动是绝对的还是相对的？', 'opts': ['A. 运动是绝对的，静止是相对的', 'B. 运动和静止都是绝对的', 'C. 运动是相对的，静止是绝对的', 'D. 运动和静止都是相对的'], 'ans': 0, 'exp': '宇宙中所有物体都在运动（运动是绝对的），静止是相对的。'},
    ],

    "flashcards": [
        {'front': '刻度尺五字口诀', 'back': '<span class="hl">选→放→看→读→记</span><br>估读到分度值的下一位'},
        {'front': '测量值公式', 'back': '测量值 = <span class="hl">准确值</span> + <span class="hl">估读值</span> + 单位'},
        {'front': '误差与错误', 'back': '误差：不可避免，可减小（取平均/换工具）<br>错误：可以避免（规范操作）'},
        {'front': '分度值反推', 'back': '最后一位是估读位<br>→前一位是分度值对应位置<br>→加单位'},
        {'front': '机械运动vs非机械运动', 'back': '机械运动：相对位置改变<br>非机械运动：分子扩散、植物生长、物态变化'},
        {'front': '风向判断', 'back': '东风 = 从东边吹来的风<br>🚩 务必画图标注箭头！'},
    ],

    "errors": [
        {'title': '读数末尾0省略 ❌', 'wrong': '读7.40cm写成7.4cm，省略了末尾的0。', 'right': '读数末尾的0不能省略！7.40cm表示分度值是0.1cm（1mm），估读到0.01cm。'},
        {'title': '分度值不带单位 ❌', 'wrong': '写\u201c分度值是1\u201d或\u201c分度值是0.1\u201d，不写单位。', 'right': '分度值必须<span class="hl">带数字和单位</span>，如\u201c分度值是0.1cm\u201d或\u201c1mm\u201d。'},
        {'title': '风向方向搞反 ❌', 'wrong': '认为\u201c东风\u201d是往东吹的风。', 'right': '<span class="hl">东风=从东边吹来的风</span>。一定要画图标注箭头——箭头指向表示风吹方向。'},
        {'title': '运动分析不做图 ❌', 'wrong': '相对运动分析空想不做图，导致判断错误。', 'right': '相对运动分析要<span class="hl">画图</span>标注物体位置和运动方向。'},
    ],
}

# ---- Biology ----
subjects['biology_7grade_interactive'] = {
    "navbar_back": "index.html",
    "navbar_title": "生物 · 7年级课堂笔记",
    "hero_title": "生物 · 7年级课堂笔记 · 互动学习",
    "hero_desc": "若琳课堂笔记 · 知识点归类 | ⭐⭐⭐",
    "meta_quiz": "6道测验题",
    "meta_cards": "4张知识卡",
    "meta_errors": "3大易错点",
    "section_title": "第七年级 · 生物（会考复习要点）",
    "teacher_talk_title": "教师寄语",
    "teacher_talk_p1": "生物会考复习要点：会考要求80分以上为满分，当地80%中考生能拿满分。班级平均分57分（年级平均72分），30名学生未及格。",
    "teacher_talk_p2": "⚠️ 每天有生物课反而不重视，其他班每周一节反而听得更认真。要端正学习态度！",
    "footer_text": "生物 · 7年级课堂笔记互动学习 | 若琳课堂笔记",
    "wrong_history_key": "quiz_biology7_wrong",
    "import_subject": "生物",
    "import_chapter": "7年级",
    "import_tags": "生物,7年级",
    "local_storage_key": "biology7_errors_check",

    "knowledge_cards": [
        ("c1", "fa-leaf", "#667eea", "会考须知", [
            "会考要求80分以上为满分",
            "当地80%中考生能拿满分",
            "罚抄措施：20分抄4遍，30分抄3遍，40分抄2遍，50分抄1遍",
        ]),
        ("c2", "fa-chart-simple", "#e67e22", "考情分析", [
            "班级平均分57分（年级平均72分）",
            "30名学生未及格",
            "成绩差原因：每天有生物课反而不重视",
            "其他班每周一节生物课反而听得更认真",
        ]),
    ],

    "questions": [
        {'q': '生物会考满分要求的最低分数是', 'opts': ['A. 60分', 'B. 70分', 'C. 80分', 'D. 90分'], 'ans': 2, 'exp': '会考要求80分以上为满分，当地80%中考生能拿满分。'},
        {'q': '班级平均分是多少？', 'opts': ['A. 57分', 'B. 72分', 'C. 80分', 'D. 65分'], 'ans': 0, 'exp': '班级平均分57分，年级平均72分。班级低于年级平均。'},
        {'q': '班级有多少名学生未及格？', 'opts': ['A. 10名', 'B. 20名', 'C. 30名', 'D. 40名'], 'ans': 2, 'exp': '班级共有30名学生未及格。'},
        {'q': '班级成绩差的主要原因是', 'opts': ['A. 太难了', 'B. 老师教得不好', 'C. 每天有生物课反而不重视', 'D. 没有复习资料'], 'ans': 2, 'exp': '成绩差原因：每天有生物课反而不重视，其他班每周一节反而听得更认真。'},
        {'q': '50分的同学需要罚抄几遍？', 'opts': ['A. 4遍', 'B. 3遍', 'C. 2遍', 'D. 1遍'], 'ans': 3, 'exp': '罚抄措施：20分抄4遍，30分抄3遍，40分抄2遍，50分抄1遍。'},
        {'q': '以下哪个不是提高生物成绩的有效方法？', 'opts': ['A. 认真听讲', 'B. 重视每一节生物课', 'C. 觉得不重要所以不听', 'D. 做好笔记和复习'], 'ans': 2, 'exp': '觉得不重要所以不听是导致成绩差的原因。要提高成绩，必须认真听讲、重视每一节课。'},
    ],

    "flashcards": [
        {'front': '会考满分要求', 'back': '80分以上为满分<br>当地80%中考生能拿满分'},
        {'front': '班级考情', 'back': '班级平均分：57分<br>年级平均分：72分<br>未及格人数：30人'},
        {'front': '成绩差原因', 'back': '每天有生物课反而不重视<br>其他班每周一节反而听得更认真'},
        {'front': '罚抄措施', 'back': '20分→4遍<br>30分→3遍<br>40分→2遍<br>50分→1遍'},
    ],

    "errors": [
        {'title': '轻视生物课 ❌', 'wrong': '因为每天都有生物课，觉得不重要所以不认真听。', 'right': '科目重要性与课时多少无关。其他班每周一节反而更认真。要<span class="hl">重视每一节课</span>。'},
        {'title': '不重视会考难度 ❌', 'wrong': '认为会考很简单，随便考考就能过。', 'right': '虽然80%中考生能拿满分，但仍需认真复习。班级30人未及格说明<span class="hl">不可掉以轻心</span>。'},
        {'title': '懒于复习和总结 ❌', 'wrong': '上课听了但课后不复习、不总结知识点。', 'right': '课后要及时复习总结、做练习。会考虽然不难但<span class="hl">覆盖面广</span>，需要系统复习。'},
    ],
}

# ============================================================
# GENERATION ENGINE
# ============================================================

def generate_page(name, cfg):
    """Generate a full HTML page for one subject."""
    tmpl = read_template()
    
    # --- Knowledge cards ---
    khtml = build_knowledge_html(cfg['knowledge_cards'])
    
    # --- Questions JS ---
    qjs = build_questions_js(cfg['questions'])
    
    # --- Flashcards JS ---
    fjs = build_flashcards_js(cfg['flashcards'])
    
    # --- Errors JS ---
    ejs = build_errors_js(cfg['errors'])
    
    n_q = len(cfg['questions'])
    n_f = len(cfg['flashcards'])
    n_e = len(cfg['errors'])
    
    # Build replacement map
    replacements = {
        # Hero / title
        '📐 物理 · 测量与声学 · 互动学习': cfg['hero_title'],
        '<title>📐 物理 · 测量与声学 · 互动学习</title>': f"<title>{cfg['hero_title']}</title>",
        
        # Navbar
        "物理 · 测量与声学": cfg['navbar_title'],
        'href="index.html"><i class="fas fa-arrow-left" style="font-size:.85rem;opacity:.8"></i> 物理 · 测量与声学': 
            f'href="{cfg["navbar_back"]}"><i class="fas fa-arrow-left" style="font-size:.85rem;opacity:.8"></i> {cfg["navbar_title"]}',
        
        # Hero
        '<i class="fas fa-calculator"></i> 物理 · 测量与声学 · 互动学习': f'<i class="fas fa-graduation-cap"></i> {cfg["hero_title"]}',
        '物理 · 测量与声学 · 互动学习': cfg['hero_title'],
        '初二暑假博学班 · 天元教育 | ⭐⭐⭐': cfg['hero_desc'],
        
        # Meta
        '30道测验题': cfg['meta_quiz'],
        '20张知识卡': cfg['meta_cards'],
        '6大易错点': cfg['meta_errors'],
        
        # Section title
        '第三讲 · 测量（声学计算+刻度尺+秒表）': cfg['section_title'],
        
        # Teacher talk
        '教师寄语': cfg['teacher_talk_title'],
        '声学计算和测量工具的使用是八上物理的两大基础。声学计算一定要掌握画图列式子的方法；秒表读数和刻度尺的使用是新的重点内容，其中单位换算的关系需要熟练掌握。': cfg['teacher_talk_p1'],
        '⚠️ 声学计算有三种题型：直接套公式、回声问题、和火车鸣笛问题。测量部分要注意估读和单位换算的幂次关系。做之前一定要复习！': cfg['teacher_talk_p2'],
        
        # Knowledge cards (replace the entire knowledge-grid section)
        # We need to find the knowledge-grid block and replace it
        # The block starts at line 140 and ends at 185 in the template
        # Actually, let me use the more precise approach - replace the inner content of the grid
        
        # Number of questions in progress display
        '0 / 30': f'0 / {n_q}',
        '0/30': f'0/{n_q}',
        
        # Flashcard count
        '共20张知识卡': f'共{n_f}张知识卡',
        '20张': f'{n_f}张',
        
        # Error items count
        '6大易错点已移除': f'{n_e}大易错点已移除',
        
        # Footer
        '数学 · 物理 · 测量与声学互动学习 | 天元教育 · 初二暑假博学班': cfg['footer_text'],
        
        # JS constants
        "const WRONG_HISTORY_KEY='quiz_lesson3_wrong'": f"const WRONG_HISTORY_KEY='{cfg['wrong_history_key']}'",
        
        # Import function
        "const item={subject:'物理',chapter:'测量（三）',content:q.q,correct_answer:q.opts[q.ans],my_answer:q.opts[myAns],error_reason:'概念不清',source:'练习',difficulty:3,tags:'测量,物理'}":
            f"const item={{subject:'{cfg['import_subject']}',chapter:'{cfg['import_chapter']}',content:q.q,correct_answer:q.opts[q.ans],my_answer:q.opts[myAns],error_reason:'概念不清',source:'练习',difficulty:3,tags:'{cfg['import_tags']}'}}",
        
        # Subject in importWB
        "subject:'物理',chapter:'测量（三）'": f"subject:'{cfg['import_subject']}',chapter:'{cfg['import_chapter']}'",
        "tags:'测量,物理'": f"tags:'{cfg['import_tags']}'",
        
        # Local storage key for error checklist
        "localStorage.getItem('physics_measure_check')": f"localStorage.getItem('{cfg['local_storage_key']}')",
        "localStorage.setItem('physics_measure_check'": f"localStorage.setItem('{cfg['local_storage_key']}'",
        "localStorage.removeItem('physics_measure_check'": f"localStorage.removeItem('{cfg['local_storage_key']}'",
    }
    
    result = tmpl
    
    # Apply replacements
    for old, new in replacements.items():
        if old in result:
            result = result.replace(old, new)
    
    # Now replace the knowledge-grid - find and replace the entire block
    # Find: the knowledge grid content between first knowledge-card div and the last one + closing div
    # Strategy: find the section between `knowledge-grid` opening and closing div using regex
    
    # The knowledge-grid starts with <div class="knowledge-grid"> and ends with </div>(closing the grid) followed by next card or section
    # Let me find what comes after the grid
    
    # Replace the questions array
    # Find the questions array in the template
    q_start = result.find('const questions=[\n')
    if q_start >= 0:
        q_end = result.find('];\n', q_start)
        # Find the '];' that ends the questions array
        # Need to find the right ]; - the one followed by newline and const
        rest = result[q_end+2:]
        # check if rest starts with \n\n
        nline = '\n\n'
        # Actually let me find the next const
        next_const = result.find('\nconst ', q_start + 20)
        if next_const >= 0:
            # The ]; before next const
            bracket_end = result.rfind('];', q_start, next_const)
            if bracket_end >= 0:
                q_end = bracket_end
    
    q_start = result.find('const questions=[\n')
    if q_start >= 0:
        # Find the matching ]; that ends this array (before next const)
        rest_after = result[q_start+17:]
        depth = 0
        end_pos = -1
        for i, ch in enumerate(rest_after):
            if ch == '[':
                depth += 1
            elif ch == ']':
                depth -= 1
                if depth == 0:
                    end_pos = q_start + 17 + i + 1
                    break
        
        if end_pos >= 0:
            result = result[:q_start] + f'const questions={qjs};' + result[end_pos:]
    
    # Replace flashcards array
    fc_start = result.find('const flashcards=[\n')
    if fc_start >= 0:
        rest_after = result[fc_start+18:]
        depth = 0
        end_pos = -1
        for i, ch in enumerate(rest_after):
            if ch == '[':
                depth += 1
            elif ch == ']':
                depth -= 1
                if depth == 0:
                    end_pos = fc_start + 18 + i + 1
                    break
        if end_pos >= 0:
            result = result[:fc_start] + f'const flashcards={fjs};' + result[end_pos:]
    
    # Replace errors array
    err_start = result.find('const errors=[\n')
    if err_start >= 0:
        rest_after = result[err_start+15:]
        depth = 0
        end_pos = -1
        for i, ch in enumerate(rest_after):
            if ch == '[':
                depth += 1
            elif ch == ']':
                depth -= 1
                if depth == 0:
                    end_pos = err_start + 15 + i + 1
                    break
        if end_pos >= 0:
            result = result[:err_start] + f'const errors={ejs};' + result[end_pos:]
    
    # Replace knowledge grid content
    kg_start = result.find('<div class="knowledge-grid">')
    if kg_start >= 0:
        # Find the closing of this grid div
        grid_content_start = kg_start + len('<div class="knowledge-grid">')
        # Find the matching </div> for the grid
        search_from = grid_content_start
        depth = 0
        end_div = -1
        for i in range(grid_content_start, len(result)):
            if result[i:i+6] == '<div c' or result[i:i+3] == '<di':
                # Check if this is an opening div
                if '<div ' in result[i:i+20] and '<div ' in result[i:i+20]:
                    # rough check
                    pass
            
            if result[i:i+6] == '<div c':
                depth += 1
            elif result[i:i+6] == '</div>':
                if depth == 0:
                    end_div = i + 6
                    break
                depth -= 1
        
        if end_div >= 0:
            new_grid = f'<div class="knowledge-grid">\n{khtml}\n</div>'
            result = result[:kg_start] + new_grid + result[end_div:]
    
    # Replace the "重点复习提示" card section - remove it since we have our own knowledge cards
    review_start = result.find('本讲重点复习提示')
    if review_start >= 0:
        # Find the enclosing card div
        # Go backwards to find <div class="card"> that starts this section
        card_start = result.rfind('<div class="card"', 0, review_start)
        if card_start >= 0:
            # Find the closing </div> for this card
            search_from = review_start
            depth = 0
            # Count from the card_start div
            card_div_end = result.find('</div>', search_from)
            # Find the right </div>
            inner = result[card_start:]
            depth = 0
            end_pos = -1
            for i, ch in enumerate(inner):
                if inner[i:i+5] == '<div ' or inner[i:i+5] == '<div ':
                    # count any opening div
                    if inner[i] == '<':
                        j = i
                        while j < len(inner) and inner[j] != '>':
                            j += 1
                        tag = inner[i+1:j].split()[0]
                        if tag == 'div':
                            depth += 1
                if inner[i:i+6] == '</div>':
                    depth -= 1
                    if depth == 0:
                        end_pos = card_start + i + 6
                        break
            
            if end_pos:
                result = result[:card_start] + result[end_pos:]
    
    return result


# ============================================================
# MAIN
# ============================================================

base_dir = '/home/administrator/xuci-jiancha'

for name, cfg in subjects.items():
    print(f"Generating {name}.html...")
    html = generate_page(name, cfg)
    filepath = f'{base_dir}/{name}.html'
    write_file(filepath, html)

print("\nDone! All 6 pages generated.")
