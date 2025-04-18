import os
from pathlib import Path
import boto3
from botocore.exceptions import NoCredentialsError, ClientError
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT")
MINIO_ROOT_USER = os.getenv("MINIO_ROOT_USER")
MINIO_ROOT_PASSWORD = os.getenv("MINIO_ROOT_PASSWORD")
MINIO_BUCKET = os.getenv("MINIO_BUCKET")
MINIO_OBJECT_PATH = os.getenv("MINIO_OBJECT_PATH")  # ex: "kolesa/kolesa_almaty_raw.csv"
LOCAL_RAW_PATH = Path(os.getenv("LOCAL_RAW_PATH"))  # ex: "lab3/data/raw/kolesa_almaty_raw.csv"

def download_from_minio():

    try:
        s3 = boto3.client(
            "s3",
            endpoint_url=MINIO_ENDPOINT,
            aws_access_key_id=MINIO_ROOT_USER,
            aws_secret_access_key=MINIO_ROOT_PASSWORD
        )

        s3.head_object(Bucket=MINIO_BUCKET, Key=MINIO_OBJECT_PATH)

        LOCAL_RAW_PATH.parent.mkdir(parents=True, exist_ok=True)

        s3.download_file(MINIO_BUCKET, MINIO_OBJECT_PATH, str(LOCAL_RAW_PATH))
        print(f"File successfully downloaded from MinIO and saved to: {LOCAL_RAW_PATH.resolve()}")

    except NoCredentialsError:
        print("ERROR: Invalid MinIO credentials.")
    except ClientError as e:
        if e.response["Error"]["Code"] == "404":
            print(f"ERROR: Object {MINIO_OBJECT_PATH} not found in bucket {MINIO_BUCKET}.")
        else:
            print(f"ERROR while accessing MinIO: {e}")

if __name__ == "__main__":
    download_from_minio()
