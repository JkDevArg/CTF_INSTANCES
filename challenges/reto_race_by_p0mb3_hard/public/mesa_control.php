<?php

declare(strict_types=1);

require_once dirname(__DIR__) . '/app/bootstrap.php';

$challengeStateService->ensureActiveWindow();
$currentCase = $incidentCaseService->currentCase();
$secondsRemaining = $challengeStateService->secondsRemaining();
$message = $_GET['msg'] ?? '';
$type = $_GET['type'] ?? 'info';
$hasReview = $currentCase !== null && (string) ($currentCase['status'] ?? '') === 'enabled';
$batchReference = (string) ($currentCase['batch_id'] ?? '');
$batchSummary = $batchReference !== '' ? $batchService->getBatchSummary($batchReference) : [];
$settlementCount = $batchReference !== '' ? $settlementService->getSettlementCount($batchReference) : 0;
$batchTotal = (int) ($batchSummary['operations_total'] ?? 0);
$visibleSuffix = $batchReference !== '' ? substr($batchReference, -4) : '';
?>
<!doctype html>
<html lang="es">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title><?= e($config['app_name']) ?> · Mesa de control</title>
    <link rel="stylesheet" href="/assets/style.css">
    <script src="/assets/app.js" defer></script>
</head>
<body>
    <div class="orb orb-a"></div>
    <div class="orb orb-b"></div>
    <main class="shell shell-narrow">
        <header class="topbar card">
            <div>
                <p class="eyebrow">Mesa de control</p>
                <h1><span>HACKL4BS</span> VAULT</h1>
                <p class="subtitle">Validación operativa de cierres pendientes</p>
            </div>
            <div class="secure-pill">
                <span class="pulse"></span>
                Ventana operativa · <strong data-timer="<?= e($secondsRemaining) ?>"><?= e($secondsRemaining) ?>s</strong>
            </div>
        </header>

        <?php if ($message !== ''): ?>
            <section class="notice notice-<?= e($type) ?> card"><?= e($message) ?></section>
        <?php endif; ?>

        <section class="card dossier-card">
            <p class="eyebrow">Revisión manual</p>
            <h2><?= $hasReview ? 'Lote derivado a mesa de control' : 'Sin expedientes disponibles' ?></h2>
            <?php if ($hasReview): ?>
                <p class="subtitle">Existe un expediente pendiente de conciliación para la ventana actual. Calcule la clave de conciliación con los datos del cierre operativo.</p>
                <div class="meta-list" style="margin:24px 0;">
                    <span>Referencia de lote: <strong><?= e($batchReference) ?></strong></span>
                    <span>Total del lote: <strong><?= e(money($batchTotal)) ?></strong></span>
                    <span>Asientos de cierre: <strong><?= e((string) $settlementCount) ?></strong></span>
                    <span>Sufijo visible: <strong><?= e($visibleSuffix) ?></strong></span>
                </div>
                <form method="get" action="/expediente.php">
                    <input type="hidden" name="lote" value="<?= e($batchReference) ?>">

                    <label for="verificador_cierre">Clave de conciliación</label>
                    <input id="verificador_cierre" name="verificador_cierre" placeholder="Ingrese la clave operativa" required>

                    <button class="btn-primary" type="submit">Abrir expediente</button>
                </form>
            <?php else: ?>
                <p class="subtitle">No hay expedientes disponibles para esta ventana operativa.</p>
                <div class="incident-empty">Mesa de control sin novedades.</div>
            <?php endif; ?>
            <p style="margin-top:18px;"><a href="/" style="color:#8AA9F5;">Volver al panel</a></p>
        </section>
    </main>
</body>
</html>
