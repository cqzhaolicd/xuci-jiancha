#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""_build_math_lesson2.py — 数学第2讲 勾股定理复习进阶（博学班教案）
基座: math26q_lesson1_interactive.html
输出: math26q_lesson2_interactive.html
"""
import re, json, subprocess

REPO = '/home/administrator/xuci-jiancha'
BASE_F = f'{REPO}/math26q_lesson1_interactive.html'
OUT_F = f'{REPO}/math26q_lesson2_interactive.html'

KNOW = [
    ("c1", "📐 模块一：展开图求最短路径", [
        "方法：把立体图形表面<strong class=\"hl\">展开成平面</strong>，再用<strong class=\"hl\">勾股定理</strong>求两点间线段长",
        "长方体：最短路径按不同展开方式分别计算，取最小值",
        "长方体体对角线：√(a²+b²+c²)",
        "圆柱：展开后横向长为<strong class=\"hl\">半周长 πr</strong>（π取3 时 = 3r），纵向为高 h",
    ]),
    ("c2", "🍶 吸管类：范围问题", [
        "长方体 6×8×24、吸管 30cm：体对角线 = √(36+64+576) = <strong class=\"hl\">26</strong>",
        "插入最深 = 体对角线 26 → a<sub>min</sub> = 30−26 = <strong class=\"hl\">4</strong>",
        "插入最浅 = 高 24 → a<sub>max</sub> = 30−24 = <strong class=\"hl\">6</strong>",
        "所以 <strong class=\"hl\">4 ≤ a ≤ 6</strong>（圆杯类同理：√(高²+底面直径²)）",
    ]),
    ("c3", "🌳 绕树/绕柱：藤条与丝带", [
        "树高 14m、底面周长 4m、绕 7 圈 → 展开后底 = 4×7 = <strong class=\"hl\">28</strong>，高 14",
        "藤长 = √(28²+14²) = √980 = <strong class=\"hl\">14√5</strong>",
        "核心：<strong class=\"hl\">绕 n 圈 → 展开后横向长 = 周长 × n</strong>",
    ]),
    ("c4", "🧗 圆柱蚂蚁：两条路线比较", [
        "高 12、底面直径 6（r=3，π取3）：路线一 A→C→B = 12+6 = <strong class=\"hl\">18</strong>",
        "路线二（侧面展开）：√(12² + (πr)²) = √(144+81) = <strong class=\"hl\">15</strong>",
        "两路线相等：h + 2r = √(h²+9r²) → 4hr = 5r² → <strong class=\"hl\">h/r = 5/4</strong>",
    ]),
    ("c5", "🟦 模块二：勾股定理面积相关", [
        "直角边上正方形面积和 = 斜边上正方形面积（a²+b²=c² 的面积化）",
        "四边形 DAB=BCD=90°，S₁+S₄=35、S₃=9 → <strong class=\"hl\">S₂ = 26</strong>",
        "（对角线 BD 分成两个直角三角形：S₁+S₃ = S₂+S₄）",
        "三边为直径作半圆：<strong class=\"hl\">S₁ + S₂ = S₃</strong>（相似图形面积同规律）",
    ]),
    ("c6", "🌲 勾股树与生长类", [
        "边长 1 的正方形每次“生长”总面积 <strong class=\"hl\">+1</strong>",
        "生长 2025 次 → 所有正方形面积和 = <strong class=\"hl\">2026</strong>",
        "逐次作垂线：OP₁=√2，OP₂=√3，…，OP<sub>n</sub> = √(n+1) → OP₂₀₂₅ = <strong class=\"hl\">√2026</strong>",
    ]),
    ("c7", "🔢 完美勾股数与偶差勾股数", [
        "完美勾股数：a² + n² = (n+1)² → a² = 2n+1（a 必为<strong class=\"hl\">奇数</strong>）",
        "n<41：a² <83 → a = 3,5,7,9 → <strong class=\"hl\">4 组</strong>",
        "n<1013：a² <2027 → a 为奇数 3~45 → <strong class=\"hl\">22 组</strong>",
        "偶差勾股数组（c²−b²=2）：(6,8,10) m=24、(8,15,17)… m₁ = <strong class=\"hl\">24</strong>，m₁₈ = <strong class=\"hl\">840</strong>",
    ]),
    ("c8", "✏️ 模块三：设元求解", [
        "核心：设所求（或最短）线段为 <strong class=\"hl\">x</strong>，在不同直角三角形中<strong class=\"hl\">列勾股方程</strong>",
        "两笔筒 8cm、12cm，铅笔露出 4cm、2cm → 铅笔长 <strong class=\"hl\">23cm</strong>",
        "芦苇（池边长 10 尺、中央高出 1 尺）：设水深 x → x²+5² = (x+1)² → x=12 → 芦长 <strong class=\"hl\">13 尺</strong>",
        "折叠类：折叠前后<strong class=\"hl\">对应边相等</strong>（AB=AF、BE=EF）",
    ]),
    ("c9", "🔁 折叠与翻折：经典题型", [
        "长方形 AB=5、AD=3，沿 AE 折叠使 B 落在 CD 上 F：AF = AB = 5 → DF = 4、FC = 1",
        "设 BE = x，则 EF = x、EC = 3−x → x² = 1²+(3−x)² → x = <strong class=\"hl\">5/3</strong>",
        "关键：找到<strong class=\"hl\">含未知数的直角三角形</strong>列方程",
    ]),
    ("c10", "📊 模块四：B卷综合", [
        "数形结合：网格中构造三角形，用<strong class=\"hl\">两边之和 > 第三边</strong>比较无理数大小（√5+1 > √10）",
        "√(x²+…)+√((…−x)²+…) 型最小值 → 转化<strong class=\"hl\">两点间距离 + 将军饮马</strong>（对称 + 直线）",
        "圆柱吸管 25cm（直径 10、高 12）：a ∈ [<strong class=\"hl\">25−2√61, 13</strong>]",
    ]),
    ("c11", "📐 模块五：解三角形（可解性）", [
        "核心：<strong class=\"hl\">作高</strong>把斜三角形转化为直角三角形求解",
        "⚠️ 钝角三角形的高可能在<strong class=\"hl\">三角形外部</strong>（必须分类讨论）",
        "特殊角边比：30°→1:√3:2；45°→1:1:√2；60°→1:√3:2",
        "已知 AB=12、AC=10、BC 边高 6：BD=6√3、CD=8 → BC = <strong class=\"hl\">6√3+8 或 6√3−8</strong>",
    ]),
    ("c12", "⚠️ 本讲六大易错点", [
        "不区分斜边与直角边，盲目套公式（<strong class=\"hl\">最长边才可能是斜边</strong>）",
        "题目无图形时<strong class=\"hl\">遗漏多种情况</strong>，缺分类讨论",
        "混淆<strong class=\"hl\">勾股定理与逆定理</strong>：定理由直角得边，逆定理由边判定直角",
        "立体图形<strong class=\"hl\">展开方式选错</strong>，最值算错",
        "勾股树不会<strong class=\"hl\">转化面积关系</strong>",
        "解斜三角形作高时忽略<strong class=\"hl\">高在外部</strong>的钝角情形",
    ]),
]

QUIZ = [
    # 模块一 最短路径
    ("长方体水杯长宽高为 6、8、24，一根 30 的吸管（底端在杯底）放入，露在外面的长度为 a，则 a 的取值范围是",
     ["A. 4 ≤ a ≤ 6", "B. 6 ≤ a ≤ 8", "C. 4 ≤ a ≤ 8", "D. 2 ≤ a ≤ 6"], 0,
     "体对角线 = √(6²+8²+24²) = √676 = <strong>26</strong>；插入最深 26 → a=4，插入最浅（竖直）= 高 24 → a=6，故 <strong>4 ≤ a ≤ 6</strong>。"),
    ("长方体长宽高分别为 a、b、c，其体对角线长为",
     ["A. a+b+c", "B. √(a²+b²+c²)", "C. √(a²+b²)", "D. (a+b+c)/3"], 1,
     "体对角线 = <strong>√(a²+b²+c²)</strong>（两次勾股：先求底面对角线 √(a²+b²)，再与高 c 组合）。"),
    ("一棵树（看作圆柱）高 14m，底面周长 4m，一根藤从底部均匀绕树 7 圈，上端刚好与树顶齐平，则藤长为",
     ["A. 28m", "B. 10√5 m", "C. 14√5 m", "D. 14√2 m"], 2,
     "展开后横向长 = 4×7 = <strong>28</strong>，纵向 14 → 藤长 = √(28²+14²) = √980 = <strong>14√5</strong> m。"),
    ("圆柱高 12cm、底面直径 6cm，蚂蚁沿 A→C→B（C 在上底圆周）走侧面，路线一（先上后绕）路程为 18cm；若把侧面展开，路线二的最短路程是（π取3）",
     ["A. 12cm", "B. 15cm", "C. 18cm", "D. 21cm"], 1,
     "展开后横向 = πr = 3×3 = 9，纵向 = 高 12 → 路线二 = √(12²+9²) = √225 = <strong>15</strong> cm。"),
    ("上题中圆柱若半径为 r、高为 h，当两种爬行路线路程相等时，h/r =",
     ["A. 3/2", "B. 4/3", "C. 5/4", "D. 2/3"], 2,
     "路线一 = h+2r，路线二 = √(h²+9r²)；相等 → h²+4hr+4r² = h²+9r² → 4hr = 5r² → <strong>h/r = 5/4</strong>。"),
    ("求立体图形表面两点间最短路径的基本方法是",
     ["A. 直接量距离", "B. 把表面展开成平面，用勾股定理求线段长", "C. 用比例计算", "D. 用面积公式"], 1,
     "核心方法：<strong>展开成平面</strong> + <strong>勾股定理</strong>；注意不同展开方式结果不同，取最小值。"),
    ("圆柱高 8cm、底面周长 6cm，蚂蚁从下底一点沿侧面绕半圈爬到上底对应点，最短路程是",
     ["A. √73 cm", "B. 10 cm", "C. √82 cm", "D. 14 cm"], 0,
     "绕半圈 → 展开横向 = 6÷2 = 3，纵向 = 8 → √(3²+8²) = <strong>√73</strong> cm。"),
    ("棱长为 1 的正方体，一只蚂蚁沿表面从一个顶点爬到与它相对的另一个顶点（不在同一面），最短路程是",
     ["A. √3", "B. √5", "C. 2", "D. 1+√2"], 1,
     "把两个相邻面展开成 2×1 的矩形 → 最短路程 = √(2²+1²) = <strong>√5</strong>（体对角线 √3 只在“穿过内部”时成立）。"),
    # 模块二 面积
    ("四边形 ABCD 中，∠DAB = ∠BCD = 90°，分别以四边向外作正方形，面积依次为 S₁、S₂、S₃、S₄。若 S₁+S₄ = 35，S₃ = 9，则 S₂ =",
     ["A. 26", "B. 44", "C. 35", "D. 9"], 0,
     "对角线 BD 把四边形分成两个直角三角形：S₁+S₃ = S₂+S₄（都等于 BD²）→ S₂ = S₁+S₄−S₃ = 35−9 = <strong>26</strong>。"),
    ("Rt△ABC 中 ∠ACB = 90°，分别以三边为直径作三个半圆，图形中两直角边上半圆阴影面积之和与斜边上半圆面积的关系是",
     ["A. 两者之和 > 斜边半圆", "B. 两者之和 = 斜边半圆", "C. 两者之和 < 斜边半圆", "D. 无法确定"], 1,
     "半圆面积 = π/8 × 边长²，由 a²+b² = c² 得 <strong>S₁+S₂ = S₃</strong>（相似图形同规律）。"),
    ("边长 1 的正方形“生长”：每次在直角边外生出小正方形。生长 2025 次后，图形中所有正方形的面积和是",
     ["A. 2025", "B. 2026", "C. 2²⁰²⁵", "D. 4049"], 1,
     "每次生长使总面积增加初始正方形的面积 1 → 2025 次后 = 1+2025 = <strong>2026</strong>。"),
    ("OP₁=1，过 P₁ 作 P₁P₂⊥OP₁ 且 P₁P₂=1 得 OP₂=√2；再过 P₂ 作垂线且长度为 1 得 OP₃=√3；…依次作下去，OP₂₀₂₅ =",
     ["A. √2024", "B. √2025", "C. √2026", "D. 2026"], 2,
     "规律 OP<sub>n</sub> = √(n+1) → OP₂₀₂₅ = <strong>√2026</strong>。"),
    ("“完美勾股数”：正整数 a、n 满足 a² + n² = (n+1)²。当 n < 41 时共有多少组",
     ["A. 3 组", "B. 4 组", "C. 5 组", "D. 6 组"], 1,
     "a² = 2n+1，a 为奇数。n<41 → a² <83 → a = 3,5,7,9 → <strong>4 组</strong>。"),
    ("同上，当 n < 1013 时共有多少组“完美勾股数”",
     ["A. 20 组", "B. 21 组", "C. 22 组", "D. 23 组"], 2,
     "a² < 2027 → a 为不超过 45 的奇数：3,5,…,45 共 (45−3)/2+1 = <strong>22 组</strong>。"),
    ("直角三角形两条直角边为 3 和 4，则以斜边为边的正方形面积是",
     ["A. 7", "B. 12", "C. 25", "D. 49"], 2,
     "斜边 = √(3²+4²) = 5 → 正方形面积 = 5² = <strong>25</strong> = 3²+4²（面积转化）。"),
    # 模块三 设元
    ("两个粗细相同的圆柱形笔筒高分别为 8cm 和 12cm，同一支铅笔先后斜放入两个笔筒，露在外面的部分分别为 4cm 和 2cm，则铅笔长为",
     ["A. 20cm", "B. 22cm", "C. 23cm", "D. 25cm"], 2,
     "设笔筒底面直径为 d、笔长 L：L² = 8²+d²+? 由两式消去 d² 得 L = <strong>23cm</strong>（8²+d² = (L−4)²，12²+d² = (L−2)²，相减可解）。"),
    ("池塘底面是边长 10 尺的正方形，芦苇 AB 生在中央、高出水面 1 尺；把芦苇沿垂直池边方向拉向岸边，顶端恰好碰到岸边 B′，则芦苇长",
     ["A. 12 尺", "B. 13 尺", "C. 14 尺", "D. 15 尺"], 1,
     "设水深 x 尺，芦长 x+1；水平距离 = 5 尺 → x²+5² = (x+1)² → x = 12 → 芦长 <strong>13 尺</strong>。"),
    ("四边形 ABCD 中 ∠B = 90°，AB = 3，BC = 4，CD = 12，AD = 13，则四边形 ABCD 的面积是",
     ["A. 30", "B. 36", "C. 60", "D. 72"], 1,
     "AC = √(3²+4²) = 5；又 5²+12² = 13² → △ACD 为直角三角形 → 面积 = ½×3×4 + ½×5×12 = 6+30 = <strong>36</strong>。"),
    ("△ABC 中，AB = 12，AC = 10，BC 边上的高 AD = 6，则 BC 的长为",
     ["A. 6√3+8", "B. 6√3−8", "C. 6√3+8 或 6√3−8", "D. 8−6√3"], 2,
     "BD = √(12²−6²) = <strong>6√3</strong>，CD = √(10²−6²) = <strong>8</strong>；锐角/钝角两种情形 → BC = <strong>6√3+8 或 6√3−8</strong>（分类讨论）。"),
    ("长方形 ABCD 中 AB = 5、AD = 3，沿 AE 折叠使点 B 落在 CD 边上的点 F 处，则 BE 的长为",
     ["A. 3/2", "B. 5/3", "C. 2", "D. 4/3"], 1,
     "AF = AB = 5，AD = 3 → DF = 4、FC = 1；设 BE = x = EF，EC = 3−x → x² = 1²+(3−x)² → x = <strong>5/3</strong>。"),
    ("在折叠问题中，设未知数列勾股方程的关键依据是",
     ["A. 折叠前后对应边相等", "B. 面积相等", "C. 周长相等", "D. 角度和为 180°"], 0,
     "折叠的性质：<strong>对应边相等、对应角相等</strong>，据此把未知量集中到一个直角三角形中。"),
    ("设元求解类几何题的一般思路是",
     ["A. 直接测量", "B. 设所求线段为 x，在不同直角三角形中用勾股定理列方程", "C. 用面积法直接得答案", "D. 逐一试值"], 1,
     "核心思路：<strong>设元（常设最短/所求线段为 x）→ 在两个直角三角形中列勾股方程 → 解方程</strong>。"),
    # 模块四 B卷综合
    ("圆柱形水杯底面直径 10cm、高 12cm，一根 25cm 的吸管（底端在杯底）放入，露在外面的长度为 a，则 a 的取值范围是",
     ["A. 13 ≤ a ≤ 25", "B. 25−2√61 ≤ a ≤ 25", "C. 25−2√61 ≤ a ≤ 13", "D. 11 ≤ a ≤ 15"], 2,
     "竖直插入最浅 → a<sub>max</sub> = 25−12 = <strong>13</strong>；沿体对角线插入最深 = √(12²+10²) = 2√61 → a<sub>min</sub> = <strong>25−2√61</strong>。"),
    ("“偶差”勾股数组（a<b，a²+b²=c²，c²−b²=2），令 m = a+b+c，(6,8,10) 对应 m = 24。则 m₁ =",
     ["A. 12", "B. 24", "C. 30", "D. 40"], 1,
     "(6,8,10) 是最小偶差勾股数组 → m₁ = 6+8+10 = <strong>24</strong>。"),
    ("在正方形网格（每个小正方形边长 1）中构造△ABC，用“两边之和大于第三边”可比较 √5+1 与 √10 的大小，结论是",
     ["A. √5+1 > √10", "B. √5+1 < √10", "C. √5+1 = √10", "D. 无法比较"], 0,
     "构造 AB = √5、BC = 1、AC = √10 的三角形 → AB+BC > AC → <strong>√5+1 > √10</strong>。"),
    ("求形如 √(x²+9) + √((15−x)²+25) 的最小值时，可利用的数学思想方法是",
     ["A. 因式分解", "B. 数形结合（两点间距离 + 将军饮马）", "C. 反证法", "D. 换元后直接配方"], 1,
     "把两式看成平面内两段距离 → 用<strong>数形结合</strong>转化：对称点连线（将军饮马），最小值 = 两点间距离。"),
    ("勾股树图形中，若一个图形的所有正方形面积总和为 S，那么继续“生长”一次后（每个直角边外再生成一个正方形），总面积变化是",
     ["A. 不变", "B. 增加初始正方形的面积", "C. 变为 2S", "D. 增加 S"], 1,
     "每次生长新增的正方形面积和 = 被生长的正方形面积（a²+b²=c²）→ 总面积<strong>每次增加初始正方形的面积</strong>（边长 1 时为 1）。"),
    # 模块五 解三角形
    ("△ACB 和 △DCE 都是直角三角形，∠ACB = ∠DCE = 90°，CB = CD，∠B = 45°，延长 BA 交 DE 于 F，取 AB 中点 G，AG = AF = 2，则 △AEF 的面积为",
     ["A. 2", "B. 3", "C. 4", "D. 6"], 2,
     "由 AG = AF = 2 得 AB = 4；△DGB ≌ △EFA（ASA）→ S△AEF = S△DGB = ½×AB×AD 型 = <strong>4</strong>。"),
    ("等边三角形 ABC 中 AB = 2，等腰 Rt△ABD 中 ∠ABD = 90°，延长 AC、BD 交于点 R，连接 CD，则 CD =",
     ["A. √2", "B. √3", "C. √6−√2", "D. √6+√2"], 2,
     "以 A 为原点、AB 为 x 轴：B(2,0)、C(1,√3)、D(2,−2)（等腰直角）→ CD = √(1²+(2−√3)²) = √(8−4√3) = <strong>√6−√2</strong>。"),
    ("解斜三角形（非直角三角形）的常用方法是",
     ["A. 直接套勾股定理", "B. 作高转化为直角三角形", "C. 用面积公式直接算边", "D. 延长一边"], 1,
     "常用方法：<strong>作高</strong>构造直角三角形，再用勾股定理与特殊角边比求解。"),
    ("△ABC 中 AB = 13、AC = 15、BC = 14，则 △ABC 的面积为",
     ["A. 84", "B. 91", "C. 96", "D. 108"], 0,
     "作高 AD：设 BD = x → 13²−x² = 15²−(14−x)² → x = 5 → AD = 12 → 面积 = ½×14×12 = <strong>84</strong>。"),
    ("Rt△ABC 中 ∠C = 90°，∠ABC = 30°，AC = 3，则 AB 与 BC 分别为",
     ["A. 6 和 3√3", "B. 3√3 和 6", "C. 6 和 3", "D. 3 和 6"], 0,
     "30° 角所对直角边 = 斜边一半 → AB = 2×3 = <strong>6</strong>，BC = √(6²−3²) = <strong>3√3</strong>（边比 1:√3:2）。"),
    ("已知三角形两边及其中一边上的高，求第三边时，若题目未给图形，必须注意",
     ["A. 直接算一次即可", "B. 高可能在三角形外部（钝角三角形），需分类讨论", "C. 只能取正值", "D. 无需考虑"], 1,
     "⚠️ 无图时高可能在<strong>内部或外部</strong>（钝角情形）→ 两个解，必须<strong>分类讨论</strong>（如 AB=12、AC=10、高=6 → BC = 6√3±8）。"),
]

FLASH = [
    ("求立体图形表面最短路径的核心方法？",
     "<strong>展开成平面</strong> + <strong>勾股定理</strong>；不同展开方式结果不同，取最小值。"),
    ("长方体 6×8×24 中 30cm 吸管露出长度 a 的范围怎么求？",
     "体对角线 = √(6²+8²+24²) = <strong>26</strong> → a<sub>min</sub> = 30−26 = 4；竖直插入 a<sub>max</sub> = 30−24 = 6 → <strong>4 ≤ a ≤ 6</strong>。"),
    ("绕树 7 圈、周长 4m、高 14m 的藤长？",
     "展开横向 = 4×7 = 28 → 藤长 = √(28²+14²) = <strong>14√5</strong> m（绕 n 圈 → 横向 = 周长×n）。"),
    ("圆柱蚂蚁两条路线相等时 h/r 的推导？",
     "h+2r = √(h²+9r²)（π取3）→ 4hr+4r² = 9r² → 4h = 5r → <strong>h/r = 5/4</strong>。"),
    ("勾股定理的面积化结论？",
     "直角边上正方形（或相似图形）面积和 = 斜边上的对应面积（a²+b²=c²）。"),
    ("四边形两对角为 90°，S₁+S₄=35、S₃=9 求 S₂？",
     "对角线分两个直角三角形 → S₁+S₃ = S₂+S₄ → S₂ = <strong>26</strong>。"),
    ("勾股树生长 2025 次后总面积？",
     "每次生长总面积 +1（初始边长 1）→ <strong>2026</strong>。"),
    ("完美勾股数 a²+n²=(n+1)² 的两组计数？",
     "a² = 2n+1（a 为奇数）：n<41 → <strong>4 组</strong>（a=3,5,7,9）；n<1013 → <strong>22 组</strong>（a 为 ≤45 的奇数）。"),
    ("芦苇题（池边长 10 尺、高出 1 尺）怎么解？",
     "设水深 x，芦长 x+1；水平距离 5 尺 → x²+25 = (x+1)² → x = 12 → 芦长 <strong>13 尺</strong>。"),
    ("长方形 AB=5、AD=3 折叠求 BE 的步骤？",
     "AF=AB=5 → DF=4、FC=1；设 BE=x=EF、EC=3−x → x² = 1+(3−x)² → <strong>x = 5/3</strong>。"),
    ("解斜三角形的方法与易错点？",
     "<strong>作高</strong>转化为直角三角形；⚠️ 钝角三角形的高可能在<strong>外部</strong>，无图时必须<strong>分类讨论</strong>。"),
    ("本讲六大易错点速记？",
     "① 斜边判断（最长边）② 无图分类讨论 ③ 定理 vs 逆定理 ④ 展开方式选错 ⑤ 勾股树面积转化 ⑥ 高在外部情形。"),
]

ERRORS = [
    ("❌ 不判断斜边就套公式",
     "看到两边 3、4 就把第三边算成 5，即使第三边可能是直角边。",
     "先判断哪条是<strong>斜边（最长边）</strong>：若已知两边为直角边 → c = √(a²+b²)；若已知斜边和一直角边 → b = √(c²−a²)。"),
    ("❌ 无图形题遗漏分类讨论",
     "AB=12、AC=10、BC 边上的高为 6，只算出 BC = 6√3+8。",
     "高可能在三角形<strong>内部或外部</strong> → BC = <strong>6√3+8 或 6√3−8</strong>（两个解都要写）。"),
    ("❌ 混淆勾股定理与逆定理",
     "由“a²+b²=c²”说“所以这个三角形是直角三角形”时，误以为是勾股定理。",
     "<strong>定理</strong>：直角 → a²+b²=c²；<strong>逆定理</strong>：a²+b²=c² → 该三角形是直角三角形（由边判定形状）。"),
    ("❌ 立体图形展开方式选错",
     "圆柱蚂蚁问题中，把纵向高与底面周长直接相加当最短路程。",
     "最短路径必须<strong>展开后取直线</strong>（勾股计算），路线一（绕顶）与路线二（侧面展开）要分别算再比较。"),
    ("❌ 勾股树类不会转化面积",
     "生长问题中逐个累加正方形边长再平方，计算量大且易错。",
     "利用 <strong>a²+b²=c²</strong>：每次生长新增面积 = 被生长正方形面积 → 生长 n 次总面积 = 初始面积 × (n+1)。"),
    ("❌ 折叠题找不到等量关系",
     "折叠后仍用原来的边长相减，忽略对应边相等。",
     "折叠性质：<strong>对应边相等、对应角相等</strong>（AB=AF、BE=EF），据此把未知量集中到一个直角三角形列方程。"),
    ("❌ 解三角形忽略高在外部",
     "钝角三角形中作高仍画在内部，导致边长算错。",
     "无图题要考虑<strong>锐角/钝角两种情形</strong>：钝角时高落在三角形<strong>外部</strong>，第三边 = 两段之差。"),
]

h = open(BASE_F, encoding='utf-8').read()
nq, nf, ne, nk = len(QUIZ), len(FLASH), len(ERRORS), len(KNOW)

h = h.replace('<title>🧮 二次根式综合复习 · 互动学习</title>', '<title>📐 勾股定理复习进阶 · 互动学习</title>', 1)
h = re.sub(r'<title>[^<]*</title>', '<title>📐 勾股定理复习进阶 · 互动学习</title>', h, count=1)
h = re.sub(r'<h1[^>]*>.*?</h1>', '<h1><i class="fas fa-drafting-compass"></i> 勾股定理复习进阶 · 互动学习</h1>', h, count=1, flags=re.DOTALL)
h = re.sub(r'<p>26秋博学班 数学第1讲 · \d+ 题 · \d+ 卡牌 \| 博学班</p>',
           f'<p>26秋博学班 数学第2讲 · {nq} 题 · {nf} 卡牌 | 博学班</p>', h, count=1)
h = re.sub(r'<span><i class="fas fa-check-circle"[^>]*></i> \d+道测验题</span>',
           f'<span><i class="fas fa-check-circle" style="color:var(--success)"></i> {nq}道测验题</span>', h, count=1)
h = re.sub(r'<span><i class="fas fa-layer-group"></i> \d+张知识卡</span>',
           f'<span><i class="fas fa-layer-group"></i> {nf}张知识卡</span>', h, count=1)
h = re.sub(r'<span><i class="fas fa-exclamation-triangle" style="color:var(--danger)"></i> \d+大易错点</span>',
           f'<span><i class="fas fa-exclamation-triangle" style="color:var(--danger)"></i> {ne}大易错点</span>', h, count=1)

g0 = h.find('<div class="knowledge-grid">'); g1 = h.find('<div class="teacher-talk">', g0)
assert g0 > 0 and g1 > g0
cards = ''
for cls, title, lis in KNOW:
    items = ''.join(f'<li>{x}</li>' for x in lis)
    cards += f'      <div class="knowledge-card {cls}"><h3>{title}</h3><ul>{items}</ul></div>\n'
h = h[:g0] + '<div class="knowledge-grid">\n' + cards + '    </div>\n    </div>\n    ' + h[g1:]

t0 = h.find('<div class="teacher-talk">'); t1 = h.find('<div id="tab-quiz"', t0)
tt = '''<div class="teacher-talk">
      <h4><i class="fas fa-microphone-alt"></i> 🎙️ 课堂要点 · 第二讲（勾股定理复习进阶）</h4>
      <p><strong>本讲核心（五大模块）</strong>：① <strong>展开图求最短路径</strong>（立体表面展开 + 勾股，取最小）；② <strong>勾股定理面积相关</strong>（正方形/半圆/勾股树面积转化）；③ <strong>设元求解</strong>（设 x 列勾股方程，折叠类用对应边相等）；④ <strong>B卷综合</strong>（数形结合、将军饮马、偶差勾股数组）；⑤ <strong>解三角形</strong>（作高转化，注意钝角高在外部）。</p>
      <p><strong>易错点（教师强调）</strong>：① 不区分斜边与直角边，盲目套公式（<strong>最长边才可能是斜边</strong>）；② 题目无图形时遗漏多种情况，缺分类讨论；③ 混淆勾股定理和逆定理；④ 立体图形展开方式选错；⑤ 勾股树不会转化面积关系；⑥ 解斜三角形作高时忽略高在三角形外部的情形。</p>
      <p><strong>教师寄语</strong>：勾股定理是平面几何核心工具——现阶段支撑几何计算；九年级学解直角三角形、圆、相似三角形、二次函数几何综合题频繁用到；也为高中平面解析几何两点间距离公式、立体几何空间距离计算奠基。</p>
      <p><strong>📝 作业</strong>：<strong>本讲巩固所有</strong>（巩固 1–4 全部完成）。</p>
    </div>
    '''
h = h[:t0] + tt + h[t1:]

q0 = h.find('const questions = ['); q1 = h.find('const flashcards = [', q0)
qdata = [{'q': q, 'opts': o, 'ans': a, 'exp': e} for q, o, a, e in QUIZ]
h = h[:q0] + 'const questions = ' + json.dumps(qdata, ensure_ascii=False, indent=1) + ';\n\n\n' + h[q1:]

f0 = h.find('const flashcards = ['); f1 = h.find('errors = [', f0)
fdata = [{'front': x, 'back': y} for x, y in FLASH]
h = h[:f0] + 'const flashcards = ' + json.dumps(fdata, ensure_ascii=False, indent=1) + ';\n\n\n' + h[f1:]

e0 = h.find('errors = ['); e1 = h.find('function toast', e0)
edata = [{'title': t, 'wrong': w, 'right': r} for t, w, r in ERRORS]
h = h[:e0] + 'errors = ' + json.dumps(edata, ensure_ascii=False, indent=1) + ';\n\n\n\n' + h[e1:]

h = h.replace('math26q_lesson1_state_check', 'math26q_lesson2_state_check')
h = h.replace("QUIZ_PROG_KEY='quiz_progress_math26q_lesson1'", "QUIZ_PROG_KEY='quiz_progress_math26q_lesson2'")
h = h.replace("WRONG_HISTORY_KEY='quiz_math26q_lesson1_wrong'", "WRONG_HISTORY_KEY='quiz_math26q_lesson2_wrong'")
h = h.replace('数学第1讲 · 二次根式综合复习', '数学第2讲 · 勾股定理复习进阶')
h = h.replace('第1讲 二次根式综合复习', '第2讲 勾股定理复习进阶')
h = h.replace('二次根式综合复习 | 博学班', '勾股定理复习进阶 | 博学班')
h = h.replace('数学 · 第1讲', '数学 · 第2讲')
h = re.sub(r"subject:'[^']*'", "subject:'数学(博学班)'", h, count=2)
h = re.sub(r"chapter:'[^']*'", "chapter:'第2讲 勾股定理复习进阶'", h, count=2)
h = re.sub(r"tags:'[^']*'", "tags:'数学,博学班,第2讲,勾股定理,最短路径,面积,设元,解三角形'", h, count=2)
h = re.sub(r'<div class="quiz-stats" id="quizStats">0 / \d+</div>', f'<div class="quiz-stats" id="quizStats">0 / {nq}</div>', h, count=1)
h = re.sub(r'共\d+张知识卡', f'共{nf}张知识卡', h, count=1)
open(OUT_F, 'w', encoding='utf-8').write(h)

js = r"""const fs=require('fs');const html=fs.readFileSync('math26q_lesson2_interactive.html','utf8');const re=/<script[^>]*>([\s\S]*?)<\/script>/g;let m,ok=true;while((m=re.exec(html))){try{new Function(m[1])}catch(e){ok=false;console.log('ERR',e.message)}}console.log(ok?'JS OK':'JS ERR')"""
r = subprocess.run(['node','-e',js], capture_output=True, text=True, cwd=REPO)
hh = open(OUT_F, encoding='utf-8').read()
print(r.stdout.strip())
print(f'题{nq} 卡{nf} 错{ne} 知识{nk}')
print('div:', len(re.findall(r'<div\b', hh)), '/', hh.count('</div>'))
print('残留 二次根式:', hh.count('二次根式'), '| lesson1:', hh.count('lesson1'), '| 第1讲:', hh.count('第1讲'))
