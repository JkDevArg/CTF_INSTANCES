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

return [
    'app_name' => (string) env_value('APP_NAME', 'Banco HACKL4BS Vault'),
    'verbose_errors' => filter_var(env_value('APP_DEBUG', false), FILTER_VALIDATE_BOOLEAN),
    'db' => [
        'host' => (string) env_value('DB_HOST', '127.0.0.1'),
        'port' => (int) env_value('DB_PORT', 3306),
        'name' => (string) env_value('DB_NAME', 'reto'),
        'user' => (string) env_value('DB_USER', 'reto_user'),
        'password' => (string) env_value('DB_PASSWORD', 'reto_password'),
    ],
    'challenge' => [
        'account_code' => 'HV001',
        'destination_alias' => 'vault.reserve@hackl4bs',
        'initial_balance' => (int) env_value('INITIAL_BALANCE', 20000),
        'max_transfer_amount' => (int) env_value('MAX_TRANSFER_AMOUNT', 100),
        'window_seconds' => (int) env_value('WINDOW_SECONDS', 60),
        'unlock_drift' => (int) env_value('UNLOCK_DRIFT', 1200),
        'min_approved_transfers' => (int) env_value('MIN_APPROVED_TRANSFERS', 8),
        'delay_min_us' => (int) env_value('TRANSFER_DELAY_MIN_US', 80000),
        'delay_max_us' => (int) env_value('TRANSFER_DELAY_MAX_US', 220000),
    ],
    'flag' => (string) env_value('CTF_FLAG', ''),
];
