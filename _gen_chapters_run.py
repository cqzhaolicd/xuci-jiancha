# -*- coding: utf-8 -*-
"""生成全部 Python 章节互动页 + 注册到 zhaoli_index (Part 2: 执行)"""
import io, sys, json, subprocess, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 加载 build_page 独立模块
ns = {'json': json, 're': re}
exec(open('/home/administrator/xuci-jiancha/_build_page_module.py', encoding='utf-8').read(), ns)
build_page = ns['build_page']

# 加载章节数据(从 CHAPTERS 定义开始, 跳过文件头的 stdout 包装)
cd_ns = {}
src = open('/home/administrator/xuci-jiancha/_gen_chapters_data.py', encoding='utf-8').read()
data_src = src[src.index('# ============ 章节内容数据'):src.index('# 汇总:')]
exec(data_src, cd_ns)
CHAPTERS = cd_ns['CHAPTERS']

# 生成所有章节页
for ch in CHAPTERS:
    n = build_page(ch['fname'], ch['title'], ch['subtitle'], ch['key'],
                   ch['knowledge'], ch['questions'], ch['flashcards'], ch['errors'], color=ch['color'])
    print(f"{ch['fname']}: {n} 字节 ({len(ch['knowledge'])}卡 {len(ch['questions'])}题 {len(ch['flashcards'])}牌 {len(ch['errors'])}错)")

# JS 验证
all_ok = True
for ch in CHAPTERS:
    f = ch['fname']
    r = subprocess.run(["node", "-e", f"""
const fs=require('fs');const html=fs.readFileSync('{f}','utf8');
const re=/<script[^>]*>([\\s\\S]*?)<\\/script>/g;let m,ok=true;
while((m=re.exec(html))){{try{{new Function(m[1])}}catch(e){{ok=false;console.log('ERR:',e.message)}}}}
console.log(ok?'OK':'FAIL');
"""], capture_output=True, text=True)
    out = r.stdout.strip()
    if out != 'OK':
        all_ok = False
        print(f"{f}: {out} {r.stderr[:200]}")

print("\n=== 全部章节页生成完成 ===" + (" JS全OK" if all_ok else " 有JS错误!"))
