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

### 3.1 Запуск контейнера и проверка статуса
Запускаем контейнер и проверяем статус
```yaml
docker-compose up -d # Для запуска
docker ps # Для проверки
```
![docker_ps (1)](https://github.com/user-attachments/assets/c2a5bdc7-8341-49dc-8b59-ae146edce0aa)

## 4. Автоматизация загрузки данных через скрипты и проверка через веб интерфейсы
На этом шаге выполним загрузку скриптов(ранее разработанных для загрузки наших csv файлов в базу данных PostgreSql и в наше S3-хранилище)

### 4.1 Загрузка csv в PostgreSql
Ранее разработал скрипт load_to_postgres.py который загружает наши csv файлы из папки data в нашу базу данных PostgreSql
Выполняем
```yaml
python scripts/load_to_postgres.py
```

### 4.2 Проверка и работа с pgAdmin
Заходим в pgAdmin по ссылке **`http://localhost:5050`**.
Подключаемся к нашему серверу с данными из **`.env`** и проверяем наши таблицы на создание и заполнение

![pgadmin](https://github.com/user-attachments/assets/23598f5f-4601-4adb-865d-fa74e5bbe7a7)

### 4.3 Загрузка файлов в MinIO
Заходим в MInIO по ссылке **`http://localhost:9001`**.
Прописываем запуск нашего скрипта в терминал
```yaml
python scripts/uploads3.py
```

![minio](https://github.com/user-attachments/assets/2f255775-8b9a-4a79-9d1f-6f9ba465c9db)



## 5. Итог
* В результате у нас развернута среда с PostgreSQL, MinIO и pgAdmin в Docker Compose.
* Данные можно загружать в PostgreSQL и MinIO с помощью Python-скриптов.
* Лаб1 работа была успешно завершена!
  #### Такой подход подходит для проектов, где важно быстро развернуть инфраструктуру и наладить работу с данными. В дальнейшем можно дополнительно автоматизировать обработку загруженных данных и интегрировать систему в более сложные проекты.










