<?php

declare(strict_types=1);

function e(mixed $value): string
{
    return htmlspecialchars((string) $value, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8');
}

function money(int|float $amount): string
{
    return '$' . number_format((float) $amount, 0, ',', '.');
}

function referenceCode(): string
{
    return 'HV-2026-' . strtoupper(bin2hex(random_bytes(3))) . '-' . strtoupper(bin2hex(random_bytes(2)));
}

function loadFlag(array $config): string
{
    if (!empty($config['flag'])) {
        return $config['flag'];
    }

    $path = dirname(__DIR__) . '/private/flag.txt';
    if (is_readable($path)) {
        return trim((string) file_get_contents($path));
    }

    return 'FLAG_NO_CONFIGURADA';
}

function redirectTo(string $path): never
{
    header('Location: ' . $path, true, 303);
    exit;
}
