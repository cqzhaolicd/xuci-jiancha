# -*- coding: utf-8 -*-
"""升级 math8_ch2(实数) + math8_ch3(坐标系) 知识图谱:配图+定理说明"""
import io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def patch_file(fname, replacements, label):
    p = fname
    h = open(p, encoding='utf-8').read()
    for old, new in replacements:
        assert old in h, f'{label}: 未找到 -> {old[:60]}'
        h = h.replace(old, new, 1)
    open(p, 'w', encoding='utf-8').write(h)
    print(f'{label} 完成 ({len(replacements)} 处)')

# ================= ch2 实数 =================
# ① 无理数 卡升级
ch2_old0 = '<div class="k-item"><h4>无理数</h4><p>无限不循环小数称为无理数，如π、√2、0.1010010001…。有理数+无理数=实数。</p></div>'
ch2_new0 = ('<div class="k-item"><h4>无理数</h4><p><strong>定义</strong>：无限不循环小数叫无理数，如 π、√2、√3、0.1010010001…。<br>'
            '<strong>快速判断</strong>：①带根号且开不尽（√2、√5、√7…）；②含 π 的式子（π、2π、π/2）；③人为构造的无限不循环小数。<br>'
            '<strong>易混</strong>：√4=2 是有理数（开得尽）；22/7、3.14 是有限小数/分数 → 有理数；1.232323… 循环 → 有理数。<br>'
            '<strong>关系</strong>：有理数 + 无理数 = 实数，两者互不包含。</p></div>')

# ② 实数的分类 卡升级 + 树状图
ch2_old1 = '<div class="k-item"><h4>实数的分类</h4><p>实数=有理数（整数/分数）+无理数。有理数=有限小数/无限循环小数。</p></div>'
ch2_new1 = ('<div class="k-item"><h4>实数的分类</h4><p><strong>按定义分</strong>：实数 = 有理数 + 无理数。<br>'
            '<strong>有理数</strong>：整数（正整数/0/负整数）+ 分数（有限小数、无限循环小数）；<br>'
            '<strong>无理数</strong>：无限不循环小数。<br>'
            '<strong>按正负分</strong>：正实数、0、负实数（正负对称）。</p>'
            '<div style="text-align:center;margin-top:.4rem">'
            '<svg viewBox="0 0 300 150" style="width:100%;max-width:280px;height:auto" xmlns="http://www.w3.org/2000/svg">'
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
            '</svg></div></div>')

# ③ 估算 卡升级 + 数轴图
ch2_old2 = '<div class="k-item"><h4>估算</h4><p>用夹逼法估算无理数范围：如√2在1和2之间，√5在2和3之间。</p></div>'
ch2_new2 = ('<div class="k-item"><h4>估算</h4><p><strong>夹逼法</strong>：找两个相邻整数夹住无理数。<br>'
            '①找平方邻近：√2 介于 √1=1 和 √4=2 之间 → 1&lt;√2&lt;2；√5 介于 √4=2 和 √9=3 之间 → 2&lt;√5&lt;3。<br>'
            '②精确到 0.1：再试 1.4²=1.96、1.5²=2.25，1.4²&lt;2&lt;1.5² → 1.4&lt;√2&lt;1.5。<br>'
            '<strong>记忆</strong>：√2≈1.414、√3≈1.732、√5≈2.236、√7≈2.646。</p>'
            '<div style="text-align:center;margin-top:.4rem">'
            '<svg viewBox="0 0 300 70" style="width:100%;max-width:280px;height:auto" xmlns="http://www.w3.org/2000/svg">'
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
            '</svg></div></div>')

patch_file('math8_ch2_interactive.html',
           [(ch2_old0, ch2_new0), (ch2_old1, ch2_new1), (ch2_old2, ch2_new2)],
           'ch2 实数')

# ================= ch3 坐标系 =================
# ① 平面直角坐标系 卡升级 + 坐标系图
ch3_old0 = '<div class="k-item"><h4>平面直角坐标系</h4><p>两条互相垂直且有公共原点的数轴组成。水平=横轴x（向右为正），竖直=纵轴y（向上为正）。</p></div>'
ch3_new0 = ('<div class="k-item"><h4>平面直角坐标系</h4><p><strong>组成</strong>：两条互相垂直且有公共原点的数轴。<br>'
            '<strong>横轴 x</strong>：水平，向右为正，向左为负；<strong>纵轴 y</strong>：竖直，向上为正，向下为负。<br>'
            '<strong>原点 O</strong>：两轴交点，坐标 (0,0)。<br>'
            '<strong>作用</strong>：用有序数对 (x,y) 表示平面内点的位置（x 先横后纵）。<br>'
            '<strong>记法</strong>：P(a,b) 中 a 是横坐标、b 是纵坐标，中间逗号，括号括起。</p>'
            '<div style="text-align:center;margin-top:.4rem">'
            '<svg viewBox="0 0 220 220" style="width:100%;max-width:200px;height:auto" xmlns="http://www.w3.org/2000/svg">'
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
            '</svg></div></div>')

