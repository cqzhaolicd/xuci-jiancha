# -*- coding: utf-8 -*-
"""重画 math8 ch2/ch3/ch4 的 SVG 图,确保几何坐标与数学声明严格一致"""
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def patch_file(fname, replacements, label):
    h = open(fname, encoding='utf-8').read()
    for old, new in replacements:
        assert old in h, f'{label}: 未找到 -> {old[:80]}'
        h = h.replace(old, new, 1)
    open(fname, 'w', encoding='utf-8').write(h)
    print(f'{label} 完成 ({len(replacements)} 处)')

# ============ ch2 数轴图: √2 在1~2之间(x≈105), √5 在2~3之间(x≈154), √3 在1~2(x≈124) ============
old_num = ('<svg viewBox="0 0 300 70" style="width:100%;max-width:280px;height:auto" xmlns="http://www.w3.org/2000/svg">'
           '<line x1="10" y1="35" x2="290" y2="35" stroke="#2d3748" stroke-width="1.5"/>'
           '<polygon points="290,35 282,31 282,39" fill="#2d3748"/>'
           '<line x1="60" y1="30" x2="60" y2="40" stroke="#2d3748" stroke-width="1"/><text x="60" y="55" font-size="10" fill="#4a5568" text-anchor="middle">1</text>'
           '<line x1="130" y1="30" x2="130" y2="40" stroke="#2d3748" stroke-width="1"/><text x="130" y="55" font-size="10" fill="#4a5568" text-anchor="middle">2</text>'
           '<line x1="200" y1="30" x2="200" y2="40" stroke="#2d3748" stroke-width="1"/><text x="200" y="55" font-size="10" fill="#4a5568" text-anchor="middle">3</text>'
           '<line x1="270" y1="30" x2="270" y2="40" stroke="#2d3748" stroke-width="1"/><text x="270" y="55" font-size="10" fill="#4a5568" text-anchor="middle">4</text>'
           '<line x1="97" y1="25" x2="97" y2="45" stroke="#e74c3c" stroke-width="2"/>'
           '<text x="97" y="20" font-size="10" fill="#c0392b" font-weight="bold" text-anchor="middle">√2≈1.41</text>'
           '<line x1="168" y1="25" x2="168" y2="45" stroke="#e74c3c" stroke-width="2"/>'
           '<text x="168" y="20" font-size="10" fill="#c0392b" font-weight="bold" text-anchor="middle">√3≈1.73</text>'
           '</svg>')

new_num = ('<svg viewBox="0 0 320 80" style="width:100%;max-width:300px;height:auto" xmlns="http://www.w3.org/2000/svg">'
           '<line x1="20" y1="42" x2="305" y2="42" stroke="#2d3748" stroke-width="1.5"/>'
           '<polygon points="305,42 297,38 297,46" fill="#2d3748"/>'
           '<line x1="20" y1="36" x2="20" y2="48" stroke="#2d3748" stroke-width="1"/><text x="20" y="62" font-size="10" fill="#4a5568" text-anchor="middle">0</text>'
           '<line x1="80" y1="36" x2="80" y2="48" stroke="#2d3748" stroke-width="1"/><text x="80" y="62" font-size="10" fill="#4a5568" text-anchor="middle">1</text>'
           '<line x1="140" y1="36" x2="140" y2="48" stroke="#2d3748" stroke-width="1"/><text x="140" y="62" font-size="10" fill="#4a5568" text-anchor="middle">2</text>'
           '<line x1="200" y1="36" x2="200" y2="48" stroke="#2d3748" stroke-width="1"/><text x="200" y="62" font-size="10" fill="#4a5568" text-anchor="middle">3</text>'
           '<line x1="260" y1="36" x2="260" y2="48" stroke="#2d3748" stroke-width="1"/><text x="260" y="62" font-size="10" fill="#4a5568" text-anchor="middle">4</text>'
           '<line x1="105" y1="32" x2="105" y2="52" stroke="#e74c3c" stroke-width="2"/>'
           '<text x="105" y="24" font-size="10" fill="#c0392b" font-weight="bold" text-anchor="middle">√2≈1.41</text>'
           '<line x1="124" y1="32" x2="124" y2="52" stroke="#e74c3c" stroke-width="2"/>'
           '<text x="124" y="74" font-size="10" fill="#c0392b" font-weight="bold" text-anchor="middle">√3≈1.73</text>'
           '<line x1="154" y1="32" x2="154" y2="52" stroke="#e74c3c" stroke-width="2"/>'
           '<text x="168" y="24" font-size="10" fill="#c0392b" font-weight="bold" text-anchor="middle">√5≈2.24</text>'
           '</svg>')

