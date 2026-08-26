# -*- coding: utf-8 -*-
"""按《Python Crash Course 3rd》20 章生成赵立学习中心章节互动页 (Part 1: 数据+生成)"""
import io, sys, json, subprocess, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# ============ 章节内容数据 (全部基于蒸馏笔记, 防幻觉) ============
# 每章: (文件名, 标题, 副标题, kp_key, 知识卡[], 题目[], 卡牌[], 易错[], 颜色)

CHAPTERS = []

# ---- Ch1 起步 ----
CHAPTERS.append(dict(
    fname='python_ch1_interactive.html', title='第1章 起步', subtitle='Python 编程 · 第1章',
    key='zhaoli_py_ch1', color='#667eea',
    knowledge=[
        ('Python 版本', '本书代码需要 Python 3.9 或更高版本。终端输入 python(Windows) 或 python3(macOS/Linux) 启动解释器, >>> 是提示符。'),
        ('安装注意', '从 python.org 下载官方安装器, 安装时必须勾选 Add Python to PATH(否则终端找不到 python 命令)。macOS/Linux 必须用 python3 命令(避免误用旧版 Python 2)。'),
        ('hello_world.py', '新建 .py 文件写 print("Hello Python world!")。VS Code 按 CTRL-F5 运行, 或终端 python hello_world.py(先 cd 到文件目录)。'),
        ('Traceback', '程序出错时 Python 显示的报错信息, 指出出错文件和行号, 是排查问题的第一线索。'),
        ('语法严格性', '编程语言要求精确语法: print 不能写成 Print, 引号/括号必须成对匹配, 否则报错。'),
        ('疑难排查', '①看 traceback ②休息一下重读代码 ③删文件重建 ④请人照步骤操作 ⑤查附录A ⑥求助社区(说明想做什么/试过什么/得到什么结果)。'),
    ],
    questions=[
        ("启动 Python 解释器的命令是(Windows)", ["A. python", "B. python3", "C. py2", "D. pyth"], 0, "Windows 用 python; macOS/Linux 用 python3。"),
        ("Windows 安装 Python 时必须勾选", ["A. Add Python to PATH", "B. Use Python 2", "C. Install Games", "D. 不需要勾选"], 0, "不勾选 PATH 终端就找不到 python 命令。"),
        (">>> 是", ["A. Python 终端提示符", "B. 注释符号", "C. 错误符号", "D. 乘法符号"], 0, ">>> 表示当前处于 Python 终端会话, 可运行代码片段。"),
        ("print 写成 Print 会怎样?", ["A. 语法错误", "B. 正常运行", "C. 警告", "D. 打印小写"], 0, "编程语言要求精确语法, 大小写敏感。"),
        ("程序出错时排查的第一线索是", ["A. traceback", "B. 重装系统", "C. 删代码", "D. 换电脑"], 0, "traceback 指出出错文件和行号。"),
        ("高效求助时要说明", ["A. 想做什么/试过什么/得到什么结果", "B. 只说报错", "C. 骂编译器", "D. 什么也不说"], 0, "清晰的求助信息能让别人快速帮你。"),
    ],
    flashcards=[
        ("Python 3.9+", "本书要求 Python 3.9 或更高版本。终端 >>> 可运行代码片段。"),
        ("Add to PATH", "Windows 安装必须勾选 Add Python to PATH, 否则找不到命令。"),
        ("Traceback", "报错信息=排查第一线索: 看文件和行号。"),
    ],
    errors=[
        ("macOS 用 python", "macOS 上 python 可能指向过时的 Python 2。", "macOS/Linux 一律用 python3 命令。"),
        ("没 cd 就运行", "在终端运行 .py 找不到文件。", "先 cd 到文件所在目录再运行。"),
    ],
))

# ---- Ch2 变量与数据类型 ----
CHAPTERS.append(dict(
    fname='python_ch2_interactive.html', title='第2章 变量与数据类型', subtitle='Python 编程 · 第2章',
    key='zhaoli_py_ch2', color='#667eea',
    knowledge=[
        ('变量', '变量是贴在值上的标签(不是盒子), 值可随时更改, Python 始终跟踪当前值。命名: 字母/下划线开头、不能以数字开头、不能含空格、避免关键字、小写。'),
        ('NameError', '变量名拼写不一致或未赋值就使用 → NameError。Python 不做拼写检查, 只要求拼写一致。'),
        ('字符串', '引号内都是字符串, 单双引号均可(这让你能放撇号)。方法: title()/upper()/lower()。'),
        ('f-string', '开引号前加 f, 花括号 {} 插入变量: f"Hello, {name}!"。忘记 f 前缀 → 花括号原样输出。'),
        ('空白处理', '\\t 制表符、\\n 换行。strip()/lstrip()/rstrip() 去空白(要重新赋值才永久); removeprefix()/removesuffix() 删前后缀。'),
        ('数字', 'int 整数、float 浮点。4/2=2.0(真除总返回浮点)。0.2+0.1=0.30000000000000004 是浮点精度问题(所有语言共有)。数字可加下划线: 14_000_000_000。常量用全大写: MAX_CONNECTIONS=5000。'),
        ('SyntaxError', '语法错误: 单引号字符串里用撇号(如 \'Python\'s\')报 unterminated string literal, 改用双引号。'),
        ('注释与 Zen', '# 后面是注释。import this 查看 Python 之禅: 优美优于丑陋、简单优于复杂、可读性很重要。'),
    ],
    questions=[
        ("`4 / 2` 的结果是", ["A. 2.0", "B. 2", "C. 2.5", "D. 报错"], 0, "真除 / 总返回浮点数, 4/2=2.0。"),
        ("`0.2 + 0.1` 的结果是", ["A. 0.30000000000000004", "B. 0.3", "C. 0.2", "D. 0.1"], 0, "浮点精度问题, 所有编程语言共有, 不是 bug。"),
        ("`\"Ada Lovelace\".title()` 结果是", ["A. Ada Lovelace", "B. ada lovelace", "C. ADA LOVELACE", "D. Ada lovelace"], 0, "title() 把每个单词首字母大写。"),
        ("`14_000_000_000` 的值是", ["A. 14000000000", "B. 14", "C. 14000000", "D. 报错"], 0, "Python 存储时忽略下划线, 用于分组长数字。"),
        ("常量在 Python 中约定用", ["A. 全大写命名", "B. 全小写", "C. 驼峰", "D. 下划线结尾"], 0, "Python 没有内置常量类型, 用全大写变量名表示不应改变的值。"),
        ("含撇号的字符串应使用", ["A. 双引号", "B. 单引号", "C. 反引号", "D. 三引号"], 0, "单引号里写撇号会 SyntaxError, 用双引号包住: \"Python's\"。"),
        ("变量 `mesage` 与 `message` 拼写不一致会", ["A. NameError", "B. 正常运行", "C. SyntaxError", "D. 警告"], 0, "NameError: name 'mesage' is not defined。Python 不做拼写检查。"),
        ("变量命名错误的是", ["A. 2name", "B. name_1", "C. my_name", "D. name2"], 0, "变量名不能以数字开头。"),
    ],
    flashcards=[
        ("变量是标签", "贴在值上不是盒子。拼写一致即可, Python 不做拼写检查。"),
        ("f-string", "f\"Hello, {name}!\" 花括号里是活的。忘 f → 原样输出。"),
        ("浮点精度", "0.2+0.1=0.30000000000000004, 所有语言共有不是 bug。"),
        ("常量", "全大写: MAX_CONNECTIONS=5000。"),
    ],
    errors=[
        ("单引号内撇号", "'Python's' 报 SyntaxError。", "用双引号包住含撇号的字符串。"),
        ("strip 不重新赋值", "favorite_language.rstrip() 只是临时去除。", "要永久生效必须赋值: favorite_language = favorite_language.rstrip()。"),
        ("f-string 忘 f", "花括号变量名不被替换。", "字符串前加 f 前缀。"),
    ],
))

