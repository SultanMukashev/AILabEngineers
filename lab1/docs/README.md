# Отчёт по выполненной работе: PostgreSQL + S3-хранилище в Docker-Compose

В этом документе описаны шаги, которые я выполнила для развёртывания **PostgreSQL**, **MinIO** и **pgAdmin** с использованием **Docker Compose**, а также автоматизация загрузки данных.

## 1. Постановка задачи

Перед началом работы я ознакомилась с заданием и изучила необходимые инструменты:
- **PostgreSQL** с автоматическим созданием и инициализацией таблиц через SQL-скрипты
- **S3-хранилище** (реализованное через MinIO)
- **pgAdmin** для работы с PostgreSQL
- Написание **Python-скриптов** для автоматической загрузки данных

## 2. Разработка инфраструктуры

### 2.1 Создание файла `.env`

Для хранения конфиденциальных данных я создала файл `.env`, в котором задаются переменные окружения:

```env
# PostgreSQL
POSTGRES_USER=fibukki
POSTGRES_PASSWORD=secret
POSTGRES_DB=postgres
POSTGRES_HOST=localhost
POSTGRES_PORT=5433
CSV_USERS=../data/users.csv
CSV_ORDERS=../data/orders.csv

# MinIO
MINIO_ROOT_USER=miniouser
MINIO_ROOT_PASSWORD=miniopassword
BUCKET_NAME=bucket

# pgAdmin
PGADMIN_DEFAULT_EMAIL=pgadmin@example.com
PGADMIN_DEFAULT_PASSWORD=pgadminpassword

```
### 2.2 Создание `docker-compose.yml`
 `docker-compose.yml` файл предназначен для развертывания трех сервисов с использованием Docker Compose
 ```
services:
  postgres:
    image: postgres:latest
    container_name: postgres
    restart: always
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
    restart: always
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
    restart: always
    environment:
      PGADMIN_DEFAULT_EMAIL: ${PGADMIN_DEFAULT_EMAIL}
      PGADMIN_DEFAULT_PASSWORD: ${PGADMIN_DEFAULT_PASSWORD}
    ports:
      - "5050:80"
 ```
## 3. Развертывание и запуск
### 3.1. Запуск контейнеров:
Запустила контейнеры:

```
docker-compose up -d
docker ps
```

![](..\screenshots\img.png)

## 4. Автоматизация работы с базой данных
### 4.1. Загрузка CSV-файла в PostgreSQL:
Написала скрипт load_postgres.py, который считывает CSV-файлы из папки data и загружает их в базу данных PostgreSql.

![](..\screenshots\img_4.png)

### 4.2. pgAdmin
#### 4.2.1 Проверим правильно ли сработал load_to_postgres.py
![](..\screenshots\img_2.png)
![](..\screenshots\img_3.png)
Так как все данные из наших файлов сохранились переходим к следующему шагу
#### 4.2.2 Проверим pgAdmin
Заходим в pgAdmin по ссылке http://localhost:5050. Проверим наши таблицы на создание и заполнение.
![](..\screenshots\img_1.png)

### 4.3. MinIO
Запускаем наш код upload_s3.py
![](..\screenshots\img_5.png)

Заходим в MInIO по ссылке http://localhost:9000. 
![](..\screenshots\img_6.png)

## 5. Итоги
- В результате была развернута интегрированная среда с использованием PostgreSQL, MinIO и pgAdmin, настроенная с помощью Docker Compose. 

- С помощью Python-скриптов данные успешно загружены в PostgreSQL и MinIO