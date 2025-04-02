import boto3
import os
from dotenv import load_dotenv

load_dotenv()

MINIO_ENDPOINT = os.getenv('MINIO_ENDPOINT')
MINIO_ACCESS_KEY = os.getenv('MINIO_ACCESS_KEY')
MINIO_SECRET_KEY = os.getenv('MINIO_SECRET_KEY')
MINIO_BUCKET_NAME = os.getenv('MINIO_BUCKET_NAME')

print("Using bucket:", MINIO_BUCKET_NAME)

s3_client = boto3.client(
    's3',
    endpoint_url=MINIO_ENDPOINT,
    aws_access_key_id=MINIO_ACCESS_KEY,
    aws_secret_access_key=MINIO_SECRET_KEY,
)

def create_bucket_if_not_exists(bucket_name):
    """
    Check if the bucket exists; if not, create it.
    """
    try:
        s3_client.head_bucket(Bucket=bucket_name)
        print(f"Bucket '{bucket_name}' already exists.")
    except Exception as e:
        try:
            s3_client.create_bucket(Bucket=bucket_name)
            print(f"Bucket '{bucket_name}' created successfully.")
        except Exception as create_e:
            print(f"Error creating bucket '{bucket_name}': {create_e}")

def upload_file_to_minio(file_path, bucket_name, object_name):
    """
    Upload a file to the specified bucket in MinIO.
    """
    try:
        with open(file_path, 'rb') as file:
            s3_client.upload_fileobj(file, bucket_name, object_name)
            print(f"Successfully uploaded {file_path} to {bucket_name}/{object_name}")
    except Exception as e:
        print(f"Error uploading {file_path}: {e}")

if __name__ == '__main__':
    # Ensure the bucket exists
    create_bucket_if_not_exists(MINIO_BUCKET_NAME)

    data_folder = "data"
    if os.path.isdir(data_folder):
        csv_files = os.listdir(data_folder)
        for csv_file in csv_files:
            file_path = os.path.join(data_folder, csv_file)
            upload_file_to_minio(file_path, MINIO_BUCKET_NAME, csv_file)
    else:
        print(f"The folder '{data_folder}' does not exist.")
