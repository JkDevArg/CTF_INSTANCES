<?php

declare(strict_types=1);

if (session_status() === PHP_SESSION_ACTIVE) {
    session_write_close();
}

require_once dirname(__DIR__) . '/app/bootstrap.php';

$challengeStateService->ensureActiveWindow();

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    redirectTo('/lote.php');
}

$batchId = trim((string) ($_POST['batch_id'] ?? ''));
$closeToken = trim((string) ($_POST['close_token'] ?? ''));
if ($batchId === '' || $closeToken === '') {
    redirectTo('/lote.php?type=error&msg=' . rawurlencode('La validación de cierre no se encuentra disponible.'));
}

try {
    $result = $settlementService->closeBatchVulnerable($batchId, $closeToken);
    if (empty($result['ok'])) {
        redirectTo('/lote.php?type=error&msg=' . rawurlencode($result['message']));
    }

    $incident = $incidentCaseService->evaluateBatchIncident($batchId);
    $message = $incident
        ? 'Lote derivado a mesa de control.'
        : 'Cierre operativo registrado.';
    redirectTo('/lote.php?type=success&msg=' . rawurlencode($message) . '&batch=' . rawurlencode($batchId));
} catch (Throwable $e) {
    if (!empty($config['verbose_errors'])) {
        throw $e;
    }
    redirectTo('/lote.php?type=error&msg=' . rawurlencode('El cierre operativo no pudo registrarse.'));
}
