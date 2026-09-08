# -*- coding: utf-8 -*-
"""生成 english9_u11.json — 人教九全 Unit 11 Sad movies make me cry."""
import json, os

data = {
    "hero_title": "Unit 11 · Sad movies make me cry.",
    "meta_desc": "人教九全 · Unit 11",
    "knowledge": [
        {
            "t": "单元话题 · 情绪与感受",
            "d": "语言目标：谈论事物如何影响你的情绪（Talk about how things affect you）。单元标题 Sad movies make me cry.（悲伤的电影让我哭）就是全单元的语法核心句。功能句型：What makes you angry? — When people throw rubbish on the streets, it makes me angry. 情绪形容词可按褒贬归类：正面 happy / relaxed / comfortable / lucky；负面 sad / nervous / angry / uncomfortable / mad / uneasy / awful。Self Check 提示：健康、家庭、友谊（health, family, friendship）比名声、权力、财富更能让人真正快乐。"
        },
        {
            "t": "make + 宾语 + 动词原形（省略 to）",
            "d": "使役动词 make 后接“宾语 + 省略 to 的动词原形”作宾语补足语，表示“使某人做某事”，动作由宾语发出：Sad movies make me cry.（单元标题句。）She said that the sad movie made her cry.（Grammar Focus 原句——注意 made 表过去。）Sad movies don't make John cry. They just make him want to leave.（2b 听力：他只是想离开——want 是省 to 的原形，want 后面再带自己的 to leave。）要点：主动句中 to 必须省略，不能说 made me to cry。"
        },
        {
            "t": "make + 宾语 + 形容词 / 名词",
            "d": "make 后接“宾语 + 形容词”作宾补，表示“使某人/某物处于某种状态”：The loud music makes me nervous.（吵闹的音乐让我紧张——Grammar Focus 原句。）Money and fame don't always make people happy.（金钱和名声并不总能使人快乐。）But that music makes me sleepy.（1c：那种音乐让我犯困。）The awful pictures make Amy uncomfortable.（1b 听力。）注意：宾补用形容词而不用副词，不说 makes me happily；也可用比较级如 make our friendship stronger（2d：让我们的友谊更牢固）。"
        },
        {
            "t": "被动语态 be made to do（to 还原）",
            "d": "主动句中 make sb do sth 省略了 to，但变为被动语态时 to 必须还原，结构为 sb be made to do sth，意为“被迫/被要求做某事”：主动 The boss made me work late. → 被动 I was made to work late.（我被要求加班到很晚。）再如 He was made to apologize to his classmate. 注意还原后 to 后仍接动词原形。口诀：主动省 to，被动还 to。同类规则也适用于 see / hear / watch sb do → be seen / heard / watched to do。"
        },
        {
            "t": "使役动词 vs 普通动词：宾语后接 do 还是 to do",
            "d": "make / let / have 是使役动词，接“宾语 + 动词原形（省 to）”：make me cry、let me go、have him wait。而 ask / tell / want 是普通动词，接“宾语 + 带 to 的不定式”：ask sb to do、tell sb to do、want sb to do。教材 2d 例句：Why don't you ask Alice to join you each time you do something with Julie?（每次你和朱莉在一起时，何不邀请艾丽斯加入呢？）判断方法：表示“使/让/允许”的使役词省 to；表示“要求/告诉/想要”的普通词必须带 to——不能说 ask me help，也不能说 make me to cry。"
        },
        {
            "t": "feel like doing sth 想要做某事",
            "d": "feel like 意为“想要”，后接名词或动名词（doing），不能接动词原形或 to do：The king didn't feel like eating.（3a 原文：国王不想吃东西。）I feel like going for a walk.（我想去散散步。）4b 调查表里还有 What makes you feel like dancing? 注意另一用法：feel like + 句子 = “感觉好像”，如《The Winning Team》中 He felt like there was a heavy weight on his shoulders.（他感觉肩上像压着千斤重担。）想要做某事若要接 to do，改用 want to do / would like to do。"
        },
        {
            "t": "would rather do A than do B 宁愿……而不愿……",
            "d": "would rather（缩写 'd rather）意为“宁愿”，是情态性短语，后接动词原形，不受主语人称影响：I'd rather go to Blue Ocean because I like to listen to quiet music while I'm eating.（1c 对话 Amy 原句：我宁愿去蓝海餐厅……）比较取舍用 than，than 前后结构平行、都用动词原形：He would rather stay at home than go shopping.（他宁愿待在家也不去购物。）否定式 would rather not do sth。另学连词短语 rather than“而不是”，如 with courage rather than fear（2b：带着勇气而不是恐惧）。"
        },
        {
            "t": "drive sb crazy / mad 使某人发疯",
            "d": "drive 本义“驾驶”，引申为“驱使、逼迫”。drive sb crazy / mad 意为“把某人逼疯/逼得发狂”，等于 make sb crazy / mad：Waiting for Amy drove Tina crazy.（2b 听力原句：等艾米把蒂娜急疯了——drove 是 drive 的过去式。）The endless noise next door is driving me mad.（隔壁没完没了的噪音快把我逼疯了。）宾语后接形容词 crazy / mad 作宾补，不加 to、也不加 -ly（不说 drive me crazily）。记住变位 drive—drove—driven。"
        },
        {
            "t": "the more…, the more… 越……越……",
            "d": "结构“the + 比较级…, the + 比较级…”表示“越……就越……”，两部分都以比较级开头，后一部分是结果：The more I get to know Julie, the more I realize that we have a lot in common.（2d 对话原句：我越了解朱莉，就越发现我们有很多共同点。）又如 The more you practise, the better you will play. 注意：句首两个 the 都不能省略；比较级形式要写对——The more careful you are, the fewer mistakes you will make.（mistakes 是可数名词复数，用 fewer 而不用 less。）"
        },
        {
            "t": "课文速览 · 快乐与团队",
            "d": "Section A 3a《The Shirt of a Happy Man (Part I)》：富饶国度里住着不开心的国王——他睡不好、脸色苍白如粉笔（pale as chalk）、不想吃饭、无缘无故地哭。医生说他病在心里，需要穿上“一个快乐之人的衬衫”。可拥有权力的首相担心失去权力，拥有财富的银行家担心钱财被盗，有名的宫廷歌星担心被人追随——竟没有一个人快乐。将军受命三天之内找到快乐的人。启示：权力、财富、名声（power, wealth, fame）换不来快乐。Section B 2b《The Winning Team》：Peter 错过进球令球队失利，他担心被教练踢出球队（kick sb off the team）、觉得让全队失望（let his whole team down）。父亲的劝慰让他明白“足球靠的是团队努力（team effort），输赢只是比赛的一半，另一半是学会与队友沟通、从错误中学习”。第二天他鼓起勇气向队友道歉（with courage rather than fear），令他又惊又喜的是（to his surprise and relief）队友们点头同意（nodded in agreement）：“输球从来不只是某一个人的错。”大家齐心协力（pull together），Peter 感到自己正处在一支“制胜的队伍”里——友谊让球队赢得未来。"
        }
    ],
    "questions": [
        {
            "q": "Sad movies make me ____.",
            "opts": ["cry", "to cry", "crying", "cried"],
            "ans": 0,
            "exp": "单元标题句。make sb do sth：make 后接“宾语 + 省略 to 的动词原形”作宾补，不能说 made me to cry。口诀：看到 make/let/have + 人，宾补优先想动词原形。"
        },
        {
            "q": "Sad movies don't make John cry. They just make him want to ____.",
            "opts": ["leave", "to leave", "leaving", "left"],
            "ans": 0,
            "exp": "2b 听力原句。make him want to leave 有两层：make sb do（want 是省略 to 的原形）+ want to leave（want 自己后接不定式 to leave）。题干空白处是 make him 后的省 to 原形，故选 leave。"
        },
        {
            "q": "The awful pictures make Amy ____.",
            "opts": ["uncomfortable", "comfortable", "happily", "excited"],
            "ans": 0,
            "exp": "1b 听力原句：可怕的图片让艾米不舒服。make sb + 形容词作宾补；comfortable 是 uncomfortable 的反义词、happily 是副词不能作宾补、excited“兴奋的”与句意不符。"
        },
        {
            "q": "Soft and quiet music makes me ____.",
            "opts": ["relax", "to relax", "relaxing", "relaxed"],
            "ans": 0,
            "exp": "Grammar Focus 原句：轻柔安静的音乐让我放松。make sb do sth——此处需要动词 relax 作省 to 的宾补；relaxed（感到放松的）和 relaxing（令人放松的）是形容词，若想表达“让我放松”状态可说 makes me relaxed，但按教材句式选动词 relax。"
        },
        {
            "q": "He was made ____ the piano for two hours every day when he was a child.",
            "opts": ["play", "to play", "playing", "played"],
            "ans": 1,
            "exp": "make sb do sth 变为被动语态 be made to do sth 时，省略的 to 必须还原：He was made to play...（他小时候被迫每天练两小时钢琴。）口诀：主动省 to，被动还 to。"
        },
        {
            "q": "Don't let the little children ____ in the street. It's dangerous.",
            "opts": ["play", "to play", "playing", "played"],
            "ans": 0,
            "exp": "let sb do sth，与 make 同类使役动词，宾语后接省略 to 的动词原形：let children play。否定祈使句 Don't let... 后同样省 to。"
        },
        {
            "q": "The boss had the workers ____ ten hours a day to finish the work on time.",
            "opts": ["work", "to work", "working", "worked"],
            "ans": 0,
            "exp": "have sb do sth 使/让某人做某事，宾语 the workers 与动作 work 是主动关系，用省 to 的原形。注意与 have sth done 区分：宾语和动作是被动关系才用过去分词，如 have the car repaired。"
        },
        {
            "q": "Why don't you ask Alice ____ you each time you do something with Julie?",
            "opts": ["join", "to join", "joining", "joined"],
            "ans": 1,
            "exp": "2d 对话原句。ask sb to do sth 邀请/要求某人做某事，后接带 to 的不定式，与 make/let/have sb do（省 to）形成对比——ask 属于“要求”类普通动词，必须带 to。"
        },
        {
            "q": "My parents want me ____ a doctor in the future.",
            "opts": ["be", "to be", "being", "been"],
            "ans": 1,
            "exp": "want sb to do sth 想要某人做某事，后接带 to 的不定式。记住：只有 make/let/have 三个使役词才省 to，want/ask/tell 都要带 to。"
        },
        {
            "q": "The unhappy king didn't feel like ____ anything.",
            "opts": ["eat", "to eat", "eating", "ate"],
            "ans": 2,
            "exp": "3a 课文原句：不开心的国王什么都不想吃。feel like doing sth 想要做某事，后接动名词，不接动词原形或 to do。"
        },
        {
            "q": "I'd rather ____ to Blue Ocean because I like to listen to quiet music while I'm eating.",
            "opts": ["go", "to go", "going", "gone"],
            "ans": 0,
            "exp": "1c 对话原句（Amy）。would rather（'d rather）后接动词原形：would rather go to...，表示“宁愿去……”。"
        },
        {
            "q": "He would rather walk to school ____ take a bus.",
            "opts": ["than", "to", "but", "and"],
            "ans": 0,
            "exp": "would rather do A than do B 宁愿做 A 而不愿做 B，than 前后动词都用原形、结构平行：would rather walk than take a bus。"
        },
        {
            "q": "Waiting for Amy drove Tina ____.",
            "opts": ["crazy", "crazily", "madly", "angrily"],
            "ans": 0,
            "exp": "2b 听力原句：等艾米把蒂娜急疯了。drive sb crazy 使某人发疯，drove 是 drive 的过去式；crazy 是形容词作宾语补足语，不能用副词 crazily/madly。"
        },
        {
            "q": "____ you eat, the fatter you will be.",
            "opts": ["The more", "More", "The most", "Much"],
            "ans": 0,
            "exp": "the + 比较级…, the + 比较级… 表示“越……就越……”，句首两个 the 都不能省略：The more you eat, the fatter you will be.（吃得越多越胖。）教材 2d 原句：The more I get to know Julie, the more I realize that we have a lot in common."
        },
        {
            "q": "Peter was worried that his coach might kick him ____ the team.",
            "opts": ["off", "down", "out", "away"],
            "ans": 0,
            "exp": "2b 课文原句：教练可能把他踢出球队。kick sb off the team 把某人开除/撵出球队；若用 out 则要说 kick sb out of the team（of 不能省）。"
        },
        {
            "q": "To his surprise and ____, his teammates all nodded in agreement.",
            "opts": ["relief", "wealth", "courage", "power"],
            "ans": 0,
            "exp": "2b 课文原句：令他既惊讶又宽慰的是，队友们都点头同意。relief 名词“宽慰”，to one's relief 令某人宽慰的是；wealth 财富、courage 勇气、power 权力均不合句意。"
        }
    ],
    "flashcards": [
        {
            "q": "make sb do sth（使某人做某事 · 省略 to）",
            "a": "make + 宾语 + 动词原形：Sad movies make me cry.（单元标题句。）She said that the sad movie made her cry. Sad movies make him want to leave.（make 后 want 省 to，want 自己再带 to leave。）注意：主动句中 to 必须省略，不能说 made me to cry。"
        },
        {
            "q": "make sb + 形容词（使某人处于……状态）",
            "a": "形容词作宾语补足语，说明宾语的状态：The loud music makes me nervous. Money and fame don't always make people happy. But that music makes me sleepy. The awful pictures make Amy uncomfortable. 宾补用形容词不用副词——不说 makes me happily；还可接比较级：make our friendship stronger."
        },
        {
            "q": "被动语态 be made to do（to 还原）",
            "a": "主动 make sb do 省 to，变被动时 to 必须还原：He was made to apologize. / I was made to wait outside. 结构：sb + be made + to do sth（被迫做某事）。口诀：主动省 to，被动还 to。"
        },
        {
            "q": "make / let / have sb do 与 ask / tell / want sb to do",
            "a": "使役词 make/let/have + 宾语 + 动词原形（省 to）：make me cry、let me go、have him wait。普通动词 ask/tell/want + 宾语 + 带 to 不定式：ask Alice to join you（2d）、tell him to stop、want you to come。记法：表“使/让/允许”的省 to；“要求/告诉/想要”的带 to。"
        },
        {
            "q": "feel like doing sth（想要做某事）",
            "a": "feel like 想要，后接动名词或名词，绝不接 to do / 动词原形：The king didn't feel like eating.（3a）I feel like going for a walk. Do you feel like a cup of tea? 想要做某事若要接 to do，用 want to do / would like to do。另义：feel like + 句子 = 感觉好像：He felt like there was a heavy weight on his shoulders.（2b）"
        },
        {
            "q": "would rather do A than do B（宁愿……而不愿……）",
            "a": "would rather（'d rather）+ 动词原形：I'd rather go to Blue Ocean.（1c）取舍句 would rather do A than do B，than 后也用动词原形：He would rather stay at home than go shopping. 否定：would rather not do sth. 另有连词短语 rather than = 而不是：with courage rather than fear（2b）。"
        },
        {
            "q": "drive sb crazy / mad（使某人发疯）",
            "a": "drive（drive—drove—driven）除“驾驶”外表“驱使、逼迫”：Waiting for Amy drove Tina crazy.（2b 听力）The noise is driving me mad. 宾语后接形容词 crazy/mad 作宾补，不加 to、不加 -ly。同义：make sb crazy；习语 drive sb up the wall 把某人逼疯。"
        },
        {
            "q": "the more…, the more…（越……越……）",
            "a": "结构：the + 比较级…, the + 比较级…，后一部分是结果：The more I get to know Julie, the more I realize that we have a lot in common.（2d 原句）The more you practise, the better you will play. 两个 the 不能省，比较级形式要写对：The more careful you are, the fewer mistakes you will make.（mistakes 可数用 fewer）"
        },
        {
            "q": "《The Winning Team》词块（Section B 2b）",
            "a": "a heavy weight on his shoulders 肩头沉甸甸；miss scoring a goal 错过进球；let his whole team down 让全队失望；kick sb off the team 把某人踢出球队；be too hard on oneself 对自己太苛刻；team effort 团队努力；winning or losing is only half the game 输赢只是比赛的一半；with courage rather than fear 带着勇气而非恐惧；pull together 齐心协力；nod in agreement 点头同意；to his surprise and relief 令他既惊讶又宽慰的是；It's never just one person's fault. 绝不是某一个人的错。"
        },
        {
            "q": "本单元词汇速记",
            "a": "rather 相当；宁愿（would rather）；drive 驾驶；驱使（drove/driven）；friendship 友谊；king 国王；power 权力；banker 银行家；pale 苍白的（pale as chalk 面如死灰）；examine 检查；wealth 财富；to start with 首先；grey 灰色的；lemon 柠檬；uncomfortable 不舒服的；weight 重量；shoulder 肩膀；goal 进球；目标；coach 教练；kick 踢；courage 勇气；pull 拉（pull together 齐心协力）；relief 宽慰（to one's relief）；agreement 同意；fault 过错；leave out 冷落；忽略；call in 召来（The doctor was called in. 医生被请来。）；take it easy 放轻松；let sb down 使某人失望。"
        }
    ],
    "errors": [
        {
            "title": "make / let / have 后误加 to",
            "wrong": "把单元标题句写成 The sad movie made me to cry.，或把“妈妈让我做作业”写成 My mother let me to do my homework.",
            "right": "使役动词 make / let / have + 宾语 + 动词原形（省略 to）：made me cry；let me do my homework。但同一结构一旦变被动，to 必须还原：He was made to work late.（他被要求加班。）两步口诀：主动省 to，被动还 to。"
        },
        {
            "title": "ask / tell / want 后漏掉 to",
            "wrong": "写成 My mother asked me go shopping. 或 The teacher told us keep quiet.",
            "right": "ask / tell / want sb to do sth，带 to 的不定式不能省：asked me to go shopping；told us to keep quiet。判别：只有表“使/让/允许”的 make / let / have 才省 to；表示“要求/告诉/想要”的普通动词必须带 to。别一看到中文“让”就省 to——得看它对应的是哪个英文动词。"
        },
        {
            "title": "feel like 后误接 to do / 动词原形",
            "wrong": "把“我想去散步”写成 I feel like to go for a walk.，或把 3a 句写成 The king didn't feel like eat.",
            "right": "feel like doing sth 想要做某事，后接动名词或名词，不接 to do：The king didn't feel like eating.（3a 原文）；I feel like going for a walk. 想要做某事若要接 to do，改用 want to do / would like to do。另注意 feel like + 句子 = “感觉好像”：He felt like there was a heavy weight on his shoulders."
        },
        {
            "title": "would rather 后误接 to do，than 前后不平行",
            "wrong": "写成 I'd rather to stay at home. 或 He would rather walk than to take a bus.",
            "right": "would rather 后接动词原形：I'd rather stay at home. 取舍句 would rather do A than do B，than 后同样用动词原形：He would rather walk than take a bus. 否定用 would rather not do sth：I would rather not tell her about it."
        },
        {
            "title": "drive 变位错误 / 宾补误用副词",
            "wrong": "把 2b 句写成 Waiting for Amy drived me crazy.，或把 Grammar Focus 句写成 The loud music makes me happily. / The noise is driving me crazily.",
            "right": "drive 的过去式是 drove、过去分词 driven：Waiting for Amy drove Tina crazy. make / drive + 宾语 + 形容词（nervous / happy / crazy / mad）作宾补，副词不能作宾补：makes me happy，不是 makes me happily。"
        },
        {
            "title": "the more…, the more… 漏 the 或比较级写错",
            "wrong": "写成 More you eat, fatter you will be.，或 The more you read, the more good your English will be.",
            "right": "结构为 the + 比较级…, the + 比较级…，两个 the 都不能省，比较级形式必须正确：The more you eat, the fatter you will be.（fatter 不是 fat）；The more you read, the better your English will be.（better 不是 more good）。越吃越胖、越读越好——前因后果两部分都要用比较级开头。"
        }
    ]
}

os.makedirs("/home/administrator/xuci-jiancha/_lql9_data", exist_ok=True)
path = "/home/administrator/xuci-jiancha/_lql9_data/english9_u11.json"
with open(path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=1)

with open(path, encoding="utf-8") as f:
    chk = json.load(f)

print("file:", path)
print("keys:", list(chk.keys()))
print("knowledge:", len(chk["knowledge"]))
print("questions:", len(chk["questions"]))
print("flashcards:", len(chk["flashcards"]))
print("errors:", len(chk["errors"]))
# sanity checks
for i, q in enumerate(chk["questions"]):
    assert len(q["opts"]) == 4 and 0 <= q["ans"] <= 3, i
    assert all(op != q["opts"][q["ans"]] for j, op in enumerate(q["opts"]) if j != q["ans"])
print("questions OK (4 opts each, ans in range, unique)")
assert chk["hero_title"].startswith("Unit 11")
assert chk["meta_desc"] == "人教九全 · Unit 11"
print("hero/meta OK")
print("ALL VALID")
