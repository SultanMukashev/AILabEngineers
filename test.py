# import os
# import psycopg2
# from dotenv import load_dotenv

# # ????????? ?????????? ????????? ?? .env ?????
# load_dotenv(dotenv_path='.env')

# # DB_CONFIG = {
# #     "host": os.getenv("POSTGRES_HOST"),
# #     "dbname": os.getenv("POSTGRES_DB"),
# #     "user": os.getenv("POSTGRES_USER"),
# #     "password": os.getenv("POSTGRES_PASSWORD"),
# #     "port": os.getenv("POSTGRES_PORT", 5432),
# # }

# host = os.getenv('POSTGRES_HOST',"postgres")
# port = os.getenv('POSTGRES_PORT', 12345)
# dbname = os.getenv('POSTGRES_DB',"postgres")
# user = os.getenv('POSTGRES_USER',"postgres")
# password = os.getenv('POSTGRES_PASSWORD',"postgres")


# # cur = conn.cursor()

# def get_connection():
#     # conn = psycopg2.connect(**DB_CONFIG)
#     # conn.set_client_encoding('utf-8')
    
#     # conn = psycopg2.connect(
#     #     host=host,
#     #     port=port,
#     #     dbname=dbname,
#     #     user=user,
#     #     password=password
#     # )
#     conn = psycopg2.connect(
#         host = "postgres",
#         port = 12345,
#         dbname = "postgres",
#         user = "postgres",
#         password = "postgres"
#     )
#     return conn

# conn = get_connection()
# print(conn.encoding)
# print("Connection successful")




import psycopg2
try:
    conn = psycopg2.connect(
        host="localhost", #bug was bcs of this mfcking host???????????????????????
        port=5432,
        dbname="qwe",  # default database
        user="qwe",    # default user
        password="qwe" # password set in the Docker command
    )
    print("Connected to PostgreSQL successfully!")
    conn.close()
except Exception as e:
    print("Connection failed:")
    print(e)

