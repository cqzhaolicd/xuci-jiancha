#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""从 physics_lesson10 模板克隆构建 物理第十二讲（透镜应用）+ 第十三讲（质量和体积）。"""
import re, json

TPL = 'physics_lesson10_interactive.html'
tpl = open(TPL, encoding='utf-8').read()

# ============================================================
# 第十二讲 透镜应用
# ============================================================
L12 = {
    'name': '透镜应用', 'num': '第十二讲',
    'title': '<title>🔍 透镜应用 · 互动学习</title>',
    'h1': '<h1><i class="fas fa-search"></i> 透镜应用 · 互动学习</h1>',
    'nav': ' 物理 · 透镜应用</a>',
    'footer': '物理 · 透镜应用互动学习 | 天元教育 · 初二博学班',
    'chapter': '透镜应用',
    'tags': '透镜应用,凸透镜,眼睛,显微镜,望远镜,物理',
    'nq': 25, 'nf': 20, 'ne': 8,
    'knowledge': [
        ('c1', 'fa-search-plus', '#667eea', '放大镜', [
            '物距 <strong class="hl">u＜f</strong>：成正立、放大的<strong class="hl">虚像</strong>',
            '像与物在透镜<strong class="hl">同侧</strong>，人从另一侧观察',
            '物体离放大镜<strong class="hl">越近</strong>，所成像越大',
            '成像原理：u＜f 虚像（<strong class="hl">同侧正大虚</strong>）',
        ]),
        ('c2', 'fa-projector', '#e67e22', '幻灯机 / 投影仪', [
            '物距 <strong class="hl">f＜u＜2f</strong>：成倒立、放大的<strong class="hl">实像</strong>',
            '为使屏幕上是正立像，幻灯片要<strong class="hl">倒放</strong>',
            '凸透镜离幻灯片<strong class="hl">越近</strong>，像越大',
            '投影仪用<strong class="hl">平面镜改变光路</strong>（竖直成像转水平）',
        ]),
        ('c3', 'fa-camera', '#3498db', '照相机', [
            '物距 <strong class="hl">u＞2f</strong>：成倒立、缩小的<strong class="hl">实像</strong>',
            '像距 <strong class="hl">f＜v＜2f</strong>（镜头=凸透镜，胶卷/传感器=光屏）',
            '物体离镜头<strong class="hl">越远</strong>，像越小，像距越小',
            '摄像头、航空摄影均为<strong class="hl">照相机原理</strong>',
        ]),
        ('c4', 'fa-eye', '#2ecc71', '眼睛', [
            '<strong class="hl">晶状体+角膜</strong>=凸透镜，<strong class="hl">视网膜</strong>=光屏',
            '物距＞2f，视网膜上成<strong class="hl">倒立缩小实像</strong>',
            '睫状体调节晶状体<strong class="hl">厚薄</strong>改变焦距（看远变薄、看近变厚）',
            '大脑将倒立像处理为<strong class="hl">正立</strong>视觉',
        ]),
        ('c5', 'fa-glasses', '#e74c3c', '近视眼', [
            '成因：晶状体<strong class="hl">曲度过大</strong>（折光过强），像成在视网膜<strong class="hl">前</strong>',
            '矫正：配戴<strong class="hl">凹透镜</strong>（发散光线使像后移）',
            '全飞秒手术：削去角膜使形成<strong class="hl">凹透镜</strong>形状',
            '近点<strong class="hl">变近</strong>，看不清远处物体',
        ]),
        ('c6', 'fa-eye-slash', '#9b59b6', '远视眼', [
            '成因：晶状体<strong class="hl">太薄/曲度过小</strong>，像成在视网膜<strong class="hl">后</strong>',
            '矫正：配戴<strong class="hl">凸透镜</strong>（会聚光线使像前移）',
            '老花眼也需凸透镜矫正',
            '正常眼<strong class="hl">明视距离=25cm</strong>，远点无限远、近点约10cm',
        ]),
        ('c7', 'fa-microscope', '#1abc9c', '显微镜', [
            '两组凸透镜：<strong class="hl">物镜（短焦）</strong>+<strong class="hl">目镜（较长焦）</strong>',
            '物镜：物体在 f＜u＜2f，成倒立放大<strong class="hl">实像</strong>',
            '目镜：实像落在 u＜f 内，当<strong class="hl">放大镜</strong>用成正立放大虚像',
            '最终看到<strong class="hl">倒立放大虚像</strong>（两次放大）',
        ]),
        ('c8', 'fa-telescope', '#34495e', '望远镜', [
            '两组凸透镜：<strong class="hl">物镜（长焦、大口径）</strong>+<strong class="hl">目镜（短焦）</strong>',
            '物镜：远处物体成倒立缩小<strong class="hl">实像</strong>（照相机原理）',
            '目镜：将实像当放大镜用，成正立放大<strong class="hl">虚像</strong>',
            '最终看到倒立缩小虚像，但<strong class="hl">视角增大</strong>显得清晰',
        ]),
    ],
    'teacher_talk': '''<div class="teacher-talk">
      <h4><i class="fas fa-microphone"></i> 🎙️ 课堂要点 · 第十二讲</h4>
      <p>
        <strong>放大镜</strong> — u＜f 成正立放大<strong>虚像</strong>，像物同侧；物越近像越大<br>
        <strong>幻灯机/投影仪</strong> — f＜u＜2f 成倒立放大<strong>实像</strong>，幻灯片倒放，平面镜改变光路<br>
        <strong>照相机</strong> — u＞2f 成倒立缩小<strong>实像</strong>，像距 f＜v＜2f；物远像小<br>
        <strong>眼睛</strong> — 晶状体=凸透镜、视网膜=光屏，成倒立缩小实像；明视距离25cm<br>
        <strong>近视/远视</strong> — 近视：像在视网膜前，<strong>凹透镜</strong>矫正；远视：像在视网膜后，<strong>凸透镜</strong>矫正<br>
        <strong>显微镜</strong> — 物镜短焦成放大实像 + 目镜放大虚像，最终倒立放大虚像<br>
        <strong>望远镜</strong> — 物镜长焦成缩小实像 + 目镜放大，视角增大<br>
        <strong>老师课后总结</strong> — 透镜应用：会判断照相机/投影仪/放大镜的成像与调节；掌握近视远视成因与矫正；了解显微镜望远镜两次成像
      </p>
    </div>''',
    'questions': [
        # === 模块一：照相机 ===
        ('小明用简易照相机模型对着远处广告牌观察，半透明纸上只能看到局部，为看到整个广告牌的像，应把相机', ['A. 远离广告牌，纸筒N往后缩','B. 远离广告牌，纸筒N往前伸','C. 靠近广告牌，纸筒N往后缩','D. 靠近广告牌，纸筒N往前伸'], 0, '要看整个广告牌→物距<strong>增大</strong>（远离），像变小，像距减小→纸筒N<strong>往后缩</strong>。'),
        ('航空摄影中照相机镜头焦距 f=50mm，则底片到镜头间的距离应为', ['A. 100mm 以外','B. 50mm 以内','C. 50mm＜v＜100mm','D. 恰为100mm'], 2, '远处物体 u＞2f，像距在<strong>f＜v＜2f</strong>，即 50mm＜v＜100mm。'),
        ('关于摄像头的说法，错误的是', ['A. 摄像头镜头对光有会聚作用','B. 物体通过摄像头成倒立、缩小的实像','C. 摄像头成像原理与投影仪相同','D. 拍摄时物体位于镜头二倍焦距以外'], 2, '摄像头与<strong>照相机</strong>原理相同（u＞2f 倒立缩小实像），不是投影仪（f＜u＜2f 倒立放大实像）。'),
        ('用自拍杆自拍与直接手持自拍相比，自拍杆可以', ['A. 增大物距，减小像的大小','B. 减小物距，减小像的大小','C. 增大物距，增大像的大小','D. 减小物距，增大像的大小'], 0, '自拍杆使手机远离人→<strong>物距增大</strong>→像变小（物远像小）。'),
        ('“强行透视法”拍摄，下列说法正确的是', ['A. 照相机镜头对光有发散作用','B. 人手和飞机成倒立、缩小的虚像','C. 拍摄时镜头离飞机更远一些','D. 若使人手的像变大，将镜头离人手更近一些'], 3, '照相机成倒立缩小<strong>实像</strong>（B错）；<strong>物近像大</strong>，镜头离人手更近像变大（D对）；镜头会聚光（A错）。'),
        # === 模块二：投影仪 ===
        ('投影仪中 h=40cm，凸透镜焦距不可能小于', ['A. 10cm','B. 20cm','C. 30cm','D. 40cm'], 1, '投影仪 f＜u＜2f，h=40cm 为像距，则 f＜40cm＜2f → <strong>20cm＜f＜40cm</strong>，焦距不可能小于20cm。'),
        ('简易投影仪（手机投影到白墙）的说法，不正确的是', ['A. 投影仪成倒立、放大的实像','B. 要在墙上正常阅读，手机应倒立放置','C. 要使像变大，应减小手机与透镜间距离且增大像距','D. 手机到凸透镜的距离应大于二倍焦距'], 3, '投影仪要求物距在 <strong>f＜u＜2f</strong>，手机距离不能大于2f（D错）；A/B/C均正确。'),
        ('关于公共场所宣传投影灯的说法，正确的是', ['A. 地面上看到的是放大的虚像','B. 缩短镜头与图片的距离时，图案变小','C. 该投影灯成像原理与照相机相同','D. 不同方向都能看到图案是光在地面发生漫反射'], 3, '投影灯成放大<strong>实像</strong>（A错）；缩短物距像应变大（B错）；与<strong>投影仪</strong>原理相同（C错）；漫反射使各方向可见（D对）。'),
        ('自制投影仪（凸透镜焦距 f=10cm）的说法，正确的是', ['A. 凸透镜对光线有发散作用','B. 白墙到凸透镜的距离应大于20cm','C. 胶片与凸透镜距离应小于10cm且倒立放置','D. 要使像更大，只将内筒往外拉一些即可'], 1, '投影仪 f＜u＜2f 且像距 v＞2f → 白墙到透镜距离（像距）<strong>＞20cm</strong>（B对）；凸透镜会聚光（A错）；胶片距离应在10~20cm（C错）。'),
        # === 模块三：放大镜 ===
        ('博物馆在文物前放凸透镜方便观察，文物在透镜中所成的像与文物在透镜的', ['A. 同侧','B. 异侧','C. 焦点上','D. 无法判断'], 0, '放大镜 u＜f 成正立放大虚像，像与物在透镜<strong>同侧</strong>。'),
        ('用焦距10cm的凸透镜看到“电”字放大的像，下列说法正确的是', ['A. 看到的放大像是实像','B. “电”字恰在凸透镜焦点上','C. “电”字到凸透镜的距离应小于10cm','D. “电”字到凸透镜的距离可能是15cm'], 2, '放大镜 u＜f → 物距<strong>小于10cm</strong>，成正立放大虚像（A错）。'),
        ('放大镜的镜头是____透镜，它对光有____作用', ['A. 凸；会聚','B. 凸；发散','C. 凹；会聚','D. 凹；发散'], 0, '放大镜是<strong>凸透镜</strong>，对光有<strong>会聚</strong>作用。'),
        ('用放大镜看书，从甲图（像大）到乙图（像小），所成的像是____物距的结果', ['A. 增大','B. 减小','C. 不变','D. 无法判断'], 0, '放大镜物距<strong>增大</strong>，像变小（物近像大、物远像小）。'),
        # === 模块四：眼睛 ===
        ('人眼成像中，相当于光屏（承接像）的是', ['A. 角膜','B. 晶状体','C. 视网膜','D. 视神经'], 2, '晶状体=凸透镜，<strong>视网膜=光屏</strong>，成倒立缩小实像。'),
        ('近视眼看远处物体时，像成在视网膜的', ['A. 前方','B. 后方','C. 上方','D. 下方'], 0, '近视眼晶状体<strong>曲度过大</strong>折光过强，像成在视网膜<strong>前方</strong>。'),
        ('一副眼镜镜片中心厚度1.7mm，边缘厚度大于1.7mm，该眼镜可用来矫正', ['A. 近视眼','B. 远视眼','C. 老花眼','D. 散光'], 0, '中心薄边缘厚=<strong>凹透镜</strong>，凹透镜矫正<strong>近视眼</strong>。'),
        ('全飞秒近视手术用激光削去部分角膜，使角膜形成____透镜形状矫正近视', ['A. 凹','B. 凸','C. 平','D. 球'], 0, '手术使角膜形成<strong>凹透镜</strong>形状，发散光线，矫正近视。'),
        ('（2025·成都）人形机器人“眼睛”光学成像与人眼相似，下列说法正确的是', ['A. 物体在成像面上成放大的虚像','B. 机器人“眼睛”镜头对光有发散作用','C. 机器人“眼睛”成像原理与照相机相同','D. 机器人“眼睛”只能“看见”发光的物体'], 2, '机器人眼睛=人眼/照相机原理：u＞2f 成倒立缩小<strong>实像</strong>（A错、C对）；镜头会聚光（B错）；能看见不发光物体（D错）。'),
        ('关于眼睛视力矫正的光路图，下列说法正确的是', ['A. 矫正镜片是凹透镜','B. 该图模拟矫正远视眼的情况','C. 去掉镜片光会聚在视网膜前','D. 正常眼的明视距离为25cm'], 3, '正常眼<strong>明视距离25cm</strong>（最清晰又不疲劳）。A/B/C 需结合图判断，D 为恒定结论。'),
        ('小刚爷爷是近视眼，下列说法正确的是', ['A. 爷爷眼睛的明视距离小于25cm','B. 远视眼是由于像成在了视网膜后方','C. 人眼视网膜上成正立、缩小的实像','D. 爷爷应佩戴合适的凸透镜矫正'], 1, 'B 物理正确：<strong>远视眼像成在视网膜后方</strong>；A错（明视距离标准25cm）；C错（视网膜成倒立像）；D错（近视配凹透镜）。'),
        ('由短文“眼睛和眼镜”：正常眼睛的观察范围是', ['A. 0~10cm','B. 10cm~25cm','C. 25cm~无限远','D. 10cm~无限远'], 3, '正常眼睛<strong>远点无限远、近点约10cm</strong>，观察范围为 10cm~无限远。'),
        ('小芳所戴眼镜度数为-500度，该镜片的焦距为', ['A. 0.1m','B. 0.2m','C. 0.5m','D. 2m'], 1, '度数=焦度×100 → 500度焦度=5m⁻¹；φ=1/f → f=1/5=<strong>0.2m</strong>（负号表示凹透镜）。'),
        # === 模块五：显微镜与望远镜 ===
        ('望远镜观察远处物体，物镜成像原理与____相同，目镜所成像是正立、放大的____像', ['A. 照相机；虚','B. 投影仪；实','C. 放大镜；实','D. 照相机；实'], 0, '物镜成倒立缩小实像=<strong>照相机</strong>原理；目镜=放大镜，成正立放大<strong>虚像</strong>。'),
        ('显微镜中，物体到物镜的距离应', ['A. 大于一倍焦距小于二倍焦距','B. 小于一倍焦距','C. 大于二倍焦距','D. 等于一倍焦距'], 0, '显微镜物镜：物体在 <strong>f＜u＜2f</strong>，成倒立放大实像，目镜再放大成虚像。'),
        ('光年（如“距离我们约130亿光年”）是____单位', ['A. 长度','B. 时间','C. 速度','D. 光强度'], 0, '<strong>光年=光一年传播的距离</strong>，是长度单位。'),
    ],
    'flashcards': [
        ('放大镜的成像规律是什么？', '物距 <strong>u＜f</strong>，成正立、放大的<strong>虚像</strong>，像与物在透镜<strong>同侧</strong>；物体越近像越大。'),
        ('幻灯机/投影仪的成像规律？', '物距 <strong>f＜u＜2f</strong>，成倒立、放大的<strong>实像</strong>；幻灯片要倒放，平面镜改变光路。'),
        ('照相机的成像规律？', '物距 <strong>u＞2f</strong>，成倒立、缩小的<strong>实像</strong>，像距 <strong>f＜v＜2f</strong>。'),
        ('实像成像口诀是什么？', '<strong>物近像远像变大</strong>，<strong>物远像近像变小</strong>（对实像）。'),
        ('眼睛的主要结构？', '<strong>晶状体+角膜</strong>=凸透镜（折射光），<strong>视网膜</strong>=光屏，成倒立缩小实像。'),
        ('近视眼的成因？', '晶状体<strong>曲度过大</strong>、折光过强，远处物体像成在视网膜<strong>前方</strong>。'),
        ('近视眼如何矫正？', '配戴<strong>凹透镜</strong>（发散光线，使像后移至视网膜）；全飞秒手术使角膜成凹透镜形。'),
        ('远视眼的成因？', '晶状体太薄/曲度过小，像成在视网膜<strong>后方</strong>。'),
        ('远视眼如何矫正？', '配戴<strong>凸透镜</strong>（会聚光线，使像前移至视网膜）；老花眼同理。'),
        ('正常眼的明视距离是多少？', '<strong>25cm</strong>——正常眼观察物体最清晰又不疲劳的距离。'),
        ('眼镜度数怎么计算？', '度数=焦度×100，焦度 φ=1/f（f单位m）；凸透镜为正、凹透镜为负。例：-200度=凹透镜，φ=2m⁻¹，f=0.5m。'),
        ('显微镜由什么组成？', '两组凸透镜：<strong>物镜（焦距短）</strong>靠近物体 + <strong>目镜（焦距较长）</strong>靠近眼睛。'),
        ('显微镜的成像原理？', '物镜（f＜u＜2f）成倒立放大<strong>实像</strong>，目镜（u＜f）当放大镜成正立放大<strong>虚像</strong>，最终为倒立放大虚像。'),
        ('望远镜由什么组成？', '<strong>物镜（口径大、焦距长）</strong> + <strong>目镜（焦距短）</strong>，如开普勒望远镜。'),
        ('望远镜的成像原理？', '物镜成倒立缩小<strong>实像</strong>（照相机原理），目镜放大成虚像；视角增大使远处物体清晰。'),
        ('投影仪中平面镜的作用？', '<strong>改变光路</strong>：将竖直向上的光反射到屏幕上，使像呈现在观众方向。'),
        ('实像与虚像的区别？', '<strong>实像</strong>：实际光线会聚，<strong>倒立</strong>，光屏可承接；<strong>虚像</strong>：光线反向延长线会聚，<strong>正立</strong>，光屏不能承接。'),
        ('照相机中像的大小如何调节？', '物体离镜头越远，像越小（像距越小）；离得越近，像越大（像距越大）。'),
        ('幻灯机中像的大小如何调节？', '凸透镜离幻灯片<strong>越近</strong>，所成像越大；越远，像越小。'),
        ('人眼看远近物体如何调节？', '<strong>睫状体</strong>调节晶状体厚薄改变焦距：看远处变<strong>薄</strong>、看近处变<strong>厚</strong>。'),
    ],
    'errors': [
        ('照相机/投影仪/放大镜物距范围记反', '把 u＞2f、f＜u＜2f、u＜f 三种情况对应错。', '口诀：<strong>u＞2f 照相机</strong>（倒小实）、<strong>f＜u＜2f 投影仪</strong>（倒大实）、<strong>u＜f 放大镜</strong>（正大虚）。'),
        ('近视眼、远视眼矫正透镜记反', '以为近视眼戴凸透镜、远视眼戴凹透镜。', '近视=像在视网膜<strong>前</strong>→<strong>凹透镜</strong>（发散后移）；远视=像在视网膜<strong>后</strong>→<strong>凸透镜</strong>（会聚前移）。'),
        ('像的大小与物距关系记反', '以为物体靠近镜头像变小。', '实像规律：<strong>物近像远像变大</strong>、物远像近像变小；照相机要拍大，人走近或镜头前伸。'),
        ('显微镜、望远镜物镜目镜焦距记反', '把两者的物镜、目镜焦距长短搞混。', '显微镜：物镜<strong>短焦</strong>、目镜较长焦；望远镜：物镜<strong>长焦</strong>（大口径）、目镜短焦。'),
        ('实像虚像的正倒判断错', '以为放大镜成像是倒立实像。', '<strong>实像倒立</strong>（照相机/投影仪，光屏承接），<strong>虚像正立</strong>（放大镜/目镜，光屏不能承接）。'),
        ('视网膜成像方向搞错', '以为眼睛看到的是正立像。', '视网膜上成<strong>倒立缩小实像</strong>，大脑自动处理为<strong>正立</strong>视觉。'),
        ('眼镜度数正负号混淆', '把凸透镜（远视）度数当负、凹透镜（近视）当正。', '凸透镜度数<strong>正</strong>（远视/老花），凹透镜度数<strong>负</strong>（近视）；-200度是凹透镜。'),
        ('明视距离与近点远点混淆', '把明视距离当成近点。', '<strong>明视距离25cm</strong>（最清晰不疲劳）、近点约10cm、远点无限远；明视距离对所有人相同。'),
    ],
}

