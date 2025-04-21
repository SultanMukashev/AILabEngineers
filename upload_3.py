import boto3
import os

s3 = boto3.client(
    's3',
    endpoint_url='http://localhost:9000',
    aws_access_key_id='minioaccesskey',
    aws_secret_access_key='minioaccesskey'
)

bucket_name = 'mybucket'
s3.create_bucket(Bucket=bucket_name)

for file_name in os.listdir('data'):
    s3.upload_file(f'data/{orders.csv}', bucket_name, orders.csv)
    print(f'Uploaded: {orders.csv}')