# ---- Ch3 列表简介 ----
CHAPTERS.append(dict(
    fname='python_ch3_interactive.html', title='第3章 列表简介', subtitle='Python 编程 · 第3章',
    key='zhaoli_py_ch3', color='#667eea',
    knowledge=[
        ('列表', '方括号 [] 定义、按特定顺序存储任意数量元素。列表通常含多个元素, 命名建议用复数: bicycles=[\'trek\', \'cannondale\']。'),
        ('索引', '从 0 开始! 第 n 个元素索引是 n-1。-1 永远返回最后一个元素, -2 倒数第二个。'),
        ('修改与添加', 'motorcycles[0]=\'ducati\' 改元素; append() 加末尾; insert(0, \'x\') 任意位置插入(其余右移)。'),
        ('删除元素', 'del motorcycles[0] 按索引删(拿不回值); pop() 删末尾并返回(还能用); remove(\'x\') 按值删(只删第一个)。原则: 删了还要用→pop, 删了不用→del。'),
        ('组织列表', 'sort() 永久排序; sorted() 临时排序(不改原列表); reverse() 永久反转(不是倒序排序)。len() 长度。'),
        ('IndexError', '访问不存在的索引: list index out of range。访问末尾永远用 -1。空列表访问 [-1] 也报错。'),
    ],
    questions=[
        ("`bicycles[0]` 返回", ["A. 第一个元素", "B. 第二个元素", "C. 最后一个", "D. 报错"], 0, "索引从 0 开始, [0] 是第一个元素。"),
        ("访问列表最后一个元素用", ["A. [-1]", "B. [last]", "C. [end]", "D. [len]"], 0, "-1 永远返回最后一个元素, 无需知道列表长度。"),
        ("`motorcycles.append(\"honda\")` 把元素加到", ["A. 末尾", "B. 开头", "C. 中间", "D. 随机位置"], 0, "append() 添加元素到末尾, 不影响其他元素。"),
        ("需要删除末尾元素并继续使用它, 应该用", ["A. pop()", "B. del", "C. remove()", "D. append()"], 0, "pop() 删除并返回该值; del 删了拿不回。原则: 还要用→pop。"),
        ("`cars.sort(reverse=True)` 的效果是", ["A. 永久按字母逆序排序", "B. 临时逆序", "C. 反转顺序", "D. 报错"], 0, "sort() 永久改变列表顺序, reverse=True 按逆序。"),
        ("`sorted(cars)` 与 cars.sort() 的区别是", ["A. sorted 不改原列表, sort 永久改", "B. 一样", "C. sorted 更慢", "D. sort 临时"], 0, "sorted() 返回排序副本, 原列表不变; sort() 永久改变。"),
        ("`motorcycles.remove(\"ducati\")` 删除的是", ["A. 第一个匹配值", "B. 所有匹配值", "C. 最后一个", "D. 索引 0"], 0, "remove() 按值删除, 只删除第一次出现的该值; 删全部需要循环。"),
        ("`reverse()` 的作用是", ["A. 把顺序倒过来(非排序)", "B. 按字母倒序", "C. 按数字排序", "D. 删除"], 0, "reverse() 只是倒过来, 不是排序。再调用一次可恢复原顺序。"),
    ],
    flashcards=[
        ("索引从 0", "第 n 个元素索引 n-1。-1 永远是最后一个。"),
        ("增删", "append 末尾 / insert 任意位置 / del 索引删 / pop 弹出并返回 / remove 按值删第一个。"),
        ("sort vs sorted", "sort 永久改; sorted 返回副本不改原列表。"),
    ],
    errors=[
        ("off-by-one", "第 3 个元素用索引 3。", "索引从 0 开始, 第 3 个元素是索引 2。"),
        ("空列表 [-1]", "空列表访问 [-1] 不报错。", "空列表访问任何索引(含 -1)都报 IndexError。"),
    ],
))

