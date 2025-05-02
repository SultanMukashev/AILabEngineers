import os, boto3, pathlib, sys

s3 = boto3.client(
    "s3",
    endpoint_url=os.environ["S3_ENDPOINT"],
    aws_access_key_id=os.environ["ACCESS_KEY"],
    aws_secret_access_key=os.environ["SECRET_KEY"],
)

bucket = os.environ["BUCKET"]
files  = [f.strip() for f in os.environ["CSV_FILES"].split(",")]

if bucket not in (b["Name"] for b in s3.list_buckets()["Buckets"]):
    s3.create_bucket(Bucket=bucket)
    print(f"Created bucket {bucket}")

for fname in files:
    path = pathlib.Path(fname)
    if not path.is_file():
        print(f"❌ {fname} not found", file=sys.stderr); continue
    s3.upload_file(str(path), bucket, path.name)
    print(f"➡️  {fname}  →  s3://{bucket}/{path.name}")
