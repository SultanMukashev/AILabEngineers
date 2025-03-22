import os
import csv
import psycopg2

DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
DB_NAME = os.getenv("POSTGRES_DB", "mydatabase")
DB_USER = os.getenv("POSTGRES_USER", "user")
DB_PASS = os.getenv("POSTGRES_PASSWORD", "password")
DB_PORT = os.getenv("POSTGRES_PORT", 5432)

def load_csv_to_db(csv_file_path, table_name):
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        port=DB_PORT
    )
    cursor = conn.cursor()
    
    with open(csv_file_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        headers = next(reader)
        placeholders = ','.join(['%s'] * len(headers))
        sql = f"INSERT INTO {table_name} VALUES ({placeholders})"
        
        for row in reader:
            cursor.execute(sql, row)
    
    conn.commit()
    cursor.close()
    conn.close()
    print(f"Data from {csv_file_path} has been successfully uploaded to the {table_name} table.")

if __name__ == '__main__':
    load_csv_to_db('../data/users.csv', 'users')
    load_csv_to_db('../data/orders.csv', 'orders')