# ---- Ch4 列表操作 ----
CHAPTERS.append(dict(
    fname='python_ch4_interactive.html', title='第4章 使用列表', subtitle='Python 编程 · 第4章',
    key='zhaoli_py_ch4', color='#667eea',
    knowledge=[
        ('for 循环', 'for magician in magicians: 缩进块逐元素执行。缩进是语法! 循环后不缩进的代码只执行一次。'),
        ('缩进 4 类错误', '①忘记缩进→IndentationError ②只缩进部分行→逻辑错误 ③不必要缩进→unexpected indent ④循环后多缩进→汇总被重复打印。'),
        ('range()', '生成数字序列, 含头不含尾: range(1,5)→1,2,3,4。三个参数带步长: range(2,11,2)→偶数。list(range()) 转列表。'),
        ('列表统计', 'min()/max()/sum() 对百万级列表同样有效。'),
        ('列表解析', '一行生成列表: [x**2 for x in range(1,11)]。for 语句末尾没有冒号!'),
        ('切片', 'players[0:3] 含头不含尾; [ :4] 从头; [2:] 到末尾; [-3:] 最后 3 个。用于 Web 分页。'),
        ('复制列表', 'friend_foods = my_foods[:] 得到独立副本; friend_foods = my_foods 只是同一列表两个名字(互相影响)!'),
        ('元组', '不可变列表, 圆括号: dimensions=(200,50)。元素不可改(TypeError), 可整体重新赋值。单元素元组要尾随逗号 (3,)。'),
        ('PEP 8', '4 空格缩进(别混 Tab)、每行 ≤79 字符、空行分组代码块。'),
    ],
    questions=[
        ("`for value in range(1, 5):` 打印的值是", ["A. 1,2,3,4", "B. 1,2,3,4,5", "C. 0,1,2,3", "D. 2,3,4"], 0, "range 含头不含尾, 到 5 之前停止 → 1,2,3,4。"),
        ("`list(range(2, 11, 2))` 的结果是", ["A. [2,4,6,8,10]", "B. [2,4,6,8]", "C. [1,3,5,7,9]", "D. [2,3,4,5]"], 0, "步长 2 从 2 到 10(不含11) → 偶数。"),
        ("`[x**2 for x in range(1,4)]` 结果是", ["A. [1,4,9]", "B. [1,4,9,16]", "C. [1,2,3]", "D. [2,4,6]"], 0, "列表解析: x 取 1,2,3, x**2 → [1,4,9]。for 无冒号。"),
        ("复制列表得到独立副本的正确写法是", ["A. friend = my_foods[:]", "B. friend = my_foods", "C. friend = copy(my_foods)", "D. friend = my_foods[0]"], 0, "[:] 切片复制得到两个独立列表; 直接 = 指向同一列表。"),
        ("元组的定义符号是", ["A. 圆括号", "B. 方括号", "C. 花括号", "D. 尖括号"], 0, "元组用圆括号定义, 元素不可修改。"),
        ("`dimensions = (200, 50); dimensions[0] = 100` 会", ["A. TypeError", "B. 正常修改", "C. 静默忽略", "D. 创建新元组"], 0, "元组元素不可修改: TypeError: \'tuple\' object does not support item assignment。"),
        ("单元素元组必须写成", ["A. (3,)", "B. (3)", "C. [3]", "D. {3}"], 0, "元组本质上由逗号定义, 单元素元组必须加尾随逗号。"),
        ("循环结束后不缩进的代码执行", ["A. 一次", "B. 每个元素一次", "C. 两次", "D. 零次"], 0, "不缩进表示不在循环内, 只执行一次(常用于汇总)。"),
    ],
    flashcards=[
        ("range 含头不含尾", "range(1,5)→1,2,3,4。三个参数=步长。"),
        ("列表解析", "[x**2 for x in range(1,11)] 一行生成。for 无冒号。"),
        ("切片", "players[0:3] 含头不含尾; [-3:] 最后3个。"),
        ("复制用 [:]", "friend=my_foods[:] 独立副本; 直接 = 同一列表。"),
        ("元组", "圆括号不可变; 单元素要 (3,)。"),
    ],
    errors=[
        ("忘缩进", "for 后不缩进报 IndentationError。", "循环体必须缩进(4空格)。"),
        ("复制用 =", "两个变量指向同一列表互相影响。", "用切片 my_foods[:] 得到独立副本。"),
        ("改元组", "dimensions[0]=100 报 TypeError。", "元组不可变, 但可整体重新赋值。"),
    ],
))

# ---- Ch5 if ----
CHAPTERS.append(dict(
    fname='python_ch5_interactive.html', title='第5章 if 语句', subtitle='Python 编程 · 第5章',
    key='zhaoli_py_ch5', color='#667eea',
    knowledge=[
        ('条件测试', '求值为 True/False 的表达式。== 是问问题(比较), = 是下命令(赋值)。相等比较区分大小写, 用 lower() 忽略大小写。'),
        ('比较运算符', '== != < <= > >=。and 所有条件为 True 才 True; or 任一为 True 即 True。'),
        ('in / not in', '检查值是否在列表中: if user not in banned_users。用于注册查重、发帖查黑名单。'),
        ('if-elif-else', '按顺序测试直到第一个通过的分支, 执行后跳过其余。适合多分支单选。'),
        ('多个独立 if', '需要检查所有条件时用多个独立 if(如给每个人加不同优惠)。'),
        ('if 与列表', '循环中处理特殊值; if not list: 检查列表是否为空; 用多个列表校验输入合法性。'),
        ('布尔表达式', '布尔值只有 True/False, 常用于跟踪程序状态: game_active = True。'),
    ],
    questions=[
        ("条件测试中比较是否相等的运算符是", ["A. ==", "B. =", "C. equals", "D. is equal"], 0, "== 是比较(问问题), = 是赋值(下命令), 含义完全不同。"),
        ("`car = 'bmw'` 中 = 的作用是", ["A. 赋值", "B. 比较", "C. 相等", "D. 报错"], 0, "单个等号是赋值; 双等号是问是否相等。"),
        ("Python 中相等比较区分大小写, 忽略大小写用", ["A. lower() 转小写再比较", "B. 大写", "C. 无法忽略", "D. strip()"], 0, "先转小写再比较: car.lower() == 'bmw'。lower() 不修改原变量。"),
        ("`and` 组合条件的结果是", ["A. 所有条件为 True 才 True", "B. 任一为 True 即 True", "C. 永远 False", "D. 永远 True"], 0, "and 要求全部为 True; or 只要任一为 True。"),
        ("检查值是否在列表中用", ["A. in", "B. contains", "C. has", "D. inside"], 0, "in 检查成员: if user not in banned_users。"),
        ("if-elif-else 链的特点是", ["A. 只执行第一个通过的分支", "B. 执行所有分支", "C. 随机执行", "D. 都执行"], 0, "按顺序测试直到第一个通过, 执行该分支后跳过其余。"),
        ("需要检查所有条件时应该用", ["A. 多个独立 if", "B. if-elif-else", "C. if-else", "D. while"], 0, "if-elif-else 只执行一个; 检查所有条件用多个独立 if。"),
        ("`if not toppings:` 检查的是", ["A. 列表是否为空", "B. 列表是否很长", "C. 列表是否排序", "D. 列表是否含 0"], 0, "空列表在布尔判断中为 False, not 取反 → 判断是否为空。"),
    ],
    flashcards=[
        ("== vs =", "== 问问题(比较), = 下命令(赋值)。"),
        ("and/or", "and 全真才真; or 一真即真。"),
        ("in/not in", "成员检查: if user not in banned_users。"),
        ("if-elif-else", "只执行第一个通过的分支。"),
    ],
    errors=[
        ("= 当 ==", "if x = 5 想比较。", "用 if x == 5: 比较; = 是赋值。"),
        ("if-elif 全执行", "以为 if-elif 会检查所有分支。", "if-elif-else 只执行第一个通过的分支。"),
    ],
))

