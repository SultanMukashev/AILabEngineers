import psycopg2
import pandas as pd

# 🔗 PostgreSQL-ге қосылу
DB_NAME = "mydatabase"
DB_USER = "admin"
DB_PASSWORD = "secret"
DB_HOST = "localhost"
DB_PORT = "5434"

def load_csv_to_table(csv_path, table_name):
    """
    CSV файлдағы деректерді PostgreSQL кестесіне жүктеу (дубликаттарды елемейді).
    """
    try:
        df = pd.read_csv(csv_path, encoding="utf-8")
        
        # ❌ Егер id қайталанатын болса, оны автоматты түрде жою
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
        print(f"✅ {csv_path} деректері '{table_name}' кестесіне жүктелді.")

        cur.close()
        conn.close()
    except Exception as e:
        print(f"❌ Қате: {e}")

# 🔹 CSV файлдарды жүктеу
if __name__ == "__main__":
    load_csv_to_table("data/users.csv", "users")
    load_csv_to_table("data/orders.csv", "orders")
