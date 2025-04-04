import boto3
import os
from dotenv import load_dotenv

# load environment variables from .env file
load_dotenv(dotenv_path='.env')

MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT")
ACCESS_KEY = os.getenv("MINIO_ROOT_USER")
SECRET_KEY = os.getenv("MINIO_ROOT_PASSWORD")
BUCKET_NAME = os.getenv("MINIO_BUCKET_NAME")

s3_client = boto3.client( #setup s3 client
    "s3",
    endpoint_url=MINIO_ENDPOINT,
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY
)

def create_bucket(bucket_name): #create bucket if it doesnt exits
    try:
        s3_client.head_bucket(Bucket=bucket_name)
        print(f"Bucket '{bucket_name}' already exists")
    except:
        try:
            s3_client.create_bucket(Bucket=bucket_name)
            print(f"Created bucket: {bucket_name}")
        except Exception as e:
            print(f"Error creating bucket: {e}")

def upload_files(bucket_name, folder): #upload all
    if not os.path.exists(folder):
        print(f"Folder {folder} not found")
        return

    for file_name in os.listdir(folder):
        file_path = os.path.join(folder, file_name)
        if os.path.isfile(file_path):
            try:
                s3_client.upload_file(file_path, bucket_name, file_name)
                print(f"Uploaded: {file_name} -> s3://{bucket_name}/{file_name}")
            except e:
                print("Error: MinIO credentials are unavailable")


if __name__ == "__main__":
    try:
        create_bucket(BUCKET_NAME)          
        upload_files(BUCKET_NAME, "data/")  #store backup of data into minio s3 storage
        print("All files uploaded successfully")
    except Exception as e:
        print(f"Error: {e}")