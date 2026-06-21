CREATE DATABASE IF NOT EXISTS reto CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE reto;

DROP TABLE IF EXISTS audit_events;
DROP TABLE IF EXISTS bank_transfers;
DROP TABLE IF EXISTS challenge_state;
DROP TABLE IF EXISTS bank_accounts;

CREATE TABLE bank_accounts (
  uid INT NOT NULL AUTO_INCREMENT,
  ucode VARCHAR(32) NOT NULL,
  account_number VARCHAR(64) NOT NULL,
  balance INT NOT NULL DEFAULT 0,
  initial_balance INT NOT NULL DEFAULT 20000,
  uname VARCHAR(80) NOT NULL,
  status VARCHAR(20) NOT NULL DEFAULT 'active',
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (uid),
  UNIQUE KEY uq_bank_accounts_ucode (ucode),
  UNIQUE KEY uq_bank_accounts_number (account_number)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE bank_transfers (
  id INT NOT NULL AUTO_INCREMENT,
  account_uid INT NOT NULL,
  reference_code VARCHAR(64) NOT NULL,
  destination_alias VARCHAR(80) NOT NULL,
  amount INT NOT NULL,
  status VARCHAR(20) NOT NULL DEFAULT 'approved',
  channel VARCHAR(40) NOT NULL DEFAULT 'private-vault',
  concept VARCHAR(120) DEFAULT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uq_bank_transfers_reference (reference_code),
  KEY idx_bank_transfers_account_status (account_uid, status),
  CONSTRAINT fk_bank_transfers_account
    FOREIGN KEY (account_uid) REFERENCES bank_accounts(uid)
    ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE challenge_state (
  id INT NOT NULL PRIMARY KEY,
  started_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  expires_at TIMESTAMP NULL,
  unlocked_at TIMESTAMP NULL,
  unlock_reason VARCHAR(255) DEFAULT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE audit_events (
  id INT NOT NULL AUTO_INCREMENT,
  event_type VARCHAR(50) NOT NULL,
  severity VARCHAR(20) NOT NULL DEFAULT 'info',
  message VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  KEY idx_audit_events_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO bank_accounts
  (uid, ucode, account_number, balance, initial_balance, uname, status)
VALUES
  (1, 'HV001', 'HL4B-2026-VAULT-001', 20000, 20000, 'Operador HV-001', 'active');

INSERT INTO challenge_state (id, expires_at)
VALUES (1, DATE_ADD(NOW(), INTERVAL 60 SECOND));

INSERT INTO audit_events (event_type, severity, message)
VALUES ('system', 'info', 'Canal privado inicializado');
