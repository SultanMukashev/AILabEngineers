# 1. technologies

- docker compose
- postgresql
- minio
- pgadmin
- uv

# 2. how to run
## 2.1 install dependencies to run scripts

```sh
uv pip install
```

## 2.2 environment

rename .env.example to .env and configure

## 2.2 run docker in background

```sh
docker compose up -d
```

## 2.3 run scripts

```
uv run scripts/upload_s3.py && uv run scripts/load_postgres.py
```

# 3. test

## 3.1 test postgresql using

change command with respect to .env file
```sh
psql -d database -h localhost -p 5432 -U admin -c "select * from users;"
```

expected output:

 id |     name      |           email
----+---------------+---------------------------
  1 | John Doe      | john.doe@example.com
  2 | Jane Smith    | jane.smith@example.com
  3 | Michael Brown | michael.brown@example.com
  4 | Beket nur     | beket@gmail.com
  5 | Aisara Nur    | aisara@gmail.com
(5 rows)

## 3.2 test pgadmin

1. open http://localhost:5050 in your browser
2. use creditionals from .env file
3. connect to database, hostname=postgres

## 3.3 test minio

1. open http://localhost:9001 in your browser
2. use creditionals from .env file
3. check bucket 'bucket' if contains 'order.back.csv'
