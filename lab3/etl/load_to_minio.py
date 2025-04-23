import os
import boto3
from dotenv import load_dotenv

# load environment variables from .env file
load_dotenv()

MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT")
ACCESS_KEY = os.getenv("MINIO_ROOT_USER")
SECRET_KEY = os.getenv("MINIO_ROOT_PASSWORD")
BUCKET_NAME = os.getenv("MINIO_BUCKET")
FILES_DIR = os.getenv("OUTPUT_DIR", "lab3/data/processed")
PREFIX = "ML"  # folder prefix inside the bucket

s3_client = boto3.client(
    "s3",
    endpoint_url=MINIO_ENDPOINT,
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY
)

def ensure_bucket_exists(bucket_name):
    existing_buckets = [b['Name'] for b in s3_client.list_buckets().get('Buckets', [])]
    if bucket_name not in existing_buckets:
        s3_client.create_bucket(Bucket=bucket_name)
        print(f"[MinIO] Created bucket: {bucket_name}")
    else:
        print(f"[MinIO] Bucket '{bucket_name}' already exists")

def upload_files(directory, bucket_name, prefix=""):
    for file_name in os.listdir(directory):
        file_path = os.path.join(directory, file_name)
        if os.path.isfile(file_path):
            object_name = os.path.join(prefix, file_name)
            try:
                s3_client.upload_file(file_path, bucket_name, object_name)
                print(f"[MinIO] Uploaded {object_name}")
            except Exception as e:
                print(f"[MinIO] Error uploading {file_name}: {e}")

if __name__ == '__main__':
    print(f"[MinIO] Uploading files from '{FILES_DIR}' to '{BUCKET_NAME}/{PREFIX}'")
    ensure_bucket_exists(BUCKET_NAME)
    upload_files(FILES_DIR, BUCKET_NAME, PREFIX)
    print("[MinIO] All done.")
