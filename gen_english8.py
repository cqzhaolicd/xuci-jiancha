#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate english8_u1..u10_interactive.html from math8_ch1_interactive.html template."""
import json, os

TPL = '/home/administrator/xuci-jiancha/math8_ch1_interactive.html'
OUT_DIR = '/home/administrator/xuci-jiancha'

def load_template():
    with open(TPL, encoding='utf-8') as f:
        return f.read()

UNITS = [
# ============ Unit 1 ============
dict(num=1, title='Where did you go on vacation?',
 questions=[
  {"q": "— Where ___ you go on vacation last summer? — I went to Beijing.", "opts": ["A. did", "B. do", "C. does", "D. are"], "ans": 0, "exp": "一般过去时疑问句借助助动词 did，后面动词用原形 go：Where did you go...?"},
  {"q": "I ___ my grandparents last weekend.", "opts": ["A. visit", "B. visited", "C. visits", "D. visiting"], "ans": 1, "exp": "last weekend 是过去时间标志，规则动词 visit 加 -ed 变为 visited。"},
  {"q": "She ___ to the mountains with her family.", "opts": ["A. go", "B. goes", "C. went", "D. gone"], "ans": 2, "exp": "go 是不规则动词，过去式是 went，不能加 -ed。"},
  {"q": "Did you buy ___ special?", "opts": ["A. something", "B. nothing", "C. anything", "D. everything"], "ans": 2, "exp": "疑问句中不定代词用 anything：Did you buy anything special? 买了什么特别的东西吗？"},
  {"q": "There was ___ to eat in the fridge, so we went out.", "opts": ["A. nothing", "B. something", "C. anything", "D. everything"], "ans": 0, "exp": "冰箱里没有吃的，所以出去了：nothing 表示全否定'什么也没有'。"},
  {"q": "I didn't ___ anyone at the party yesterday.", "opts": ["A. saw", "B. seen", "C. seeing", "D. see"], "ans": 3, "exp": "助动词 didn't 后动词用原形：I didn't see anyone... 我没有见到任何人。"},
  {"q": "— Did you enjoy yourself? — Yes, I ___.", "opts": ["A. do", "B. was", "C. am", "D. did"], "ans": 3, "exp": "一般过去时简短回答用助动词 did：Yes, I did. / No, I didn't."},
  {"q": "Last weekend, we ___ some delicious food at the restaurant.", "opts": ["A. have", "B. had", "C. has", "D. having"], "ans": 1, "exp": "have 是不规则动词，过去式是 had：We had some delicious food."},
 ],
 knowledge=[
  ("一般过去时·规则动词", "动词过去式加 -ed：visit→visited、play→played。表示过去发生的动作或状态。"),
  ("一般过去时·不规则动词", "go→went、have→had、see→saw、eat→ate、buy→bought。不规则变化需逐个记忆。"),
  ("一般疑问句与否定", "Did + 主语 + 动词原形？主语 + didn't + 动词原形。助动词 did 后动词用原形。"),
  ("特殊疑问句", "Where/What/When + did + 主语 + 动词原形？如 Where did you go on vacation?"),
  ("不定代词", "something（肯定）、anything（疑问/否定）、nothing（全否定）、everything（一切）。"),
  ("时间标志词", "yesterday、last weekend、last summer、two days ago、in 2020 等与一般过去时连用。"),
  ("be 动词过去式", "am/is→was，are→were。I was...；They were... 注意主谓一致。"),
  ("简短回答", "Did you...? — Yes, I did. / No, I didn't. 用助动词 did 回答。" ),
 ],
 flashcards=[
  ("go 的过去式","went（不规则变化）"),
  ("visit 的过去式","visited（规则加 -ed）"),
  ("have 的过去式","had"),
  ("see 的过去式","saw"),
  ("eat 的过去式","ate"),
  ("buy 的过去式","bought"),
  ("一般过去时疑问句","Did + 主语 + 动词原形?"),
  ("不定代词","something 肯定 / anything 疑问否定 / nothing 全否定"),
  ("时间标志","yesterday, last weekend, two days ago"),
  ("be 动词过去式","was(am/is) / were(are)"),
 ],
 errors=[
  ("不规则动词加 ed","把 go 的过去式写成 goed。","go 是不规则动词，过去式是 went，不能加 -ed。"),
  ("助动词后未还原","Did you went to Beijing?","did 后动词用原形：Did you go to Beijing?"),
  ("不定代词混用","疑问句写成 Did you buy something special?","疑问句和否定句用 anything：Did you buy anything special?"),
  ("was/were 混用","You was at home yesterday.","you 用 were：You were at home yesterday."),
  ("过去式与现在时混用","Last weekend I visit my uncle.","有 last weekend 要用过去式：I visited my uncle."),
 ]),

# ============ Unit 2 ============
dict(num=2, title='How often do you exercise?',
 questions=[
  {"q": "— ___ do you exercise? — Three times a week.", "opts": ["A. How often", "B. How long", "C. How many", "D. How much"], "ans": 0, "exp": "回答 Three times a week（一周三次）是频率，用 How often 提问。"},
  {"q": "She ___ eats junk food because it's bad for her health.", "opts": ["A. always", "B. usually", "C. hardly ever", "D. often"], "ans": 2, "exp": "垃圾食品对健康有害，所以'几乎从不'吃：hardly ever 表示几乎不。"},
  {"q": "下列频率副词按频率从高到低排列正确的是", "opts": ["A. always, usually, often, sometimes", "B. often, always, sometimes, usually", "C. usually, sometimes, always, often", "D. sometimes, often, always, usually"], "ans": 0, "exp": "频率排序：always(100%) > usually(80%) > often(60%) > sometimes(40%)。"},
  {"q": "He goes swimming ___ a week.", "opts": ["A. two time", "B. second", "C. twice", "D. two"], "ans": 2, "exp": "一周两次用 twice a week。一次是 once，两次是 twice，三次以上用 three times。"},
  {"q": "— How often does your father exercise? — He ___ every day.", "opts": ["A. exercises", "B. exercise", "C. exercising", "D. exercised"], "ans": 0, "exp": "主语 He 是第三人称单数，一般现在时动词加 -s：exercises。"},
  {"q": "She ___ late for school.", "opts": ["A. never is", "B. does never", "C. is never", "D. never does"], "ans": 2, "exp": "频度副词放在 be 动词之后：She is never late for school."},
  {"q": "— How long do you sleep every night? — ___", "opts": ["A. About eight hours", "B. Twice a week", "C. Every day", "D. Never"], "ans": 0, "exp": "How long 问时长，回答 About eight hours（大约八小时）。Twice a week 是频率，回答 How often。"},
  {"q": "He ___ his homework on time.", "opts": ["A. never do", "B. does never", "C. never is", "D. never does"], "ans": 3, "exp": "频度副词放在实义动词前：He never does his homework on time."},
 ],
 knowledge=[
  ("频度副词", "always(100%) > usually(80%) > often(60%) > sometimes(40%) > hardly ever(5%) > never(0%)。"),
  ("频度副词位置", "放在实义动词之前、be 动词/助动词/情态动词之后：He never does...；She is never late."),
  ("How often 问频率", "How often do you...? 答：once a week、twice a month、three times a day、every day。"),
  ("once/twice/three times", "一次 once、两次 twice，三次以上 three times/four times，后接 a week/a month。"),
  ("How long vs How often", "How long 问时长（睡了多久），How often 问频率（多久一次）。"),
  ("一般现在时三单", "主语 he/she/it 时动词加 -s/-es：exercises、goes、watches。"),
  ("健康生活表达", "exercise 锻炼、keep healthy 保持健康、eat healthy food 吃健康食物、drink milk 喝牛奶。"),
  ("周末活动句型", "What do you do on weekends? — I usually... 询问和回答周末活动。"),
 ],
 flashcards=[
  ("always","总是（100%）"),
  ("usually","通常（80%）"),
  ("often","经常（60%）"),
  ("sometimes","有时（40%）"),
  ("hardly ever","几乎不（5%）"),
  ("never","从不（0%）"),
  ("How often","多久一次（问频率）"),
  ("How long","多久（问时长）"),
  ("once / twice","一次 / 两次"),
  ("三单变化","He exercises every day."),
 ],
 errors=[
  ("How often 与 How long 混淆","— How long do you exercise? — Three times a week.","问频率用 How often；How long 问时长。"),
  ("频度副词位置","She never is late for school.","频度副词在 be 动词后：She is never late for school."),
  ("hardly ever 误读","把 hardly ever 理解为'努力地经常'。","hardly ever 是'几乎从不'，频率接近 never。"),
  ("三单漏 s","He exercise every morning.","主语三单动词加 s：He exercises every morning."),
  ("twice 表达错误","把'两次'写成 two time。","两次是 twice，一次是 once；三次起才用 three times。"),
 ]),

# ============ Unit 3 ============
dict(num=3, title="I'm more outgoing than my sister.",
 questions=[
  {"q": "Tom is ___ than his brother.", "opts": ["A. more tall", "B. taller", "C. tallest", "D. tall"], "ans": 1, "exp": "单音节形容词 tall 加 -er 构成比较级：taller，与 than 连用。"},
  {"q": "She is ___ outgoing than me.", "opts": ["A. most", "B. many", "C. more", "D. much"], "ans": 2, "exp": "outgoing 是多音节词，比较级用 more + 原级：more outgoing。"},
  {"q": "My bag is as ___ as yours.", "opts": ["A. heavy", "B. heavier", "C. heaviest", "D. more heavy"], "ans": 0, "exp": "as...as 中间用形容词原级：as heavy as 和……一样重。"},
  {"q": "good 的比较级是", "opts": ["A. better", "B. gooder", "C. best", "D. more good"], "ans": 0, "exp": "good 是不规则变化，比较级是 better（最高级 best）。"},
  {"q": "He is ___ smarter than me.", "opts": ["A. very", "B. a little", "C. too", "D. more"], "ans": 1, "exp": "a little 可修饰比较级加强程度：a little smarter 稍微聪明一点。very/too 不修饰比较级。"},
  {"q": "下列哪句话是正确的比较级表达？", "opts": ["A. She is more tall than me.", "B. She is the taller than me.", "C. She is taller than me.", "D. She is tall than me."], "ans": 2, "exp": "单音节 tall 用 taller，比较级前不加 the：She is taller than me."},
  {"q": "天气越来越暖和：The weather is getting ___.", "opts": ["A. warmer and warmer", "B. warm and warm", "C. more warm and more warm", "D. warmest and warmest"], "ans": 0, "exp": "比较级 + and + 比较级表示'越来越……'：warmer and warmer。"},
  {"q": "— Who is ___, you or your sister? — My sister is.", "opts": ["A. more careful", "B. the most careful", "C. careful", "D. most careful"], "ans": 0, "exp": "两者之间比较用比较级：more careful（careful 是多音节词用 more）。"},
 ],
 knowledge=[
  ("单音节比较级", "形容词 + er：tall→taller、short→shorter、small→smaller。"),
  ("多音节比较级", "more + 形容词原级：more outgoing、more beautiful、more careful。"),
  ("特殊变化", "good/well→better，bad→worse，many/much→more，little→less。"),
  ("比较级句型", "A + be + 比较级 + than + B：Tom is taller than Jim."),
  ("as...as 原级比较", "as + 原级 + as 表示'和……一样'；否定用 not as/so...as。"),
  ("比较级修饰语", "a little、much、even、far、a lot 可修饰比较级加强程度。"),
  ("越来越…", "比较级 + and + 比较级：warmer and warmer、more and more beautiful。"),
  ("拼写规则", "重读闭音节双写尾字母：big→bigger；辅音+y 变 i：heavy→heavier。"),
 ],
 flashcards=[
  ("tall 比较级","taller"),
  ("heavy 比较级","heavier（y 变 i 加 er）"),
  ("big 比较级","bigger（双写 g）"),
  ("fun 比较级","funnier（双写 n）"),
  ("outgoing 比较级","more outgoing"),
  ("good 比较级","better"),
  ("bad 比较级","worse"),
  ("比较级句型","A + be + 比较级 + than + B"),
  ("as...as","和……一样（中间用原级）"),
  ("修饰比较级","a little / much / even / far"),
 ],
 errors=[
  ("双重比较级","She is more taller than me.","单音节加 er，多音节用 more，二者不能同时用：taller 或 more beautiful。"),
  ("双写规则","big 的比较级写成 biger。","重读闭音节双写尾字母：bigger。"),
  ("good 不规则变化","good 的比较级写成 gooder。","不规则变化：better。"),
  ("as...as 中间用比较级","He is as taller as me.","as...as 中间用原级：He is as tall as me."),
  ("than 前用原级","She is tall than me.","than 前必须是比较级：She is taller than me."),
 ]),

# ============ Unit 4 ============
dict(num=4, title="What's the best movie theater?",
 questions=[
  {"q": "This is ___ movie theater in town.", "opts": ["A. best", "B. the best", "C. better", "D. a best"], "ans": 1, "exp": "三者以上比较用最高级，且最高级前要加 the：the best movie theater。"},
  {"q": "My sister is the ___ girl in our class.", "opts": ["A. smartest", "B. smarter", "C. most smart", "D. smart"], "ans": 0, "exp": "单音节 smart 加 -est 构成最高级，前面加 the：the smartest girl。"},
  {"q": "good 的最高级是", "opts": ["A. better", "B. best", "C. goodest", "D. most good"], "ans": 1, "exp": "good 不规则变化：比较级 better，最高级 best。"},
  {"q": "Which is ___, the sun, the moon or the earth?", "opts": ["A. big", "B. bigger", "C. the biggest", "D. biggest"], "ans": 2, "exp": "三者（sun/moon/earth）比较用最高级，前面加 the：the biggest。"},
  {"q": "He is ___ student in his class.", "opts": ["A. the funniest", "B. funnier", "C. the funnier", "D. funniest"], "ans": 0, "exp": "fun 最高级 funniest（双写 n），全班范围内用最高级 the funniest。"},
  {"q": "Shanghai is one of ___ cities in China.", "opts": ["A. the biggest", "B. the bigger", "C. biggest", "D. bigger"], "ans": 0, "exp": "one of + the + 最高级 + 复数名词，表示'最……之一'：one of the biggest cities。"},
  {"q": "This restaurant has the ___ service in the city.", "opts": ["A. good", "B. better", "C. best", "D. well"], "ans": 2, "exp": "in the city 是范围标志，用最高级 the best service。"},
  {"q": "— ___ is the best movie theater? — Screen City is.", "opts": ["A. Who", "B. Which", "C. What time", "D. How much"], "ans": 1, "exp": "从多个选项中选'哪一个'用 Which 提问：Which is the best...?"},
 ],
 knowledge=[
  ("单音节最高级", "形容词 + est：tall→tallest、smart→smartest、small→smallest。"),
  ("多音节最高级", "the most + 形容词原级：the most beautiful、the most popular。"),
  ("特殊变化", "good/well→best，bad→worst，many/much→most，little→least。"),
  ("最高级句型", "the + 最高级 + in/of + 范围：the tallest in our class / of all the students。"),
  ("one of + the 最高级", "one of the biggest cities：'最……之一'，后接复数名词。"),
  ("三者以上比较", "两者用比较级，三者及以上用最高级：Which is the best of the three?"),
  ("拼写规则", "双写：big→biggest；y 变 i：heavy→heaviest；多音节：the most popular。"),
  ("询问最佳", "Which is the best movie theater? — Screen City is. 回答用 the best。"),
 ],
 flashcards=[
  ("tall 最高级","tallest"),
  ("big 最高级","biggest（双写 g）"),
  ("heavy 最高级","heaviest（y 变 i）"),
  ("fun 最高级","funniest"),
  ("good 最高级","best"),
  ("bad 最高级","worst"),
  ("多音节最高级","the most beautiful"),
  ("最高级句型","the + 最高级 + in/of + 范围"),
  ("one of...","one of the biggest cities（最……之一）"),
  ("比较级 vs 最高级","两者比较级，三者以上最高级"),
 ],
 errors=[
  ("漏掉 the","She is tallest in our class.","最高级前必须加 the：the tallest。"),
  ("in/of 用错","the tallest of our class.","in 接集体范围（in our class），of 接同类个体（of all the students）。"),
  ("good 最高级写错","good 的最高级写成 goodest。","不规则变化：best。"),
  ("比较级当最高级","三者比较时用 bigger。","三者及以上用最高级 the biggest。"),
  ("most 与 est 重复","the most biggest。","最高级只能二选一：the biggest，不能重复。"),
 ]),

# ============ Unit 5 ============
dict(num=5, title='Do you want to watch a game show?',
 questions=[
  {"q": "— What do you think of talk shows? — I ___ them.", "opts": ["A. stand", "B. can stand", "C. can't stand", "D. don't stand"], "ans": 2, "exp": "can't stand 表示'无法忍受'：我受不了脱口秀。这是表达讨厌的常用说法。"},
  {"q": "I want ___ a game show tonight.", "opts": ["A. to watch", "B. watch", "C. watching", "D. watched"], "ans": 0, "exp": "want to do sth：想要做某事，不定式作宾语：I want to watch a game show."},
  {"q": "She plans ___ a talent show this weekend.", "opts": ["A. watches", "B. to watch", "C. watching", "D. watch"], "ans": 1, "exp": "plan to do sth：计划做某事，to watch a talent show 看选秀节目。"},
  {"q": "— Do you want to watch a game show? — ___.", "opts": ["A. Yes, I do", "B. Yes, I want", "C. No, I want", "D. Yes, I watch"], "ans": 0, "exp": "Do 引导的一般疑问句简短回答用 do：Yes, I do. / No, I don't."},
  {"q": "I like soap operas, but I ___ watch them very often.", "opts": ["A. don't", "B. doesn't", "C. not", "D. am not"], "ans": 0, "exp": "主语 I 的否定用 don't + 动词原形：I don't watch them very often."},
  {"q": "He ___ to be a reporter one day.", "opts": ["A. hope", "B. hopes", "C. hoping", "D. hoped"], "ans": 1, "exp": "主语三单 He 加 -s：hopes；hope to do sth 希望做某事。"},
  {"q": "We decided ___ a movie this evening.", "opts": ["A. watched", "B. watch", "C. to watch", "D. watching"], "ans": 2, "exp": "decide to do sth：决定做某事，不定式作宾语：decided to watch a movie。"},
  {"q": "表达'非常喜欢'用英语说是", "opts": ["A. can't stand", "B. love", "C. mind", "D. hate"], "ans": 1, "exp": "love 表示'非常喜欢'；can't stand 受不了、hate 讨厌、mind 介意。"},
 ],
 knowledge=[
  ("询问看法", "What do you think of...? 相当于 How do you like...?，问对某事物的看法。"),
  ("表达喜好程度", "love 非常喜欢 > like 喜欢 > don't mind 不介意 > can't stand 无法忍受 > hate 讨厌。"),
  ("电视节目词汇", "game show 游戏节目、talk show 脱口秀、soap opera 肥皂剧、talent show 选秀、news 新闻。"),
  ("不定式作宾语", "want/plan/hope/decide + to do：I want to watch a game show."),
  ("一般疑问句", "Do you want to watch...? — Yes, I do. / No, I don't."),
  ("三单与否定", "主语三单用 doesn't + 动词原形：He doesn't like soap operas."),
  ("回答看法", "回答用 I love/like/don't mind/can't stand + 名词，不直接答 yes/no。"),
  ("日常口语", "What's on TV tonight? 今晚有什么节目？常用于谈论电视节目。"),
 ],
 flashcards=[
  ("询问看法","What do you think of...? = How do you like...?"),
  ("love","非常喜欢"),
  ("like","喜欢"),
  ("don't mind","不介意"),
  ("can't stand","无法忍受"),
  ("game show","游戏节目"),
  ("talk show","脱口秀"),
  ("soap opera","肥皂剧"),
  ("want to do","想要做某事（want + to + 动词原形）"),
  ("简短回答","Yes, I do. / No, I don't."),
 ],
 errors=[
  ("want 后漏 to","I want watch a game show.","want 后接不定式：I want to watch a game show."),
  ("do/does 混用","He don't like game shows.","三单否定用 doesn't：He doesn't like game shows."),
  ("can't stand 误解","把 can't stand 理解为'不能站'。","can't stand 表'无法忍受'，用于表达讨厌。"),
  ("答语不规范","Do you want...? 回答 Yes, I want.","简短回答用 Yes, I do. / No, I don't."),
  ("think of 漏 of","What do you think the game show?","固定搭配 think of：What do you think of the game show?"),
 ]),

# ============ Unit 6 ============
dict(num=6, title="I'm going to study computer science.",
 questions=[
  {"q": "I ___ going to study computer science.", "opts": ["A. is", "B. am", "C. are", "D. be"], "ans": 1, "exp": "主语 I 用 am：I am going to study... 我打算学习计算机科学。"},
  {"q": "She ___ going to be a doctor.", "opts": ["A. am", "B. are", "C. is", "D. be"], "ans": 2, "exp": "主语三单 She 用 is：She is going to be a doctor."},
  {"q": "They ___ going to play basketball tomorrow.", "opts": ["A. are", "B. is", "C. am", "D. be"], "ans": 0, "exp": "主语 They 用 are：They are going to play basketball tomorrow."},
  {"q": "— What do you want to be? — I want to be ___.", "opts": ["A. a engineer", "B. an engineer", "C. engineer", "D. engineers"], "ans": 1, "exp": "engineer 以元音音素开头，用 an；want to be + 职业名词。"},
  {"q": "He is going to ___ computer science.", "opts": ["A. studies", "B. studying", "C. study", "D. studied"], "ans": 2, "exp": "be going to 后接动词原形：is going to study。"},
  {"q": "'飞行员'用英语说是", "opts": ["A. engineer", "B. scientist", "C. doctor", "D. pilot"], "ans": 3, "exp": "pilot 飞行员；engineer 工程师、scientist 科学家、doctor 医生。"},
  {"q": "— What are you going to do this weekend? — ___.", "opts": ["A. I'm going to visit my grandparents", "B. I visited my grandparents", "C. I visit my grandparents", "D. I am visit my grandparents"], "ans": 0, "exp": "询问周末计划用 be going to 回答：I'm going to visit my grandparents."},
  {"q": "表示'明年'的时间标志词是", "opts": ["A. next year", "B. last year", "C. yesterday", "D. two days ago"], "ans": 0, "exp": "next year 明年，与一般将来时（be going to / will）连用。其他三个是过去时间。"},
 ],
 knowledge=[
  ("be going to 结构", "be(am/is/are) + going to + 动词原形，表示打算/计划做某事。"),
  ("be 动词搭配", "I→am；he/she/it→is；we/you/they→are。如 I'm going to study computer science."),
  ("否定形式", "be + not + going to：I'm not going to watch TV tonight."),
  ("一般疑问句", "Are you going to...? — Yes, I am. / No, I'm not."),
  ("职业词汇", "doctor 医生、engineer 工程师、pilot 飞行员、scientist 科学家、teacher 教师、cook 厨师。"),
  ("What do you want to be?", "询问理想职业，回答 I want to be + 职业名词。"),
  ("时间标志词", "next year/month/week、tomorrow、this weekend 等将来时间。"),
  ("与 will 的区别", "be going to 表有计划打算，will 表临时决定或预测。"),
 ],
 flashcards=[
  ("be going to 结构","be + going to + 动词原形"),
  ("I","am going to"),
  ("He/She/It","is going to"),
  ("We/You/They","are going to"),
  ("否定形式","be not going to（I'm not going to...）"),
  ("疑问形式","Are you going to...? Yes, I am."),
  ("want to be","想成为（接职业名词）"),
  ("职业词汇","engineer 工程师 / pilot 飞行员 / scientist 科学家"),
  ("时间标志","next year / tomorrow / this weekend"),
  ("计划表达","What are you going to do?"),
 ],
 errors=[
  ("be 动词用错","She are going to be a doctor.","三单用 is：She is going to be a doctor."),
  ("going to 后接原形","He is going to studies computer science.","going to 后接动词原形：going to study。"),
  ("a/an 混用","I want to be a engineer.","engineer 以元音音素开头，用 an：an engineer。"),
  ("want to be 漏 be","I want to a doctor.","want to be + 职业：I want to be a doctor."),
  ("与 will 混用","用 be going to 表达临时决定。","临时决定用 will，计划打算用 be going to。"),
 ]),

# ============ Unit 7 ============
dict(num=7, title='Will people have robots?',
 questions=[
  {"q": "People ___ have robots in their homes in the future.", "opts": ["A. will", "B. do", "C. are", "D. were"], "ans": 0, "exp": "in the future 是将来时间标志，用 will + 动词原形：People will have robots."},
  {"q": "There ___ more robots in the future.", "opts": ["A. will have", "B. will be", "C. have", "D. is"], "ans": 1, "exp": "存在句'将会有'用 There will be：There will be more robots."},
  {"q": "I think I ___ free tomorrow.", "opts": ["A. will be", "B. will", "C. am be", "D. be"], "ans": 0, "exp": "free 是形容词，前面需要 be：I will be free tomorrow."},
  {"q": "She ___ come to the party tomorrow because she is busy.", "opts": ["A. willn't", "B. won't", "C. doesn't", "D. isn't"], "ans": 1, "exp": "will not 缩略为 won't：She won't come... 她不会来。willn't 不存在。"},
  {"q": "— Will there be more trees? — Yes, ___.", "opts": ["A. there will", "B. there is", "C. it will", "D. they will"], "ans": 0, "exp": "There be 句型的简短回答：Yes, there will. / No, there won't."},
  {"q": "'in the future' 的意思是", "opts": ["A. 在过去", "B. 在未来", "C. 现在", "D. 马上"], "ans": 1, "exp": "in the future 在未来，与一般将来时连用。"},
  {"q": "Robots will help people ___ a lot of work.", "opts": ["A. doing", "B. do", "C. does", "D. did"], "ans": 1, "exp": "help sb do sth：帮助某人做某事，do 用动词原形。"},
  {"q": "人们将来会种更多树：People ___ more trees in the future.", "opts": ["A. plant", "B. will plant", "C. planted", "D. plants"], "ans": 1, "exp": "in the future 表将来，用 will + 动词原形：People will plant more trees."},
 ],
 knowledge=[
  ("will 将来时", "will + 动词原形，表示将来发生的动作或状态。"),
  ("否定形式", "will not = won't + 动词原形：People won't have robots at home."),
  ("一般疑问句", "Will + 主语 + 动词原形？— Yes, ... will. / No, ... won't."),
  ("There will be", "表示'将会有'，后接名词：There will be more robots in the future."),
  ("时间标志词", "in the future、in 100 years、tomorrow、next year 等。"),
  ("预测句型", "People will... / Robots will... / There will be...，用于对未来的预测。"),
  ("help sb do sth", "帮助某人做某事，do 用原形：Robots will help people do housework."),
  ("两种将来表达", "will 表预测/临时决定；be going to 表计划打算。"),
 ],
 flashcards=[
  ("will 结构","will + 动词原形"),
  ("否定形式","won't（will not）+ 动词原形"),
  ("疑问形式","Will + 主语 + 动词原形?"),
  ("There will be","将会有（后接名词）"),
  ("in the future","在未来"),
  ("in 100 years","一百年后"),
  ("help sb do sth","帮助某人做某事"),
  ("简短回答","Yes, there will. / No, there won't."),
  ("预测句型","People will have robots at home."),
  ("will vs be going to","will 预测，be going to 计划"),
 ],
 errors=[
  ("will 后接原形","He will comes tomorrow.","will 后接动词原形：He will come tomorrow."),
  ("There will have","There will have more robots.","存在句用 There will be more robots."),
  ("won't 拼写","把 will not 缩略成 willn't。","正确缩略式是 won't。"),
  ("简短回答错误","Will there be...? 回答 Yes, it will.","回答 Yes, there will. / No, there won't."),
  ("will 后漏 be","I will free tomorrow.","形容词前要有 be：I will be free tomorrow."),
 ]),

# ============ Unit 8 ============
dict(num=8, title='How do you make a banana milk shake?',
 questions=[
  {"q": "___ the bananas and put them in the blender.", "opts": ["A. Cut up", "B. Cutting up", "C. Cutted up", "D. To cut up"], "ans": 0, "exp": "祈使句以动词原形开头：Cut up the bananas. 把香蕉切碎。cut 过去式仍是 cut。"},
  {"q": "How many ___ do we need?", "opts": ["A. banana", "B. bananas", "C. bananaes", "D. a banana"], "ans": 1, "exp": "How many 后接可数名词复数：How many bananas do we need? 我们需要多少根香蕉？"},
  {"q": "How much ___ do we need?", "opts": ["A. milk", "B. milks", "C. a milk", "D. milkses"], "ans": 0, "exp": "milk 是不可数名词，用 How much 提问，不加 -s。"},
  {"q": "一茶匙糖：a ___ of sugar.", "opts": ["A. cup", "B. teaspoon", "C. piece", "D. glass"], "ans": 1, "exp": "a teaspoon of 一茶匙；a cup of 一杯、a piece of 一片。"},
  {"q": "两杯酸奶：two ___ of yogurt.", "opts": ["A. cupes", "B. a cup", "C. cups", "D. cup"], "ans": 2, "exp": "量词变复数：two cups of yogurt；yogurt 不可数不加 s。"},
  {"q": "First, ___ the bananas. Then cut them up.", "opts": ["A. peeling", "B. peel", "C. peels", "D. peeled"], "ans": 1, "exp": "祈使句用动词原形：First, peel the bananas. 先给香蕉剥皮。"},
  {"q": "___ water do you need? — Two glasses.", "opts": ["A. How many", "B. How much", "C. How often", "D. How long"], "ans": 1, "exp": "water 不可数，用 How much 提问：How much water do you need?"},
  {"q": "___ cut up the vegetables! It's dangerous.", "opts": ["A. Don't", "B. Not", "C. No", "D. Doesn't"], "ans": 0, "exp": "祈使句否定用 Don't + 动词原形：Don't cut up the vegetables!"},
 ],
 knowledge=[
  ("祈使句", "以动词原形开头，表命令/建议：Cut up the bananas. Turn on the blender."),
  ("祈使句否定", "Don't + 动词原形：Don't pour the milk into the blender."),
  ("How many", "问可数名词数量，后接复数：How many bananas do we need?"),
  ("How much", "问不可数名词数量：How much milk do we need?"),
  ("量词表达", "a cup of 一杯、a teaspoon of 一茶匙、a piece of 一片、a glass of 一杯（玻璃杯）。"),
  ("量词复数", "量词变复数，名词不变：two cups of yogurt、three pieces of bread。"),
  ("顺序词", "first 首先、then 然后、next 接下来、finally 最后，用于描述制作步骤。"),
  ("制作词汇", "peel 削皮、cut up 切碎、pour 倒入、mix 搅拌、add 加入、turn on 打开。"),
 ],
 flashcards=[
  ("祈使句","动词原形开头：Cut up the bananas."),
  ("祈使句否定","Don't + 动词原形"),
  ("How many","问可数名词（后接复数）"),
  ("How much","问不可数名词"),
  ("a cup of","一杯"),
  ("a teaspoon of","一茶匙"),
  ("a piece of","一片/一块"),
  ("two cups of","两杯（量词变复数）"),
  ("顺序词","first, then, next, finally"),
  ("制作词汇","peel 削皮 / cut up 切碎 / pour 倒入"),
 ],
 errors=[
  ("How many/How much 混用","How many milk do we need?","milk 不可数用 How much；bananas 可数用 How many。"),
  ("不可数名词加 s","two milks、two waters。","milk、water、yogurt 不可数不加 s，用量词表达数量。"),
  ("祈使句用三单","Cuts up the bananas!","祈使句用动词原形：Cut up the bananas!"),
  ("量词漏 of","a cup milk。","量词结构 a cup of milk，of 不能漏。"),
  ("步骤缺顺序词","制作过程不用 first/then/next/finally 连接。","用顺序词使步骤清晰：First, ... Then, ... Finally, ..."),
 ]),

# ============ Unit 9 ============
dict(num=9, title='Can you come to my party?',
 questions=[
  {"q": "— Can you come to my party on Saturday? — ___.", "opts": ["A. Sorry, I can", "B. Sure, I'd love to", "C. No, I'd love to", "D. Yes, I can't"], "ans": 1, "exp": "接受邀请：Sure, I'd love to. 好的，我很乐意。I'd = I would。"},
  {"q": "— Can you come to my birthday party? — ___. I have to visit my grandma.", "opts": ["A. Sorry, I can't", "B. Sure, I'd love to", "C. Yes, I can", "D. Of course"], "ans": 0, "exp": "拒绝邀请并说明原因：Sorry, I can't. I have to visit my grandma."},
  {"q": "I have ___ finish my homework first.", "opts": ["A. for", "B. to", "C. at", "D. in"], "ans": 1, "exp": "have to + 动词原形：不得不做某事。I have to finish my homework first."},
  {"q": "She ___ go to the doctor because she is ill.", "opts": ["A. have to", "B. has", "C. has to", "D. have"], "ans": 2, "exp": "主语三单 She，have 变 has：She has to go to the doctor."},
  {"q": "I'm not sure. I ___ practice the violin.", "opts": ["A. might", "B. must", "C. can", "D. am"], "ans": 0, "exp": "不确定时用 might 表示'可能'：I might practice the violin. 我可能练小提琴。"},
  {"q": "'星期二'用英语说是", "opts": ["A. Thursday", "B. Tuesday", "C. Saturday", "D. Sunday"], "ans": 1, "exp": "Tuesday 星期二；Thursday 星期四（注意拼写区分）。"},
  {"q": "— What are you doing tomorrow? — I'm ___ my grandparents.", "opts": ["A. visit", "B. visits", "C. visiting", "D. visited"], "ans": 2, "exp": "现在进行时表将来的计划安排：I'm visiting my grandparents tomorrow."},
  {"q": "'mustn't' 的意思是", "opts": ["A. 必须", "B. 禁止、不可以", "C. 不必", "D. 可以"], "ans": 1, "exp": "mustn't = must not 表示'禁止、不可以'；'不必'是 don't have to。"},
 ],
 knowledge=[
  ("邀请句型", "Can you come to my party? 你能来参加我的聚会吗？"),
  ("接受邀请", "Sure, I'd love to. / Of course. / Yes, I can."),
  ("拒绝邀请", "Sorry, I can't. I have to... / I'm afraid I can't. 并说明原因。"),
  ("have to", "不得不、必须做，三单用 has to：She has to do her homework."),
  ("must 与 might", "must 必须（mustn't 禁止）；might 可能（表不确定）。"),
  ("星期表达", "Monday 周一、Tuesday 周二、Wednesday 周三、Thursday 周四、Friday 周五、Saturday 周六、Sunday 周日。"),
  ("现在进行时表将来", "I'm visiting my grandparents tomorrow. 表示已安排好的计划。"),
  ("礼貌用语", "I'm afraid... 恐怕……；Thanks for asking. 谢谢邀请。"),
 ],
 flashcards=[
  ("邀请","Can you come to my party?"),
  ("接受","Sure, I'd love to."),
  ("拒绝","Sorry, I can't. I have to..."),
  ("have to","不得不（三单 has to）"),
  ("must","必须；mustn't 禁止"),
  ("might","可能"),
  ("星期","Monday, Tuesday, Wednesday..."),
  ("weekend","Saturday & Sunday（周末）"),
  ("现在进行时表将来","I'm visiting my grandparents tomorrow."),
  ("礼貌表达","I'm afraid I can't. Thanks for asking."),
 ],
 errors=[
  ("have to 漏 to","I have finish my homework first.","have to + 动词原形：I have to finish my homework."),
  ("have/has 混用","She have to go to the doctor.","三单用 has to：She has to go to the doctor."),
  ("mustn't 误解","把 mustn't 理解为'不必'。","mustn't 表'禁止'；'不必'是 don't have to。"),
  ("星期拼写","把周二写成 Tuseday、周四写成 Thuesday。","Tuesday、Thursday，注意拼写。"),
  ("拒绝却说接受语","想拒绝却说 Sure, I'd love to.","拒绝用 Sorry, I can't. + 原因。"),
 ]),

# ============ Unit 10 ============
dict(num=10, title="If you go to the party, you'll have a great time!",
 questions=[
  {"q": "If you ___ to the party, you'll have a great time.", "opts": ["A. will go", "B. go", "C. went", "D. going"], "ans": 1, "exp": "主将从现：主句用 will，if 从句用一般现在时 go。"},
  {"q": "If it ___ tomorrow, we'll stay at home.", "opts": ["A. will rain", "B. rained", "C. rains", "D. raining"], "ans": 2, "exp": "if 从句主语三单 it，用一般现在时三单 rains：If it rains tomorrow..."},
  {"q": "You'll be late ___ you don't hurry.", "opts": ["A. because", "B. so", "C. but", "D. if"], "ans": 3, "exp": "if 引导条件句：如果你不快点，你会迟到。"},
  {"q": "If he ___ hard, he will pass the exam.", "opts": ["A. study", "B. will study", "C. studies", "D. studied"], "ans": 2, "exp": "if 从句主语三单 he，动词加 -s：If he studies hard..."},
  {"q": "If she comes, I ___ her the news.", "opts": ["A. tell", "B. will tell", "C. told", "D. telling"], "ans": 1, "exp": "主句用一般将来时 will tell：如果她来了，我会告诉她这个消息。"},
  {"q": "If it ___ rain, we'll go out.", "opts": ["A. don't", "B. won't", "C. doesn't", "D. not"], "ans": 2, "exp": "if 从句否定，主语三单 it 用 doesn't：If it doesn't rain, we'll go out."},
  {"q": "unless 的意思接近", "opts": ["A. if not", "B. if", "C. because", "D. so"], "ans": 0, "exp": "unless = if...not，表示'除非、如果不'。"},
  {"q": "___ you study hard, you will get good grades.", "opts": ["A. So", "B. But", "C. Because", "D. If"], "ans": 3, "exp": "if 引导条件句放句首，主句用 will：如果你努力学习，你会取得好成绩。"},
 ],
 knowledge=[
  ("if 条件句", "if 引导条件状语从句，表示'如果……就……'。"),
  ("主将从现", "主句用一般将来时（will + 动词原形），从句用一般现在时。"),
  ("从句三单", "if 从句主语三单时动词加 -s/es：If it rains tomorrow, we'll stay at home."),
  ("从句否定", "从句否定用 don't/doesn't + 动词原形：If it doesn't rain, we'll go out."),
  ("unless", "相当于 if...not，表示'除非、如果不'：You'll be late unless you hurry."),
  ("从句位置", "if 从句放句首用逗号隔开，放句尾不用逗号。"),
  ("句型示范", "If you go to the party, you'll have a great time!"),
  ("缩略形式", "you'll = you will，we'll = we will，口语中常用。"),
 ],
 flashcards=[
  ("if 条件句","如果……就……"),
  ("主将从现","主句 will + 动原，从句一般现在时"),
  ("从句三单","If it rains tomorrow..."),
  ("从句否定","If it doesn't rain..."),
  ("unless","除非 = if...not"),
  ("句首从句","If you study hard, you'll pass."),
  ("句尾从句","You'll pass if you study hard."),
  ("you'll","you will"),
  ("句型示范","If you go to the party, you'll have a great time!"),
  ("条件句标志","if / unless"),
 ],
 errors=[
  ("主句用现在时","If you go, you have a great time.","主句用将来时：you'll have a great time。"),
  ("从句用将来时","If it will rain, we'll stay at home.","从句用一般现在时：If it rains..."),
  ("三单漏 s","If he study hard, he will pass.","从句主语三单加 s：If he studies hard..."),
  ("don't/doesn't 混用","If it don't rain, we'll go out.","主语三单用 doesn't：If it doesn't rain..."),
  ("unless 后加 not","You'll be late unless you don't hurry.","unless 本身含否定，后面不能再加 not：unless you hurry。"),
 ]),
]

