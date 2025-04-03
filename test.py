import psycopg2
# conn.set_client_encoding('utf-8')

conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="postgres",
    host="localhost",
    port=5432
)
print(conn.encoding)
print("Connection successful")
