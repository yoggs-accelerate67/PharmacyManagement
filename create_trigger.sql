-- Trigger to update last_modified timestamp on drug update
CREATE TRIGGER IF NOT EXISTS update_drug_last_modified
BEFORE INSERT ON drugs
FOR EACH ROW
SET NEW.last_modified = NOW();
