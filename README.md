# Отчёт о выполнении задания: PostgreSQL + S3-хранилище в Docker Compose

Этот документ описывает шаги, выполненные для развёртывания среды с PostgreSQL, MinIO и pgAdmin с помощью Docker Compose, а также автоматизацию загрузки данных.

---

## 1. Подготовительный этап

### 1.1 Анализ требований

Для выполнения задачи необходимо развернуть следующие сервисы:
- **PostgreSQL** – реляционная база данных с автоматической инициализацией через SQL-скрипты.
- **MinIO** – S3-совместимое объектное хранилище.
- **pgAdmin** – веб-интерфейс для управления PostgreSQL.
- **Python-скрипты** – загрузка CSV-файлов в PostgreSQL и файлов в MinIO.

### 1.2 Выбор инструментов и источников

Использовалось **Docker Compose** для управления многоконтейнерной средой. В качестве образов использовались официальные репозитории:
- **PostgreSQL:** [https://hub.docker.com/_/postgres](https://hub.docker.com/_/postgres)
- **pgAdmin:** [https://hub.docker.com/r/dpage/pgadmin4](https://hub.docker.com/r/dpage/pgadmin4)
- **MinIO:** [https://hub.docker.com/r/minio/minio](https://hub.docker.com/r/minio/minio)

---

## 2. Разработка инфраструктуры

### 2.1 Создание `.env` для хранения переменных окружения

```ini
# Конфигурация PostgreSQL
POSTGRES_USER=smth
POSTGRES_PASSWORD=smth
POSTGRES_DB=smth

# Конфигурация MinIO
MINIO_ROOT_USER=smth
MINIO_ROOT_PASSWORD=smth

# Конфигурация pgAdmin
PGADMIN_DEFAULT_EMAIL=smth@smth.com
PGADMIN_DEFAULT_PASSWORD=smth
```

### 2.2 Создание `docker-compose.yml`

```yaml
services:
  postgres:
    image: postgres:16
    container_name: postgres_db
    restart: always
    env_file:
      - .env-non-dev
    ports:
      - "5433:5432"  # Проброс порта
    volumes:
      - ./pgdata:/var/lib/postgresql/data  # Хранилище данных на хосте
      - ./scripts:/docker-entrypoint-initdb.d  # Это монтирует папку scripts
    networks:
      - app-network

  pgadmin:
    image: dpage/pgadmin4
    container_name: pgadmin
    restart: always
    env_file:
      - .env-non-dev
    ports:
      - "5080:80"
    depends_on:
      - postgres
    networks:
      - app-network

  minio:
    image: minio/minio
    container_name: minio_storage
    command: server --console-address ":9001" /data
    env_file:
      - .env-non-dev
    ports:
      - "9000:9000"
      - "9001:9001"
    volumes:
      - ./s3data:/data
    networks:
      - app-network

networks:
  app-network:
    driver: bridge

```

---

## 3. Настройка PostgreSQL

### 3.1 Изменение `pg_hba.conf` для удобного подключения

Войти в контейнер PostgreSQL:
```bash
docker exec -it postgres bash
```

Открыть файл конфигурации:
```bash
vi /var/lib/postgresql/data/pg_hba.conf
```

Изменить настройки доступа:
```plaintext
host    all             all             0.0.0.0/0               trust
```

Перезапустить контейнер:
```bash
docker restart postgres
```

---

## 4. Автоматизация работы с базой данных

### 4.1 Скрипт для загрузки CSV-файла в PostgreSQL
load_postgres.py

### 4.2 Скрипт для загрузки файлов в MinIO
upload_s3.py

## 5. Запуск и тестирование

### 5.1 Запуск сервисов Docker Compose
```bash
docker-compose up -d
```

### 5.2 Проверка работающих контейнеров
```bash
docker ps
```
![image](https://github.com/user-attachments/assets/59ce7deb-2b02-4d3f-9ed5-f9e7bbe9f118)
![image](https://github.com/user-attachments/assets/631f0ec9-56cd-442f-ba9e-91aecae19116)

### 5.3 Подключение к PostgreSQL через pgAdmin

1. Открыть `http://localhost:8080`
2. Ввести учетные данные `admin@example.com / admin`
3. Добавить сервер PostgreSQL, используя `postgres` в качестве хоста

### 5.4 Проверка загрузки данных

```bash
psql -U admin -d mydatabase -h localhost -c "SELECT * FROM my_table;"
![image](https://github.com/user-attachments/assets/b9c60e7a-d90b-47b2-8d8d-74c369cf5355)

```

### 5.5 Проверка файлов в MinIO

1. Открыть `http://localhost:9001`
2. Войти с логином `minioadmin` и паролем `minioadmin`
3. Перейти в `my-bucket` и проверить наличие `backup.sql`
![image](https://github.com/user-attachments/assets/330df89d-2b74-42fa-832c-156cc448b0db)
---

## Итог
- Развернута среда с PostgreSQL, MinIO и pgAdmin
- Настроены скрипты для загрузки данных в базу и хранилище
- Проверена работа автоматизированных процессов

Проект успешно выполнен!

