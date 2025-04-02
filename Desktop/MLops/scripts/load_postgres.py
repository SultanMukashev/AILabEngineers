import psycopg2
import pandas as pd
import os
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

DB_NAME = os.getenv("POSTGRES_DB")
DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_HOST = os.getenv("POSTGRES_HOST")
DB_PORT = os.getenv("POSTGRES_PORT")

def load_csv_to_table(csv_path, table_name):
    try:
        df = pd.read_csv(csv_path, encoding="utf-8")
        if table_name == "orders":
            df.rename(columns={"price": "amount"}, inplace=True)
        if 'id' in df.columns:
            df.drop_duplicates(subset=['id'], inplace=True)

        columns = list(df.columns)
        columns_str = ', '.join(columns)
        placeholders = ', '.join(['%s'] * len(columns))

        query = f"""
            INSERT INTO {table_name} ({columns_str}) 
            VALUES ({placeholders}) 
            ON CONFLICT (id) DO NOTHING;
        """

        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        cur = conn.cursor()

        for _, row in df.iterrows():
            values = tuple(row)
            cur.execute(query, values)

        conn.commit()
        print(f"✅ {csv_path} загружен в '{table_name}'.")

        cur.close()
        conn.close()
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    load_csv_to_table("data/users.csv", "users")
    load_csv_to_table("data/orders.csv", "orders")
