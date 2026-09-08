# -*- coding: utf-8 -*-
"""人教九全英语 Unit 1 · How can we become good learners? 互动内容 JSON 生成器"""
import json, os, sys

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "english9_u1.json")

hero_title = "Unit 1 · How can we become good learners?"
meta_desc = "人教九全 · Unit 1"

# ---------- knowledge (t, d<=80) ----------
knowledge = [
    {"t": "单元主题",
     "d": "本单元围绕“如何学习”展开：用 by doing 表达方式，用 How 问方法，并谈论如何成为好的学习者。"},
    {"t": "语法 · by + v-ing",
     "d": "介词 by 后接动名词，表“通过……方式”，常用来回答 How 的提问。例：I learn English by reading aloud."},
    {"t": "句型 · How ...?",
     "d": "问“方式”用 How：How do you learn English? 答：I learn by studying with a group."},
    {"t": "patient 一词多义",
     "d": "patient 形容词“有耐心的”，be patient with sb. 对某人有耐心；也可作名词“病人”。名词“耐心”是 patience。"},
    {"t": "pronounce / pronunciation",
     "d": "pronounce 动词“发音”，pronunciation 名词“发音”。动词用于 How do you ...? 句型。"},
    {"t": "短语 pay attention to",
     "d": "pay attention to 意为“注意”，to 是介词，后接名词或动名词：pay attention to your pronunciation。"},
    {"t": "短语 connect ... with",
     "d": "把……和……联系起来。例：Connect what you learn with something interesting. 把所学与有趣的事物联系起来。"},
    {"t": "短语 be born with / fall in love with",
     "d": "be born with 天生具有；fall in love with 爱上、迷上（过去式 fell），后接人或物。"},
    {"t": "重点词汇",
     "d": "textbook 课本；conversation 交谈；expression 表达；grammar 语法；review 复习；repeat 重复。"},
    {"t": "提建议句型",
     "d": "How/What about + 动名词？……怎么样？Why not + 动词原形？……例：How about watching English movies?"},
]

