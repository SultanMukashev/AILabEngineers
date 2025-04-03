import psycopg2
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

conn_params = {
    "host": os.getenv("POSTGRES_HOST"),
    "port": int(os.getenv("POSTGRES_PORT")),
    "dbname": os.getenv("POSTGRES_DB"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD")
}

def load_csv_to_table(csv_path, table_name, columns):
    df = pd.read_csv(csv_path)
    conn = psycopg2.connect(**conn_params)
    cursor = conn.cursor()

    for _, row in df.iterrows():
        values = [row[col] if pd.notna(row[col]) else None for col in columns]
        placeholders = ', '.join(['%s'] * len(columns))
        sql = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"
        cursor.execute(sql, values)

    conn.commit()
    cursor.close()
    conn.close()
    print(f"✅ Loaded {len(df)} records into '{table_name}'")

if __name__ == "__main__":
    load_csv_to_table("./data/users.csv", "users", ["id", "name", "email", "created_at"])
    load_csv_to_table("./data/orders.csv", "orders", ["id", "user_id", "product", "amount", "order_date"])
