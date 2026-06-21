<?php

declare(strict_types=1);

final class SettlementService
{
    public function __construct(
        private PDO $pdo,
        private array $config
    ) {
    }

    public function calculateBatchTotal(string $batchId): int
    {
        $stmt = $this->pdo->prepare('SELECT COALESCE(SUM(amount), 0) FROM bank_batch_operations WHERE batch_id = :batch_id');
        $stmt->execute(['batch_id' => $batchId]);
        return (int) $stmt->fetchColumn();
    }

    public function closeBatchVulnerable(string $batchId, string $closeToken): array
    {
        $batch = $this->getBatch($batchId);
        if (!$batch) {
            return ['ok' => false, 'message' => 'Cierre no disponible.'];
        }

        if ((string) $batch['status'] !== 'ready_to_close') {
            return ['ok' => false, 'message' => 'El cierre indicado no se encuentra disponible.'];
        }

        if (!$this->verifyCloseToken($batch, $closeToken)) {
            return ['ok' => false, 'message' => 'La validación operativa no pudo completarse.'];
        }

        $total = $this->calculateBatchTotal($batchId);
        if ($total < 1) {
            return ['ok' => false, 'message' => 'El lote actual no registra operaciones aplicables.'];
        }

        $window = (int) $this->config['challenge']['batch_close_window_us'];
        usleep($window);

        $settlementId = settlementReference();
        $stmt = $this->pdo->prepare(
            'INSERT INTO settlement_entries (settlement_id, batch_id, amount, source_request_id)
             VALUES (:settlement_id, :batch_id, :amount, :source_request_id)'
        );
        $stmt->execute([
            'settlement_id' => $settlementId,
            'batch_id' => $batchId,
            'amount' => $total,
            'source_request_id' => requestReference(),
        ]);

        usleep(max(1000, (int) ($window / 4)));

        $update = $this->pdo->prepare('UPDATE bank_batches SET status = :status, closed_at = NOW() WHERE batch_id = :batch_id');
        $update->execute([
            'status' => 'closed',
            'batch_id' => $batchId,
        ]);

        return [
            'ok' => true,
            'message' => 'Cierre registrado.',
            'batch_id' => $batchId,
            'settlement_id' => $settlementId,
            'amount' => $total,
        ];
    }

    public function getSettlementCount(string $batchId): int
    {
        $stmt = $this->pdo->prepare('SELECT COUNT(*) FROM settlement_entries WHERE batch_id = :batch_id');
        $stmt->execute(['batch_id' => $batchId]);
        return (int) $stmt->fetchColumn();
    }

    public function getSettlementTotal(string $batchId): int
    {
        $stmt = $this->pdo->prepare('SELECT COALESCE(SUM(amount), 0) FROM settlement_entries WHERE batch_id = :batch_id');
        $stmt->execute(['batch_id' => $batchId]);
        return (int) $stmt->fetchColumn();
    }

    public function getBatch(string $batchId): ?array
    {
        $stmt = $this->pdo->prepare('SELECT * FROM bank_batches WHERE batch_id = :batch_id LIMIT 1');
        $stmt->execute(['batch_id' => $batchId]);
        $batch = $stmt->fetch();
        return $batch ?: null;
    }

    private function verifyCloseToken(array $batch, string $token): bool
    {
        return hash_equals((string) $batch['close_token_hash'], hash('sha256', $token));
    }
}
