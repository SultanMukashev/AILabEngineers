# Lab 1 

## 📌 Описание проекта

Этот проект поднимает полностью контейнеризированную среду для работы с:
- 📦 **PostgreSQL** — реляционная база данных
- 🌐 **pgAdmin 4** — визуальный интерфейс для работы с PostgreSQL
- ☁️ **MinIO** — локальное S3-хранилище для документов, изображений и резервных копий

Также реализованы два Python-скрипта:
- `load_postgres.py` — загружает CSV-файлы в таблицы базы данных
- `upload_s3.py` — загружает локальные файлы (документы/изображения) в бакет MinIO

---

## ⚙️ Как запустить

### 1. Клонируй проект

```bash
git clone https://github.com/SultanMukashev/AILabEngineers
cd AILabEngineers/lab1
git checkout daniyal
 ```

### 2. Настрой .env

Создай файл .env:

POSTGRES_USER=daniyal
POSTGRES_PASSWORD=daniyal
POSTGRES_DB=labwork
POSTGRES_PORT=5432
PGADMIN_DEFAULT_EMAIL=admin@admin.com
PGADMIN_DEFAULT_PASSWORD=admin
PGADMIN_PORT=5050
MINIO_ROOT_USER=minioadmin
MINIO_ROOT_PASSWORD=minioadmin
MINIO_ENDPOINT=http://localhost:9000
MINIO_BUCKET=lab-bucket

### 3. Запусти сервисы
``` bash
docker-compose up -d
```

Проверь, что контейнеры работают:

docker ps
✅ Пример: ![Postgres Load](./Screenshot%20from%202025-04-03%2019-48-49.png)

Иницилизация данных при запуске контейнера
![Init db](./Screenshot%20from%202025-04-03%2019-48-23.png)
###  PostgreSQL

База данных labwork

Скрипт scripts/load_postgres.py загружает данные из:

    data/users.csv

    data/orders.csv

Запуск:
``` bash
python scripts/load_postgres.py
```

✅ Пример: ![Postgres Load](./Screenshot%20from%202025-04-03%2019-48-01.png)

📊 Просмотр в pgAdmin: ![pgAdmin Orders](./Screenshot%20from%202025-04-03%2020-10-05.png) 
![pgAdmin Users](./Screenshot%20from%202025-04-03%2020-10-20.png)
#### MinIO

Поднимается на http://localhost:9001

Скрипт scripts/upload_s3.py загружает файлы из data/images/ в бакет lab-bucket

Запуск:
```bash
python scripts/upload_s3.py
```

✅ Пример: ![MinIO Upload](./Screenshot%20from%202025-04-03%2020-08-37.png)
📸 Скриншоты контейнеров
📊 Просмотр в Minio: ![Minio bucket](./Screenshot%20from%202025-04-03%2020-10-53.png) 
