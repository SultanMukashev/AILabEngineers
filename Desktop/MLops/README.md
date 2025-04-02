Проект: PostgreSQL + MinIO в Docker Compose
Описание
Этот проект разворачивает PostgreSQL, MinIO и pgAdmin в Docker Compose с кастомной конфигурацией.
Основные возможности:

Автоматическое развертывание PostgreSQL и MinIO в контейнерах

Импорт данных из CSV в PostgreSQL

Загрузка файлов в MinIO (S3-хранилище)

Визуализация данных через pgAdmin

Автоматический бэкап PostgreSQL в MinIO

Как запустить проект?
1️⃣ Создать .env файл (или использовать готовый)
2️⃣ Запустить Docker Compose

sh
Копировать
Редактировать
docker-compose up -d
3️⃣ Импортировать CSV в PostgreSQL

sh
Копировать
Редактировать
python scripts/load_postgres.py
4️⃣ Загрузить файлы в MinIO

sh
Копировать
Редактировать
python scripts/upload_s3.py
5️⃣ Открыть pgAdmin и MinIO в браузере:

pgAdmin: http://localhost:5050

MinIO: http://localhost:9001
