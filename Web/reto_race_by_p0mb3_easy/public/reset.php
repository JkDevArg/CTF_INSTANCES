<?php

declare(strict_types=1);

require_once dirname(__DIR__) . '/app/bootstrap.php';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $challengeStateService->reset('Ventana operativa reiniciada');
}

redirectTo('/?type=success&msg=' . rawurlencode('El entorno fue restaurado correctamente.'));
