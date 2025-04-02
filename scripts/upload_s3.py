import os
import boto3
from botocore.exceptions import NoCredentialsError

# Read environment variables
MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT", "http://localhost:9000")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY", "admin")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY", "password")
BUCKET_NAME = os.getenv("MINIO_BUCKET", "bucket")
UPLOAD_FOLDER = "s3data/"

# Configure MinIO client (boto3)
s3_client = boto3.client(
    "s3",
    endpoint_url=MINIO_ENDPOINT,
    aws_access_key_id=MINIO_ACCESS_KEY,
    aws_secret_access_key=MINIO_SECRET_KEY
)

def create_bucket(bucket_name):
    try:
        s3_client.head_bucket(Bucket=bucket_name)
        print(f"Bucket '{bucket_name}' already exists")
    except:
        try:
            s3_client.create_bucket(Bucket=bucket_name)
            print(f"Created bucket: {bucket_name}")
        except Exception as e:
            print(f"Error creating bucket: {e}")

def upload_files(bucket_name, folder):
    if not os.path.exists(folder):
        print(f"Folder {folder} not found")
        return

    for file_name in os.listdir(folder):
        file_path = os.path.join(folder, file_name)
        if os.path.isfile(file_path):
            try:
                s3_client.upload_file(file_path, bucket_name, file_name)
                print(f"Uploaded: {file_name} -> s3://{bucket_name}/{file_name}")
            except NoCredentialsError:
                print("Error: MinIO credentials are unavailable")

if __name__ == "__main__":
    try:
        create_bucket(BUCKET_NAME)  # Create bucket if it doesn't exist
        upload_files(BUCKET_NAME, UPLOAD_FOLDER)  # Upload files
        print("All files uploaded successfully")
    except Exception as e:
        print(f"Error: {e}")
