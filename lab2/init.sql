CREATE USER admin WITH PASSWORD 'password';
CREATE DATABASE postgres OWNER admin;

CREATE TABLE IF NOT EXISTS accounts (
    customer_id INT PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    address_1 VARCHAR(100),
    address_2 VARCHAR(100),
    city VARCHAR(50),
    state VARCHAR(50),
    zip_code VARCHAR(20),
    join_date DATE
);

CREATE TABLE IF NOT EXISTS products (
    product_id INT PRIMARY KEY,
    product_code VARCHAR(20),
    product_description VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS transactions (
    transaction_id VARCHAR(100) PRIMARY KEY,
    transaction_date DATE,
    product_id INT REFERENCES products(product_id),
    quantity INT,
    account_id INT REFERENCES accounts(customer_id)
);