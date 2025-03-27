import os
import csv
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv

load_dotenv()  

DB_HOST = os.getenv("POSTGRES_HOST")
DB_NAME = os.getenv("POSTGRES_DB")
DB_USER = os.getenv("POSTGRES_USER")
DB_PASS = os.getenv("POSTGRES_PASSWORD")
DB_PORT = os.getenv("POSTGRES_PORT")

CSV_USERS = os.getenv("CSV_USERS")
CSV_ORDERS = os.getenv("CSV_ORDERS")

def load_csv_to_db(csv_file_path, table_name):
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        port=DB_PORT
    )
    cursor = conn.cursor()
    cursor.execute(f"TRUNCATE TABLE {table_name} RESTART IDENTITY CASCADE;")

    
    with open(csv_file_path, 'r', encoding='utf-8') as file:
        copy_sql = sql.SQL("COPY {} FROM STDIN WITH CSV HEADER DELIMITER ','"). \
        format(sql.Identifier(table_name))
        cursor.copy_expert(copy_sql.as_string(conn), file)
        
    conn.commit()
    cursor.close()
    conn.close()
    print(f"Data from {csv_file_path} has been successfully uploaded to the {table_name} table.")

if __name__ == '__main__':
    load_csv_to_db(CSV_USERS, 'users')
    load_csv_to_db(CSV_ORDERS, 'orders')
