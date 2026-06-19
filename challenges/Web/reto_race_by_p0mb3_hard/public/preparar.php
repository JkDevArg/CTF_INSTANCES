<?php

declare(strict_types=1);

require_once dirname(__DIR__) . '/app/bootstrap.php';

$challengeStateService->ensureActiveWindow();

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    redirectTo('/');
}

$amount = filter_input(INPUT_POST, 'monto_operacion', FILTER_VALIDATE_INT);
$destination = trim((string) ($_POST['alias_destino'] ?? $config['challenge']['destination_alias']));
$concept = trim((string) ($_POST['referencia_cliente'] ?? 'Movimiento diferido'));

if ($amount === false || $amount === null) {
    redirectTo('/?type=error&msg=' . rawurlencode('La solicitud no pudo ser preparada.'));
}

$result = $operationService->createPendingOperation((int) $amount, $destination, $concept);
if (!$result['ok']) {
    redirectTo('/?type=error&msg=' . rawurlencode($result['message']));
}
?>
<!doctype html>
<html lang="es">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title><?= e($config['app_name']) ?> · Confirmación operativa</title>
    <link rel="stylesheet" href="/assets/style.css">
</head>
<body>
    <div class="orb orb-a"></div>
    <div class="orb orb-b"></div>
    <main class="shell shell-narrow">
        <section class="card dossier-card">
            <p class="eyebrow">Solicitud preparada</p>
            <h1><span>HACKL4BS</span> VAULT</h1>
            <p class="subtitle">Revise los datos antes de confirmar. La operación quedará sujeta a control de cierre.</p>

            <div class="meta-list" style="margin: 24px 0;">
                <span>Alias destino: <strong><?= e($result['destination_alias']) ?></strong></span>
                <span>Referencia: <strong><?= e($result['concept']) ?></strong></span>
                <span>Monto: <strong><?= e(money((int) $result['amount'])) ?></strong></span>
                <span>Autorización disponible por: <strong><?= e((string) $result['ttl_seconds']) ?> segundos</strong></span>
            </div>

            <form method="post" action="/confirmar.php">
                <input type="hidden" name="operation_id" value="<?= e($result['operation_id']) ?>">
                <input type="hidden" name="transfer_token" value="<?= e($result['transfer_token']) ?>">
                <button class="btn-primary" type="submit">Confirmar operación</button>
            </form>

            <p style="margin-top:16px;"><a href="/" style="color:#8AA9F5;">Volver al panel</a></p>
        </section>
    </main>
</body>
</html>
