<?php

declare(strict_types=1);

final class BatchService
{
    public function __construct(
        private PDO $pdo,
        private ChallengeStateService $challengeStateService,
        private array $config
    ) {
    }

    public function createOrGetOpenBatch(): array
    {
        $windowId = $this->challengeStateService->currentWindowId();
        $stmt = $this->pdo->prepare(
            "SELECT * FROM bank_batches WHERE operator_window_id = :operator_window_id AND status IN ('open', 'ready_to_close') ORDER BY id DESC LIMIT 1"
        );
        $stmt->execute(['operator_window_id' => $windowId]);
        $batch = $stmt->fetch();
        if ($batch) {
            $this->challengeStateService->updateBatchState((string) $batch['batch_id']);
            return $batch;
        }

        $batchId = batchPublicId();
        $closeToken = batchCloseToken();
        $stmt = $this->pdo->prepare(
            'INSERT INTO bank_batches (batch_id, status, operator_window_id, close_token_hash)
             VALUES (:batch_id, :status, :operator_window_id, :close_token_hash)'
        );
        $stmt->execute([
            'batch_id' => $batchId,
            'status' => 'open',
            'operator_window_id' => $windowId,
            'close_token_hash' => hash('sha256', $closeToken),
        ]);
        $this->challengeStateService->updateBatchState($batchId);

        return [
            'batch_id' => $batchId,
            'status' => 'open',
            'operator_window_id' => $windowId,
            'close_token_hash' => hash('sha256', $closeToken),
            'close_token' => $closeToken,
            'created_at' => date('Y-m-d H:i:s'),
            'ready_at' => null,
            'closed_at' => null,
        ];
    }

    public function attachApprovedOperationToBatch(string $operationId): array
    {
        $batch = $this->createOrGetOpenBatch();
        if ((string) $batch['status'] !== 'open') {
            return ['ok' => false, 'message' => 'El lote actual no admite nuevas derivaciones.'];
        }

        if ($this->countBatchOperations((string) $batch['batch_id']) >= (int) $this->config['challenge']['max_batch_operations']) {
            return ['ok' => false, 'message' => 'El lote actual ya completó su capacidad operativa.'];
        }

        $operation = $this->getApprovedOperation($operationId);
        if (!$operation) {
            return ['ok' => false, 'message' => 'La operación indicada no se encuentra disponible para el lote.'];
        }

        $stmt = $this->pdo->prepare(
            'INSERT INTO bank_batch_operations (batch_id, operation_id, amount, status)
             VALUES (:batch_id, :operation_id, :amount, :status)'
        );

        try {
            $stmt->execute([
                'batch_id' => (string) $batch['batch_id'],
                'operation_id' => (string) $operation['operation_id'],
                'amount' => (int) $operation['amount'],
                'status' => 'attached',
            ]);
        } catch (PDOException $e) {
            if ($e->getCode() === '23000') {
                return ['ok' => true, 'message' => 'La operación ya se encuentra derivada al lote actual.', 'batch_id' => (string) $batch['batch_id']];
            }
            throw $e;
        }

        return ['ok' => true, 'message' => 'Operación vinculada al lote operativo.', 'batch_id' => (string) $batch['batch_id']];
    }

    public function markBatchReady(string $batchId): array
    {
        $batch = $this->getBatch($batchId);
        if (!$batch) {
            return ['ok' => false, 'message' => 'Lote no disponible.'];
        }

        if ((string) $batch['status'] === 'closed') {
            return ['ok' => false, 'message' => 'El lote seleccionado ya no admite nuevos cierres.'];
        }

        if ($this->countBatchOperations($batchId) < 1) {
            return ['ok' => false, 'message' => 'El lote no contiene operaciones derivadas.'];
        }

        $closeToken = batchCloseToken();
        $stmt = $this->pdo->prepare(
            'UPDATE bank_batches
             SET status = :status,
                 ready_at = COALESCE(ready_at, NOW()),
                 close_token_hash = :close_token_hash
             WHERE batch_id = :batch_id'
        );
        $stmt->execute([
            'status' => 'ready_to_close',
            'close_token_hash' => hash('sha256', $closeToken),
            'batch_id' => $batchId,
        ]);
        $this->challengeStateService->updateBatchState($batchId, 'Normal');

        return [
            'ok' => true,
            'message' => 'Lote preparado para cámara operativa.',
            'batch_id' => $batchId,
            'close_token' => $closeToken,
        ];
    }

