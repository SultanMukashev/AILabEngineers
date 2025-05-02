import os, io, pathlib, boto3, pandas as pd, psycopg2

s3 = boto3.client(
    "s3",
    endpoint_url=os.environ["S3_ENDPOINT"],
    aws_access_key_id=os.environ["ACCESS_KEY"],
    aws_secret_access_key=os.environ["SECRET_KEY"],
)
bucket = os.environ["BUCKET"]

PARENTS  = ["products.csv", "accounts.csv"]      
CHILDREN = ["transactions.csv"]                 

pg_conn = (
    f"dbname={os.environ['POSTGRES_DB']} "
    f"user={os.environ['POSTGRES_USER']} "
    f"password={os.environ['POSTGRES_PASSWORD']} "
    f"host=postgres port=5432"
)

def load_csv(cur, csv_name, cascade=False):
    path  = pathlib.Path(csv_name)
    key   = path.name         
    table = path.stem          

    cur.execute(f"TRUNCATE {table} {'CASCADE' if cascade else ''};")

    obj = s3.get_object(Bucket=bucket, Key=key)
    df  = pd.read_csv(io.BytesIO(obj["Body"].read()))
    print(f"⬇️  {key}: {df.shape}")

    buf = io.StringIO()
    df.to_csv(buf, header=False, index=False)
    buf.seek(0)
    cur.copy_expert(
        f"COPY {table} ({', '.join(df.columns)}) FROM STDIN WITH CSV",
        buf
    )
    print(f"   → loaded into {table} ({len(df)} rows)")

with psycopg2.connect(pg_conn) as conn, conn.cursor() as cur:
    for csv_file in PARENTS:
        load_csv(cur, csv_file, cascade=True)

    for csv_file in CHILDREN:
        load_csv(cur, csv_file, cascade=False)
