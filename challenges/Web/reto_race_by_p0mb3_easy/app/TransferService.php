<?php

declare(strict_types=1);

final class TransferService
{
    public function __construct(
        private PDO $pdo,
        private AccountService $accountService,
        private array $config
    ) {
    }

    public function executeTransfer(int $amount, string $concept, string $destinationAlias, ReconciliationService $reconciliationService): array
    {
        $limit = (int) $this->config['challenge']['max_transfer_amount'];
        if ($amount < 1 || $amount > $limit) {
            return ['ok' => false, 'message' => 'El monto debe estar entre $1 y ' . money($limit) . '.'];
        }

        $account = $this->accountService->findByCode((string) $this->config['challenge']['account_code']);
        if (!$account || $account['status'] !== 'active') {
            return ['ok' => false, 'message' => 'La operación no pudo ser procesada por el canal privado.'];
        }

        $balance = $this->accountService->getBalance((int) $account['uid']);
        if ($amount > $balance) {
            return ['ok' => false, 'message' => 'Fondos insuficientes para completar la operación.'];
        }

        usleep(random_int(
            (int) $this->config['challenge']['delay_min_us'],
            (int) $this->config['challenge']['delay_max_us']
        ));

        $newBalance = $balance - $amount;
        $this->accountService->setBalance((int) $account['uid'], $newBalance);

        $reference = $this->insertApprovedTransfer((int) $account['uid'], $amount, $concept, $destinationAlias);
        $this->insertAudit('transfer', 'info', 'Transferencia registrada en canal privado');
        $reconciliationService->checkUnlockCondition((int) $account['uid']);

        return ['ok' => true, 'message' => 'Transferencia aprobada. Referencia interna: ' . $reference, 'reference' => $reference];
    }

    public function insertApprovedTransfer(int $accountUid, int $amount, string $concept, string $destinationAlias): string
    {
        $reference = referenceCode();
        $stmt = $this->pdo->prepare(
            'INSERT INTO bank_transfers (account_uid, reference_code, destination_alias, amount, status, channel, concept)
             VALUES (:account_uid, :reference_code, :destination_alias, :amount, :status, :channel, :concept)'
        );
        $stmt->execute([
            'account_uid' => $accountUid,
            'reference_code' => $reference,
            'destination_alias' => $destinationAlias,
            'amount' => $amount,
            'status' => 'approved',
            'channel' => 'private-vault',
            'concept' => substr($concept, 0, 120),
        ]);
        return $reference;
    }

    public function latest(int $accountUid, int $limit = 8): array
    {
        $stmt = $this->pdo->prepare(
            'SELECT reference_code, destination_alias, amount, status, concept, created_at
             FROM bank_transfers
             WHERE account_uid = :account_uid
             ORDER BY id DESC
             LIMIT ' . max(1, min(25, $limit))
        );
        $stmt->execute(['account_uid' => $accountUid]);
        return $stmt->fetchAll();
    }

    public function sumApproved(int $accountUid): int
    {
        $stmt = $this->pdo->prepare("SELECT COALESCE(SUM(amount), 0) FROM bank_transfers WHERE account_uid = :account_uid AND status = 'approved'");
        $stmt->execute(['account_uid' => $accountUid]);
        return (int) $stmt->fetchColumn();
    }

    public function countApproved(int $accountUid): int
    {
        $stmt = $this->pdo->prepare("SELECT COUNT(*) FROM bank_transfers WHERE account_uid = :account_uid AND status = 'approved'");
        $stmt->execute(['account_uid' => $accountUid]);
        return (int) $stmt->fetchColumn();
    }

    public function clear(): void
    {
        $this->pdo->exec('DELETE FROM bank_transfers');
    }

    public function insertAudit(string $type, string $severity, string $message): void
    {
        $stmt = $this->pdo->prepare('INSERT INTO audit_events (event_type, severity, message) VALUES (:event_type, :severity, :message)');
        $stmt->execute(['event_type' => $type, 'severity' => $severity, 'message' => $message]);
    }
}
