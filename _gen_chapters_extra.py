# -*- coding: utf-8 -*-
"""补充章节数据: Ch13/Ch14/Ch16/Ch17/Ch19/Ch20 (基于蒸馏笔记拆章)"""
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

EXTRA_CHAPTERS = []

# ---- Ch13 外星人! ----
EXTRA_CHAPTERS.append(dict(
    fname='python_ch13_interactive.html', title='第13章 外星人!', subtitle='Python 编程 · 项目1',
    key='zhaoli_py_ch13', color='#9b59b6',
    knowledge=[
        ('Alien 类', 'class Alien(Sprite): 继承 Sprite, 加载图片 alien.bmp, rect 定位。位置默认左上角(左边距=自身宽度, 上边距=自身高度)。只需精确跟踪水平位置 self.x。'),
        ('创建舰队', '嵌套循环: 内层按 x 填满一行(间距=一个外星人宽, 右留2宽), 外层按 y 逐行(行距=一个外星人高, 底部留3高给飞船)。每行结束重置 current_x、递增 current_y。'),
        ('舰队移动', 'fleet_direction 用 1(右)/-1(左) 数值而非字符串, 方便直接乘坐标: self.x += alien_speed * fleet_direction。'),
        ('边缘转向', 'check_edges() 检测是否碰到左右边缘; 碰到时整个舰队下移 fleet_drop_speed 并反转方向(fleet_direction *= -1, 只反转一次, 不在 for 内)。'),
        ('groupcollide 碰撞', 'pygame.sprite.groupcollide(bullets, aliens, True, True) 比较两组 rect, 返回字典(key=子弹, value=被击中外星人列表)。两个 True=同时删除碰撞的子弹和外星人。'),
        ('舰队重建', 'if not self.aliens: 空组求值为 False; 清掉剩余子弹 self.bullets.empty(), 重新生成舰队 _create_fleet()。'),
        ('spritecollideany', 'pygame.sprite.spritecollideany(ship, aliens) 返回与飞船碰撞的第一个外星人(无碰撞返回 None)。'),
        ('GameStats 类', '单独成类跟踪游戏统计。reset_stats() 与 __init__() 分离: 每局重置(ships_left=ship_limit) vs 全局不变。'),
        ('_ship_hit()', '飞船被撞: ships_left -= 1, 清空子弹和外星人, 重建舰队, 飞船居中, time.sleep(0.5) 暂停半秒。整局只创建一个飞船实例, 被撞后重复居中复用。'),
        ('外星人触底', '逐只检查 alien.rect.bottom >= screen_height, 触底与撞船同等处理(调用 _ship_hit()), 找到一个即 break。'),
        ('game_active', '游戏状态标志。ships_left 用尽 → game_active = False。主循环中事件检查和画面更新始终执行, 元素位置更新仅在激活时执行。'),
    ],
    questions=[
        ("Alien 类应继承", ["A. pygame.sprite.Sprite", "B. pygame.Rect", "C. object", "D. pygame.Font"], 0, "Alien(Sprite) 继承 Sprite, 可加入 sprite.Group 统一管理。"),
        ("舰队方向用 1/-1 而不是字符串的好处是", ["A. 直接乘到坐标上", "B. 更美观", "C. 更快", "D. 必须"], 0, "fleet_direction 数值可直接乘: self.x += alien_speed * fleet_direction。"),
        ("`pygame.sprite.groupcollide(bullets, aliens, True, True)` 两个 True 表示", ["A. 同时删除碰撞的子弹和外星人", "B. 保留两者", "C. 只删子弹", "D. 只删外星人"], 0, "两个 True = 双删。若子弹 False、外星人 True 就是穿透型\"强力子弹\"。"),
        ("`if not self.aliens:` 判断的是", ["A. 外星人组是否为空", "B. 外星人数量", "C. 飞船状态", "D. 分数"], 0, "空 sprite.Group 求值为 False, not 取反 → 舰队全灭。"),
        ("`pygame.sprite.spritecollideany(ship, aliens)` 返回", ["A. 碰撞的第一个外星人或 None", "B. 所有外星人", "C. 飞船", "D. 布尔值"], 0, "返回与指定精灵碰撞的组内第一个成员, 无碰撞返回 None。"),
        ("GameStats 中 `reset_stats()` 与 `__init__()` 分离是为了", ["A. 区分每局重置与全局统计", "B. 减少代码", "C. 加快速度", "D. 无原因"], 0, "ships_left 每局重置; 最高分等全局不变。"),
        ("`_ship_hit()` 中 `time.sleep(0.5)` 的作用是", ["A. 暂停半秒让玩家看清碰撞", "B. 减少 CPU", "C. 加载资源", "D. 无作用"], 0, "让玩家看清发生了什么再继续。"),
        ("外星人触底时处理方式是", ["A. 与撞船同等(调用 _ship_hit)", "B. 忽略", "C. 加分", "D. 加速"], 0, "触底与撞船同等处理: _ship_hit(), 找到第一个即 break。"),
    ],
    flashcards=[
        ("Alien(Sprite)", "继承 Sprite, 加载图片, 精确跟踪 self.x。"),
        ("舰队生成", "嵌套循环: 内层填行, 外层逐行。间距=外星人尺寸。"),
        ("fleet_direction", "1/-1 数值控制方向, 直接乘坐标。"),
        ("groupcollide", "子弹vs外星人, 双 True 双删; 返回碰撞字典。"),
        ("GameStats", "reset_stats 每局重置 / __init__ 全局统计。"),
        ("game_active", "ships_left 用尽游戏结束。"),
    ],
    errors=[
        ("方向反转在 for 内", "每只外星人都反转一次方向。", "碰到边缘只反转一次: _change_fleet_direction 中循环外 fleet_direction *= -1。"),
        ("重建舰队忘清子弹", "舰队重建后旧子弹残留。", "self.bullets.empty() 清掉剩余子弹。"),
        ("碰撞只删一侧", "groupcollide 参数设错。", "两个 True 双删。"),
    ],
))