# ============ ch3 坐标系图: 原点(120,120) 每单位20px, P(4,3)=(200,60) ============
old_cs = ('<svg viewBox="0 0 220 220" style="width:100%;max-width:200px;height:auto" xmlns="http://www.w3.org/2000/svg">'
          '<line x1="20" y1="110" x2="200" y2="110" stroke="#2d3748" stroke-width="1.5"/>'
          '<polygon points="200,110 192,106 192,114" fill="#2d3748"/>'
          '<line x1="110" y1="200" x2="110" y2="20" stroke="#2d3748" stroke-width="1.5"/>'
          '<polygon points="110,20 106,28 114,28" fill="#2d3748"/>'
          '<circle cx="110" cy="110" r="3" fill="#e74c3c"/>'
          '<text x="204" y="114" font-size="11" fill="#2d3748">x</text>'
          '<text x="114" y="24" font-size="11" fill="#2d3748">y</text>'
          '<text x="96" y="126" font-size="10" fill="#718096">O</text>'
          '<circle cx="150" cy="60" r="3.5" fill="#e74c3c"/>'
          '<text x="156" y="56" font-size="10" fill="#c0392b" font-weight="bold">P(4,3)</text>'
          '<line x1="150" y1="60" x2="150" y2="110" stroke="#e74c3c" stroke-width="1" stroke-dasharray="3,3"/>'
          '<line x1="150" y1="110" x2="110" y2="110" stroke="#e74c3c" stroke-width="1" stroke-dasharray="3,3"/>'
          '<text x="135" y="125" font-size="9" fill="#718096">横4</text>'
          '<text x="128" y="95" font-size="9" fill="#718096">纵3</text>'
          '</svg>')

new_cs = ('<svg viewBox="0 0 240 240" style="width:100%;max-width:210px;height:auto" xmlns="http://www.w3.org/2000/svg">'
          '<line x1="20" y1="120" x2="220" y2="120" stroke="#2d3748" stroke-width="1.5"/>'
          '<polygon points="220,120 212,116 212,124" fill="#2d3748"/>'
          '<line x1="120" y1="220" x2="120" y2="20" stroke="#2d3748" stroke-width="1.5"/>'
          '<polygon points="120,20 116,28 124,28" fill="#2d3748"/>'
          '<line x1="140" y1="115" x2="140" y2="125" stroke="#2d3748" stroke-width="1"/><text x="140" y="136" font-size="9" fill="#4a5568" text-anchor="middle">1</text>'
          '<line x1="160" y1="115" x2="160" y2="125" stroke="#2d3748" stroke-width="1"/><text x="160" y="136" font-size="9" fill="#4a5568" text-anchor="middle">2</text>'
          '<line x1="180" y1="115" x2="180" y2="125" stroke="#2d3748" stroke-width="1"/><text x="180" y="136" font-size="9" fill="#4a5568" text-anchor="middle">3</text>'
          '<line x1="200" y1="115" x2="200" y2="125" stroke="#2d3748" stroke-width="1"/><text x="200" y="136" font-size="9" fill="#4a5568" text-anchor="middle">4</text>'
          '<line x1="115" y1="100" x2="125" y2="100" stroke="#2d3748" stroke-width="1"/><text x="110" y="103" font-size="9" fill="#4a5568" text-anchor="end">1</text>'
          '<line x1="115" y1="80" x2="125" y2="80" stroke="#2d3748" stroke-width="1"/><text x="110" y="83" font-size="9" fill="#4a5568" text-anchor="end">2</text>'
          '<line x1="115" y1="60" x2="125" y2="60" stroke="#2d3748" stroke-width="1"/><text x="110" y="63" font-size="9" fill="#4a5568" text-anchor="end">3</text>'
          '<circle cx="120" cy="120" r="3" fill="#e74c3c"/>'
          '<text x="224" y="124" font-size="11" fill="#2d3748">x</text>'
          '<text x="124" y="24" font-size="11" fill="#2d3748">y</text>'
          '<text x="104" y="136" font-size="10" fill="#718096">O</text>'
          '<circle cx="200" cy="60" r="4" fill="#e74c3c"/>'
          '<text x="206" y="54" font-size="10" fill="#c0392b" font-weight="bold">P(4,3)</text>'
          '<line x1="200" y1="60" x2="200" y2="120" stroke="#e74c3c" stroke-width="1" stroke-dasharray="3,3"/>'
          '<line x1="200" y1="120" x2="120" y2="120" stroke="#e74c3c" stroke-width="1" stroke-dasharray="3,3"/>'
          '<text x="204" y="134" font-size="9" fill="#718096">横4</text>'
          '<text x="206" y="88" font-size="9" fill="#718096">纵3</text>'
          '</svg>')

