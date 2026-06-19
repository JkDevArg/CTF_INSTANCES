<?php

declare(strict_types=1);

require_once dirname(__DIR__) . '/app/bootstrap.php';

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo 'Método no permitido';
    exit;
}

$resetToken = trim((string) ($_POST['reset_token'] ?? ''));
if ($resetToken === '' || !$challengeStateService->isValidResetToken($resetToken)) {
    http_response_code(403);
    echo 'Solicitud no autorizada';
    exit;
}

$challengeStateService->reset('Ventana operativa reiniciada');
redirectTo('/?type=success&msg=' . rawurlencode('La ventana operativa fue renovada correctamente.'));
