<?php

declare(strict_types=1);

require_once __DIR__ . '/helpers.php';
require_once __DIR__ . '/db.php';
require_once __DIR__ . '/AccountService.php';
require_once __DIR__ . '/TransferService.php';
require_once __DIR__ . '/ChallengeStateService.php';
require_once __DIR__ . '/OperationService.php';
require_once __DIR__ . '/IncidentService.php';
require_once __DIR__ . '/BatchService.php';
require_once __DIR__ . '/SettlementService.php';
require_once __DIR__ . '/IncidentCaseService.php';

$config = require __DIR__ . '/config.php';
$pdo = db($config);
$accountService = new AccountService($pdo);
$transferService = new TransferService($pdo, $accountService, $config);
$challengeStateService = new ChallengeStateService($pdo, $accountService, $config);
$operationService = new OperationService($pdo, $accountService, $transferService, $challengeStateService, $config);
$incidentService = new IncidentService($pdo, $accountService, $transferService, $config);
$batchService = new BatchService($pdo, $challengeStateService, $config);
$settlementService = new SettlementService($pdo, $config);
$incidentCaseService = new IncidentCaseService($pdo, $settlementService, $batchService, $challengeStateService, $config);
