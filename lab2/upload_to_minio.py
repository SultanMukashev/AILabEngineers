import asyncio # we will use asyncio to run the upload tasks concurrently
import os
import sys
from contextlib import asynccontextmanager

from aiobotocore.session import get_session 
from botocore.exceptions import ClientError
from dotenv import load_dotenv, find_dotenv

class S3Client: # this class handles S3 operations
    def __init__(
            self,
            access_key: str,
            secret_key: str,
            endpoint_url: str,
            bucket_name: str,
    ):
        self.config = {
            "aws_access_key_id": access_key,
            "aws_secret_access_key": secret_key,
            "endpoint_url": endpoint_url,
        }

        self.bucket_name = bucket_name
        self.session = get_session()
        print(f"S3Client configured for endpoint: {endpoint_url}, bucket: {bucket_name}")
 # this method creates an S3 client
    @asynccontextmanager
    async def get_client(self):
        async with self.session.create_client("s3", **self.config) as client:
            yield client
            
 # this method checks if the bucket exists and creates it if not
    async def ensure_bucket_exists(self):
        try:
            async with self.get_client() as client:
                await client.head_bucket(Bucket=self.bucket_name)
                print(f"Bucket '{self.bucket_name}' already exists.")
        except ClientError as e:
            error_code = e.response.get('Error', {}).get('Code')
            if error_code == '404' or error_code == 'NoSuchBucket':
                print(f"Bucket '{self.bucket_name}' not found. Attempting to create...")
                try:
                    async with self.get_client() as client:
                        await client.create_bucket(Bucket=self.bucket_name)
                        print(f"Bucket '{self.bucket_name}' created successfully.")
                except ClientError as e_create:
                    print(f"CRITICAL: Error creating bucket '{self.bucket_name}': {e_create}", file=sys.stderr)
                    raise 
            else:
                print(f"CRITICAL: Error checking bucket '{self.bucket_name}': {e}", file=sys.stderr)
                raise
            
# this method uploads a file to the S3 bucket
    async def upload_file(
            self,
            file_path: str,
    ):
        object_name = os.path.basename(file_path)
        try:
            async with self.get_client() as client:
                with open(file_path, "rb") as file_data:
                    await client.put_object(
                        Bucket=self.bucket_name,
                        Key=object_name,
                        Body=file_data,
                    )
                print(f"Successfully uploaded: '{file_path}' to '{self.bucket_name}/{object_name}'")
        except ClientError as e:
            print(f"ERROR uploading file '{file_path}': {e}", file=sys.stderr)
            raise
        except FileNotFoundError:
             print(f"ERROR: File not found at '{file_path}'", file=sys.stderr)
             raise
        except Exception as e:
            print(f"ERROR: An unexpected error occurred during upload of '{file_path}': {e}", file=sys.stderr)
            raise

# this method is the main entry point of the script
async def main():
    env_path = find_dotenv()
    if not env_path:
        print("Error: .env file not found.", file=sys.stderr)
        sys.exit(1)
    load_dotenv(dotenv_path=env_path)
    print(f"Loaded .env file from: {env_path}")

    access_key = os.getenv('MINIO_ROOT_USER')
    secret_key = os.getenv('MINIO_ROOT_PASSWORD')
    endpoint_url = os.getenv('MINIO_ENDPOINT')
    bucket_name = os.getenv('BUCKET_NAME')

    if not all([access_key, secret_key, endpoint_url, bucket_name]):
         print("CRITICAL Error: Missing S3 configuration in .env (MINIO_ROOT_USER, MINIO_ROOT_PASSWORD, MINIO_ENDPOINT, BUCKET_NAME).", file=sys.stderr)
         sys.exit(1)

    s3_client = S3Client(
        access_key=access_key,
        secret_key=secret_key,
        endpoint_url=endpoint_url,
        bucket_name=bucket_name,
    )

    try:
        await s3_client.ensure_bucket_exists()
    except Exception:
         sys.exit(1)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    source_dir_abs = os.path.join(script_dir, 'data')
    files_to_upload = ['kolesa_almaty_cleaned.csv']

    upload_tasks = []
    valid_files_to_upload = []
    print("\nPreparing upload tasks...")
    for filename in files_to_upload:
        file_path = os.path.join(source_dir_abs, filename)
        if os.path.exists(file_path):
            upload_tasks.append(s3_client.upload_file(file_path))
            valid_files_to_upload.append(filename)
        else:
            print(f"Warning: File not found at '{file_path}', skipping.")

    if upload_tasks:
         print(f"Starting concurrent upload of {len(upload_tasks)} files...")
         results = await asyncio.gather(*upload_tasks, return_exceptions=True)
         print("\nUpload process finished.")

         success_count = 0
         error_found = False
         for i, result in enumerate(results):
             filename = valid_files_to_upload[i] 
             if isinstance(result, Exception):
                 error_found = True
             else:
                 success_count += 1

         print(f"\nSummary: {success_count}/{len(valid_files_to_upload)} files uploaded successfully.")
         if error_found:
             sys.exit(1)

    else:
         print("No valid files found in the source directory to upload.")
         sys.exit(1)

# this method is used to run the script
if __name__ == "__main__":
    try:
        asyncio.run(main())
        print("Script finished successfully.")
    except Exception as e:
        print(f"Script exited with an error: {e}", file=sys.stderr)
        sys.exit(1)