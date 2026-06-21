<?php

declare(strict_types=1);

final class ChallengeStateService
{
    public function __construct(
        private PDO $pdo,
        private AccountService $accountService,
        private TransferService $transferService,
        private array $config
    ) {
    }

    public function ensureActiveWindow(): bool
    {
        $this->ensureRow();
        $stmt = $this->pdo->query('SELECT expires_at, NOW() AS now_value FROM challenge_state WHERE id = 1');
        $state = $stmt->fetch();
        if (!$state || strtotime((string) $state['expires_at']) <= strtotime((string) $state['now_value'])) {
            $this->reset('Ventana operativa reiniciada');
            return true;
        }
        return false;
    }

    public function reset(string $message = 'Entorno restaurado por solicitud operativa'): void
    {
        $seconds = (int) $this->config['challenge']['window_seconds'];
        $initialBalance = (int) $this->config['challenge']['initial_balance'];

        $this->pdo->beginTransaction();
        try {
            $this->transferService->clear();
            $this->pdo->exec('DELETE FROM audit_events');
            $this->accountService->resetBalances($initialBalance);
            $stmt = $this->pdo->prepare(
                'UPDATE challenge_state
                 SET started_at = NOW(), expires_at = DATE_ADD(NOW(), INTERVAL ' . $seconds . ' SECOND), unlocked_at = NULL, unlock_reason = NULL
                 WHERE id = 1'
            );
            $stmt->execute();
            $this->transferService->insertAudit('system', 'info', $message);
            $this->pdo->commit();
        } catch (Throwable $e) {
            $this->pdo->rollBack();
            throw $e;
        }
    }

    public function secondsRemaining(): int
    {
        $stmt = $this->pdo->query('SELECT GREATEST(TIMESTAMPDIFF(SECOND, NOW(), expires_at), 0) FROM challenge_state WHERE id = 1');
        return (int) $stmt->fetchColumn();
    }

    public function state(): array
    {
        $stmt = $this->pdo->query('SELECT * FROM challenge_state WHERE id = 1');
        return $stmt->fetch() ?: [];
    }

    private function ensureRow(): void
    {
        $stmt = $this->pdo->query('SELECT COUNT(*) FROM challenge_state WHERE id = 1');
        if ((int) $stmt->fetchColumn() === 0) {
            $seconds = (int) $this->config['challenge']['window_seconds'];
            $insert = $this->pdo->prepare('INSERT INTO challenge_state (id, expires_at) VALUES (1, DATE_ADD(NOW(), INTERVAL ' . $seconds . ' SECOND))');
            $insert->execute();
        }
    }
}
