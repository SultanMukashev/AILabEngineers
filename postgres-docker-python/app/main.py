import os
import psycopg2
import time
import locale

# Force UTF-8 encoding
# DB connection details
host = os.environ.get("DB_HOST", "localhost")
dbname = os.environ.get("DB_NAME", "mydatabase")
user = os.environ.get("DB_USER", "dataminer0")
password = os.environ.get("DB_PASS", "dataminer01")

print(password)
try:
    conn = psycopg2.connect(
        dbname=dbname, user=user, password=password, host=host, port=5432
    )

    cur = conn.cursor()
    cur.execute("SELECT * FROM datacamp_courses;")
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    for row in rows:
        print(row)

except Exception as e:
    print("Error:", e)