# ---- Ch14 计分 ----
EXTRA_CHAPTERS.append(dict(
    fname='python_ch14_interactive.html', title='第14章 计分', subtitle='Python 编程 · 项目1',
    key='zhaoli_py_ch14', color='#9b59b6',
    knowledge=[
        ('Play 按钮 Button 类', 'pygame 没有内置按钮, 自己写\"填充色矩形+文字标签\"的通用类。pygame.font.SysFont(None, 48) 创建字体, font.render(msg, True, 颜色) 渲染文字(第二参数抗锯齿)。'),
        ('按钮显示逻辑', '游戏默认 game_active=False 启动; _update_screen() 中 if not self.game_active: draw_button() 仅在未激活时绘制。'),
        ('鼠标点击检测', 'pygame.MOUSEBUTTONDOWN 事件; pygame.mouse.get_pos() 取坐标; rect.collidepoint(pos) 判断是否在按钮内。'),
        ('防误点重启', 'if button_clicked and not self.game_active: 防止游戏中误点按钮重启。点开始后 pygame.mouse.set_visible(False) 隐藏光标。'),
        ('难度递增', 'Settings 分两类: __init__() 静态设置 + initialize_dynamic_settings() 动态设置(速度/方向/分值)。speedup_scale=1.1 每清空一波全提速, increase_speed() 递增。'),
        ('计分系统', '每个外星人 50 分(alien_points), 随关卡按 score_scale=1.5 增长。碰撞字典 value 是外星人列表, 遍历 values 用 len(aliens) 保证每次命中都计分。'),
        ('Scoreboard 类', 'pygame.font 把分数渲染成图像显示。分数四舍五入到 10, 加千分位逗号。'),
        ('最高分与关卡', 'GameStats 记录最高分(本局内存)和当前关卡; 每清空一波 level += 1。'),
        ('飞船图标组', '用缩小的飞船图标组显示剩余飞船数。'),
    ],
    questions=[
        ("pygame 中 Play 按钮需要", ["A. 自己写 Button 类", "B. 内置按钮", "C. 系统按钮", "D. 网页按钮"], 0, "pygame 没有内置按钮, 自己写\"矩形+文字\"通用类。"),
        ("`pygame.font.SysFont(None, 48)` 创建的是", ["A. 字体对象", "B. 图像", "C. 矩形", "D. 颜色"], 0, "SysFont 创建字体, 用 font.render() 渲染成图像。"),
        ("检测鼠标点击是否在按钮内用", ["A. rect.collidepoint(pos)", "B. mouse.click()", "C. rect.contains()", "D. pos == rect"], 0, "pygame.mouse.get_pos() 取坐标, collidepoint() 判断。"),
        ("`if button_clicked and not self.game_active` 防止", ["A. 游戏中误点重启", "B. 重复加分", "C. 外星人穿墙", "D. 音效重叠"], 0, "防止按钮区域在游戏进行中仍响应点击。"),
        ("speedup_scale=1.1 的作用是", ["A. 每清空一波全游戏提速", "B. 加快渲染", "C. 提高分辨率", "D. 增加音效"], 0, "每清空一波舰队调用 increase_speed(), 速度按 1.1 倍递增。"),
        ("宽子弹一次穿多个外星人, 计分要", ["A. 遍历 values 用 len() 全计", "B. 只加一分", "C. 不算", "D. 随机"], 0, "collisions.values() 是外星人列表, len(aliens) 保证每次命中都计分。"),
        ("每个外星人基础分值(alien_points)是", ["A. 50", "B. 10", "C. 100", "D. 5"], 0, "alien_points = 50, 随关卡按 score_scale=1.5 增长。"),
        ("游戏结束时鼠标光标", ["A. 重现 set_visible(True)", "B. 一直隐藏", "C. 消失", "D. 变颜色"], 0, "_ship_hit() 中游戏结束时 pygame.mouse.set_visible(True) 让光标重现。"),
    ],
    flashcards=[
        ("Button 类", "矩形+文字; SysFont+render; collidepoint 检测点击。"),
        ("动态设置", "initialize_dynamic_settings() 复位难度; speedup_scale 提速。"),
        ("计分", "50分/外星人, score_scale=1.5; len(aliens) 全计分。"),
        ("Scoreboard", "pygame.font 渲染分数; 千分位逗号; 最高分/关卡。"),
        ("游戏流程", "Play 按钮开始 → 清空战场 → 重建舰队 → 隐藏光标。"),
    ],
    errors=[
        ("防误点", "游戏中点按钮区域触发重启。", "加 not self.game_active 条件。"),
        ("漏 speedup_scale", "难度不递增, 游戏单调。", "每清空一波调用 increase_speed() 并 level += 1。"),
        ("计分只加一分", "宽子弹穿多个只算一分。", "遍历 collisions.values() 用 len(aliens) 全计。"),
    ],
))

