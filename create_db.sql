CREATE DATABASE movies;
CREATE USER ciku WITH PASSWORD 'root';
ALTER ROLE ciku SET client_encoding TO 'utf8';
ALTER ROLE ciku SET default_transaction_isolation TO 'read committed';
ALTER ROLE ciku SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE movies TO ciku;