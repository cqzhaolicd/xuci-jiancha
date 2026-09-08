# -*- coding: utf-8 -*-
"""Build english9_u12.json (人教九全 Unit 12 Life is full of the unexpected.)"""
import json, os

data = {
 "hero_title": "Unit 12 · Life is full of the unexpected.",
 "meta_desc": "人教九全 · Unit 12",
 "knowledge": [
  {
   "t": "单元话题 · 意外与过去完成时",
   "d": "本单元话题是“意外经历”：倒霉的一天（睡过头、错过公交、把书包落在家里）和愚人节（April Fool's Day）整人／被骗的经历。核心语法是过去完成时（the past perfect tense）：had + 动词过去分词，表示“过去的过去”——即发生在过去某一动作或时间点之前的动作。单元标题句 Life is full of the unexpected.（生活中充满了意外之事。）正是用 be full of 点题。"
  },
  {
   "t": "过去完成时 · 构成与“过去的过去”",
   "d": "结构：had + 过去分词（had done），所有人称都用 had。表示在过去某时之前已经发生的动作——先发生的用 had done。教材核心句：By the time I got up, my brother had already gotten in the shower.（到我起床时，哥哥已经进淋浴间洗澡了。）先发生的是“哥哥洗澡”，后发生的是“我起床”，所以哥哥的动作用 had already gotten。get 的过去分词美式英语用 gotten，英式英语常用 got。否定：had not (hadn't) done；疑问：Had + 主语 + done?"
  },
  {
   "t": "by the time / when / before 与过去完成时",
   "d": "by the time / when / before 引导时间状语从句时，从句常用一般过去时，主句用过去完成时，表示主句动作先于从句动作发生。教材 Grammar Focus 例句：By the time I got outside, the bus had already left.（我到外面时，公交车已经开走了——车先开走）；When I got to school, I realized I had left my backpack at home.（我到校才意识到把书包落在家里了——落书包在先）；Before I got to the bus stop, the bus had already left. 判断方法：找到两个过去的动作，哪个先发生，哪个就用 had done。"
  },
  {
   "t": "go off · 闹钟响",
   "d": "go off 在本单元意为“（闹钟等）响”：My alarm didn't go off.（我的闹钟没响。）go off 还可表示“（炸弹）爆炸；（枪）开火”；人“离开”用 leave / go away。同义表达：闹钟响了 = The alarm went off = The alarm clock rang（ring 的过去式是 rang，过去分词是 rung）。闹钟没响的结果自然是睡过头：oversleep（过去式 overslept）。课文原句：I woke up at 10:00 a.m. and realized that my alarm had never gone off.（我上午十点醒来，才发现闹钟根本没响过。）"
  },
  {
   "t": "be full of = be filled with",
   "d": "be full of 充满……，与 be filled with 同义，但介词不同：full 后接 of，filled 后接 with。Life is full of the unexpected. = Life is filled with the unexpected.（生活充满意外。）The room was full of people. = The room was filled with people.（房间里挤满了人。）full 不能接 with，filled 不能接 of，这是高频考点。"
  },
  {
   "t": "Section A 3a ·《Life Is Full of the Unexpected》",
   "d": "课文讲作者两次“幸运的意外”。第一次（2001年9月11日）：他正要上楼进办公室（I was about to go up to my office when...）时决定先去买杯咖啡，结果第一架飞机撞上了他的办公楼；他和同事们 stare in disbelief at the black smoke rising above the burning building（难以置信地凝视着燃烧的大楼上空升起的黑烟），庆幸自己还活着（I felt lucky to be alive.）。第二次（2011年2月21日）：他在新西兰地震前一天因错过飞机而逃过一劫——醒来时已上午十点（alarm had never gone off），跳下床直奔机场（went straight to the airport），可飞机早已起飞（had already taken off），只好等到第二天，结果得知了新西兰地震的消息：My bad luck had unexpectedly turned into a good thing.（我的倒霉竟意外地变成了好事。）"
  },
  {
   "t": "Section B 2b · April Fool's Day 愚人节",
   "d": "阅读介绍 April Fool's Day（4月1日愚人节）上的整人与被骗玩笑：有人被朋友邀请参加化妆舞会（costume party），兴冲冲赶到（show up）才发现是玩笑；一位电视明星在节目里向女友求婚，女友说 yes 后他却说 “April Fool!”，结果 end up 失去女友、节目也被砍（ended up losing his girlfriend and his show was cancelled）；英国一则“意大利面（spaghetti）绝产”的假报道，让大家冲进超市抢购，等人们发现是骗局（hoax）时，全国的意大利面都被卖光了（had been sold out）。相关词：fool 傻瓜／愚弄（人）；embarrassed 感到尴尬的。"
  },
  {
   "t": "易混易错词族",
   "d": "① costume 戏装、化妆服 vs custom 风俗习惯 vs customer 顾客：costume party 化妆舞会。② embarrassed 感到尴尬的（修饰人）vs embarrassing 令人尴尬的（修饰事物）：He felt embarrassed. / It was an embarrassing moment. ③ alive 活着的（表语形容词，说 be alive，不放在名词前）vs living 活着的（可作定语）：the living people。④ above 在……上方（不一定垂直）vs over 在……正上方。⑤ burn 燃烧（过去式／过去分词 burned / burnt），burning 燃烧着的，作定语：the burning building 燃烧的大楼。⑥ unexpected 出乎意料的，the unexpected 意外之事；disbelief 不相信（dis- 否定前缀 + belief）。"
  },
  {
   "t": "重点短语速记（一）· 倒霉的一天",
   "d": "by the time 到……的时候；go off （闹钟）响；wake up 醒来（woke up）；get up 起床（got up）；get dressed 穿好衣服；put on 穿上；take a shower / get in the shower 洗澡、淋浴；oversleep 睡过头（overslept）；jump out of bed 跳下床；go straight to 直奔；run to the bus stop 跑向公交站；wait for sb 等某人；leave sth at home 把某物落在家里。"
  },
  {
   "t": "重点短语速记（二）· 愚人节与句型",
   "d": "be full of 充满（= be filled with）；show up 出现、露面；end up doing sth 最终（落得）做某事；sell out 卖光；stare in disbelief at sth 难以置信地凝视某物；take off （飞机）起飞；turn into 变成；wait in line 排队等候。句型：be about to do sth when... 正要做某事，这时……（3a：I was about to go up to my office when I decided to get a coffee first.）；过去完成时中常与 already / never / just 连用（had already gotten / had never gone off）。"
  }
 ],
 "questions": [
  {
   "q": "By the time I got up, my brother ____ already gotten in the shower.",
   "opts": ["has", "had", "have", "was"],
   "ans": 1,
   "exp": "过去完成时核心句：哥哥“洗澡”发生在我“起床”之前——过去的过去，先发生的动作用 had + 过去分词，故选 had already gotten。get 的过去分词美式用 gotten。教材原句：By the time I got up, my brother had already gotten in the shower."
  },
  {
   "q": "When I got to school, I realized I ____ my backpack at home.",
   "opts": ["leaves", "has left", "had left", "is leaving"],
   "ans": 2,
   "exp": "“落书包”发生在“到校、意识到”之前，即过去中的过去，用过去完成时 had left。教材原句：When I got to school, I realized I had left my backpack at home. realize 后接宾语从句，that 可省略；leave sth at home 把某物落在家里。"
  },
  {
   "q": "The bus ____ already left by the time I got to the bus stop.",
   "opts": ["has", "had", "have", "is"],
   "ans": 1,
   "exp": "公交车“先开走”，我“后到站”——先发生的动作用过去完成时 had already left；by the time 引导的从句用一般过去时 got。教材 Grammar Focus 句：By the time I got outside, the bus had already left."
  },
  {
   "q": "My alarm didn't ____ this morning, so I woke up late.",
   "opts": ["go off", "go on", "go out", "go away"],
   "ans": 0,
   "exp": "go off （闹钟）响：My alarm didn't go off.（我的闹钟没响。）didn't 后接动词原形。go on 继续、go out 外出／熄灭、go away 离开，均不合句意。闹钟没响的结果是睡过头（oversleep）。"
  },
  {
   "q": "The alarm clock ____ loudly at six o'clock, but I was still sleeping.",
   "opts": ["rang", "rung", "rings", "ringing"],
   "ans": 0,
   "exp": "句中有过去时间 at six o'clock，叙述过去发生的动作，用 ring 的过去式 rang（响了）；rung 是过去分词，须与 has / had 连用。闹钟响了也可说 The alarm went off.，两者同义。"
  },
  {
   "q": "By the time I ____ to the airport, my plane to New Zealand had already taken off.",
   "opts": ["get", "got", "had got", "was getting"],
   "ans": 1,
   "exp": "by the time 引导的时间状语从句用一般过去时（got 我到机场是较后发生的动作），主句动作（飞机起飞）先发生、用过去完成时 had already taken off；不要两个分句都用过去完成。课文原句：…by the time I got to the airport, my plane to New Zealand had already taken off."
  },
  {
   "q": "Life is full ____ the unexpected.",
   "opts": ["of", "with", "in", "for"],
   "ans": 0,
   "exp": "be full of 充满……，介词用 of：Life is full of the unexpected.（生活中充满意外。）同义表达 be filled with 才用 with，不可写成 full with the unexpected。"
  },
  {
   "q": "The bottle is full of milk. → The bottle is ____ with milk.",
   "opts": ["fill", "filled", "filling", "full"],
   "ans": 1,
   "exp": "be full of = be filled with 同义转换：fill 的过去分词 filled 作表语，接介词 with。is filled with milk = is full of milk（瓶子里装满了牛奶）。"
  },
  {
   "q": "We ____ in disbelief at the black smoke rising above the burning building.",
   "opts": ["stared", "smiled", "laughed", "sang"],
   "ans": 0,
   "exp": "stare at 凝视、盯着看；stare in disbelief 难以置信地凝视（in disbelief 作方式状语，意为“难以置信地”）。教材3a原句描写人们望着燃烧的大楼上空升起的黑烟。smile / laugh / sing 均不合语境。"
  },
  {
   "q": "My bad luck had unexpectedly ____ into a good thing.",
   "opts": ["turned", "turning", "turns", "turn"],
   "ans": 0,
   "exp": "turn into 变成；had + 过去分词构成过去完成时，turn 的过去分词仍是 turned。课文3a末句：My bad luck had unexpectedly turned into a good thing.（我的倒霉竟意外地变成了一件好事。）"
  },
  {
   "q": "He said he would come to my party, but he never ____ up.",
   "opts": ["showed", "gave", "woke", "stayed"],
   "ans": 0,
   "exp": "show up 出现、露面：he never showed up 他根本没露面。give up 放弃、wake up 醒来、stay up 熬夜，均不合句意。“答应来却始终没出现”正是愚人节课文里的整人桥段。"
  },
  {
   "q": "The TV star's joke had a bad ending. He ____ up losing his girlfriend.",
   "opts": ["ended", "showed", "woke", "gave"],
   "ans": 0,
   "exp": "end up doing sth 最终（落得）做某事：ended up losing his girlfriend（最终失去了女友）。课文2b：他在节目上开“求婚”玩笑，结果 ended up losing his girlfriend and his show was cancelled."
  },
  {
   "q": "All the tickets had been ____ out by the time we got to the cinema.",
   "opts": ["sold", "bought", "put", "worked"],
   "ans": 0,
   "exp": "sell out 卖光：票“被卖光”用被动语态 had been sold out。课文2b里超市的意大利面 all had been sold out（被抢购一空）。bought out 意为“买断”，put out 扑灭、work out 算出，均不合语境。"
  },
  {
   "q": "My friend invited me to a ____ party on April Fool's Day, but it was just a joke.",
   "opts": ["costume", "custom", "customer", "cost"],
   "ans": 0,
   "exp": "costume party 化妆舞会（costume 戏装、化妆服）。custom 风俗习惯、customer 顾客、cost 花费／成本——形近词辨析，注意别混淆。"
  },
  {
   "q": "I ____ up at 10:00 a.m. and realized that my alarm had never gone off.",
   "opts": ["woke", "waked", "woken", "wakes"],
   "ans": 0,
   "exp": "wake up 醒来，过去式是 woke（waked 不规范）；woken 是过去分词，须与 have / had 连用（如 had woken up）。课文3a原句：I woke up at 10:00 a.m. on February 21, 2011 and realized that my alarm had never gone off."
  },
  {
   "q": "By the time I walked into the classroom, the teacher ____ teaching.",
   "opts": ["has started", "had started", "will start", "is starting"],
   "ans": 1,
   "exp": "老师“先”开始上课（先发生的动作，用过去完成时 had started），我“后”走进教室（从句 walked，一般过去时）。has / will / is 均与过去语境 by the time I walked into 不符。"
  }
 ],
 "flashcards": [
  {
   "q": "By the time I got up, my brother had already gotten in the shower.",
   "a": "到我起床时，哥哥已经进淋浴间洗澡了。拆解：从句 got up（我起床，过去时间点，用一般过去时）；主句 had already gotten in the shower（哥哥洗澡在我起床之前已完成——过去的过去，用过去完成时）。get 的过去分词：美式 gotten，英式 got。"
  },
  {
   "q": "go off · 闹钟响（didn't go off）",
   "a": "go off （闹钟）响：My alarm didn't go off this morning.（今天早上我的闹钟没响。）注意 didn't 后接动词原形 go off，不能写 didn't went off。同义说法：The alarm clock rang. ring 的过去式是 rang，过去分词是 rung。"
  },
  {
   "q": "时态搭配：by the time / when / before + 过去完成时",
   "a": "从句（by the time / when / before + 一般过去时）给出过去的参照点，主句用过去完成时 had done，表示主句动作先发生。By the time I got outside, the bus had already left.（我到外面时，公交已开走。）When I got to school, I realized I had left my backpack at home.（到校才知书包落在家里。）"
  },
  {
   "q": "起床四连：wake up / get up / get dressed / put on",
   "a": "wake up 醒来（woke up）→ get up 起床（got up）→ get dressed 穿好衣服（get dressed 中 dressed 是形容词）→ put on 穿上（衣服）。课文句：I jumped out of bed and went straight to the airport.（我跳下床直奔机场。）"
  },
  {
   "q": "Life is full of the unexpected.",
   "a": "生活中充满了意外。be full of 充满 = be filled with（介词不同：full 接 of，filled 接 with）。unexpected 是形容词“出乎意料的”，the unexpected 指“意外之事”。"
  },
  {
   "q": "We stared in disbelief at the black smoke rising above the burning building.",
   "a": "我们难以置信地凝视着燃烧的大楼上空升起的黑烟。stare at 凝视，at 不能丢；in disbelief 难以置信地（dis- 否定前缀 + belief 相信）；above 在……上方；burning 燃烧着的（现在分词作定语）；I felt lucky to be alive.（我庆幸自己还活着，alive 是表语形容词。）"
  },
  {
   "q": "take off · 起飞；go straight to · 直奔；turn into · 变成",
   "a": "I went straight to the airport, but by the time I got there, my plane had already taken off.（我直奔机场，可赶到时飞机已经起飞了。）take off 起飞（过去分词 taken off）。My bad luck had unexpectedly turned into a good thing.（我的倒霉竟意外变成好事。）"
  },
  {
   "q": "show up 与 costume party（愚人节课文）",
   "a": "show up 出现、露面：He said he would come, but he never showed up.（他说会来，却始终没露面。）costume party 化妆舞会（costume 戏装）；fool 傻瓜／愚弄人——April Fool's Day 愚人节（4月1日），那天小心被整！"
  },
  {
   "q": "end up doing sth · 最终（落得）",
   "a": "end up doing sth 最终做某事，后接 doing，不接 to do。课文2b：He ended up losing his girlfriend and his show was cancelled.（他最终失去了女友，节目也被砍掉了。）类似结构还有 finish / practice 等后接 doing。"
  },
  {
   "q": "sell out / oversleep / embarrassed 等高频词一卡记",
   "a": "sell out 卖光：All the tickets were sold out.（票全卖光了。）oversleep 睡过头（过去式 overslept）。embarrassed 感到尴尬的：He felt embarrassed.（他感到很尴尬。）alive 活着的（表语形容词）；market 市场；cream 奶油；pie 馅饼；bean 豆子；worker 工人；officer 军官／警官；lady 女士；till = until 直到。"
  }
 ],
 "errors": [
  {
   "title": "主句漏掉 had，丢了“过去的过去”",
   "wrong": "把句子写成 By the time I got up, my brother already got in the shower. 或 When I got to school, I realized I left my backpack at home.（两个动作都用一般过去时）",
   "right": "哥哥洗澡、落书包都发生在后面的过去动作之前——过去的过去，先发生的动作必须用 had + 过去分词：my brother had already gotten in the shower；I realized I had left my backpack at home. 口诀：动作在先，had 在前。"
  },
  {
   "title": "by the time 从句误用过去完成时",
   "wrong": "写成 By the time I had got to the airport, my plane had already taken off.（从句也用了过去完成时）",
   "right": "by the time / when / before 引导的从句只提供过去的参照时间点，用一般过去时：By the time I got to the airport, my plane had already taken off. 只有主句（先发生的动作）才用过去完成时。"
  },
  {
   "title": "didn't 后误用过去式，go off 误写成 go on",
   "wrong": "写成 My alarm didn't went off this morning. 或 My alarm didn't go on this morning, so I woke up late.",
   "right": "didn't 后用动词原形：My alarm didn't go off.（我的闹钟没响。）go off 表示“（闹钟）响”，go on 是“继续”，不能混用。闹钟响了可说 The alarm went off. 或 The alarm rang."
  },
  {
   "title": "be full of 与 be filled with 介词互换",
   "wrong": "写成 The room was full with people. 或 The room was filled of people.",
   "right": "be full of 接 of；be filled with 接 with，不可互换：The room was full of people. = The room was filled with people. 同理只说 Life is full of the unexpected.，不说 full with the unexpected。"
  },
  {
   "title": "wake / oversleep 的不规则过去式误加 -ed",
   "wrong": "写成 I waked up at 10:00 a.m. 或 I oversleeped and was late for school.",
   "right": "不规则动词不能加 -ed：wake → woke（过去式）／ woken（过去分词）：I woke up at 10:00 a.m.; oversleep → overslept：I overslept and was late for school.（我睡过头，上学迟到了。）"
  },
  {
   "title": "stare in disbelief 后漏介词 at；show up 误作 show off",
   "wrong": "写成 We stared in disbelief the black smoke. 或 He said he would come, but he didn't show off.",
   "right": "stare at sth 凝视某物：We stared in disbelief at the black smoke.（in disbelief 是方式状语，介词 at 不能丢。）show up 出现、露面；show off 炫耀——答应来却没来是 never showed up。"
  }
 ]
}

out = "/home/administrator/xuci-jiancha/_lql9_data/english9_u12.json"
os.makedirs(os.path.dirname(out), exist_ok=True)
with open(out, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=1)

# 校验：json.load 读回并核对数量与结构
with open(out, encoding="utf-8") as f:
    loaded = json.load(f)

assert list(loaded.keys()) == ["hero_title", "meta_desc", "knowledge", "questions", "flashcards", "errors"]
assert loaded["hero_title"] == data["hero_title"]
for item in loaded["questions"]:
    assert set(item.keys()) == {"q", "opts", "ans", "exp"} and len(item["opts"]) == 4 and 0 <= item["ans"] <= 3
for item in loaded["knowledge"]:
    assert set(item.keys()) == {"t", "d"}
for item in loaded["flashcards"]:
    assert set(item.keys()) == {"q", "a"}
for item in loaded["errors"]:
    assert set(item.keys()) == {"title", "wrong", "right"}

print("file:", out)
print("counts: knowledge=%d, questions=%d, flashcards=%d, errors=%d" % (
    len(loaded["knowledge"]), len(loaded["questions"]), len(loaded["flashcards"]), len(loaded["errors"])))
print("json.dump + json.load OK")
