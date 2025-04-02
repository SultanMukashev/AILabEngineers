import os
import subprocess
import boto3
from datetime import datetime
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

DB_NAME = os.getenv("POSTGRES_DB")
DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_HOST = os.getenv("POSTGRES_HOST")
DB_PORT = os.getenv("POSTGRES_PORT")

MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY")
MINIO_BUCKET = os.getenv("MINIO_BUCKET")

# Подключение к MinIO
s3 = boto3.client(
    "s3",
    endpoint_url=MINIO_ENDPOINT,
    aws_access_key_id=MINIO_ACCESS_KEY,
    aws_secret_access_key=MINIO_SECRET_KEY
)

# Имя файла для бэкапа
backup_file = f"backup_{DB_NAME}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.sql"

# Выполняем команду для дампа БД
backup_command = f'PGPASSWORD={DB_PASSWORD} pg_dump -h
