<?php

declare(strict_types=1);

require_once dirname(__DIR__) . '/app/bootstrap.php';

$challengeStateService->ensureActiveWindow();
$message = $_GET['msg'] ?? '';
$type = $_GET['type'] ?? 'info';
$closeToken = trim((string) ($_GET['close_token'] ?? ''));

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $action = (string) ($_POST['action'] ?? '');
    if ($action === 'attach') {
        $result = $batchService->attachApprovedOperationToBatch(trim((string) ($_POST['operation_id'] ?? '')));
        $message = $result['message'];
        $type = !empty($result['ok']) ? 'success' : 'error';
    } elseif ($action === 'ready') {
        $result = $batchService->markBatchReady(trim((string) ($_POST['batch_id'] ?? '')));
        $message = $result['message'];
        $type = !empty($result['ok']) ? 'success' : 'error';
        if (!empty($result['ok'])) {
            $closeToken = (string) ($result['close_token'] ?? '');
        }
    }
}

$currentBatch = $batchService->getActiveBatch();
if (!$currentBatch || (string) $currentBatch['status'] === 'closed') {
    $currentBatch = $batchService->createOrGetOpenBatch();
}
$batchId = (string) ($currentBatch['batch_id'] ?? '');
$summary = $batchId !== '' ? $batchService->getBatchSummary($batchId) : [];
$batchOperations = $batchId !== '' ? $batchService->listBatchOperations($batchId) : [];
$availableOperations = $batchService->listAttachableOperations();
$secondsRemaining = $challengeStateService->secondsRemaining();
$currentCase = $incidentCaseService->currentCase();
$hasReview = $currentCase !== null && (string) ($currentCase['status'] ?? '') === 'enabled';
$statusLabel = match ((string) ($summary['status'] ?? 'open')) {
    'ready_to_close' => 'Listo para cierre',
    'closed' => 'Cierre registrado',
    'observed' => 'Con observación',
    default => 'En preparación',
};
?>
<!doctype html>
<html lang="es">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title><?= e($config['app_name']) ?> · Lote operativo</title>
    <link rel="stylesheet" href="/assets/style.css">
    <script src="/assets/app.js" defer></script>
