import boto3
import os

# Настройки MinIO
minio_client = boto3.client(
    's3',
    endpoint_url="http://localhost:9000",
    aws_access_key_id="admin",
    aws_secret_access_key="secretkey"
)

# Создание бакета (если его нет)
bucket_name = "my-bucket"
try:
    minio_client.create_bucket(Bucket=bucket_name)
except:
    pass  # Бакет уже существует

# Загрузка случайного файла
file_name = "example.txt"
with open(file_name, "w") as f:
    f.write("Hello, MinIO!")

minio_client.upload_file(file_name, bucket_name, file_name)

print(f"Файл {file_name} успешно загружен в MinIO!")

