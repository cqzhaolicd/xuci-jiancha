# -*- coding: utf-8 -*-
"""升级 math8_ch6(数据分析) + math8_ch7(平行线的证明) 知识图谱:配图+定理说明"""
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def patch_file(fname, replacements, label):
    p = fname
    h = open(p, encoding='utf-8').read()
    for old, new in replacements:
        assert old in h, f'{label}: 未找到 -> {old[:60]}'
        h = h.replace(old, new, 1)
    open(p, 'w', encoding='utf-8').write(h)
    print(f'{label} 完成 ({len(replacements)} 处)')

# ================= ch6 数据分析 =================
# ① 中位数 升级
ch6_old2 = '<div class="k-item"><h4>中位数</h4><p>将数据从小到大排序后，位于中间的数（偶数个取中间两数平均数）。</p></div>'
ch6_new2 = ('<div class="k-item"><h4>中位数</h4><p><strong>定义</strong>：把数据<strong>从小到大排序</strong>后，位于中间位置的数。<br>'
            '<strong>求法</strong>：①排序；②奇数个 → 正中间那个；偶数个 → 中间两个的平均数。<br>'
            '<strong>例</strong>：数据 3,1,4,1,5 → 排序 1,1,3,4,5 → 中位数 3；<br>'
            '数据 3,1,4,1 → 排序 1,1,3,4 → 中位数 (1+3)/2 = 2。<br>'
            '<strong>特点</strong>：不受极端值影响（如收入中位数比平均数更能反映"大多数"水平）。</p></div>')

# ② 众数 升级
ch6_old3 = '<div class="k-item"><h4>众数</h4><p>一组数据中出现次数最多的数。可能不止一个，也可能没有。</p></div>'
ch6_new3 = ('<div class="k-item"><h4>众数</h4><p><strong>定义</strong>：一组数据中<strong>出现次数最多</strong>的数。<br>'
            '<strong>注意</strong>：①可能不止一个（如 1,1,2,2,3 众数是 1 和 2，都是众数）；②可能没有（各数据出现次数相同）；③众数<strong>不需要排序</strong>。<br>'
            '<strong>例</strong>：鞋店进哪种尺码 → 看众数（多数人穿这个码）。<br>'
            '<strong>区分</strong>：平均数=算术中心，中位数=位置中心，众数=出现最多的数。</p></div>')

# ③ 极差 升级
ch6_old4 = '<div class="k-item"><h4>极差</h4><p>最大值-最小值，反映数据波动范围。</p></div>'
ch6_new4 = ('<div class="k-item"><h4>极差</h4><p><strong>定义</strong>：极差 = 最大值 − 最小值。<br>'
            '<strong>意义</strong>：反映数据<strong>波动范围</strong>（最简单但只用了两个数据，受极端值影响大）。<br>'
            '<strong>例</strong>：数据 3,8,9,15 → 极差 = 15 − 3 = 12。<br>'
            '<strong>与方差区别</strong>：极差只看两端；方差看整体波动（每个数据都参与计算）。</p></div>')

# ④ 方差 升级 + 波动对比图
ch6_old5 = '<div class="k-item"><h4>方差</h4><p>各数据与平均数差的平方的平均数：S²=[∑(xi-x̄)²]/n。方差越小数据越稳定。</p></div>'
ch6_new5 = ('<div class="k-item"><h4>方差</h4><p><strong>定义</strong>：各数据与平均数<strong>差的平方的平均数</strong>：<br>S² = [(x₁−x̄)² + (x₂−x̄)² + … + (xₙ−x̄)²] / n。<br>'
            '<strong>意义</strong>：衡量数据<strong>波动大小</strong>——方差越小，数据越集中、越稳定。<br>'
            '<strong>步骤</strong>：①求平均数；②每个数据减平均数求差；③差平方；④求平均。<br>'
            '<strong>例</strong>：数据 5,5,6,6 → x̄=5.5，S²=[0.25+0.25+0.25+0.25]/4=0.25。<br>'
            '<strong>易错</strong>：方差单位是原数据单位的平方，比较稳定性看方差（或标准差）大小。</p>'
            '<div style="text-align:center;margin-top:.4rem">'
            '<svg viewBox="0 0 320 130" style="width:100%;max-width:300px;height:auto" xmlns="http://www.w3.org/2000/svg">'
            '<text x="10" y="16" font-size="10" fill="#4a5568" font-weight="bold">甲(稳定)：5,5,6,6</text>'
            '<line x1="20" y1="40" x2="300" y2="40" stroke="#e2e8f0" stroke-width="1"/>'
            '<circle cx="60" cy="35" r="4" fill="#48bb78"/><circle cx="120" cy="35" r="4" fill="#48bb78"/>'
            '<circle cx="180" cy="35" r="4" fill="#48bb78"/><circle cx="240" cy="35" r="4" fill="#48bb78"/>'
            '<text x="10" y="66" font-size="10" fill="#4a5568" font-weight="bold">乙(波动)：2,5,6,9</text>'
            '<line x1="20" y1="90" x2="300" y2="90" stroke="#e2e8f0" stroke-width="1"/>'
            '<circle cx="60" cy="95" r="4" fill="#e74c3c"/><circle cx="150" cy="82" r="4" fill="#e74c3c"/>'
            '<circle cx="200" cy="88" r="4" fill="#e74c3c"/><circle cx="270" cy="95" r="4" fill="#e74c3c"/>'
            '<text x="150" y="118" font-size="9" fill="#718096" text-anchor="middle">同一平均数5.5，乙偏离更远 → 方差大</text>'
            '</svg></div></div>')