</head>
<body>
    <div class="orb orb-a"></div>
    <div class="orb orb-b"></div>
    <main class="shell">
        <header class="topbar card">
            <div>
                <p class="eyebrow">Cámara de compensación</p>
                <h1><span>HACKL4BS</span> VAULT</h1>
                <p class="subtitle">Lote operativo de la ventana actual</p>
            </div>
            <div class="secure-pill">
                <span class="pulse"></span>
                Ventana operativa · <strong data-timer="<?= e($secondsRemaining) ?>"><?= e($secondsRemaining) ?>s</strong>
            </div>
        </header>

        <?php if ($message !== ''): ?>
            <section class="notice notice-<?= e($type) ?> card"><?= e($message) ?></section>
        <?php endif; ?>

        <?php if ($hasReview): ?>
            <section class="card review-banner">
                <p class="eyebrow">Mesa de control</p>
                <h2>Lote derivado a mesa de control</h2>
                <p class="subtitle">Existe un expediente pendiente para la ventana actual.</p>
                <div class="incident-stack">
                    <a class="btn-primary btn-inline" href="/mesa_control.php">Ir a mesa de control</a>
                </div>
            </section>
        <?php endif; ?>

        <section class="grid">
            <article class="card account-card">
                <p class="eyebrow">Lote operativo</p>
                <h2><?= e($batchId !== '' ? $batchId : 'Sin referencia') ?></h2>
                <div class="meta-list">
                    <span>Estado: <strong><?= e($statusLabel) ?></strong></span>
                    <span>Operaciones: <strong><?= e((string) ($summary['operations_count'] ?? 0)) ?></strong></span>
                    <span>Total: <strong><?= e(money((int) ($summary['operations_total'] ?? 0))) ?></strong></span>
                </div>
                <p style="margin-top:16px;"><a class="btn-secondary btn-inline" href="/">Volver al panel</a></p>
            </article>

            <article class="card transfer-card">
                <p class="eyebrow">Preparación de cierre</p>
                <h2>Cierre del lote</h2>
                <p class="subtitle">Derive operaciones al lote y prepare el envío a la cámara operativa.</p>
                <form method="post" action="/lote.php">
                    <input type="hidden" name="action" value="ready">
                    <input type="hidden" name="batch_id" value="<?= e($batchId) ?>">
                    <button class="btn-primary" type="submit">Preparar cierre</button>
                </form>

                <?php if (((string) ($summary['status'] ?? '')) === 'ready_to_close' && $closeToken !== ''): ?>
                    <form method="post" action="/cerrar_lote.php" style="margin-top:16px;">
                        <input type="hidden" name="batch_id" value="<?= e($batchId) ?>">
                        <input type="hidden" name="close_token" value="<?= e($closeToken) ?>">
                        <button class="btn-secondary" type="submit">Enviar a cámara operativa</button>
                    </form>
                <?php elseif (((string) ($summary['status'] ?? '')) === 'ready_to_close'): ?>
                    <p class="subtitle" style="margin-top:16px;">Renueve la validación de cierre para continuar con el envío.</p>
                <?php endif; ?>
            </article>
        </section>

        <section class="card movements-card">
            <div class="section-head">
                <div>
                    <p class="eyebrow">Operaciones disponibles</p>
                    <h2>Derivación al lote</h2>
                </div>
            </div>

            <?php if (!$availableOperations): ?>
                <p class="empty">No hay operaciones aprobadas pendientes de lote en esta ventana.</p>
            <?php else: ?>
                <div class="table-wrap">
                    <table>
                        <thead>
                            <tr>
                                <th>Operación</th>
                                <th>Destino</th>
                                <th>Concepto</th>
                                <th>Monto</th>
                                <th>Acción</th>
                            </tr>
                        </thead>
                        <tbody>
                            <?php foreach ($availableOperations as $operation): ?>
                                <tr>
                                    <td><?= e($operation['operation_id']) ?></td>
                                    <td><?= e($operation['destination_alias']) ?></td>
                                    <td><?= e($operation['concept']) ?></td>
                                    <td><?= e(money((int) $operation['amount'])) ?></td>
                                    <td>
                                        <form method="post" action="/lote.php">
                                            <input type="hidden" name="action" value="attach">
                                            <input type="hidden" name="operation_id" value="<?= e($operation['operation_id']) ?>">
                                            <button class="btn-secondary btn-inline" type="submit">Agregar</button>
                                        </form>
                                    </td>
                                </tr>
                            <?php endforeach; ?>
                        </tbody>
                    </table>
                </div>
            <?php endif; ?>
        </section>

        <section class="card movements-card">
            <div class="section-head">
                <div>
                    <p class="eyebrow">Contenido actual</p>
                    <h2>Operaciones del lote</h2>
                </div>
            </div>

            <?php if (!$batchOperations): ?>
                <p class="empty">El lote actual todavía no registra operaciones derivadas.</p>
            <?php else: ?>
                <div class="table-wrap">
                    <table>
                        <thead>
                            <tr>
                                <th>Operación</th>
                                <th>Destino</th>
                                <th>Concepto</th>
                                <th>Monto</th>
                                <th>Estado</th>
                            </tr>
                        </thead>
                        <tbody>
                            <?php foreach ($batchOperations as $operation): ?>
                                <tr>
                                    <td><?= e($operation['operation_id']) ?></td>
                                    <td><?= e($operation['destination_alias']) ?></td>
                                    <td><?= e($operation['concept']) ?></td>
                                    <td><?= e(money((int) $operation['amount'])) ?></td>
                                    <td><span class="tag"><?= e($operation['status'] === 'observed' ? 'Con revisión' : 'Derivada') ?></span></td>
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
