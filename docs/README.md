# Отчёт о выполнении задания: PostgreSQL + S3-хранилище в Docker Compose

Этот документ описывает шаги, выполненные для развёртывания среды с PostgreSQL, MinIO и pgAdmin с помощью Docker Compose, а также автоматизацию загрузки данных.

---

## 1. Подготовительный этап

1. **Анализ требований:**  
   Изучил задание, определил, что нужно развернуть следующие сервисы:  
   - PostgreSQL с автоматической инициализацией через SQL-скрипты  
   - MinIO как S3-хранилище  
   - pgAdmin для управления PostgreSQL  
   - Скрипты на Python для загрузки CSV-файлов в PostgreSQL и файлов в MinIO

2. **Выбор инструментов и источников:**  
   Использовалось Docker Compose для упрощённого развёртывания. В качестве образов использовались официальные репозитории:
   - **Docker Hub:** [https://hub.docker.com/](https://hub.docker.com/)
   - **PostgreSQL на Docker Hub:** [https://hub.docker.com/_/postgres](https://hub.docker.com/_/postgres)
   - **pgAdmin на Docker Hub:** [https://hub.docker.com/r/dpage/pgadmin4](https://hub.docker.com/r/dpage/pgadmin4)

---

## 2. Разработка инфраструктуры

###  2.1. **Создание `docker-compose.yml`:** 
   
   - **Environment (Переменные окружения):** Все чувствительные данные, такие как имена пользователей и пароли, вынесены в файл .env. Это позволяет не хранить их непосредственно в docker-compose.yml и легко менять настройки без пересборки образов.
  
   - **Volumes (Тома):** Использование томов позволяет сохранять данные между перезапусками контейнеров. Например, ./pgdata хранит данные PostgreSQL, а ./s3data — файлы MinIO. Также можно монтировать инициализационные скрипты для автоматической настройки баз данных.
  
   - **Ports (Порты):**
    Проброс портов обеспечивает доступ к сервисам извне. Например, порт 5432 для PostgreSQL, 9000/9001 для MinIO и 8080 для pgAdmin.
  
  ```yml
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
    environment:
      MINIO_ROOT_USER: ${MINIO_ROOT_USER}    
      MINIO_ROOT_PASSWORD: ${MINIO_ROOT_PASSWORD}  
    command: server /data --console-address ":9001"  
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
      - "8080:80"              
```
### 2.2. **Подготовка файла `.env`:**  
Создал файл `.env` со следующими переменными:
   ```ini
   POSTGRES_USER=user
   POSTGRES_PASSWORD=password
   POSTGRES_DB=mydatabase

   MINIO_ROOT_USER=minioaccesskey
   MINIO_ROOT_PASSWORD=miniosecretkey

   PGADMIN_DEFAULT_EMAIL=admin@admin.com
   PGADMIN_DEFAULT_PASSWORD=admin
   ```
## 3. Развёртывание среды
### 3.1. Запуск контейнеров (Containers):
   
Выполнил команду для старта всех сервисов:
```console
docker-compose up -d
```
Docker Desktop:

!['Docker Desktop'](/docs/screenshots/docker.jpg)
### 3.2. Проверка статуса:
Убедился, что контейнеры запущены:
```console
docker ps
```
!['Terminal'](/docs/screenshots/terminal.jpg)

## 4. Автоматизация загрузки данных
### 4.1. Загрузка данных в PostgreSQL:
Разработал скрипт scripts/load_postgres.py, который считывает CSV-файлы (CSV files) из директории data и загружает их в базу данных.

Выполнил команду:
```console
python scripts/load_postgres.py
```
### 4.2. Работа с pgAdmin:
Открыл веб-интерфейс (Web Interface) по адресу `http://localhost:8080`

Выполнил тестовый SQL-запрос для проверки данных, например:
```sql
SELECT * FROM public.orders
ORDER BY id ASC;
```
!['PostreSQL'](/docs/screenshots/pgadmin-orders.jpg)

### 4.3. Загрузка файлов в S3 (MinIO):

Разработал скрипт scripts/upload_s3.py для загрузки случайных файлов в MinIO.

Запустил скрипт:
```python
python scripts/upload_s3.py
```
Проверил веб-интерфейс MinIO по адресу `http://localhost:9000` и проверил bucket который был создан до этого вручную 

!['MinIO'](/docs/screenshots/minio.jpg)

## 5. Документирование и итоговый отчёт

### 5.1 Скриншоты и документация:
- Сохранил все скриншоты (Docker Desktop, терминал, pgAdmin, MinIO) в папке docs/screenshots.
- В папке docs/technologies.md оформил краткий конспект изученных технологий (например, Docker, PostgreSQL, MinIO, Python).
### 5.2. Итог
В результате задания была успешно создана и протестирована контейнеризированная среда, позволяющая:

- Автоматически разворачивать PostgreSQL, MinIO и pgAdmin.
- Загружать данные в PostgreSQL и MinIO посредством скриптов на Python.
- Получать доступ к данным через удобный веб-интерфейс.

Также дополнительно настроен файл `.env` с необходимыми переменными для PostgreSQL, MinIO и pgAdmin.