# ⑤ 数据分析应用 升级
ch6_old7 = '<div class="k-item"><h4>数据分析应用</h4><p>选运动员（方差小更稳定）、评商品（众数代表多数意见）、测试成绩（中位数抗极端值）。</p></div>'
ch6_new7 = ('<div class="k-item"><h4>数据分析应用</h4><p><strong>选运动员</strong>：先看平均成绩，再看<strong>方差</strong>（方差小更稳定，优先选）。<br>'
            '<strong>评商品/进货</strong>：用<strong>众数</strong>（卖得最多的尺码/款式）。<br>'
            '<strong>考试成绩</strong>：用<strong>中位数</strong>（抗极端值，如一个 0 分不拉低整体水平）。<br>'
            '<strong>月收入/房价</strong>：中位数比平均数更真实（少数高收入拉高平均数）。<br>'
            '<strong>决策口诀</strong>："看水平用平均，看普遍用众数，看中间用中位，看稳定用方差"。</p></div>')

patch_file('math8_ch6_interactive.html',
           [(ch6_old2, ch6_new2), (ch6_old3, ch6_new3), (ch6_old4, ch6_new4),
            (ch6_old5, ch6_new5), (ch6_old7, ch6_new7)],
           'ch6 数据分析')

# ================= ch7 平行线的证明 =================
# ① 公理与定理 升级
ch7_old1 = '<div class="k-item"><h4>公理与定理</h4><p>公理：不需证明的基本事实；定理：经过证明的真命题。</p></div>'
ch7_new1 = ('<div class="k-item"><h4>公理与定理</h4><p><strong>公理</strong>：不需证明就承认的基本事实。如：两点确定一条直线；两点之间线段最短；同位角相等，两直线平行。<br>'
            '<strong>定理</strong>：经过<strong>推理证明</strong>的真命题，如：内错角相等两直线平行、三角形内角和 180°。<br>'
            '<strong>区别</strong>：公理是"起点"（默认成立），定理是"由公理推出的结论"（需证明）。<br>'
            '<strong>证明的依据</strong>：定义、公理、已证明的定理，每一步都要有依据。</p></div>')

# ② 平行线判定 升级(明示定理) + 角关系图
ch7_old2 = '<div class="k-item"><h4>平行线判定</h4><p>①同位角相等→平行 ②内错角相等→平行 ③同旁内角互补→平行 ④平行于同一直线的两直线平行。</p></div>'
ch7_new2 = ('<div class="k-item"><h4>平行线判定（定理）</h4><p><strong>判定定理</strong>（由角推线平行）：<br>'
            '① <strong>同位角相等</strong>，两直线平行（公理）；<br>'
            '② <strong>内错角相等</strong>，两直线平行；<br>'
            '③ <strong>同旁内角互补</strong>，两直线平行；<br>'
            '④ 平行于同一直线的两直线平行（传递性）。<br>'
            '<strong>记忆</strong>："F 型同位角、Z 型内错角、U 型同旁内角"。</p>'
            '<div style="text-align:center;margin-top:.4rem">'
            '<svg viewBox="0 0 300 160" style="width:100%;max-width:280px;height:auto" xmlns="http://www.w3.org/2000/svg">'
            '<line x1="40" y1="40" x2="280" y2="40" stroke="#e74c3c" stroke-width="2"/>'
            '<line x1="40" y1="110" x2="280" y2="110" stroke="#48bb78" stroke-width="2"/>'
            '<line x1="80" y1="140" x2="240" y2="15" stroke="#2d3748" stroke-width="1.5"/>'
            '<text x="288" y="44" font-size="10" fill="#c0392b" font-weight="bold">a</text>'
            '<text x="288" y="114" font-size="10" fill="#2f855a" font-weight="bold">b</text>'
            '<text x="228" y="26" font-size="10" fill="#718096">截线c</text>'
            '<circle cx="160" cy="40" r="1.5" fill="#e74c3c"/><circle cx="172" cy="40" r="1.5" fill="#e74c3c"/>'
            '<text x="150" y="30" font-size="9" fill="#c0392b" font-weight="bold">∠1=∠2</text>'
            '<text x="150" y="55" font-size="9" fill="#718096">同位角(F)</text>'
            '<circle cx="166" cy="110" r="1.5" fill="#48bb78"/><circle cx="178" cy="110" r="1.5" fill="#48bb78"/>'
            '<text x="160" y="126" font-size="9" fill="#718096">内错角(Z)</text>'
            '<circle cx="126" cy="40" r="1.5" fill="#e74c3c"/><circle cx="138" cy="110" r="1.5" fill="#48bb78"/>'
            '<text x="96" y="88" font-size="9" fill="#4c51bf" font-weight="bold">同旁内角(U)</text>'
            '</svg></div></div>')

