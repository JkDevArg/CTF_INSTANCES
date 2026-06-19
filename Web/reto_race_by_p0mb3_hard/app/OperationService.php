<?php

declare(strict_types=1);

final class OperationService
{
    public function __construct(
        private PDO $pdo,
        private AccountService $accountService,
        private TransferService $transferService,
        private ChallengeStateService $challengeStateService,
        private array $config
    ) {
    }

    public function createPendingOperation(int $amount, string $destinationAlias, string $concept): array
    {
        $limit = (int) $this->config['challenge']['max_transfer_amount'];
        if ($amount < 1 || $amount > $limit) {
            return ['ok' => false, 'message' => 'El monto debe estar entre $1 y ' . money($limit) . '.'];
        }

        $destinationAlias = trim($destinationAlias);
        if ($destinationAlias === '') {
            $destinationAlias = (string) $this->config['challenge']['destination_alias'];
        }

        $concept = trim($concept);
        if ($concept === '') {
            $concept = 'Movimiento diferido';
        }

        $account = $this->accountService->findByCode((string) $this->config['challenge']['account_code']);
        if (!$account || $account['status'] !== 'active') {
            return ['ok' => false, 'message' => 'La operación no se encuentra disponible para este operador.'];
        }

        if ($this->countOperationsInWindow() >= (int) $this->config['challenge']['max_operations_per_window']) {
            return ['ok' => false, 'message' => 'La ventana actual no admite nuevas solicitudes.'];
        }

        $operationId = operationPublicId();
        $token = transferToken();
        $tokenHash = hash('sha256', $token);
        $ttlSeconds = (int) $this->config['challenge']['token_ttl_seconds'];

        $stmt = $this->pdo->prepare(
            'INSERT INTO bank_operations (operation_id, account_uid, amount, destination_alias, concept, token_hash, status, expires_at)
             VALUES (:operation_id, :account_uid, :amount, :destination_alias, :concept, :token_hash, :status, DATE_ADD(NOW(), INTERVAL ' . $ttlSeconds . ' SECOND))'
        );
        $stmt->execute([
            'operation_id' => $operationId,
            'account_uid' => (int) $account['uid'],
            'amount' => $amount,
            'destination_alias' => substr($destinationAlias, 0, 120),
            'concept' => substr($concept, 0, 180),
            'token_hash' => $tokenHash,
            'status' => 'pending',
        ]);

        $this->transferService->insertAudit('operation_prepare', 'Solicitud preparada para revisión operativa');

        return [
            'ok' => true,
            'operation_id' => $operationId,
            'transfer_token' => $token,
            'amount' => $amount,
            'destination_alias' => substr($destinationAlias, 0, 120),
            'concept' => substr($concept, 0, 180),
            'ttl_seconds' => $ttlSeconds,
        ];
    }

    public function getOperation(string $operationId): ?array
    {
        $stmt = $this->pdo->prepare('SELECT * FROM bank_operations WHERE operation_id = :operation_id LIMIT 1');
        $stmt->execute(['operation_id' => $operationId]);
        $operation = $stmt->fetch();
        return $operation ?: null;
    }

    public function verifyToken(array $operation, string $token): bool
    {
        return hash_equals((string) $operation['token_hash'], hash('sha256', $token));
    }

    public function expireOldOperations(): void
    {
        $stmt = $this->pdo->prepare("UPDATE bank_operations SET status = 'expired' WHERE status = 'pending' AND expires_at IS NOT NULL AND expires_at < NOW()");
        $stmt->execute();
    }

    public function countOperationsInWindow(): int
    {
        $state = $this->challengeStateService->state();
        $startedAt = $state['window_started_at'] ?? date('Y-m-d H:i:s');
        $stmt = $this->pdo->prepare('SELECT COUNT(*) FROM bank_operations WHERE created_at >= :started_at');
        $stmt->execute(['started_at' => $startedAt]);
        return (int) $stmt->fetchColumn();
    }

    public function clear(): void
    {
        $this->pdo->exec('DELETE FROM bank_operations');
    }

    public function confirmOperationVulnerable(string $operationId, string $token): array
    {
        $this->expireOldOperations();
        $operation = $this->getOperation($operationId);
        if (!$operation) {
            return ['ok' => false, 'message' => 'Operación no disponible.'];
        }

        if ((string) $operation['status'] !== 'pending') {
            return ['ok' => false, 'message' => 'La autorización no se encuentra disponible.'];
        }

        if (!$this->verifyToken($operation, $token)) {
            return ['ok' => false, 'message' => 'La autorización no pudo ser validada.'];
        }

        if (!empty($operation['expires_at']) && strtotime((string) $operation['expires_at']) < time()) {
            $this->markExpired($operationId);
            return ['ok' => false, 'message' => 'La autorización operativa expiró.'];
        }

        $balance = $this->accountService->getBalance((int) $operation['account_uid']);
        $amount = (int) $operation['amount'];
        if ($balance < $amount) {
            $this->markRejected($operationId);
            return ['ok' => false, 'message' => 'Fondos no disponibles para el lote solicitado.'];
        }

        $newBalance = $balance - $amount;

        usleep((int) $this->config['challenge']['confirmation_window_us']);

        $reference = $this->transferService->insertApprovedTransfer(
            (int) $operation['account_uid'],
            (string) $operation['operation_id'],
            $amount,
            (string) $operation['concept'],
            (string) $operation['destination_alias']
        );
        $this->accountService->setBalance((int) $operation['account_uid'], $newBalance);

        usleep((int) $this->config['challenge']['confirmation_window_us']);

        $this->markApproved($operationId);

        $this->transferService->insertAudit('operation_confirm', 'Operación derivada al lote interno');

        return [
            'ok' => true,
            'message' => 'La operación fue derivada al lote interno.',
            'reference' => $reference,
            'account_uid' => (int) $operation['account_uid'],
            'operation_id' => (string) $operation['operation_id'],
        ];
    }

    private function markExpired(string $operationId): void
    {
        $stmt = $this->pdo->prepare("UPDATE bank_operations SET status = 'expired' WHERE operation_id = :operation_id");
        $stmt->execute(['operation_id' => $operationId]);
    }

    private function markRejected(string $operationId): void
    {
        $stmt = $this->pdo->prepare("UPDATE bank_operations SET status = 'rejected' WHERE operation_id = :operation_id");
        $stmt->execute(['operation_id' => $operationId]);
    }

    private function markApproved(string $operationId): void
    {
        $stmt = $this->pdo->prepare("UPDATE bank_operations SET status = 'approved', approved_at = NOW() WHERE operation_id = :operation_id");
        $stmt->execute(['operation_id' => $operationId]);
    }
}
