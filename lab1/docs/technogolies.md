# Technologies Learned

In the course of completing the task, the following technologies were studied and applied:

## Containerization and Docker
- **Docker Compose:** Utilized `docker-compose.yml` to organize multi-container applications. This allowed for setting up a comprehensive stack consisting of PostgreSQL, MinIO, and pgAdmin with custom configurations.

## Databases and PostgreSQL
- **PostgreSQL:** Studied the basic SQL commands, creation and management of tables, and the process of importing data from CSV files. This enabled the automation of database population.
- **pgAdmin:** Learned one of the popular GUIs for PostgreSQL, which simplified data visualization and executing SQL queries to verify data loading accuracy.

## Cloud Storage and MinIO
- **S3 Storage:** Explored the concept of buckets and object management. This knowledge formed the basis for setting up cloud storage for file uploads and storage.
- **MinIO:** Used MinIO as an alternative to Amazon S3. The basic configuration and methods for interacting through the web interface were studied, which enabled the upload of random files.

## Programming and Scripts
- Developed scripts for the automated loading of data into PostgreSQL and MinIO. In this project, the following were implemented:
  - The `load_postgres.py` script for importing data from CSV files into the database using the `psycopg2` library.
  - The `upload_s3.py` script for uploading files to S3 storage using the `boto3` library.
- **Libraries:**
  - **psycopg2:** A tool for connecting to and working with PostgreSQL from Python.
  - **boto3:** A library for interacting with S3 storage, used for working with MinIO.

## Documentation and Visualization
- **MinIO with Uploaded Files:**
  
  ![MinIO](docs/images/mybucket.png)

- **pgAdmin Interface with Executed SQL Queries and Data Visualization:**

  ![pgAdmin](docs/images/pgadmin.png)

- **Docker Containers Status Confirming the Proper Deployment of Services:**

  ![Docker containers](docs/images/docker_ps.png)
