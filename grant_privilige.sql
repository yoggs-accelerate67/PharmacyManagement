-- Grant SELECT privilege to a user for the drugs table
GRANT SELECT ON drugs TO 'tes1'@'127.0.0.1';

-- Revoke INSERT privilege from a user for the drugs table
REVOKE INSERT ON drugs FROM 'root'@'localhost';

-- Revoke UPDATE privilege from a user for the drugs table
REVOKE UPDATE ON drugs FROM 'root'@'localhost';

-- Revoke DELETE privilege from a user for the drugs table
REVOKE DELETE ON drugs FROM 'root'@'localhost';
