CREATE DATABASE test_db;

USE test_db;

CREATE TABLE users (
    id VARCHAR(50) PRIMARY KEY,
    email VARCHAR(100),
    country VARCHAR(3)
);

CREATE TABLE transactions (
    id VARCHAR(50) PRIMARY KEY,
    quote_currency VARCHAR(10),
    usd_amount DECIMAL(10, 2),
    user_id VARCHAR(50),
    FOREIGN KEY (user_id) REFERENCES users(id)
);
