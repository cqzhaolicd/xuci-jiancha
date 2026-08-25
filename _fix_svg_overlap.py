# -*- coding: utf-8 -*-
"""修复数学8页 SVG 文字重叠问题:
1. ch2 分类树: 整数/分数重叠 → 重新布局加宽
2. ch4 k三线图: 两标签同行重叠 → 错开布局
3. ch5 解的判断图: 超出viewBox → 左移
4. ch3 对称图: P″贴边 → 微调
"""
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def patch_file(fname, replacements, label):
    h = open(fname, encoding='utf-8').read()
    for old, new in replacements:
        assert old in h, f'{label}: 未找到 -> {old[:80]}'
        h = h.replace(old, new, 1)
    open(fname, 'w', encoding='utf-8').write(h)
    print(f'{label} 完成 ({len(replacements)} 处)')

# ============ 1. ch2 分类树状图 重布局 ============
old_tree = ('<svg viewBox="0 0 300 150" style="width:100%;max-width:280px;height:auto" xmlns="http://www.w3.org/2000/svg">'
            '<rect x="8" y="8" width="284" height="134" rx="8" fill="#f7fafc" stroke="#e2e8f0"/>'
            '<text x="150" y="26" font-size="12" fill="#e74c3c" font-weight="bold" text-anchor="middle">实数</text>'
            '<line x1="150" y1="32" x2="80" y2="55" stroke="#718096" stroke-width="1"/><line x1="150" y1="32" x2="220" y2="55" stroke="#718096" stroke-width="1"/>'
            '<text x="70" y="70" font-size="11" fill="#2d3748" font-weight="bold" text-anchor="middle">有理数</text>'
            '<line x1="60" y1="78" x2="60" y2="95" stroke="#718096" stroke-width="1"/><line x1="80" y1="78" x2="80" y2="95" stroke="#718096" stroke-width="1"/>'
            '<text x="50" y="110" font-size="10" fill="#4a5568" text-anchor="middle">整数</text>'
            '<text x="90" y="110" font-size="10" fill="#4a5568" text-anchor="middle">分数(有限/循环)</text>'
            '<text x="220" y="70" font-size="11" fill="#c0392b" font-weight="bold" text-anchor="middle">无理数</text>'
            '<line x1="220" y1="78" x2="220" y2="95" stroke="#718096" stroke-width="1"/>'
            '<text x="220" y="110" font-size="10" fill="#c0392b" text-anchor="middle">无限不循环</text>'
            '<text x="220" y="124" font-size="10" fill="#718096" text-anchor="middle">π、√2、√3…</text>'
            '</svg>')

new_tree = ('<svg viewBox="0 0 300 170" style="width:100%;max-width:280px;height:auto" xmlns="http://www.w3.org/2000/svg">'
            '<rect x="8" y="8" width="284" height="154" rx="8" fill="#f7fafc" stroke="#e2e8f0"/>'
            '<text x="150" y="28" font-size="12" fill="#e74c3c" font-weight="bold" text-anchor="middle">实数</text>'
            '<line x1="150" y1="34" x2="75" y2="56" stroke="#718096" stroke-width="1"/><line x1="150" y1="34" x2="225" y2="56" stroke="#718096" stroke-width="1"/>'
            '<text x="70" y="74" font-size="11" fill="#2d3748" font-weight="bold" text-anchor="middle">有理数</text>'
            '<text x="230" y="74" font-size="11" fill="#c0392b" font-weight="bold" text-anchor="middle">无理数</text>'
            '<line x1="55" y1="80" x2="55" y2="98" stroke="#718096" stroke-width="1"/><line x1="85" y1="80" x2="85" y2="98" stroke="#718096" stroke-width="1"/>'
            '<line x1="230" y1="80" x2="230" y2="98" stroke="#718096" stroke-width="1"/>'
            '<text x="42" y="116" font-size="10" fill="#4a5568" text-anchor="middle">整数</text>'
            '<text x="100" y="116" font-size="10" fill="#4a5568" text-anchor="middle">分数</text>'
            '<text x="55" y="132" font-size="9" fill="#a0aec0" text-anchor="middle">(正整数/0/负整数)</text>'
            '<text x="100" y="132" font-size="9" fill="#a0aec0" text-anchor="middle">(有限/循环小数)</text>'
            '<text x="230" y="116" font-size="10" fill="#c0392b" text-anchor="middle">无限不循环</text>'
            '<text x="230" y="136" font-size="10" fill="#718096" text-anchor="middle">π、√2、√3…</text>'
            '</svg>')

# ============ 2. ch4 k三线图 标签错开 ============
old_k = ('<line x1="40" y1="140" x2="200" y2="60" stroke="#48bb78" stroke-width="2"/>'
         '<text x="150" y="80" font-size="10" fill="#2f855a" font-weight="bold">y=2x (k&gt;0)</text>'
         '<line x1="200" y1="140" x2="40" y2="60" stroke="#e74c3c" stroke-width="2"/>'
         '<text x="52" y="80" font-size="10" fill="#c0392b" font-weight="bold">y=−2x (k&lt;0)</text>'
         '<line x1="60" y1="130" x2="180" y2="70" stroke="#667eea" stroke-width="2"/>'
         '<text x="98" y="128" font-size="10" fill="#4c51bf" font-weight="bold">y=x (较缓)</text>')

new_k = ('<line x1="40" y1="140" x2="200" y2="60" stroke="#48bb78" stroke-width="2"/>'
         '<text x="168" y="52" font-size="10" fill="#2f855a" font-weight="bold">y=2x (k&gt;0)</text>'
         '<line x1="200" y1="140" x2="40" y2="60" stroke="#e74c3c" stroke-width="2"/>'
         '<text x="30" y="112" font-size="10" fill="#c0392b" font-weight="bold">y=−2x (k&lt;0)</text>'
         '<line x1="60" y1="130" x2="180" y2="70" stroke="#667eea" stroke-width="2"/>'
         '<text x="118" y="140" font-size="10" fill="#4c51bf" font-weight="bold">y=x (较缓)</text>')

# ============ 3. ch5 解的判断图 超出viewBox ============
old_judge = '<text x="295" y="102" font-size="9" fill="#718096">重合 → 无数解</text>'
new_judge = '<text x="282" y="102" font-size="9" fill="#718096">重合→无数解</text>'

# ============ 4. ch3 对称图 P″ 微调 ============
old_sym = '<circle cx="70" cy="60" r="3.5" fill="#4c51bf"/><text x="20" y="56" font-size="9" fill="#4c51bf" font-weight="bold">P″(−2,3)</text>'
new_sym = '<circle cx="70" cy="60" r="3.5" fill="#4c51bf"/><text x="12" y="68" font-size="9" fill="#4c51bf" font-weight="bold">P″(−2,3)</text>'

patch_file('math8_ch2_interactive.html', [(old_tree, new_tree)], 'ch2 树状图')
patch_file('math8_ch4_interactive.html', [(old_k, new_k)], 'ch4 k三线图')
patch_file('math8_ch5_interactive.html', [(old_judge, new_judge)], 'ch5 解的判断')
patch_file('math8_ch3_interactive.html', [(old_sym, new_sym)], 'ch3 对称图')
print('ALL DONE')