# ============================================================
# 第十三讲 质量和体积
# ============================================================
L13 = {
    'name': '质量和体积', 'num': '第十三讲',
    'title': '<title>⚖️ 质量和体积 · 互动学习</title>',
    'h1': '<h1><i class="fas fa-weight-hanging"></i> 质量和体积 · 互动学习</h1>',
    'nav': ' 物理 · 质量和体积</a>',
    'footer': '物理 · 质量和体积互动学习 | 天元教育 · 初二博学班',
    'chapter': '质量和体积',
    'tags': '质量,体积,天平,量筒,排水法,物理',
    'nq': 22, 'nf': 20, 'ne': 8,
    'knowledge': [
        ('c1', 'fa-weight-hanging', '#667eea', '质量', [
            '定义：物体所含<strong class="hl">物质的多少</strong>，符号 m',
            '质量是物体的<strong class="hl">基本属性</strong>，不随位置、形状、温度、状态变化',
            '宇航员到月球质量<strong class="hl">不变</strong>；冰熔化成水质量不变',
        ]),
        ('c2', 'fa-balance-scale', '#e67e22', '质量单位', [
            '国际单位：<strong class="hl">千克(kg)</strong>；常用 t、g、mg',
            '换算：1t=1000kg=10⁶g=10⁹mg',
            '1克拉=0.2g，1磅=450g',
            '单位符号：t 吨、kg 千克、g 克、mg 毫克',
        ]),
        ('c3', 'fa-egg', '#2ecc71', '质量估测', [
            '回形针 30mg；一元硬币 <strong class="hl">6g</strong>；药片 200mg',
            '鸡蛋 <strong class="hl">50g</strong>；苹果 150g；物理书 200g',
            '矿泉水 500g；老母鸡 3kg；中学生 <strong class="hl">50kg</strong>',
            '大象 5t；蓝鲸 150t；小轿车 1~2t',
        ]),
        ('c4', 'fa-tools', '#3498db', '托盘天平使用', [
            '测量工具：托盘天平、台秤、杆秤、电子秤、地磅',
            '<strong class="hl">放</strong>：天平放水平桌面；<strong class="hl">调</strong>：游码归零、平衡螺母调平（<strong class="hl">左偏右调</strong>）',
            '<strong class="hl">称</strong>：左物右码、砝码从大到小；<strong class="hl">读</strong>：m物=m砝码+游码示数（<strong class="hl">游码读左边</strong>）',
        ]),
        ('c5', 'fa-exclamation-triangle', '#e74c3c', '天平注意事项', [
            '调平后称量时<strong class="hl">不能再动平衡螺母</strong>',
            '砝码、游码用<strong class="hl">镊子</strong>夹取，防腐蚀',
            '液体<strong class="hl">装杯</strong>测；固体<strong class="hl">垫纸</strong>（脏、化、腐物品不能直接放盘）',
            '烧杯左右都垫或单边垫完再调零；<strong class="hl">不能用量筒</strong>装液体称量（太高易倒）',
        ]),
        ('c6', 'fa-cube', '#9b59b6', '体积定义与单位', [
            '定义：物体所占<strong class="hl">空间的大小</strong>，符号 V',
            '国际单位：<strong class="hl">立方米(m³)</strong>；常用 dm³、cm³、L、mL',
            '换算：1m³=10³dm³=10⁶cm³；<strong class="hl">1L=1dm³</strong>，1mL=1cm³',
        ]),
        ('c7', 'fa-flask', '#1abc9c', '体积测量', [
            '测液体：<strong class="hl">量筒、量杯</strong>；读数视线与<strong class="hl">凹液面最低处</strong>相平（仰小俯大）',
            '规则固体：测边长用公式计算',
            '不规则固体：<strong class="hl">排水法</strong> V物=V₂-V₁',
            '漂浮物：<strong class="hl">针压法、吊重物法</strong>；溶水物：<strong class="hl">排沙法、排油法</strong>',
        ]),
        ('c8', 'fa-chart-line', '#34495e', '误差分析', [
            '先测V₁再测V₂（正常排水法）→ 结果准确',
            '取出物<strong class="hl">沾水带出</strong>→V₁偏小→测得体积<strong class="hl">偏大</strong>',
            '木块<strong class="hl">吸水</strong>→V₃偏小→测得体积<strong class="hl">偏小</strong>',
            '解决吸水：<strong class="hl">包一层薄膜</strong>或<strong class="hl">吸足水再测</strong>',
            'V铁=V₂-V₁；V木=V₃-V₂',
        ]),
    ],
    'teacher_talk': '''<div class="teacher-talk">
      <h4><i class="fas fa-microphone"></i> 🎙️ 课堂要点 · 第十三讲</h4>
      <p>
        <strong>质量</strong> — 物体所含物质的多少；属性：不随位置/形状/温度/状态变化<br>
        <strong>单位</strong> — kg（国际）、t/g/mg；1t=1000kg=10⁶g；1克拉=0.2g、1磅=450g<br>
        <strong>估测</strong> — 鸡蛋50g、一元硬币6g、中学生50kg、矿泉水500g、大象5t<br>
        <strong>天平</strong> — 放→调→称→读：左偏右调、左物右码、m物=m砝码+游码（游码读左边）<br>
        <strong>天平注意</strong> — 调平后不动平衡螺母、砝码用镊子、液体装杯、固体垫纸<br>
        <strong>体积</strong> — 国际单位m³；1L=1dm³、1mL=1cm³；量筒读数凹液面最低处（仰小俯大）<br>
        <strong>测固体</strong> — 排水法V物=V₂-V₁；漂浮物针压法/吊重物；溶水物排沙/排油；吸水物包薄膜<br>
        <strong>老师课后总结</strong> — 质量与体积：掌握质量属性与天平规范使用；会用排水法测体积并分析误差
      </p>
    </div>''',
    'questions': [
        # === 模块一：质量 ===
        ('质量是指物体所含', ['A. 物质的多少','B. 重力的大小','C. 体积的大小','D. 密度的大小'], 0, '质量定义：物体所含<strong>物质的多少</strong>（m）。'),
        ('宇航员从地球到月球，他的质量将', ['A. 变大','B. 变小','C. 不变','D. 变为零'], 2, '质量是物体的<strong>属性</strong>，不随位置变化，宇航员到月球质量不变。'),
        ('把铁块加热熔化成铁水，它的质量', ['A. 变大','B. 变小','C. 不变','D. 无法判断'], 2, '质量不随<strong>温度、状态</strong>变化，铁块变铁水质量不变。'),
        ('1t 等于', ['A. 10kg','B. 100kg','C. 1000kg','D. 10000kg'], 2, '1t=<strong>1000</strong>kg。'),
        ('一个鸡蛋质量约50g，合', ['A. 0.05kg','B. 0.5kg','C. 5kg','D. 500g'], 0, '1kg=1000g，50g=<strong>0.05</strong>kg。'),
        ('下列估测最接近实际的是', ['A. 一个鸡蛋约500g','B. 一名中学生约50kg','C. 一元硬币约50g','D. 一瓶矿泉水约5kg'], 1, '中学生约<strong>50kg</strong>；鸡蛋约50g、硬币约6g、矿泉水约500g。'),
        ('实验室测量质量的工具是', ['A. 量筒','B. 刻度尺','C. 托盘天平','D. 弹簧测力计'], 2, '测量质量用<strong>托盘天平</strong>；量筒测体积、刻度尺测长度。'),
        ('使用托盘天平时，首先应', ['A. 将天平放在水平桌面上','B. 左物右码开始称量','C. 调节游码归零','D. 直接放物体'], 0, '天平使用第一步：<strong>放</strong>——放在水平桌面上。'),
        ('调节天平横梁平衡时，指针左偏，应将平衡螺母向', ['A. 左调','B. 右调','C. 上调','D. 下调'], 1, '<strong>左偏右调</strong>：指针左偏说明左盘重，平衡螺母向右调。'),
        ('称量时物体应放在____盘，砝码放在____盘', ['A. 左；右','B. 右；左','C. 左；左','D. 右；右'], 0, '天平称量规则：<strong>左物右码</strong>。'),
        ('砝码50g+20g，游码示数2.4g，物体质量为', ['A. 72.4g','B. 67.6g','C. 70g','D. 74g'], 0, 'm物=m砝码+游码示数=50+20+2.4=<strong>72.4g</strong>。'),
        ('读取游码示数时，应读游码', ['A. 左边所对刻度','B. 右边所对刻度','C. 中间所对刻度','D. 任意位置'], 0, '游码读数：读<strong>左边</strong>所对刻度。'),
        ('天平调平后，称量过程中', ['A. 不能再调节平衡螺母','B. 可以调节平衡螺母','C. 可以移动游码归零','D. 可以左右换盘'], 0, '调平后称量时<strong>不能动平衡螺母</strong>，只能加减砝码、移动游码。'),
        ('取放砝码应使用', ['A. 镊子','B. 手直接拿','C. 小刀','D. 夹子随意'], 0, '砝码、游码用<strong>镊子</strong>夹取，防止腐蚀生锈。'),
        # === 模块二：体积 ===
        ('体积的国际单位是', ['A. 立方米(m³)','B. 升(L)','C. 立方厘米(cm³)','D. 毫升(mL)'], 0, '体积国际单位<strong>m³</strong>；L、cm³、mL 是常用单位。'),
        ('1L 等于', ['A. 1m³','B. 1dm³','C. 1cm³','D. 10dm³'], 1, '<strong>1L=1dm³</strong>；1mL=1cm³。'),
        ('用量筒测液体体积，读数时视线应', ['A. 与凹液面最低处相平','B. 与凹液面最高处相平','C. 俯视量筒刻度','D. 仰视量筒刻度'], 0, '量筒读数：视线与<strong>凹液面最低处</strong>相平；俯视偏大、仰视偏小。'),
        ('量筒内原有水V₁，放入石块后示数为V₂，石块体积为', ['A. V₂-V₁','B. V₂+V₁','C. V₁-V₂','D. V₂'], 0, '排水法：V物=<strong>V₂-V₁</strong>。'),
        ('测石块体积时，从水中取出石块带出一部分水，测得体积会', ['A. 偏大','B. 偏小','C. 不变','D. 无法判断'], 0, '带出水→量筒中水<strong>V₁偏小</strong>→V₂-V₁<strong>偏大</strong>。'),
        ('测木块（会吸水）体积，正确的做法是', ['A. 直接放入水中读数','B. 包一层薄膜再测','C. 用排沙法','D. 用针压法'], 1, '木块吸水会使测得体积<strong>偏小</strong>，应<strong>包一层薄膜</strong>或吸足水后再测。'),
        ('漂浮在水面的小木块测体积，可采用', ['A. 针压法或吊重物法','B. 直接排水法','C. 排油法','D. 刻度尺量'], 0, '漂浮物不能自然浸没，用<strong>针压法</strong>（针压入水）或<strong>吊重物法</strong>使其浸没。'),
        ('易溶于水的物体（如食盐）测体积，应用', ['A. 排水法','B. 排沙法或排油法','C. 量筒直接测','D. 天平换算'], 1, '溶水物不能排水法，用<strong>排沙法、排油法</strong>。'),
    ],
    'flashcards': [
        ('什么是质量？', '物体所含<strong>物质的多少</strong>，符号 m；是物体的基本属性。'),
        ('质量有什么特点？', '<strong>不随位置、形状、温度、状态</strong>变化而变化（到月球不变、冰化水不变）。'),
        ('质量单位有哪些？', '国际单位<strong>千克(kg)</strong>；常用 t、g、mg；1t=1000kg=10⁶g=10⁹mg。'),
        ('常见质量估测？', '鸡蛋<strong>50g</strong>、一元硬币6g、中学生50kg、苹果150g、矿泉水500g、大象5t、蓝鲸150t。'),
        ('托盘天平使用四步？', '<strong>放</strong>（水平桌面）→<strong>调</strong>（游码归零、螺母调平）→<strong>称</strong>（左物右码）→<strong>读</strong>（m物=m砝码+游码）。'),
        ('天平指针左偏怎么办？', '<strong>左偏右调</strong>：指针左偏说明左盘重，平衡螺母向右调。'),
        ('天平读数公式？', 'm物=<strong>m砝码+游码示数</strong>；游码读数读<strong>左边</strong>。'),
        ('天平使用注意事项？', '调平后<strong>不动平衡螺母</strong>；砝码游码用<strong>镊子</strong>；液体装杯、固体垫纸；不能用量筒装液体称。'),
        ('什么是体积？', '物体所占<strong>空间的大小</strong>，符号 V；国际单位<strong>立方米(m³)</strong>。'),
        ('体积单位换算？', '1m³=10³dm³=10⁶cm³；<strong>1L=1dm³</strong>，1mL=1cm³。'),
        ('量筒读数要点？', '视线与<strong>凹液面最低处</strong>相平；<strong>俯视偏大、仰视偏小</strong>。'),
        ('测液体体积用什么？', '<strong>量筒、量杯</strong>。'),
        ('测规则固体体积？', '直接测量边长，用公式计算（如正方体 V=a³、长方体 V=abh）。'),
        ('排水法测体积？', '量筒水V₁，放入物体示数V₂，V物=<strong>V₂-V₁</strong>。'),
        ('漂浮物体如何测体积？', '<strong>针压法</strong>（用针把物体压入水中）或<strong>吊重物法</strong>。'),
        ('溶水物体如何测体积？', '<strong>排沙法、排油法</strong>（如食盐不能排水法）。'),
        ('排水法误差：沾水带出？', '取出物带出水→V₁偏小→测得体积<strong>偏大</strong>。'),
        ('排水法误差：木块吸水？', 'V₃偏小→测得体积<strong>偏小</strong>；应<strong>包薄膜</strong>或<strong>吸足水</strong>再测。'),
        ('质量测量工具有哪些？', '托盘天平（实验室）、台秤、杆秤、电子秤、地磅。'),
        ('天平称量特殊物体？', '液体<strong>装杯</strong>称（杯+液再减杯）；脏/化/腐固体<strong>垫纸</strong>；烧杯垫纸后调零。'),
    ],
    'errors': [
        ('质量随位置/状态变化', '以为宇航员到月球质量变小、冰化成水质量变大。', '质量是<strong>属性</strong>：不随位置、形状、温度、状态变化；月球、冰水质量都不变。'),
        ('调平后称量时动平衡螺母', '称量中发现不平衡就调平衡螺母。', '调平后<strong>不能再动平衡螺母</strong>；只能加减砝码、移动游码。'),
        ('游码读数读右边', '把游码右端对着的刻度当成示数。', '游码读数读<strong>左边</strong>所对刻度。'),
        ('左码右物', '把物体放右盘、砝码放左盘。', '必须<strong>左物右码</strong>；若放反，m物=砝码-游码（游码被加反）。'),
        ('量筒读数俯视/仰视', '俯视或仰视量筒刻度读数。', '<strong>俯视偏大、仰视偏小</strong>，必须平视<strong>凹液面最低处</strong>。'),
        ('木块吸水误差方向', '以为吸水使体积偏大。', '吸水使V₃<strong>偏小</strong>→体积<strong>偏小</strong>；应包薄膜或吸足水再测。'),
        ('排水法取出带水', '忽略取出物带出的水。', '带出水→V₁偏小→体积<strong>偏大</strong>；应将带出的水冲回量筒。'),
        ('单位换算混淆', '1L=1cm³、1t=100g 等错记。', '<strong>1L=1dm³</strong>=10⁻³m³、1mL=1cm³；1t=1000kg=10⁶g。'),
    ],
}

