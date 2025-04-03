import os
import csv
import psycopg2
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv(dotenv_path='.env')

# DB_CONFIG = {
#     "host": os.getenv("POSTGRES_HOST"),
#     "dbname": os.getenv("POSTGRES_DB"),
#     "user": os.getenv("POSTGRES_USER"),
#     "password": os.getenv("POSTGRES_PASSWORD"),
#     "port": os.getenv("POSTGRES_PORT", 5432),
# }


DB_HOST = os.getenv('POSTGRES_HOST',"postgres")
DB_PORT = os.getenv('POSTGRES_PORT',5432)
DB_NAME = os.getenv('POSTGRES_DB',"postgres")
DB_USER = os.getenv('POSTGRES_USER',"postgres")
DB_PASSWORD = os.getenv('POSTGRES_PASSWORD',"postgres")


# cur = conn.cursor()

def get_connection():
    # conn = psycopg2.connect(**DB_CONFIG)
    # conn.set_client_encoding('utf-8')
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    return conn

# ignore_encoding = lambda s: s.decode('utf8', 'ignore')

def load_csv_to_db(csv_file_path, table_name):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Get table column names
        cursor.execute("""
            SELECT column_name FROM information_schema.columns
            WHERE table_name = %s
            ORDER BY ordinal_position;
        """, (table_name,))
        table_columns = [row[0] for row in cursor.fetchall()]
        print(f"DB columns: {table_columns}")

        # First read: just get header from CSV
        with open(csv_file_path, 'r', encoding='utf-8', errors="ignore") as f:
            reader = csv.reader(f)
            csv_columns = next(reader)
            print(f"CSV columns: {csv_columns}")

        if [c.lower() for c in table_columns] != [c.lower() for c in csv_columns]:
            print("Column mismatch. Aborting.")
            return

        # Clear existing data
        cursor.execute(f"DELETE FROM {table_name};")

        # Second read: for actual copy
        with open(csv_file_path, 'r', errors="ignore") as f:
            cursor.copy_expert(f"""
                COPY {table_name} ({', '.join(table_columns)})
                FROM STDIN WITH CSV HEADER
            """, f)
        
        conn.commit()
        print(f"✅ Loaded {csv_file_path} into table {table_name}.")

    # except Exception as e:
        # print(f"❌ Error: {e}")
        # print(csv_file_path )
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

if __name__ == '__main__':
    # load_csv_to_db('users.csv', 'users')
    # load_csv_to_db('orders.csv', 'orders')
    # SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))  # current script dir
    # print(SCRIPT_DIR)
    # use it to construct full path
    # p = os.path.join(SCRIPT_DIR, '\\data\\users.csv')
    
    p = "../data/users.csv"
    print(p)
    print(repr(DB_HOST),repr(DB_USER),repr(DB_PORT),repr(DB_PASSWORD),repr(DB_NAME),)
    load_csv_to_db(p, 'users')
    # print(DB_CONFIG)

    # load_csv_to_db(os.path.join(SCRIPT_DIR, '../data/orders.csv'), 'orders')

    # print(DB_CONFIG)