import os
import csv
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST = os.getenv("POSTGRES_HOST")
DB_NAME = os.getenv("POSTGRES_DB")
DB_USER = os.getenv("POSTGRES_USER")
DB_PASS = os.getenv("POSTGRES_PASSWORD")
DB_PORT = os.getenv("POSTGRES_PORT")
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CSV_USERS = os.path.join(BASE_DIR, "data", "users.csv")
CSV_ORDERS = os.path.join(BASE_DIR, "data", "orders.csv")


def load_csv_to_db(csv_file_path, table_name):
    try:
        csv_path = os.path.abspath(csv_file_path)
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"CSV file not found: {csv_path}")

        conn = psycopg2.connect(
            host=DB_HOST, database=DB_NAME,
            user=DB_USER, password=DB_PASS,
            port=DB_PORT
        )
        cursor = conn.cursor()

        # Verify table exists
        cursor.execute(f"SELECT EXISTS(SELECT 1 FROM information_schema.tables WHERE table_name='{table_name}')")
        if not cursor.fetchone()[0]:
            raise ValueError(f"Table {table_name} doesn't exist")

        with open(csv_path, "r", encoding="utf-8") as file:
            # Specify columns based on table
            if table_name == "users":
                columns = "(name, email)"  # Skip id since it's SERIAL
            elif table_name == "orders":
                columns = "(user_id, order_date, amount)"  # Skip id
            else:
                columns = ""

            copy_sql = sql.SQL("COPY {} {} FROM STDIN WITH CSV HEADER DELIMITER ','").format(
                sql.Identifier(table_name),
                sql.SQL(columns)
            )
            cursor.copy_expert(copy_sql.as_string(conn), file)

        conn.commit()
        print(f"Successfully loaded {csv_path} to {table_name}")

    except Exception as e:
        print(f"Error loading {table_name}: {str(e)}")
        if 'conn' in locals():
            conn.rollback()
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    load_csv_to_db(CSV_USERS, "users")
    load_csv_to_db(CSV_ORDERS, "orders")
