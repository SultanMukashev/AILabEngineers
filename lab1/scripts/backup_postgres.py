import os
import boto3
import subprocess
from dotenv import load_dotenv
from datetime import datetime
from botocore.client import Config

load_dotenv(dotenv_path='./.env')

DB_USER = os.getenv("POSTGRES_USER")
DB_NAME = os.getenv("POSTGRES_DB")
DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")

MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT", "http://localhost:9000")
MINIO_ACCESS_KEY = os.getenv("MINIO_ROOT_USER")
MINIO_SECRET_KEY = os.getenv("MINIO_ROOT_PASSWORD")
BUCKET_NAME = os.getenv("MINIO_BUCKET", "lab-bucket")

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
backup_file = f"backup_{timestamp}.sql"

def dump_postgres():
    print("📦 Dumping PostgreSQL...")
    cmd = [
        "pg_dump",
        "-U", DB_USER,
        "-h", DB_HOST,
        "-p", DB_PORT,
        "-d", DB_NAME,
        "-f", backup_file
    ]
    env = os.environ.copy()
    env["PGPASSWORD"] = os.getenv("POSTGRES_PASSWORD")
    subprocess.run(cmd, env=env, check=True)
    print(f"✅ Dump saved as {backup_file}")

def upload_to_minio():
    print("🚀 Uploading dump to MinIO...")
    s3 = boto3.client(
        "s3",
        endpoint_url=MINIO_ENDPOINT,
        aws_access_key_id=MINIO_ACCESS_KEY,
        aws_secret_access_key=MINIO_SECRET_KEY,
        config=Config(signature_version='s3v4'),
        region_name="us-east-1"
    )
    s3.upload_file(backup_file, BUCKET_NAME, f"backups/{backup_file}")
    print(f"✅ Uploaded to MinIO: backups/{backup_file}")

if __name__ == "__main__":
    dump_postgres()
    upload_to_minio()
