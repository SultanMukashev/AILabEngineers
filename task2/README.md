# 🧪 Лабораторная работа №2: Загрузка CSV в MinIO → PostgreSQL

## 📌 Цель работы

Настроить ETL-конвейер, передающий данные из CSV-файла `clean_krisha_kokshetau.csv`:

1. 📤 Загрузка файла в MinIO-объектное хранилище.
2. 📥 Загрузка этого файла из MinIO и вставка в таблицу PostgreSQL.
3. ⚙️ Поднятие инфраструктуры с помощью `docker-compose`.

---
## 🚀 Запуск пайплайна

### 📤 Шаг 1. Загрузка в MinIO

```bash
python scripts/upload_to_minio.py
```

✅ Скрипт подключается к MinIO и загружает файл в бакет `mybucket`.

---

### 📥 Шаг 2. Загрузка в PostgreSQL

```bash
python scripts/from_minio_upload_to_pg.py
```

✅ Скрипт скачивает файл из MinIO и вставляет данные в таблицу `apartments` (см. `init.sql`).

---

## ✅ Результат

- Таблица `apartments` создана и заполнена в базе PostgreSQL.
- CSV передан через MinIO без ошибок типов и форматирования.
- Весь пайплайн управляется Python-скриптами и `docker-compose`.

---


