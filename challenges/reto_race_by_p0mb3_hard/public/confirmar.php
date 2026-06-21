<?php

declare(strict_types=1);

if (session_status() === PHP_SESSION_ACTIVE) {
    session_write_close();
}

require_once dirname(__DIR__) . '/app/bootstrap.php';

$challengeStateService->ensureActiveWindow();

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    redirectTo('/');
}

$operationId = trim((string) ($_POST['operation_id'] ?? ''));
$transferToken = trim((string) ($_POST['transfer_token'] ?? ''));

if ($operationId === '' || $transferToken === '') {
    redirectTo('/?type=error&msg=' . rawurlencode('La autorización operativa no fue aceptada.'));
}

try {
    $result = $operationService->confirmOperationVulnerable($operationId, $transferToken);
    if (!empty($result['ok'])) {
        redirectTo('/?type=success&msg=' . rawurlencode('La operación fue derivada al lote interno.'));
    }

    redirectTo('/?type=error&msg=' . rawurlencode($result['message']));
} catch (Throwable $e) {
    if (!empty($config['verbose_errors'])) {
        throw $e;
    }
    redirectTo('/?type=error&msg=' . rawurlencode('La autorización operativa no pudo completarse.'));
}
