import os
import boto3
from dotenv import load_dotenv
from botocore.client import Config

load_dotenv(dotenv_path='./.env')

MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT")
MINIO_ACCESS_KEY = os.getenv("MINIO_ROOT_USER")
MINIO_SECRET_KEY = os.getenv("MINIO_ROOT_PASSWORD")
BUCKET_NAME = os.getenv("MINIO_BUCKET")
LOCAL_FOLDER = "./data/images"

s3 = boto3.client(
    "s3",
    endpoint_url=MINIO_ENDPOINT,
    aws_access_key_id=MINIO_ACCESS_KEY,
    aws_secret_access_key=MINIO_SECRET_KEY,
    config=Config(signature_version='s3v4'),
    region_name="us-east-1"
)

def create_bucket(bucket_name):
    existing = [b['Name'] for b in s3.list_buckets()['Buckets']]
    if bucket_name not in existing:
        s3.create_bucket(Bucket=bucket_name)
        print(f"✅ Bucket '{bucket_name}' создан")
    else:
        print(f"ℹ️ Bucket '{bucket_name}' уже существует")

def upload_files(folder_path, bucket_name):
    for filename in os.listdir(folder_path):
        filepath = os.path.join(folder_path, filename)
        if os.path.isfile(filepath):
            s3.upload_file(filepath, bucket_name, filename)
            print(f"📤 Загрузил: {filename}")

if __name__ == "__main__":
    create_bucket(BUCKET_NAME)
    upload_files(LOCAL_FOLDER, BUCKET_NAME)
