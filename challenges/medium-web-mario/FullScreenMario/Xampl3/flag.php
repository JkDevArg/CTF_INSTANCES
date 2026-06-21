<?php
/**
 * Step 2 of the handshake: hand out the per-session flag.
 *
 * The flag is only issued if the session:
 *   1) came from our own page (same-origin),
 *   2) went through arm.php (is "armed"),
 *   3) presents the matching challenge token,
 *   4) waited at least a moment after arming (blocks instant scripted solves).
 *
 * The flag itself is an unforgeable HMAC (see guard.php), so even a player who
 * bypasses the puzzle can only ever obtain THEIR OWN session's flag — never a
 * forged one and never someone else's.
 *
 * Scoreboard helper:  GET flag.php?check=HL4{...}  ->  VALID / INVALID
 * (validates a submitted flag against the caller's own session).
 */
require __DIR__ . '/guard.php';

// --- Scoreboard validation (no handshake needed) -------------------------
if (isset($_GET['check'])) {
    header('Content-Type: text/plain; charset=utf-8');
    echo hash_equals(ctf_flag(), (string) $_GET['check']) ? 'VALID' : 'INVALID';
    exit;
}

// --- Normal flag delivery ------------------------------------------------
ctf_require_same_origin();

header('Content-Type: text/plain; charset=utf-8');
header('Cache-Control: no-store');

// 2) must have been armed
if (empty($_SESSION['armed']) || empty($_SESSION['challenge'])) {
    http_response_code(403);
    echo 'locked - load and solve the level first';
    exit;
}

// 3) token must match
$token = $_POST['token'] ?? $_GET['token'] ?? '';
if (!hash_equals($_SESSION['challenge'], (string) $token)) {
    http_response_code(403);
    echo 'locked - bad token';
    exit;
}

// 4) anti-instant gate
if (time() - (int) ($_SESSION['armed_at'] ?? 0) < 1) {
    http_response_code(403);
    echo 'locked - too fast';
    exit;
}

echo ctf_flag();