# ③ 平行线性质 升级(明示定理) + 图
ch7_old3 = '<div class="k-item"><h4>平行线性质</h4><p>两直线平行→①同位角相等 ②内错角相等 ③同旁内角互补。</p></div>'
ch7_new3 = ('<div class="k-item"><h4>平行线性质（定理）</h4><p><strong>性质定理</strong>（由线平行推角关系）：<br>'
            '两直线平行 → ① <strong>同位角相等</strong>；② <strong>内错角相等</strong>；③ <strong>同旁内角互补</strong>。<br>'
            '<strong>判定 vs 性质</strong>：<br>判定——由角的关系 → 推两线平行（"角推线"）；<br>性质——由两线平行 → 推角的关系（"线推角"）。<br>'
            '<strong>注意</strong>：只有两直线<strong>确实平行</strong>时，性质才成立！</p>'
            '<div style="text-align:center;margin-top:.4rem">'
            '<svg viewBox="0 0 300 160" style="width:100%;max-width:280px;height:auto" xmlns="http://www.w3.org/2000/svg">'
            '<line x1="40" y1="40" x2="280" y2="40" stroke="#e74c3c" stroke-width="2"/>'
            '<line x1="40" y1="110" x2="280" y2="110" stroke="#48bb78" stroke-width="2"/>'
            '<line x1="80" y1="140" x2="240" y2="15" stroke="#2d3748" stroke-width="1.5"/>'
            '<text x="288" y="44" font-size="10" fill="#c0392b" font-weight="bold">a∥b</text>'
            '<text x="60" y="128" font-size="10" fill="#c0392b" font-weight="bold">a</text>'
            '<text x="60" y="86" font-size="10" fill="#2f855a" font-weight="bold">b</text>'
            '<text x="10" y="20" font-size="9" fill="#718096">a∥b 时：</text>'
            '<circle cx="160" cy="40" r="1.5" fill="#e74c3c"/><circle cx="172" cy="40" r="1.5" fill="#e74c3c"/>'
            '<text x="150" y="30" font-size="9" fill="#c0392b" font-weight="bold">∠1=∠2</text>'
            '<text x="150" y="55" font-size="9" fill="#718096">同位角相等</text>'
            '<text x="96" y="88" font-size="9" fill="#4c51bf" font-weight="bold">∠3+∠4=180°</text>'
            '<circle cx="126" cy="40" r="1.5" fill="#e74c3c"/><circle cx="138" cy="110" r="1.5" fill="#48bb78"/>'
            '</svg></div></div>')

