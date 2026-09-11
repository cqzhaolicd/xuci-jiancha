#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""部署 english26q_read1 相关文件到威联通(FTP) + 群晖(从威联通拉取) + 校验 md5"""
import os, sys, time, hashlib, ftplib, subprocess

REPO = '/home/administrator/xuci-jiancha'
FILES = ['index.html', 'english26q_read1_interactive.html']
QNAP_HOST, QNAP_USER, QNAP_PASS = '192.168.3.88', 'hermes', 'Zl150601'
SYN_HOST, SYN_USER, SYN_PASS = '192.168.3.190', 'hermes', 'Zl150601'
QNAP_DIR = '/Web/xuci-jiancha'
SYN_DIR = '/var/services/web/xuci-jiancha'


def md5(p):
    return hashlib.md5(open(p, 'rb').read()).hexdigest()


def ftp_upload(f):
    """ftp 路径必须落在 Web/ 下；重试直到 226"""
    local = os.path.join(REPO, f)
    for attempt in range(1, 5):
        try:
            ftp = ftplib.FTP(QNAP_HOST, timeout=60)
            ftp.login(QNAP_USER, QNAP_PASS)
            ftp.cwd(QNAP_DIR)
            with open(local, 'rb') as fh:
                ftp.storbinary(f'STOR {f}', fh)
            ftp.quit()
            print(f'  [QNAP] {f} 上传成功 (第{attempt}次)')
            return True
        except Exception as e:
            print(f'  [QNAP] {f} 第{attempt}次失败: {e}')
            time.sleep(3)
    return False


def syn_pull(f):
    """群晖从威联通 HTTP 拉取（威联通在线时首选）。
    ⚠️ 两条血泪规则（2026-09-11 实证）：
      ① 时间戳必须让【远端 shell】展开：URL 里写 ?t=`date +%s`（反引号）。
      ② 远端命令里【不要出现任何引号】——pexpect.spawn(字符串) 会先本地 shlex 拆词并剥掉引号，
         引号被剥后 `-H Cache-Control: no-cache` 会裂成多个参数（curl 把 no-cache 当第二个 URL，
         内容打到 stdout、-o 不生效 → 目标文件静默不更新）。同理 '$(date +%s)' 单引号方案会让
         curl 收到字面量报 curl: (3) Error。
    """
    import pexpect
    remote = (f'curl -sS -m 60 -o {SYN_DIR}/{f} http://192.168.3.88/xuci-jiancha/{f}?t=`date +%s`; '
              f'echo rc=$?; md5sum {SYN_DIR}/{f}')
    child = pexpect.spawn(f'ssh -o StrictHostKeyChecking=no {SYN_USER}@{SYN_HOST} "{remote}"',
                          timeout=150, encoding='utf-8', codec_errors='replace')
    if child.expect(['[Pp]assword', pexpect.EOF], timeout=30) == 0:
        child.sendline(SYN_PASS)
        child.expect(pexpect.EOF, timeout=150)
    out = (child.before or '')
    lines = [l for l in out.strip().splitlines() if l.strip()]
    return lines[-1] if lines else 'NO OUTPUT'


def http_md5(url):
    tmp = '/tmp/deploy_check.bin'
    subprocess.run(['curl', '-s', url, '-o', tmp], timeout=90)
    return md5(tmp) if os.path.exists(tmp) else 'ERR'


ok = True
print('== ① 威联通 FTP 上传 ==')
for f in FILES:
    if not ftp_upload(f):
        ok = False

print('== ② 群晖从威联通拉取 ==')
for f in FILES:
    print(f'  [SYN] {f}: {syn_pull(f)}')

print('== ③ 三方 md5 校验 ==')
for f in FILES:
    local = md5(os.path.join(REPO, f))
    qnap = http_md5(f'http://192.168.3.88/xuci-jiancha/{f}?t={int(time.time())}')
    syn = http_md5(f'http://192.168.3.190/xuci-jiancha/{f}?t={int(time.time())}')
    gh = http_md5(f'https://ghfast.top/https://raw.githubusercontent.com/cqzhaolicd/xuci-jiancha/main/{f}')
    match = (local == qnap == syn)
    print(f'  {f}\n    本地={local[:10]} 威联通={qnap[:10]} 群晖={syn[:10]} GitHub={gh[:10]}  {"✅ 一致" if match else "⚠️ 不一致"}')
    if not match:
        ok = False

print('全部一致 ✅' if ok else '⚠️ 存在不一致，需排查')
