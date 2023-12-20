-- Create or use the hbnb_test_db database
-- Create or use the hbnb_test user
-- Grant privileges to the hbnb_test user

CREATE DATABASE IF NOT EXISTS hbnb_test_db;
DROP USER IF EXISTS 'hbnb_test'@'localhost';
CREATE USER IF NOT EXISTS 'hbnb_test'@'localhost' IDENTIFIED BY 'Hbnb_test_pwd8@';
GRANT ALL PRIVILEGES ON hbnb_test_db.* TO 'hbnb_test'@'localhost';
GRANT SELECT ON performance_schema.* TO 'hbnb_test'@'localhost';
FLUSH PRIVILEGES;
