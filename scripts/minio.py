import boto3

# Подключаемся к MinIO
s3 = boto3.client(
    's3',
    endpoint_url='http://localhost:9000',  # Адрес MinIO
    aws_access_key_id='minioaccesskey',  # Ключ доступа
    aws_secret_access_key='miniosecretkey',  # Секретный ключ
    region_name='us-east-1'
)

bucket_name = 'your-bucket'

# Загружаем файл в MinIO
def upload_file(file_name):
    try:
        s3.upload_file(file_name, bucket_name, file_name.split("/")[2])
        print(f"Файл {file_name} успешно загружен в {bucket_name}.")
    except Exception as e:
        print(f"Ошибка: {e}")

upload_file('./data/users.csv')