# ============================================================
# 克隆构建
# ============================================================
def build_lesson(data, dst):
    h = tpl
    nq, nf, ne = data['nq'], data['nf'], data['ne']
    name = data['name']
    # part1 全局替换
    h = h.replace('<title>🔦 光的折射 · 互动学习</title>', data['title'])
    h = h.replace('<h1><i class="fas fa-lightbulb"></i> 光的折射 · 互动学习</h1>', data['h1'])
    h = h.replace(' 物理 · 光的折射</a>', data['nav'])
    h = h.replace('物理 · 光的折射互动学习 | 天元教育 · 初二博学班', data['footer'])
    h = h.replace('初二博学班 · 4 模块 · 40 题 · 20 卡牌 | 天元教育',
                  '初二博学班 · 4 模块 · %d 题 · %d 卡牌 | 天元教育' % (nq, nf))
    h = re.sub(r'\d+道测验题', '%d道测验题' % nq, h)
    h = re.sub(r'\d+张知识卡', '%d张知识卡' % nf, h)
    h = re.sub(r'\d+大易错点', '%d大易错点' % ne, h)
    h = h.replace('0 / 40', '0 / %d' % nq)
    # 知识图谱段整体替换（tab-knowledge 到 tab-quiz 前）
    ki = h.find('id="tab-knowledge"')
    kj = h.find('<div id="tab-quiz"', ki)
    assert ki > 0 and kj > ki, '知识段锚点失败'
    cards_html = '\n'.join(
        '      <div class="knowledge-card %s"><h3><i class="fas %s" style="color:%s"></i> %s</h3><ul>\n%s\n      </ul></div>' % (
            cls, icon, color, title,
            '\n'.join('        <li>%s</li>' % li for li in lis))
        for cls, icon, color, title, lis in data['knowledge'])
    new_knowledge = ('id="tab-knowledge" class="tab-content active">\n'
                     '    <div class="section-header"><i class="fas fa-sitemap" style="color:#667eea"></i> %s · %s</div>\n\n'
                     '        <div class="knowledge-grid">\n%s\n      </div>\n\n'
                     '    %s\n    </div>' % (data['num'], name, cards_html, data['teacher_talk']))
    h = h[:ki] + new_knowledge + h[kj:]
    # part2/3/4 数组整体替换
    q_items = ',\n'.join("{q:'%s',opts:%s,ans:%d,exp:'%s'}" % (q, json.dumps(opts, ensure_ascii=False), ans, exp)
                        for q, opts, ans, exp in data['questions'])
    f_items = ',\n'.join("{front:'%s',back:'%s'}" % (f, b) for f, b in data['flashcards'])
    e_items = ',\n'.join("{title:'❌ %s',desc:'<strong>易错</strong>：%s<strong>正解</strong>：%s'}" % (t, w, r)
                        for t, w, r in data['errors'])
    qi = h.find('const questions = [')
    qj = h.find('\n];', qi)
    h = h[:qi] + 'const questions = [\n' + q_items + '\n];' + h[qj + 3:]
    fi = h.find('const flashcards = [')
    fj = h.find('\n];', fi)
    h = h[:fi] + 'const flashcards = [\n' + f_items + '\n];' + h[fj + 3:]
    ei = h.find('const errors = [')
    ej = h.find('\n];', ei)
    h = h[:ei] + 'const errors = [\n' + e_items + '\n];' + h[ej + 3:]
    # part5 元数据 key
    h = h.replace("QUIZ_PROG_KEY='quiz_progress_physics_lesson10'",
                  "QUIZ_PROG_KEY='quiz_progress_physics_lesson%s'" % ('12' if name == '透镜应用' else '13'))
    h = h.replace("WRONG_HISTORY_KEY='quiz_physics9_state'",
                  "WRONG_HISTORY_KEY='quiz_physics_lesson%s_wrong'" % ('12' if name == '透镜应用' else '13'))
    h = re.sub(r"chapter:'[^']*'", "chapter:'%s'" % data['chapter'], h)
    h = re.sub(r"tags:'[^']*'", "tags:'%s'" % data['tags'], h)
    open(dst, 'w', encoding='utf-8').write(h)
    print('✅ 生成 %s（%s）: %d题/%d卡/%d错' % (dst, name, nq, nf, ne))

build_lesson(L12, 'physics_lesson12_interactive.html')
build_lesson(L13, 'physics_lesson13_interactive.html')
print('完成')
