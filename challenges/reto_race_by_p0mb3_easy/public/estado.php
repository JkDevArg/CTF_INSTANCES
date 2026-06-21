<?php

declare(strict_types=1);

require_once dirname(__DIR__) . '/app/bootstrap.php';

$challengeStateService->ensureActiveWindow();
$account = $accountService->findByCode($config['challenge']['account_code']);
$integrity = $account ? $reconciliationService->status((int) $account['uid']) : [];

header('Content-Type: application/json; charset=utf-8');
echo json_encode([
    'saldo' => $account ? (int) $account['balance'] : null,
    'tiempo_restante' => $challengeStateService->secondsRemaining(),
    'integridad' => $integrity['label'] ?? 'No disponible',
    'desbloqueado' => (bool) ($integrity['unlocked'] ?? false),
], JSON_UNESCAPED_UNICODE);
