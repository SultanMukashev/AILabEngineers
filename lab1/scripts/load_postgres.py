import os
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv('POSTGRES_HOST')
DB_PORT = os.getenv('POSTGRES_PORT')
DB_NAME = os.getenv('POSTGRES_DB')
DB_USER = os.getenv('POSTGRES_USER')
DB_PASSWORD = os.getenv('POSTGRES_PASSWORD')

conn = psycopg2.connect(
    host=DB_HOST,
    port=DB_PORT,
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD
)

cur = conn.cursor()

def load_csv_to_db(csv_file, table_name):
    with open(csv_file, 'r', encoding='utf-8') as file:
        copy_sql = sql.SQL("COPY {} FROM STDIN WITH CSV HEADER DELIMITER ','").format(sql.Identifier(table_name))
        cur.copy_expert(copy_sql.as_string(conn), file)
    conn.commit()

if __name__ == '__main__':
    csv_files = os.listdir("data")[::-1]  # Correct the reversal
    for csv_file in csv_files:
        full_path = os.path.join("data", csv_file)
        table_name = os.path.splitext(os.path.basename(csv_file))[0]  # Use os.path for correct path handling
        print(f"Loading data into table: {table_name}")

        try:
            load_csv_to_db(full_path, table_name)
        except Exception as e:
            print(f"Error loading {csv_file}: {e}")

    cur.close()
    conn.close()
