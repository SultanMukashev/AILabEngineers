echo "Starting Docker containers..."
docker-compose up -d

echo "Waiting for PostgreSQL to be ready..."
sleep 10

echo "Installing Python requirements..."
pip install -r requirements.txt

echo "Uploading data to S3..."
cd docker && python upload_s3.py && cd ..

echo "Loading data into PostgreSQL..."
cd docker && python load_postgres.py && cd ..

echo "Running the Titanic survival prediction..."
cd ml && python train.py && cd ..

