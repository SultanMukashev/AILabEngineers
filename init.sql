CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    namee VARCHAR(100),
    email VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS orders (
    id SERIAL PRIMARY KEY,
    user_id INT,
    product VARCHAR(100),
    amount NUMERIC
);

-- Загрузка данных из CSV-файлов
COPY users(namee, email)
FROM '/data/users.csv'
DELIMITER ','
CSV HEADER;

COPY orders(user_id, product, amount)
FROM '/data/orders.csv'
DELIMITER ','
CSV HEADER;
