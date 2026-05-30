CREATE DATABASE IF NOT EXISTS dvwa;
USE dvwa;
CREATE TABLE IF NOT EXISTS ctf_flags (
    id INT AUTO_INCREMENT PRIMARY KEY,
    flag_name VARCHAR(100),
    flag_value VARCHAR(200),
    hint TEXT
);
INSERT INTO ctf_flags (flag_name, flag_value, hint) VALUES
('flag1_sqli', 'FLAG{sql_1nj3ct10n_m4st3r_2024}', 'Extraída via UNION SELECT desde ctf_flags'),
('flag1_bonus','FLAG{b0nus_bl1nd_sqli}','Requiere blind SQLi para extraer este valor');
