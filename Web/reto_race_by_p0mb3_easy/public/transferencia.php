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

$amount = filter_input(INPUT_POST, 'amount', FILTER_VALIDATE_INT);
$concept = trim((string) ($_POST['concept'] ?? 'Movimiento interno'));
$destination = trim((string) ($_POST['destination_alias'] ?? $config['challenge']['destination_alias']));

if ($destination === '') {
    $destination = (string) $config['challenge']['destination_alias'];
}

if ($amount === false || $amount === null) {
    redirectTo('/?type=error&msg=' . rawurlencode('El monto debe estar entre $1 y ' . money((int) $config['challenge']['max_transfer_amount']) . '.'));
}

try {
    $result = $transferService->executeTransfer((int) $amount, $concept, $destination, $reconciliationService);
    redirectTo('/?type=' . ($result['ok'] ? 'success' : 'error') . '&msg=' . rawurlencode($result['message']));
} catch (Throwable $e) {
    if (!empty($config['verbose_errors'])) {
        throw $e;
    }
    redirectTo('/?type=error&msg=' . rawurlencode('La operación no pudo ser procesada por el canal privado.'));
}
