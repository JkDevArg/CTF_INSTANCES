<?php

declare(strict_types=1);

require_once dirname(__DIR__) . '/app/bootstrap.php';

$challengeStateService->ensureActiveWindow();
$batchReference = trim((string) ($_GET['lote'] ?? $_POST['lote'] ?? ''));
$controlValue = trim((string) (
    $_GET['clave_operativa']
    ?? $_POST['clave_operativa']
    ?? $_GET['verificador_cierre']
    ?? $_POST['verificador_cierre']
    ?? $_GET['control']
    ?? $_POST['control']
    ?? ''
));
$case = ($batchReference !== '' && $controlValue !== '')
    ? $incidentCaseService->validateCaseAccess($batchReference, $controlValue)
    : null;
$available = $case !== null;
$code = $available ? $incidentCaseService->auditCode() : null;
?>
<!doctype html>
<html lang="es">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title><?= e($config['app_name']) ?> · Expediente interno</title>
    <link rel="stylesheet" href="/assets/style.css">
</head>
<body>
    <div class="orb orb-a"></div>
    <div class="orb orb-b"></div>
    <main class="shell shell-narrow">
        <section class="card dossier-card">
            <p class="eyebrow">Expediente interno</p>
            <h1><span>HACKL4BS</span> VAULT</h1>
            <?php if ($available): ?>
                <p class="subtitle">Código de auditoría habilitado para revisión del operador.</p>
                <div class="incident-stack">
                    <div class="incident-chip">Referencia de lote: <?= e((string) $case['batch_id']) ?></div>
                    <div class="audit-code"><?= e($code) ?></div>
                </div>
            <?php else: ?>
                <p class="subtitle">La solicitud no coincide con un cierre habilitado para esta ventana operativa.</p>
                <div class="incident-empty">Expediente no disponible</div>
            <?php endif; ?>
            <p style="margin-top:18px;"><a href="/mesa_control.php" style="color:#8AA9F5;">Volver a mesa de control</a></p>
        </section>
    </main>
</body>
</html>