# ---------- questions (q, opts[4], ans, exp) ----------
# exp 自动加前缀“答案 X。”，X 由 ans 计算，保证与选项顺序一致
_raw_q = [
    # ---- by + v-ing 语法（含必考句）----
    {"q": "我通过大声朗读来学习英语。I learn English by ______ (read) aloud.",
     "opts": ["reading", "to read", "read", "reads"], "ans": 0,
     "exp": "介词 by 后接动名词（v-ing），表“通过……的方式”，作方式状语。括号动词 read 需改为 reading。语法点：by + v-ing。句意：我通过大声朗读学英语。"},
    {"q": "——你是怎样学英语的？——我通过和小组一起学习来学。— How do you learn English? — I learn by ______ with a group.",
     "opts": ["to study", "studying", "studied", "studies"], "ans": 1,
     "exp": "问方式用疑问词 How；答语 by + v-ing 说明方式。by 是介词，后接动名词，study → studying。核心句型：How do you learn English? — I learn by studying with a group."},
    {"q": "——你是怎样提高听力的？——通过每天听英文歌曲。— ______ do you improve your listening? — By listening to English songs every day.",
     "opts": ["Why", "When", "How", "Where"], "ans": 2,
     "exp": "答语 By + v-ing 表“通过……方式”，对方式提问用 How（怎样）。Why 问原因，When 问时间，Where 问地点，均不合语境。"},
    {"q": "他通过制作单词卡来学新单词。He learns new words by ______ (make) word cards.",
     "opts": ["makes", "made", "to make", "making"], "ans": 3,
     "exp": "by 后接动名词作方式状语，make → making。by making word cards（制作单词卡）是课文列举的学习方法。动词原形 makes/made 均不可接在介词 by 后。"},
    {"q": "你可以通过向老师求助来提高英语。You can improve your English by ______ (ask) the teacher for help.",
     "opts": ["asking", "asked", "to ask", "asks"], "ans": 0,
     "exp": "ask sb. for help 意为“向某人求助”；介词 by 后接动名词，故用 asking。by asking the teacher for help 也是课本中的学习方法表达。"},
    # ---- patient / pronounce / pronunciation 等词汇 ----
    {"q": "要有耐心，汤姆！学一门语言需要时间。Be ______, Tom! Learning a language takes time.",
     "opts": ["patience", "patient", "patiently", "patients"], "ans": 1,
     "exp": "空格在 be 动词后作表语，需形容词。patient 形容词“有耐心的”，Be patient!＝耐心点！patience 是名词“耐心”，patiently 是副词，patients 是“病人们”，均不适用。be patient with sb. 对某人有耐心。"},
    {"q": "李医生对医院里的每位病人（病人）都很和善。Dr. Li is kind to every ______ in the hospital.",
     "opts": ["patience", "patients", "patient", "patiently"], "ans": 2,
     "exp": "every 后接可数名词单数。patient 作名词意为“病人”，此处用单数 patient。patience 意为“耐心”，词义不符；patients 是复数，不能用于 every 之后。"},
    {"q": "这个词你怎么发音？How do you ______ this word?",
     "opts": ["pronunciation", "pronouncing", "pronounces", "pronounce"], "ans": 3,
     "exp": "一般现在时疑问句 do you 后接动词原形。pronounce 是动词“发音”。句意：这个词你怎么发音？注意 pronunciation 是名词“发音”，不能放在 do 后。"},
    {"q": "你的英语发音非常好。Your ______ is really good.",
     "opts": ["pronunciation", "pronounce", "pronouncing", "pronounced"], "ans": 0,
     "exp": "your 是形容词性物主代词，后接名词。pronunciation 名词“发音”；pronounce 是动词。记法：pronounce v. 发音 / pronunciation n. 发音。"},
    {"q": "我听不懂这部电影里的那段对话。I can't understand the ______ in this movie.",
     "opts": ["expression", "conversation", "communication", "pronunciation"], "ans": 1,
     "exp": "题干“对话”对应 conversation（交谈；对话）。expression 是“表达；表情”，communication 是“交流”，pronunciation 是“发音”，词义均不符。"},
    {"q": "请把课本翻到第十页。Please open your ______ and turn to Page 10.",
     "opts": ["notebook", "handbook", "textbook", "dictionary"], "ans": 2,
     "exp": "textbook 名词“课本、教科书”，由 text（课文）+ book 构成，符合“课本”之意。notebook 笔记本，handbook 手册，dictionary 词典。"},
    {"q": "你应该明智地利用学习时间。You should use your study time ______.",
     "opts": ["wise", "wiser", "wisdom", "wisely"], "ans": 3,
     "exp": "修饰动词 use 需用副词，wisely 副词“明智地”，放在动词后作状语。wise 是形容词，wisdom 是名词“智慧”。课本句：use your time wisely。"},
    # ---- 短语：pay attention to / connect...with / fall in love with / be born with ----
    {"q": "课堂上请注意听老师讲课。Please pay ______ to the teacher in class.",
     "opts": ["attention", "attentive", "attentively", "attend"], "ans": 0,
     "exp": "固定短语 pay attention to“注意”，to 是介词。pay 后接名词 attention，后接对象用 to：pay attention to the teacher。attentive 是形容词，attend 是动词“参加”。"},
    {"q": "当你把新单词和图片联系起来时，你能记得更牢。When you ______ the new words with the pictures, you can remember them better.",
     "opts": ["complete", "connect", "compare", "share"], "ans": 1,
     "exp": "固定搭配 connect...with... 意为“把……和……联系起来”，由介词 with 对应“和……”。complete 完成、compare 比较、share 分享，词义均不符。"},
    {"q": "她第一次看这部电影时就爱上了它。She ______ in love with the movie the first time she saw it.",
     "opts": ["failed", "felt", "fell", "fallen"], "ans": 2,
     "exp": "固定短语 fall in love with“爱上”。由 saw 可知句子用一般过去时，fall 的过去式是不规则变化 fell。failed 失败、felt 感觉，与 in love with 不搭配。"},
    {"q": "每个人天生都有学习的能力。Everyone is born ______ the ability to learn.",
     "opts": ["for", "from", "as", "with"], "ans": 3,
     "exp": "固定搭配 be born with“天生具有”，with 表“带有、具有”。这是课本原句：Everyone is born with the ability to learn. 每个人天生都具备学习的能力。"},
]

questions = []
for it in _raw_q:
    letter = chr(65 + it["ans"])
    questions.append({"q": it["q"], "opts": it["opts"], "ans": it["ans"],
                      "exp": "答案 " + letter + "。" + it["exp"]})

