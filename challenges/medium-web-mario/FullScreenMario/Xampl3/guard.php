<?php
/**
 * Shared guard / helpers for the CTF flag handshake.
 * Included by arm.php and flag.php. Not meant to be requested directly
 * (doing so just starts a session and returns nothing useful).
 */

if (session_status() === PHP_SESSION_NONE) {
    session_start();
}

/* ----------------------------------------------------------------------------
 * Server secret. >>> CHANGE THIS, ideally load from OUTSIDE the web root. <<<
 *   e.g.  $SERVER_SECRET = trim(file_get_contents('C:/ctf/secret.txt'));
 * -------------------------------------------------------------------------- */
// Se lee de la variable de entorno SERVER_SECRET (Docker / hosting). El valor
// por defecto es SOLO para pruebas locales: en el evento real define el secreto
// en el archivo .env (nunca se sube a GitHub).
$SERVER_SECRET = getenv('SERVER_SECRET') ?: 'CHANGE_ME_to_a_long_random_string_kept_off_the_webroot';

/** Reject anything that isn't our own page asking (blocks naive curl / cross-site). */
function ctf_require_same_origin() {
    $host    = preg_replace('/:\d+$/', '', $_SERVER['HTTP_HOST'] ?? '');
    $origin  = $_SERVER['HTTP_ORIGIN']  ?? '';
    $referer = $_SERVER['HTTP_REFERER'] ?? '';

    $src = '';
    if ($origin !== '')       $src = parse_url($origin,  PHP_URL_HOST);
    else if ($referer !== '') $src = parse_url($referer, PHP_URL_HOST);

    if (!$src || strcasecmp((string)$src, $host) !== 0) {
        header('Content-Type: text/plain; charset=utf-8');
        http_response_code(403);
        echo '403 - nice try';
        exit;
    }
}

/** Deterministic, unforgeable, per-session flag. */
function ctf_flag() {
    global $SERVER_SECRET;
    // Whale/CTFd inyecta una flag por equipo en la variable de entorno FLAG.
    // Si existe, ESA es la flag oficial (la que el scoreboard sabe validar) y
    // se usa tanto para entregarla como para el endpoint ?check=. Si no hay
    // FLAG, se cae al modelo HMAC por-sesion (util en local / dev sin Whale).
    $injected = getenv('FLAG');
    if ($injected !== false && trim($injected) !== '') {
        return trim($injected);
    }
    if (!isset($_SESSION['ctf_seed'])) {
        $_SESSION['ctf_seed'] = bin2hex(random_bytes(8));
    }
    $digest = hash_hmac('sha256', $_SESSION['ctf_seed'], $SERVER_SECRET);
    return 'HL4{' . substr($digest, 0, 24) . '}';
}
