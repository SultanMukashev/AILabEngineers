FROM python:3.12-slim

WORKDIR /app
ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY wait-for-it.sh upload_data.py load_to_postgres.py ./
CMD ["/bin/bash", "-c", "\
  chmod +x wait-for-it.sh && \
  MINIO_HOST_PORT=$(echo \"$S3_ENDPOINT\" | sed -E 's~^https?://~~') && \
  ./wait-for-it.sh \"$MINIO_HOST_PORT\" 60 && \
  ./wait-for-it.sh postgres:5432 60 && \
  python upload_data.py && \
  python load_to_postgres.py \
"]
    