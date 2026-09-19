#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""补传新图片到群晖（scp -O）"""
import pexpect, os, sys

PASS = 'Zl150601'
HOST = 'hermes@192.168.3.190'
REPO = '/home/administrator/xuci-jiancha'
FILES = ['uploads/wrong_bank/physics_20260919_p2.jpg', 'uploads/wrong_bank/physics_20260919_p3.jpg']

for f in FILES:
    # 确保远端目录存在
    c = pexpect.spawn(f'ssh -o StrictHostKeyChecking=no {HOST} "mkdir -p /volume1/web/xuci-jiancha/uploads/wrong_bank && ls -d /volume1/web/xuci-jiancha/uploads/wrong_bank"',
                      timeout=60, encoding='utf-8')
    i = c.expect(['[Pp]assword:', pexpect.EOF, pexpect.TIMEOUT])
    if i == 0:
        c.sendline(PASS)
    c.expect([pexpect.EOF, pexpect.TIMEOUT], timeout=60)
    out = (c.before or '').strip()
    print('远端目录:', out.splitlines()[-1] if out else '(无输出)')

    c = pexpect.spawn(f'scp -O -o StrictHostKeyChecking=no {os.path.join(REPO, f)} {HOST}:/volume1/web/xuci-jiancha/{f}',
                      timeout=180, encoding='utf-8')
    i = c.expect(['[Pp]assword:', pexpect.EOF, pexpect.TIMEOUT])
    if i == 0:
        c.sendline(PASS)
    c.expect([pexpect.EOF, pexpect.TIMEOUT], timeout=180)
    print('scp:', f, '完成')
