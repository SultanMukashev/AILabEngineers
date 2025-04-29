import os
import boto3
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv

load_dotenv()

# Настройки для Postgres
DB_HOST = os.getenv("POSTGRES_HOST")
DB_NAME = os.getenv("POSTGRES_DB")
DB_USER = os.getenv("POSTGRES_USER")
DB_PASS = os.getenv("POSTGRES_PASSWORD")
DB_PORT = os.getenv("POSTGRES_PORT")

# Настройки для MinIO
MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT", "http://localhost:9000")
ACCESS_KEY = os.getenv("MINIO_ROOT_USER")
SECRET_KEY = os.getenv("MINIO_ROOT_PASSWORD")
BUCKET_NAME = os.getenv("BUCKET_NAME")
FILES_DIR = os.getenv("FILES_DIR", "./data")

# Название файла
FILE_NAME = "clean_krisha_kokshetau.csv"
LOCAL_DOWNLOAD_PATH = os.path.join(FILES_DIR, f"downloaded_{FILE_NAME}")

def download_from_minio(bucket_name, object_name, download_path):
    s3_client = boto3.client(
        "s3",
        endpoint_url=MINIO_ENDPOINT,
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
    )

    try:
        s3_client.download_file(bucket_name, object_name, download_path)
        print(f"✅ File '{object_name}' downloaded from bucket '{bucket_name}' to '{download_path}'.")
    except Exception as e:
        print(f"❌ Error downloading file: {e}")
        exit(1)

def load_csv_to_db(csv_file_path, table_name):
    conn = psycopg2.connect(
        host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS, port=DB_PORT
    )
    cursor = conn.cursor()

    with open(csv_file_path, "r", encoding="utf-8") as file:
        copy_sql = sql.SQL("COPY {} FROM STDIN WITH CSV HEADER DELIMITER ','").format(
            sql.Identifier(table_name)
        )
        cursor.copy_expert(copy_sql.as_string(conn), file)

    conn.commit()
    cursor.close()
    conn.close()
    print(f"✅ Data from {csv_file_path} has been successfully loaded into {table_name}.")

if __name__ == "__main__":
    download_from_minio(BUCKET_NAME, FILE_NAME, LOCAL_DOWNLOAD_PATH)
    load_csv_to_db(LOCAL_DOWNLOAD_PATH, "apartments")
