import boto3
import os
from dotenv import load_dotenv

load_dotenv()

MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT", "http://localhost:9000") 

ACCESS_KEY = os.getenv("MINIO_ROOT_USER")
SECRET_KEY = os.getenv("MINIO_ROOT_PASSWORD")
BUCKET_NAME = os.getenv("BUCKET_NAME")
FILES_DIR = os.getenv("FILES_DIR")

if not all([ACCESS_KEY, SECRET_KEY, BUCKET_NAME, FILES_DIR]):
    print("ERROR: Not all variables are written!")
    exit(0)

s3_client = boto3.client(
    "s3",
    endpoint_url=MINIO_ENDPOINT,
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY
)

def upload_files(directory, bucket_name):
    """Upload all files from a directory to the specified S3 bucket."""
    for file_name in os.listdir(directory):
        file_path = os.path.join(directory, file_name)
        if os.path.isfile(file_path):
            try:
                s3_client.upload_file(file_path, bucket_name, file_name)
                print(f"Uploaded: {file_name}")
            except Exception as e:
                print(f"Error uploading {file_name}: {e}")

if __name__ == "__main__":
    upload_files(FILES_DIR, BUCKET_NAME)