# -*- coding: utf-8 -*-
"""重画 math8 ch5/ch6/ch7 的 SVG 图,确保几何坐标与数学声明严格一致"""
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def patch_file(fname, replacements, label):
    h = open(fname, encoding='utf-8').read()
    for old, new in replacements:
        assert old in h, f'{label}: 未找到 -> {old[:80]}'
        h = h.replace(old, new, 1)
    open(fname, 'w', encoding='utf-8').write(h)
    print(f'{label} 完成 ({len(replacements)} 处)')

# ============ ch5 交点图: x+y=5(y=−x+5) 与 x−y=1(y=x−1) 交点(3,2)。原点(120,110) 每单位20px ============
# y=−x+5: (0,5)=(120,10), (5,0)=(220,110); y=x−1: (1,0)=(140,110), (4,3)=(200,50); 交点(3,2)=(180,70)
old_int5 = ('<svg viewBox="0 0 240 220" style="width:100%;max-width:220px;height:auto" xmlns="http://www.w3.org/2000/svg">'
            '<line x1="30" y1="110" x2="210" y2="110" stroke="#2d3748" stroke-width="1.5"/>'
            '<line x1="120" y1="200" x2="120" y2="20" stroke="#2d3748" stroke-width="1.5"/>'
            '<text x="214" y="114" font-size="11" fill="#2d3748">x</text><text x="124" y="24" font-size="11" fill="#2d3748">y</text>'
            '<line x1="40" y1="170" x2="200" y2="50" stroke="#e74c3c" stroke-width="2"/>'
            '<text x="160" y="60" font-size="10" fill="#c0392b" font-weight="bold">x+y=5</text>'
            '<line x1="40" y1="50" x2="200" y2="170" stroke="#48bb78" stroke-width="2"/>'
            '<text x="40" y="60" font-size="10" fill="#2f855a" font-weight="bold">x−y=1</text>'
            '<circle cx="120" cy="110" r="4" fill="#e74c3c"/>'
            '<text x="104" y="100" font-size="10" fill="#c0392b" font-weight="bold">交点(3,2)</text>'
            '</svg>')

new_int5 = ('<svg viewBox="0 0 240 220" style="width:100%;max-width:220px;height:auto" xmlns="http://www.w3.org/2000/svg">'
            '<line x1="30" y1="110" x2="210" y2="110" stroke="#2d3748" stroke-width="1.5"/>'
            '<line x1="120" y1="200" x2="120" y2="20" stroke="#2d3748" stroke-width="1.5"/>'
            '<text x="214" y="114" font-size="11" fill="#2d3748">x</text><text x="124" y="24" font-size="11" fill="#2d3748">y</text>'
            '<line x1="120" y1="10" x2="220" y2="110" stroke="#e74c3c" stroke-width="2"/>'
            '<text x="132" y="28" font-size="10" fill="#c0392b" font-weight="bold">x+y=5</text>'
            '<line x1="140" y1="110" x2="200" y2="50" stroke="#48bb78" stroke-width="2"/>'
            '<text x="202" y="92" font-size="10" fill="#2f855a" font-weight="bold">x−y=1</text>'
            '<circle cx="180" cy="70" r="4" fill="#e74c3c"/>'
            '<text x="186" y="62" font-size="10" fill="#c0392b" font-weight="bold">交点(3,2)</text>'
            '</svg>')

# ============ ch5 解的判断图: 相交(斜率异号)→唯一解; 平行(同斜率)→无解; 重合(同线)→无数解 ============
old_judge = ('<svg viewBox="0 0 320 110" style="width:100%;max-width:300px;height:auto" xmlns="http://www.w3.org/2000/svg">'
             '<line x1="20" y1="80" x2="90" y2="20" stroke="#e74c3c" stroke-width="2"/>'
             '<line x1="50" y1="90" x2="120" y2="30" stroke="#48bb78" stroke-width="2"/>'
             '<circle cx="74" cy="53" r="3.5" fill="#e74c3c"/><text x="60" y="50" font-size="9" fill="#c0392b" font-weight="bold">相交</text>'
             '<text x="30" y="102" font-size="9" fill="#718096">唯一解</text>'
             '<line x1="170" y1="85" x2="240" y2="25" stroke="#e74c3c" stroke-width="2"/>'
             '<line x1="180" y1="85" x2="250" y2="25" stroke="#48bb78" stroke-width="2"/>'
             '<text x="185" y="102" font-size="9" fill="#718096">平行 → 无解</text>'
             '<line x1="290" y1="70" x2="290" y2="30" stroke="#e74c3c" stroke-width="3"/>'
             '<line x1="300" y1="70" x2="300" y2="30" stroke="#48bb78" stroke-width="3" stroke-dasharray="3,3"/>'
             '<text x="282" y="102" font-size="9" fill="#718096">重合→无数解</text>'
             '</svg>')