# ② 象限划分 卡升级 + 象限图
ch3_old1 = '<div class="k-item"><h4>象限划分</h4><p>第一象限(+,+)，第二(-,+)，第三(-,-)，第四(+,-)。坐标轴上的点不属于任何象限。</p></div>'
ch3_new1 = ('<div class="k-item"><h4>象限划分</h4><p><strong>定义</strong>：x 轴和 y 轴把平面分成四个区域，按逆时针依次叫第一、二、三、四象限。<br>'
            '<strong>符号规律</strong>：第一象限 (+,+)；第二象限 (−,+)；第三象限 (−,−)；第四象限 (+,−)。<br>'
            '<strong>关键</strong>：坐标轴上的点（x 轴、y 轴、原点）<strong>不属于任何象限</strong>。<br>'
            '<strong>判断技巧</strong>：看符号定象限——正正一、负正二、负负三、正负四。</p>'
            '<div style="text-align:center;margin-top:.4rem">'
            '<svg viewBox="0 0 220 220" style="width:100%;max-width:200px;height:auto" xmlns="http://www.w3.org/2000/svg">'
            '<line x1="20" y1="110" x2="200" y2="110" stroke="#2d3748" stroke-width="1.5"/>'
            '<line x1="110" y1="200" x2="110" y2="20" stroke="#2d3748" stroke-width="1.5"/>'
            '<rect x="110" y="20" width="90" height="90" fill="#48bb7818"/>'
            '<rect x="20" y="20" width="90" height="90" fill="#e74c3c18"/>'
            '<rect x="20" y="110" width="90" height="90" fill="#ed893618"/>'
            '<rect x="110" y="110" width="90" height="90" fill="#667eea18"/>'
            '<text x="155" y="70" font-size="11" fill="#2f855a" font-weight="bold" text-anchor="middle">一(+,+)</text>'
            '<text x="65" y="70" font-size="11" fill="#c0392b" font-weight="bold" text-anchor="middle">二(-,+)</text>'
            '<text x="65" y="160" font-size="11" fill="#c05621" font-weight="bold" text-anchor="middle">三(-,-)</text>'
            '<text x="155" y="160" font-size="11" fill="#4c51bf" font-weight="bold" text-anchor="middle">四(+,-)</text>'
            '<text x="204" y="114" font-size="11" fill="#2d3748">x</text>'
            '<text x="114" y="24" font-size="11" fill="#2d3748">y</text>'
            '<text x="96" y="126" font-size="10" fill="#718096">O</text>'
            '</svg></div></div>')

# ③ 点的坐标 卡升级 + 图示(并入特殊点升级)
ch3_old2 = '<div class="k-item"><h4>点的坐标</h4><p>有序数对(x,y)：x是横坐标（到y轴距离），y是纵坐标（到x轴距离）。</p></div>'
ch3_new2 = ('<div class="k-item"><h4>点的坐标</h4><p><strong>有序数对 (x,y)</strong>：x 是横坐标（先写），y 是纵坐标（后写）。<br>'
            '<strong>几何意义</strong>：|x| = 点到 y 轴的距离，|y| = 点到 x 轴的距离。<br>'
            '<strong>写坐标步骤</strong>：①过点分别作 x 轴、y 轴的垂线；②垂足在 x 轴上读数=横坐标，在 y 轴上读数=纵坐标；③写成 (x,y)。<br>'
            '<strong>注意</strong>：(2,3) 与 (3,2) 是两个不同的点——顺序不能交换！</p></div>')

# ④ 对称三卡 升级 + 综合对称图
ch3_old3 = '<div class="k-item"><h4>关于x轴对称</h4><p>(x,y)→(x,-y)：横坐标不变，纵坐标互为相反数。</p></div>'
ch3_new3 = ('<div class="k-item"><h4>关于x轴对称</h4><p><strong>规律</strong>：(x,y) → (x,−y)。横坐标不变，纵坐标互为相反数。<br>'
            '例：P(2,3) 关于 x 轴对称 → P′(2,−3)。<br>'
            '<strong>理解</strong>：关于 x 轴对称即"上下翻"，x 不动、y 变号。</p></div>')
