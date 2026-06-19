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

$integrity = $reconciliationService->status((int) $account['uid']);
$movements = $transferService->latest((int) $account['uid'], 10);
$secondsRemaining = $challengeStateService->secondsRemaining();
$flag = $integrity['unlocked'] ? loadFlag($config) : '';
$message = $_GET['msg'] ?? ($wasReset ? 'La ventana operativa expiró. El entorno fue restaurado.' : '');
$type = $_GET['type'] ?? ($wasReset ? 'warning' : 'info');
$concepts = ['Compensación privada', 'Reserva operativa', 'Movimiento interno'];
?>
<!doctype html>
<html lang="es">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title><?= e($config['app_name']) ?> · Portal privado de transferencias</title>
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
                <p class="subtitle">Portal privado de transferencias</p>
            </div>
            <div class="secure-pill">
                <span class="pulse"></span>
                Sesión segura · <strong data-timer="<?= e($secondsRemaining) ?>"><?= e($secondsRemaining) ?>s</strong>
            </div>
        </header>

        <?php if ($message): ?>
            <section class="notice notice-<?= e($type) ?> card"><?= e($message) ?></section>
        <?php endif; ?>

        <?php if ($integrity['unlocked']): ?>
            <section class="alert-unlocked card">
                <p class="eyebrow">Alerta de conciliación</p>
                <h2>El motor de integridad detectó un desvío contable entre operaciones aprobadas y saldo disponible.</h2>
                <p>Código de auditoría desbloqueado:</p>
                <code><?= e($flag) ?></code>
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
                <p class="eyebrow">Integridad transaccional</p>
                <h2><?= e($integrity['label']) ?></h2>
                <div class="status-row"><span>Motor de riesgo</span><strong>Activo</strong></div>
                <div class="status-row"><span>Conciliación</span><strong><?= e($integrity['label']) ?></strong></div>
                <div class="status-row"><span>Operaciones aprobadas</span><strong><?= e($integrity['approved_count']) ?></strong></div>
            </article>

            <article class="card balance-card">
                <p class="eyebrow">Saldo disponible</p>
                <div class="balance"><?= e(money((int) $account['balance'])) ?></div>
                <div class="meta-list">
                    <span>Límite por operación: <strong><?= e(money((int) $config['challenge']['max_transfer_amount'])) ?></strong></span>
                    <span>Ventana operativa: <strong><?= e($config['challenge']['window_seconds']) ?> segundos</strong></span>
                </div>
            </article>

            <article class="card transfer-card">
                <p class="eyebrow">Nueva transferencia</p>
                <h2>Canal privado</h2>
                <form method="post" action="/transferencia.php" autocomplete="off">
                    <label for="amount">Monto</label>
                    <input id="amount" name="amount" type="number" min="1" max="<?= e($config['challenge']['max_transfer_amount']) ?>" value="100" required>

                    <label for="destination_alias">Alias destino</label>
                    <input id="destination_alias" name="destination_alias" value="<?= e($config['challenge']['destination_alias']) ?>" readonly>

                    <label for="concept">Concepto</label>
                    <select id="concept" name="concept">
                        <?php foreach ($concepts as $concept): ?>
                            <option value="<?= e($concept) ?>"><?= e($concept) ?></option>
                        <?php endforeach; ?>
                    </select>

                    <button class="btn-primary" type="submit">Ejecutar transferencia</button>
                </form>
            </article>
        </section>

        <section class="card movements-card">
            <div class="section-head">
                <div>
                    <p class="eyebrow">Historial de movimientos</p>
                    <h2>Movimientos recientes</h2>
                </div>
                <form method="post" action="/reset.php">
                    <button class="btn-secondary" type="submit">Restaurar entorno</button>
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
                                    <td><span class="tag">Aprobada</span></td>
                                    <td><?= e($movement['destination_alias']) ?></td>
                                    <td><?= e($movement['concept'] ?? 'Operación interna') ?></td>
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
