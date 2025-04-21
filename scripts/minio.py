import boto3
import os

# Подключение к MinIO
s3 = boto3.client(
    's3',
    endpoint_url='http://localhost:9000',
    aws_access_key_id='minioaccesskey',
    aws_secret_access_key='minioaccesskey',
    region_name='us-east-1'
)

bucket_name = 'your-bucket'

# Создание bucket (если он ещё не создан)
try:
    s3.create_bucket(Bucket=bucket_name)
    print(f"Бакет '{bucket_name}' создан.")
except s3.exceptions.BucketAlreadyOwnedByYou:
    print(f"Бакет '{bucket_name}' уже существует.")

# Загрузка всех файлов из папки data/
def upload_all_files():
    try:
        for file_name in os.listdir('data'):
            full_path = os.path.join('data', file_name)
            s3.upload_file(full_path, bucket_name, file_name)
            print(f"Файл {file_name} успешно загружен в {bucket_name}.")
    except Exception as e:
        print(f"Ошибка при загрузке файлов: {e}")

upload_all_files()
