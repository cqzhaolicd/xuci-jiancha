# -*- coding: utf-8 -*-
"""升级 math8_ch4(一次函数) + math8_ch5(二元一次方程组) 知识图谱:配图+定理说明"""
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

# ================= ch4 一次函数 =================
# ① 函数概念 升级
ch4_old0 = '<div class="k-item"><h4>函数概念</h4><p>一般地，在一个变化过程中有两个变量x、y，对于x的每一个确定值，y都有唯一确定的值与之对应，y是x的函数。</p></div>'
ch4_new0 = ('<div class="k-item"><h4>函数概念</h4><p><strong>定义</strong>：在一个变化过程中有两个变量 x、y，对于 x 的每一个确定值，y 都有<strong>唯一确定</strong>的值与之对应，则 y 是 x 的函数，x 叫自变量。<br>'
            '<strong>三要素</strong>：①两个变量；②x 有范围（定义域）；③y 唯一对应（一对多不行）。<br>'
            '<strong>判断函数</strong>：给一个 x，看 y 是否唯一——y²=x 不是函数（一个 x 对应 ±y），y=2x+1 是函数。<br>'
            '<strong>表示方法</strong>：解析式法（y=kx+b）、列表法、图象法。</p></div>')

# ② 一次函数 升级(明示这是"函数定义")
ch4_old1 = '<div class="k-item"><h4>一次函数</h4><p>形如y=kx+b（k、b为常数，k≠0）的函数。当b=0时，y=kx是正比例函数。</p></div>'
ch4_new1 = ('<div class="k-item"><h4>一次函数</h4><p><strong>定义</strong>：形如 <strong>y=kx+b</strong>（k、b 为常数，<strong>k≠0</strong>）的函数叫一次函数。<br>'
            '<strong>正比例函数</strong>：当 b=0 时，y=kx（k≠0），它是特殊的一次函数（必过原点）。<br>'
            '<strong>判断</strong>：①x 的次数是 1；②x 的系数 k≠0；③式子中不能有 x²、1/x、|x| 等。<br>'
            '<strong>易混</strong>：y=2 不是一次函数（无 x 项）；y=1/x 不是（x 次数 -1）；y=3x² 不是（次数 2）。<br>'
            '<strong>关系</strong>：正比例函数 ⊂ 一次函数 ⊂ 函数。</p></div>')

# ③ 一次函数图象 升级 + 直线图
ch4_old2 = '<div class="k-item"><h4>一次函数图象</h4><p>是一条直线。k=斜率（倾斜程度），b=与y轴交点纵坐标(0,b)。画图方法：两点确定一条直线，常取与y轴交点(0,b)和与x轴交点(-b/k,0)连线。</p></div>'
ch4_new2 = ('<div class="k-item"><h4>一次函数图象</h4><p><strong>图象</strong>：一次函数 y=kx+b 的图象是一条<strong>直线</strong>。<br>'
            '<strong>两点画图法</strong>：直线由两点确定——常取①与 y 轴交点 (0,b)；②与 x 轴交点 (−b/k, 0)，连线即可。<br>'
            '<strong>k = 斜率</strong>：决定倾斜方向与陡峭程度；<strong>b = 截距</strong>：与 y 轴交点纵坐标。<br>'
            '<strong>例</strong>：y=2x−1，取 (0,−1) 和 (1/2,0) 连线。</p>'
            '<div style="text-align:center;margin-top:.4rem">'
            '<svg viewBox="0 0 240 220" style="width:100%;max-width:220px;height:auto" xmlns="http://www.w3.org/2000/svg">'
            '<line x1="30" y1="110" x2="210" y2="110" stroke="#2d3748" stroke-width="1.5"/>'
            '<line x1="120" y1="200" x2="120" y2="20" stroke="#2d3748" stroke-width="1.5"/>'
            '<polygon points="210,110 202,106 202,114" fill="#2d3748"/>'
            '<polygon points="120,20 116,28 124,28" fill="#2d3748"/>'
            '<text x="214" y="114" font-size="11" fill="#2d3748">x</text><text x="124" y="24" font-size="11" fill="#2d3748">y</text>'
            '<line x1="30" y1="190" x2="200" y2="50" stroke="#e74c3c" stroke-width="2"/>'
            '<circle cx="120" cy="110" r="3" fill="#e74c3c"/><text x="126" y="114" font-size="10" fill="#718096">(0,0)</text>'
            '<circle cx="155" cy="85" r="3" fill="#e74c3c"/><text x="161" y="81" font-size="10" fill="#c0392b" font-weight="bold">y=2x−1</text>'
            '<circle cx="120" cy="138" r="3" fill="#4c51bf"/><text x="126" y="142" font-size="10" fill="#4c51bf">(0,−1)</text>'
            '<circle cx="135" cy="110" r="3" fill="#2f855a"/><text x="141" y="114" font-size="10" fill="#2f855a">(1/2,0)</text>'
            '</svg></div></div>')

