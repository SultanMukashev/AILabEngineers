import psycopg2
import os
import glob
import csv
from dotenv import load_dotenv

load_dotenv(dotenv_path='../.env')

# Настройки подключения к PostgreSQL
DB_CONFIG = {
    "host": os.getenv("POSTGRES_HOST"),
    "dbname": os.getenv("POSTGRES_DB"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
    "port": os.getenv("POSTGRES_PORT", 5432)
}

DATA_DIR = "C:/Users/altyn/projects/AILabEngineers/lab1/data/"  # Папка с CSV-файлами
# "C:\Users\altyn\projects\AILabEngineers\lab1\data\users.csv"
# print(DB_CONFIG)


def get_connection():
    """Создаёт подключение к БД"""
    return psycopg2.connect(**DB_CONFIG)


def get_table_columns(cursor, table_name):

    cursor.execute(f"""
        SELECT column_name FROM information_schema.columns
        WHERE table_name = '{table_name}'
        ORDER BY ordinal_position
    """)
    return [row[0] for row in cursor.fetchall()]


def import_csv_to_postgres():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # find all csv from folder
        csv_files = {os.path.splitext(os.path.basename(f))[0]: f for f in glob.glob(os.path.join(DATA_DIR, "*.csv"))}

        if not csv_files:
            print("No csv from data/!")
            return
        
        print(f"Found {len(csv_files)} CSV-files: {list(csv_files.keys())}")

        for table, file_path in csv_files.items():
            print(f"Load {file_path} in table {table}...")

            # Get list of columns from table
            table_columns = get_table_columns(cursor, table)
            print(f"Table columns {table}: {table_columns}")

            # Read the csv headers
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                csv_columns = next(reader)
            
            print(f"Columns in CSV: {csv_columns}")

            if table_columns != csv_columns:
                raise ValueError(f"Error: Columns in table {table} ({table_columns}) dont match with CSV ({csv_columns})")

            # Clear table before download
            cursor.execute(f"DELETE FROM {table};")

            # Load csv
            with open(file_path, 'r', encoding='utf-8') as f:
                next(f)  
                cursor.copy_expert(f"COPY {table} ({', '.join(table_columns)}) FROM STDIN WITH CSV", f)
            
            print(f"Data Dowloaded in {table}")

        conn.commit()
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    # import_csv_to_postgres()
    print(DB_CONFIG)