    public function getBatch(string $batchId): ?array
    {
        $stmt = $this->pdo->prepare('SELECT * FROM bank_batches WHERE batch_id = :batch_id LIMIT 1');
        $stmt->execute(['batch_id' => $batchId]);
        $batch = $stmt->fetch();
        return $batch ?: null;
    }

    public function getActiveBatch(): ?array
    {
        $state = $this->challengeStateService->state();
        $activeBatchId = $state['active_batch_id'] ?? null;
        if (is_string($activeBatchId) && $activeBatchId !== '') {
            $batch = $this->getBatch($activeBatchId);
            if ($batch) {
                return $batch;
            }
        }

        $windowId = $this->challengeStateService->currentWindowId();
        $stmt = $this->pdo->prepare('SELECT * FROM bank_batches WHERE operator_window_id = :operator_window_id ORDER BY id DESC LIMIT 1');
        $stmt->execute(['operator_window_id' => $windowId]);
        $batch = $stmt->fetch();
        return $batch ?: null;
    }

    public function getBatchSummary(string $batchId): array
    {
        $batch = $this->getBatch($batchId) ?? [];
        $batch['operations_count'] = $this->countBatchOperations($batchId);
        $batch['operations_total'] = $this->calculateBatchTotal($batchId);
        return $batch;
    }

    public function listBatchOperations(string $batchId): array
    {
        $stmt = $this->pdo->prepare(
            'SELECT b.operation_id, b.amount, b.status, o.concept, o.destination_alias, o.approved_at, o.created_at
             FROM bank_batch_operations b
             INNER JOIN bank_operations o ON o.operation_id = b.operation_id
             WHERE b.batch_id = :batch_id
             ORDER BY b.id ASC'
        );
        $stmt->execute(['batch_id' => $batchId]);
        return $stmt->fetchAll();
    }

    public function listAttachableOperations(): array
    {
        $stmt = $this->pdo->query(
            "SELECT o.operation_id, o.amount, o.concept, o.destination_alias, o.approved_at
             FROM bank_operations o
             WHERE o.status = 'approved'
               AND NOT EXISTS (
                   SELECT 1 FROM bank_batch_operations b WHERE b.operation_id = o.operation_id
               )
             ORDER BY o.id DESC"
        );
        return $stmt->fetchAll();
    }

    public function calculateBatchTotal(string $batchId): int
    {
        $stmt = $this->pdo->prepare('SELECT COALESCE(SUM(amount), 0) FROM bank_batch_operations WHERE batch_id = :batch_id');
        $stmt->execute(['batch_id' => $batchId]);
        return (int) $stmt->fetchColumn();
    }

    public function countBatchOperations(string $batchId): int
    {
        $stmt = $this->pdo->prepare('SELECT COUNT(*) FROM bank_batch_operations WHERE batch_id = :batch_id');
        $stmt->execute(['batch_id' => $batchId]);
        return (int) $stmt->fetchColumn();
    }

    private function getApprovedOperation(string $operationId): ?array
    {
        $stmt = $this->pdo->prepare("SELECT operation_id, amount, status FROM bank_operations WHERE operation_id = :operation_id AND status = 'approved' LIMIT 1");
        $stmt->execute(['operation_id' => $operationId]);
        $row = $stmt->fetch();
        return $row ?: null;
    }
}