# ---- Ch6 字典 ----
CHAPTERS.append(dict(
    fname='python_ch6_interactive.html', title='第6章 字典', subtitle='Python 编程 · 第6章',
    key='zhaoli_py_ch6', color='#667eea',
    knowledge=[
        ('字典基础', '花括号键值对: alien_0={\'color\':\'green\',\'points\':5}。用 字典名[键] 取值。值可以是任何 Python 对象。'),
        ('增删改', '添加/修改: d[\'新键\']=新值; 删除: del d[\'键\'](永久删除不可恢复)。字典保留插入顺序。'),
        ('get() 安全取值', 'd[\'键\'] 不存在→KeyError。d.get(\'键\', 默认值) 安全; 省略默认返回 None(不是错误)。'),
        ('遍历', 'items() 遍历键值对; keys() 遍历键(默认行为); values() 遍历值; sorted() 排序; set() 去重。'),
        ('嵌套-列表的字典', '多个字典存入列表, 每个描述一个对象。用 range() 批量生成, 切片处理前几个, if 按条件修改。'),
        ('嵌套-字典的列表', '一个键对应多个值: 把列表作为字典的值, 双层 for 循环访问。'),
        ('嵌套-字典的字典', '用户名作外层键, 用户信息字典作值。外层循环拿 username 和 user_info, 再按内层键取值。'),
        ('集合 set', '花括号里只有元素(无冒号)是集合, 元素必须唯一, 不保留顺序。'),
    ],
    questions=[
        ("`alien_0['color']` 返回", ["A. green", "B. blue", "C. 报错", "D. 5"], 0, "字典用键取值: alien_0={'color':'green','points':5} → green。"),
        ("访问不存在的键会报", ["A. KeyError", "B. IndexError", "C. ValueError", "D. 返回 None"], 0, "方括号访问不存在的键 → KeyError。用 get() 规避。"),
        ("`alien_0.get('points', '无')` 键不存在时返回", ["A. 无", "B. 报错", "C. None", "D. 0"], 0, "get() 第二个参数是键不存在时返回的默认值。"),
        ("删除字典键值对用", ["A. del", "B. remove", "C. pop 必须", "D. delete"], 0, "del d['键'] 永久删除。"),
        ("遍历字典的所有键值对用", ["A. items()", "B. keys()", "C. values()", "D. pairs()"], 0, "items() 返回键值对序列, 用两个变量接收键和值。"),
        ("`for name in d:` 默认遍历的是", ["A. 键", "B. 值", "C. 键值对", "D. 长度"], 0, "遍历键是字典的默认行为, 与 d.keys() 等价。"),
        ("花括号 `{1, 2, 3}` 是", ["A. 集合", "B. 字典", "C. 列表", "D. 元组"], 0, "只有元素(无冒号)是集合; 带冒号键值对才是字典。"),
        ("字典中一个键对应多个值, 应使用", ["A. 列表作为值", "B. 数字", "C. 字符串", "D. 元组必须"], 0, "把列表作为字典的值, 双层 for 循环访问。"),
    ],
    flashcards=[
        ("字典", "花括号键值对。d['k'] 取值, del 删除。"),
        ("get()", "d.get('k',默认) 安全取值; 省略默认返回 None。"),
        ("遍历", "items 键值对 / keys 键 / values 值; sorted 排序; set 去重。"),
        ("嵌套", "列表的字典 / 字典的列表 / 字典的字典。"),
    ],
    errors=[
        ("KeyError", "方括号取不存在的键。", "用 get() 并提供默认值。"),
        ("集合 vs 字典", "以为 {1,2,3} 是字典。", "无冒号是集合, 有冒号键值对才是字典。"),
    ],
))

# ---- Ch7 输入与while ----
CHAPTERS.append(dict(
    fname='python_ch7_interactive.html', title='第7章 输入与 while', subtitle='Python 编程 · 第7章',
    key='zhaoli_py_ch7', color='#667eea',
    knowledge=[
        ('input()', '暂停程序等待用户输入, 返回字符串(永远!)。提示语末尾建议加空格: input(\"How old are you? \")。'),
        ('int() 转换', 'input() 返回 \'21\' 是字符串, 与数字比较报 TypeError, 必须 int(age) 转换。'),
        ('% 模运算符', '返回两数相除的余数, 判断奇偶: number % 2 == 0 为偶数。'),
        ('while 循环', '条件为真就重复执行, 循环体内必须有让条件最终为 False 的语句(如 +=)。'),
        ('退出值模式', '用哨兵值控制结束: while message != \'quit\': 循环变量必须先给初始值。'),
        ('flag 标志', '布尔变量代表\"是否继续运行\": active=True; 多个事件都可置 active=False 结束。'),
        ('break / continue', 'break 立即退出整个循环; continue 跳过本次循环剩余部分, 进入下一次。'),
        ('while 与列表/字典', '修改列表内容时用 while 而不是 for: 在列表间移动元素、删除全部指定值、用字典收集调查数据。'),
    ],
    questions=[
        ("`input()` 返回的值类型总是", ["A. 字符串", "B. 整数", "C. 浮点数", "D. 布尔值"], 0, "input() 永远返回字符串, 做数值运算必须先 int()/float() 转换。"),
        ("`age = int(age)` 的作用是", ["A. 字符串转整数", "B. 整数转字符串", "C. 取整", "D. 报错"], 0, "把 input() 返回的字符串 \'21\' 转换为数值 21。"),
        ("判断偶数用", ["A. n % 2 == 0", "B. n / 2 == 0", "C. n * 2", "D. n - 2"], 0, "% 取余, 余 0 为偶数。"),
        ("`while True:` 搭配什么退出循环?", ["A. break", "B. continue", "C. pass", "D. return"], 0, "while True 是无限循环, 用 break 退出。"),
        ("`continue` 的作用是", ["A. 跳过本次循环剩余部分", "B. 退出整个循环", "C. 结束程序", "D. 报错"], 0, "continue 跳过本次迭代, 进入下一次; break 退出整个循环。"),
        ("flag 模式中, `active = False` 的作用是", ["A. 结束循环", "B. 开始循环", "C. 打印", "D. 报错"], 0, "flag 是布尔变量, 置 False 表示程序不应继续, while 结束。"),
        ("删除列表中所有指定值, 应该用", ["A. while 循环", "B. for 循环", "C. del 一次", "D. remove 一次"], 0, "修改列表内容时用 while 而不是 for(remove 只删第一个, 循环删全部)。"),
        ("`while current_number <= 5:` 循环体内必须", ["A. 有让条件变 False 的语句", "B. 有 print", "C. 有 input", "D. 有 break"], 0, "否则死循环! 如 current_number += 1。"),
    ],
    flashcards=[
        ("input 字符串", "input() 永远返回字符串, 数值要 int() 转换。"),
        ("% 取余", "n % 2 == 0 是偶数。"),
        ("退出循环 4 法", "退出值 / flag / break / continue。"),
        ("while vs for", "修改列表用 while(移动/删除全部值)。"),
    ],
    errors=[
        ("input 忘转换", "直接和数字比较报 TypeError。", "int(input()) 转换后再运算。"),
        ("死循环", "while 条件永远为 True。", "循环体内要有让条件变 False 的语句(+=)。"),
    ],
))

