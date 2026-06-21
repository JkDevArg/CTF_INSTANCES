<?php

declare(strict_types=1);

final class AccountService
{
    public function __construct(private PDO $pdo)
    {
    }

    public function findByCode(string $code): ?array
    {
        $stmt = $this->pdo->prepare('SELECT * FROM bank_accounts WHERE ucode = :ucode LIMIT 1');
        $stmt->execute(['ucode' => $code]);
        $account = $stmt->fetch();
        return $account ?: null;
    }

    public function findById(int $uid): ?array
    {
        $stmt = $this->pdo->prepare('SELECT * FROM bank_accounts WHERE uid = :uid LIMIT 1');
        $stmt->execute(['uid' => $uid]);
        $account = $stmt->fetch();
        return $account ?: null;
    }

    public function getBalance(int $uid): int
    {
        $stmt = $this->pdo->prepare('SELECT balance FROM bank_accounts WHERE uid = :uid');
        $stmt->execute(['uid' => $uid]);
        return (int) $stmt->fetchColumn();
    }

    public function setBalance(int $uid, int $balance): void
    {
        $stmt = $this->pdo->prepare('UPDATE bank_accounts SET balance = :balance WHERE uid = :uid');
        $stmt->execute(['balance' => $balance, 'uid' => $uid]);
    }

    public function resetBalances(int $initialBalance): void
    {
        $stmt = $this->pdo->prepare('UPDATE bank_accounts SET balance = :balance, initial_balance = :initial_balance');
        $stmt->execute(['balance' => $initialBalance, 'initial_balance' => $initialBalance]);
    }
}