# ④ 三角形内角和 升级 + 图
ch7_old4 = '<div class="k-item"><h4>三角形内角和</h4><p>三角形三个内角之和等于180°。用途：已知两角求第三角，如∠A=40°、∠B=60°，则∠C=180°-40°-60°=80°。</p></div>'
ch7_new4 = ('<div class="k-item"><h4>三角形内角和（定理）</h4><p><strong>定理</strong>：三角形三个内角之和等于 <strong>180°</strong>。<br>'
            '<strong>证明思路</strong>：过顶点作对边平行线，把三个角"搬"到一起拼成平角。<br>'
            '<strong>推论</strong>：①直角三角形两锐角互余（和为 90°）；②一个三角形至多一个直角/钝角；③三角形至少两个锐角。<br>'
            '<strong>应用</strong>：已知两角求第三角——∠C = 180° − ∠A − ∠B。<br>'
            '例：∠A=40°、∠B=60°，则 ∠C = 180°−40°−60° = 80°。</p>'
            '<div style="text-align:center;margin-top:.4rem">'
            '<svg viewBox="0 0 240 150" style="width:100%;max-width:220px;height:auto" xmlns="http://www.w3.org/2000/svg">'
            '<polygon points="40,130 210,130 100,25" fill="#e74c3c18" stroke="#e74c3c" stroke-width="2"/>'
            '<text x="48" y="124" font-size="11" fill="#2d3748" font-weight="bold">A</text>'
            '<text x="214" y="124" font-size="11" fill="#2d3748" font-weight="bold">B</text>'
            '<text x="98" y="22" font-size="11" fill="#2d3748" font-weight="bold">C</text>'
            '<path d="M 55 120 A 18 18 0 0 0 70 130" fill="none" stroke="#48bb78" stroke-width="1.2"/>'
            '<text x="44" y="108" font-size="9" fill="#2f855a">∠A</text>'
            '<path d="M 205 120 A 20 20 0 0 0 195 130" fill="none" stroke="#4c51bf" stroke-width="1.2"/>'
            '<text x="196" y="108" font-size="9" fill="#4c51bf">∠B</text>'
            '<path d="M 112 32 A 16 16 0 0 0 100 40" fill="none" stroke="#c05621" stroke-width="1.2"/>'
            '<text x="112" y="52" font-size="9" fill="#c05621">∠C</text>'
            '<text x="120" y="142" font-size="10" fill="#c0392b" font-weight="bold" text-anchor="middle">∠A+∠B+∠C=180°</text>'
            '</svg></div></div>')

# ⑤ 三角形外角 升级 + 图
ch7_old5 = '<div class="k-item"><h4>三角形外角</h4><p>三角形的一个外角等于与它不相邻的两个内角之和。例：△ABC中∠A=50°、∠B=60°，则∠C的外角=∠A+∠B=110°。</p></div>'
ch7_new5 = ('<div class="k-item"><h4>三角形外角（定理）</h4><p><strong>外角定义</strong>：三角形一边与另一边的延长线组成的角。<br>'
            '<strong>定理</strong>：三角形的一个外角<strong>等于</strong>与它不相邻的两个内角之和。<br>'
            '<strong>推论</strong>：外角大于任何一个与它不相邻的内角。<br>'
            '<strong>应用</strong>：∠ACD = ∠A + ∠B（不经过中间步骤直接求）。<br>'
            '例：∠A=50°、∠B=60°，则 ∠C 的外角 = 50°+60° = 110°。<br>'
            '<strong>注意</strong>：外角与相邻内角互补（和为 180°）。</p>'
            '<div style="text-align:center;margin-top:.4rem">'
            '<svg viewBox="0 0 260 150" style="width:100%;max-width:240px;height:auto" xmlns="http://www.w3.org/2000/svg">'
            '<polygon points="40,130 200,130 90,25" fill="#e74c3c18" stroke="#e74c3c" stroke-width="2"/>'
            '<line x1="200" y1="130" x2="250" y2="130" stroke="#e74c3c" stroke-width="2"/>'
            '<text x="48" y="124" font-size="11" fill="#2d3748" font-weight="bold">A</text>'
            '<text x="204" y="124" font-size="11" fill="#2d3748" font-weight="bold">B</text>'
            '<text x="204" y="140" font-size="10" fill="#c0392b" font-weight="bold">D</text>'
            '<text x="88" y="22" font-size="11" fill="#2d3748" font-weight="bold">C</text>'
            '<path d="M 215 124 A 12 12 0 0 0 212 130" fill="none" stroke="#c05621" stroke-width="1.5"/>'
            '<text x="216" y="116" font-size="9" fill="#c05621">∠ACD</text>'
            '<path d="M 55 120 A 18 18 0 0 0 70 130" fill="none" stroke="#48bb78" stroke-width="1.2"/>'
            '<text x="44" y="108" font-size="9" fill="#2f855a">∠A</text>'
            '<path d="M 193 120 A 20 20 0 0 0 183 130" fill="none" stroke="#4c51bf" stroke-width="1.2"/>'
            '<text x="174" y="108" font-size="9" fill="#4c51bf">∠B</text>'
            '<text x="120" y="148" font-size="10" fill="#c0392b" font-weight="bold" text-anchor="middle">∠ACD = ∠A + ∠B</text>'
            '</svg></div></div>')

patch_file('math8_ch7_interactive.html',
           [(ch7_old1, ch7_new1), (ch7_old2, ch7_new2), (ch7_old3, ch7_new3),
            (ch7_old4, ch7_new4), (ch7_old5, ch7_new5)],
           'ch7 平行线证明')
print('ALL DONE')