# ============ ch3 对称图: 原点(120,120) 每单位20px, P(2,3)=(160,60) P'(2,-3)=(160,180) P''(-2,3)=(80,60) P'''(-2,-3)=(80,180) ============
old_sym = ('<svg viewBox="0 0 220 220" style="width:100%;max-width:200px;height:auto" xmlns="http://www.w3.org/2000/svg">'
           '<line x1="20" y1="110" x2="200" y2="110" stroke="#2d3748" stroke-width="1.5"/>'
           '<line x1="110" y1="200" x2="110" y2="20" stroke="#2d3748" stroke-width="1.5"/>'
           '<circle cx="150" cy="60" r="3.5" fill="#e74c3c"/><text x="156" y="56" font-size="9" fill="#c0392b" font-weight="bold">P(2,3)</text>'
           '<circle cx="150" cy="160" r="3.5" fill="#2f855a"/><text x="133" y="175" font-size="9" fill="#2f855a" font-weight="bold">P′(2,−3)</text>'
           '<circle cx="70" cy="60" r="3.5" fill="#4c51bf"/><text x="12" y="68" font-size="9" fill="#4c51bf" font-weight="bold">P″(−2,3)</text>'
           '<circle cx="70" cy="160" r="3.5" fill="#c05621"/><text x="22" y="175" font-size="9" fill="#c05621" font-weight="bold">P‴(−2,−3)</text>'
           '<line x1="150" y1="60" x2="70" y2="60" stroke="#e2e8f0" stroke-width="1"/>'
           '<line x1="150" y1="60" x2="150" y2="160" stroke="#e2e8f0" stroke-width="1"/>'
           '<line x1="70" y1="160" x2="70" y2="60" stroke="#e2e8f0" stroke-width="1"/>'
           '<line x1="150" y1="160" x2="70" y2="160" stroke="#e2e8f0" stroke-width="1"/>'
           '<text x="204" y="114" font-size="11" fill="#2d3748">x</text>'
           '<text x="114" y="24" font-size="11" fill="#2d3748">y</text>'
           '</svg>')

new_sym = ('<svg viewBox="0 0 240 240" style="width:100%;max-width:210px;height:auto" xmlns="http://www.w3.org/2000/svg">'
           '<line x1="20" y1="120" x2="220" y2="120" stroke="#2d3748" stroke-width="1.5"/>'
           '<line x1="120" y1="220" x2="120" y2="20" stroke="#2d3748" stroke-width="1.5"/>'
           '<circle cx="160" cy="60" r="4" fill="#e74c3c"/><text x="166" y="54" font-size="9" fill="#c0392b" font-weight="bold">P(2,3)</text>'
           '<circle cx="160" cy="180" r="4" fill="#2f855a"/><text x="142" y="196" font-size="9" fill="#2f855a" font-weight="bold">P′(2,−3)</text>'
           '<circle cx="80" cy="60" r="4" fill="#4c51bf"/><text x="14" y="54" font-size="9" fill="#4c51bf" font-weight="bold">P″(−2,3)</text>'
           '<circle cx="80" cy="180" r="4" fill="#c05621"/><text x="20" y="196" font-size="9" fill="#c05621" font-weight="bold">P‴(−2,−3)</text>'
           '<line x1="160" y1="60" x2="80" y2="60" stroke="#e2e8f0" stroke-width="1"/>'
           '<line x1="160" y1="60" x2="160" y2="180" stroke="#e2e8f0" stroke-width="1"/>'
           '<line x1="80" y1="180" x2="80" y2="60" stroke="#e2e8f0" stroke-width="1"/>'
           '<line x1="160" y1="180" x2="80" y2="180" stroke="#e2e8f0" stroke-width="1"/>'
           '<text x="224" y="124" font-size="11" fill="#2d3748">x</text>'
           '<text x="124" y="24" font-size="11" fill="#2d3748">y</text>'
           '</svg>')

