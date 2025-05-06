import os
import psycopg2
from psycopg2 import sql
from minio import Minio
from dotenv import load_dotenv
import logging
from io import StringIO

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

load_dotenv()


class Config:
    POSTGRES = {
        'host': os.getenv('POSTGRES_HOST'),
        'database': os.getenv('POSTGRES_DB'),
        'user': os.getenv('POSTGRES_USER'),
        'password': os.getenv('POSTGRES_PASSWORD'),
        'port': os.getenv('POSTGRES_PORT')
    }
    MINIO = {
        'endpoint': os.getenv('MINIO_ENDPOINT'),
        'access_key': os.getenv('ACCESS_KEY'),
        'secret_key': os.getenv('SECRET_KEY'),
        'secure': False
    }
    BUCKET_NAME = os.getenv('BUCKET_NAME')


class DataLoader:
    def __init__(self):
        self.pg_conn = None
        try:
            self.minio_client = Minio(
                Config.MINIO['endpoint'],
                access_key=Config.MINIO['access_key'],
                secret_key=Config.MINIO['secret_key'],
                secure=Config.MINIO['secure']
            )
            logger.info(f"Connected to MinIO at {Config.MINIO['endpoint']}")

            self.pg_conn = psycopg2.connect(**Config.POSTGRES)
            logger.info(f"Connected to PostgreSQL at {Config.POSTGRES['host']}")

        except Exception as e:
            logger.error(f"Initialization failed: {str(e)}")
            raise

    def close(self):
        if self.pg_conn:
            self.pg_conn.close()
            logger.info("PostgreSQL connection closed")

    def _get_csv_from_minio(self, object_name):

        try:
            response = self.minio_client.get_object(
                Config.BUCKET_NAME,
                f"{object_name}.csv"
            )
            data = StringIO(response.read().decode('utf-8'))
            response.close()
            response.release_conn()
            return data
        except Exception as e:
            logger.error(f"Error downloading {object_name}.csv: {str(e)}")
            return None

    def process_table(self, table_name):
        try:
            csv_data = self._get_csv_from_minio(table_name)
            if not csv_data:
                return False

            if table_name == 'transactions':
                transformed_data = StringIO()
                for line in csv_data:
                    parts = line.strip().split(', ')
                    transformed_data.write(','.join([
                        parts[0],
                        parts[1],
                        parts[2],
                        parts[5],
                        parts[6]
                    ]) + '\n')
                transformed_data.seek(0)
                csv_data = transformed_data

            with self.pg_conn.cursor() as cursor:
                cursor.copy_expert(
                    sql.SQL("COPY {} FROM STDIN WITH CSV HEADER").format(
                        sql.Identifier(table_name)
                    ),
                    csv_data
                )
                self.pg_conn.commit()
                logger.info(f"Loaded {table_name} successfully")
                return True

        except Exception as e:
            if self.pg_conn:
                self.pg_conn.rollback()
            logger.error(f"Error processing {table_name}: {str(e)}")
            return False


if __name__ == "__main__":
    loader = None
    try:
        loader = DataLoader()
        tables = ['test', 'train']
        for table in tables:
            objects = loader.minio_client.list_objects(Config.BUCKET_NAME, prefix=f"{table}.csv")
            if not any(obj.object_name == f"{table}.csv" for obj in objects):
                logger.error(f"File not found in MinIO: {table}.csv")
                continue

            logger.info(f"\n{'=' * 50}\nProcessing: {table}\n{'=' * 50}")
            if loader.process_table(table):
                logger.info(f"SUCCESS: {table}")
            else:
                logger.error(f"FAILED: {table}")

    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
    finally:
        if loader:
            loader.close()