# ---------- flashcards (q, a) ----------
flashcards = [
    {"q": "by + 动名词（by doing）怎么用？",
     "a": "介词 by 后接 v-ing，表“通过……的方式”，常回答 How 的提问。例：I learn English by reading aloud. 我通过大声朗读学英语。"},
    {"q": "怎样问、答“学习方法”？",
     "a": "问：How do you learn English?（你怎样学英语？）答：I learn by studying with a group.（我通过小组合作学习。）答语用 by + v-ing 说明方式。"},
    {"q": "patient 有哪些意思？",
     "a": "一词多义：形容词“有耐心的”，be patient with sb. 对某人有耐心；名词“病人”。名词“耐心”是 patience，别混淆。"},
    {"q": "pronounce 与 pronunciation 怎么区分？",
     "a": "pronounce 是动词“发音”，如 How do you pronounce this word?；pronunciation 是名词“发音”，如 Your pronunciation is good."},
    {"q": "pay attention to 怎么用？",
     "a": "固定短语“注意”，to 是介词，后接名词或动名词：pay attention to your pronunciation / to listening in class."},
    {"q": "connect...with 是什么意思？",
     "a": "把……和……联系起来。例：Connect what you learn with what you already know. 把所学与你已知的内容联系起来。"},
    {"q": "be born with 是什么意思？",
     "a": "天生具有。例：Everyone is born with the ability to learn. 每个人都天生具备学习能力。ability 是名词“能力”。"},
    {"q": "fall in love with 怎么用？",
     "a": "爱上、迷上某人/某物，后接宾语。例：I fell in love with this English song. 我迷上了这首英文歌。过去式 fell。"},
    {"q": "discover 和 create 有什么不同？",
     "a": "discover 发现（本来存在的事物），如 discover a good way to learn；create 创造（新事物），如 create an interest in learning."},
    {"q": "提建议有哪些句型？",
     "a": "How/What about + v-ing?（……怎么样？）Why not + 动词原形?（为什么不……？）例：How about keeping a diary in English?"},
]

# ---------- errors (title, wrong, right) ----------
errors = [
    {"title": "by 后接动词原形还是 v-ing？",
     "wrong": "把“I learn English by read aloud.”当成正确句子。",
     "right": "by 是介词，后接动名词：by reading aloud；同类还有 by working with friends / by making word cards。介词 by + v-ing 常用来回答 How 引导的提问，动词不能用原形。"},
    {"title": "patient 是“病人”还是“耐心的”？",
     "wrong": "把 patient 只记成“病人”，或把名词 patience 当形容词用：The teacher is patience with us.",
     "right": "patient 作形容词是“有耐心的”（be patient with sb. 对某人有耐心），作名词是“病人”；“耐心”的名词是 patience。正确句：The teacher is patient with us. 医生对病人也常用 patient 一词。"},
    {"title": "pronounce 与 pronunciation 混用",
     "wrong": "Your pronounce is very good.（把动词当名词用）",
     "right": "pronounce 是动词“发音”，pronunciation 是名词“发音”。正确句：Your pronunciation is very good. 问“这个词怎么读”用动词：How do you pronounce this word?"},
    {"title": "pay attention to 的介词写成 on",
     "wrong": "You should pay attention on your spelling. / pay attention your spelling",
     "right": "固定搭配是 pay attention to，介词用 to：Pay attention to your spelling. to 后接名词或动名词：pay attention to listening in class."},
    {"title": "fall in love with 的介词写成 of",
     "wrong": "She fell in love of the English song.",
     "right": "固定搭配 fall in love with sb./sth.“爱上、迷上……”，介词用 with；过去式是 fell。正确句：She fell in love with the English song."},
    {"title": "把 memory 当动词用（中式英语）",
     "wrong": "I memory new words by making word cards.",
     "right": "memory 是名词“记忆力”，不能作动词；记单词用 memorize 或 remember。正确句：I memorize new words by making word cards."},
]

# ---------- 组装 & 校验 ----------
data = {"hero_title": hero_title, "meta_desc": meta_desc,
        "knowledge": knowledge, "questions": questions,
        "flashcards": flashcards, "errors": errors}

for k in data["knowledge"]:
    if len(k["d"]) > 80:
        print("TOO LONG:", k["t"], len(k["d"]))
        print("   text:", k["d"])
for k in data["knowledge"]:
    assert len(k["d"]) <= 80, ("knowledge d 超长", k["t"], len(k["d"]))
assert 8 <= len(knowledge) <= 10 and 14 <= len(questions) <= 16
assert 8 <= len(flashcards) <= 10 and 4 <= len(errors) <= 6
for q in questions:
    assert len(q["opts"]) == 4 and 0 <= q["ans"] <= 3
    assert q["exp"].startswith("答案 " + chr(65 + q["ans"]) + "。"), q["q"]

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=1)

# 重新载入校验
d2 = json.load(open(OUT, encoding="utf-8"))
for k in d2["knowledge"]:
    assert len(k["d"]) <= 80
print("written:", OUT)
print("knowledge=%d questions=%d flashcards=%d errors=%d" % (
    len(d2["knowledge"]), len(d2["questions"]), len(d2["flashcards"]), len(d2["errors"])))
from collections import Counter
print("ans 分布:", dict(sorted(Counter(q["ans"] for q in d2["questions"]).items())))