# ④ k的几何意义 升级 + 三线图
ch4_old3 = '<div class="k-item"><h4>k的几何意义</h4><p>k>0：y随x增大而增大（上升）；k<0：y随x增大而减小（下降）。|k|越大直线越陡。</p></div>'
ch4_new3 = ('<div class="k-item"><h4>k的几何意义</h4><p><strong>k>0</strong>：y 随 x 增大而增大，直线<strong>上升</strong>（过一三象限方向）；<br>'
            '<strong>k&lt;0</strong>：y 随 x 增大而减小，直线<strong>下降</strong>（过二四象限方向）；<br>'
            '<strong>|k| 越大</strong>：直线越<strong>陡</strong>；|k| 越小，直线越平缓。<br>'
            '<strong>记忆</strong>："正升负降，绝对值大陡峭"。</p>'
            '<div style="text-align:center;margin-top:.4rem">'
            '<svg viewBox="0 0 240 200" style="width:100%;max-width:220px;height:auto" xmlns="http://www.w3.org/2000/svg">'
            '<line x1="30" y1="100" x2="210" y2="100" stroke="#2d3748" stroke-width="1.5"/>'
            '<line x1="120" y1="180" x2="120" y2="20" stroke="#2d3748" stroke-width="1.5"/>'
            '<text x="214" y="104" font-size="11" fill="#2d3748">x</text><text x="124" y="24" font-size="11" fill="#2d3748">y</text>'
            '<line x1="40" y1="140" x2="200" y2="60" stroke="#48bb78" stroke-width="2"/>'
            '<text x="150" y="80" font-size="10" fill="#2f855a" font-weight="bold">y=2x (k&gt;0)</text>'
            '<line x1="200" y1="140" x2="40" y2="60" stroke="#e74c3c" stroke-width="2"/>'
            '<text x="52" y="80" font-size="10" fill="#c0392b" font-weight="bold">y=−2x (k&lt;0)</text>'
            '<line x1="60" y1="130" x2="180" y2="70" stroke="#667eea" stroke-width="2"/>'
            '<text x="98" y="128" font-size="10" fill="#4c51bf" font-weight="bold">y=x (较缓)</text>'
            '</svg></div></div>')

# ⑤ b的几何意义 升级
ch4_old4 = '<div class="k-item"><h4>b的几何意义</h4><p>b>0：交y轴正半轴；b<0：交y轴负半轴；b=0：过原点（正比例）。</p></div>'
ch4_new4 = ('<div class="k-item"><h4>b的几何意义</h4><p><strong>b>0</strong>：直线与 y 轴交于<strong>正半轴</strong> (0,b)，b 越大交点越高；<br>'
            '<strong>b&lt;0</strong>：交于<strong>负半轴</strong> (0,b)；<strong>b=0</strong>：过原点 → 正比例函数。<br>'
            '<strong>图象平移</strong>：b 相当于把 y=kx 的图象<strong>上下平移</strong> |b| 个单位（b&gt;0 上移，b&lt;0 下移）。<br>'
            '<strong>例</strong>：y=2x+1 是 y=2x 上移 1 个单位；y=2x−3 是 y=2x 下移 3 个单位。</p></div>')

