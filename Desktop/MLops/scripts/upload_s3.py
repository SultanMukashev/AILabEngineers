import boto3
import os
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY")
MINIO_BUCKET = os.getenv("MINIO_BUCKET")

s3 = boto3.client(
    "s3",
    endpoint_url=MINIO_ENDPOINT,
    aws_access_key_id=MINIO_ACCESS_KEY,
    aws_secret_access_key=MINIO_SECRET_KEY
)

def upload_file(file_path, bucket_name):
    try:
        file_name = os.path.basename(file_path)
        s3.upload_file(file_path, bucket_name, file_name)
        print(f"✅ Файл '{file_name}' загружен в {bucket_name}.")
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    upload_file("data/example.txt", MINIO_BUCKET)
