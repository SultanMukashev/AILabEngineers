import boto3
import os
from dotenv import load_dotenv

load_dotenv()

MINIO_ENDPOINT = os.getenv(
    "MINIO_ENDPOINT", "http://localhost:9000") 

ACCESS_KEY = os.getenv("MINIO_ROOT_USER")
SECRET_KEY = os.getenv("MINIO_ROOT_PASSWORD")
BUCKET_NAME = os.getenv("BUCKET_NAME")
FILES_DIR = os.getenv("FILES_DIR")

if not all([ACCESS_KEY, SECRET_KEY, BUCKET_NAME, FILES_DIR]):
    print("ERROR: Not all variables are written!")
    exit(1)

s3_client = boto3.client(
    "s3",
    endpoint_url=MINIO_ENDPOINT,
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,)


def create_bucket(bucket_name):
    "Create the bucket, if it's not exist"
    try:
        s3_client.head_bucket(Bucket=bucket_name)
        print(f"Bucket '{bucket_name}' already exist.")
    except Exception:
        s3_client.create_bucket(Bucket=bucket_name)
        print(f"New bucket created: {bucket_name}")


def upload_files(directory, bucket_name):
    "Load files to MinIO"
    if not os.path.exists(directory):
        print(f"ERROR: folder {directory} is not exist!")
        return

    for file_name in os.listdir(directory):
        file_path = os.path.join(directory, file_name)
        if os.path.isfile(file_path):
            try:
                s3_client.upload_file(file_path, bucket_name, file_name)
                print(f"Uploaded: {file_name}")
            except Exception as e:
                print(f"Error uploading {file_name}: {e}")


if __name__ == "__main__":
    create_bucket(BUCKET_NAME)
    upload_files(FILES_DIR, BUCKET_NAME)  