# ---- Ch8 函数 ----
CHAPTERS.append(dict(
    fname='python_ch8_interactive.html', title='第8章 函数', subtitle='Python 编程 · 第8章',
    key='zhaoli_py_ch8', color='#667eea',
    knowledge=[
        ('定义函数', 'def 函数名(参数): 缩进块。docstring 三引号紧跟定义。def greet_user(): 必须有括号和冒号。'),
        ('形参 vs 实参', '形参(parameter)=定义中的变量, 实参(argument)=调用时传入的值。'),
        ('位置实参', '实参按定义中形参顺序一一对应, 顺序错了结果错乱。'),
        ('关键字实参', '调用时用 形参名=值: describe_pet(animal_type=\'hamster\', pet_name=\'harry\')。顺序无关, 名字必须精确。'),
        ('默认值', 'def describe_pet(pet_name, animal_type=\'dog\'): 有默认值的形参必须放在最后。'),
        ('return', '把值送回调用处, 调用时赋给变量。没有 return 的函数返回 None。'),
        ('*args / **kwargs', '*args 收任意数量实参打包成元组; **kwargs 收关键字实参打包成字典。必须放在参数最后。'),
        ('传递列表', '函数内修改列表是永久的(pop/append 影响原列表)。传副本用 [:], 但默认应传原列表。'),
        ('模块导入 5 种', 'import pizza; from pizza import make_pizza; 函数别名 mp; 模块别名 p; from pizza import *(不推荐, 可能覆盖)。'),
        ('可变默认参数陷阱', 'def add(item, lst=[]) 默认值只创建一次被共享累积! 应改用 None 占位。'),
    ],
    questions=[
        ("定义函数的关键字是", ["A. def", "B. function", "C. func", "D. define"], 0, "Python 用 def 定义函数。"),
        ("`def greet_user(username):` 中 username 是", ["A. 形参", "B. 实参", "C. 返回值", "D. 模块"], 0, "定义中的变量叫形参; 调用时传入的值叫实参。"),
        ("调用 `describe_pet(animal_type='hamster', pet_name='harry')` 是", ["A. 关键字实参", "B. 位置实参", "C. 默认值", "D. 形参"], 0, "用 形参名=值 调用是关键字实参, 顺序无关。"),
        ("`def f(a, b=10):` 中 b=10 是", ["A. 默认值参数", "B. 位置实参", "C. 关键字实参", "D. 任意参数"], 0, "b=10 是默认值; 有默认值的形参必须放在无默认值之后。"),
        ("没有 return 的函数返回", ["A. None", "B. 0", "C. False", "D. 报错"], 0, "没有 return 的函数返回 None(表示没有值)。"),
        ("`def make_pizza(*toppings):` 中 *toppings 把实参打包成", ["A. 元组", "B. 字典", "C. 列表", "D. 集合"], 0, "*args 把任意数量实参打包成元组; **kwargs 打包成字典。"),
        ("`def add_item(item, lst=[])` 的问题是", ["A. 默认列表被共享累积", "B. 语法错误", "C. 太慢", "D. 没问题"], 0, "可变默认参数陷阱: 默认值只创建一次, 多次调用共享。用 None 占位。"),
        ("函数内修改传入的列表会", ["A. 永久影响原列表", "B. 不影响", "C. 报错", "D. 复制后修改"], 0, "传列表给函数, 函数内改动永久影响原列表。要保护传副本 [:] 。"),
        ("`from pizza import *` 为什么不推荐?", ["A. 可能覆盖同名函数", "B. 太慢", "C. 会报错", "D. 不能导入"], 0, "导入全部可能覆盖当前文件同名函数。"),
        ("`from pizza import make_pizza as mp` 中 mp 是", ["A. 函数别名", "B. 模块别名", "C. 参数", "D. 返回值"], 0, "as mp 给函数起别名; import pizza as p 给模块起别名。"),
    ],
    flashcards=[
        ("形参实参", "形参=定义占位, 实参=调用传入值。"),
        ("关键字实参", "describe_pet(animal_type='hamster') 顺序无关, 名字精确。"),
        ("*args/**kwargs", "*收元组 **收字典, 必须放最后。"),
        ("模块导入", "import pizza / from pizza import fn / 别名 / import * 不推荐。"),
        ("可变默认参数", "def f(lst=None): if lst is None: lst=[]。"),
    ],
    errors=[
        ("默认值位置", "默认值参数放最前。", "有默认值的形参必须放在无默认值形参之后。"),
        ("实参数目不匹配", "少传/多传报 TypeError。", "按定义传参, 或使用默认值/关键字实参。"),
        ("可变默认参数", "def add(item, lst=[]) 共享累积。", "用 None 占位: def add(item, lst=None)。"),
    ],
))

# ---- Ch9 类 ----
CHAPTERS.append(dict(
    fname='python_ch9_interactive.html', title='第9章 类', subtitle='Python 编程 · 第9章',
    key='zhaoli_py_ch9', color='#667eea',
    knowledge=[
        ('类与实例', 'class 定义模板: class Dog:; __init__() 创建实例时自动运行初始化属性; self 指向实例本身(第一个参数自动传入)。my_dog=Dog(\'Willie\',6) 创建实例。'),
        ('属性与方法', '属性=实例数据, 点号访问 my_dog.name; 方法=实例行为, 调用加括号 my_dog.sit()。属性访问不加括号, 方法调用要加括号!'),
        ('修改属性 3 方式', '①直接赋值 my_car.odometer=23 ②通过方法改(可加校验, 如拒绝回拨里程) ③通过方法递增 increment_odometer(miles)。'),
        ('继承', 'class ElectricCar(Car): 子类; __init__ 里 super().__init__(...) 继承父类属性。可添加专属属性、重写父类方法。父类必须先定义。'),
        ('组合', '实例作为另一个类的属性: self.battery = Battery()。把复杂类拆小。\"是一个\"用继承, \"有一个\"用组合。'),
        ('导入类', 'from car import Car; from car import Car, ElectricCar; import car 用 car.Car。标准库: import random, random.choice/randint。'),
        ('random 模块', 'random.choice([1,-1]) 随机选; random.randint(1,6) 随机整数。'),
        ('类命名 PEP 8', '类名 CamelCase(首字母大写), 实例/变量小写下划线。'),
    ],
    questions=[
        ("类中 `__init__` 的作用是", ["A. 创建实例时初始化属性", "B. 删除实例", "C. 打印", "D. 导入"], 0, "__init__ 是特殊方法(两侧各两个下划线), 创建实例时自动调用。"),
        ("`self` 在类方法中指向", ["A. 实例本身", "B. 类", "C. 模块", "D. 父类"], 0, "self 指向实例本身, 是方法第一个参数, 自动传入。"),
        ("访问属性 vs 调用方法的区别是", ["A. 属性不加括号, 方法加括号", "B. 一样", "C. 属性加括号", "D. 方法不加"], 0, "属性访问 my_dog.name 不加括号; 方法调用 my_dog.sit() 要加括号。"),
        ("子类继承父类, 在 __init__ 中调用", ["A. super().__init__()", "B. parent.init()", "C. self.parent()", "D. base().__init__()"], 0, "super().__init__(...) 调用父类初始化, 继承父类全部属性。"),
        ("\"汽车有一个电池\" 应使用", ["A. 组合(实例作为属性)", "B. 继承", "C. 复制", "D. 导入"], 0, "\"有一个\"用组合; \"是一个\"用继承。"),
        ("`random.randint(1, 6)` 返回", ["A. 1-6 的随机整数", "B. 1-6 的随机浮点", "C. 随机列表", "D. 报错"], 0, "randint 返回 1 到 6 之间的随机整数(含端点)。"),
        ("修改属性值的方法二: 通过方法修改的好处是", ["A. 可加逻辑校验", "B. 更快", "C. 更慢", "D. 不需要"], 0, "方法内可加校验, 如拒绝回拨里程: if mileage >= self.odometer_reading。"),
        ("类的命名规范是", ["A. CamelCase 首字母大写", "B. 全小写", "C. 全大写", "D. 数字开头"], 0, "类名用 CamelCase(如 ElectricCar), 变量小写下划线。"),
    ],
    flashcards=[
        ("__init__/self", "__init__ 自动初始化; self 指向实例, 方法第一个参数。"),
        ("继承", "class ElectricCar(Car): super().__init__(...)。"),
        ("组合", "实例作为属性: self.battery=Battery()。\"有一个\"用组合。"),
        ("修改属性", "直接赋值 / 方法改(可校验) / 方法递增。"),
    ],
    errors=[
        ("忘 self", "类方法定义漏 self 参数。", "self 必须是类方法第一个参数(调用时不传)。"),
        ("属性方法混淆", "调用属性加括号。", "属性不加括号, 方法才加括号。"),
        ("__init__ 下划线", "写错下划线数量。", "__init__ 每侧两个下划线。"),
    ],
))

