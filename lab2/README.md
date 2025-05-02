# Lab 2 – S3 → Postgres ETL with Docker

## 💡 Task overview
1. **Exercise 5 (SQL)** – write **`creatingtables.sql`** that creates all required tables in PostgreSQL (e.g. `products`, `accounts`, `transactions`, …).
2. Place the CSV files you produced in **Task 5** into the project’s **`data/`** folder.
3. Spin up the stack with Docker Compose:

   * **MinIO** – S3‑compatible object storage  
   * **PostgreSQL** – relational database  
   * **pipeline** – one‑shot container that  
     1. uploads the CSVs to MinIO,  
     2. downloads them back,  
     3. loads them into the tables created by `creatingtables.sql`.

```bash
# first run – build images, create DB schema, run ETL
docker compose up --build
```

Postgres & MinIO keep running.  
When you update the CSVs, re‑run only the ETL:

```bash
docker compose up -d pipeline
```

---

## 🗄️ Project layout

```
lab2/
├─ data/                    # <- your *.csv go here
│   ├─ products.csv
│   ├─ accounts.csv
│   └─ transactions.csv
│
├─ creatingtables.sql       # <- Task 5 DDL
│
├─ Dockerfile               # builds the pipeline image
├─ docker-compose.yml       # services: minio, postgres, pipeline
├─ .env                     # secrets & tweak‑able settings
│
├─ wait-for-it.sh           # tiny “wait host:port” helper
├─ upload_data.py           # 1️⃣ upload CSVs → MinIO
└─ load_to_postgres.py      # 2️⃣ download CSVs → Postgres
```

---

## ⚙️ Configuration (`.env`)

```dotenv
# ---------- MinIO ----------
MINIO_ROOT_USER=minioadmin
MINIO_ROOT_PASSWORD=minioadmin
S3_ENDPOINT=http://minio:9000
BUCKET=demo-bucket

# ---------- PostgreSQL ----------
POSTGRES_USER=demo
POSTGRES_PASSWORD=demo
POSTGRES_DB=demo

# ---------- CSV list (order matters!) ----------
CSV_FILES=products.csv,accounts.csv,transactions.csv
```

Docker Compose reads `.env` automatically.

---

## 🚀 Lifecycle

| Stage | Action |
|-------|--------|
| **Boot** | `docker compose up --build` starts MinIO & Postgres, waits until healthy, then launches **pipeline**. |
| **Schema** | On the very first run Postgres executes `creatingtables.sql` (mounted into `/docker-entrypoint-initdb.d`). |
| **Upload** | `upload_data.py` loops over `CSV_FILES` and puts each file into MinIO. |
| **Load** | `load_to_postgres.py` downloads each object, truncates (parents with `CASCADE`), then streams data into Postgres with `COPY`. |
| **Done** | `pipeline` exits; DB & MinIO keep running. |

---

## 🛠️ psql cheatsheet

```bash
docker compose exec postgres psql -U $POSTGRES_USER -d $POSTGRES_DB
```

| Command | Description |
|---------|-------------|
| `\dt` | list tables |
| `\d tablename` | describe table |
| `SELECT * FROM tablename LIMIT 10;` | peek at data |
| `\q` | quit |

---

## 🧩 Extend

* Add a new CSV/table:  
  1. Add DDL to `creatingtables.sql`.  
  2. Drop CSV into `data/`.  
  3. Append file name to `CSV_FILES` in `.env`.  
  4. Run `docker compose up -d pipeline`.

* For production‑grade migrations consider Alembic or Flyway.

Enjoy your Docker‑powered S3 → Postgres workflow!
