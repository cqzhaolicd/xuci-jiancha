# -*- coding: utf-8 -*-
"""Build interactive content JSON for 人教九全 Unit 14 (english9_u14.json)."""
import json, os

DATA = {
    "hero_title": "Unit 14 · I remember meeting all of you in Grade 7.",
    "meta_desc": "人教九全 · Unit 14",
    "knowledge": [
        {
            "t": "单元话题 · 毕业回忆与展望",
            "d": "本单元话题是“回忆初中三年 + 展望未来”。Section A 用 I remember doing… 回忆初中生活片段：winning a prize 获奖、doing a school survey 做调查、scoring two goals in a row 连进两球；Section B 是一篇毕业典礼致辞（graduation ceremony speech）：致辞者先感谢到场的师生家长，再祝贺全体毕业生，叮嘱大家记住帮助过自己的人、对自己的决定和行为负责，然后带着新的旅程出发。学完本单元，你会用英语回顾成长、感谢师友、畅谈毕业后的打算。"
        },
        {
            "t": "核心语法 · remember/forget doing 与 to do（重点）",
            "d": "remember/forget + doing 表示“记得/忘记（曾）做过某事”，动作已发生：I remember meeting all of you in Grade 7.（我记得七年级时与你们大家初次见面——已经见过）。remember/forget + to do 表示“记得/忘记要去做某事”，动作尚未发生：I remember to close the door.（我记得要关门——门还没关）；I forgot to bring my homework.（我忘了带作业——没带来）。记忆口诀：doing 已做，to do 将做。否定式 I'll never forget doing sth. 意为“永远不会忘记曾做过……”。"
        },
        {
            "t": "同类结构 · stop / try 的 doing 与 to do",
            "d": "和 remember 结构相似的还有 stop、try，初中重点两组辨析：stop doing sth. 停止做（正在做的事）↔ stop to do sth. 停下来去做（另一件事），如 Stop talking, please.（请别讲话了）He stopped to have a rest.（他停下来去休息）；try doing sth. 尝试做 ↔ try to do sth. 尽力做，如 Why not try doing it in another way?（何不换个方法试试？）Try to finish it on time.（尽量按时完成）。判断标准与 remember 相同：看动作是已做过还是将要去做。"
        },
        {
            "t": "毕业短语（一）· graduate from / set out / look back at",
            "d": "graduate from + 学校，意为“从……毕业”（graduate 也可作名词“毕业生”；graduation ceremony 毕业典礼）：We will graduate from junior high school in June. set out 出发、启程，开始新的征程，课文原句 As you set out on your new journey…（当你们踏上新的旅程时）；set off 也表示“出发”，如 set off for the airport 动身去机场。look back at 回首、回顾：When I look back at my junior high school days, I feel warm.（回首初中时光，我心里很暖）。"
        },
        {
            "t": "毕业短语（二）· 感谢、祝贺与负责",
            "d": "be thankful to sb. for sth. 因某事感激某人（to 接人、for 接事）：Never fail to be thankful to the people around you.（永远不要忘记感激身边的人）。be responsible for 对……负责：Choose wisely and be responsible for your decisions and actions.（做明智的选择，对自己的决定和行动负责）。congratulate sb. on sth. 就某事祝贺某人：I'd like to congratulate all the students who are here today.（我要祝贺今天在场的所有同学）。be thirsty for 渴求：You were thirsty for knowledge.（你们渴望知识）；be proud of 为……而骄傲：I'm so proud of you."
        },
        {
            "t": "高频短语补遗 · first of all / ahead of / separate from / in a row",
            "d": "first of all 首先（用于列举开头）；ahead of 在……前面（时间上）、等待着，如 many difficult tasks ahead of you 摆在你们面前的许多难题（区分 in front of：只表空间位置“在……前面”，如 stand in front of the blackboard）；separate from 与……分离：It is always hard to separate from good friends.（与好朋友分离总是很难）；in a row 连续地：score two goals in a row 连进两球；keep one's cool 保持冷静；make a mess 弄得一团糟；none of us 我们中没有一个。"
        },
        {
            "t": "综合复习 · used to do（过去常常）",
            "d": "used to do sth. 表示“过去常常做某事 / 曾经是……”，暗示现在已不这样，只用于过去时间：I used to be a really shy person.（我过去很害羞——现在不害羞了）。务必区分三个形近结构：① used to do 过去常常（to 后原形）；② be/get used to doing sth. 习惯于做某事（to 是介词，后接动名词）：I'm used to getting up early.；③ be used to do sth. 被用来做某事（被动语态）：Wood is used to make paper. 否定与疑问常借助 didn't：He didn't use to live here. / Did you use to play the piano?"
        },
        {
            "t": "综合复习 · 被动语态（be + 过去分词）",
            "d": "被动语态结构是 be + 及物动词的过去分词，be 随主语人称数和时态变化：一般现在时 is/am/are done（The classroom is cleaned every day.）；一般过去时 was/were done（The prize was given by our head teacher.）；一般将来时 will be done（The graduation ceremony will be held next Friday. 毕业典礼将于下周五举行）；含情态动词 must/can/should + be done（The task must be finished today.）。由主动变被动时，把主动句的宾语变成主语，谓语动词改为“be + 过去分词”，原主语常由 by 引出。"
        },
        {
            "t": "综合复习 · 定语从句（that / who / which / whom）",
            "d": "定语从句放在名词（先行词）之后起修饰作用，关系词由先行词和从句成分共同决定：指人用 who/whom/that，指物用 which/that；关系词在从句中作主语时不能省略，作宾语时可省略。例：The teachers who helped us most are standing on the stage.（帮助过我们最多的老师们正站在台上——先行词 teachers 指人，who 在从句中作主语）；the people who helped and supported you；those whom you have spent so much time with（those 指人，whom 作介词 with 的宾语）。中考常见考点是“指人作主语用 who（或 that），不能误用 which/whom”。"
        },
        {
            "t": "词汇小贴士 · 本单元重点词",
            "d": "survey 调查；standard 标准；keyboard 键盘；method 方法；instruction 指示、说明；double 两倍的；shall 将要（多用于第一人称，We shall never forget…）；overcome 克服（overcome difficulties 克服困难）；caring 体贴的、关心人的（a caring teacher）；senior 级别高的（senior high school 高中）；level 水平、级别（reach a higher level）；text 课文、文本；task 任务；wing 翅膀（Knowledge gives us wings to fly. 知识给我们飞翔的翅膀）。派生记忆：graduate→graduation；thank→thankful；care→caring/careful；act→action；decide→decision；responsible→responsibility。"
        }
    ],
    "questions": [
        {
            "q": "Remember ____ the lights when you leave the classroom, please.",
            "opts": ["to turn off", "turning off", "turned off", "turn off"],
            "ans": 0,
            "exp": "remember to do sth. 记得要去做某事，动作尚未发生。离开教室时灯还没关，所以用 to turn off，句意“请记得要关灯”。若说 remember turning off the lights，则表示“记得（曾）关过灯”，不符合“离开前去做”的语境。"
        },
        {
            "q": "I remember ____ you at the school art festival last year. You sang an English song.",
            "opts": ["meeting", "to meet", "meet", "met"],
            "ans": 0,
            "exp": "去年艺术节见面是已经发生的事，remember doing sth. 表示记得（曾）做过某事：I remember meeting you…（我记得见过你）。remember to meet 是“记得要去见面（尚未发生）”，与 last year 的语境矛盾。"
        },
        {
            "q": "Don't forget ____ your homework to school tomorrow.",
            "opts": ["to bring", "bringing", "brought", "bring"],
            "ans": 0,
            "exp": "forget to do sth. 忘记要去做（还没做）。作业是明天要带的，动作尚未发生，用 to bring。forget doing sth. 表示忘记（曾）做过某事，如 I forgot locking the door.（我忘了锁过门——其实锁了），意思完全不同。"
        },
        {
            "q": "I'll never forget ____ two goals in a row in the soccer competition.",
            "opts": ["scoring", "to score", "scored", "score"],
            "ans": 0,
            "exp": "进球已发生在过去且令人难忘，否定句 I'll never forget doing sth. 意为“永远不会忘记（曾）做过某事”，用 scoring。in a row 意为“连续地”。forget to do 表示“忘记要去做”，与“难忘的回忆”语境不符。"
        },
        {
            "q": "After three years of hard work, we will ____ from No. 3 Junior High School next month.",
            "opts": ["graduate", "graduation", "graduated", "graduating"],
            "ans": 0,
            "exp": "空格在 will 之后，需要动词原形；graduate from + 学校，意为“从……毕业”。graduation 是名词（毕业；毕业典礼），graduated / graduating 不能与 will 直接构成将来时。"
        },
        {
            "q": "You are old enough to be responsible ____ your own decisions and actions.",
            "opts": ["for", "of", "with", "to"],
            "ans": 0,
            "exp": "be responsible for sth. 对……负责，固定搭配，介词用 for。课文原句：Choose wisely and be responsible for your decisions and actions.（做明智的选择，对自己的决定和行动负责。）"
        },
        {
            "q": "I am thankful ____ my teachers ____ everything they have done for me.",
            "opts": ["to; for", "for; to", "to; with", "with; for"],
            "ans": 0,
            "exp": "be thankful to sb. for sth. 因某事感激某人：to 后接“人”（thankful to my teachers），for 后接“事”（for everything they have done for me）。其余介词组合都不能表达此搭配。"
        },
        {
            "q": "We all look forward to ____ the new school in senior high.",
            "opts": ["entering", "enter", "entered", "enters"],
            "ans": 0,
            "exp": "look forward to 中的 to 是介词，后面接名词或动名词，即 look forward to doing sth. 盼望做某事。enter the new school 意为“进入新学校”，此处须用动名词 entering，不能用动词原形 enter。"
        },
        {
            "q": "It is hard to leave, but we are still excited to set ____ on a new journey.",
            "opts": ["out", "up", "back", "down"],
            "ans": 0,
            "exp": "set out 出发、启程；set out on a new journey 踏上新的旅程，课文原句 As you set out on your new journey, you shouldn't forget where you came from. set up 建立，set back 使倒退，set down 放下，均不能与 on a new journey 搭配。"
        },
        {
            "q": "The head teacher congratulated every student ____ finishing junior high school.",
            "opts": ["on", "with", "at", "about"],
            "ans": 0,
            "exp": "congratulate sb. on sth. / doing sth. 就某事祝贺某人，介词用 on。课文原句：First of all, I'd like to congratulate all the students who are here today. congratulate 不与 with / at / about 搭配。"
        },
        {
            "q": "My father used to ____ in a small village before he moved to this city.",
            "opts": ["live", "living", "lived", "lives"],
            "ans": 0,
            "exp": "used to do sth. 过去常常做（现在不再），used to 后接动词原形，故用 live：他搬到这座城市之前曾住在小村庄。若表示“习惯于做”才是 be used to doing（后接动名词）；lived / lives 不能直接放在 used to 之后。"
        },
        {
            "q": "The graduation ceremony ____ in the school hall next Friday afternoon.",
            "opts": ["will be held", "is held", "was held", "will hold"],
            "ans": 0,
            "exp": "ceremony（典礼）与 hold（举行）是被动关系，且时间状语 next Friday 表示将来，故用一般将来时的被动语态 will be held（将被举行）。is held 表示经常发生的动作，was held 是一般过去时，均与 next Friday 矛盾；will hold 缺少被动形式。"
        },
        {
            "q": "The teachers ____ helped us most are standing on the stage now.",
            "opts": ["who", "whom", "which", "what"],
            "ans": 0,
            "exp": "先行词 teachers 指人，从句 helped 缺少主语，须用主格关系代词 who（或 that）作主语。whom 是宾格，只能作宾语，不能作从句主语；which 指物；what 不能引导定语从句。"
        },
        {
            "q": "In Grade 7 you were all full of energy and thirsty ____ knowledge.",
            "opts": ["for", "about", "of", "to"],
            "ans": 0,
            "exp": "be thirsty for sth. 渴求某物，固定搭配。课文原句：You were all so full of energy and thirsty for knowledge.（你们都充满活力、渴望知识。）thirsty 不与 about / of / to 构成此搭配。"
        },
        {
            "q": "When I ____ at my three years of junior high school, I feel warm and thankful.",
            "opts": ["look back", "look up", "look after", "look over"],
            "ans": 0,
            "exp": "look back at sth. 回首、回顾：When I look back at my junior high school days…（当我回首初中时光……）。look up 抬头看 / 查阅，look after 照顾，look over 检查，均不符合“回忆三年时光”的语境。"
        },
        {
            "q": "There are many difficult tasks ____ us in senior high, but we will never give up.",
            "opts": ["ahead of", "in front of", "instead of", "because of"],
            "ans": 0,
            "exp": "ahead of 此处表示“（时间上）在前面、等待着”：many difficult tasks ahead of us 摆在我们面前的许多难题，课文原句 you have many difficult tasks ahead of you。in front of 只表空间“在……前面”；instead of 代替；because of 因为，均不合语境。"
        }
    ],
    "flashcards": [
        {
            "q": "I remember meeting all of you in Grade 7.（标题句拆解）",
            "a": "结构：I + remember + 动名词短语 meeting all of you in Grade 7。remember doing sth. 记得（曾）做过某事——meeting 指“与大家见面”这件事已在七年级发生过。全句：我记得七年级时与你们大家初次见面。"
        },
        {
            "q": "remember / forget 后用 doing 还是 to do？",
            "a": "看动作发生了没有：已发生用 doing——I remember closing the door.（我记得关过门）；尚未发生用 to do——I remember to close the door.（我记得要关门）。口诀：doing 已做，to do 将做。forget 用法相同：forgot to bring 忘了带（没带）≠ forgot bringing 忘了带过（带了）。"
        },
        {
            "q": "graduate 的用法与词性",
            "a": "动词（不及物）：graduate from + 学校，从……毕业——We will graduate from junior high school in June.（我们六月将从初中毕业）；名词：graduate 毕业生，graduation 毕业 / 毕业典礼（graduation ceremony）。注意：graduate 后要加 from 再接学校名。"
        },
        {
            "q": "Never fail to be thankful to the people around you.",
            "a": "永远不要忘记感激身边的人。be thankful to sb. for sth. 因某事感激某人（to 接人、for 接事）；fail to do sth. 未能 / 忘记做某事。同义表达：be grateful to sb. for sth."
        },
        {
            "q": "be responsible for 的用法（课文原句）",
            "a": "对……负责。Choose wisely and be responsible for your decisions and actions.（做出明智的选择，对自己的决定和行为负责。）介词固定用 for；名词形式 responsibility：take responsibility for 对……负责。"
        },
        {
            "q": "look forward to 后面接什么？",
            "a": "to 是介词，后接名词或动名词：look forward to meeting you / to new experiences in senior high。不能接动词原形，也不能说 will look forward to。常用进行时表“正盼望着”：I'm looking forward to hearing from you.（我盼望着你的来信。）"
        },
        {
            "q": "set out 与 set off 的区别与搭配",
            "a": "两者都可表示“出发、动身”。set out 常搭配 on a journey（踏上旅程）或 to do（着手做）：As you set out on your new journey…（当你们踏上新的旅程时）；set off 常搭配 for + 地点：They set off for Beijing early this morning. 与 journey / way 搭配时多用 set out on。"
        },
        {
            "q": "congratulate 的正确搭配",
            "a": "congratulate sb. on sth. / doing sth. 就某事祝贺某人：The teacher congratulated me on passing the exam.（老师祝贺我通过了考试。）课文原句：I'd like to congratulate all the students who are here today.（我要祝贺今天在场的所有同学。）注意介词用 on，congratulate 后必须直接接人。"
        },
        {
            "q": "used to do / be used to doing / be used to do（综合复习）",
            "a": "used to do：过去常常、曾经（现在不了），后接动词原形——I used to be a really shy person.（我过去很害羞）；be/get used to doing：习惯于做，to 是介词后接动名词——I'm used to getting up early.；be used to do：被用来做（被动语态）——Wood is used to make paper."
        },
        {
            "q": "It is always hard to separate from those whom you have spent so much time with.",
            "a": "与那些共度了那么多时光的人分离总是很难。separate from 与……分离；whom 引导定语从句修饰 those（指人），在从句中作 with 的宾语（也可写成 those with whom you have spent…）；spend time with sb. 与某人共度时光。"
        }
    ],
    "errors": [
        {
            "title": "remember doing 与 remember to do 混淆",
            "wrong": "把“请记得要关门”写成 Please remember closing the door.；把“我记得去年见过他”写成 I remember to meet him last year.",
            "right": "动作未发生、将要做，用 to do：Please remember to close the door.（记得要关门——门还没关）；动作已发生，用 doing：I remember meeting him last year.（我记得（曾）见过他）。判定法：这件事做了没有？做了 → doing；没做、将要做 → to do。"
        },
        {
            "title": "forget to do 与 forget doing 用反",
            "wrong": "想表达“今早忘了锁门（结果没锁）”，却写成 I forgot locking the door this morning.",
            "right": "应写 I forgot to lock the door this morning.（忘记要锁门 = 没锁）。而 I forgot locking the door. 的意思是“我忘了（曾）锁过门”——门其实锁了，只是忘了这回事。to do 表“忘做”，doing 表“忘了做过”。"
        },
        {
            "title": "look forward to 后误接动词原形",
            "wrong": "把句子写成 I look forward to see you again at the party. 或 She looks forward to enter senior high school.",
            "right": "look forward to 中的 to 是介词，后接名词或动名词：I'm looking forward to seeing you again.（我盼望着再见到你）；She looks forward to entering senior high school. 与它同型的“to 介词 + doing”还有 be used to、pay attention to 等，见到它们后一律不能直接加动词原形。"
        },
        {
            "title": "graduate 的介词与词性误用",
            "wrong": "把“明年从初中毕业”写成 We will graduate No. 3 Junior High School next year.；把“毕业后”写成 after graduate.",
            "right": "graduate 是不及物动词，须用 graduate from + 学校：We will graduate from No. 3 Junior High School next year. 名词形式：graduation（毕业；毕业典礼），graduate 也可作名词“毕业生”。“毕业后”说 after graduation 或 after we graduate，不能说 after graduate。"
        },
        {
            "title": "thankful / responsible / thirsty / congratulate 的介词张冠李戴",
            "wrong": "I'm thankful for my teachers with their help. / We should be responsible of our actions. / The students are thirsty to knowledge. / He congratulated me for my success.",
            "right": "四组固定搭配成对记牢：be thankful to sb. for sth.（to 接人，for 接事）；be responsible for sth.（对……负责）；be thirsty for sth.（渴求）；congratulate sb. on sth.（就某事祝贺某人）。介词一旦换错，整个搭配就错。"
        },
        {
            "title": "used to 与 be used to doing 混用",
            "wrong": "想表达“我过去很害羞”写成 I am used to being very shy.；想表达“我习惯早起”写成 I used to getting up early.",
            "right": "used to do 表示过去常常 / 曾经（现在不这样），后接动词原形：I used to be very shy.（我过去很害羞）；be/get used to doing 表示习惯于做，to 后接动名词：I'm used to getting up early.（我习惯早起）。判断：一看是否表“过去”且现已不再，二看 to 后是原形还是 doing。"
        }
    ]
}

