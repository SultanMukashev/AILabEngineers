import os
import psycopg2
import pandas as pd

# Читаем переменные окружения
DB_CONFIG = {
    "dbname": os.getenv("POSTGRES_DB", "database"),
    "user": os.getenv("POSTGRES_USER", "admin"),
    "password": os.getenv("POSTGRES_PASSWORD", "password"),
    "host": os.getenv("POSTGRES_HOST", "localhost"),
    "port": os.getenv("POSTGRES_PORT", "5432"),
}

CSV_FILES = {
    "users": "data/users.csv",
    "orders": "data/orders.csv"
}

def load_csv_to_postgres(table_name, csv_file, conn):
    df = pd.read_csv(csv_file)

    with conn.cursor() as cur:
        for _, row in df.iterrows():
            if table_name == "users":
                cur.execute("""
                    INSERT INTO users (id, name, email) VALUES (%s, %s, %s)
                    ON CONFLICT (id) DO NOTHING;
                """, (int(row["id"]), row["name"], row["email"]))
            elif table_name == "orders":
                cur.execute("""
                    INSERT INTO orders (id, user_id, amount) VALUES (%s, %s, %s)
                    ON CONFLICT (id) DO NOTHING;
                """, (int(row["id"]), int(row["user_id"]), float(row["amount"])))

    conn.commit()

if __name__ == "__main__":
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        for table, file in CSV_FILES.items():
            print(f"Loading {table} from {file}")
            load_csv_to_postgres(table, file, conn)
        print("Data loaded")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if conn:
            conn.close()