def gen_file(u):
    html = load_template()
    n = u['num']
    title_en = u['title']
    qj = json.dumps(u['questions'], ensure_ascii=False)
    fj = json.dumps([{"q": a, "a": b} for a, b in u['flashcards']], ensure_ascii=False)
    ej = json.dumps([{"title": t, "wrong": w, "right": r} for t, w, r in u['errors']], ensure_ascii=False)
    khtml = '\n      ' + '\n      '.join('<div class="k-item"><h4>%s</h4><p>%s</p></div>' % (t, d) for t, d in u['knowledge']) + '\n  '

    # knowledge grid block
    s = html.index('<div class="knowledge-grid">')
    e = html.index('</div></div><div id="tab-quiz"', s)
    html = html[:s] + '<div class="knowledge-grid">' + khtml + html[e:]

    # questions array
    s = html.index('const questions=[')
    e = html.index('const flashcards=', s)
    html = html[:s] + 'const questions=' + qj + '\n' + html[e:]

    # flashcards array
    s = html.index('const flashcards=[')
    e = html.index('const errors=', s)
    html = html[:s] + 'const flashcards=' + fj + '\n' + html[e:]

    # errors array
    s = html.index('const errors=[')
    e = html.index('let curQ=0', s)
    html = html[:s] + 'const errors=' + ej + '\n' + html[e:]

    # small replacements
    html = html.replace('<title>勾股定理 · 8年级上数学</title>',
                        '<title>Unit %d · %s · 8年级上英语</title>' % (n, title_en))
    html = html.replace('--primary:#e74c3c', '--primary:#2980b9')
    html = html.replace('<h1><i class="fas fa-book-open"></i> 勾股定理</h1>',
                        '<h1><i class="fas fa-book-open"></i> Unit %d · %s</h1>' % (n, title_en))
    html = html.replace('第1章 勾股定理 · 15 题 · 12 卡牌',
                        '人教版八年级上册 · Unit %d · %d 题 · %d 卡牌' % (n, len(u['questions']), len(u['flashcards'])))
    html = html.replace('为若琳定制的学习工具 | 北师大版八年级上册 · 第1章 | 持续更新中',
                        '为若琳定制的学习工具 | 人教版英语八年级上册 · Unit %d · %s | 持续更新中' % (n, title_en))
    html = html.replace("subject:'勾股定理'", "subject:'英语8上 Unit %d'" % n)
    html = html.replace("tags:'勾股定理,课堂练习'", "tags:'英语8上U%d,课堂练习'" % n)
    html = html.replace('quiz_progress_math8_ch1', 'quiz_progress_english8_u%d' % n)

    out = os.path.join(OUT_DIR, 'english8_u%d_interactive.html' % n)
    with open(out, 'w', encoding='utf-8') as f:
        f.write(html)
    return out

if __name__ == '__main__':
    for u in UNITS:
        p = gen_file(u)
        print('OK', p, 'questions=%d flashcards=%d errors=%d knowledge=%d' % (
            len(u['questions']), len(u['flashcards']), len(u['errors']), len(u['knowledge'])))
    print('TOTAL UNITS:', len(UNITS))