# 相交: 线1 (20,90)-(90,20) 斜率-1; 线2 (20,30)-(90,100) 斜率+1; 交点(55,60)
# 平行: 线1 (160,90)-(230,20) 斜率-1; 线2 (170,90)-(240,20) 斜率-1
# 重合: 线 (280,80)-(310,50) 斜率-1, 实线+虚线叠加
new_judge = ('<svg viewBox="0 0 320 110" style="width:100%;max-width:300px;height:auto" xmlns="http://www.w3.org/2000/svg">'
             '<line x1="20" y1="90" x2="90" y2="20" stroke="#e74c3c" stroke-width="2"/>'
             '<line x1="20" y1="30" x2="90" y2="100" stroke="#48bb78" stroke-width="2"/>'
             '<circle cx="55" cy="60" r="3.5" fill="#e74c3c"/><text x="62" y="50" font-size="9" fill="#c0392b" font-weight="bold">相交</text>'
             '<text x="30" y="104" font-size="9" fill="#718096">唯一解</text>'
             '<line x1="160" y1="90" x2="230" y2="20" stroke="#e74c3c" stroke-width="2"/>'
             '<line x1="170" y1="90" x2="240" y2="20" stroke="#48bb78" stroke-width="2"/>'
             '<text x="183" y="104" font-size="9" fill="#718096">平行 → 无解</text>'
             '<line x1="280" y1="80" x2="310" y2="50" stroke="#e74c3c" stroke-width="3"/>'
             '<line x1="280" y1="80" x2="310" y2="50" stroke="#48bb78" stroke-width="2" stroke-dasharray="4,3"/>'
             '<text x="295" y="104" font-size="9" fill="#718096">重合 → 无数解</text>'
             '</svg>')

# ============ ch6 方差图: 甲 5,5,6,6 均5.5 波动小; 乙 2,5,6,9 均5.5 波动大。点位置: 甲(60,33)(120,33)(180,37)(240,37); 乙(60,112)(150,98)(200,92)(270,78) ============
old_var = ('<svg viewBox="0 0 320 130" style="width:100%;max-width:300px;height:auto" xmlns="http://www.w3.org/2000/svg">'
           '<text x="10" y="16" font-size="10" fill="#4a5568" font-weight="bold">甲(稳定)：5,5,6,6</text>'
           '<line x1="20" y1="40" x2="300" y2="40" stroke="#e2e8f0" stroke-width="1"/>'
           '<circle cx="60" cy="35" r="4" fill="#48bb78"/><circle cx="120" cy="35" r="4" fill="#48bb78"/>'
           '<circle cx="180" cy="35" r="4" fill="#48bb78"/><circle cx="240" cy="35" r="4" fill="#48bb78"/>'
           '<text x="10" y="66" font-size="10" fill="#4a5568" font-weight="bold">乙(波动)：2,5,6,9</text>'
           '<line x1="20" y1="90" x2="300" y2="90" stroke="#e2e8f0" stroke-width="1"/>'
           '<circle cx="60" cy="95" r="4" fill="#e74c3c"/><circle cx="150" cy="82" r="4" fill="#e74c3c"/>'
           '<circle cx="200" cy="88" r="4" fill="#e74c3c"/><circle cx="270" cy="95" r="4" fill="#e74c3c"/>'
           '<text x="150" y="118" font-size="9" fill="#718096" text-anchor="middle">同一平均数5.5，乙偏离更远 → 方差大</text>'
           '</svg>')

