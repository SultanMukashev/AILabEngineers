## CSV to PostgreSQL using Docker Compose

This project demonstrates how to use Docker Compose to set up a PostgreSQL database, load CSV data into it, and manage everything inside a containerized environment.

## Project Overview

We are importing two CSV files — users.csv and orders.csv — into a PostgreSQL database running inside a Docker container. This setup is ideal for simulating real-world data ingestion and database handling for analytics or backend purposes.

## Features

- PostgreSQL database containerized via Docker
- PgAdmin web interface for easy database access
- Sample CSV data loading using SQL commands
- Pre-configured docker-compose.yml for one-command startup
- SQL backup file included

## Folder Structure
project_folder/
├── data/
│   ├── users.csv
│   └── orders.csv
├── scripts/
│   ├── load_postgres.py
│   └── upload_s3.py
├── pgdata/                  
├── backup.sql              
├── docker-compose.yml
└── README.md
## Technologies Used

- Docker
- Docker Compose
- PostgreSQL
- pgAdmin
- Python (for optional scripts)

## How to Run

1. Clone this repository:
```bash
git clone https://github.com/SultanMukashev/AIlabEngineers.git
cd AIlabEngineers
docker-compose up -d
docker cp data/users.csv postgres_db:/tmp/users.csv                            ## load ccv data
docker cp data/orders.csv postgres_db:/tmp/orders.csv
docker exec -it postgres_db psql -U myuser -d mydatabase

CREATE TABLE IF NOT EXISTS users (                                               ##inside PostgreSql
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS orders (
    id SERIAL PRIMARY KEY,
    user_id INT,
    product VARCHAR(100),
    amount DECIMAL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

COPY users(namee, email) FROM '/tmp/users.csv' DELIMITER ',' CSV HEADER;
COPY orders(user_id, product, amount) FROM '/tmp/orders.csv' DELIMITER ',' CSV HEADER;


docker exec -t postgres_db pg_dump -U myuser mydatabase > backup.sql   ##backup the database

##Author Yersultan SDU University