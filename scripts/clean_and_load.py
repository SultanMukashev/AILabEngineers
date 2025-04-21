import boto3
import pandas as pd
import psycopg2
from io import BytesIO

# Настройки подключения
s3 = boto3.client(
    's3',
    endpoint_url='http://localhost:9000',
    aws_access_key_id='minioadmin',
    aws_secret_access_key='minioadmin'
)
bucket_name = 'mybucket'

conn = psycopg2.connect(
    dbname="your_database",
    user="user",
    password="password",
    host="localhost",
    port=5432
)
cur = conn.cursor()

# Пример обработки одного файла
file_key = 'users.csv'
obj = s3.get_object(Bucket=bucket_name, Key=file_key)
df = pd.read_csv(BytesIO(obj['Body'].read()))

# Очистка данных (пример)
df.dropna(inplace=True)

# Загрузка в PostgreSQL
cur.execute("DROP TABLE IF EXISTS users;")
cur.execute("""
    CREATE TABLE users (
        id INT,
        name TEXT,
        email TEXT
    );
""")

for _, row in df.iterrows():
    cur.execute("INSERT INTO users VALUES (%s, %s, %s)", tuple(row))

conn.commit()
cur.close()
conn.close()
print("Данные загружены в PostgreSQL")