new_var = ('<svg viewBox="0 0 320 130" style="width:100%;max-width:300px;height:auto" xmlns="http://www.w3.org/2000/svg">'
           '<text x="10" y="16" font-size="10" fill="#4a5568" font-weight="bold">甲(稳定)：5,5,6,6</text>'
           '<line x1="20" y1="35" x2="300" y2="35" stroke="#e2e8f0" stroke-width="1" stroke-dasharray="3,3"/>'
           '<text x="302" y="38" font-size="8" fill="#a0aec0">x̄=5.5</text>'
           '<circle cx="60" cy="32" r="4" fill="#48bb78"/><circle cx="120" cy="32" r="4" fill="#48bb78"/>'
           '<circle cx="180" cy="38" r="4" fill="#48bb78"/><circle cx="240" cy="38" r="4" fill="#48bb78"/>'
           '<text x="10" y="66" font-size="10" fill="#4a5568" font-weight="bold">乙(波动)：2,5,6,9</text>'
           '<line x1="20" y1="95" x2="300" y2="95" stroke="#e2e8f0" stroke-width="1" stroke-dasharray="3,3"/>'
           '<text x="302" y="98" font-size="8" fill="#a0aec0">x̄=5.5</text>'
           '<circle cx="60" cy="112" r="4" fill="#e74c3c"/><circle cx="150" cy="98" r="4" fill="#e74c3c"/>'
           '<circle cx="200" cy="92" r="4" fill="#e74c3c"/><circle cx="270" cy="78" r="4" fill="#e74c3c"/>'
           '<text x="160" y="124" font-size="9" fill="#718096" text-anchor="middle">同一平均数5.5，乙偏离更远 → 方差大</text>'
           '</svg>')

# ============ ch7 三线八角图(判定+性质): 两平行线 a(y=40) b(y=110), 截线过 A(208,40) 与 B(118.4,110) ============
# 截线 (80,140)→(240,15)。A 在 y=40: x=208; B 在 y=110: x=118.4
old_para_judge = ('<svg viewBox="0 0 300 160" style="width:100%;max-width:280px;height:auto" xmlns="http://www.w3.org/2000/svg">'
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
                  '</svg>')

new_para_judge = ('<svg viewBox="0 0 300 160" style="width:100%;max-width:280px;height:auto" xmlns="http://www.w3.org/2000/svg">'
                  '<line x1="40" y1="40" x2="280" y2="40" stroke="#e74c3c" stroke-width="2"/>'
                  '<line x1="40" y1="110" x2="280" y2="110" stroke="#48bb78" stroke-width="2"/>'
                  '<line x1="80" y1="140" x2="240" y2="15" stroke="#2d3748" stroke-width="1.5"/>'
                  '<text x="288" y="44" font-size="10" fill="#c0392b" font-weight="bold">a</text>'
                  '<text x="288" y="114" font-size="10" fill="#2f855a" font-weight="bold">b</text>'
                  '<text x="228" y="26" font-size="10" fill="#718096">截线c</text>'
                  '<circle cx="208" cy="40" r="2.5" fill="#e74c3c"/>'
                  '<circle cx="118" cy="110" r="2.5" fill="#48bb78"/>'
                  '<text x="214" y="32" font-size="9" fill="#c0392b" font-weight="bold">∠1</text>'
                  '<text x="106" y="100" font-size="9" fill="#48bb78" font-weight="bold">∠2</text>'
                  '<text x="214" y="52" font-size="9" fill="#4c51bf" font-weight="bold">∠3</text>'
                  '<text x="96" y="120" font-size="9" fill="#c05621" font-weight="bold">∠4</text>'
                  '<text x="150" y="150" font-size="9" fill="#718096" text-anchor="middle">同位角∠1=∠2 · 内错角∠3=∠4 · 同旁内角互补</text>'
                  '</svg>')

old_para_prop = ('<svg viewBox="0 0 300 160" style="width:100%;max-width:280px;height:auto" xmlns="http://www.w3.org/2000/svg">'
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
                 '</svg>')

new_para_prop = ('<svg viewBox="0 0 300 160" style="width:100%;max-width:280px;height:auto" xmlns="http://www.w3.org/2000/svg">'
                 '<line x1="40" y1="40" x2="280" y2="40" stroke="#e74c3c" stroke-width="2"/>'
                 '<line x1="40" y1="110" x2="280" y2="110" stroke="#48bb78" stroke-width="2"/>'
                 '<line x1="80" y1="140" x2="240" y2="15" stroke="#2d3748" stroke-width="1.5"/>'
                 '<text x="288" y="44" font-size="10" fill="#c0392b" font-weight="bold">a</text>'
                 '<text x="288" y="114" font-size="10" fill="#2f855a" font-weight="bold">b</text>'
                 '<text x="228" y="26" font-size="10" fill="#718096">截线c</text>'
                 '<text x="10" y="20" font-size="9" fill="#718096">a∥b 时：</text>'
                 '<circle cx="208" cy="40" r="2.5" fill="#e74c3c"/>'
                 '<circle cx="118" cy="110" r="2.5" fill="#48bb78"/>'
                 '<text x="214" y="32" font-size="9" fill="#c0392b" font-weight="bold">∠1</text>'
                 '<text x="106" y="100" font-size="9" fill="#48bb78" font-weight="bold">∠2</text>'
                 '<text x="214" y="52" font-size="9" fill="#4c51bf" font-weight="bold">∠3</text>'
                 '<text x="96" y="120" font-size="9" fill="#c05621" font-weight="bold">∠4</text>'
                 '<text x="150" y="150" font-size="9" fill="#718096" text-anchor="middle">同位角∠1=∠2 · 内错角∠3=∠4 · 同旁内角∠3+∠4=180°</text>'
                 '</svg>')

