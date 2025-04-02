import boto3
import glob

MINIO_ENDPOINT = "http://localhost:9000"
ACCESS_KEY = "miniouser"
SECRET_KEY = "miniopassword"
BUCKET_NAME = "bucket"
FILES_DIR = "../data"

if not all([ACCESS_KEY, SECRET_KEY, BUCKET_NAME, FILES_DIR]):
    print("ERROR: Not all variables are written!")
    exit(1)

s3_client = boto3.client(
    "s3",
    endpoint_url=MINIO_ENDPOINT,
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
)


def create_bucket(bucket_name):
    try:
        s3_client.head_bucket(Bucket=bucket_name)
        print(f"Bucket '{bucket_name}' exist.")
    except Exception:
        s3_client.create_bucket(Bucket=bucket_name)
        print(f"Bucket created: {bucket_name}")


def upload_files(directory, bucket_name):
    files = glob.glob(f"{directory}/*")

    if not files:
        print(f"ERROR: No files found in {directory}")
        return

    for file_path in files:
        if file_path:
            try:
                file_name = file_path.split("/")[-1]
                s3_client.upload_file(file_path, bucket_name, file_name)
                print(f"Uploaded: {file_name}")
            except Exception as e:
                print(f"Error uploading {file_name}: {e}")


if __name__ == "__main__":
    create_bucket(BUCKET_NAME)
    upload_files(FILES_DIR, BUCKET_NAME)
