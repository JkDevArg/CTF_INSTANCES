<?php

declare(strict_types=1);

require_once dirname(__DIR__) . '/app/bootstrap.php';

$wasReset = $challengeStateService->ensureActiveWindow();
$account = $accountService->findByCode($config['challenge']['account_code']);
if (!$account) {
    http_response_code(500);
    echo 'Cuenta no disponible';
    exit;
}

$status = $incidentService->status((int) $account['uid']);
$movements = $transferService->latest((int) $account['uid'], 10);
$secondsRemaining = $challengeStateService->secondsRemaining();
$resetToken = $challengeStateService->generateResetToken();
$message = $_GET['msg'] ?? ($wasReset ? 'La ventana operativa fue renovada automáticamente.' : '');
$type = $_GET['type'] ?? ($wasReset ? 'warning' : 'info');
$concepts = ['Compensación privada', 'Reserva operativa', 'Movimiento diferido'];
$activeBatch = $batchService->getActiveBatch();
$batchLabel = $activeBatch['batch_id'] ?? 'Sin preparar';
$batchStatus = $activeBatch['status'] ?? 'open';
$batchStatusLabel = match ($batchStatus) {
    'ready_to_close' => 'Listo para cierre',
    'closed' => 'Cierre aplicado',
    'observed' => 'Con observación',
    default => 'En preparación',
};
$currentCase = $incidentCaseService->currentCase();
$hasReview = $currentCase !== null && (string) ($currentCase['status'] ?? '') === 'enabled';
?>
<!doctype html>
<html lang="es">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title><?= e($config['app_name']) ?> · Portal privado de operaciones</title>
    <link rel="stylesheet" href="/assets/style.css">
    <script src="/assets/app.js" defer></script>
</head>
<body>
    <div class="orb orb-a"></div>
    <div class="orb orb-b"></div>
    <main class="shell">
        <header class="topbar card">
            <div>
                <p class="eyebrow">Banca privada digital</p>
                <h1><span>HACKL4BS</span> VAULT</h1>
                <p class="subtitle">Portal privado de operaciones</p>
            </div>
            <div class="secure-pill">
                <span class="pulse"></span>
                Ventana operativa · <strong data-timer="<?= e($secondsRemaining) ?>"><?= e($secondsRemaining) ?>s</strong>
            </div>
        </header>

        <?php if ($message): ?>
            <section class="notice notice-<?= e($type) ?> card"><?= e($message) ?></section>
        <?php endif; ?>

        <?php if ($hasReview): ?>
            <section class="card review-banner">
                <p class="eyebrow">Control de cierre</p>
                <h2>Lote derivado a mesa de control</h2>
                <p class="subtitle">Existe un expediente pendiente de conciliación para la ventana actual.</p>
                <div class="incident-stack">
                    <a class="btn-primary btn-inline" href="/mesa_control.php">Ir a mesa de control</a>
                </div>
            </section>
        <?php endif; ?>

        <section class="grid">
            <article class="card account-card">
                <p class="eyebrow">Cuenta privada</p>
                <h2><?= e($account['uname']) ?></h2>
                <p class="account-number"><?= e($account['account_number']) ?></p>
                <div class="meta-list">
                    <span>Perfil: <strong>Cliente privado</strong></span>
                    <span>Estado: <strong>Activa</strong></span>
                    <span>Canal: <strong>Privado</strong></span>
                </div>
            </article>

            <article class="card integrity-card">
                <p class="eyebrow">Control operativo</p>
                <h2><?= e($status['label']) ?></h2>
                <div class="status-row"><span>Mesa interna</span><strong>Activa</strong></div>
                <div class="status-row"><span>Conciliación</span><strong><?= e($status['label']) ?></strong></div>
                <div class="status-row"><span>Ventana</span><strong><?= $secondsRemaining > 0 ? 'Activa' : 'Cierre' ?></strong></div>
            </article>

            <article class="card balance-card">
                <p class="eyebrow">Saldo disponible</p>
                <div class="balance"><?= e(money((int) $account['balance'])) ?></div>
                <div class="meta-list">
                    <span>Límite por operación: <strong><?= e(money((int) $config['challenge']['max_transfer_amount'])) ?></strong></span>
                    <span>Solicitudes por ventana: <strong><?= e((string) $config['challenge']['max_operations_per_window']) ?></strong></span>
                </div>
            </article>

            <article class="card transfer-card">
                <p class="eyebrow">Nueva operación</p>
                <h2>Solicitud de lote</h2>
                <form method="post" action="/preparar.php" autocomplete="off">
                    <label for="monto_operacion">Monto</label>
                    <input id="monto_operacion" name="monto_operacion" type="number" min="1" max="<?= e($config['challenge']['max_transfer_amount']) ?>" value="100" required>

                    <label for="alias_destino">Alias destino</label>
                    <input id="alias_destino" name="alias_destino" value="<?= e($config['challenge']['destination_alias']) ?>" required>

                    <label for="referencia_cliente">Referencia</label>
                    <select id="referencia_cliente" name="referencia_cliente">
                        <?php foreach ($concepts as $concept): ?>
                            <option value="<?= e($concept) ?>"><?= e($concept) ?></option>
                        <?php endforeach; ?>
                    </select>

                    <button class="btn-primary" type="submit">Preparar operación</button>
                </form>
                <div class="meta-list" style="margin-top:18px;">
                    <span>Lote activo: <strong><?= e($batchLabel) ?></strong></span>
                    <span>Estado de lote: <strong><?= e($batchStatusLabel) ?></strong></span>
                </div>
                <p style="margin-top:16px;"><a class="btn-secondary btn-inline" href="/lote.php">Ir al lote operativo</a></p>
            </article>
        </section>

        <section class="card movements-card">
            <div class="section-head">
                <div>
                    <p class="eyebrow">Movimientos recientes</p>
                    <h2>Actividad del operador</h2>
                </div>
                <form method="post" action="/reset.php">
                    <input type="hidden" name="reset_token" value="<?= e($resetToken) ?>">
                    <button class="btn-secondary" type="submit">Nueva ventana operativa</button>
                </form>
            </div>

            <?php if (!$movements): ?>
                <p class="empty">Sin movimientos registrados en la ventana actual.</p>
            <?php else: ?>
                <div class="table-wrap">
                    <table>
                        <thead>
                            <tr>
                                <th>Referencia</th>
                                <th>Estado</th>
                                <th>Destino</th>
                                <th>Concepto</th>
                                <th>Monto</th>
                                <th>Fecha</th>
                            </tr>
                        </thead>
                        <tbody>
                            <?php foreach ($movements as $movement): ?>
                                <tr>
                                    <td><?= e($movement['reference_code']) ?></td>
                                    <td><span class="tag">Derivada</span></td>
                                    <td><?= e($movement['destination_alias']) ?></td>
                                    <td><?= e($movement['concept'] ?? 'Movimiento interno') ?></td>
                                    <td><?= e(money((int) $movement['amount'])) ?></td>
                                    <td><?= e($movement['created_at']) ?></td>
                                </tr>
                            <?php endforeach; ?>
                        </tbody>
                    </table>
                </div>
            <?php endif; ?>
        </section>
    </main>
</body>
</html>
