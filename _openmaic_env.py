#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""为 OpenMAIC 生成 .env.local（从 ~/.hermes/.env 取 DeepSeek key，不打印密钥）"""
import re, os

env_path = os.path.expanduser('~/.hermes/.env')
vals = {}
for line in open(env_path, encoding='utf-8', errors='ignore'):
    line = line.strip()
    if not line or line.startswith('#') or '=' not in line:
        continue
    k, v = line.split('=', 1)
    vals[k.strip()] = v.strip().strip('"').strip("'")

key = vals.get('DEEPSEEK_API_KEY', '')
base = vals.get('DEEPSEEK_BASE_URL', '') or 'https://api.deepseek.com'

out = os.path.expanduser('~/OpenMAIC/.env.local')
content = f"""# OpenMAIC 本地部署配置（自动生成）
# 模型：DeepSeek
DEEPSEEK_API_KEY={key}
DEEPSEEK_BASE_URL={base}
DEEPSEEK_MODELS=deepseek-v4-flash,deepseek-v4-pro

# 自托管：允许访问本机/内网模型服务（如需 Ollama 可打开）
# ALLOW_LOCAL_NETWORKS=true

# 访问码（留空 = 不设密码）
# ACCESS_CODE=
"""
open(out, 'w', encoding='utf-8').write(content)
print('.env.local 已写入，key 长度:', len(key), '| base:', base)
print('文件行数:', content.count('\n'))