# ---- Ch16 下载数据 ----
EXTRA_CHAPTERS.append(dict(
    fname='python_ch16_interactive.html', title='第16章 下载数据', subtitle='Python 编程 · 项目2',
    key='zhaoli_py_ch16', color='#e67e22',
    knowledge=[
        ('CSV 格式', '逗号分隔值: \"USW00025333\",\"SITKA AIRPORT, AK US\",\"2021-01-01\",,\"44\",\"40\"。用 Path.read_text().splitlines() 读成行列表。'),
        ('csv.reader', 'csv.reader(lines) 创建解析器; next(reader) 返回下一行(第一次=表头)。用 enumerate() 打印表头索引。'),
        ('提取数据', 'reader 从当前位置继续, 表头读完循环直接从第二行开始。CSV 读出的都是字符串, 用 int() 转数值: high = int(row[4])。'),
        ('日期解析', 'datetime.strptime(\'2021-07-01\', \'%Y-%m-%d\') 把日期字符串转成日期对象。格式符: %Y 四位年、%m 月、%d 日、%A 星期名、%B 月份名。'),
        ('autofmt_xdate', 'fig.autofmt_xdate() 把日期标签斜排, 防止重叠。'),
        ('双数据与 alpha', '高温红、低温蓝: ax.plot(dates, highs, color=\'red\')。alpha 控制透明度(0全透明, 1不透明)。'),
        ('fill_between', 'ax.fill_between(dates, highs, lows, facecolor=\'blue\', alpha=0.1) 填充两序列之间, 展示每日温差。'),
        ('缺失数据处理', '不同站点列索引不同(Sitka TMAX@4, Death Valley @3), 空字符串转 int 抛 ValueError → try-except-else 处理。'),
        ('JSON 处理', 'json.loads(contents) 字符串→对象; json.dumps(obj, indent=4) 对象→易读字符串。'),
        ('GeoJSON 结构', 'metadata → features(列表, 每项=一个地震) → 每项含 properties(mag/title) 和 geometry(coordinates: [经度, 纬度, 深度])。'),
        ('px.scatter_geo', '世界地图: scatter_geo(lat=lats, lon=lons)。size=mags 按震级控大小, color=mags 着色, hover_name 定制悬停。'),
    ],
    questions=[
        ("CSV 文件中下一行数据用", ["A. next(reader)", "B. reader.read()", "C. reader[0]", "D. reader.pop()"], 0, "next(reader) 返回下一行, 第一次调用返回表头。"),
        ("打印表头及其索引用", ["A. enumerate()", "B. range()", "C. len()", "D. max()"], 0, "for index, column_header in enumerate(header_row): 打印索引和列名。"),
        ("CSV 读出的数据转数值用", ["A. int()", "B. str()", "C. bool()", "D. 不用转"], 0, "CSV 读出的都是字符串, 用 int() 转数值。"),
        ("`datetime.strptime('2021-07-01', '%Y-%m-%d')` 把", ["A. 字符串转日期对象", "B. 日期转字符串", "C. 数字转日期", "D. 报错"], 0, "strptime 按格式把字符串解析为日期对象。"),
        ("防止日期标签重叠用", ["A. fig.autofmt_xdate()", "B. plt.show()", "C. ax.grid()", "D. plt.savefig()"], 0, "autofmt_xdate() 把日期标签斜排。"),
        ("填充两条线之间区域用", ["A. ax.fill_between(dates, highs, lows)", "B. ax.fill()", "C. ax.area()", "D. plt.shade()"], 0, "fill_between 填充两 y 序列之间的空间, 展示温差范围。"),
        ("GeoJSON 中 coordinates[0] 是", ["A. 经度", "B. 纬度", "C. 深度", "D. 震级"], 0, "GeoJSON 采用(经度, 纬度)即(x, y)约定, 搞反会画到错误位置!"),
        ("空字符串转 int 抛出的异常是", ["A. ValueError", "B. KeyError", "C. IndexError", "D. TypeError"], 0, "空字符串 '' 转 int 抛 ValueError, 用 try-except-else 处理缺失数据。"),
        ("不同站点 TMAX 列索引可能不同, 应对方法是", ["A. 先 enumerate 表头确认", "B. 写死索引", "C. 跳过", "D. 猜"], 0, "Sitka TMAX@4, Death Valley @3, 先确认表头。"),
        ("`json.dumps(obj, indent=4)` 的作用是", ["A. 对象转带缩进的易读JSON", "B. 字符串转对象", "C. 压缩", "D. 删除"], 0, "dumps 对象→字符串, indent=4 带缩进易读。"),
    ],
    flashcards=[
        ("csv.reader", "splitlines 读行 → csv.reader → next 表头 → 循环数据。"),
        ("strptime", "字符串按格式转日期: %Y-%m-%d。"),
        ("fill_between", "填充温差区域, alpha 透明度。"),
        ("缺失数据", "空串转 int 抛 ValueError, try-except-else。"),
        ("GeoJSON", "features → properties/geometry; coordinates[0]=经度!"),
    ],
    errors=[
        ("列索引写死", "Sitka 和 Death Valley 列索引不同。", "先 enumerate(header_row) 确认。"),
        ("经纬度搞反", "coordinates[0] 当纬度。", "GeoJSON 是(经度, 纬度), [0]=经度 [1]=纬度。"),
        ("loads/dumps 方向", "把 dumps 当读入。", "loads=字符串→对象, dumps=对象→字符串。"),
    ],
))

