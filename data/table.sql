-- users
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name TEXT,
    email TEXT,
    year INTEGER
);

-- orders
CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    product_id INTEGER,
    product TEXT,
    quantity INTEGER,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
