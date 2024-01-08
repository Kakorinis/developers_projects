import psycopg2
import csv
import os


# Устанавливаем подключение к серверу PostgreSQL
conn = psycopg2.connect(
    host= "localhost",#"0.0.0.0",#"db",
    port="5432",#"5432",
    user="postgres",
    password="1111",
    dbname="postgres"  # Имя базы данных по умолчанию postgres
)


conn.autocommit = True
cur = conn.cursor()
cur.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = 'ka_clients'")
exists = cur.fetchone()
if not exists:
    cur.execute("CREATE DATABASE ka_clients")

cur.close()
conn.close()

# Подключаемся к новой базе данных "ka_validation_data"
conn = psycopg2.connect(
    host="localhost",
    port="5432",
    user="postgres",
    password="1111",
    dbname="ka_clients" # Имя созданной базы данных
)

# Создаем таблицу в базе данных "ka_validation_data"
cur = conn.cursor()
cur.execute("DROP TABLE IF EXISTS all_clients")
cur.execute("""
    CREATE TABLE all_clients(
        id INTEGER,
        fullname TEXT COLLATE "C",
        phone TEXT
    )
""")

nums = [i for i in range(1000)]
fullname = []
while len(fullname) != 1000:
    for i in ['Иванов', 'Сидоров','Петров','Гришковец','Елесеенко','Кантемиров','Иваненко','Абрамов','Лукин','Ветров']:
        if len(fullname) == 1000:
            break
        for el in ['Иван','Петр','Сергей','Артем','Егор','Игорь','Ян','Миша','Яков','Андрей','Ислам','Хабиб','Артур','Батур']:
            fullname.append(i + ' ' + el)
            if len(fullname) == 1000:
                break
phone = ['79891960000' for i in range(996)] + ['79891968092', '79891968093', '79891968094', '79891968095']
#
for i in range(len(nums)):
    cur.execute("""
        INSERT INTO all_clients (id, fullname, phone)
        VALUES (%s, %s, %s)
    """, (nums[i], fullname[i], phone[i]))

# Сохранение изменений и закрытие соединения с базой данных
conn.commit()
conn.close()


