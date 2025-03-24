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
version: '3.8'

services:
  postgres:
    image: postgres:13
    container_name: postgres
    env_file:
      - .env-non-dev
    volumes:
      - ./pgdata:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
    ports:
      - "5432:5432"

  minio:
    image: minio/minio
    container_name: minio
    env_file:
      - .env-non-dev}
    command: server /data --console-address ":9001"
    volumes:
      - ./s3data:/data
    ports:
      - "9000:9000"
      - "9001:9001"

  pgadmin:
    image: dpage/pgadmin4
    container_name: pgadmin
    env_file:
      - .env-non-dev}
    ports:
      - "8080:80"
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
![alt text](image.png)

### 5.3 Подключение к PostgreSQL через pgAdmin

1. Открыть `http://localhost:8080`
2. Ввести учетные данные `admin@example.com / admin`
3. Добавить сервер PostgreSQL, используя `postgres` в качестве хоста

### 5.4 Проверка загрузки данных

```bash
psql -U admin -d mydatabase -h localhost -c "SELECT * FROM my_table;"

```

### 5.5 Проверка файлов в MinIO

1. Открыть `http://localhost:9001`
2. Войти с логином `minioadmin` и паролем `minioadmin`
3. Перейти в `my-bucket` и проверить наличие `backup.sql`
![alt text](image-1.png)
---

## Итог
- Развернута среда с PostgreSQL, MinIO и pgAdmin
- Настроены скрипты для загрузки данных в базу и хранилище
- Проверена работа автоматизированных процессов

Проект успешно выполнен!

