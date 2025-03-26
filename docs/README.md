# Отчет о выполненной lab1 работе: PostgreSql + S3-хранилище в Docker-Compose
Этот отчет опишет все проделанные шаги для развертывания pgAdmin, MinIO, PostgreSql с помощью Docker Compose, и автоматизация загрузки данных в PostgreSql и MinIO

## 1.Изучение задания и инструментов.
### 1.1 Постановка задачи
В первом этапе я изучил само задание и ознакомился с нужными инструментами которые нужно развернуть:
* PostgreSQL и автоматически инициализировать создание таблиц с помощью SQL-скриптов.
* S3-хранилище, в моем случае MinIO
* pgAdmin для отслеживания и работы с PostgreSql
* Sql-скрипты для автоматической загрузки csv файлов в PostgreSql, и файлов в MinIO

### 1.2 Источники
Использовал Docker Compose для развёртывания. Образы были взяты из официальных репозиториев:
* Docker Hub: https://hub.docker.com/
* PostgreSQL на Docker Hub: https://hub.docker.com/_/postgres
* pgAdmin на Docker Hub: https://hub.docker.com/r/dpage/pgadmin4

## 2. Разработка инфраструктуры

### 2.1 Создание файла **`.env`**
Файл **`.env`** используется для хранения конфиденциальных данных, таких как логины и пароли, отдельно от кода. 
```ini
# PostgreSQL
POSTGRES_USER=psw
POSTGRES_PASSWORD=psw
POSTGRES_DB=psw
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

# MinIO
MINIO_ENDPOINT=http://localhost:9000
MINIO_ROOT_USER=psw
MINIO_ROOT_PASSWORD=psw
BUCKET_NAME=mybucket
FILES_DIR=./data

# pgAdmin
PGADMIN_DEFAULT_EMAIL=psw@example.com
PGADMIN_DEFAULT_PASSWORD=psw

# Пути к CSV-файлам
CSV_USERS=data/users.csv
CSV_ORDERS=data/orders.csv
```
### 2.2 Создание **`docker-compose.yml`**
Этот **`docker-compose.yml`** файл предназначен для развертывания трех сервисов с использованием Docker Compose
```yaml
services:
  postgres:
    image: postgres:13
    container_name: postgres
    environment:
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: ${POSTGRES_DB}
    volumes:
      - ./pgdata:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
    ports:
      - "5432:5432"
    

  minio:
    image: minio/minio
    container_name: minio
    command: server /data --console-address ":9001"
    environment:
      MINIO_ROOT_USER: ${MINIO_ROOT_USER}
      MINIO_ROOT_PASSWORD: ${MINIO_ROOT_PASSWORD}
    volumes:
      - ./s3data:/data
    ports:
      - "9000:9000"
      - "9001:9001"
    
  pgadmin:
    image: dpage/pgadmin4
    container_name: pgadmin
    environment:
      PGADMIN_DEFAULT_EMAIL: ${PGADMIN_DEFAULT_EMAIL}
      PGADMIN_DEFAULT_PASSWORD: ${PGADMIN_DEFAULT_PASSWORD}
    ports:
      - "5050:80"
  ```
## 3. Развертывание и запуск

### 3.1 Запуск контейнера.
```yaml
docker-compose up -d
```











