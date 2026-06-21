CREATE DATABASE IF NOT EXISTS reto CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE reto;

DROP TABLE IF EXISTS incident_cases;
DROP TABLE IF EXISTS settlement_entries;
DROP TABLE IF EXISTS bank_batch_operations;
DROP TABLE IF EXISTS bank_batches;
DROP TABLE IF EXISTS audit_events;
DROP TABLE IF EXISTS bank_transfers;
DROP TABLE IF EXISTS bank_operations;
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

CREATE TABLE bank_operations (
  id INT NOT NULL AUTO_INCREMENT,
  operation_id VARCHAR(64) NOT NULL,
  account_uid INT NOT NULL,
  amount INT NOT NULL,
  destination_alias VARCHAR(120) NOT NULL,
  concept VARCHAR(180) NOT NULL,
  token_hash VARCHAR(255) NOT NULL,
  status ENUM('pending', 'approved', 'rejected', 'expired') NOT NULL DEFAULT 'pending',
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  expires_at TIMESTAMP NULL,
  approved_at TIMESTAMP NULL,
  PRIMARY KEY (id),
  UNIQUE KEY uq_bank_operations_operation_id (operation_id),
  KEY idx_bank_operations_status (status),
  KEY idx_bank_operations_account_uid (account_uid),
  CONSTRAINT fk_bank_operations_account
    FOREIGN KEY (account_uid) REFERENCES bank_accounts(uid)
    ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE bank_transfers (
  id INT NOT NULL AUTO_INCREMENT,
  account_uid INT NOT NULL,
  operation_id VARCHAR(64) DEFAULT NULL,
  reference_code VARCHAR(64) NOT NULL,
  reconciliation_ref VARCHAR(64) DEFAULT NULL,
  destination_alias VARCHAR(120) NOT NULL,
  amount INT NOT NULL,
  status VARCHAR(20) NOT NULL DEFAULT 'approved',
  channel VARCHAR(40) NOT NULL DEFAULT 'private-vault',
  concept VARCHAR(180) DEFAULT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uq_bank_transfers_reference (reference_code),
  KEY idx_bank_transfers_account_status (account_uid, status),
  KEY idx_bank_transfers_operation_id (operation_id),
  CONSTRAINT fk_bank_transfers_account
    FOREIGN KEY (account_uid) REFERENCES bank_accounts(uid)
    ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE challenge_state (
  id INT NOT NULL PRIMARY KEY,
  window_started_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  window_expires_at TIMESTAMP NULL,
  integrity_status VARCHAR(40) NOT NULL DEFAULT 'Normal',
  unlocked TINYINT(1) NOT NULL DEFAULT 0,
  incident_id VARCHAR(64) DEFAULT NULL,
  unlocked_at TIMESTAMP NULL,
  unlock_reason VARCHAR(120) DEFAULT NULL,
  last_reset_reason VARCHAR(180) DEFAULT NULL,
  operator_window_id VARCHAR(64) DEFAULT NULL,
  active_batch_id VARCHAR(64) DEFAULT NULL,
  active_incident_id VARCHAR(64) DEFAULT NULL,
  control_digit VARCHAR(16) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE bank_batches (
  id INT NOT NULL AUTO_INCREMENT,
  batch_id VARCHAR(64) NOT NULL,
  status ENUM('open','ready_to_close','closed','observed') NOT NULL DEFAULT 'open',
  operator_window_id VARCHAR(64) NOT NULL,
  close_token_hash VARCHAR(128) NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  ready_at TIMESTAMP NULL,
  closed_at TIMESTAMP NULL,
  PRIMARY KEY (id),
  UNIQUE KEY uq_bank_batches_batch_id (batch_id),
  KEY idx_bank_batches_status (status),
  KEY idx_bank_batches_window (operator_window_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE bank_batch_operations (
  id INT NOT NULL AUTO_INCREMENT,
  batch_id VARCHAR(64) NOT NULL,
  operation_id VARCHAR(64) NOT NULL,
  amount INT NOT NULL,
  status ENUM('attached','observed') NOT NULL DEFAULT 'attached',
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uniq_batch_operation (batch_id, operation_id),
  KEY idx_batch_operation_batch (batch_id),
  KEY idx_batch_operation_operation (operation_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE settlement_entries (
  id INT NOT NULL AUTO_INCREMENT,
  settlement_id VARCHAR(64) NOT NULL,
  batch_id VARCHAR(64) NOT NULL,
  amount INT NOT NULL,
  source_request_id VARCHAR(64) NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uq_settlement_entries_settlement_id (settlement_id),
  KEY idx_settlement_batch (batch_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE incident_cases (
  id INT NOT NULL AUTO_INCREMENT,
  incident_id VARCHAR(64) NOT NULL,
  batch_id VARCHAR(64) NOT NULL,
  operator_window_id VARCHAR(64) NOT NULL,
  control_digit VARCHAR(16) NOT NULL,
  status ENUM('pending','enabled','closed') NOT NULL DEFAULT 'pending',
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uq_incident_cases_incident_id (incident_id),
  UNIQUE KEY uq_incident_cases_batch (batch_id),
  KEY idx_incident_cases_batch (batch_id),
  KEY idx_incident_cases_window (operator_window_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE audit_events (
  id INT NOT NULL AUTO_INCREMENT,
  event_type VARCHAR(60) NOT NULL,
  event_message VARCHAR(255) NOT NULL,
  metadata_json JSON DEFAULT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  KEY idx_audit_events_type (event_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO bank_accounts
  (uid, ucode, account_number, balance, initial_balance, uname, status)
VALUES
  (1, 'HV-001', 'HL4B-2026-VAULT-001', 20000, 20000, 'Operador HV-001', 'active');

INSERT INTO challenge_state (
  id, window_expires_at, integrity_status, unlocked, last_reset_reason, operator_window_id,
  active_batch_id, active_incident_id, control_digit
)
VALUES (
  1, DATE_ADD(NOW(), INTERVAL 60 SECOND), 'Normal', 0, 'Inicialización', 'WND-BOOTSTRAP',
  NULL, NULL, NULL
);

INSERT INTO audit_events (event_type, event_message, metadata_json)
VALUES ('system', 'Canal privado inicializado', NULL);