# ============ ch4 直线图 y=2x−1: 原点(120,110) 每单位30px。点(0,-1)=(120,140),(1/2,0)=(135,110)。直线过(105,170)&(165,50) ============
old_line = ('<svg viewBox="0 0 240 220" style="width:100%;max-width:220px;height:auto" xmlns="http://www.w3.org/2000/svg">'
            '<line x1="30" y1="110" x2="210" y2="110" stroke="#2d3748" stroke-width="1.5"/>'
            '<line x1="120" y1="200" x2="120" y2="20" stroke="#2d3748" stroke-width="1.5"/>'
            '<polygon points="210,110 202,106 202,114" fill="#2d3748"/>'
            '<polygon points="120,20 116,28 124,28" fill="#2d3748"/>'
            '<text x="214" y="114" font-size="11" fill="#2d3748">x</text><text x="124" y="24" font-size="11" fill="#2d3748">y</text>'
            '<line x1="30" y1="190" x2="200" y2="50" stroke="#e74c3c" stroke-width="2"/>'
            '<circle cx="120" cy="110" r="3" fill="#e74c3c"/><text x="94" y="122" font-size="10" fill="#718096">(0,0)</text>'
            '<circle cx="155" cy="85" r="3" fill="#e74c3c"/><text x="161" y="81" font-size="10" fill="#c0392b" font-weight="bold">y=2x−1</text>'
            '<circle cx="120" cy="138" r="3" fill="#4c51bf"/><text x="126" y="142" font-size="10" fill="#4c51bf">(0,−1)</text>'
            '<circle cx="135" cy="110" r="3" fill="#2f855a"/><text x="150" y="122" font-size="10" fill="#2f855a">(1/2,0)</text>'
            '</svg>')

new_line = ('<svg viewBox="0 0 240 220" style="width:100%;max-width:220px;height:auto" xmlns="http://www.w3.org/2000/svg">'
            '<line x1="30" y1="110" x2="210" y2="110" stroke="#2d3748" stroke-width="1.5"/>'
            '<line x1="120" y1="200" x2="120" y2="20" stroke="#2d3748" stroke-width="1.5"/>'
            '<polygon points="210,110 202,106 202,114" fill="#2d3748"/>'
            '<polygon points="120,20 116,28 124,28" fill="#2d3748"/>'
            '<text x="214" y="114" font-size="11" fill="#2d3748">x</text><text x="124" y="24" font-size="11" fill="#2d3748">y</text>'
            '<line x1="105" y1="170" x2="165" y2="50" stroke="#e74c3c" stroke-width="2"/>'
            '<circle cx="120" cy="110" r="3" fill="#e74c3c"/><text x="94" y="124" font-size="10" fill="#718096">(0,0)</text>'
            '<circle cx="168" cy="52" r="3" fill="#e74c3c"/><text x="174" y="48" font-size="10" fill="#c0392b" font-weight="bold">y=2x−1</text>'
            '<circle cx="120" cy="140" r="3.5" fill="#4c51bf"/><text x="126" y="144" font-size="10" fill="#4c51bf">(0,−1)</text>'
            '<circle cx="135" cy="110" r="3.5" fill="#2f855a"/><text x="148" y="122" font-size="10" fill="#2f855a">(1/2,0)</text>'
            '</svg>')

# ============ ch4 k三线图: 原点(120,100) 每单位20px。y=2x: (90,160)-(160,20); y=−2x: (90,40)-(160,180); y=x: (90,130)-(160,60) ============
old_k = ('<svg viewBox="0 0 240 200" style="width:100%;max-width:220px;height:auto" xmlns="http://www.w3.org/2000/svg">'
         '<line x1="30" y1="100" x2="210" y2="100" stroke="#2d3748" stroke-width="1.5"/>'
         '<line x1="120" y1="180" x2="120" y2="20" stroke="#2d3748" stroke-width="1.5"/>'
         '<text x="214" y="104" font-size="11" fill="#2d3748">x</text><text x="124" y="24" font-size="11" fill="#2d3748">y</text>'
         '<line x1="40" y1="140" x2="200" y2="60" stroke="#48bb78" stroke-width="2"/>'
         '<text x="168" y="52" font-size="10" fill="#2f855a" font-weight="bold">y=2x (k&gt;0)</text>'
         '<line x1="200" y1="140" x2="40" y2="60" stroke="#e74c3c" stroke-width="2"/>'
         '<text x="30" y="112" font-size="10" fill="#c0392b" font-weight="bold">y=−2x (k&lt;0)</text>'
         '<line x1="60" y1="130" x2="180" y2="70" stroke="#667eea" stroke-width="2"/>'
         '<text x="118" y="140" font-size="10" fill="#4c51bf" font-weight="bold">y=x (较缓)</text>'
         '</svg>')

