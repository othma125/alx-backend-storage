DELIMITER //
CREATE TRIGGER before_user_update
BEFORE UPDATE ON users
FOR EACH ROW
BEGIN
    IF OLD.email <> NEW.email THEN
        SET NEW.valid_email = 0;
    -- ELSE
    --     SET NEW.valid_email = OLD.valid_email;
    END IF;
END;
//
DELIMITER ;
