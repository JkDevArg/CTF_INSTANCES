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

    public function insertApprovedTransfer(
        int $accountUid,
        ?string $operationId,
        int $amount,
        string $concept,
        string $destinationAlias,
        ?string $reconciliationRef = null
    ): string {
        $reference = referenceCode();
        $stmt = $this->pdo->prepare(
            'INSERT INTO bank_transfers (account_uid, operation_id, reference_code, reconciliation_ref, destination_alias, amount, status, channel, concept)
             VALUES (:account_uid, :operation_id, :reference_code, :reconciliation_ref, :destination_alias, :amount, :status, :channel, :concept)'
        );
        $stmt->execute([
            'account_uid' => $accountUid,
            'operation_id' => $operationId,
            'reference_code' => $reference,
            'reconciliation_ref' => $reconciliationRef,
            'destination_alias' => $destinationAlias,
            'amount' => $amount,
            'status' => 'approved',
            'channel' => 'private-vault',
            'concept' => substr($concept, 0, 180),
        ]);
        return $reference;
    }

    public function latest(int $accountUid, int $limit = 8): array
    {
        $stmt = $this->pdo->prepare(
            'SELECT reference_code, operation_id, destination_alias, amount, status, concept, created_at
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


    public function countTransfersForOperation(string $operationId): int
    {
        $stmt = $this->pdo->prepare("SELECT COUNT(*) FROM bank_transfers WHERE operation_id = :operation_id AND status = 'approved'");
        $stmt->execute(['operation_id' => $operationId]);
        return (int) $stmt->fetchColumn();
    }

    public function findDuplicateOperation(int $accountUid, int $minimumDuplicates): ?array
    {
        $stmt = $this->pdo->prepare(
            'SELECT operation_id, COUNT(*) AS approvals
             FROM bank_transfers
             WHERE account_uid = :account_uid AND status = :status AND operation_id IS NOT NULL
             GROUP BY operation_id
             HAVING COUNT(*) >= :minimum_duplicates
             ORDER BY approvals DESC, operation_id ASC
             LIMIT 1'
        );
        $stmt->bindValue('account_uid', $accountUid, PDO::PARAM_INT);
        $stmt->bindValue('status', 'approved', PDO::PARAM_STR);
        $stmt->bindValue('minimum_duplicates', $minimumDuplicates, PDO::PARAM_INT);
        $stmt->execute();
        $row = $stmt->fetch();
        return $row ?: null;
    }

    public function clear(): void
    {
        $this->pdo->exec('DELETE FROM bank_transfers');
    }

    public function insertAudit(string $type, string $message, ?string $metadataJson = null): void
    {
        $stmt = $this->pdo->prepare('INSERT INTO audit_events (event_type, event_message, metadata_json) VALUES (:event_type, :event_message, :metadata_json)');
        $stmt->execute([
            'event_type' => $type,
            'event_message' => $message,
            'metadata_json' => $metadataJson,
        ]);
    }
}
