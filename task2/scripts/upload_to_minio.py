import boto3
import os
from dotenv import load_dotenv

load_dotenv()

# Подключение к MinIO
MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT", "http://localhost:9000")
ACCESS_KEY = os.getenv("MINIO_ROOT_USER")
SECRET_KEY = os.getenv("MINIO_ROOT_PASSWORD")
BUCKET_NAME = os.getenv("BUCKET_NAME")
FILES_DIR = os.getenv("FILES_DIR")

if not all([ACCESS_KEY, SECRET_KEY, BUCKET_NAME, FILES_DIR]):
    print("❌ ERROR: Not all variables are set in .env!")
    exit(1)

s3_client = boto3.client(
    "s3",
    endpoint_url=MINIO_ENDPOINT,
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
)

def create_bucket(bucket_name):
    "Создаём бакет если нет"
    try:
        s3_client.head_bucket(Bucket=bucket_name)
        print(f"✅ Bucket '{bucket_name}' already exists.")
    except Exception:
        s3_client.create_bucket(Bucket=bucket_name)
        print(f"✅ New bucket created: {bucket_name}")

def upload_file(file_path, bucket_name):
    "Загружаем один файл"
    if not os.path.exists(file_path):
        print(f"❌ ERROR: File {file_path} does not exist!")
        return

    file_name = os.path.basename(file_path)

    try:
        s3_client.upload_file(file_path, bucket_name, file_name)
        print(f"✅ Uploaded: {file_name}")
    except Exception as e:
        print(f"❌ Error uploading {file_name}: {e}")

if __name__ == "__main__":
    create_bucket(BUCKET_NAME)

    file_name = "clean_krisha_kokshetau.csv"
    file_path = os.path.join(FILES_DIR, file_name)
    upload_file(file_path, BUCKET_NAME)
