<?php
/**
 * Step 1 of the handshake.
 * Called by the secret level when it loads. Marks this session as "armed",
 * stamps the time, and issues a per-session challenge token. The flag endpoint
 * will only hand out the flag to a session that went through here.
 */
require __DIR__ . '/guard.php';
ctf_require_same_origin();

$_SESSION['armed']    = true;
$_SESSION['armed_at'] = time();
if (empty($_SESSION['challenge'])) {
    $_SESSION['challenge'] = bin2hex(random_bytes(16));
}

header('Content-Type: application/json; charset=utf-8');
header('Cache-Control: no-store');
echo json_encode(['token' => $_SESSION['challenge']]);
