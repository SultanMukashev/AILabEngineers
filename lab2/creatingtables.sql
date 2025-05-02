CREATE TABLE IF NOT EXISTS accounts (
    customer_id     INTEGER PRIMARY KEY,
    first_name      VARCHAR(50) NOT NULL,
    last_name       VARCHAR(50) NOT NULL,
    address_1       VARCHAR(100) NOT NULL,
    address_2       VARCHAR(100) ,
    city            VARCHAR(50) NOT NULL,
    state           VARCHAR(50) NOT NULL,
    zip_code        VARCHAR(10) NOT NULL,
    join_date       DATE NOT NULL
);

CREATE TABLE IF NOT EXISTS products (
    product_id      INTEGER PRIMARY KEY,
    product_code    VARCHAR(10) NOT NULL,
    product_description VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS transactions (
    transaction_id  VARCHAR(100) PRIMARY KEY,
    transaction_date DATE NOT NULL,
    product_id      INTEGER NOT NULL REFERENCES products(product_id),
    product_code    VARCHAR(10) NOT NULL,
    product_description VARCHAR(100) NOT NULL,
    quantity        INTEGER NOT NULL,
    account_id      INTEGER NOT NULL REFERENCES accounts(customer_id)
);
