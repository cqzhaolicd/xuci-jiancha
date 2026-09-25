<?php
// 错题本跨设备同步接口（部署在威联通 Web/xuci-jiancha/）
// GET  ?action=load               -> 返回全量数据
// POST ?action=save  (JSON body)  -> 覆盖保存
// 全部请求需带 token 参数（防止误写）
declare(strict_types=1);

const SYNC_TOKEN = 'xuji-sync-2026';
const DATA_FILE  = __DIR__ . '/wrong_bank_data.json';
const BACKUP_DIR = __DIR__ . '/wrong_bank_backups';

header('Content-Type: application/json; charset=utf-8');
header('Cache-Control: no-store');
// 允许跨源调用（群晖版页面 / 局域网其它地址），自定义头 X-Sync-Token 会触发预检
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Headers: Content-Type, X-Sync-Token');
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

$action = $_GET['action'] ?? 'load';
$token  = '';
if (isset($_SERVER['HTTP_X_SYNC_TOKEN'])) {
    $token = $_SERVER['HTTP_X_SYNC_TOKEN'];
} elseif (isset($_GET['token'])) {
    $token = (string)$_GET['token'];
}

if (!hash_equals(SYNC_TOKEN, $token)) {
    out(['ok' => false, 'error' => 'token 不正确'], 403);
}

if ($action === 'load') {
    if (!is_file(DATA_FILE)) {
        out(['ok' => true, 'data' => null, 'updated_at' => null, 'empty' => true]);
    }
    $raw = file_get_contents(DATA_FILE);
    $decoded = json_decode($raw, true);
    if ($decoded === null) {
        out(['ok' => false, 'error' => '服务端数据文件损坏'], 500);
    }
    out([
        'ok'         => true,
        'data'       => $decoded,
        'updated_at' => date('c', filemtime(DATA_FILE)),
        'size'       => strlen($raw),
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

    // 保存前对旧文件做滚动备份（保留最近 10 份）
    if (is_file(DATA_FILE)) {
        @mkdir(BACKUP_DIR, 0755, true);
        @copy(DATA_FILE, BACKUP_DIR . '/wrong_bank_data_' . date('Ymd_His') . '.json');
        $olds = glob(BACKUP_DIR . '/wrong_bank_data_*.json') ?: [];
        if (count($olds) > 10) {
            sort($olds);
            foreach (array_slice($olds, 0, count($olds) - 10) as $f) { @unlink($f); }
        }
    }

    $tmp = DATA_FILE . '.tmp';
    $pretty = json_encode($decoded, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT);
    if ($pretty === false || file_put_contents($tmp, $pretty) === false) {
        out(['ok' => false, 'error' => '写入失败，请检查目录权限'], 500);
    }
    if (!rename($tmp, DATA_FILE)) {
        @unlink($tmp);
        out(['ok' => false, 'error' => '重命名失败'], 500);
    }
    out([
        'ok'         => true,
        'updated_at' => date('c'),
        'questions'  => count($decoded['questions']),
        'size'       => strlen($pretty),
    ]);
}

if ($action === 'ping') {
    out(['ok' => true, 'pong' => true, 'php' => PHP_VERSION, 'has_data' => is_file(DATA_FILE)]);
}

out(['ok' => false, 'error' => '未知的 action'], 400);