out = "/home/administrator/xuci-jiancha/_lql9_data/english9_u14.json"
os.makedirs(os.path.dirname(out), exist_ok=True)

with open(out, "w", encoding="utf-8") as f:
    json.dump(DATA, f, ensure_ascii=False, indent=1)

# --- validation ---
with open(out, encoding="utf-8") as f:
    check = json.load(f)

assert check["hero_title"] == DATA["hero_title"]
assert set(check.keys()) == {"hero_title", "meta_desc", "knowledge", "questions", "flashcards", "errors"}
assert 8 <= len(check["knowledge"]) <= 10
assert 14 <= len(check["questions"]) <= 16
assert 8 <= len(check["flashcards"]) <= 10
assert 4 <= len(check["errors"]) <= 6
for q in check["questions"]:
    assert len(q["opts"]) == 4 and isinstance(q["ans"], int) and 0 <= q["ans"] <= 3
    assert len(set(q["opts"])) == 4, q["q"]
    assert q["q"] and q["exp"]
for k in check["knowledge"]:
    assert k["t"] and k["d"]
for fc in check["flashcards"]:
    assert fc["q"] and fc["a"]
for e in check["errors"]:
    assert e["title"] and e["wrong"] and e["right"]

print("VALIDATED OK ->", out)
print("counts: knowledge=%d questions=%d flashcards=%d errors=%d" % (
    len(check["knowledge"]), len(check["questions"]), len(check["flashcards"]), len(check["errors"])))
