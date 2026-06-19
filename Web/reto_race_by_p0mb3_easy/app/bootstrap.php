<?php

declare(strict_types=1);

require_once __DIR__ . '/helpers.php';
require_once __DIR__ . '/db.php';
require_once __DIR__ . '/AccountService.php';
require_once __DIR__ . '/TransferService.php';
require_once __DIR__ . '/ReconciliationService.php';
require_once __DIR__ . '/ChallengeStateService.php';

$config = require __DIR__ . '/config.php';
$pdo = db($config);
$accountService = new AccountService($pdo);
$transferService = new TransferService($pdo, $accountService, $config);
$reconciliationService = new ReconciliationService($pdo, $accountService, $transferService, $config);
$challengeStateService = new ChallengeStateService($pdo, $accountService, $transferService, $config);