# ---- Ch10 文件与异常 ----
CHAPTERS.append(dict(
    fname='python_ch10_interactive.html', title='第10章 文件与异常', subtitle='Python 编程 · 第10章',
    key='zhaoli_py_ch10', color='#667eea',
    knowledge=[
        ('pathlib 读文件', 'from pathlib import Path; path=Path(\'a.txt\'); contents=path.read_text()。第3版用 pathlib 替代 open/with。'),
        ('rstrip 与方法链', 'read_text() 读到末尾返回空字符串, 用 rstrip() 去末尾空白。返回值上直接调方法叫方法链: contents=path.read_text().rstrip()。'),
        ('路径', '相对路径以程序目录为起点; 绝对路径从根写起。Windows 显示用 \\, 代码里写 /。read_text() 可加 encoding=\'utf-8\'。'),
        ('逐行处理', 'contents.splitlines() 按行拆列表, for 循环逐行。读出的都是字符串, 数值要 int()/float() 转换。'),
        ('write_text 写文件', 'path.write_text(contents) 写字符串。文件不存在自动创建; 已存在会先清空再写(覆盖!)。多行要拼 \'\\n\'。'),
        ('异常 try-except', 'try 放可能出错行, except 指定异常类型(ZeroDivisionError/FileNotFoundError), else 放依赖成功的结果。'),
        ('FileNotFoundError', '文件不存在/路径错/名字拼错都抛 FileNotFoundError。用 try-except 给出友好提示(不泄露 traceback)。'),
        ('pass 静默失败', 'except 里写 pass 什么都不做, 程序继续, 用户看不到错误。也作占位符。'),
        ('JSON 持久化', 'json.dumps() 对象→JSON 字符串, json.loads() 读回。dump/load 配文件对象, dumps/loads 配字符串。'),
        ('多文件处理', '把逻辑封装成函数, for 循环处理文件列表; 某文件缺失不影响其他(else 块保证)。'),
    ],
    questions=[
        ("第3版读取文件的推荐方式是", ["A. pathlib.Path + read_text()", "B. open() + read()", "C. file() 函数", "D. import 文件"], 0, "第3版用 pathlib: path=Path('a.txt'); path.read_text()。"),
        ("`path.read_text().rstrip()` 是", ["A. 方法链", "B. 循环", "C. 赋值", "D. 报错"], 0, "在返回值上直接调用方法叫方法链。"),
        ("`write_text()` 对已存在文件", ["A. 先清空再覆盖", "B. 追加", "C. 报错", "D. 跳过"], 0, "文件已存在时 write_text() 会先清空原内容再写(覆盖!)。"),
        ("`5 / 0` 抛出的异常是", ["A. ZeroDivisionError", "B. FileNotFoundError", "C. KeyError", "D. IndexError"], 0, "除以零 → ZeroDivisionError。"),
        ("文件不存在抛出的异常是", ["A. FileNotFoundError", "B. ZeroDivisionError", "C. KeyError", "D. TypeError"], 0, "文件不存在/路径错 → FileNotFoundError。"),
        ("try-except-else 中 else 块放", ["A. 依赖 try 成功的代码", "B. 可能出错的代码", "C. 所有代码", "D. 错误处理"], 0, "try 只放可能出错的行, else 放依赖成功的结果。"),
        ("`json.dumps()` 的作用是", ["A. Python对象→JSON字符串", "B. JSON→对象", "C. 打印", "D. 删除"], 0, "dumps=导出(对象→字符串), loads=加载(字符串→对象)。"),
        ("except 中写 `pass` 表示", ["A. 静默失败, 程序继续", "B. 崩溃", "C. 重试", "D. 打印错误"], 0, "pass 什么都不做, 程序继续运行, 用户看不到错误提示。"),
        ("从文本文件读出的数字需要", ["A. int()/float() 转换", "B. 直接运算", "C. str() 转换", "D. 不用处理"], 0, "读出的所有内容都是字符串, 数值运算必须先转换。"),
        ("多行写入文件要", ["A. 拼成带 \\n 的完整字符串", "B. 多次 write_text", "C. 用 append", "D. 无法实现"], 0, "write_text() 接收一个字符串, 多行要自己拼 \'\\n\'。"),
    ],
    flashcards=[
        ("pathlib", "Path('a.txt').read_text() 读 / write_text() 写(覆盖)。"),
        ("try-except-else", "try 可能出错行, except 捕获, else 依赖成功。"),
        ("FileNotFoundError", "文件不存在 → 友好提示, 不泄露 traceback。"),
        ("JSON", "dumps 导出 / loads 加载; dump/load 配文件。"),
        ("pass", "静默失败, 程序继续。"),
    ],
    errors=[
        ("裸 except", "except: 吞掉所有错误。", "指定异常类型: except FileNotFoundError: 或 except Exception as e。"),
        ("write_text 覆盖", "以为写文件是追加。", "write_text 会先清空再写。追加要读出拼好再写。"),
        ("数字当字符串", "文件读出的数字直接运算。", "int()/float() 转换后再运算。"),
    ],
))