# ---- Ch17 使用 API ----
EXTRA_CHAPTERS.append(dict(
    fname='python_ch17_interactive.html', title='第17章 使用 API', subtitle='Python 编程 · 项目2',
    key='zhaoli_py_ch17', color='#e67e22',
    knowledge=[
        ('API 概念', 'API=网站中专供程序交互的部分。程序用特定 URL 请求信息(API call)。GitHub 示例: api.github.com/search/repositories?q=language:python+sort:stars。? 后是参数, + 连接。'),
        ('安装 Requests', 'python -m pip install --user requests。'),
        ('requests.get', 'r = requests.get(url, headers=headers); 检查 r.status_code==200 表示成功。headers 可指定 Accept。'),
        ('r.json()', '把 JSON 响应转成 Python 字典。GitHub 搜索响应只有三个键: total_count / incomplete_results / items。'),
        ('提取仓库详情', 'repo_dicts = response_dict[\'items\'] 仓库信息列表(每项78个键)。嵌套取值: repo_dict[\'owner\'][\'login\']。'),
        ('API 限流', 'GitHub 搜索 API 未认证约 10 次/分钟。访问 api.github.com/rate_limit 查看。很多 API 需注册获取 API key。'),
        ('px.bar 可视化', 'fig = px.bar(x=repo_names, y=stars, title=title, labels=labels) 两行出图。'),
        ('hover_name', '自定义悬停提示, 支持 HTML: 用 <br /> 换行拼接 owner 与描述。'),
        ('可点击链接', '用 <a href=\'URL\'>text</a> 把 x 轴标签变超链接。'),
        ('update_traces', 'trace=图表上一组数据; marker_ 开头参数作用于标记: fig.update_traces(marker_color=\'SteelBlue\')。'),
        ('Hacker News API', '无需注册 key。item/{id}.json 返回详情; topstories.json 返回最多500个ID。用 itemgetter(\'comments\') 按评论数排序。'),
    ],
    questions=[
        ("`r.status_code == 200` 表示", ["A. 请求成功", "B. 失败", "C. 重定向", "D. 超时"], 0, "200 = 请求成功, 之后才能 r.json()。"),
        ("`r.json()` 把响应转成", ["A. Python 字典/列表", "B. 字符串", "C. JSON 文件", "D. 图片"], 0, "把 JSON 响应解析为 Python 数据结构。"),
        ("GitHub 搜索响应中仓库列表在", ["A. items 键", "B. total_count 键", "C. owner 键", "D. name 键"], 0, "response_dict[\'items\'] 是仓库信息列表。"),
        ("`repo_dict['owner']['login']` 中 owner 是", ["A. 嵌套字典", "B. 列表", "C. 字符串", "D. 数字"], 0, "owner 键的值是另一个字典, 需二级取值。"),
        ("GitHub 搜索 API 未认证的限流约", ["A. 10次/分钟", "B. 100次/分钟", "C. 无限", "D. 1次/天"], 0, "未认证约 10 次/分钟; 获取令牌后限额大幅提高。"),
        ("`fig.update_traces(marker_color='SteelBlue')` 中 marker_ 前缀作用于", ["A. 数据标记", "B. 标题", "C. 坐标轴", "D. 图例"], 0, "任何以 marker_ 开头的参数作用于标记。"),
        ("Plotly 悬停提示支持", ["A. HTML(<br /> 换行)", "B. 纯文本", "C. 图片", "D. 视频"], 0, "hover_name 支持 HTML, 用 <br /> 换行拼接。"),
        ("Hacker News API 的 topstories.json 返回", ["A. 最多500个文章ID列表", "B. 文章内容", "C. 用户信息", "D. 评论"], 0, "返回最多 500 个热门文章 ID 列表, 再逐条请求详情。"),
        ("按评论数排序用", ["A. itemgetter('comments')", "B. sorted 默认", "C. max()", "D. sum()"], 0, "from operator import itemgetter; sorted(..., key=itemgetter('comments'), reverse=True)。"),
        ("API 调用前必须先", ["A. 检查 status_code", "B. 打印响应", "C. 关闭连接", "D. 转换类型"], 0, "不检查 status_code, 4xx/5xx 时 r.json() 结构不是预期。"),
    ],
    flashcards=[
        ("API 三步", "requests.get(url) → 检查 status_code==200 → r.json()。"),
        ("GitHub API", "search/repositories?q=language:python+sort:stars。"),
        ("嵌套取值", "repo_dict['owner']['login'], 多级键名错→KeyError。"),
        ("限流", "未认证约10次/分钟; rate_limit 查看。"),
        ("px.bar", "x 名称 y 星数两行出图; hover_name 定制提示。"),
    ],
    errors=[
        ("不检查 status", "4xx/5xx 还 r.json()。", "先断言 status_code==200。"),
        ("嵌套 KeyError", "多级键名写错。", "用 try-except 跳过, 或先 print(keys())。"),
        ("限流触发", "循环请求太多。", "先查 rate_limit; 注意 incomplete_results 标志。"),
    ],
))

