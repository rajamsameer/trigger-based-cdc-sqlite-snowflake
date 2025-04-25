-- Create main table
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create CDC table to store changes
CREATE TABLE user_changes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    operation TEXT,
    changed_data TEXT,
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Trigger for INSERT
CREATE TRIGGER user_insert_trigger
AFTER INSERT ON users
BEGIN
    INSERT INTO user_changes (operation, changed_data)
    VALUES ('INSERT', json_object('id', NEW.id, 'name', NEW.name, 'email', NEW.email));
END;

-- Trigger for UPDATE
CREATE TRIGGER user_update_trigger
AFTER UPDATE ON users
BEGIN
    INSERT INTO user_changes (operation, changed_data)
    VALUES ('UPDATE', json_object('id', NEW.id, 'name', NEW.name, 'email', NEW.email));
END;  

-- Trigger for DELETE
CREATE TRIGGER user_delete_trigger
AFTER DELETE ON users
BEGIN
    INSERT INTO user_changes (operation, changed_data)
    VALUES ('DELETE', json_object('id', OLD.id, 'name', OLD.name, 'email', OLD.email));
END;



-- -- 1. Create users table first
-- CREATE TABLE IF NOT EXISTS users (
--     id INTEGER PRIMARY KEY AUTOINCREMENT,
--     name TEXT NOT NULL,
--     mail TEXT NOT NULL
-- );

-- -- 2. Create CDC log table
-- CREATE TABLE IF NOT EXISTS cdc_log (
--     id INTEGER PRIMARY KEY AUTOINCREMENT,
--     table_name TEXT,
--     operation TEXT,
--     data TEXT,
--     changed_by TEXT,
--     timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
-- );

-- -- 3. INSERT Trigger
-- CREATE TRIGGER IF NOT EXISTS trg_users_insert
-- AFTER INSERT ON users
-- BEGIN
--     INSERT INTO cdc_log(table_name, operation, data, changed_by)
--     VALUES (
--         'users',
--         'INSERT',
--         json_object('new', json_object('id', NEW.id, 'name', NEW.name, 'mail', NEW.mail)),
--         'admin'
--     );
-- END;

-- -- 4. UPDATE Trigger
-- CREATE TRIGGER IF NOT EXISTS trg_users_update
-- AFTER UPDATE ON users
-- BEGIN
--     INSERT INTO cdc_log(table_name, operation, data, changed_by)
--     VALUES (
--         'users',
--         'UPDATE',
--         json_object(
--             'old', json_object('id', OLD.id, 'name', OLD.name, 'mail', OLD.mail),
--             'new', json_object('id', NEW.id, 'name', NEW.name, 'mail', NEW.mail)
--         ),
--         'admin'
--     );
-- END;

-- -- 5. DELETE Trigger
-- CREATE TRIGGER IF NOT EXISTS trg_users_delete
-- AFTER DELETE ON users
-- BEGIN
--     INSERT INTO cdc_log(table_name, operation, data, changed_by)
--     VALUES (
--         'users',
--         'DELETE',
--         json_object('old', json_object('id', OLD.id, 'name', OLD.name, 'mail', OLD.mail)),
--         'admin'
--     );
-- END;

