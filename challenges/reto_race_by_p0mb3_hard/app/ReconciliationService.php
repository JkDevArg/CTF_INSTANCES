<?php

declare(strict_types=1);

final class ReconciliationService
{
    public function __construct(
        private PDO $pdo,
        private AccountService $accountService,
        private TransferService $transferService,
        private array $config
    ) {
    }

    public function checkUnlockCondition(int $accountUid): bool
    {
        $account = $this->accountService->findById($accountUid);
        if (!$account) {
            return false;
        }

        $approvedTotal = $this->transferService->sumApproved($accountUid);
        $approvedCount = $this->transferService->countApproved($accountUid);
        $realDebit = (int) $account['initial_balance'] - (int) $account['balance'];
        $drift = $approvedTotal - $realDebit;

        if ($drift >= (int) $this->config['challenge']['unlock_drift']
            && $approvedCount >= (int) $this->config['challenge']['min_approved_transfers']
            && !$this->isUnlocked()) {
            $this->markUnlocked('Desvío contable detectado por conciliación interna');
            $this->transferService->insertAudit('integrity', 'warning', 'Desvío contable pendiente de revisión');
            return true;
        }

        return $this->isUnlocked();
    }

    public function status(int $accountUid): array
    {
        $account = $this->accountService->findById($accountUid);
        $approvedTotal = $this->transferService->sumApproved($accountUid);
        $approvedCount = $this->transferService->countApproved($accountUid);
        $realDebit = $account ? ((int) $account['initial_balance'] - (int) $account['balance']) : 0;
        $drift = $approvedTotal - $realDebit;

        return [
            'unlocked' => $this->isUnlocked(),
            'approved_total' => $approvedTotal,
            'approved_count' => $approvedCount,
            'real_debit' => $realDebit,
            'drift' => $drift,
            'label' => $this->isUnlocked() ? 'Revisión requerida' : 'Normal',
        ];
    }

    public function isUnlocked(): bool
    {
        $stmt = $this->pdo->query('SELECT unlocked_at FROM challenge_state WHERE id = 1');
        return (bool) $stmt->fetchColumn();
    }

    public function markUnlocked(string $reason): void
    {
        $stmt = $this->pdo->prepare('UPDATE challenge_state SET unlocked_at = NOW(), unlock_reason = :reason WHERE id = 1 AND unlocked_at IS NULL');
        $stmt->execute(['reason' => $reason]);
    }
}