# ⑥ 与方程的联系 升级 + 交点图
ch4_old6 = '<div class="k-item"><h4>与方程的联系</h4><p>一次函数y=kx+b的图象与x轴交点横坐标=方程kx+b=0的解。<br>步骤：令y=0→解kx+b=0→得x，交点即(x,0)。<br>例：y=2x-6，令2x-6=0得x=3，与x轴交于(3,0)，3就是方程2x-6=0的解。<br>推广：两个一次函数图象的交点坐标=联立两解析式所得方程组的解。</p></div>'
ch4_new6 = ('<div class="k-item"><h4>与方程的联系</h4><p><strong>定理（数形结合）</strong>：一次函数 y=kx+b 的图象与 x 轴交点横坐标 = 方程 kx+b=0 的解。<br>'
            '<strong>步骤</strong>：令 y=0 → 解 kx+b=0 → 得 x，交点即 (x,0)。<br>'
            '<strong>例</strong>：y=2x−6，令 2x−6=0 得 x=3，与 x 轴交于 (3,0)，3 就是方程 2x−6=0 的解。<br>'
            '<strong>推广（两线交点）</strong>：两个一次函数图象的交点坐标 = 联立两解析式所得方程组的解。<br>'
            '<strong>例</strong>：y=x+1 与 y=−x+3 联立得 x=1、y=2，交点 (1,2)。</p>'
            '<div style="text-align:center;margin-top:.4rem">'
            '<svg viewBox="0 0 240 220" style="width:100%;max-width:220px;height:auto" xmlns="http://www.w3.org/2000/svg">'
            '<line x1="30" y1="110" x2="210" y2="110" stroke="#2d3748" stroke-width="1.5"/>'
            '<line x1="120" y1="200" x2="120" y2="20" stroke="#2d3748" stroke-width="1.5"/>'
            '<text x="214" y="114" font-size="11" fill="#2d3748">x</text><text x="124" y="24" font-size="11" fill="#2d3748">y</text>'
            '<line x1="40" y1="170" x2="200" y2="50" stroke="#e74c3c" stroke-width="2"/>'
            '<text x="160" y="60" font-size="10" fill="#c0392b" font-weight="bold">y=x+1</text>'
            '<line x1="40" y1="50" x2="200" y2="170" stroke="#48bb78" stroke-width="2"/>'
            '<text x="40" y="60" font-size="10" fill="#2f855a" font-weight="bold">y=−x+3</text>'
            '<circle cx="120" cy="110" r="4" fill="#e74c3c"/>'
            '<text x="104" y="100" font-size="10" fill="#c0392b" font-weight="bold">交点(1,2)</text>'
            '</svg></div></div>')

patch_file('math8_ch4_interactive.html',
           [(ch4_old0, ch4_new0), (ch4_old1, ch4_new1), (ch4_old2, ch4_new2),
            (ch4_old3, ch4_new3), (ch4_old4, ch4_new4), (ch4_old6, ch4_new6)],
           'ch4 一次函数')

# ================= ch5 方程组 =================
# ① 二元一次方程 升级
ch5_old0 = '<div class="k-item"><h4>二元一次方程</h4><p>含两个未知数，且含未知数项的次数都是1的方程，如2x+y=5。一般形式：ax+by=c。</p></div>'
ch5_new0 = ('<div class="k-item"><h4>二元一次方程</h4><p><strong>定义</strong>：含<strong>两个未知数</strong>，且含未知数项的次数都是 <strong>1</strong> 的整式方程。<br>'
            '例：2x+y=5、x−3y=0 都是；x²+y=5 不是（次数 2）；xy=4 不是（次数 2）。<br>'
            '<strong>一般形式</strong>：ax+by=c（a、b 不同时为 0）。<br>'
            '<strong>解</strong>：使方程成立的未知数的值，一个二元一次方程有<strong>无数个解</strong>。<br>'
            '<strong>几何意义</strong>：ax+by=c 可变形为 y=(c−ax)/b，对应一条直线，每个解都是直线上一个点。</p></div>')

# ② 二元一次方程组 升级
ch5_old1 = '<div class="k-item"><h4>二元一次方程组</h4><p>由两个二元一次方程组成的方程组。公共解叫方程组的解。</p></div>'
ch5_new1 = ('<div class="k-item"><h4>二元一次方程组</h4><p><strong>定义</strong>：由<strong>两个二元一次方程</strong>组成的方程组。<br>'
            '<strong>方程组的解</strong>：两个方程的<strong>公共解</strong>（同时满足两个方程），写成一组的两个值：{x=a, y=b}。<br>'
            '<strong>几何意义</strong>：每个方程是一条直线，方程组的解 = 两直线<strong>交点坐标</strong>。<br>'
            '<strong>检验</strong>：把解代入两个方程都成立才正确。</p></div>')

