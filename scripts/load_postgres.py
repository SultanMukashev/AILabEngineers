import psycopg2
import pandas as pd


conn = psycopg2.connect(
    host="localhost",
    database="mydatabase",
    user="myuser",
    password="mypassword"
)
cur = conn.cursor()


df_users = pd.read_csv("./data/users.csv")
for _, row in df_users.iterrows():
    cur.execute("INSERT INTO users (id, name, email) VALUES (%s, %s, %s)", 
                (row["id"], row["name"], row["email"]))

df_orders = pd.read_csv("./data/orders.csv")
for _, row in df_orders.iterrows():
    cur.execute("INSERT INTO orders (id, user_id, amount) VALUES (%s, %s, %s)", 
                (row["id"], row["user_id"], row["amount"]))

conn.commit()
cur.close()
conn.close()