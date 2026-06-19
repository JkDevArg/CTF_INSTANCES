<?php

declare(strict_types=1);

final class ChallengeStateService
{
    public function __construct(
        private PDO $pdo,
        private AccountService $accountService,
        private array $config
    ) {
    }

    public function ensureActiveWindow(): bool
    {
        $this->ensureRow();
        $state = $this->state();
        if (!$state || strtotime((string) $state['window_expires_at']) <= time()) {
            $this->reset('Ventana operativa reiniciada');
            return true;
        }
        return false;
    }

    public function reset(string $message = 'Entorno restaurado por solicitud operativa'): void
    {
        $seconds = (int) $this->config['challenge']['window_seconds'];
        $initialBalance = (int) $this->config['challenge']['initial_balance'];
        $windowId = operatorWindowReference();

        $this->pdo->beginTransaction();
        try {
            $this->pdo->exec('DELETE FROM incident_cases');
            $this->pdo->exec('DELETE FROM settlement_entries');
            $this->pdo->exec('DELETE FROM bank_batch_operations');
            $this->pdo->exec('DELETE FROM bank_batches');
            $this->pdo->exec('DELETE FROM bank_transfers');
            $this->pdo->exec('DELETE FROM bank_operations');
            $this->pdo->exec('DELETE FROM audit_events');
            $this->accountService->resetBalances($initialBalance);
            $stmt = $this->pdo->prepare(
                'UPDATE challenge_state
                 SET window_started_at = NOW(),
                     window_expires_at = DATE_ADD(NOW(), INTERVAL ' . $seconds . ' SECOND),
                     integrity_status = :integrity_status,
                     unlocked = :unlocked,
                     incident_id = :incident_id,
                     unlocked_at = :unlocked_at,
                     unlock_reason = :unlock_reason,
                     last_reset_reason = :last_reset_reason,
                     operator_window_id = :operator_window_id,
                     active_batch_id = :active_batch_id,
                     active_incident_id = :active_incident_id,
                     control_digit = :control_digit
                 WHERE id = 1'
            );
            $stmt->execute([
                'integrity_status' => 'Normal',
                'unlocked' => 0,
                'incident_id' => null,
                'unlocked_at' => null,
                'unlock_reason' => null,
                'last_reset_reason' => $message,
                'operator_window_id' => $windowId,
                'active_batch_id' => null,
                'active_incident_id' => null,
                'control_digit' => null,
            ]);
            $audit = $this->pdo->prepare('INSERT INTO audit_events (event_type, event_message, metadata_json) VALUES (:event_type, :event_message, :metadata_json)');
            $audit->execute([
                'event_type' => 'system',
                'event_message' => $message,
                'metadata_json' => null,
            ]);
            $this->pdo->commit();
        } catch (Throwable $e) {
            $this->pdo->rollBack();
            throw $e;
        }
    }

    public function secondsRemaining(): int
    {
        $stmt = $this->pdo->query('SELECT GREATEST(TIMESTAMPDIFF(SECOND, NOW(), window_expires_at), 0) FROM challenge_state WHERE id = 1');
        return (int) $stmt->fetchColumn();
    }

    public function state(): array
    {
        $stmt = $this->pdo->query('SELECT * FROM challenge_state WHERE id = 1');
        return $stmt->fetch() ?: [];
    }

    public function currentWindowId(): string
    {
        $state = $this->state();
        $windowId = $state['operator_window_id'] ?? null;
        if (!is_string($windowId) || $windowId === '') {
            $windowId = operatorWindowReference();
            $stmt = $this->pdo->prepare('UPDATE challenge_state SET operator_window_id = :operator_window_id WHERE id = 1');
            $stmt->execute(['operator_window_id' => $windowId]);
        }
        return $windowId;
    }

    public function generateResetToken(): string
    {
        $state = $this->state();
        $payload = ($state['window_started_at'] ?? '') . '|' . ($state['window_expires_at'] ?? '') . '|1';
        return hash_hmac('sha256', $payload, (string) $this->config['challenge']['action_secret']);
    }

    public function isValidResetToken(string $token): bool
    {
        return hash_equals($this->generateResetToken(), $token);
    }

    public function updateBatchState(?string $batchId, ?string $integrityStatus = null): void
    {
        $stmt = $this->pdo->prepare(
            'UPDATE challenge_state SET active_batch_id = :active_batch_id, integrity_status = COALESCE(:integrity_status, integrity_status) WHERE id = 1'
        );
        $stmt->execute([
            'active_batch_id' => $batchId,
            'integrity_status' => $integrityStatus,
        ]);
    }

    public function updateIncidentState(?string $incidentId, ?string $controlDigit, string $integrityStatus = 'Revisión requerida'): void
    {
        $stmt = $this->pdo->prepare(
            'UPDATE challenge_state
             SET active_incident_id = :active_incident_id,
                 control_digit = :control_digit,
                 integrity_status = :integrity_status
             WHERE id = 1'
        );
        $stmt->execute([
            'active_incident_id' => $incidentId,
            'control_digit' => $controlDigit,
            'integrity_status' => $integrityStatus,
        ]);
    }

    private function ensureRow(): void
    {
        $stmt = $this->pdo->query('SELECT COUNT(*) FROM challenge_state WHERE id = 1');
        if ((int) $stmt->fetchColumn() === 0) {
            $seconds = (int) $this->config['challenge']['window_seconds'];
            $windowId = operatorWindowReference();
            $insert = $this->pdo->prepare(
                'INSERT INTO challenge_state (
                    id, window_started_at, window_expires_at, integrity_status, unlocked, last_reset_reason,
                    operator_window_id, active_batch_id, active_incident_id, control_digit
                 )
                 VALUES (
                    1, NOW(), DATE_ADD(NOW(), INTERVAL ' . $seconds . ' SECOND), :integrity_status, :unlocked, :last_reset_reason,
                    :operator_window_id, :active_batch_id, :active_incident_id, :control_digit
                 )'
            );
            $insert->execute([
                'integrity_status' => 'Normal',
                'unlocked' => 0,
                'last_reset_reason' => 'Inicialización',
                'operator_window_id' => $windowId,
                'active_batch_id' => null,
                'active_incident_id' => null,
                'control_digit' => null,
            ]);
        }
    }
}
