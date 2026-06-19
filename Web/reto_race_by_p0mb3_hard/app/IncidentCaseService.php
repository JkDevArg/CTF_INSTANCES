<?php

declare(strict_types=1);

final class IncidentCaseService
{
    public function __construct(
        private PDO $pdo,
        private SettlementService $settlementService,
        private BatchService $batchService,
        private ChallengeStateService $challengeStateService,
        private array $config
    ) {
    }

    public function evaluateBatchIncident(string $batchId): ?array
    {
        $batch = $this->batchService->getBatch($batchId);
        if (!$batch || (string) $batch['status'] !== 'closed') {
            return null;
        }

        $count = $this->settlementService->getSettlementCount($batchId);
        $settlementTotal = $this->settlementService->getSettlementTotal($batchId);
        $approvedTotal = $this->batchService->calculateBatchTotal($batchId);
        $drift = $settlementTotal - $approvedTotal;

        if (
            $count < (int) $this->config['challenge']['min_duplicate_settlements'] ||
            $drift < (int) $this->config['challenge']['settlement_unlock_drift']
        ) {
            return null;
        }

        $existing = $this->getCaseByBatchId($batchId);
        if ($existing) {
            return $existing;
        }

        return $this->createIncidentCase($batchId, (string) $batch['operator_window_id'], $approvedTotal, $count);
    }

    public function currentCase(): ?array
    {
        $state = $this->challengeStateService->state();
        $incidentId = $state['active_incident_id'] ?? null;
        if (is_string($incidentId) && $incidentId !== '') {
            $stmt = $this->pdo->prepare('SELECT * FROM incident_cases WHERE incident_id = :incident_id LIMIT 1');
            $stmt->execute(['incident_id' => $incidentId]);
            $row = $stmt->fetch();
            if ($row) {
                return $row;
            }
        }

        $batchId = $state['active_batch_id'] ?? null;
        if (is_string($batchId) && $batchId !== '') {
            return $this->getCaseByBatchId($batchId);
        }

        return null;
    }

    public function hasActiveCase(): bool
    {
        $case = $this->currentCase();
        return $case !== null && (string) $case['status'] === 'enabled';
    }

    public function getCaseByBatchId(string $batchId): ?array
    {
        $stmt = $this->pdo->prepare('SELECT * FROM incident_cases WHERE batch_id = :batch_id ORDER BY id DESC LIMIT 1');
        $stmt->execute(['batch_id' => $batchId]);
        $row = $stmt->fetch();
        return $row ?: null;
    }

    public function validateCaseAccess(string $batchReference, string $controlDigit): ?array
    {
        $case = $this->currentCase();
        if (!$case) {
            return null;
        }

        $state = $this->challengeStateService->state();
        if ((string) ($state['integrity_status'] ?? 'Normal') !== 'Revisión requerida') {
            return null;
        }

        if (!hash_equals((string) $case['batch_id'], $batchReference)) {
            return null;
        }

        if (!hash_equals((string) $case['control_digit'], $controlDigit)) {
            return null;
        }

        if (!hash_equals((string) $case['operator_window_id'], $this->challengeStateService->currentWindowId())) {
            return null;
        }

        if ((string) $case['status'] !== 'enabled') {
            return null;
        }

        return $case;
    }

    public function auditCode(): string
    {
        return loadFlag($this->config);
    }

    public function calculateControlDigit(string $batchId, int $batchTotal, int $settlementCount): string
    {
        $suffix = $this->batchNumericSuffix($batchId);
        $value = ($batchTotal + $settlementCount + $suffix) % 97;
        return str_pad((string) $value, 2, '0', STR_PAD_LEFT);
    }

    public function batchNumericSuffix(string $batchId): int
    {
        $suffix = substr($batchId, -4);
        if ($suffix === false || $suffix === '') {
            return 0;
        }

        return hexdec($suffix);
    }

    private function createIncidentCase(string $batchId, string $windowId, int $approvedTotal, int $settlementCount): array
    {
        $incidentId = incidentReference();
        $controlDigit = $this->calculateControlDigit($batchId, $approvedTotal, $settlementCount);

        $stmt = $this->pdo->prepare(
            'INSERT INTO incident_cases (incident_id, batch_id, operator_window_id, control_digit, status)
             VALUES (:incident_id, :batch_id, :operator_window_id, :control_digit, :status)'
        );

        try {
            $stmt->execute([
                'incident_id' => $incidentId,
                'batch_id' => $batchId,
                'operator_window_id' => $windowId,
                'control_digit' => $controlDigit,
                'status' => 'enabled',
            ]);
        } catch (PDOException $e) {
            if ($e->getCode() === '23000') {
                $existing = $this->getCaseByBatchId($batchId);
                if ($existing) {
                    return $existing;
                }
            }
            throw $e;
        }

        $this->challengeStateService->updateIncidentState($incidentId, $controlDigit, 'Revisión requerida');

        return [
            'incident_id' => $incidentId,
            'batch_id' => $batchId,
            'operator_window_id' => $windowId,
            'control_digit' => $controlDigit,
            'status' => 'enabled',
        ];
    }
}
