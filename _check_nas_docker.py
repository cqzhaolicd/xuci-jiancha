#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""检测 NAS 的 Docker 与资源情况（用于 OpenMAIC 长期部署评估）"""
import pexpect, sys

PASS = 'Zl150601'
hosts = {'群晖 192.168.3.190': 'hermes@192.168.3.190', '威联通 192.168.3.88': 'hermes@192.168.3.88'}

for name, target in hosts.items():
    print(f'===== {name} =====')
    try:
        c = pexpect.spawn(f'ssh -o StrictHostKeyChecking=no -o ConnectTimeout=15 {target} '
                          f'"echo PW_OK; uname -m; cat /proc/meminfo | head -1; df -h / | tail -1; '
                          f'(docker --version || /usr/local/bin/docker --version || echo NO_DOCKER) 2>&1; '
                          f'(docker ps -a --format \'{{{{.Names}}}}\' | head -10) 2>&1"',
                          timeout=60, encoding='utf-8')
        i = c.expect(['[Pp]assword:', 'PW_OK', pexpect.EOF, pexpect.TIMEOUT])
        if i == 0:
            c.sendline(PASS)
        c.expect([pexpect.EOF, pexpect.TIMEOUT], timeout=45)
        print(c.before.strip()[:900])
    except Exception as e:
        print('失败:', e)
    print()
