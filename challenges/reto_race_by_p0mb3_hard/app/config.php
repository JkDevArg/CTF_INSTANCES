<?php

declare(strict_types=1);

function env_value(string $key, mixed $default = null): mixed
{
    $value = getenv($key);
    if ($value === false || $value === '') {
        return $default;
    }
    return $value;
}

function env_int(string $key, int $default): int
{
    return (int) env_value($key, $default);
}

function env_bool(string $key, bool $default): bool
{
    return filter_var(env_value($key, $default), FILTER_VALIDATE_BOOLEAN);
}

return [
    'app_name' => (string) env_value('APP_NAME', 'Banco HACKL4BS Vault'),
    'verbose_errors' => env_bool('APP_DEBUG', false),
    'db' => [
        'host' => (string) env_value('DB_HOST', '127.0.0.1'),
        'port' => env_int('DB_PORT', 3306),
        'name' => (string) env_value('DB_NAME', 'reto'),
        'user' => (string) env_value('DB_USER', 'reto_user'),
        'password' => (string) env_value('DB_PASSWORD', 'reto_password'),
    ],
    'challenge' => [
        'account_code' => (string) env_value('ACCOUNT_CODE', 'HV-001'),
        'destination_alias' => (string) env_value('DEFAULT_DESTINATION_ALIAS', 'vault.reserve@hackl4bs'),
        'initial_balance' => env_int('INITIAL_BALANCE', 20000),
        'max_transfer_amount' => env_int('MAX_TRANSFER_AMOUNT', 100),
        'window_seconds' => env_int('WINDOW_SECONDS', 60),
        'max_operations_per_window' => env_int('MAX_OPERATIONS_PER_WINDOW', 5),
        'token_ttl_seconds' => env_int('TOKEN_TTL_SECONDS', 15),
        'unlock_drift' => env_int('UNLOCK_DRIFT', 1200),
        'min_duplicate_approvals' => env_int('MIN_DUPLICATE_APPROVALS', 8),
        'confirmation_window_us' => env_int('CONFIRMATION_WINDOW_US', 1200000),
        'batch_close_window_us' => env_int('BATCH_CLOSE_WINDOW_US', 1200000),
        'settlement_unlock_drift' => env_int('SETTLEMENT_UNLOCK_DRIFT', 1200),
        'min_duplicate_settlements' => env_int('MIN_DUPLICATE_SETTLEMENTS', 2),
        'max_batch_operations' => env_int('MAX_BATCH_OPERATIONS', 5),
        'action_secret' => (string) env_value('APP_ACTION_SECRET', 'vault-action-secret'),
    ],
    'flag' => (string) env_value('CTF_FLAG', ''),
];