ch3_old4 = '<div class="k-item"><h4>关于y轴对称</h4><p>(x,y)→(-x,y)：纵坐标不变，横坐标互为相反数。</p></div>'
ch3_new4 = ('<div class="k-item"><h4>关于y轴对称</h4><p><strong>规律</strong>：(x,y) → (−x,y)。纵坐标不变，横坐标互为相反数。<br>'
            '例：P(2,3) 关于 y 轴对称 → P″(−2,3)。<br>'
            '<strong>理解</strong>：关于 y 轴对称即"左右翻"，y 不动、x 变号。</p></div>')
ch3_old5 = '<div class="k-item"><h4>关于原点对称</h4><p>(x,y)→(-x,-y)：横纵坐标都互为相反数。</p></div>'
ch3_new5 = ('<div class="k-item"><h4>关于原点对称</h4><p><strong>规律</strong>：(x,y) → (−x,−y)。横、纵坐标都变相反数。<br>'
            '例：P(2,3) 关于原点对称 → P‴(−2,−3)。<br>'
            '<strong>一句话记忆</strong>：关于谁对称，谁不变，另一个变号；关于原点对称，两个都变号。<br>'
            '<strong>坐标轴上的对称</strong>：x 轴上点关于 y 轴对称 = 关于原点对称。</p>'
            '<div style="text-align:center;margin-top:.4rem">'
            '<svg viewBox="0 0 220 220" style="width:100%;max-width:200px;height:auto" xmlns="http://www.w3.org/2000/svg">'
            '<line x1="20" y1="110" x2="200" y2="110" stroke="#2d3748" stroke-width="1.5"/>'
            '<line x1="110" y1="200" x2="110" y2="20" stroke="#2d3748" stroke-width="1.5"/>'
            '<circle cx="150" cy="60" r="3.5" fill="#e74c3c"/><text x="156" y="56" font-size="9" fill="#c0392b" font-weight="bold">P(2,3)</text>'
            '<circle cx="150" cy="160" r="3.5" fill="#2f855a"/><text x="133" y="175" font-size="9" fill="#2f855a" font-weight="bold">P′(2,−3)</text>'
            '<circle cx="70" cy="60" r="3.5" fill="#4c51bf"/><text x="20" y="56" font-size="9" fill="#4c51bf" font-weight="bold">P″(−2,3)</text>'
            '<circle cx="70" cy="160" r="3.5" fill="#c05621"/><text x="22" y="175" font-size="9" fill="#c05621" font-weight="bold">P‴(−2,−3)</text>'
            '<line x1="150" y1="60" x2="70" y2="60" stroke="#e2e8f0" stroke-width="1"/>'
            '<line x1="150" y1="60" x2="150" y2="160" stroke="#e2e8f0" stroke-width="1"/>'
            '<line x1="70" y1="160" x2="70" y2="60" stroke="#e2e8f0" stroke-width="1"/>'
            '<line x1="150" y1="160" x2="70" y2="160" stroke="#e2e8f0" stroke-width="1"/>'
            '<text x="204" y="114" font-size="11" fill="#2d3748">x</text>'
            '<text x="114" y="24" font-size="11" fill="#2d3748">y</text>'
            '</svg></div></div>')

# ⑤ 坐标与图形 升级
ch3_old6 = '<div class="k-item"><h4>坐标与图形</h4><p>用坐标表示位置（地图定位）；平行于坐标轴的线段长度：水平=|x₁-x₂|，竖直=|y₁-y₂|。</p></div>'
ch3_new6 = ('<div class="k-item"><h4>坐标与图形</h4><p><strong>两点间距离（平行于轴）</strong>：水平距离 = |x₁−x₂|；竖直距离 = |y₁−y₂|。<br>'
            '<strong>斜线段</strong>：不在同一直线上时用勾股定理求距离：d=√[(x₁−x₂)²+(y₁−y₂)²]。<br>'
            '<strong>中点坐标</strong>：两端点中点 ((x₁+x₂)/2, (y₁+y₂)/2)。<br>'
            '<strong>应用</strong>：地图定位（经纬度思想）、三角形面积（底×高，高为到轴距离）。<br>'
            '例：A(1,2)、B(5,2) 水平距离=4；A(1,2)、C(1,6) 竖直距离=4。</p></div>')

patch_file('math8_ch3_interactive.html',
           [(ch3_old0, ch3_new0), (ch3_old1, ch3_new1), (ch3_old2, ch3_new2),
            (ch3_old3, ch3_new3), (ch3_old4, ch3_new4), (ch3_old5, ch3_new5),
            (ch3_old6, ch3_new6)],
           'ch3 坐标系')
print('ALL DONE')