# ---- Ch11 测试 ----
CHAPTERS.append(dict(
    fname='python_ch11_interactive.html', title='第11章 测试你的代码', subtitle='Python 编程 · 第11章',
    key='zhaoli_py_ch11', color='#667eea',
    knowledge=[
        ('pytest 安装', 'python -m pip install --user pytest。pytest 是第三方包, Python 默认不含。'),
        ('命名约定', '测试文件名 test_ 开头, 测试函数名 test_ 开头, pytest 才会收集运行。函数名要描述性。'),
        ('assert 断言', 'assert 条件: True 通过, False 失败。常用: assert a==b、assert element in list、assert not a。'),
        ('运行 pytest', '在测试目录运行 pytest; 输出 . 表示通过, F 表示失败。pytest test_survey.py 只跑指定文件。'),
        ('失败应对', '通过=函数行为正确, 失败=被测代码有错。不要改测试来让它通过! 要修复被测代码(如把必填参数改成可选)。'),
        ('测试类', '测类=验证方法行为: 创建实例 → 调用方法 → 断言状态。'),
        ('fixture', '@pytest.fixture 装饰器复用测试资源, 避免重复代码。'),
        ('测试的意义', '改代码时立刻发现是否破坏已有功能, 比收到 bug 报告再修容易得多。'),
    ],
    questions=[
        ("测试文件命名必须以什么开头?", ["A. test_", "B. check_", "C. verify_", "D. 任意"], 0, "pytest 只收集 test_ 开头的文件和函数。"),
        ("测试函数中验证行为用", ["A. assert", "B. print", "C. return", "D. pass"], 0, "assert 断言: 条件为 True 通过, False 失败。"),
        ("`assert element in list` 的含义是", ["A. 元素在列表中", "B. 元素不在", "C. 列表为空", "D. 列表排序"], 0, "断言元素在列表中, 否则测试失败。"),
        ("pytest 输出中 F 表示", ["A. 测试失败", "B. 通过", "C. 跳过", "D. 完成"], 0, ". 表示通过, F 表示失败, 100% 是进度。"),
        ("测试失败时正确的做法是", ["A. 修复被测代码", "B. 修改测试让它通过", "C. 删除测试", "D. 忽略"], 0, "不要改测试来让它通过, 要修复被测代码。"),
        ("pytest 的 fixture 用于", ["A. 复用测试资源", "B. 定义变量", "C. 输出", "D. 安装"], 0, "@pytest.fixture 复用共享数据, 避免重复代码。"),
        ("`get_formatted_name('janis', 'joplin') == 'Janis Joplin'` 是", ["A. 断言", "B. 循环", "C. 导入", "D. 报错"], 0, "断言函数输出符合预期。"),
        ("测试的意义是", ["A. 改代码时发现破坏", "B. 让代码变慢", "C. 替代文档", "D. 无意义"], 0, "改代码时立刻发现是否破坏已有功能。"),
    ],
    flashcards=[
        ("命名", "test_ 开头的文件和函数, pytest 自动收集。"),
        ("assert", "断言条件; 常用 ==、in、not。"),
        ("失败不改测试", "修复被测代码, 别改测试让它通过。"),
        ("fixture", "@pytest.fixture 复用资源。"),
    ],
    errors=[
        ("测试命名错", "函数不叫 test_ 开头。", "pytest 只跑 test_ 开头的文件和函数。"),
        ("改测试让它过", "测试失败就改断言。", "断言正确就修被测代码, 否则所有调用都悄悄坏掉。"),
    ],
))

# ---- Ch12-14 项目1: 外星人入侵 ----
CHAPTERS.append(dict(
    fname='python_ch12_interactive.html', title='项目1 外星人入侵(pygame)', subtitle='Python 编程 · 项目1',
    key='zhaoli_py_ch12', color='#9b59b6',
    knowledge=[
        ('pygame 基础', 'pip install pygame。游戏循环: 处理事件→更新位置→绘制屏幕。窗口/事件循环/rect 定位。'),
        ('Settings 类', '把游戏设置集中到一个类(屏幕尺寸、颜色、速度), 便于统一修改。'),
        ('rect 定位', 'pygame.Rect 用 rect.x/rect.y 控制位置, 支持 centerx/centery/midbottom 等属性定位。移动速度用 float 存, 再赋给 rect(避免精度问题)。'),
        ('按键移动', '事件循环里 KEYDOWN/KEYUP 检测方向键, 用 flag(moving_right=True) 跟踪按键状态。'),
        ('Bullet + Group', '子弹类继承 Sprite, pygame.sprite.Group 管理所有子弹。更新+绘制+删除出界子弹。'),
        ('外星人舰队', '用嵌套循环生成网格状舰队, 边缘转向(全部外星人右移并下降)。'),
        ('碰撞检测', 'pygame.sprite.groupcollide(子弹, 外星人, True, True) 比较两组 rect, 返回碰撞字典。spritecollideany 检测飞船与外 星人。'),
        ('GameStats 与 game_active', 'GameStats 类跟踪游戏统计(reset_stats 与 __init__ 分离: 每局重置 vs 全局)。game_active 控制游戏是否继续。'),
        ('计分系统', 'groupcollide 返回的字典 value 是子弹命中的所有外星人列表, 遍历 values 用 len(aliens) 保证每次命中都计分。'),
        ('难度递增', 'speedup_scale 随分数提高逐渐加快速度, 每波外星人消灭后升级。'),
        ('Play 按钮与最高分', 'Play 按钮开始游戏; 最高分写入文件持久化; Scoreboard 类显示得分/最高分/等级。'),
    ],
    questions=[
        ("pygame 游戏循环的典型顺序是", ["A. 处理事件→更新→绘制", "B. 绘制→处理→更新", "C. 更新→绘制→处理", "D. 随机"], 0, "游戏循环: 处理事件 → 更新位置 → 绘制屏幕。"),
        ("pygame 中控制对象位置的类是", ["A. pygame.Rect", "B. pygame.Font", "C. pygame.Color", "D. pygame.Sound"], 0, "Rect 用 rect.x/rect.y 控制位置。"),
        ("为什么移动速度用 float 存再赋给 rect?", ["A. 避免精度问题", "B. 更快", "C. 必须", "D. 无原因"], 0, "float 保证平滑移动, rect 需要整数坐标。"),
        ("`pygame.sprite.groupcollide(bullets, aliens, True, True)` 中两个 True 表示", ["A. 同时删除碰撞的子弹和外星人", "B. 保留两者", "C. 只删子弹", "D. 只删外星人"], 0, "两个 True = 同时删除碰撞的子弹和外星人。"),
        ("game_active 变量的作用是", ["A. 控制游戏是否继续", "B. 控制速度", "C. 计分", "D. 音效"], 0, "game_active 为 False 时游戏结束。"),
        ("游戏统计中\"每局重置\"与\"全局不变\"分离用", ["A. reset_stats 与 __init__ 分离", "B. 一个变量", "C. 硬编码", "D. 全局变量"], 0, "GameStats 的 reset_stats() 与 __init__() 分离, 每局重置/全局区分。"),
        ("宽子弹一次穿透多个外星人, 计分要", ["A. 遍历 value 列表用 len()", "B. 只加一分", "C. 不算", "D. 随机"], 0, "collisions 字典 value 是命中的外星人列表, len(aliens) 保证全计分。"),
        ("游戏难度递增通过", ["A. speedup_scale 提高速度", "B. 减小窗口", "C. 删除代码", "D. 降低帧率"], 0, "每波消灭后 speedup_scale 加速, 难度递增。"),
    ],
    flashcards=[
        ("游戏循环", "处理事件 → 更新 → 绘制。"),
        ("Settings 类", "集中管理所有设置, 便于统一修改。"),
        ("groupcollide", "子弹vs外星人碰撞, True=True 双删。"),
        ("GameStats", "reset_stats 每局重置, __init__ 全局统计。"),
        ("计分", "遍历碰撞字典 values 用 len() 全计分。"),
    ],
    errors=[
        ("整型移动", "rect.x 直接加减整数导致移动不平滑。", "用 float 存速度再赋给 rect。"),
        ("忘记删除出界子弹", "子弹一直留着内存膨胀。", "更新时删除 rect.bottom < 0 的子弹。"),
        ("碰撞只删一侧", "groupcollide 参数设错。", "两个 True 双删, 否则残留。"),
    ],
))

