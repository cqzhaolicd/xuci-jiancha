# -*- coding: utf-8 -*-
"""给 math8_ch1 赵爽弦图·进阶 知识卡内联 SVG 图（外弦图+内弦图 并排）"""
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

P = 'math8_ch1_interactive.html'
h = open(P, encoding='utf-8').read()

old = ('<div class="k-item"><h4>赵爽弦图·进阶</h4><p><strong>构图</strong>：四个全等直角三角形（直角边a、b，斜边c）拼成正方形，用<strong>等面积法</strong>证勾股定理。<br>'
       '<strong>外弦图</strong>（三角在外）：大正方形边长 <strong>a+b</strong>，中间小正方形边长 <strong>c</strong>（由斜边构成），S大=(a+b)²=c²+4×½ab → a²+b²=c²。<br>'
       '<strong>内弦图</strong>（三角在内）：大正方形边长 <strong>c</strong>（由斜边构成），中间小正方形边长 <strong>|a−b|</strong>，c²=(a−b)²+4×½ab → a²+b²=c²。<br>'
       '<strong>历史</strong>：三国·赵爽为《周髀算经》作注时创制，是最早的勾股定理严格证明之一。<br>'
       '<strong>考法</strong>：①给面积反求边长（列方程）；②弦图+坐标系求点坐标。</p></div>')
assert old in h, '知识卡未找到'

svg = '''<p><strong>构图</strong>：四个全等直角三角形（直角边a、b，斜边c）拼成正方形，用<strong>等面积法</strong>证勾股定理。<br>
<strong>外弦图</strong>（三角在外）：大正方形边长 <strong>a+b</strong>，中间小正方形边长 <strong>c</strong>（由斜边构成），S大=(a+b)²=c²+4×½ab → a²+b²=c²。<br>
<strong>内弦图</strong>（三角在内）：大正方形边长 <strong>c</strong>（由斜边构成），中间小正方形边长 <strong>|a−b|</strong>，c²=(a−b)²+4×½ab → a²+b²=c²。<br>
<strong>历史</strong>：三国·赵爽为《周髀算经》作注时创制，是最早的勾股定理严格证明之一。<br>
<strong>考法</strong>：①给面积反求边长（列方程）；②弦图+坐标系求点坐标。</p>
<div style="text-align:center;margin-top:.5rem">
<svg viewBox="0 0 660 330" style="width:100%;max-width:460px;height:auto" xmlns="http://www.w3.org/2000/svg">
  <!-- 外弦图：大正方形 a+b=7，三角在外，小正方形 c=5 -->
  <rect x="20" y="20" width="280" height="280" fill="none" stroke="#e74c3c" stroke-width="2.5"/>
  <polygon points="20,20 180,20 20,140" fill="#e74c3c22" stroke="#e74c3c" stroke-width="1.6"/>
  <polygon points="300,20 180,20 300,180" fill="#e74c3c22" stroke="#e74c3c" stroke-width="1.6"/>
  <polygon points="300,300 140,300 300,180" fill="#e74c3c22" stroke="#e74c3c" stroke-width="1.6"/>
  <polygon points="20,300 140,300 20,180" fill="#e74c3c22" stroke="#e74c3c" stroke-width="1.6"/>
  <polygon points="180,20 300,180 140,300 20,180" fill="#48bb7822" stroke="#48bb78" stroke-width="2.2"/>
  <text x="100" y="42" font-size="16" fill="#c0392b" font-weight="bold" text-anchor="middle">a</text>
  <text x="32" y="88" font-size="16" fill="#c0392b" font-weight="bold">b</text>
  <text x="160" y="175" font-size="15" fill="#2f855a" font-weight="bold" text-anchor="middle">c</text>
  <text x="160" y="318" font-size="14" fill="#555" text-anchor="middle">外弦图：大正方形边长 a+b，中间小正方形边长 c</text>
  <!-- 分隔线 -->
  <line x1="340" y1="20" x2="340" y2="300" stroke="#e2e8f0" stroke-width="1.5" stroke-dasharray="4,4"/>
  <!-- 内弦图：大正方形 c=5，三角在内，小正方形 |a-b|=1（右移 340） -->
  <rect x="375" y="35" width="250" height="250" fill="none" stroke="#e74c3c" stroke-width="2.5"/>
  <polygon points="375,35 625,35 465,155" fill="#e74c3c22" stroke="#e74c3c" stroke-width="1.6"/>
  <polygon points="625,35 625,285 505,125" fill="#e74c3c22" stroke="#e74c3c" stroke-width="1.6"/>
  <polygon points="625,285 375,285 535,165" fill="#e74c3c22" stroke="#e74c3c" stroke-width="1.6"/>
  <polygon points="375,285 375,35 495,195" fill="#e74c3c22" stroke="#e74c3c" stroke-width="1.6"/>
  <polygon points="465,155 505,125 535,165 495,195" fill="#48bb7822" stroke="#48bb78" stroke-width="2.2"/>
  <text x="500" y="28" font-size="16" fill="#c0392b" font-weight="bold" text-anchor="middle">c</text>
  <text x="545" y="100" font-size="14" fill="#c0392b" font-weight="bold">a</text>
  <text x="420" y="100" font-size="14" fill="#c0392b" font-weight="bold">b</text>
  <text x="500" y="172" font-size="14" fill="#2f855a" font-weight="bold" text-anchor="middle">a−b</text>
  <text x="500" y="318" font-size="14" fill="#555" text-anchor="middle">内弦图：大正方形边长 c，中间小正方形边长 |a−b|</text>
</svg>
</div></div>'''

h = h.replace(old, svg)
open(P, 'w', encoding='utf-8').write(h)
print('SVG 插入 OK')

# 校验
h2 = open(P, encoding='utf-8').read()
print('外弦图标签:', h2.count('外弦图：大正方形边长'))
print('内弦图标签:', h2.count('内弦图：大正方形边长'))
print('svg 数量:', h2.count('<svg'))
print('k-item 数量:', h2.count('k-item'))