# ---- Ch19 用户账户 ----
EXTRA_CHAPTERS.append(dict(
    fname='python_ch19_interactive.html', title='第19章 用户账户', subtitle='Python 编程 · 项目3',
    key='zhaoli_py_ch19', color='#27ae60',
    knowledge=[
        ('ModelForm', '基于模型自动生成表单。Meta 嵌套类指定 model、fields、labels: class TopicForm(forms.ModelForm): class Meta: model=Topic; fields=[\'text\']。'),
        ('GET vs POST', 'GET 只读数据(首次访问返回空白表单); POST 通过表单提交数据。视图用 if request.method != \'POST\' 区分。'),
        ('表单流程', 'GET 建空白实例 → POST 用 data=request.POST 填充 → form.is_valid() 校验 → form.save() 入库 → redirect() 跳走。末尾无条件渲染(覆盖空白/无效表单)。'),
        ('csrf_token', '模板表单必须 {% csrf_token %} 防跨站请求伪造攻击(CSRF)。{{ form.as_div }} 一条语句渲染全部字段。'),
        ('widgets 自定义', '覆盖默认 HTML 控件: widgets={\'text\': forms.Textarea(attrs={\'cols\': 80})}。'),
        ('commit=False', '先创建对象不入库, 手动设置外键再 save(): new_entry = form.save(commit=False); new_entry.topic = topic; new_entry.save()。'),
        ('编辑 instance', 'EntryForm(instance=entry) 预填充表单; POST 时同时传 instance 和 data, 校验后 save() 已关联正确主题。'),
        ('accounts 应用', '用户功能独立成 app。urls.py include django.contrib.auth.urls 自带 login/logout。登录模板位置: accounts/templates/registration/login.html。'),
        ('LOGIN_REDIRECT_URL', 'settings.py 指定登录成功后跳转: LOGIN_REDIRECT_URL = \'learning_logs:index\'。登出同理 LOGOUT_REDIRECT_URL。'),
        ('user 对象', '每个模板有 user: user.is_authenticated 判断登录, user.username 显示用户名。'),
        ('登出用 POST', '登出请求必须 POST(防强制踢人), base.html 放空表单。'),
        ('注册 UserCreationForm', 'Django 默认注册表单(校验用户名合法、两次密码一致)。注册成功 login(request, new_user) 自动登录。'),
        ('@login_required', '装饰器放视图前, 未登录访问被重定向到登录页。需 settings.py 指定 LOGIN_URL = \'accounts:login\'。'),
        ('owner 外键', '把层级最高的数据关联用户, 下层自动跟随。Topic.owner = models.ForeignKey(User, on_delete=models.CASCADE)。'),
        ('只显示自己的数据', 'filter(owner=request.user) 只查当前用户; 访问他人数据用 Http404。'),
    ],
    questions=[
        ("ModelForm 的 Meta 嵌套类指定", ["A. model 和 fields", "B. 颜色", "C. 路径", "D. 大小"], 0, "Meta 指定 model(哪个模型)、fields(哪些字段)、labels(标签)。"),
        ("GET 请求的用途是", ["A. 只从服务器读数据", "B. 提交表单", "C. 删除数据", "D. 上传文件"], 0, "GET 只读; POST 提交表单数据。"),
        ("`form.is_valid()` 校验通过后写入数据库用", ["A. form.save()", "B. form.write()", "C. form.insert()", "D. form.update()"], 0, "is_valid() → save() 入库 → redirect() 跳走。"),
        ("模板中防 CSRF 攻击的标签是", ["A. {% csrf_token %}", "B. {% secure %}", "C. {% token %}", "D. {% csrf %}"], 0, "{% csrf_token %} 必须放在 POST 表单中。"),
        ("`form.save(commit=False)` 的作用是", ["A. 创建对象但不入库, 手动设外键", "B. 立即保存", "C. 删除", "D. 校验"], 0, "先创建对象不入库, 设置外键后手动 save()。"),
        ("预填充编辑表单用", ["A. EntryForm(instance=entry)", "B. EntryForm()", "C. EntryForm(data=entry)", "D. EntryForm(edit=True)"], 0, "instance=entry 用已有对象预填充。"),
        ("登录成功后的跳转地址在 settings.py 用", ["A. LOGIN_REDIRECT_URL", "B. REDIRECT_URL", "C. HOME_URL", "D. LOGIN_PAGE"], 0, "LOGIN_REDIRECT_URL 指定登录后跳转; LOGOUT_REDIRECT_URL 登出后。"),
        ("限制页面只允许登录用户访问用", ["A. @login_required", "B. @admin_only", "C. @private", "D. @secure"], 0, "@login_required 放视图前, 未登录重定向登录页。"),
        ("让用户只看自己的数据, 查询用", ["A. filter(owner=request.user)", "B. filter(user=all)", "C. get(owner=1)", "D. 不筛选"], 0, "filter(owner=request.user) 只查当前用户数据。"),
        ("登出请求必须用", ["A. POST 表单", "B. GET 链接", "C. 直接删除", "D. 任何方式"], 0, "登出必须 POST(防攻击者强制踢人下线)。"),
    ],
    flashcards=[
        ("ModelForm", "Meta 指定 model/fields/labels; 自动生成表单。"),
        ("表单流程", "GET 空白 → POST data → is_valid → save → redirect。"),
        ("csrf_token", "POST 表单必加, 防 CSRF 攻击。"),
        ("commit=False", "先建对象, 手动设外键, 再 save。"),
        ("owner 外键", "数据关联用户; filter(owner=request.user)。"),
        ("@login_required", "装饰器限登录用户; LOGIN_URL 指定登录页。"),
    ],
    errors=[
        ("漏 csrf_token", "POST 表单没有 csrf_token 报错。", "表单模板加 {% csrf_token %}。"),
        ("外键忘关联", "新增条目没挂到主题下。", "URL 带 topic_id, save(commit=False) 手动设 topic。"),
        ("数据没隔离", "用户看到所有用户的数据。", "filter(owner=request.user) 只查自己的。"),
    ],
))

