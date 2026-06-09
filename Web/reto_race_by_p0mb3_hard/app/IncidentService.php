<?php

declare(strict_types=1);

final class IncidentService
{
    public function __construct(
        private PDO $pdo,
        private AccountService $accountService,
        private TransferService $transferService,
        private array $config
    ) {
    }

    public function evaluateUnlock(?int $accountUid = null): bool
    {
        $accountUid ??= $this->accountUid();
        $account = $this->accountService->findById($accountUid);
        if (!$account) {
            return false;
        }

        $approvedSum = $this->transferService->sumApproved($accountUid);
        $realDebit = (int) $account['initial_balance'] - (int) $account['balance'];
        $drift = $approvedSum - $realDebit;
        $duplicate = $this->transferService->findDuplicateOperation(
            $accountUid,
            (int) $this->config['challenge']['min_duplicate_approvals']
        );

        if ($drift >= (int) $this->config['challenge']['unlock_drift'] && $duplicate) {
            $this->unlockState((string) $duplicate['operation_id']);
            $this->transferService->insertAudit('integrity', 'El lote fue derivado a revisión operativa');
            return true;
        }

        return $this->isUnlocked();
    }

    public function status(?int $accountUid = null): array
    {
        $state = $this->state();
        return [
            'unlocked' => (bool) ($state['unlocked'] ?? false),
            'label' => $state['integrity_status'] ?? 'Normal',
            'incident_id' => $state['incident_id'] ?? null,
        ];
    }

    public function state(): array
    {
        $stmt = $this->pdo->query('SELECT * FROM challenge_state WHERE id = 1');
        return $stmt->fetch() ?: [];
    }

    public function isUnlocked(): bool
    {
        $state = $this->state();
        return (bool) ($state['unlocked'] ?? false);
    }

    public function currentIncidentId(): ?string
    {
        $state = $this->state();
        $incidentId = $state['incident_id'] ?? null;
        return is_string($incidentId) && $incidentId !== '' ? $incidentId : null;
    }

    public function canShowIncident(string $incidentId): bool
    {
        return $this->isUnlocked() && hash_equals((string) $this->currentIncidentId(), $incidentId);
    }

    public function getAuditCode(): string
    {
        return loadFlag($this->config);
    }

    private function unlockState(string $operationId): void
    {
        if ($this->isUnlocked()) {
            return;
        }

        $incidentId = incidentReference();
        $stmt = $this->pdo->prepare(
            'UPDATE challenge_state
             SET integrity_status = :integrity_status,
                 unlocked = :unlocked,
                 incident_id = :incident_id,
                 unlocked_at = NOW(),
                 unlock_reason = :unlock_reason
             WHERE id = 1 AND unlocked = 0'
        );
        $stmt->execute([
            'integrity_status' => 'Revisión requerida',
            'unlocked' => 1,
            'incident_id' => $incidentId,
            'unlock_reason' => 'Control manual requerido para la operación ' . $operationId,
        ]);
    }

    private function accountUid(): int
    {
        $account = $this->accountService->findByCode((string) $this->config['challenge']['account_code']);
        return (int) ($account['uid'] ?? 0);
    }
}