# ③ 与一次函数 升级 + 交点图
ch5_old6 = '<div class="k-item"><h4>与一次函数</h4><p>二元一次方程组的解=两直线交点坐标。</p></div>'
ch5_new6 = ('<div class="k-item"><h4>与一次函数</h4><p><strong>定理（数形结合）</strong>：二元一次方程组的解 = 两直线交点坐标。<br>'
            '<strong>方法</strong>：①把每个方程化为 y=kx+b 形式；②在坐标系画出两条直线；③交点坐标即方程组的解。<br>'
            '<strong>例</strong>：{x+y=5, x−y=1} → y=−x+5 与 y=x−1，交点 (3,2)，即解 x=3、y=2。<br>'
            '<strong>验证</strong>：3+2=5 ✓，3−2=1 ✓。</p>'
            '<div style="text-align:center;margin-top:.4rem">'
            '<svg viewBox="0 0 240 220" style="width:100%;max-width:220px;height:auto" xmlns="http://www.w3.org/2000/svg">'
            '<line x1="30" y1="110" x2="210" y2="110" stroke="#2d3748" stroke-width="1.5"/>'
            '<line x1="120" y1="200" x2="120" y2="20" stroke="#2d3748" stroke-width="1.5"/>'
            '<text x="214" y="114" font-size="11" fill="#2d3748">x</text><text x="124" y="24" font-size="11" fill="#2d3748">y</text>'
            '<line x1="40" y1="170" x2="200" y2="50" stroke="#e74c3c" stroke-width="2"/>'
            '<text x="160" y="60" font-size="10" fill="#c0392b" font-weight="bold">x+y=5</text>'
            '<line x1="40" y1="50" x2="200" y2="170" stroke="#48bb78" stroke-width="2"/>'
            '<text x="40" y="60" font-size="10" fill="#2f855a" font-weight="bold">x−y=1</text>'
            '<circle cx="120" cy="110" r="4" fill="#e74c3c"/>'
            '<text x="104" y="100" font-size="10" fill="#c0392b" font-weight="bold">交点(3,2)</text>'
            '</svg></div></div>')

# ④ 解的判断 升级 + 三情况图
ch5_old7 = '<div class="k-item"><h4>解的判断</h4><p>有唯一解（两直线相交）；无解（平行）；无数解（重合）。</p></div>'
ch5_new7 = ('<div class="k-item"><h4>解的判断</h4><p><strong>唯一解</strong>：两直线<strong>相交</strong>（k₁≠k₂）——方程组有唯一解。<br>'
            '<strong>无解</strong>：两直线<strong>平行</strong>（k₁=k₂ 且 b₁≠b₂）——方程组无解。<br>'
            '<strong>无数解</strong>：两直线<strong>重合</strong>（k₁=k₂ 且 b₁=b₂，即方程成比例）——有无数解。<br>'
            '<strong>判断口诀</strong>："斜率不同定相交，斜率相同看截距——截距不同平行无解，截距相同重合无数解"。</p>'
            '<div style="text-align:center;margin-top:.4rem">'
            '<svg viewBox="0 0 320 110" style="width:100%;max-width:300px;height:auto" xmlns="http://www.w3.org/2000/svg">'
            '<line x1="20" y1="80" x2="90" y2="20" stroke="#e74c3c" stroke-width="2"/>'
            '<line x1="50" y1="90" x2="120" y2="30" stroke="#48bb78" stroke-width="2"/>'
            '<circle cx="74" cy="53" r="3.5" fill="#e74c3c"/><text x="60" y="50" font-size="9" fill="#c0392b" font-weight="bold">相交</text>'
            '<text x="30" y="102" font-size="9" fill="#718096">唯一解</text>'
            '<line x1="170" y1="85" x2="240" y2="25" stroke="#e74c3c" stroke-width="2"/>'
            '<line x1="180" y1="85" x2="250" y2="25" stroke="#48bb78" stroke-width="2"/>'
            '<text x="185" y="102" font-size="9" fill="#718096">平行 → 无解</text>'
            '<line x1="290" y1="70" x2="290" y2="30" stroke="#e74c3c" stroke-width="3"/>'
            '<line x1="300" y1="70" x2="300" y2="30" stroke="#48bb78" stroke-width="3" stroke-dasharray="3,3"/>'
            '<text x="295" y="102" font-size="9" fill="#718096">重合 → 无数解</text>'
            '</svg></div></div>')

patch_file('math8_ch5_interactive.html',
           [(ch5_old0, ch5_new0), (ch5_old1, ch5_new1), (ch5_old6, ch5_new6), (ch5_old7, ch5_new7)],
           'ch5 方程组')
print('ALL DONE')