# ============ ch7 内角和图: 三角形 A(40,130) B(210,130) C(100,25) 修正文字位置 ============
old_sum = ('<svg viewBox="0 0 240 150" style="width:100%;max-width:220px;height:auto" xmlns="http://www.w3.org/2000/svg">'
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
           '</svg>')

new_sum = ('<svg viewBox="0 0 240 150" style="width:100%;max-width:220px;height:auto" xmlns="http://www.w3.org/2000/svg">'
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
           '</svg>')

# ============ ch7 外角图: 三角形 A(40,130) B(200,130) C(90,25), 延长 CB 到 D ============
# 外角 ∠ACD = ∠A + ∠B。延长 BC(C 的延长方向)? 标准:延长 BC 到 D,外角 ∠ACD 顶点 C。
# 但 C 是顶角,延长 BC 到 D 使 D 在 C 下方右侧: C(90,25) 方向沿 CB(200,130): 方向(110,105)
# D = C + (C-B) = (90+(-110), 25+(-105)) = (-20,-80) 出界。改用延长 AC 或选三角形旋转。
# 简单方案: 三角形 A(90,25) B(40,130) C(240,130), 延长 BC 到 D(280,130), 外角 ∠ACD 顶点 C(240,130)
old_ext = ('<svg viewBox="0 0 260 150" style="width:100%;max-width:240px;height:auto" xmlns="http://www.w3.org/2000/svg">'
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
           '</svg>')

# 重画: A(90,25) 顶, B(40,130) 左底, C(240,130) 右底, 延长 BC 到 D(280,130)
# 外角 ∠ACD 在 C(240,130): 边 CA 与 CD(水平向右)。弧线在 C 处画一个弧(表示外角)
new_ext = ('<svg viewBox="0 0 290 150" style="width:100%;max-width:260px;height:auto" xmlns="http://www.w3.org/2000/svg">'
           '<polygon points="90,25 40,130 240,130" fill="#e74c3c18" stroke="#e74c3c" stroke-width="2"/>'
           '<line x1="240" y1="130" x2="280" y2="130" stroke="#c05621" stroke-width="2"/>'
           '<text x="96" y="22" font-size="11" fill="#2d3748" font-weight="bold">A</text>'
           '<text x="30" y="134" font-size="11" fill="#2d3748" font-weight="bold">B</text>'
           '<text x="244" y="134" font-size="11" fill="#2d3748" font-weight="bold">C</text>'
           '<text x="284" y="134" font-size="10" fill="#c05621" font-weight="bold">D</text>'
           '<path d="M 248 120 A 14 14 0 0 1 252 130" fill="none" stroke="#c05621" stroke-width="1.5"/>'
           '<text x="254" y="116" font-size="9" fill="#c05621">∠ACD</text>'
           '<path d="M 92 32 A 16 16 0 0 0 84 40" fill="none" stroke="#48bb78" stroke-width="1.2"/>'
           '<text x="70" y="42" font-size="9" fill="#2f855a">∠A</text>'
           '<path d="M 50 122 A 16 16 0 0 0 42 128" fill="none" stroke="#4c51bf" stroke-width="1.2"/>'
           '<text x="26" y="118" font-size="9" fill="#4c51bf">∠B</text>'
           '<text x="145" y="148" font-size="10" fill="#c0392b" font-weight="bold" text-anchor="middle">∠ACD = ∠A + ∠B（C的外角）</text>'
           '</svg>')

patch_file('math8_ch5_interactive.html', [(old_int5, new_int5), (old_judge, new_judge)], 'ch5 交点/判断')
patch_file('math8_ch6_interactive.html', [(old_var, new_var)], 'ch6 方差')
patch_file('math8_ch7_interactive.html', [(old_para_judge, new_para_judge), (old_para_prop, new_para_prop), (old_sum, new_sum), (old_ext, new_ext)], 'ch7 平行/内角/外角')
print('ALL DONE')
