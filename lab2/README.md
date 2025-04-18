# Лабораторная работа №2: Конвейер MinIO -> PostgreSQL

## Задача

Реализовать передачу данных из файла CSV (`kolesa_almaty_cleaned.csv`):
1. Загрузить файл в бакет MinIO.
2. Загрузить данные из файла в MinIO в таблицу PostgreSQL (`lab2_kolesa_ads`), предварительно создав таблицу программно из Python, если она отсутствует.

## Содержимое папки `lab2`

* `upload_to_minio.py`: Скрипт для загрузки локального CSV в MinIO.
* `load_to_postgres.py`: Скрипт для создания таблицы в Postgres (если не существует), скачивания объекта из MinIO и загрузки данных в таблицу.
* `data/`: Папка с исходным файлом `kolesa_almaty_cleaned.csv`.

## Предварительные требования

* Запущенное Docker-окружение (PostgreSQL, MinIO), определенное в `docker-compose.yml` в корне проекта (`docker-compose up -d` из корня).
* Наличие файла `.env` в корне проекта с корректными настройками (`POSTGRES_DB`, `MINIO_BUCKET`, учетные данные).
* Установленные Python зависимости (например, `psycopg2-binary`, `boto3`, `python-dotenv`) в активном виртуальном окружении.
* Наличие исходного файла `lab2/data/kolesa_almaty_cleaned.csv`.

## Порядок запуска

Команды выполняются из **корневой директории проекта**:

1.  **Загрузка в MinIO:**
    ```bash
    # Активировать venv: source venv/bin/activate
    python lab2/upload_to_minio.py
    ```
    *(Объект будет сохранен как `lab2/kolesa_almaty_cleaned.csv` в бакете `nurassyl-bucket`)*

2.  **Загрузка в PostgreSQL:**
    ```bash
    # Активировать venv: source venv/bin/activate
    python lab2/load_to_postgres.py
    ```
    *(Скрипт создаст таблицу `lab2_kolesa_ads` в БД `nurassyl-db`, скачает объект из MinIO и вставит данные)*

## Конфигурация

Параметры подключения к БД и MinIO, имена базы и бакета читаются из файла `.env` в корне проекта. Имя целевой таблицы и ключ объекта S3 задаются в Python-скриптах.