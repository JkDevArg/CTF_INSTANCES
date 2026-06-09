<?php

declare(strict_types=1);

require_once dirname(__DIR__) . '/app/bootstrap.php';

$challengeStateService->ensureActiveWindow();
$state = $challengeStateService->state();

header('Content-Type: application/json; charset=utf-8');
echo json_encode([
    'estado' => !empty($state['unlocked']) ? 'Control pendiente' : 'Operativo',
    'ventana' => $challengeStateService->secondsRemaining() > 0 ? 'Activa' : 'Cierre',
], JSON_UNESCAPED_UNICODE);
