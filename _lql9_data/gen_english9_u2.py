# -*- coding: utf-8 -*-
"""人教九全英语 Unit 2 互动内容生成器"""
import json, os

data = {
  "hero_title": "Unit 2 · I think that mooncakes are delicious!",
  "meta_desc": "人教九全 · Unit 2",

  "knowledge": [
    {"t": "单元概览与语法主线",
     "d": "本单元话题是中外传统节日（Water Festival 泼水节、Mid-Autumn Festival 中秋节、Halloween 万圣节、Easter 复活节、Christmas 圣诞节），语法重点是两类：①宾语从句（连接词 that / if / whether）；②感叹句（What…! / How…!）。标题句 I think (that) mooncakes are delicious! 正是“主句 I think + that 引导的宾语从句”，口语中 that 常被省略。"},
    {"t": "宾语从句（一）：that 引导的陈述从句",
     "d": "当宾语从句由陈述句变来时，用连接词 that 引导。that 只起连接作用，没有实际词义，在口语和非正式语中常常省略。如 I think (that) mooncakes are delicious. / He said (that) he would come back. 注意：that 从句陈述的是“一件事”，与表“是否”的 if / whether 意思不同。"},
    {"t": "宾语从句（二）：if / whether 表“是否”",
     "d": "由一般疑问句转化来的宾语从句用 if 或 whether 引导，意为“是否”，二者常可互换，且都不能省略，语序要改成陈述语序。如 Do you like it? → I wonder if/whether he likes it.（比较原句助动词 do 要去掉）。whether 用法更宽：与 or not 连用、或从句位于句首时，只能用 whether：I don't know whether he will come or not."},
    {"t": "宾语从句（三）：陈述语序与否定前移",
     "d": "宾语从句一律用“连接词＋主语＋谓语”的陈述语序，不能说 Do you know where is the library? 而要说 Do you know where the library is? 另外，当主句谓语是 think / believe / suppose 等表“认为”的动词、从句想表达否定时，习惯把 not 前移到主句，这叫“否定前移”。如：我认为他不对 → I don't think he is right.（不说 I think he isn't right.）"},
    {"t": "感叹句（一）：What 型",
     "d": "What + 形容词 + 名词（＋主语＋谓语）!，有三种情况：①What a/an + 形 + 单数可数名词：What a clever boy he is! ②What + 形 + 复数名词：What beautiful flowers they are! ③What + 形 + 不可数名词：What fine weather it is! 规则：单数可数名词前必须带 a/an，复数名词和不可数名词前不加 a/an。如 What good news it is!（news 不可数，不加 a）。"},
    {"t": "感叹句（二）：How 型与判断口诀",
     "d": "How + 形容词 / 副词（＋主语＋谓语）! 如 How fast he runs! / How clever the boy is! 判断口诀：先看被强调的中心词是名词还是形容词、副词——中心词是名词（短语）用 What（单数可数要加 a/an），中心词是形容词或副词用 How。同一内容常可互换：What a clever boy he is! = How clever the boy is! What delicious mooncakes they are! = How delicious the mooncakes are!"},
    {"t": "中秋节与嫦娥传说",
     "d": "Mid-Autumn Festival 中秋节：家人团聚，吃月饼（eat mooncakes）、赏月（admire the moon）。最动人的传说是嫦娥奔月：后羿（Hou Yi）射日后，女神赐他仙药（magic medicine），谁喝了谁就能长生不老。坏人逢蒙（Pang Meng）趁后羿不在家来偷药，嫦娥（Chang'e）不肯交出，自己喝下仙药，身体变轻，飞上了月宫。后羿伤心极了，每晚望月呼唤她的名字。后来他见月亮又亮又圆，仿佛看见妻子，就赶紧在园中摆出妻子爱吃的水果点心。从此，人们便在中秋赏月、与家人分享月饼，寄托对亲人的思念。"},
    {"t": "其他节日习俗",
     "d": "①Water Festival 泼水节（泰国等地，在四月中旬的新年期间）：人们上街互相泼水（throw water at each other），寓意洗去霉运、辞旧迎新。②Halloween 万圣节前夜（10 月 31 日，美国等）：孩子们装扮成鬼怪精灵，挨家挨户敲门要糖果，玩“trick or treat”（不给糖就捣蛋），人们还会雕刻南瓜灯。③Easter 复活节（春季）：人们互赠并寻找彩蛋（Easter eggs），彩蛋象征新生命。④Christmas 圣诞节（12 月 25 日）：纪念耶稣诞生，人们互送礼物（presents）。"},
    {"t": "重点短语",
     "d": "put on 穿上/戴上（也可表“增加”）：Put on your coat; it's cold. lay out 摆开、铺开：He laid out the fruits and desserts in the garden. end up 最终成为、最后处于（end up doing sth）：He ended up staying at home. remind sb of sth 使某人想起：The photo reminds me of my grandmother. remind sb to do sth 提醒某人做某事。warn sb (not) to do sth 警告某人（不要）做某事：The sign warns us not to swim here."},
    {"t": "易混词与词形变化",
     "d": "①steal—stole—stolen 偷。②lay—laid—laid 放置、摆开、下蛋；lie—lay—lain 躺、平放；lie—lied—lied 说谎——三组极易混：注意 lie（躺）的过去式 lay 恰与“放置”的原形同形。③die—died—died 死（动词）；dead 死的（形容词）；death 死（名词）。④warm 温暖的（形容词）→warmth 温暖（名词）；warn 警告（动词），拼写别漏 r。⑤present 礼物（名词，同 gift）/ 现在的、出席的（形容词）。"}
  ],

  "questions": [
    {"q": "宾语从句中，连接词 that 的正确说法是（　）",
     "opts": ["表示“是否”，不能省略", "没有实际词义，在口语和非正式语中可以省略", "表示“因为”，必须保留", "用来提问，必须重读"],
     "ans": 1,
     "exp": "that 只起连接作用、没有词义；从句为陈述句时 that 常可省略。表“是否”要用 if/whether，that 并不表“是否”。"},
    {"q": "Do you know ___?",
     "opts": ["where is the library", "where the library is", "the library is where", "where does the library"],
     "ans": 1,
     "exp": "宾语从句必须用“连接词＋主语＋谓语”的陈述语序，疑问语序 where is…/where does… 都不能用。"},
    {"q": "把“Do you like the movie?”改为含宾语从句的句子：He asked me ___ I liked the movie.",
     "opts": ["if", "what", "that", "when"],
     "ans": 0,
     "exp": "原句是一般疑问句，改为宾语从句要用 if/whether 引导、表“是否”（此处备选项中为 if），语序要改成陈述语序 I liked…。"},
    {"q": "“我认为他不是一个好学生。”的正确英语是（　）",
     "opts": ["I think he isn't a good student.", "I don't think he is a good student.", "I not think he is a good student.", "I don't think he isn't a good student."],
     "ans": 1,
     "exp": "主句是 I think/believe 等时，从句的否定习惯上“前移”到主句：I don't think he is a good student.（否定前移）"},
    {"q": "___ clever boy he is!",
     "opts": ["What", "What a", "How", "How a"],
     "ans": 1,
     "exp": "被强调的中心词是名词短语 a clever boy，感叹名词短语用 What；boy 是单数可数名词，必须加 a：What a clever boy he is!"},
    {"q": "___ beautiful flowers they are!",
     "opts": ["What", "What a", "How", "How a"],
     "ans": 0,
     "exp": "中心词是名词短语 beautiful flowers，用 What；flowers 是复数名词，前面不加 a/an。"},
    {"q": "___ fine weather it is!",
     "opts": ["What", "What a", "How", "How a"],
     "ans": 0,
     "exp": "中心词是名词短语 fine weather，用 What；weather 是不可数名词，不加 a/an。"},
    {"q": "___ fast he runs!",
     "opts": ["What", "What a", "How", "How a"],
     "ans": 2,
     "exp": "中心词是副词 fast（没有名词），感叹副词用 How：How fast he runs!"},
    {"q": "___ delicious the mooncakes are!",
     "opts": ["What", "What a", "How", "How a"],
     "ans": 2,
     "exp": "中心词是形容词 delicious，用 How。若改成 What delicious mooncakes they are! 也正确——关键看感叹的中心词是名词还是形容词。"},
    {"q": "— ___ good time we had at the party! — Yes. ___ happy we were!",
     "opts": ["What a; How", "What; What", "How; What a", "What a; What a"],
     "ans": 0,
     "exp": "have a good time 中中心词是可数名词短语 a good time，用 What a；happy 是形容词，用 How。这类“一空 What、一空 How”是经典考法。"},
    {"q": "Halloween falls on ___ 31st.",
     "opts": ["October", "November", "December", "September"],
     "ans": 0,
     "exp": "Halloween 万圣节（前夜）在每年 10 月 31 日，孩子们装扮后挨家敲门要糖果。"},
    {"q": "During the Water Festival in Thailand, people ___ water at each other for good luck.",
     "opts": ["throw", "steal", "lay", "punish"],
     "ans": 0,
     "exp": "泼水节（Water Festival）期间人们上街互相泼水 throw water at each other，寓意洗去霉运、迎来好运。"},
    {"q": "In the folk story, after Chang'e drank the magic medicine, she ___ up to the moon.",
     "opts": ["fly", "flew", "flies", "flown"],
     "ans": 1,
     "exp": "叙述故事用一般过去时：嫦娥喝下仙药后飞（flew）上月宫。flown 不能单独作谓语。"},
    {"q": "Hou Yi ___ out his wife's favorite fruits and desserts in the garden.",
     "opts": ["laid", "lay", "lain", "lied"],
     "ans": 0,
     "exp": "lay out（摆开、铺开）的过去式是 laid。lay—laid—laid（放置）≠lie—lay—lain（躺）≠lie—lied—lied（说谎）。"},
    {"q": "These old photos ___ me ___ my childhood in the countryside.",
     "opts": ["remind; of", "warn; of", "think; of", "remind; to"],
     "ans": 0,
     "exp": "remind sb of sth 意为“使某人想起某事”，主语可以是物；think of 的主语须是人，照片不会 think。"},
    {"q": "At Easter, children often look for colorful ___ as a symbol of new life.",
     "opts": ["mooncakes", "eggs", "dumplings", "turkeys"],
     "ans": 1,
     "exp": "复活节（Easter，在春天）人们寻找彩蛋 Easter eggs，象征新生命；月饼属中秋、饺子粽子属中国年节、火鸡是感恩节/圣诞大餐，勿混淆。"}
  ],

  "flashcards": [
    {"q": "本单元主要学哪两大语法点？",
     "a": "①宾语从句：连接词 that（可省略）、if/whether（表“是否”，不可省略）；②感叹句：What + 名词短语! / How + 形容词或副词!"},
    {"q": "宾语从句中 that 何时可以省略？if 与 whether 有何区别？",
     "a": "that 无实义，从句是陈述句时口语中常省略。if/whether 表“是否”，从句是一般疑问句变来时用，都不能省；与 or not 连用或从句放句首时只用 whether，不用 if。"},
    {"q": "“我认为他不对”英语为什么说 I don't think he is right?",
     "a": "主句谓语是 think/believe/suppose 时，从句的否定习惯前移到主句，叫“否定前移”。不说 I think he isn't right. 又如 I don't think it will rain.（我认为不会下雨。）"},
    {"q": "感叹句 What 与 How 怎么区分？请各举一例。",
     "a": "看被强调的中心词：是名词短语用 What（单数可数加 a/an），是形容词/副词用 How。如 What a clever boy he is! / What beautiful flowers they are! / What fine weather it is! / How fast he runs! / How delicious the mooncakes are!"},
    {"q": "中秋节有哪些习俗？嫦娥奔月的故事大意是什么？",
     "a": "Mid-Autumn Festival 是家庭团聚的节日，人们吃月饼（mooncakes）、赏月（admire the moon）。传说后羿射日后获女神所赐仙药，坏人逢蒙来偷，嫦娥不肯交出、自己喝下，飞上月宫；后羿望月思念，摆出她爱吃的水果点心。此后人们便在中秋赏月、分享月饼寄托团圆思念。"},
    {"q": "泰国泼水节（Water Festival）的时间、习俗和寓意是什么？",
     "a": "泼水节在四月中旬泰国新年期间举行：人们走上街头互相泼水 throw water at each other，寓意洗去过去一年的霉运、迎接崭新的一年。"},
    {"q": "Halloween 是哪一天？人们怎么庆祝？",
     "a": "Halloween 万圣节（前夜）在每年 10 月 31 日。孩子们装扮成鬼怪等（dress up as ghosts…）挨家敲门要糖果（trick or treat，不给糖就捣蛋），人们还雕南瓜灯。"},
    {"q": "Easter（复活节）在什么时候？有什么象征物？",
     "a": "Easter 在春天（每年春分月圆后的第一个星期日前后）。人们互赠、寻找复活节彩蛋 Easter eggs，彩蛋象征新生命（new life）。"},
    {"q": "put on、lay out、end up、remind…of、warn…to do 分别怎么用？",
     "a": "put on 穿上/戴上：Put on your coat. lay out 摆开、铺开：He laid out the fruits. end up（doing）最终……：He ended up staying home. remind sb of sth 使某人想起：The song reminds me of my childhood. warn sb (not) to do sth 警告某人（不要）做：They warned us not to swim here."},
    {"q": "lay / lie（躺）/ lie（说谎）三组动词的过去式分别是什么？",
     "a": "lay—laid—laid 放置、摆开、下蛋（课文：Hou Yi laid out fruits and desserts.）；lie—lay—lain 躺；lie—lied—lied 说谎。注意 lie（躺）的过去式 lay 与“放置”的原形同形，最容易混。"}
  ],

  "errors": [
    {"title": "把 that 当成“是否”或以为 must 保留",
     "wrong": "写宾语从句时，一见到从句就担心丢分而硬加 that，或者把 that 当成“是否”。",
     "right": "that 在宾语从句中无实义、可省略（口语常省）；表“是否”的是 if/whether，且 if/whether 不能省略。判断依据：从句是陈述句用 that（可省），从句由一般疑问句变来用 if/whether。"},
    {"title": "if/whether 从句仍用疑问语序",
     "wrong": "把疑问句直接搬进从句：I wonder if does he like the movie.（助动词 still 提前）",
     "right": "宾语从句一律用陈述语序：I wonder if he likes the movie. 原问句的助动词 do/does/did 在从句中要去掉，主语放谓语之前。"},
    {"title": "把“我认为他不……”直译成 I think he isn't…",
     "wrong": "按汉语语序把否定留在从句里：I think he is not a good student. / I think he isn't right.",
     "right": "主句是 I think/believe/suppose 等表“认为”的动词时，习惯把 not 前移到主句（否定前移）：I don't think he is a good student. / I don't think he is right."},
    {"title": "感叹句用错 What/How，或漏 a/an、给不可数加 a/an",
     "wrong": "How beautiful flowers they are!（中心词是名词却用 How）；What clever boy he is!（单数可数漏了 a）；What a good news it is!（news 不可数却加了 a）。",
     "right": "先看中心词：名词短语用 What，形容词/副词用 How。改对：What beautiful flowers they are! / What a clever boy he is! / What good news it is!"},
    {"title": "lay（放置）与 lie（躺/说谎）的过去式混淆",
     "wrong": "把“摆开”写成 Hou Yi lied out the fruits. 或 Hou Yi lay out the fruits.（时态、词形都不对）",
     "right": "lay—laid—laid（放置、摆开、下蛋），lie—lay—lain（躺），lie—lied—lied（说谎）。课文原句是 Hou Yi laid out her favorite fruits and desserts in the garden."},
    {"title": "节日习俗张冠李戴",
     "wrong": "把 Halloween 记在 12 月、把泼水说成端午习俗、把吃粽子安到中秋节上。",
     "right": "中秋节吃月饼、赏月；泰国泼水节互相泼水迎新；Halloween 是 10 月 31 日（装扮讨糖）；复活节在春天、彩蛋象征新生；端午吃粽子赛龙舟、感恩节吃火鸡、圣诞收礼物——逐一对应，别记串。"}
  ]
}

path = "/home/administrator/xuci-jiancha/_lql9_data/english9_u2.json"
with open(path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=1)
    f.write("\n")

with open(path, encoding="utf-8") as f:
    check = json.load(f)

print("file:", path)
print("hero_title:", check["hero_title"])
print("meta_desc:", check["meta_desc"])
print("knowledge:", len(check["knowledge"]))
print("questions:", len(check["questions"]))
print("flashcards:", len(check["flashcards"]))
print("errors:", len(check["errors"]))

# 每题校验：4 个选项、ans 越界
bad = []
for i, q in enumerate(check["questions"]):
    if len(q["opts"]) != 4 or not (0 <= q["ans"] < 4):
        bad.append(i)
print("bad_questions:", bad)
