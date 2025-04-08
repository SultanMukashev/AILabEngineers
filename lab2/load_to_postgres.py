import os
import sys
import pandas as pd
import psycopg2
import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv, find_dotenv
import io
import csv

def main():
    # load environment variables from .env file
    env_path = find_dotenv()
    if not env_path:
        print("Error: .env file not found.", file=sys.stderr)
        sys.exit(1)
    load_dotenv(dotenv_path=env_path)

    # get config from .env
    db_name = os.getenv('POSTGRES_DB')
    db_user = os.getenv('POSTGRES_USER')
    db_password = os.getenv('POSTGRES_PASSWORD')
    db_host = os.getenv('POSTGRES_HOST', 'localhost')
    db_port = os.getenv('POSTGRES_PORT', '5432')
    s3_endpoint_url = os.getenv('MINIO_ENDPOINT')
    s3_access_key = os.getenv('MINIO_ROOT_USER')
    s3_secret_key = os.getenv('MINIO_ROOT_PASSWORD')
    s3_bucket_name = os.getenv('MINIO_BUCKET')

    # validate config
    if not all([db_name, db_user, db_password, db_host, db_port,
                s3_endpoint_url, s3_access_key, s3_secret_key, s3_bucket_name]):
        print("Missing required configuration in .env file.", file=sys.stderr)
        sys.exit(1)

    # file to table mapping: you can extend this dictionary
    files_to_process = {
        'kolesa_almaty_cleaned.csv': ('kolesa_cars', """
            CREATE TABLE IF NOT EXISTS kolesa_cars (
                brand TEXT, model TEXT, year INTEGER, city TEXT, price BIGINT, mileage INTEGER,
                engine_volume_liters FLOAT, body_style TEXT, color TEXT, transmission TEXT,
                drive_type TEXT, url TEXT, parsed_at TIMESTAMP
            );
        """)
    }

    # connect to postgresql
    conn = None
    try:
        conn = psycopg2.connect(dbname=db_name, user=db_user, password=db_password, host=db_host, port=db_port)
        conn.autocommit = False
    except Exception as e:
        print(f"PostgreSQL connection failed: {e}", file=sys.stderr)
        sys.exit(1)

    # ensure schema exists
    try:
        with conn.cursor() as cur:
            for file, (table_name, schema_sql) in files_to_process.items():
                cur.execute(schema_sql)
            conn.commit()
    except Exception as e:
        print(f"Schema execution failed: {e}", file=sys.stderr)
        conn.rollback()
        conn.close()
        sys.exit(1)

    # connect to minio s3 
    s3_client = None
    try:
        s3_client = boto3.client('s3', endpoint_url=s3_endpoint_url,
                                 aws_access_key_id=s3_access_key, aws_secret_access_key=s3_secret_key)
        s3_client.list_buckets() # test connection
    except Exception as e:
        print(f"CRITICAL: S3/MinIO connection failed: {e}", file=sys.stderr)
        if conn: conn.close()
        sys.exit(1)

    # process each file
    print("\nStarting data loading process...")
    all_successful = True
    for s3_object_key, (table_name, _) in files_to_process.items():
        try:
            # download from s3
            s3_response = s3_client.get_object(Bucket=s3_bucket_name, Key=s3_object_key)
            file_content = s3_response['Body'].read()

            # read csv into pandas dataframe
            data_buffer = io.BytesIO(file_content)
            dtype_options = {'zip_code': str} if table_name == 'accounts' else None
            # set parse_dates options based on table name
            if table_name == 'accounts':
                parse_dates_options = [8]
            elif table_name == 'transactions':
                parse_dates_options = [1]
            else:
                parse_dates_options = None 
                
            df = pd.read_csv(data_buffer, dtype=dtype_options, parse_dates=parse_dates_options)
            df.columns = df.columns.str.strip() # strip whitespace from column names

            if df.empty:
                print(f"Warning: File '{s3_object_key}' is empty. Skipping load.")
                continue

            # load data into PostgreSQL
            buffer = io.StringIO()
            # use settings compatible with postgresql COPY CSV FROM STDIN
            df.to_csv(buffer, index=False, header=False, sep='\t', na_rep='\\N', quoting=csv.QUOTE_NONE)
            buffer.seek(0)

            with conn.cursor() as cur:

                table_columns = df.columns
                safe_columns = [f'"{col}"' for col in table_columns]
                cur.execute(f"TRUNCATE TABLE {table_name};")
                print(f"Table '{table_name}' truncated.")
                # use COPY command to load data
                # E'\\t' is the delimiter, '\\N' is the null representation, and E'\\b' is the quote character
                copy_sql = f"""
                    COPY {table_name} ({",".join(safe_columns)})
                    FROM STDIN WITH (FORMAT CSV, HEADER FALSE, DELIMITER E'\\t', NULL '\\N', QUOTE E'\\b')
                """
                cur.copy_expert(sql=copy_sql, file=buffer)
                conn.commit()
                print(f"Successfully loaded {len(df)} rows into '{table_name}'.")

        except Exception as e:
            print(f"ERROR processing file '{s3_object_key}': {type(e).__name__} - {e}", file=sys.stderr)
            all_successful = False
            conn.rollback()

    # finalize
    if conn:
        conn.close()

    print("\nData loading process finished.")
    if not all_successful:
        print("Errors occurred during processing.", file=sys.stderr)
        sys.exit(1)
    else:
        print("All files processed successfully.")

if __name__ == "__main__":
    main()