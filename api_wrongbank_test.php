<?php
// 【测试版专用接口 · 按账号隔离版】每个登录账号各存一份数据，互不相通。
//   数据文件：__DIR__/wrong_bank_test_data/u_<slot>.json   （slot = sha256(user|SYNC_TOKEN) 前 24 位）
//   账号对照：__DIR__/wrong_bank_test_data/meta.json       （slot -> 账号，仅用于排查，不含错题内容）
//   滚动备份：__DIR__/wrong_bank_test_data/backups/u_<slot>_<时间>.json（每账号保留 10 份）
// 与正式库 api_wrongbank.php 完全隔离（正式版仍走原接口）。
//
// 请求头/参数：
//   X-Sync-Token 或 ?token=   共用同步令牌（防止误写/误读）
//   X-Sync-User  或 ?user=    登录账号（手机号）——决定读写哪一份数据
//   ?action=load              读该账号数据
//   ?action=save  (JSON body) 覆盖保存该账号数据
//   ?action=ping              健康检查
declare(strict_types=1);

const SYNC_TOKEN   = 'xuji-sync-2026';
const DATA_DIR     = __DIR__ . '/wrong_bank_test_data';
const LEGACY_FILE  = __DIR__ . '/wrong_bank_data_test.json';   // 改造前的共用文件（保留不动，作为历史备份）

header('Content-Type: application/json; charset=utf-8');
header('Cache-Control: no-store');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Headers: Content-Type, X-Sync-Token, X-Sync-User');
header('Access-Control-Allow-Methods: GET, POST, OPTIONS');
if (($_SERVER['REQUEST_METHOD'] ?? 'GET') === 'OPTIONS') {
    http_response_code(204);
    exit;
}

function out(array $a, int $code = 200): void {
    http_response_code($code);
    echo json_encode($a, JSON_UNESCAPED_UNICODE);
    exit;
}

function slot_of(string $user): string {
    return substr(hash('sha256', $user . '|' . SYNC_TOKEN), 0, 24);
}

function data_file(string $slot): string {
    return DATA_DIR . '/u_' . $slot . '.json';
}

function backup_dir(string $slot): string {
    return DATA_DIR . '/backups/u_' . $slot;
}

$action = $_GET['action'] ?? 'load';

$token = $_SERVER['HTTP_X_SYNC_TOKEN'] ?? ($_GET['token'] ?? '');
if (!hash_equals(SYNC_TOKEN, (string)$token)) {
    out(['ok' => false, 'error' => 'token 不正确'], 403);
}

if ($action === 'ping') {
    out(['ok' => true, 'pong' => true, 'php' => PHP_VERSION, 'per_user' => true,
         'data_dir' => is_dir(DATA_DIR), 'legacy_exists' => is_file(LEGACY_FILE)]);
}

// 账号：决定读写哪一份数据
$user = trim((string)($_SERVER['HTTP_X_SYNC_USER'] ?? ($_GET['user'] ?? '')));
if ($user === '') {
    out(['ok' => false, 'error' => '未登录：缺少账号，已退回本机模式'], 403);
}
if (!preg_match('/^[A-Za-z0-9_@.+\-]{3,64}$/', $user)) {
    out(['ok' => false, 'error' => '账号格式不合法'], 400);
}
$slot = slot_of($user);
$file = data_file($slot);

if ($action === 'whoami') {
    out(['ok' => true, 'user' => $user, 'slot' => $slot,
         'has_data' => is_file($file), 'updated_at' => is_file($file) ? date('c', filemtime($file)) : null]);
}

if ($action === 'load') {
    if (!is_file($file)) {
        out(['ok' => true, 'data' => null, 'updated_at' => null, 'empty' => true, 'user' => $user]);
    }
    $raw = file_get_contents($file);
    $decoded = json_decode((string)$raw, true);
    if ($decoded === null) {
        out(['ok' => false, 'error' => '服务端数据文件损坏'], 500);
    }
    out([
        'ok'         => true,
        'user'       => $user,
        'data'       => $decoded,
        'updated_at' => date('c', filemtime($file)),
        'size'       => strlen((string)$raw),
    ]);
}

if ($action === 'save') {
    $body = file_get_contents('php://input');
    if ($body === false || strlen($body) < 10) {
        out(['ok' => false, 'error' => '请求体为空'], 400);
    }
    if (strlen($body) > 8 * 1024 * 1024) {
        out(['ok' => false, 'error' => '数据过大(>8MB)'], 413);
    }
    $decoded = json_decode($body, true);
    if ($decoded === null) {
        out(['ok' => false, 'error' => 'JSON 格式错误'], 400);
    }
    if (!isset($decoded['questions']) || !is_array($decoded['questions'])) {
        out(['ok' => false, 'error' => '数据结构不合法(缺 questions)'], 400);
    }

    if (!is_dir(DATA_DIR) && !@mkdir(DATA_DIR, 0755, true)) {
        out(['ok' => false, 'error' => '无法创建数据目录，请检查权限'], 500);
    }

    // 保存前滚动备份（每个账号保留最近 10 份）
    if (is_file($file)) {
        $bd = backup_dir($slot);
        @mkdir($bd, 0755, true);
        @copy($file, $bd . '/u_' . $slot . '_' . date('Ymd_His') . '.json');
        $olds = glob($bd . '/*.json') ?: [];
        if (count($olds) > 10) {
            sort($olds);
            foreach (array_slice($olds, 0, count($olds) - 10) as $f) { @unlink($f); }
        }
    }

    $tmp = $file . '.tmp';
    $pretty = json_encode($decoded, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT);
    if ($pretty === false || file_put_contents($tmp, $pretty) === false) {
        out(['ok' => false, 'error' => '写入失败，请检查目录权限'], 500);
    }
    if (!rename($tmp, $file)) {
        @unlink($tmp);
        out(['ok' => false, 'error' => '重命名失败'], 500);
    }

    // 账号对照表（只记 slot→账号，便于排查“数据在哪个文件”）
    $metaFile = DATA_DIR . '/meta.json';
    $meta = is_file($metaFile) ? (json_decode((string)file_get_contents($metaFile), true) ?: []) : [];
    $meta[$slot] = ['user' => $user, 'questions' => count($decoded['questions']), 'updated_at' => date('c')];
    @file_put_contents($metaFile, json_encode($meta, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT));

    out([
        'ok'         => true,
        'user'       => $user,
        'slot'       => $slot,
        'updated_at' => date('c'),
        'questions'  => count($decoded['questions']),
        'size'       => strlen($pretty),
    ]);
}

out(['ok' => false, 'error' => '未知的 action'], 400);
