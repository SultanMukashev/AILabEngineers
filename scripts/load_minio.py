import boto3
import pandas as pd
import psycopg2
from io import BytesIO

# --- Настройки MinIO ---
minio_client = boto3.client(
    's3',
    endpoint_url='http://localhost:9000',
    aws_access_key_id='minioaccesskey',
    aws_secret_access_key='minioaccesskey'
)

# --- Настройки PostgreSQL ---
conn = psycopg2.connect(
    host="localhost",
    port=5432,
    dbname="your_database",
    user="user",
    password="password"
)
cursor = conn.cursor()

# --- Дропаем таблицы, если они уже существуют ---
cursor.execute("DROP TABLE IF EXISTS users;")
cursor.execute("DROP TABLE IF EXISTS orders;")
conn.commit()

# --- Создание таблиц с правильными колонками ---
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INT PRIMARY KEY,
        name TEXT,
        email TEXT,
        year INT
    );
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        order_id INT PRIMARY KEY,
        product_id INT,
        quantity INT
    );
""")
conn.commit()

# --- Функция: загрузка CSV из MinIO ---
def load_csv_from_minio(bucket, file_name):
    obj = minio_client.get_object(Bucket=bucket, Key=file_name)
    return pd.read_csv(BytesIO(obj['Body'].read()))

# --- Пример данных для загрузки в PostgreSQL ---
users_data = [
    (1, 'John', 'john@example.com', 20),
    (2, 'Jane', 'jane@example.com', 21),
    (3, 'Alina', 'alina@example.com', 19),
    (4, 'Ayan', 'ayan@mail.com', 23),
    (5, 'Nur', 'nur@mail.com', 25)
]

orders_data = [
    (101, 1, 2),
    (102, 2, 1),
    (103, 1, 2),
    (105, 1, 2)
]

# --- Загрузка данных пользователей в PostgreSQL ---
for user in users_data:
    cursor.execute(
        "INSERT INTO users (id, name, email, year) VALUES (%s, %s, %s, %s)",
        user
    )

# --- Загрузка данных заказов в PostgreSQL ---
for order in orders_data:
    cursor.execute(
        "INSERT INTO orders (order_id, product_id, quantity) VALUES (%s, %s, %s)",
        order
    )

# Подтверждение транзакции
conn.commit()
cursor.close()
conn.close()

print("Данные успешно загружены в PostgreSQL.")