# ---- Ch20 样式与部署 ----
EXTRA_CHAPTERS.append(dict(
    fname='python_ch20_interactive.html', title='第20章 样式与部署', subtitle='Python 编程 · 项目3',
    key='zhaoli_py_ch20', color='#27ae60',
    knowledge=[
        ('django-bootstrap5', 'pip install django-bootstrap5 第三方应用, 加入 INSTALLED_APPS(第三方分区, My apps 之后默认之前)。开发顺序: 先功能可用, 再外观。'),
        ('bootstrap 模板标签', 'base.html 头部: {% load django_bootstrap5 %} 加载自定义标签; {% bootstrap_css %} 引入 CSS; {% bootstrap_javascript %} 启用交互(可折叠导航栏)。'),
        ('Bootstrap 导航栏', 'navbar/navbar-expand-md/navbar-light bg-light/mb-4/border 控制样式; navbar-brand 品牌; collapse 让窄屏收进下拉; navbar-nav > nav-item 放链接。ms-auto 把账户链接推右侧。'),
        ('账户链接与登出', '已登录显示 Hello, {{ user.username }}.; 未登录显示 Register/Log in; 登出表单(POST+csrf)放导航栏。'),
        ('美化页面', 'jumbotron 美化首页; {% bootstrap_form %} 美化登录等表单; list-group 和 card 组件美化主题列表与条目卡片。'),
        ('部署准备', '注册 Platform.sh、安装 CLI 与 platformshconfig、pip freeze 生成 requirements.txt、写 YAML 配置文件、Git 版本控制。'),
        ('platform push', 'git push 后 platform push 推到线上。'),
        ('远程设置', '远程创建超级用户; DEBUG = False; 编写自定义 404/500 错误页。'),
        ('部署三要点', 'DEBUG=False(不泄露调试信息)、requirements.txt 锁定依赖、配置文件分离。'),
    ],
    questions=[
        ("django-bootstrap5 是", ["A. 第三方应用", "B. Django 内置", "C. 数据库", "D. 编辑器"], 0, "第三方 app, 把 Bootstrap 集成进 Django。"),
        ("模板中引入 Bootstrap CSS 用", ["A. {% bootstrap_css %}", "B. {% css %}", "C. {% style %}", "D. {% load_css %}"], 0, "{% bootstrap_css %} 引入全部 CSS; {% bootstrap_javascript %} 启用交互。"),
        ("使用自定义 bootstrap 标签的模板需先", ["A. {% load django_bootstrap5 %}", "B. {% import bootstrap %}", "C. {% use css %}", "D. 无需加载"], 0, "凡要用自定义 bootstrap 标签的模板都需 load django_bootstrap5。"),
        ("把账户链接推到导航栏右侧用", ["A. ms-auto", "B. mr-auto", "C. center", "D. left"], 0, "ms-auto(margin-start-automatic) 把链接组推到右侧。"),
        ("部署前锁定依赖版本用", ["A. pip freeze > requirements.txt", "B. pip list", "C. pip update", "D. pip delete"], 0, "pip freeze 生成 requirements.txt, 记录全部依赖版本。"),
        ("生产环境必须设置", ["A. DEBUG = False", "B. DEBUG = True", "C. 不设置", "D. DEBUG = None"], 0, "DEBUG=False 不泄露调试信息(生产必须)。"),
        ("部署平台本书使用", ["A. Platform.sh", "B. GitHub Pages", "C. 本地", "D. FTP"], 0, "Platform.sh 云部署平台。"),
        ("开发顺序原则是", ["A. 先功能可用, 再外观", "B. 先外观, 再功能", "C. 同时做", "D. 只做外观"], 0, "先保证功能可用, 再做外观美化。"),
    ],
    flashcards=[
        ("django-bootstrap5", "第三方 app; bootstrap_css/javascript 模板标签。"),
        ("导航栏", "navbar-expand-md + collapse 响应式; ms-auto 右侧账户。"),
        ("部署", "requirements.txt + YAML 配置 + platform push。"),
        ("生产设置", "DEBUG=False; 自定义 404/500。"),
    ],
    errors=[
        ("忘 load 标签", "用 bootstrap 标签没 load django_bootstrap5。", "模板开头 {% load django_bootstrap5 %}。"),
        ("DEBUG=True 上线", "生产环境泄露调试信息。", "部署后设置 DEBUG=False。"),
        ("依赖没锁定", "requirements.txt 缺失, 线上装不上。", "pip freeze > requirements.txt。"),
    ],
))

print(f"共定义 {len(EXTRA_CHAPTERS)} 个补充章节")