# ---- Ch18-20 项目3: Django ----
CHAPTERS.append(dict(
    fname='python_ch18_interactive.html', title='项目3 Django Web 应用', subtitle='Python 编程 · 项目3',
    key='zhaoli_py_ch18', color='#27ae60',
    knowledge=[
        ('虚拟环境', 'python -m venv ll_env 创建隔离环境; 激活: source ll_env/bin/activate(Windows: ll_env\\Scripts\\activate); deactivate 退出。部署项目必需。'),
        ('创建 Django 项目', 'pip install django; django-admin startproject ll_project . (末尾点号很重要, 当前目录即项目根)。生成 manage.py 和 ll_project/(settings.py/urls.py/wsgi.py)。'),
        ('数据库与迁移', 'python manage.py migrate 用 SQLite 自动建库(db.sqlite3)。迁移=任何修改数据库的操作。'),
        ('runserver', 'python manage.py runserver 本地开发服务器(localhost:8000), 仅本机可访问。端口占用用 8001。'),
        ('startapp 创建应用', 'python manage.py startapp learning_logs。项目=网站整体配置, 应用=完成具体功能的一组文件。models.py 定义数据, admin.py 注册后台, views.py 视图。'),
        ('模型 models.py', 'class Topic(models.Model): 继承 models.Model。CharField 短文本(max_length 必填), DateTimeField 日期时间(auto_now_add=True 自动记录创建时刻), __str__() 定义字符串表示。'),
        ('激活模型三步', '①settings.py 的 INSTALLED_APPS 注册应用 ②python manage.py makemigrations learning_logs ③python manage.py migrate。修改数据固定三步: 改 models → makemigrations → migrate。'),
        ('管理后台', 'python manage.py createsuperuser 创建超级用户(密码哈希存储); admin.py 注册自己的模型(Django 内置 User/Group 自动注册)。'),
        ('URL-视图-模板', '定义 URL → 编写视图 → 编写模板 三步法。模板继承 base.html 复用布局。'),
        ('用户账户', 'forms.py 定义 ModelForm; 处理 GET-POST; 模板 csrf_token; 用户认证; @login_required 限制登录用户; owner 外键让用户只看自己的数据。'),
        ('样式与部署', 'Bootstrap 美化(django_bootstrap5); 部署 Platform.sh; DEBUG=False; 404/500 自定义页面。'),
        ('MVT 模式', 'Model(数据)→View(逻辑)→Template(展示) 三层分离; URL 负责路由。URL 找视图, 视图取模型, 模板画页面。Django 的 View ≈ MVC 的 Controller。'),
    ],
    questions=[
        ("创建虚拟环境的命令是", ["A. python -m venv ll_env", "B. pip install venv", "C. django-admin startproject", "D. python manage.py runserver"], 0, "venv 创建隔离环境, 激活后安装包不影响系统。ll_env 是两小写 L。"),
        ("`django-admin startproject ll_project .` 末尾点号的作用是", ["A. 当前目录即项目根", "B. 创建隐藏文件", "C. 必须删掉", "D. 无作用"], 0, "点号让新项目以当前目录为根, 方便部署; 忘记会导致部署配置问题。"),
        ("首次迁移创建数据库用的引擎是", ["A. SQLite", "B. MySQL", "C. PostgreSQL", "D. Oracle"], 0, "migrate 用 SQLite 自动建库(db.sqlite3), 适合简单应用。"),
        ("`python manage.py runserver` 启动的是", ["A. 本地开发服务器", "B. 公网服务器", "C. 数据库", "D. 编辑器"], 0, "localhost 本地预览, 仅本机可访问。"),
        ("`CharField` 必须指定", ["A. max_length", "B. default", "C. null", "D. blank"], 0, "CharField 存短文本, 必须指定 max_length。"),
        ("模型修改后的固定三步是", ["A. 改models→makemigrations→migrate", "B. 改views→改urls→改模板", "C. 删除→重建→重启", "D. 安装→卸载→安装"], 0, "改 models.py → 跑 makemigrations → 跑 migrate。"),
        ("创建管理后台超级用户的命令是", ["A. createsuperuser", "B. createadmin", "C. superuser", "D. adduser"], 0, "python manage.py createsuperuser, 密码以哈希存储。"),
        ("Django 的 MVT 中 V 是", ["A. View 视图(逻辑)", "B. Value", "C. Variable", "D. Vector"], 0, "MVT: Model→View→Template。URL 找视图, 视图取模型, 模板画页面。"),
        ("限制页面只允许登录用户访问用", ["A. @login_required", "B. @admin_only", "C. @private", "D. @secure"], 0, "@login_required 装饰器限制登录用户访问。"),
        ("让用户只能看到自己的数据, 模型用", ["A. owner 外键", "B. 全局变量", "C. 硬编码", "D. 缓存"], 0, "owner 外键关联 User 模型, 视图按当前用户过滤。"),
    ],
    flashcards=[
        ("虚拟环境", "python -m venv ll_env; source 激活; deactivate 退出。"),
        ("项目 vs 应用", "项目=整体配置, 应用=具体功能(learning_logs)。"),
        ("模型三步", "改 models → makemigrations → migrate。"),
        ("MVT", "Model 数据 / View 逻辑 / Template 展示; URL 路由。"),
        ("三步法", "定义 URL → 编写视图 → 编写模板。"),
    ],
    errors=[
        ("忘点号", "startproject 末尾漏 . 导致部署配置问题。", "django-admin startproject ll_project . 点号必须有。"),
        ("漏 csrf_token", "POST 表单模板没有 csrf_token 报错。", "表单模板加 {% csrf_token %}。"),
        ("迁移忘跑", "改了 models 不迁移, 数据库没更新。", "改 models → makemigrations → migrate 三步。"),
    ],
))

# 汇总: 20 章 = Ch1-11 + 项目1(12-14) + 项目2(15-17, 已有ai_dataviz) + 项目3(18-20)
# 已有页复用: python_basics=Ch1-2合并? 不, 现在按章节独立, 用新页面覆盖目录
print(f"共定义 {len(CHAPTERS)} 个章节数据")
