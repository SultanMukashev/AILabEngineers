-- Создание таблицы пользователей
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL
);

-- Создание таблицы заказов
CREATE TABLE IF NOT EXISTS orders (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    product_name VARCHAR(255) NOT NULL,
    amount DECIMAL(10,2) NOT NULL, -- Используем "amount", так как у тебя была ошибка с "price"
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Заполнение тестовыми данными (чтобы не было дубликатов, проверяем)
INSERT INTO users (name, email) VALUES
    ('Алихан', 'alihan@example.com'),
    ('Мария', 'maria@example.com')
ON CONFLICT (email) DO NOTHING;  -- Если email уже есть, не вставляем

INSERT INTO orders (user_id, product_name, amount) VALUES
    (1, 'Ноутбук', 150000),
    (2, 'Смартфон', 100000)
ON CONFLICT (id) DO NOTHING;  -- Если заказ уже есть, не вставляем