new_k = ('<svg viewBox="0 0 240 200" style="width:100%;max-width:220px;height:auto" xmlns="http://www.w3.org/2000/svg">'
         '<line x1="30" y1="100" x2="210" y2="100" stroke="#2d3748" stroke-width="1.5"/>'
         '<line x1="120" y1="180" x2="120" y2="20" stroke="#2d3748" stroke-width="1.5"/>'
         '<text x="214" y="104" font-size="11" fill="#2d3748">x</text><text x="124" y="24" font-size="11" fill="#2d3748">y</text>'
         '<line x1="90" y1="160" x2="160" y2="20" stroke="#48bb78" stroke-width="2"/>'
         '<text x="162" y="34" font-size="10" fill="#2f855a" font-weight="bold">y=2x (k&gt;0)</text>'
         '<line x1="90" y1="40" x2="160" y2="180" stroke="#e74c3c" stroke-width="2"/>'
         '<text x="38" y="168" font-size="10" fill="#c0392b" font-weight="bold">y=−2x (k&lt;0)</text>'
         '<line x1="90" y1="130" x2="160" y2="60" stroke="#667eea" stroke-width="2"/>'
         '<text x="136" y="82" font-size="10" fill="#4c51bf" font-weight="bold">y=x (较缓)</text>'
         '</svg>')

# ============ ch4 交点图: y=x+1: (90,110)-(180,20); y=−x+3: (120,20)-(210,110); 交点(1,2)=(150,50) ============
old_int4 = ('<svg viewBox="0 0 240 220" style="width:100%;max-width:220px;height:auto" xmlns="http://www.w3.org/2000/svg">'
            '<line x1="30" y1="110" x2="210" y2="110" stroke="#2d3748" stroke-width="1.5"/>'
            '<line x1="120" y1="200" x2="120" y2="20" stroke="#2d3748" stroke-width="1.5"/>'
            '<text x="214" y="114" font-size="11" fill="#2d3748">x</text><text x="124" y="24" font-size="11" fill="#2d3748">y</text>'
            '<line x1="40" y1="170" x2="200" y2="50" stroke="#e74c3c" stroke-width="2"/>'
            '<text x="160" y="60" font-size="10" fill="#c0392b" font-weight="bold">y=x+1</text>'
            '<line x1="40" y1="50" x2="200" y2="170" stroke="#48bb78" stroke-width="2"/>'
            '<text x="40" y="60" font-size="10" fill="#2f855a" font-weight="bold">y=−x+3</text>'
            '<circle cx="120" cy="110" r="4" fill="#e74c3c"/>'
            '<text x="104" y="100" font-size="10" fill="#c0392b" font-weight="bold">交点(1,2)</text>'
            '</svg>')

new_int4 = ('<svg viewBox="0 0 240 220" style="width:100%;max-width:220px;height:auto" xmlns="http://www.w3.org/2000/svg">'
            '<line x1="30" y1="110" x2="210" y2="110" stroke="#2d3748" stroke-width="1.5"/>'
            '<line x1="120" y1="200" x2="120" y2="20" stroke="#2d3748" stroke-width="1.5"/>'
            '<text x="214" y="114" font-size="11" fill="#2d3748">x</text><text x="124" y="24" font-size="11" fill="#2d3748">y</text>'
            '<line x1="90" y1="110" x2="180" y2="20" stroke="#e74c3c" stroke-width="2"/>'
            '<text x="164" y="38" font-size="10" fill="#c0392b" font-weight="bold">y=x+1</text>'
            '<line x1="120" y1="20" x2="210" y2="110" stroke="#48bb78" stroke-width="2"/>'
            '<text x="56" y="38" font-size="10" fill="#2f855a" font-weight="bold">y=−x+3</text>'
            '<circle cx="150" cy="50" r="4" fill="#e74c3c"/>'
            '<text x="156" y="68" font-size="10" fill="#c0392b" font-weight="bold">交点(1,2)</text>'
            '</svg>')

patch_file('math8_ch2_interactive.html', [(old_num, new_num)], 'ch2 数轴')
patch_file('math8_ch3_interactive.html', [(old_cs, new_cs), (old_sym, new_sym)], 'ch3 坐标/对称')
patch_file('math8_ch4_interactive.html', [(old_line, new_line), (old_k, new_k), (old_int4, new_int4)], 'ch4 直线/k/交点')
print('ALL DONE')
