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

function operationPublicId(): string
{
    return 'OP-' . strtoupper(bin2hex(random_bytes(8)));
}

function transferToken(): string
{
    return rtrim(strtr(base64_encode(random_bytes(24)), '+/', '-_'), '=');
}

function incidentReference(): string
{
    return 'HV-' . strtoupper(bin2hex(random_bytes(3)));
}

function batchPublicId(): string
{
    return 'LT-' . strtoupper(bin2hex(random_bytes(6)));
}

function batchCloseToken(): string
{
    return rtrim(strtr(base64_encode(random_bytes(24)), '+/', '-_'), '=');
}

function settlementReference(): string
{
    return 'ST-' . strtoupper(bin2hex(random_bytes(6)));
}

function requestReference(): string
{
    return 'RQ-' . strtoupper(bin2hex(random_bytes(6)));
}

function operatorWindowReference(): string
{
    return 'WND-' . strtoupper(bin2hex(random_bytes(5)));
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

    return 'CODIGO_NO_CONFIGURADO';
}

function redirectTo(string $path): never
{
    header('Location: ' . $path, true, 303);
    exit;
}
