CREATE DATABASE webapp;
CREATE USER webapp_master WITH PASSWORD '949fa84a';
ALTER USER webapp_master CREATEDB;
GRANT ALL PRIVILEGES ON DATABASE webapp to webapp_master;
\c webapp
GRANT CREATE ON SCHEMA PUBLIC TO webapp_master;
