import psycopg2
import csv

# Подключаемся к базе данных PostgreSQL
conn = psycopg2.connect(
    host="localhost",  # Адрес сервера
    port="5432",  # Порт, на котором работает PostgreSQL
    dbname="your_database",  # Имя базы данных
    user="user",  # Имя пользователя
    password="password"  # Пароль
)

cur = conn.cursor()

# Открываем CSV файл и загружаем данные в таблицу
with open('./data/orders.csv', 'r') as file:
    reader = csv.reader(file)
    next(reader)  # Пропустить заголовок файла
    for row in reader:
        # Вставляем данные в таблицу
        cur.execute(
            "INSERT INTO example_table (name, value) VALUES (%s, %s)",
            (row[0], int(row[1]))
        )

conn.commit()  # Сохраняем изменения
cur.close()
conn.close()  # Закрываем соединение

