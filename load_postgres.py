import psycopg2
import pandas as pd

DB_HOST = "localhost"  
DB_PORT = "5432"
DB_NAME = "my_database"
DB_USER = "admin"
DB_PASSWORD = "secret"


conn = psycopg2.connect(
    host=DB_HOST,
    port=DB_PORT,
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD
)
cursor = conn.cursor()


cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name TEXT,
    age INTEGER,
    city TEXT
);
""")
conn.commit()


csv_file = "data.csv"  
df = pd.read_csv(csv_file)

for _, row in df.iterrows():
    cursor.execute(
        "INSERT INTO users (name, age, city) VALUES (%s, %s, %s)",
        (row["name"], row["age"], row["city"])
    )

conn.commit()
cursor.close()
conn.close()

print(" Данные успешно загружены в PostgreSQL!")

